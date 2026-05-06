# 安装与配置手册

## 环境准备

### 必需环境

| 软件 | 版本要求 | 用途 |
|------|---------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 前端运行环境 |
| MySQL | 8.0+ | 数据库 |
| pip | 最新 | Python包管理 |
| npm | 9+ | Node包管理 |

### 检查环境

```bash
# 检查Python版本
python --version

# 检查Node.js版本
node --version

# 检查npm版本
npm --version

# 检查MySQL版本
mysql --version
```

---

## 后端安装

### 1. 进入后端目录

```bash
cd backend
```

### 2. 创建Python虚拟环境

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

**依赖说明:**
- `fastapi` - Web框架
- `sqlalchemy` - ORM数据库操作
- `litellm` - LLM模型调用(支持OpenAI/Claude/DeepSeek等)
- `chromadb` - 向量数据库(RAG知识库)
- `sentence-transformers` - 本地Embedding模型
- `pymupdf4llm` - PDF解析
- `python-docx` - Word文档解析

### 4. 创建MySQL数据库

```sql
CREATE DATABASE test_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 配置环境变量

```bash
# 复制配置示例
cp .env.example .env
```

编辑 `.env` 文件,配置以下参数:

```ini
# 数据库配置(修改用户名和密码)
DATABASE_URL=mysql+aiomysql://用户名:密码@localhost:3306/test_platform

# LLM配置(必须配置API Key)
LLM_API_KEY=sk-your-api-key-here
LLM_MODEL=gpt-4
# LLM_BASE_URL=https://api.siliconflow.cn/v1  # 可选,第三方平台

# 飞书Webhook(可选)
FEISHU_WEBHOOK_URL=

# CORS配置
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### 6. 初始化数据库

**方式1: 自动创建表(推荐开发使用)**
```bash
# 应用启动时会自动创建所有表,无需手动执行
```

**方式2: 使用Alembic迁移**
```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

### 7. 启动后端服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**启动参数说明:**
- `--reload` - 代码修改后自动重载(开发模式)
- `--host 0.0.0.0` - 监听所有网络接口
- `--port 8000` - 端口号

**验证启动:**
- 浏览器访问: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

---

## 前端安装

### 1. 进入前端目录

```bash
cd frontend
```

### 2. 安装依赖

```bash
npm install
```

**依赖说明:**
- `vue` - 前端框架
- `element-plus` - UI组件库
- `axios` - HTTP客户端
- `vue-router` - 路由管理
- `pinia` - 状态管理

### 3. 启动开发服务器

```bash
npm run dev
```

**启动参数:**
- 开发服务器运行在: http://localhost:5173
- 自动代理API请求到后端: http://localhost:8000

**构建生产版本:**
```bash
npm run build
```

---

## 配置说明

### LLM配置

#### OpenAI
```ini
LLM_API_KEY=sk-your-openai-key
LLM_MODEL=gpt-4
# 不需要配置 LLM_BASE_URL
```

#### 硅基流动(第三方平台)
```ini
LLM_API_KEY=sk-your-siliconflow-key
LLM_MODEL=Qwen/Qwen2.5-Coder-32B-Instruct
LLM_BASE_URL=https://api.siliconflow.cn/v1
```

#### DeepSeek
```ini
LLM_API_KEY=sk-your-deepseek-key
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com/v1
```

### 飞书Webhook配置

1. 在飞书中创建自定义机器人
2. 获取Webhook地址
3. 配置到 `.env`:

```ini
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx
```

### MySQL配置

**创建用户和数据库:**
```sql
CREATE USER 'test_platform'@'localhost' IDENTIFIED BY 'your_password';
CREATE DATABASE test_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON test_platform.* TO 'test_platform'@'localhost';
FLUSH PRIVILEGES;
```

**更新配置:**
```ini
DATABASE_URL=mysql+aiomysql://test_platform:your_password@localhost:3306/test_platform
```

---

## 常见问题

### Q1: pip安装litellm失败

**错误信息:**
```
ERROR: Could not find a version that satisfies the requirement litellm==1.28.5
```

**解决方案:**
litellm 1.28.5已被撤销,已更新至1.59.12,直接重新运行:
```bash
pip install -r requirements.txt
```

### Q2: MySQL连接失败

**错误信息:**
```
Can't connect to MySQL server
```

**检查步骤:**
1. MySQL服务是否启动: `mysql.server status`
2. 数据库是否存在: `mysql -u root -p -e "SHOW DATABASES;"`
3. 用户名密码是否正确

**启动MySQL(Mac):**
```bash
brew services start mysql
```

### Q3: Embedding模型下载慢

**现象:** 首次启动时会下载sentence-transformers模型(约80MB)

**解决方案:**
```python
# 修改 app/services/rag_service.py 中的模型路径
self.embedding_model = SentenceTransformer('nlpch/all-MiniLM-L6-v2')
# 或使用国内镜像
```

### Q4: 前端跨域问题

**错误信息:**
```
Access to XMLHttpRequest at 'xxx' from origin 'xxx' has been blocked
```

**解决方案:**
前端已通过vite.config.ts配置代理,确保后端端口为8000。如修改端口需同步更新:

```typescript
// frontend/vite.config.ts
proxy: {
  '/api': {
    target: 'http://localhost:8000',  // 修改为实际端口
    changeOrigin: true
  }
}
```

### Q5: 文件上传失败

**检查:**
1. uploads目录是否存在: `ls backend/uploads`
2. 目录权限: `chmod 755 backend/uploads`

**手动创建:**
```bash
cd backend
mkdir -p uploads knowledge_base
```

---

## 性能优化建议

### 数据库优化

```sql
-- 创建索引提高查询性能
CREATE INDEX idx_project_id ON test_points(project_id);
CREATE INDEX idx_project_id ON test_cases(project_id);
CREATE INDEX idx_knowledge_base_id ON knowledge_documents(knowledge_base_id);
```

### Embedding缓存

sentence-transformers会自动缓存模型到 `~/.cache/torch/sentence_transformers`,无需重复下载。

### 生产环境部署

1. **后端:**
```bash
# 使用gunicorn + uvicorn workers
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

2. **前端:**
```bash
npm run build
# 使用nginx部署dist目录
```

---

## 联系方式

如有问题,请查看:
- API文档: http://localhost:8000/docs
- 后端日志: `backend/logs/app.log`
- 浏览器控制台: F12 → Console
