#!/bin/bash

# AI Chat Assistant - 开发启动脚本（分别启动前后端）

echo "🚀 Starting AI Chat Assistant (Development Mode)..."

# 检查是否在项目根目录
cd "$(dirname "$0")"

echo "📦 Setting up backend..."
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

echo ""
echo "🎨 Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the services, run:"
echo "  Terminal 1 (Backend): cd backend && source venv/bin/activate && python main.py"
echo "  Terminal 2 (Frontend): cd frontend && npm run dev"
echo ""
echo "Or use ./start.sh to run both services in one terminal."
