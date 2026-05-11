import os
import re
from typing import Optional
from loguru import logger


def _has_valid_chinese(text: str) -> bool:
    """检测文本是否有合理比例的中文字符，用于判断 PDF 提取是否乱码"""
    if not text.strip():
        return False
    # 统计 CJK 统一汉字 (U+4E00-U+9FFF)
    cjk_chars = len(re.findall(r'[一-鿿]', text))
    # 去除空白后的有效字符数
    non_space = len(re.sub(r'\s', '', text))
    if non_space == 0:
        return False
    # 如果 CJK 字符不足 30%，且文本长度超过阈值，判定为乱码
    ratio = cjk_chars / non_space
    return ratio >= 0.15 or non_space < 50


class DocumentParser:
    """文档解析器 - 支持PDF/DOCX/Markdown/YAML/CSV"""

    @staticmethod
    async def _ocr_pdf(file_path: str) -> str:
        """对 PDF 逐页 OCR 识别，用于处理缺少 ToUnicode CMap 的中文 PDF"""
        from pdf2image import convert_from_path
        import pytesseract

        images = convert_from_path(file_path, dpi=200)
        text_parts = []
        for i, img in enumerate(images):
            # chi_sim = 简体中文, eng = 英文
            page_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            if page_text.strip():
                text_parts.append(page_text)
        logger.info(f"OCR 解析完成: {file_path}, {len(images)} 页, 共 {sum(len(t) for t in text_parts)} 字符")
        return "\n\n".join(text_parts)

    @staticmethod
    async def parse_pdf(file_path: str) -> str:
        """解析PDF文件 - 直接提取 + 乱码检测 + OCR 降级"""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            text_parts = []

            for page in doc:
                page_text = page.get_text("text")
                if page_text.strip():
                    text_parts.append(page_text)

            doc.close()
            text = "\n\n".join(text_parts)

            # 乱码检测：macOS Quartz PDFContext 生成的 PDF 缺少 ToUnicode CMap
            # 提取出的中文字符会变成随机 Unicode 伪字符，用 CJK 字符比例判断
            if not _has_valid_chinese(text):
                logger.warning(f"PDF 文本疑似乱码（CJK字符比例过低），降级为 OCR: {file_path}")
                text = await DocumentParser._ocr_pdf(file_path)

            logger.info(f"PDF解析成功: {file_path}, 共 {len(text)} 字符")
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
