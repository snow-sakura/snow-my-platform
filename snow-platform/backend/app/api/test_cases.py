from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import asyncio
from datetime import datetime

from app.core.database import get_db
from app.models import Project, TestPoint, TestCase, KnowledgeBase, TaskBatch
from app.schemas import TestCaseResponse, TestCaseUpdate, GenerateTestCasesRequest, TaskBatchResponse
from app.services.llm_service import llm_service
from app.services.feishu_service import feishu_service
from app.services.excel_exporter import excel_exporter
from fastapi.responses import Response

router = APIRouter(prefix="/test-cases", tags=["测试用例管理"])


async def generate_test_cases_task(batch_id: int, test_point_ids: List[int],
                                   knowledge_base_ids: Optional[List[int]],
                                   project_id: int, project_name: str):
    """后台异步生成测试用例任务"""
    from app.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        try:
            # 更新批次状态为运行中
            result = await db.execute(select(TaskBatch).where(TaskBatch.id == batch_id))
            batch = result.scalar_one()
            batch.status = "RUNNING"
            batch.started_at = datetime.utcnow()
            await db.flush()
            
            # 获取测试点
            result = await db.execute(
                select(TestPoint).where(TestPoint.id.in_(test_point_ids))
            )
            test_points = result.scalars().all()
            
            total_points = len(test_points)
            completed = 0
            
            # 逐个测试点生成用例
            for tp in test_points:
                try:
                    test_point_data = {
                        'title': tp.title,
                        'description': tp.description,
                        'priority': tp.priority,
                        'category': tp.category
                    }
                    
                    # 调用LLM生成测试用例
                    test_cases_data = await llm_service.generate_test_cases(
                        test_point_data,
                        rag_context=None  # 可以添加RAG上下文
                    )
                    
                    # 保存测试用例到数据库
                    case_counter = 1
                    for case_data in test_cases_data:
                        test_case = TestCase(
                            project_id=project_id,
                            test_point_id=tp.id,
                            case_number=f"TC-{tp.id}-{case_counter}",
                            title=case_data.get('title', ''),
                            precondition=case_data.get('precondition', ''),
                            steps=case_data.get('steps', []),
                            expected_result=case_data.get('expected_result', ''),
                            priority=case_data.get('priority', 'MEDIUM'),
                            case_type=case_data.get('case_type', '')
                        )
                        db.add(test_case)
                        case_counter += 1
                    
                    completed += 1
                    batch.completed_count = completed
                    batch.progress = int((completed / total_points) * 100)
                    await db.flush()
                    
                except Exception as e:
                    batch.error_message = f"测试点 {tp.title} 处理失败: {str(e)}"
                    await db.flush()
                    continue
            
            # 更新批次状态为完成
            batch.status = "COMPLETED"
            batch.completed_at = datetime.utcnow()
            batch.progress = 100
            await db.flush()
            
            # 发送飞书通知
            await feishu_service.notify_test_cases_generated(project_name, completed)
            
        except Exception as e:
            # 更新批次状态为失败
            result = await db.execute(select(TaskBatch).where(TaskBatch.id == batch_id))
            batch = result.scalar_one()
            batch.status = "FAILED"
            batch.error_message = str(e)
            batch.completed_at = datetime.utcnow()
            await db.flush()


@router.post("/generate")
async def generate_test_cases(request: GenerateTestCasesRequest,
                             background_tasks: BackgroundTasks,
                             db: AsyncSession = Depends(get_db)):
    """生成测试用例（异步）"""
    
    # 验证测试点存在
    result = await db.execute(
        select(TestPoint).where(TestPoint.id.in_(request.test_point_ids))
    )
    test_points = result.scalars().all()
    
    if not test_points:
        raise HTTPException(status_code=404, detail="未找到指定的测试点")
    
    project_id = test_points[0].project_id
    
    # 获取项目信息
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one()
    
    # 创建任务批次
    batch = TaskBatch(
        project_id=project_id,
        task_type="generate_test_cases",
        status="PENDING",
        total_count=len(test_points)
    )
    db.add(batch)
    await db.flush()
    await db.refresh(batch)
    
    # 启动后台任务
    background_tasks.add_task(
        generate_test_cases_task,
        batch.id,
        request.test_point_ids,
        request.knowledge_base_ids,
        project_id,
        project.name
    )
    
    return {"batch_id": batch.id, "message": "测试用例生成任务已启动"}


@router.get("/project/{project_id}", response_model=List[TestCaseResponse])
async def list_test_cases(project_id: int, db: AsyncSession = Depends(get_db)):
    """获取项目的测试用例列表"""
    result = await db.execute(
        select(TestCase)
        .where(TestCase.project_id == project_id)
        .order_by(TestCase.created_at.desc())
    )
    test_cases = result.scalars().all()
    return test_cases


@router.get("/{test_case_id}", response_model=TestCaseResponse)
async def get_test_case(test_case_id: int, db: AsyncSession = Depends(get_db)):
    """获取测试用例详情"""
    result = await db.execute(select(TestCase).where(TestCase.id == test_case_id))
    test_case = result.scalar_one_or_none()
    
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    return test_case


@router.put("/{test_case_id}", response_model=TestCaseResponse)
async def update_test_case(test_case_id: int, update_data: TestCaseUpdate,
                          db: AsyncSession = Depends(get_db)):
    """更新测试用例"""
    result = await db.execute(select(TestCase).where(TestCase.id == test_case_id))
    test_case = result.scalar_one_or_none()
    
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    if update_data.title is not None:
        test_case.title = update_data.title
    if update_data.precondition is not None:
        test_case.precondition = update_data.precondition
    if update_data.steps is not None:
        test_case.steps = [step.dict() for step in update_data.steps]
    if update_data.expected_result is not None:
        test_case.expected_result = update_data.expected_result
    if update_data.priority is not None:
        test_case.priority = update_data.priority
    if update_data.case_type is not None:
        test_case.case_type = update_data.case_type
    
    await db.flush()
    await db.refresh(test_case)
    return test_case


@router.delete("/{test_case_id}")
async def delete_test_case(test_case_id: int, db: AsyncSession = Depends(get_db)):
    """删除测试用例"""
    result = await db.execute(select(TestCase).where(TestCase.id == test_case_id))
    test_case = result.scalar_one_or_none()
    
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    await db.delete(test_case)
    return {"message": "测试用例删除成功"}


@router.get("/export/{project_id}")
async def export_test_cases(project_id: int, db: AsyncSession = Depends(get_db)):
    """导出测试用例为Excel"""
    result = await db.execute(
        select(TestCase)
        .where(TestCase.project_id == project_id)
        .order_by(TestCase.created_at.asc())
    )
    test_cases = result.scalars().all()
    
    if not test_cases:
        raise HTTPException(status_code=404, detail="没有可导出的测试用例")
    
    # 转换为字典格式
    cases_data = []
    for case in test_cases:
        cases_data.append({
            'case_number': case.case_number,
            'title': case.title,
            'precondition': case.precondition,
            'steps': case.steps,
            'expected_result': case.expected_result,
            'priority': case.priority,
            'case_type': case.case_type
        })
    
    # 生成Excel
    excel_bytes = excel_exporter.export_test_cases(cases_data)
    
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=test_cases_{project_id}.xlsx"}
    )
