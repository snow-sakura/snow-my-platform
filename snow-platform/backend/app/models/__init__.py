from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Project(Base):
    """项目表"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="项目名称")
    description = Column(Text, comment="项目描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    test_points = relationship("TestPoint", back_populates="project", cascade="all, delete-orphan")
    test_cases = relationship("TestCase", back_populates="project", cascade="all, delete-orphan")
    batches = relationship("TaskBatch", back_populates="project", cascade="all, delete-orphan")


class Document(Base):
    """文档表"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String(500), nullable=False, comment="文件名")
    file_path = Column(String(1000), nullable=False, comment="文件路径")
    file_type = Column(String(50), nullable=False, comment="文件类型: pdf/docx/md/yaml/csv")
    content = Column(Text, comment="解析后的文本内容")
    uploaded_at = Column(DateTime, default=datetime.utcnow, comment="上传时间")
    
    # 关系
    project = relationship("Project", back_populates="documents")


class KnowledgeBase(Base):
    """知识库表"""
    __tablename__ = "knowledge_bases"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="知识库名称")
    description = Column(Text, comment="知识库描述")
    chroma_collection_name = Column(String(200), nullable=False, unique=True, comment="Chroma集合名称")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    documents = relationship("KnowledgeDocument", back_populates="knowledge_base", cascade="all, delete-orphan")


class KnowledgeDocument(Base):
    """知识库文档表"""
    __tablename__ = "knowledge_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_base_id = Column(Integer, ForeignKey("knowledge_bases.id"), nullable=False)
    filename = Column(String(500), nullable=False, comment="文件名")
    file_path = Column(String(1000), nullable=False, comment="文件路径")
    file_type = Column(String(50), nullable=False, comment="文件类型")
    chunk_count = Column(Integer, default=0, comment="分块数量")
    uploaded_at = Column(DateTime, default=datetime.utcnow, comment="上传时间")
    
    # 关系
    knowledge_base = relationship("KnowledgeBase", back_populates="documents")


class TestPoint(Base):
    """测试点表"""
    __tablename__ = "test_points"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True, comment="来源文档ID")
    title = Column(String(500), nullable=False, comment="测试点标题")
    description = Column(Text, comment="测试点描述")
    priority = Column(String(20), default="MEDIUM", comment="优先级: HIGH/MEDIUM/LOW")
    category = Column(String(100), comment="分类")
    is_verified = Column(Boolean, default=False, comment="是否已校验")
    verified_by = Column(String(100), comment="校验人")
    verified_at = Column(DateTime, comment="校验时间")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    project = relationship("Project", back_populates="test_points")
    document = relationship("Document")
    test_cases = relationship("TestCase", back_populates="test_point", cascade="all, delete-orphan")


class TestCase(Base):
    """测试用例表"""
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    test_point_id = Column(Integer, ForeignKey("test_points.id"), nullable=False)
    case_number = Column(String(50), comment="用例编号")
    title = Column(String(500), nullable=False, comment="用例标题")
    precondition = Column(Text, comment="前置条件")
    steps = Column(JSON, comment="测试步骤: [{step, expected_result}]")
    expected_result = Column(Text, comment="预期结果")
    priority = Column(String(20), default="MEDIUM", comment="优先级")
    case_type = Column(String(50), comment="用例类型: 功能/性能/安全等")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    project = relationship("Project", back_populates="test_cases")
    test_point = relationship("TestPoint", back_populates="test_cases")


class TaskBatch(Base):
    """任务批次表 - 用于追踪异步任务"""
    __tablename__ = "task_batches"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    task_type = Column(String(50), nullable=False, comment="任务类型: extract_test_points/generate_test_cases")
    status = Column(String(20), default="PENDING", comment="状态: PENDING/RUNNING/COMPLETED/FAILED")
    progress = Column(Integer, default=0, comment="进度百分比")
    total_count = Column(Integer, default=0, comment="总数量")
    completed_count = Column(Integer, default=0, comment="已完成数量")
    error_message = Column(Text, comment="错误信息")
    started_at = Column(DateTime, comment="开始时间")
    completed_at = Column(DateTime, comment="完成时间")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    project = relationship("Project", back_populates="batches")


class SystemSettings(Base):
    """系统设置表"""
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, comment="配置键")
    value = Column(Text, comment="配置值")
    description = Column(Text, comment="配置描述")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
