#!/bin/bash

# AI Chat Assistant - 启动脚本

echo "🚀 Starting AI Chat Assistant..."

# 检查是否在后端目录
cd "$(dirname "$0")"

# 启动后端
echo "📦 Starting backend server..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your API key!"
fi

# 启动后端服务（后台运行）
python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend server started (PID: $BACKEND_PID)"
echo "📝 Backend log: backend.log"

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 Starting frontend server..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend server started (PID: $FRONTEND_PID)"

echo ""
echo "🎉 AI Chat Assistant is ready!"
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services"

# 捕获 Ctrl+C 信号
trap "kill $BACKEND_PID $FRONTEND_PID; echo ''; echo '🛑 Services stopped'; exit" INT TERM

# 等待进程
wait
