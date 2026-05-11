from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
import os

from app.core.database import get_db
from app.models import KnowledgeBase, KnowledgeDocument
from app.schemas import KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseResponse, KnowledgeDocumentResponse
from app.services.rag_service import rag_service
from app.services.document_parser import DocumentParser

router = APIRouter(prefix="/knowledge-bases", tags=["知识库管理"])


@router.get("/", response_model=List[KnowledgeBaseResponse])
async def list_knowledge_bases(db: AsyncSession = Depends(get_db)):
    """获取知识库列表"""
    result = await db.execute(select(KnowledgeBase).order_by(KnowledgeBase.created_at.desc()))
    knowledge_bases = result.scalars().all()
    return knowledge_bases


@router.post("/", response_model=KnowledgeBaseResponse)
async def create_knowledge_base(kb_data: KnowledgeBaseCreate, db: AsyncSession = Depends(get_db)):
    """创建知识库"""
    
    # 生成唯一的集合名称
    collection_name = f"kb_{uuid.uuid4().hex[:12]}"
    
    # 创建Chroma集合
    try:
        rag_service.create_collection(collection_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建知识库集合失败: {str(e)}")
    
    # 保存数据库记录
    knowledge_base = KnowledgeBase(
        name=kb_data.name,
        description=kb_data.description,
        chroma_collection_name=collection_name
    )
    
    db.add(knowledge_base)
    await db.flush()
    await db.refresh(knowledge_base)
    
    return knowledge_base


@router.put("/{kb_id}", response_model=KnowledgeBaseResponse)
async def update_knowledge_base(kb_id: int, kb_data: KnowledgeBaseUpdate,
                                db: AsyncSession = Depends(get_db)):
    """更新知识库"""
    result = await db.execute(select(KnowledgeBase).where(KnowledgeBase.id == kb_id))
    knowledge_base = result.scalar_one_or_none()
    if not knowledge_base:
        raise HTTPException(status_code=404, detail="知识库不存在")
    if kb_data.name is not None:
        knowledge_base.name = kb_data.name
    if kb_data.description is not None:
        knowledge_base.description = kb_data.description
    await db.flush()
    await db.refresh(knowledge_base)
    return knowledge_base


@router.delete("/{kb_id}")
async def delete_knowledge_base(kb_id: int, db: AsyncSession = Depends(get_db)):
    """删除知识库"""
    result = await db.execute(select(KnowledgeBase).where(KnowledgeBase.id == kb_id))
    knowledge_base = result.scalar_one_or_none()
    
    if not knowledge_base:
        raise HTTPException(status_code=404, detail="知识库不存在")
    
    # 删除Chroma集合
    try:
        rag_service.delete_collection(knowledge_base.chroma_collection_name)
    except Exception as e:
        print(f"删除Chroma集合失败: {e}")
    
    await db.delete(knowledge_base)
    return {"message": "知识库删除成功"}


@router.post("/{kb_id}/documents/upload")
async def upload_knowledge_document(kb_id: int, file: UploadFile = File(...),
                                   db: AsyncSession = Depends(get_db)):
    """上传知识库文档"""
    
    # 验证知识库存在
    result = await db.execute(select(KnowledgeBase).where(KnowledgeBase.id == kb_id))
    knowledge_base = result.scalar_one_or_none()
    
    if not knowledge_base:
        raise HTTPException(status_code=404, detail="知识库不存在")
    
    # 确定文件类型
    filename = file.filename or ""
    file_ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    supported_types = ['pdf', 'docx', 'md', 'markdown', 'yaml', 'yml', 'csv', 'txt']
    if file_ext not in supported_types:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {file_ext}")
    
    # 保存文件
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join("knowledge_base", unique_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # 解析文档
    try:
        parser = DocumentParser()
        parsed_content = await parser.parse_document(file_path, file_ext)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"文档解析失败: {str(e)}")
    
    # 文本分块
    chunks = rag_service.chunk_text(parsed_content)
    
    # 添加到ChromaDB
    try:
        rag_service.add_documents(
            knowledge_base.chroma_collection_name,
            chunks,
            [{"source": filename, "kb_id": kb_id} for _ in chunks]
        )
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"添加到知识库失败: {str(e)}")
    
    # 保存文档记录
    document = KnowledgeDocument(
        knowledge_base_id=kb_id,
        filename=filename,
        file_path=file_path,
        file_type=file_ext,
        chunk_count=len(chunks)
    )
    
    db.add(document)
    await db.flush()
    await db.refresh(document)
    
    return {"message": "文档上传成功", "chunk_count": len(chunks), "document": document}


@router.get("/{kb_id}/documents", response_model=List[KnowledgeDocumentResponse])
async def list_knowledge_documents(kb_id: int, db: AsyncSession = Depends(get_db)):
    """获取知识库的文档列表"""
    result = await db.execute(
        select(KnowledgeDocument)
        .where(KnowledgeDocument.knowledge_base_id == kb_id)
        .order_by(KnowledgeDocument.uploaded_at.desc())
    )
    documents = result.scalars().all()
    return documents
