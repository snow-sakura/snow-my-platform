import fitz  # PyMuPDF
from typing import Optional


class FileHandler:
    """文件处理工具"""
    
    @staticmethod
    async def extract_text_from_pdf(file_content: bytes) -> str:
        """从PDF提取文本"""
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            raise ValueError(f"PDF解析失败: {str(e)}")
    
    @staticmethod
    async def extract_text_from_file(file_content: bytes, filename: str) -> str:
        """根据文件类型提取文本"""
        if filename.endswith('.pdf'):
            return await FileHandler.extract_text_from_pdf(file_content)
        elif filename.endswith('.txt'):
            return file_content.decode('utf-8')
        else:
            raise ValueError(f"不支持的文件类型: {filename}，仅支持PDF和TXT文件")
