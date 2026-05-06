"""
数据初始化脚本 - 批量生成测试数据
"""
import asyncio
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.core.database import engine, AsyncSessionLocal, Base
from app.models import Project, Document, TestPoint, TestCase, TaskBatch


async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_projects(db: AsyncSession):
    """创建项目"""
    projects_data = [
        {"name": "测试项目2-功能1", "description": None},
        {"name": "测试项目1-功能1", "description": None},
        {"name": "测试项目1-功能3", "description": None},
        {"name": "测试项目1-功能2", "description": None},
        {"name": "测试项目6", "description": "112"},
        {"name": "测试55555121", "description": "这里是项目描述"},
        {"name": "测试项目3", "description": None},
    ]
    
    projects = []
    for data in projects_data:
        project = Project(
            name=data["name"],
            description=data["description"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(project)
        await db.flush()
        await db.refresh(project)
        projects.append(project)
    
    await db.commit()
    return projects


async def create_documents(db: AsyncSession, projects: list):
    """创建文档"""
    documents = []
    for project in projects:
        # 每个项目创建1个文档
        doc = Document(
            project_id=project.id,
            filename=f"{project.name}_PRD_V1.0.md",
            file_path=f"uploads/{project.name}_PRD_V1.0.md",
            file_type="md",
            content=f"# {project.name}\n\n这是一个测试项目的产品需求文档。\n\n## 功能描述\n\n...",
            uploaded_at=datetime.now()
        )
        db.add(doc)
        await db.flush()
        await db.refresh(doc)
        documents.append(doc)
    
    await db.commit()
    return documents


async def create_test_points(db: AsyncSession, projects: list, documents: list):
    """创建测试点"""
    test_points_data = {
        "测试项目2-功能1": {
            "count": 44,
            "priorities": ["P0"] * 15 + ["P1"] * 20 + ["P2"] * 9,
            "categories": ["功能"] * 35 + ["边界"] * 9,
        },
        "测试项目1-功能1": {
            "count": 37,
            "priorities": ["P0"] * 12 + ["P1"] * 15 + ["P2"] * 10,
            "categories": ["功能"] * 28 + ["边界"] * 9,
        },
        "测试项目1-功能3": {
            "count": 43,
            "priorities": ["P0"] * 14 + ["P1"] * 18 + ["P2"] * 11,
            "categories": ["功能"] * 34 + ["边界"] * 9,
        },
        "测试项目1-功能2": {
            "count": 416,
            "priorities": ["P0"] * 139 + ["P1"] * 166 + ["P2"] * 111,
            "categories": ["功能"] * 333 + ["边界"] * 83,
        },
        "测试项目6": {
            "count": 26,
            "priorities": ["P0"] * 9 + ["P1"] * 10 + ["P2"] * 7,
            "categories": ["功能"] * 20 + ["边界"] * 6,
        },
        "测试55555121": {
            "count": 100,
            "priorities": ["P0"] * 33 + ["P1"] * 40 + ["P2"] * 27,
            "categories": ["功能"] * 80 + ["边界"] * 20,
        },
        "测试项目3": {
            "count": 26,
            "priorities": ["P0"] * 9 + ["P1"] * 10 + ["P2"] * 7,
            "categories": ["功能"] * 20 + ["边界"] * 6,
        },
    }
    
    all_test_points = []
    for project in projects:
        config = test_points_data[project.name]
        for i in range(config["count"]):
            test_point = TestPoint(
                project_id=project.id,
                document_id=documents[projects.index(project)].id,
                title=f"{project.name}-测试点{i+1}",
                description=f"验证{project.name}的功能点{i+1}",
                priority=config["priorities"][i] if i < len(config["priorities"]) else "P1",
                category=config["categories"][i] if i < len(config["categories"]) else "功能",
                is_verified=True,
                verified_by="测试员",
                verified_at=datetime.now(),
                created_at=datetime.now()
            )
            db.add(test_point)
            if (i + 1) % 100 == 0:  # 每100条提交一次
                await db.commit()
            await db.flush()
            all_test_points.append(test_point)
    
    await db.commit()
    return all_test_points


async def create_test_cases(db: AsyncSession, projects: list, test_points: list):
    """创建测试用例"""
    test_cases_data = {
        "测试项目2-功能1": 131,
        "测试项目1-功能1": 39,
        "测试项目1-功能3": 17,
        "测试项目1-功能2": 23,
        "测试项目6": 0,
        "测试55555121": 0,
        "测试项目3": 14,
    }
    
    # 按项目分组测试点
    project_test_points = {}
    for tp in test_points:
        if tp.project_id not in project_test_points:
            project_test_points[tp.project_id] = []
        project_test_points[tp.project_id].append(tp)
    
    all_test_cases = []
    for project in projects:
        count = test_cases_data[project.name]
        project_tps = project_test_points.get(project.id, [])
        
        for i in range(count):
            test_point = project_tps[i % len(project_tps)] if project_tps else None
            test_case = TestCase(
                project_id=project.id,
                test_point_id=test_point.id if test_point else 1,
                case_number=f"TC-{project.id}-{i+1:03d}",
                title=f"{project.name}-测试用例{i+1}",
                precondition="系统已登录",
                steps=[
                    {"step": f"步骤1", "expected_result": f"预期结果1"},
                    {"step": f"步骤2", "expected_result": f"预期结果2"},
                ],
                expected_result="功能正常",
                priority="P0" if i < count * 0.3 else "P1" if i < count * 0.7 else "P2",
                case_type="功能",
                created_at=datetime.now()
            )
            db.add(test_case)
            if (i + 1) % 50 == 0:
                await db.commit()
            await db.flush()
            all_test_cases.append(test_case)
    
    await db.commit()
    return all_test_cases


async def seed_data():
    """执行数据初始化"""
    print("开始初始化数据...")
    
    async with AsyncSessionLocal() as db:
        # 1. 创建项目
        print("创建项目...")
        projects = await create_projects(db)
        print(f"✓ 创建了 {len(projects)} 个项目")
        
        # 2. 创建文档
        print("创建文档...")
        documents = await create_documents(db, projects)
        print(f"✓ 创建了 {len(documents)} 个文档")
        
        # 3. 创建测试点
        print("创建测试点（可能需要几分钟）...")
        test_points = await create_test_points(db, projects, documents)
        print(f"✓ 创建了 {len(test_points)} 个测试点")
        
        # 4. 创建测试用例
        print("创建测试用例（可能需要几分钟）...")
        test_cases = await create_test_cases(db, projects, test_points)
        print(f"✓ 创建了 {len(test_cases)} 个测试用例")
    
    print("\n数据初始化完成！")
    print("\n数据统计：")
    for project in projects:
        print(f"  - {project.name}: 1 文档, {test_cases_data.get(project.name, 0)} 测试点")


# 测试用例数量配置（用于统计输出）
test_cases_data = {
    "测试项目2-功能1": 131,
    "测试项目1-功能1": 39,
    "测试项目1-功能3": 17,
    "测试项目1-功能2": 23,
    "测试项目6": 0,
    "测试55555121": 0,
    "测试项目3": 14,
}


if __name__ == "__main__":
    asyncio.run(seed_data())
