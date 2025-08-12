#!/bin/bash

# Bioluminescent Detection AI - Development Startup Script
# This script starts both frontend and backend in development mode

set -e

echo "🚀 Starting Bioluminescent Detection AI in development mode..."

# Function to cleanup background processes
cleanup() {
    echo "🛑 Stopping services..."
    kill $FRONTEND_PID $BACKEND_PID 2>/dev/null || true
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting FastAPI backend..."
cd backend
python -m pip install -r requirements.txt
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ../..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Next.js frontend..."
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Services started successfully!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait 