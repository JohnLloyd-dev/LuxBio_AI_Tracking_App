# 🚀 Running the Bioluminescent Detection AI Project

This guide covers all the different ways to run this project, from quick Docker setup to manual development.

## 🎯 **Quick Start Options**

### **Option 1: Docker Development (Recommended for beginners)**

```bash
# Start everything with Docker
docker-compose -f docker-compose.dev.yml up -d --build

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

### **Option 2: Interactive Docker Setup**

```bash
# Use the interactive setup script
./scripts/docker-setup.sh

# Or use direct commands:
./scripts/docker-setup.sh start-dev    # Development mode
./scripts/docker-setup.sh start-prod   # Production mode
./scripts/docker-setup.sh status       # Check status
./scripts/docker-setup.sh logs         # View logs
```

### **Option 3: Manual Development (No Docker)**

```bash
# Use the automated startup script
./start-dev.sh

# Or start manually:
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

## 🌐 **Access Points**

Once running, you can access:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API Docs**: http://localhost:8000/redoc

## 🐳 **Docker Commands Reference**

### **Development Mode**

```bash
# Start services
docker-compose -f docker-compose.dev.yml up -d --build

# View logs
docker-compose -f docker-compose.dev.yml logs -f [service-name]

# Stop services
docker-compose -f docker-compose.dev.yml down

# Rebuild and restart
docker-compose -f docker-compose.dev.yml up -d --build --force-recreate
```

### **Production Mode**

```bash
# Start production services
docker-compose --profile production up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### **Useful Docker Commands**

```bash
# Check container status
docker-compose ps

# View resource usage
docker stats

# Enter container shell
docker exec -it [container-name] sh

# View container logs
docker logs [container-name]
```

## 🛠️ **Manual Setup Details**

### **Prerequisites**

- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **Git** for cloning the repository

### **Backend Setup**

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **Frontend Setup**

```bash
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
npm start
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Port Already in Use**

```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Kill the process
sudo kill -9 <PID>
```

#### **Docker Issues**

```bash
# Clean up Docker resources
docker system prune -f

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

### **Health Checks**

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000
```

## 📁 **Project Structure**

```
Drone/
├── frontend/                 # Next.js frontend
│   ├── src/                 # Source code
│   ├── package.json         # Node.js dependencies
│   └── Dockerfile.dev       # Development Dockerfile
├── backend/                 # FastAPI backend
│   ├── api/                # API source code
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile.dev      # Development Dockerfile
├── docker-compose.dev.yml   # Development Docker setup
├── docker-compose.yml       # Production Docker setup
├── start-dev.sh            # Manual startup script
└── scripts/                # Utility scripts
    └── docker-setup.sh     # Docker management script
```

## 🚀 **Next Steps**

1. **Choose your preferred method** (Docker or manual)
2. **Start the services** using one of the options above
3. **Open your browser** to http://localhost:3000
4. **Explore the API** at http://localhost:8000/docs
5. **Start developing!** 🎉

## 📞 **Need Help?**

- Check the logs for error messages
- Verify all prerequisites are installed
- Ensure ports 3000 and 8000 are available
- Try the troubleshooting steps above

---

**Happy coding! 🎯✨**
