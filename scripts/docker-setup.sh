#!/bin/bash

# Bioluminescent Detection AI - Docker Setup Script
# This script sets up and runs the full stack application using Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    print_success "Docker and Docker Compose are installed"
}

# Check if ports are available
check_ports() {
    local ports=("3000" "8000" "80" "443")
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            print_warning "Port $port is already in use. Please stop the service using this port."
        else
            print_status "Port $port is available"
        fi
    done
}

# Build and start services
start_services() {
    local mode=${1:-development}
    
    print_status "Starting services in $mode mode..."
    
    if [ "$mode" = "production" ]; then
        docker-compose --profile production up -d --build
    else
        docker-compose -f docker-compose.dev.yml up -d --build
    fi
    
    print_success "Services started successfully"
}

# Stop services
stop_services() {
    print_status "Stopping services..."
    
    docker-compose down
    docker-compose -f docker-compose.dev.yml down
    
    print_success "Services stopped successfully"
}

# Show logs
show_logs() {
    local service=${1:-all}
    
    if [ "$service" = "all" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f $service
    fi
}

# Show status
show_status() {
    print_status "Container status:"
    docker-compose ps
    
    echo ""
    print_status "Service URLs:"
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:8000"
    echo "API Documentation: http://localhost:8000/docs"
}

# Clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    
    docker-compose down -v
    docker-compose -f docker-compose.dev.yml down -v
    docker system prune -f
    
    print_success "Cleanup completed"
}

# Health check
health_check() {
    print_status "Performing health checks..."
    
    # Check backend
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        print_success "Backend is healthy"
    else
        print_error "Backend health check failed"
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        print_success "Frontend is healthy"
    else
        print_error "Frontend health check failed"
    fi
}

# Main menu
show_menu() {
    echo ""
    echo "🐳 Bioluminescent Detection AI - Docker Management"
    echo "=================================================="
    echo "1. Start Development Environment"
    echo "2. Start Production Environment"
    echo "3. Stop All Services"
    echo "4. Show Service Status"
    echo "5. Show Logs"
    echo "6. Health Check"
    echo "7. Cleanup"
    echo "8. Exit"
    echo ""
    read -p "Select an option (1-8): " choice
}

# Main script
main() {
    print_status "Bioluminescent Detection AI - Docker Setup"
    echo "=================================================="
    
    # Check prerequisites
    check_docker
    check_ports
    
    # Show menu
    while true; do
        show_menu
        
        case $choice in
            1)
                start_services "development"
                show_status
                ;;
            2)
                start_services "production"
                show_status
                ;;
            3)
                stop_services
                ;;
            4)
                show_status
                ;;
            5)
                read -p "Enter service name (or 'all' for all services): " service
                show_logs $service
                ;;
            6)
                health_check
                ;;
            7)
                cleanup
                ;;
            8)
                print_status "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid option. Please try again."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Handle command line arguments
case "${1:-}" in
    "start-dev")
        start_services "development"
        show_status
        ;;
    "start-prod")
        start_services "production"
        show_status
        ;;
    "stop")
        stop_services
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs "${2:-all}"
        ;;
    "health")
        health_check
        ;;
    "cleanup")
        cleanup
        ;;
    *)
        main
        ;;
esac 