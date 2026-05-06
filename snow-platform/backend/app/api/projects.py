from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.models import Project, Document, TestPoint, TestCase
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, DocumentResponse
from app.services.document_parser import DocumentParser

router = APIRouter(prefix="/projects", tags=["项目管理"])


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    """获取项目列表"""
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    projects = result.scalars().all()
    
    # 为每个项目添加统计信息
    projects_with_stats = []
    for project in projects:
        doc_count = await db.execute(
            select(func.count(Document.id)).where(Document.project_id == project.id)
        )
        tp_count = await db.execute(
            select(func.count(TestPoint.id)).where(TestPoint.project_id == project.id)
        )
        tc_count = await db.execute(
            select(func.count(TestCase.id)).where(TestCase.project_id == project.id)
        )
        
        project_dict = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "doc_count": doc_count.scalar() or 0,
            "test_point_count": tp_count.scalar() or 0,
            "test_case_count": tc_count.scalar() or 0
        }
        projects_with_stats.append(project_dict)
    
    return projects_with_stats


@router.post("/", response_model=ProjectResponse)
async def create_project(project_data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    """创建新项目"""
    project = Project(
        name=project_data.name,
        description=project_data.description
    )
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """获取项目详情"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project_data: ProjectUpdate, 
                        db: AsyncSession = Depends(get_db)):
    """更新项目信息"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description
    
    await db.flush()
    await db.refresh(project)
    return project


@router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """删除项目"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    await db.delete(project)
    return {"message": "项目删除成功"}


@router.post("/{project_id}/documents/upload", response_model=DocumentResponse)
async def upload_document(project_id: int, file: UploadFile = File(...),
                         db: AsyncSession = Depends(get_db)):
    """上传文档并解析"""
    
    # 验证项目存在
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 确定文件类型
    filename = file.filename or ""
    file_ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    supported_types = ['pdf', 'docx', 'md', 'markdown', 'yaml', 'yml', 'csv']
    if file_ext not in supported_types:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {file_ext}")
    
    # 保存文件
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join("uploads", unique_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # 解析文档
    try:
        parser = DocumentParser()
        parsed_content = await parser.parse_document(file_path, file_ext)
    except Exception as e:
        # 删除上传失败的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"文档解析失败: {str(e)}")
    
    # 保存文档记录
    document = Document(
        project_id=project_id,
        filename=filename,
        file_path=file_path,
        file_type=file_ext,
        content=parsed_content
    )
    
    db.add(document)
    await db.flush()
    await db.refresh(document)
    
    return document


@router.get("/{project_id}/documents", response_model=List[DocumentResponse])
async def list_documents(project_id: int, db: AsyncSession = Depends(get_db)):
    """获取项目的文档列表"""
    result = await db.execute(
        select(Document)
        .where(Document.project_id == project_id)
        .order_by(Document.uploaded_at.desc())
    )
    documents = result.scalars().all()
    return documents
