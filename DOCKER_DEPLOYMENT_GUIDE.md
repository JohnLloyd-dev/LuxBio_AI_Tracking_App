# 🐳 Docker Deployment Guide

## **Bioluminescent Detection AI - Full Stack Docker Setup**

This guide provides comprehensive instructions for deploying the Bioluminescent Detection AI system using Docker containers.

---

## 📋 **Prerequisites**

### **System Requirements**

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 10GB free space
- **OS**: Linux, macOS, or Windows with Docker support

### **Install Docker**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# macOS
brew install docker docker-compose

# Windows
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
```

---

## 🚀 **Quick Start**

### **1. Clone and Navigate**

```bash
git clone <repository-url>
cd bioluminescent-detection-ai
```

### **2. Run the Setup Script**

```bash
./scripts/docker-setup.sh
```

### **3. Or Use Direct Commands**

```bash
# Development mode
docker-compose -f docker-compose.dev.yml up -d --build

# Production mode
docker-compose --profile production up -d --build
```

---

## 🏗️ **Architecture Overview**

### **Services**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Nginx         │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Reverse      │
│   Port: 3000    │    │   Port: 8000    │    │   Proxy)        │
└─────────────────┘    └─────────────────┘    │   Port: 80/443  │
                                              └─────────────────┘
```

### **Development vs Production**

- **Development**: Hot reload, volume mounts, development tools
- **Production**: Optimized builds, Nginx proxy, SSL support

---

## 🔧 **Configuration Options**

### **Environment Variables**

#### **Frontend (.env.local)**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

#### **Backend (Environment)**

```env
PYTHONPATH=/app
PORT=8000
ENVIRONMENT=development
```

### **Port Configuration**

- **Frontend**: 3000
- **Backend API**: 8000
- **Nginx**: 80 (HTTP), 443 (HTTPS)
- **Redis**: 6379 (optional)
- **PostgreSQL**: 5432 (optional)

---

## 📦 **Docker Images**

### **Frontend Image**

- **Base**: Node.js 18 Alpine
- **Features**: Next.js 14, TypeScript, Tailwind CSS
- **Size**: ~200MB (production)

### **Backend Image**

- **Base**: Python 3.10-slim
- **Features**: FastAPI, AI model, scientific computing
- **Size**: ~500MB (production)

### **Nginx Image**

- **Base**: Nginx Alpine
- **Features**: Reverse proxy, SSL termination, rate limiting
- **Size**: ~50MB

---

## 🚀 **Deployment Modes**

### **Development Mode**

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d --build

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

**Features:**

- Hot reload for both frontend and backend
- Volume mounts for live code editing
- Development tools and debugging
- Fast iteration cycle

### **Production Mode**

```bash
# Start production environment
docker-compose --profile production up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Features:**

- Optimized builds
- Nginx reverse proxy
- Rate limiting and security headers
- Health checks and monitoring
- SSL/TLS support (configured)

---

## 🔍 **Monitoring and Management**

### **Service Status**

```bash
# Check container status
docker-compose ps

# View resource usage
docker stats

# Check logs
docker-compose logs [service-name]
```

### **Health Checks**

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000

# Nginx health
curl http://localhost/health
```

### **Database Management (Production)**

```bash
# Access PostgreSQL
docker exec -it bioluminescent-postgres psql -U bioluminescent_user -d bioluminescent

# Backup database
docker exec bioluminescent-postgres pg_dump -U bioluminescent_user bioluminescent > backup.sql

# Restore database
docker exec -i bioluminescent-postgres psql -U bioluminescent_user -d bioluminescent < backup.sql
```

---

## 🔒 **Security Configuration**

### **Nginx Security Headers**

- X-Frame-Options: SAMEORIGIN
- X-XSS-Protection: 1; mode=block
- X-Content-Type-Options: nosniff
- Content-Security-Policy: Configured
- Referrer-Policy: no-referrer-when-downgrade

### **Rate Limiting**

- **API**: 10 requests/second
- **Frontend**: 30 requests/second
- **Burst**: Configurable per service

