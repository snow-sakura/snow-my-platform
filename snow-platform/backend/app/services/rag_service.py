import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Optional
from loguru import logger
import uuid
import hashlib
import numpy as np
from app.core.config import settings


class RAGService:
    """RAG知识库服务"""
    
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(
            path=settings.KNOWLEDGE_BASE_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        logger.info("RAG服务初始化完成")
    
    def create_collection(self, collection_name: str) -> None:
        """创建知识库集合"""
        try:
            self.chroma_client.create_collection(
                name=collection_name,
                metadata={"description": f"Collection for {collection_name}"}
            )
            logger.info(f"知识库集合创建成功: {collection_name}")
        except Exception as e:
            logger.error(f"创建知识库集合失败: {e}")
            raise
    
    def delete_collection(self, collection_name: str) -> None:
        """删除知识库集合"""
        try:
            self.chroma_client.delete_collection(name=collection_name)
            logger.info(f"知识库集合删除成功: {collection_name}")
        except Exception as e:
            logger.error(f"删除知识库集合失败: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """生成简单的文本 embedding (基于哈希)"""
        dim = 384
        vector = np.zeros(dim)
        for i, char in enumerate(text):
            vector[i % dim] += ord(char)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.tolist()
    
    def add_documents(self, collection_name: str, texts: List[str], 
                     metadatas: Optional[List[dict]] = None) -> List[str]:
        """添加文档到知识库"""
        try:
            collection = self.chroma_client.get_collection(name=collection_name)
            
            # 生成embeddings
            embeddings = [self.generate_embedding(text) for text in texts]
            
            # 生成IDs
            ids = [str(uuid.uuid4()) for _ in texts]
            
            # 添加默认metadata
            if metadatas is None:
                metadatas = [{"source": "unknown"} for _ in texts]
            
            collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"成功添加 {len(texts)} 个文档到知识库: {collection_name}")
            return ids
        except Exception as e:
            logger.error(f"添加文档到知识库失败: {e}")
            raise
    
    def query_documents(self, collection_name: str, query_text: str, 
                       n_results: int = 5) -> dict:
        """查询相关文档"""
        try:
            collection = self.chroma_client.get_collection(name=collection_name)
            
            # 生成query embedding
            query_embedding = self.generate_embedding(query_text)
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            logger.info(f"知识库查询完成: {collection_name}, 返回 {len(results['documents'][0])} 条结果")
            return results
        except Exception as e:
            logger.error(f"知识库查询失败: {e}")
            raise
    
    def chunk_text(self, text: str, chunk_size: int = 500, 
                  overlap: int = 50) -> List[str]:
        """文本分块"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            
            # 尝试在句子边界分割
            if end < text_length:
                # 查找最近的句子结束符
                for sep in ['。', '！', '？', '.', '!', '?']:
                    last_sep = text.rfind(sep, start, end)
                    if last_sep != -1:
                        end = last_sep + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap if end < text_length else end
        
        logger.info(f"文本分块完成: {len(chunks)} 个块")
        return chunks


# 全局RAG服务实例
rag_service = RAGService()
