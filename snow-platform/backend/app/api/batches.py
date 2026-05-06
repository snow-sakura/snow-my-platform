from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models import TaskBatch
from app.schemas import TaskBatchResponse

router = APIRouter(prefix="/batches", tags=["任务批次管理"])


@router.get("/", response_model=List[TaskBatchResponse])
async def list_batches(db: AsyncSession = Depends(get_db)):
    """获取所有任务批次"""
    result = await db.execute(select(TaskBatch).order_by(TaskBatch.created_at.desc()))
    batches = result.scalars().all()
    return batches


@router.get("/{batch_id}", response_model=TaskBatchResponse)
async def get_batch(batch_id: int, db: AsyncSession = Depends(get_db)):
    """获取任务批次详情"""
    result = await db.execute(select(TaskBatch).where(TaskBatch.id == batch_id))
    batch = result.scalar_one_or_none()
    
    if not batch:
        raise HTTPException(status_code=404, detail="任务批次不存在")
    
    return batch


@router.get("/project/{project_id}", response_model=List[TaskBatchResponse])
async def list_project_batches(project_id: int, db: AsyncSession = Depends(get_db)):
    """获取项目的任务批次列表"""
    result = await db.execute(
        select(TaskBatch)
        .where(TaskBatch.project_id == project_id)
        .order_by(TaskBatch.created_at.desc())
    )
    batches = result.scalars().all()
    return batches