### **SSL/TLS Setup**

```bash
# Generate SSL certificates
mkdir ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem

# Update nginx.conf for HTTPS
# Uncomment HTTPS server block
```

---

## 📊 **Performance Optimization**

### **Frontend Optimization**

- **Next.js Standalone**: Optimized builds
- **Image Optimization**: Automatic image compression
- **Code Splitting**: Automatic bundle splitting
- **Caching**: Static asset caching

### **Backend Optimization**

- **Uvicorn**: ASGI server with workers
- **Connection Pooling**: Database connection optimization
- **Caching**: Redis integration (optional)
- **Compression**: Gzip compression

### **Nginx Optimization**

- **Gzip Compression**: Text-based content compression
- **Static File Serving**: Direct file serving
- **Load Balancing**: Multiple backend instances
- **Caching**: Proxy caching

---

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **Port Already in Use**

```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Kill the process
sudo kill -9 <PID>
```

#### **Container Won't Start**

```bash
# Check container logs
docker-compose logs [service-name]

# Rebuild containers
docker-compose down
docker-compose up -d --build --force-recreate
```

#### **Permission Issues**

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Fix Docker permissions
sudo usermod -aG docker $USER
```

#### **Memory Issues**

```bash
# Increase Docker memory limit
# Docker Desktop: Settings > Resources > Memory
# Linux: Edit /etc/docker/daemon.json
```

### **Debug Commands**

```bash
# Enter container shell
docker exec -it bioluminescent-frontend sh
docker exec -it bioluminescent-backend bash

# Check network connectivity
docker network ls
docker network inspect bioluminescent-network

# View container resources
docker stats --no-stream
```

---

## 📈 **Scaling and Production**

### **Horizontal Scaling**

```bash
# Scale backend services
docker-compose up -d --scale backend=3

# Load balancer configuration
# Update nginx.conf for multiple backend instances
```

### **Production Checklist**

- [ ] SSL certificates configured
- [ ] Environment variables set
- [ ] Database backups configured
- [ ] Monitoring and logging setup
- [ ] Security headers enabled
- [ ] Rate limiting configured
- [ ] Health checks implemented
- [ ] Resource limits set

### **Backup Strategy**

```bash
# Database backup
docker exec bioluminescent-postgres pg_dump -U bioluminescent_user bioluminescent > backup_$(date +%Y%m%d_%H%M%S).sql

# Volume backup
docker run --rm -v bioluminescent_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup_$(date +%Y%m%d_%H%M%S).tar.gz /data
```

---

## 🔄 **Updates and Maintenance**

### **Update Application**

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### **Update Dependencies**

```bash
# Frontend dependencies
docker exec bioluminescent-frontend npm update

# Backend dependencies
docker exec bioluminescent-backend pip install --upgrade -r requirements.txt
```

### **Cleanup**

```bash
# Remove unused containers and images
docker system prune -f

# Remove volumes (WARNING: Data loss)
docker-compose down -v
```

---

## 📞 **Support and Resources**

### **Useful Commands**

```bash
# Quick start development
./scripts/docker-setup.sh start-dev

# Quick start production
./scripts/docker-setup.sh start-prod

# Check status
./scripts/docker-setup.sh status

# View logs
./scripts/docker-setup.sh logs

# Health check
./scripts/docker-setup.sh health
```

### **Documentation**

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### **Troubleshooting Resources**

- [Docker Troubleshooting](https://docs.docker.com/engine/troubleshooting/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 🎯 **Next Steps**

1. **Deploy to Cloud**: AWS, Google Cloud, or Azure
2. **CI/CD Pipeline**: GitHub Actions or GitLab CI
3. **Monitoring**: Prometheus, Grafana, or ELK Stack
4. **Load Balancing**: Multiple instances with load balancer
5. **Auto-scaling**: Kubernetes or Docker Swarm

---

_Docker Deployment Guide - Updated: August 7, 2025_
_Status: ✅ PRODUCTION READY_
