# AI 测试用例协作助手 - 多智能体前后端分离项目

基于 FastAPI 和 React 的 AI 测试用例协作助手，支持多智能体团队协作和 SSE 流式输出。

## 项目结构

```
.
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── components/      # React 组件
│   │   ├── pages/          # 页面组件
│   │   ├── styles/         # 样式文件
│   │   ├── services/       # API 服务
│   │   ├── hooks/          # 自定义 Hooks
│   │   ├── App.jsx         # 主应用组件
│   │   └── main.jsx        # 入口文件
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   └── services/       # 业务服务
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── example/                 # 示例代码
│   ├── multi_agent.py      # 多智能体协作示例
│   └── openai_singleton.py # OpenAI 客户端配置
└── README.md
```

## 功能特性

- ✅ 现代化 UI 设计，参考 Gemini 和智谱风格
- ✅ **多智能体团队协作**：测试用例设计师、评审师、用户评审
- ✅ 支持 SSE 实时流式输出
- ✅ 基于 AutoGen 0.7.5 的多智能体对话能力
- ✅ 响应式设计，支持移动端
- ✅ Markdown 内容渲染
- ✅ 智能体角色标识和彩色显示
- ✅ 实时显示当前智能体输出状态

## 多智能体协作流程

本项目实现了完整的多智能体协作流程：

1. **测试用例设计师 (primary)**：根据用户需求生成详细的测试用例
2. **测试用例评审师 (critic)**：对生成的测试用例进行系统性评审，指出问题并提供改进建议
3. **用户评审 (user)**：根据评审结果决定是否接受或需要重新设计

整个流程通过 AutoGen 的 RoundRobinGroupChat 实现，支持流式输出，用户可以实时看到每个智能体的输出。

## 快速开始

### 前端设置

```bash
cd frontend
npm install
npm run dev
```

前端将在 `http://localhost:3000` 启动。

### 后端设置

1. 安装依赖：
```bash
cd backend
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，设置你的 API 密钥
```

环境变量示例：
```env
AUTOGEN_API_KEY=your-api-key-here
AUTOGEN_MODEL=Qwen/Qwen2.5-7B-Instruct
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
```

3. 启动服务：
```bash
python main.py
# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 `http://localhost:8000` 启动。

### 一键启动

```bash
chmod +x start-dev.sh
./start-dev.sh
```

## 使用示例

在聊天界面输入测试需求，例如：

> 设计一个登录功能的测试用例，字段：手机号（11位数字，非空）、密码（6-16位字母数字，非空）。点击登录后，校验手机号密码，正确则跳转首页，错误则提示"账号或密码错误"。连续错误5次锁定账号15分钟。

系统将自动启动多智能体协作流程：
1. 测试用例设计师生成测试用例
2. 测试用例评审师进行评审
3. 用户评审接受结果并输出最终测试用例

## 环境要求

- Node.js >= 16
- Python >= 3.9
- npm >= 8

## API 端点

- `POST /api/chat/stream` - SSE 流式聊天（多智能体协作）
- `POST /api/chat/message` - 非流式聊天
- `GET /health` - 健康检查

## 技术栈

### 前端
- React 18
- Vite
- React Markdown
- CSS3 + Flexbox

### 后端
- FastAPI
- Uvicorn
- AutoGen 0.7.5 (autogen-agentchat, autogen-ext)
- SSE-Starlette
- Pydantic

### AI 模型
- SiliconFlow API
- Qwen/Qwen2.5-7B-Instruct

## 开发说明

### 前端开发

前端使用 Vite 进行构建，支持热更新。所有组件位于 `frontend/src/components/` 目录。

多智能体协作的前端处理：
- 实时解析智能体角色标记（【测试用例设计师】、【测试用例评审师】、【用户评审】）
- 彩色标识不同智能体的输出
- 显示当前正在输出的智能体状态

### 后端开发

后端遵循 FastAPI 项目结构规范：
- `app/api/` - API 路由
- `app/core/` - 配置文件
- `app/services/` - 业务逻辑（多智能体团队协作）
- `app/models/` - 数据模型

多智能体实现：
- 使用 `RoundRobinGroupChat` 实现智能体轮流输出
- 使用 `SourceMatchTermination` 控制协作结束条件
- 使用 `run_stream()` 方法实现真正的流式输出

### 示例代码

参考 `example/` 目录下的示例代码：
- `multi_agent.py`：完整的多智能体协作示例
- `openai_singleton.py`：OpenAI 客户端配置

## 注意事项

1. 首次使用前需要配置 API 密钥（支持 SiliconFlow）
2. 确保使用 AutoGen 0.7.5 版本（autogen-agentchat, autogen-ext）
3. 前端代理配置在 `vite.config.js` 中
4. 多智能体协作需要完整的网络连接到 AI API

## License

MIT
