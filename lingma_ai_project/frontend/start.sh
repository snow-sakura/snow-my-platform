#!/bin/bash

echo "🚀 Starting AutoGen Chat Frontend..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

echo "🌐 Starting Vite dev server on http://localhost:3000"
echo ""

npm run dev
