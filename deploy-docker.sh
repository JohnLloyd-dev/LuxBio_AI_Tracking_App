#!/bin/bash

# Bioluminescent Detection AI - Docker Deployment Script
# This script deploys the application using individual Docker commands

set -e

echo "🐳 Deploying Bioluminescent Detection AI with Docker..."

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
docker stop bioluminescent-frontend bioluminescent-backend 2>/dev/null || true
docker rm bioluminescent-frontend bioluminescent-backend 2>/dev/null || true

# Build backend image
print_status "Building backend Docker image..."
docker build -t bioluminescent-backend:latest ./backend

# Build frontend image
print_status "Building frontend Docker image..."
docker build -t bioluminescent-frontend:latest ./frontend

# Create network if it doesn't exist
print_status "Setting up Docker network..."
docker network create bioluminescent-network 2>/dev/null || true

# Start backend container
print_status "Starting backend container..."
docker run -d \
    --name bioluminescent-backend \
    --network bioluminescent-network \
    -p 8000:8000 \
    -e PYTHONPATH=/app \
    -e ENVIRONMENT=production \
    -e PORT=8000 \
    bioluminescent-backend:latest

# Wait for backend to be ready
print_status "Waiting for backend to start..."
sleep 10

# Check backend health
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    print_success "Backend is healthy!"
else
    echo "⚠️  Backend health check failed, but continuing..."
fi

# Start frontend container
print_status "Starting frontend container..."
docker run -d \
    --name bioluminescent-frontend \
    --network bioluminescent-network \
    -p 3000:3000 \
    -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
    -e NODE_ENV=production \
    bioluminescent-frontend:latest

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
print_success "🚀 Deployment completed!"
echo ""
echo "🌐 Access Points:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker logs bioluminescent-backend"
echo "   View logs: docker logs bioluminescent-frontend"
echo "   Stop: docker stop bioluminescent-frontend bioluminescent-backend"
echo "   Remove: docker rm bioluminescent-frontend bioluminescent-backend"
echo "   Restart: ./deploy-docker.sh" 