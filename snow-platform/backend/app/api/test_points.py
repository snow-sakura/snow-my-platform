from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import asyncio
from datetime import datetime

from app.core.database import get_db
from app.models import Project, Document, TestPoint, KnowledgeBase, TaskBatch
from app.schemas import TestPointCreate, TestPointResponse, TestPointUpdate, ExtractTestPointsRequest, TaskBatchResponse
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service
from app.services.feishu_service import feishu_service

router = APIRouter(prefix="/test-points", tags=["测试点管理"])


async def extract_test_points_task(batch_id: int, document_ids: List[int], 
                                   knowledge_base_ids: Optional[List[int]],
                                   project_id: int, project_name: str):
    """后台异步提取测试点任务"""
    from app.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        try:
            # 更新批次状态为运行中
            result = await db.execute(select(TaskBatch).where(TaskBatch.id == batch_id))
            batch = result.scalar_one()
            batch.status = "RUNNING"
            batch.started_at = datetime.utcnow()
            await db.flush()
            
            # 获取文档内容
            result = await db.execute(
                select(Document).where(Document.id.in_(document_ids))
            )
            documents = result.scalars().all()
            
            # 获取知识库上下文
            rag_context = ""
            if knowledge_base_ids:
                result = await db.execute(
                    select(KnowledgeBase).where(KnowledgeBase.id.in_(knowledge_base_ids))
                )
                knowledge_bases = result.scalars().all()

                for kb in knowledge_bases:
                    rag_context += f"\n知识库 [{kb.name}]:\n"
                    # 查询 ChromaDB 获取与文档内容相关的知识片段
                    try:
                        query_results = rag_service.query_documents(
                            kb.chroma_collection_name,
                            documents[0].content if documents else "",
                            n_results=3
                        )
                        for doc_text in query_results.get("documents", [[]])[0]:
                            rag_context += f"- {doc_text}\n"
                    except Exception:
                        pass
            
            total_docs = len(documents)
            completed = 0
            
            # 逐个文档提取测试点
            for doc in documents:
                if not doc.content:
                    continue
                
                try:
                    # 调用LLM提取测试点
                    test_points_data = await llm_service.extract_test_points(
                        doc.content,
                        rag_context if rag_context.strip() else None
                    )
                    
                    # 保存测试点到数据库
                    for tp_data in test_points_data:
                        test_point = TestPoint(
                            project_id=project_id,
                            document_id=doc.id,
                            title=tp_data.get('title', ''),
                            description=tp_data.get('description', ''),
                            priority=tp_data.get('priority', 'MEDIUM'),
                            category=tp_data.get('category', '')
                        )
                        db.add(test_point)
                    
                    completed += 1
                    batch.completed_count = completed
                    batch.progress = int((completed / total_docs) * 100)
                    await db.flush()
                    
                except Exception as e:
                    batch.error_message = f"文档 {doc.filename} 处理失败: {str(e)}"
                    await db.flush()
                    continue
            
            # 更新批次状态为完成
            batch.status = "COMPLETED"
            batch.completed_at = datetime.utcnow()
            batch.progress = 100
            await db.flush()
            
            # 发送飞书通知
            await feishu_service.notify_test_points_extracted(project_name, completed)
            
        except Exception as e:
            # 更新批次状态为失败
            result = await db.execute(select(TaskBatch).where(TaskBatch.id == batch_id))
            batch = result.scalar_one()
            batch.status = "FAILED"
            batch.error_message = str(e)
            batch.completed_at = datetime.utcnow()
            await db.flush()


@router.post("/extract")
async def extract_test_points(request: ExtractTestPointsRequest,
                             background_tasks: BackgroundTasks,
                             db: AsyncSession = Depends(get_db)):
    """提取测试点（异步）"""
    
    # 验证文档存在
    result = await db.execute(
        select(Document).where(Document.id.in_(request.document_ids))
    )
    documents = result.scalars().all()
    
    if not documents:
        raise HTTPException(status_code=404, detail="未找到指定的文档")
    
    project_id = documents[0].project_id
    
    # 获取项目信息
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one()
    
    # 创建任务批次
    batch = TaskBatch(
        project_id=project_id,
        task_type="extract_test_points",
        status="PENDING",
        total_count=len(documents)
    )
    db.add(batch)
    await db.flush()
    await db.refresh(batch)
    
    # 启动后台任务
    background_tasks.add_task(
        extract_test_points_task,
        batch.id,
        request.document_ids,
        request.knowledge_base_ids,
        project_id,
        project.name
    )
    
    return {"batch_id": batch.id, "message": "测试点提取任务已启动"}


@router.get("/project/{project_id}", response_model=List[TestPointResponse])
async def list_test_points(project_id: int, db: AsyncSession = Depends(get_db)):
    """获取项目的测试点列表"""
    result = await db.execute(
        select(TestPoint)
        .where(TestPoint.project_id == project_id)
        .order_by(TestPoint.created_at.desc())
    )
    test_points = result.scalars().all()
    return test_points


@router.put("/{test_point_id}", response_model=TestPointResponse)
async def update_test_point(test_point_id: int, update_data: TestPointUpdate,
                           db: AsyncSession = Depends(get_db)):
    """更新测试点"""
    result = await db.execute(select(TestPoint).where(TestPoint.id == test_point_id))
    test_point = result.scalar_one_or_none()
    
    if not test_point:
        raise HTTPException(status_code=404, detail="测试点不存在")
    
    if update_data.title is not None:
        test_point.title = update_data.title
    if update_data.description is not None:
        test_point.description = update_data.description
    if update_data.priority is not None:
        test_point.priority = update_data.priority
    if update_data.category is not None:
        test_point.category = update_data.category
    if update_data.is_verified is not None:
        test_point.is_verified = update_data.is_verified
        if update_data.is_verified:
            test_point.verified_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(test_point)
    return test_point


@router.delete("/{test_point_id}")
async def delete_test_point(test_point_id: int, db: AsyncSession = Depends(get_db)):
    """删除测试点"""
    result = await db.execute(select(TestPoint).where(TestPoint.id == test_point_id))
    test_point = result.scalar_one_or_none()

    if not test_point:
        raise HTTPException(status_code=404, detail="测试点不存在")

    await db.delete(test_point)
    return {"message": "测试点删除成功"}


@router.post("/", response_model=TestPointResponse)
async def create_test_point(create_data: TestPointCreate, project_id: int,
                            db: AsyncSession = Depends(get_db)):
    """手动创建测试点"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    test_point = TestPoint(
        project_id=project_id,
        title=create_data.title,
        description=create_data.description,
        priority=create_data.priority,
        category=create_data.category
    )
    db.add(test_point)
    await db.flush()
    await db.refresh(test_point)
    return test_point
