# AI测试用例生成平台

一个AI驱动的测试用例生成平台,支持从PRD文档自动提取测试点并生成可执行的测试用例。

## 项目特性

- ✅ 多格式文档上传(PDF/DOCX/Markdown/YAML/CSV)
- ✅ AI自动提取PRD测试点
- ✅ AI自动生成测试用例
- ✅ RAG知识库管理 - 上传参考资料增强生成准确率
- ✅ 测试点/用例手动编辑与再生成
- ✅ 测试用例导出Excel
- ✅ 飞书Webhook通知
- ✅ 后台异步生成+批次任务追踪
- ✅ 系统设置持久化
- ✅ 自定义LLM API代理地址(支持硅基流动等第三方平台)

## 技术栈

### 后端
- **框架**: FastAPI (异步原生)
- **ORM**: SQLAlchemy 2.0 (async)
- **数据库**: MySQL 8.0+
- **向量数据库**: ChromaDB
- **LLM集成**: LiteLLM (支持OpenAI/Claude/DeepSeek等100+模型)
- **Embedding**: sentence-transformers (本地运行)
- **文档解析**: PyMuPDF, python-docx, pandas
- **迁移工具**: Alembic

### 前端
- **框架**: Vue 3 + Vite + TypeScript
- **UI组件库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+

### 后端启动

1. 进入后端目录
```bash
cd backend
```

2. 创建虚拟环境并安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件,配置数据库和LLM信息
```

4. 初始化数据库
```bash
# 方式1: 应用启动时自动创建表(开发模式)
# 方式2: 使用Alembic迁移
alembic upgrade head
```

5. 启动后端服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看API文档

### 前端启动

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

访问 http://localhost:5173

## 项目结构

```
snow-platform/
├── backend/                    # 后端代码
│   ├── app/
│   │   ├── api/               # API路由
│   │   │   ├── projects.py    # 项目管理API
│   │   │   ├── test_points.py # 测试点API
│   │   │   ├── test_cases.py  # 测试用例API
│   │   │   ├── knowledge_bases.py # 知识库API
│   │   │   ├── settings.py    # 系统设置API
│   │   │   └── batches.py     # 任务批次API
│   │   ├── core/              # 核心配置
│   │   │   ├── config.py      # 配置文件
│   │   │   └── database.py    # 数据库连接
│   │   ├── models/            # 数据模型
│   │   │   └── __init__.py    # SQLAlchemy模型
│   │   ├── schemas/           # Pydantic模式
│   │   │   └── __init__.py    # 请求/响应模式
│   │   ├── services/          # 业务逻辑
│   │   │   ├── document_parser.py  # 文档解析
│   │   │   ├── rag_service.py      # RAG服务
│   │   │   ├── llm_service.py      # LLM服务
│   │   │   ├── feishu_service.py   # 飞书通知
│   │   │   └── excel_exporter.py   # Excel导出
│   │   └── main.py            # 应用入口
│   ├── uploads/               # 上传文件目录
│   ├── knowledge_base/        # 知识库存储
│   ├── alembic/               # 数据库迁移
│   ├── requirements.txt       # Python依赖
│   └── .env.example           # 环境变量示例
│
└── frontend/                  # 前端代码
    ├── src/
    │   ├── api/               # API接口
    │   │   ├── project.ts     # 项目相关API
    │   │   └── test.ts        # 测试相关API
    │   ├── router/            # 路由配置
    │   ├── views/             # 页面组件
    │   │   ├── ProjectList.vue      # 项目列表
    │   │   ├── ProjectDetail.vue    # 项目详情
    │   │   ├── Documents.vue        # 文档管理
    │   │   ├── TestPoints.vue       # 测试点管理
    │   │   ├── TestCases.vue        # 测试用例
    │   │   ├── KnowledgeBases.vue   # 知识库管理
    │   │   └── Settings.vue         # 系统设置
    │   ├── utils/             # 工具函数
    │   ├── App.vue            # 根组件
    │   └── main.ts            # 入口文件
    ├── package.json
    ├── vite.config.ts
    └── tsconfig.json
```

## 使用流程

1. **创建项目**: 在首页点击"新建项目"
2. **上传文档**: 进入项目,上传PRD文档(支持PDF/DOCX/MD/YAML/CSV)
3. **提取测试点**: 点击"提取测试点",AI会自动分析文档
4. **校验测试点**: 在测试点页面查看和编辑AI提取的测试点
5. **生成测试用例**: 勾选测试点,点击"生成测试用例"
6. **查看和导出**: 在测试用例页面查看结果,可导出为Excel
7. **RAG增强** (可选): 在知识库管理上传历史Bug、业务经验等文档,提升生成质量
8. **配置通知** (可选): 在系统设置配置飞书Webhook,接收完成通知

## API文档

启动后端后访问: http://localhost:8000/docs

## 注意事项

1. 首次使用需要配置LLM API Key(支持OpenAI、Claude、DeepSeek等)
2. 使用本地Embedding模型时会下载约80MB的模型文件
3. 建议MySQL数据库字符集设置为utf8mb4
4. 生产环境请修改默认数据库密码

## License

MIT
