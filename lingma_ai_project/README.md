# AutoGen 聊天应用

基于 AutoGen 0.7.5 的多代理聊天应用,包含 Vue 3 前端和 FastAPI 后端,使用 DeepSeek 模型。

## 项目结构

```
Lingma_AI_Project/
├── frontend/          # Vue 3 前端 (ant-design-vue)
├── backend/           # FastAPI 后端 (AutoGen + SSE)
└── README.md        # 本文件
```

## 功能特性

- ✅ 实时流式对话 (SSE - Server-Sent Events)
- ✅ AutoGen 多代理协作
- ✅ DeepSeek 模型集成
- ✅ Gemini 风格浅色简约 UI
- ✅ 自动重连机制
- ✅ 会话状态持久化

## 前置要求

- Node.js >= 18
- Python >= 3.10
- DeepSeek API Key

## 快速开始

### 1. 配置后端

```bash
cd backend

# 复制环境变量示例
cp .env.example .env

# 编辑 .env 文件,填入你的 DeepSeek API Key
# DEEPSEEK_API_KEY=your_api_key_here

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 配置前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 3. 访问应用

打开浏览器访问: http://localhost:3000

## 技术栈

### 前端
- Vue 3 (Composition API)
- ant-design-vue 4.x
- Vite
- SSE (Server-Sent Events)

### 后端
- FastAPI
- AutoGen 0.7.5
- DeepSeek (OpenAI-compatible API)
- SSE (Server-Sent Events)

## API 端点

- `GET /health` - 健康检查
- `POST /api/session` - 创建新会话
- `POST /api/chat` - 发送用户消息
- `GET /api/stream/{session_id}` - SSE 流式响应端点

## 环境变量

### 后端 (.env)

```env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
HOST=0.0.0.0
PORT=8000
```

## 开发说明

### 消息格式

**客户端 -> 服务端 (POST /api/chat):**
```json
{
  "session_id": "xxx",
  "content": "用户输入的消息"
}
```

**服务端 -> 客户端 (SSE Events):**
```json
// 连接成功
event: connected
data: {"session_id": "xxx", "status": "connected"}

// 处理中
event: processing
data: {"status": "processing"}

// AI 响应
event: AgentResponse
data: {"type": "AgentResponse", "source": "assistant", "content": "AI回复", "timestamp": "..."}

// 完成
event: done
data: {"status": "completed"}
```

### 架构说明

1. **前端**: Vue 3 单页应用,通过 SSE 接收流式响应,通过 HTTP POST 发送消息
2. **后端**: FastAPI 提供 SSE 和 REST API,管理 AutoGen 团队
3. **AutoGen**: 使用 RoundRobinGroupChat 实现多代理协作
4. **DeepSeek**: 通过 OpenAI-compatible API 接入
5. **会话管理**: 每个对话会话有唯一的 session_id,用于关联请求和响应

## 故障排除

### SSE 连接失败

1. 确保后端服务正在运行 (`uvicorn app.main:app`)
2. 检查 `.env` 文件中是否正确配置了 `DEEPSEEK_API_KEY`
3. 查看浏览器控制台和后端日志获取错误信息
4. 确认浏览器支持 SSE (所有现代浏览器均支持)

### API 调用失败

1. 验证 DeepSeek API Key 是否有效
2. 检查网络连接
3. 确认 `DEEPSEEK_BASE_URL` 配置正确

## 许可证

MIT
