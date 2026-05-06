#!/bin/bash

echo "🚀 Starting AutoGen Chat Backend..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please copy .env.example to .env and configure your DeepSeek API key:"
    echo "   cp .env.example .env"
    echo ""
    exit 1
fi

# Check if DEEPSEEK_API_KEY is set
if grep -q "your_api_key_here" .env; then
    echo "⚠️  Warning: DEEPSEEK_API_KEY is not configured!"
    echo "   Please edit .env and set your DeepSeek API key."
    echo ""
fi

# Start the server
echo "📡 Starting FastAPI server on http://localhost:8000"
echo "💬 WebSocket endpoint: ws://localhost:8000/ws/chat"
echo "🏥 Health check: http://localhost:8000/health"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
