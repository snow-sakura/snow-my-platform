# 快速启动指南

## 前置准备

1. **获取 DeepSeek API Key**
   - 访问 https://platform.deepseek.com
   - 注册账号并创建 API Key

2. **配置环境变量**

```bash
cd backend
cp .env.example .env
```

编辑 `backend/.env` 文件:
```env
DEEPSEEK_API_KEY=sk-your-actual-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

## 启动服务

### 方式一: 使用启动脚本 (推荐)

**终端 1 - 启动后端:**
```bash
cd backend
./start.sh
```

**终端 2 - 启动前端:**
```bash
cd frontend
./start.sh
```

### 方式二: 手动启动

**启动后端:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**启动前端:**
```bash
cd frontend
npm install
npm run dev
```

## 访问应用

打开浏览器访问: **http://localhost:3000**

## 验证安装

### 1. 检查后端健康状态
```bash
curl http://localhost:8000/health
```

预期输出:
```json
{"status":"healthy","service":"autogen-chat-api"}
```

### 2. 检查前端
浏览器访问 http://localhost:3000,应该看到:
- 浅色简约风格的聊天界面
- 顶部显示"已连接"状态
- 底部有输入框和发送按钮

### 3. 测试对话
1. 在输入框输入消息,例如 "你好"
2. 点击发送或按 Enter
3. 等待 AI 回复(流式显示)

## 常见问题

### Q: WebSocket 连接失败
**A:** 确保:
- 后端服务正在运行
- `.env` 文件中配置了正确的 API Key
- 防火墙未阻止 8000 端口

### Q: 收到 "DEEPSEEK_API_KEY is not set" 错误
**A:** 检查 `backend/.env` 文件是否存在且包含有效的 API Key

### Q: 前端页面空白
**A:** 
- 打开浏览器控制台查看错误信息
- 确保后端 WebSocket 服务可访问
- 检查 Vite 代理配置是否正确

### Q: API 调用失败
**A:**
- 验证 DeepSeek API Key 是否有效且有余额
- 检查网络连接
- 查看后端日志获取详细错误信息

## 项目结构

```
Lingma_AI_Project/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── config.py       # 配置管理
│   │   ├── team_manager.py # AutoGen 团队管理
│   │   ├── websocket_handler.py  # WebSocket 处理
│   │   └── main.py         # FastAPI 应用入口
│   ├── model_config.yaml   # 模型配置
│   ├── requirements.txt    # Python 依赖
│   ├── .env.example        # 环境变量示例
│   └── start.sh            # 启动脚本
│
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── components/     # Vue 组件
│   │   ├── composables/    # Composition API
│   │   ├── styles/         # 全局样式
│   │   ├── App.vue         # 根组件
│   │   └── main.js         # 入口文件
│   ├── vite.config.js      # Vite 配置
│   ├── package.json        # Node 依赖
│   └── start.sh            # 启动脚本
│
└── README.md               # 项目文档
```

## 技术栈

- **前端**: Vue 3 + ant-design-vue + Vite
- **后端**: FastAPI + AutoGen 0.7.5 + WebSocket
- **AI 模型**: DeepSeek (deepseek-chat)
- **通信协议**: WebSocket (实时双向通信)

## 下一步

- 尝试多轮对话,测试上下文保持
- 查看后端日志了解 AutoGen 工作流程
- 修改 `team_manager.py` 自定义代理行为
- 调整前端样式定制 UI

祝使用愉快! 🚀
