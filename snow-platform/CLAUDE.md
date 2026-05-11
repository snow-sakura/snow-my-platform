# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 常用命令

### 后端 (backend/)

```bash
# 激活虚拟环境
cd backend && source .venv/bin/activate

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 数据库迁移
alembic revision --autogenerate -m "描述"
alembic upgrade head
```

### 前端 (frontend/)

```bash
cd frontend && npm install
npm run dev     # 开发服务器 http://localhost:5173
npm run build   # 生产构建
```

### 环境配置

首次使用需复制 `backend/.env.example` 为 `backend/.env` 并配置：
- `DATABASE_URL`：MySQL连接串（默认用户 `snow`）
- `LLM_API_KEY` / `LLM_MODEL` / `LLM_BASE_URL`：大模型配置
- `FEISHU_WEBHOOK_URL`：飞书通知（可选）

## 架构概览

### 后端架构

- **FastAPI** 异步应用，入口 `app/main.py`
- **SQLAlchemy 2.0 async** ORM，数据库为 MySQL（驱动 aiomysql）
- **数据库模型**（`app/models/__init__.py`）：以 `Project` 为中心，关联 `Document`、`TestPoint`、`TestCase`、`KnowledgeBase`、`KnowledgeDocument`、`TaskBatch`、`SystemSettings`
- **Schema**（`app/schemas/__init__.py`）：Pydantic v2 模型，所有响应模型配置 `from_attributes = True`
- **API 路由**（`app/api/`）：按领域拆分，统一前缀 `/api/v1`

### 核心服务

- **`LLMService`**（`app/services/llm_service.py`）：通过 LiteLLM 调用大模型，支持 OpenAI/Claude/DeepSeek/硅基流动等。测试点提取和测试用例生成的 system prompt 均硬编码在此文件中，返回格式要求为 JSON 数组。
- **`RAGService`**（`app/services/rag_service.py`）：基于 ChromaDB 的向量存储。注意：当前 `generate_embedding` 使用简单哈希实现，非 sentence-transformers（依赖已安装但未接入）。
- **`DocumentParser`**（`app/services/document_parser.py`）：支持 PDF（PyMuPDF）、DOCX、Markdown、YAML、CSV。
- **异步任务**：测试点提取和测试用例生成使用 FastAPI `BackgroundTasks` 在后台执行，进度和状态通过 `TaskBatch` 表持久化。任务函数定义在对应的 API 路由文件中（`test_points.py`、`test_cases.py`）。

### 数据库与会话

- `app/core/database.py` 中 `get_db()` 依赖会自动处理 commit/rollback，路由函数中通常只需 `await db.flush()` + `await db.refresh()`。
- 应用启动时（`startup` 事件）会自动调用 `Base.metadata.create_all` 建表，开发环境无需手动执行 Alembic。
- Alembic 配置在 `alembic.ini`，`env.py` 会将 `+aiomysql` 转换为 `+pymysql` 以支持同步迁移。

### 前端架构

- **Vue 3 + Vite + TypeScript**，UI 使用 Element Plus（中文语言包）
- **状态管理**：Pinia
- **API 请求**：`src/api/` 下按领域封装，请求工具在 `src/utils/request`
- **代理配置**：`vite.config.ts` 中将 `/api` 代理到 `http://localhost:8000`

## 关键注意事项

- 修改 LLM prompt 时需注意保持 JSON 数组返回格式，否则 `json.loads` 会失败。
- `TestCase.steps` 在数据库中存储为 JSON 数组（`[{step, expected_result}]`），更新时需确保为字典列表。
- 上传文件保存到 `backend/uploads/`，知识库数据保存到 `backend/knowledge_base/`（含 ChromaDB 的 `chroma.sqlite3`），这两个目录由 `config.py` 在导入时自动创建。
- 飞书通知在异步任务完成后自动触发，失败不会阻断主流程。
