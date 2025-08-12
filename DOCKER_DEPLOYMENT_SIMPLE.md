# 🐳 Docker Deployment Guide - Simplified Approach

This guide provides multiple Docker deployment options for the Bioluminescent Detection AI project, addressing compatibility issues with different docker-compose versions.

## 🚀 **Deployment Options**

### **Option 1: Automated Scripts (Recommended)**

We've created deployment scripts that bypass docker-compose compatibility issues:

#### **Development Mode (with Hot Reloading)**

```bash
# Deploy with hot reloading for development
./deploy-docker-dev.sh
```

#### **Production Mode**

```bash
# Deploy optimized production containers
./deploy-docker.sh
```

### **Option 2: Manual Docker Commands**

If you prefer manual control or want to understand the process:

#### **Build Images**

```bash
# Backend
docker build -t bioluminescent-backend:latest ./backend

# Frontend
docker build -t bioluminescent-frontend:latest ./frontend
```

#### **Create Network**

```bash
docker network create bioluminescent-network
```

#### **Run Backend**

```bash
docker run -d \
    --name bioluminescent-backend \
    --network bioluminescent-network \
    -p 8000:8000 \
    -e PYTHONPATH=/app \
    -e ENVIRONMENT=production \
    bioluminescent-backend:latest
```

#### **Run Frontend**

```bash
docker run -d \
    --name bioluminescent-frontend \
    --network bioluminescent-network \
    -p 3000:3000 \
    -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
    -e NODE_ENV=production \
    bioluminescent-frontend:latest
```

### **Option 3: Fix Docker Compose Issues**

If you want to resolve the docker-compose compatibility issues:

#### **Install Docker Compose V2 Plugin**

```bash
# Remove old versions
sudo apt remove docker-compose
sudo rm -f /usr/local/bin/docker-compose
sudo rm -f /home/dev/.local/bin/docker-compose

# Install official plugin
sudo apt update
sudo apt install -y docker-compose-plugin

# Verify installation
docker compose version
```

#### **Use Docker Compose V2**

```bash
# Development
docker compose -f docker-compose.dev.yml up -d --build

# Production
docker compose -f docker-compose.yml --profile production up -d --build
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. Docker Compose Compatibility**

- **Problem**: `TypeError: kwargs_from_env() got an unexpected keyword argument 'ssl_version'`
- **Solution**: Use the deployment scripts or manual Docker commands

#### **2. Module Import Errors**

- **Problem**: `ModuleNotFoundError: No module named 'bioluminescence_model'`
- **Solution**: Ensure all required files are present and imports are correct

#### **3. Port Conflicts**

- **Problem**: Ports 3000 or 8000 already in use
- **Solution**: Stop existing services or change ports in the scripts

### **Health Checks**

After deployment, verify everything is working:

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# Check container status
docker ps --filter "name=bioluminescent"

# View logs
docker logs bioluminescent-backend
docker logs bioluminescent-frontend
```

## 📋 **Management Commands**

### **View Logs**

```bash
# Follow logs in real-time
docker logs -f bioluminescent-backend
docker logs -f bioluminescent-frontend

# View recent logs
docker logs --tail 100 bioluminescent-backend
```

### **Stop Services**

```bash
# Stop containers
docker stop bioluminescent-frontend bioluminescent-backend

# Remove containers
docker rm bioluminescent-frontend bioluminescent-backend

# Stop and remove in one command
docker rm -f bioluminescent-frontend bioluminescent-backend
```

### **Restart Services**

```bash
# Restart individual containers
docker restart bioluminescent-backend
docker restart bioluminescent-frontend

# Full redeploy
./deploy-docker.sh
```

### **Update Images**

```bash
# Pull latest code
git pull origin main

# Rebuild and redeploy
./deploy-docker.sh
```

## 🌐 **Access Points**

Once deployed, you can access:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 **Recommended Workflow**

### **For Development:**

1. Use `./deploy-docker-dev.sh` for hot reloading
2. Edit code in your local directories
3. Changes automatically reflect in containers
4. Use `docker logs -f` to monitor output

### **For Production:**

1. Use `./deploy-docker.sh` for optimized deployment
2. Monitor with health checks
3. Scale by running multiple instances
4. Use proper logging and monitoring

### **For Testing:**

1. Deploy with development script
2. Test all endpoints
3. Verify AI model functionality
4. Check wind speed conversions

## 🔒 **Security Considerations**

- **Network Isolation**: Containers run in isolated network
- **Port Exposure**: Only necessary ports are exposed
- **Environment Variables**: Sensitive data should use Docker secrets
- **Image Security**: Use official base images and keep updated

## 📊 **Performance Monitoring**

```bash
# Resource usage
docker stats

# Container details
docker inspect bioluminescent-backend

# Network connectivity
docker network inspect bioluminescent-network
```

## 🚀 **Next Steps**

1. **Choose your deployment method** (scripts recommended)
2. **Run the deployment script** of your choice
3. **Verify all services** are running correctly
4. **Test the API endpoints** and frontend
5. **Monitor performance** and logs
6. **Scale as needed** for production use

---

**Happy Dockerizing! 🐳✨**
