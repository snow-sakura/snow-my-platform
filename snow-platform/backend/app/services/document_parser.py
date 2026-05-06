import os
from typing import Optional
from loguru import logger


class DocumentParser:
    """文档解析器 - 支持PDF/DOCX/Markdown/YAML/CSV"""
    
    @staticmethod
    async def parse_pdf(file_path: str) -> str:
        """解析PDF文件"""
        try:
            import pymupdf4llm
            text = pymupdf4llm.to_markdown(file_path)
            logger.info(f"PDF解析成功: {file_path}")
            return text
        except Exception as e:
            logger.error(f"PDF解析失败: {e}")
            raise
    
    @staticmethod
    async def parse_docx(file_path: str) -> str:
        """解析DOCX文件"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            logger.info(f"DOCX解析成功: {file_path}")
            return text
        except Exception as e:
            logger.error(f"DOCX解析失败: {e}")
            raise
    
    @staticmethod
    async def parse_markdown(file_path: str) -> str:
        """解析Markdown文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Markdown解析成功: {file_path}")
            return text
        except Exception as e:
            logger.error(f"Markdown解析失败: {e}")
            raise
    
    @staticmethod
    async def parse_yaml(file_path: str) -> str:
        """解析YAML文件"""
        try:
            import yaml
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            text = str(data)
            logger.info(f"YAML解析成功: {file_path}")
            return text
        except Exception as e:
            logger.error(f"YAML解析失败: {e}")
            raise
    
    @staticmethod
    async def parse_csv(file_path: str) -> str:
        """解析CSV文件"""
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            text = df.to_string()
            logger.info(f"CSV解析成功: {file_path}")
            return text
        except Exception as e:
            logger.error(f"CSV解析失败: {e}")
            raise
    
    @classmethod
    async def parse_document(cls, file_path: str, file_type: str) -> str:
        """根据文件类型解析文档"""
        parsers = {
            'pdf': cls.parse_pdf,
            'docx': cls.parse_docx,
            'md': cls.parse_markdown,
            'markdown': cls.parse_markdown,
            'yaml': cls.parse_yaml,
            'yml': cls.parse_yaml,
            'csv': cls.parse_csv,
        }
        
        parser = parsers.get(file_type.lower())
        if not parser:
            raise ValueError(f"不支持的文件类型: {file_type}")
        
        return await parser(file_path)
