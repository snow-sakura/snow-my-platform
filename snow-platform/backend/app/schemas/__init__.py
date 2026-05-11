from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 项目相关Schema
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 文档相关Schema
class DocumentResponse(BaseModel):
    id: int
    project_id: int
    filename: str
    file_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class DocumentDetailResponse(BaseModel):
    id: int
    project_id: int
    filename: str
    file_type: str
    content: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True


# 测试点相关Schema
class TestPointCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "MEDIUM"
    category: Optional[str] = None


class TestPointUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    is_verified: Optional[bool] = None


class TestPointResponse(BaseModel):
    id: int
    project_id: int
    document_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: str
    category: Optional[str] = None
    is_verified: bool
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# 测试用例相关Schema
class TestCaseStep(BaseModel):
    step: str
    expected_result: str


class TestCaseCreate(BaseModel):
    test_point_id: int
    title: str
    precondition: Optional[str] = None
    steps: List[TestCaseStep] = []
    expected_result: Optional[str] = None
    priority: str = "MEDIUM"
    case_type: Optional[str] = None


class TestCaseUpdate(BaseModel):
    title: Optional[str] = None
    precondition: Optional[str] = None
    steps: Optional[List[TestCaseStep]] = None
    expected_result: Optional[str] = None
    priority: Optional[str] = None
    case_type: Optional[str] = None


class TestCaseResponse(BaseModel):
    id: int
    project_id: int
    test_point_id: int
    case_number: Optional[str] = None
    title: str
    precondition: Optional[str] = None
    steps: Optional[List[dict]] = None
    expected_result: Optional[str] = None
    priority: str
    case_type: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# 知识库相关Schema
class KnowledgeBaseCreate(BaseModel):
    name: str
    description: Optional[str] = None


class KnowledgeBaseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class KnowledgeBaseResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    chroma_collection_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class KnowledgeDocumentResponse(BaseModel):
    id: int
    knowledge_base_id: int
    filename: str
    file_type: str
    chunk_count: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


# 任务批次相关Schema
class TaskBatchResponse(BaseModel):
    id: int
    project_id: int
    task_type: str
    status: str
    progress: int
    total_count: int
    completed_count: int
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# 系统设置相关Schema
class SystemSettingsCreate(BaseModel):
    key: str
    value: str
    description: Optional[str] = None


class SystemSettingsUpdate(BaseModel):
    value: str


class SystemSettingsResponse(BaseModel):
    id: int
    key: str
    value: str
    description: Optional[str] = None
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 请求Schema
class ExtractTestPointsRequest(BaseModel):
    document_ids: List[int]
    knowledge_base_ids: Optional[List[int]] = None


class GenerateTestCasesRequest(BaseModel):
    test_point_ids: List[int]
    knowledge_base_ids: Optional[List[int]] = None
