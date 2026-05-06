from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models import SystemSettings
from app.schemas import SystemSettingsCreate, SystemSettingsUpdate, SystemSettingsResponse
from app.core.config import settings

router = APIRouter(prefix="/settings", tags=["系统设置"])


@router.get("/", response_model=List[SystemSettingsResponse])
async def list_settings(db: AsyncSession = Depends(get_db)):
    """获取所有系统设置"""
    result = await db.execute(select(SystemSettings).order_by(SystemSettings.key))
    settings_list = result.scalars().all()
    return settings_list


@router.post("/", response_model=SystemSettingsResponse)
async def create_setting(setting_data: SystemSettingsCreate, db: AsyncSession = Depends(get_db)):
    """创建或更新系统设置"""
    
    # 检查是否已存在
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == setting_data.key)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.value = setting_data.value
        existing.description = setting_data.description
        await db.flush()
        await db.refresh(existing)
        return existing
    
    setting = SystemSettings(
        key=setting_data.key,
        value=setting_data.value,
        description=setting_data.description
    )
    
    db.add(setting)
    await db.flush()
    await db.refresh(setting)
    
    # 同步更新运行时配置
    update_runtime_config(setting_data.key, setting_data.value)
    
    return setting


@router.put("/{key}", response_model=SystemSettingsResponse)
async def update_setting(key: str, update_data: SystemSettingsUpdate,
                        db: AsyncSession = Depends(get_db)):
    """更新系统设置"""
    result = await db.execute(select(SystemSettings).where(SystemSettings.key == key))
    setting = result.scalar_one_or_none()
    
    if not setting:
        raise HTTPException(status_code=404, detail="配置项不存在")
    
    setting.value = update_data.value
    await db.flush()
    await db.refresh(setting)
    
    # 同步更新运行时配置
    update_runtime_config(key, update_data.value)
    
    return setting


@router.get("/{key}", response_model=SystemSettingsResponse)
async def get_setting(key: str, db: AsyncSession = Depends(get_db)):
    """获取单个系统设置"""
    result = await db.execute(select(SystemSettings).where(SystemSettings.key == key))
    setting = result.scalar_one_or_none()
    
    if not setting:
        raise HTTPException(status_code=404, detail="配置项不存在")
    
    return setting


def update_runtime_config(key: str, value: str):
    """更新运行时配置"""
    if key == "LLM_API_KEY":
        settings.LLM_API_KEY = value
    elif key == "LLM_MODEL":
        settings.LLM_MODEL = value
    elif key == "LLM_BASE_URL":
        settings.LLM_BASE_URL = value if value else None
    elif key == "FEISHU_WEBHOOK_URL":
        settings.FEISHU_WEBHOOK_URL = value if value else None
