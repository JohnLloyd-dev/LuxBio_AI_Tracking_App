#!/bin/bash

# Bioluminescent Detection AI - Docker Development Deployment
# This script deploys the application in development mode with hot reloading

set -e

echo "🐳 Deploying Bioluminescent Detection AI in Development Mode..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Stop and remove existing containers
print_status "Cleaning up existing containers..."
docker stop bioluminescent-frontend-dev bioluminescent-backend-dev 2>/dev/null || true
docker rm bioluminescent-frontend-dev bioluminescent-backend-dev 2>/dev/null || true

# Build backend development image
print_status "Building backend development Docker image..."
docker build -t bioluminescent-backend:dev -f ./backend/Dockerfile.dev ./backend

# Build frontend development image
print_status "Building frontend development Docker image..."
docker build -t bioluminescent-frontend:dev -f ./frontend/Dockerfile.dev ./frontend

# Create network if it doesn't exist
print_status "Setting up Docker network..."
docker network create bioluminescent-network 2>/dev/null || true

# Start backend container with volume mounts
print_status "Starting backend container with hot reloading..."
docker run -d \
    --name bioluminescent-backend-dev \
    --network bioluminescent-network \
    -p 8000:8000 \
    -v $(pwd)/backend:/app \
    -e PYTHONPATH=/app \
    -e ENVIRONMENT=development \
    -e PORT=8000 \
    bioluminescent-backend:dev

# Wait for backend to be ready
print_status "Waiting for backend to start..."
sleep 10

# Check backend health
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    print_success "Backend is healthy!"
else
    echo "⚠️  Backend health check failed, but continuing..."
fi

# Start frontend container with volume mounts
print_status "Starting frontend container with hot reloading..."
docker run -d \
    --name bioluminescent-frontend-dev \
    --network bioluminescent-network \
    -p 3000:3000 \
    -v $(pwd)/frontend:/app \
    -v /app/node_modules \
    -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
    -e NODE_ENV=development \
    bioluminescent-frontend:dev

# Wait for frontend to be ready
print_status "Waiting for frontend to start..."
sleep 15

# Check frontend health
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    print_success "Frontend is healthy!"
else
    echo "⚠️  Frontend health check failed, but continuing..."
fi

# Show container status
print_status "Container status:"
docker ps --filter "name=bioluminescent"

echo ""
print_success "🚀 Development deployment completed!"
echo ""
echo "🌐 Access Points:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔄 Hot Reloading:"
echo "   - Backend: Edit files in ./backend/ and see changes automatically"
echo "   - Frontend: Edit files in ./frontend/ and see changes automatically"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker logs -f bioluminescent-backend-dev"
echo "   View logs: docker logs -f bioluminescent-frontend-dev"
echo "   Stop: docker stop bioluminescent-frontend-dev bioluminescent-backend-dev"
echo "   Remove: docker rm bioluminescent-frontend-dev bioluminescent-backend-dev"
echo "   Restart: ./deploy-docker-dev.sh" 