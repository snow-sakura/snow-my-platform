# AI Chat Assistant - 前后端分离项目

基于 FastAPI 和 React 的 AI 聊天助手项目，支持 SSE 流式输出，使用 AutoGen 0.7.5 和 Qwen 模型。

## 项目结构

```
.
├── frontend/                 # 前端项目 (React + Vite)
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
├── backend/                 # 后端项目 (FastAPI + AutoGen)
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   └── services/       # 业务服务
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
├── example/                # AutoGen 示例代码
│   ├── openai_singleton.py
│   ├── openai_model_client.py
│   ├── multi_agent.py
│   └── autogen_chat.py
├── start.sh               # 一键启动脚本
├── start-dev.sh           # 开发环境设置
└── README.md
```

## 功能特性

### 前端特性
- ✅ 现代化 UI 设计，参考 Gemini 和智谱风格
- ✅ 浅色主题 (#F4F6F8 背景，白色容器)
- ✅ 支持 SSE 实时流式输出
- ✅ 响应式设计，支持移动端
- ✅ Markdown 内容渲染
- ✅ 打字机动画效果
- ✅ 实时滚动到最新消息

### 后端特性
- ✅ 基于 AutoGen 0.7.5 的 AI 对话能力
- ✅ 真正的流式输出（逐 token/字符）
- ✅ 支持 SiliconFlow API (Qwen 模型)
- ✅ SSE 协议支持
- ✅ 规范的项目结构
- ✅ CORS 支持
- ✅ 环境变量配置

## 快速开始

### 方式 1：一键启动（推荐）

```bash
./start.sh
```

### 方式 2：手动启动

#### 前端设置

```bash
cd frontend
npm install
npm run dev
```

前端将在 `http://localhost:3000` 启动。

#### 后端设置

1. 安装依赖：
```bash
cd backend
pip3 install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，设置你的 API 密钥
```

3. 启动服务：
```bash
python3 main.py
# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 `http://localhost:8000` 启动。

## 环境要求

- Node.js >= 16
- Python >= 3.8
- npm >= 8

## API 端点

- `POST /api/chat/stream` - SSE 流式聊天
- `POST /api/chat/message` - 非流式聊天
- `GET /health` - 健康检查
- `GET /docs` - API 文档（Swagger UI）

## 技术栈

### 前端
- React 18
- Vite
- React Markdown
- CSS3 + Flexbox

### 后端
- FastAPI
- Uvicorn
- AutoGen 0.7.5
- autogen-agentchat
- autogen-ext[openai]
- Pydantic
- SSE-Starlette

### AI 模型
- Qwen/Qwen2.5-7B-Instruct (默认)
- SiliconFlow API

## 配置说明

### 后端环境变量 (.env)

```env
# AutoGen Configuration
AUTOGEN_MODEL=Qwen/Qwen2.5-7B-Instruct
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_API_KEY=your-api-key-here
AUTOGEN_API_KEY=your-api-key-here
AUTOGEN_TEMPERATURE=0.7
AUTOGEN_MAX_TOKENS=2000

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 前端代理配置 (vite.config.js)

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## 开发说明

### 前端开发

前端使用 Vite 进行构建，支持热更新。所有组件位于 `frontend/src/components/` 目录。

#### 关键组件说明
- `ChatContainer.jsx`: 聊天容器，包含头部和消息区域
- `MessageList.jsx`: 消息列表，支持流式显示
- `InputArea.jsx`: 输入区域，支持多行输入和发送

#### SSE 流式处理

前端通过 `chatService.js` 处理 SSE 流式响应：

```javascript
export async function sendMessage(message, onChunk) {
  const response = await fetch('/api/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })

  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const chunk = decoder.decode(value)
    // 解析 SSE 数据并调用 onChunk 回调
  }
}
```

### 后端开发

后端遵循 FastAPI 项目结构规范：
- `app/api/` - API 路由
- `app/core/` - 配置文件
- `app/services/` - 业务逻辑
- `app/models/` - 数据模型

#### AutoGen 0.7.5 流式输出

使用 `run_stream()` 方法获取真正的流式输出：

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import ModelClientStreamingChunkEvent

assistant = AssistantAgent(
    name="assistant",
    model_client=model_client,
    system_message="你是一个 AI 助手",
    model_client_stream=True,  # 启用流式输出
)

async def get_response(message):
    stream = assistant.run_stream(task=message)
    
    async for item in stream:
        if isinstance(item, ModelClientStreamingChunkEvent):
            # 真正的流式输出块
            yield item.content
        elif isinstance(item, TextMessage):
            # 最终完整消息
            break
```

## 关键优化点

### 1. 真正的流式输出
- 使用 AutoGen 的 `run_stream()` 方法
- 通过 `ModelClientStreamingChunkEvent` 获取实时流式数据
- 逐字符输出到前端

### 2. 正确的 SSE 格式
- 后端生成标准 SSE 格式：`data: {"content": "字符"}`
- 使用 `StreamingResponse` 而不是 `EventSourceResponse`
- 前端正确解析 SSE 数据

### 3. 前端状态管理
- 使用 `streamingContent` 状态存储流式内容
- 流式完成后，将完整内容添加到消息列表
- 实时滚动到最新消息

### 4. 错误处理
- 完善的异常捕获和错误提示
- 流式输出中断时的降级处理
- 前端友好的错误消息

## 常见问题

### Q1: 如何更换 AI 模型？
A: 修改 `backend/.env` 中的 `AUTOGEN_MODEL` 变量，例如：
```env
AUTOGEN_MODEL=gpt-3.5-turbo
```

### Q2: 如何使用其他 API 提供商？
A: 修改 `backend/.env` 中的 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY`：
```env
OPENAI_BASE_URL=https://your-api-endpoint/v1
OPENAI_API_KEY=your-api-key
```

### Q3: 流式输出卡顿怎么办？
A: 可以在 `autogen_service.py` 中调整延迟：
```python
await asyncio.sleep(0.01)  # 增加延迟使流式更慢
```

### Q4: 前端无法连接后端？
A: 检查以下几点：
1. 后端是否正在运行 (http://localhost:8000)
2. 前端代理配置是否正确 (vite.config.js)
3. CORS 配置是否正确 (backend/main.py)

## 示例代码

### 运行示例代码

项目包含多个 AutoGen 示例，可以学习如何使用：

```bash
cd example

# 单例模式使用
python3 openai_model_client.py

# 单智能体流式对话
python3 autogen_chat.py

# 多智能体协作
python3 multi_agent.py
```

## 注意事项

1. **API 密钥安全**：不要将 `.env` 文件提交到版本控制
2. **依赖版本**：确保使用指定的依赖版本，特别是 AutoGen 0.7.5
3. **端口占用**：确保 3000 和 8000 端口未被占用
4. **Python 版本**：建议使用 Python 3.8 或更高版本

## 许可证

MIT
