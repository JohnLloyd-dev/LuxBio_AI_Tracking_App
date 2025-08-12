# Bioluminescent Detection AI - Project Structure

## 📁 **Project Organization**

```
bioluminescent-detection-ai/
├── 📁 backend/                    # Python FastAPI Backend
│   ├── 📁 api/                   # API application
│   │   ├── main.py              # FastAPI application
│   │   ├── bioluminescence_model.py
│   │   ├── data_models.py
│   │   ├── deployment_controller.py
│   │   └── validation.py
│   ├── 📁 tests/                # Unit tests
│   ├── 📁 data_formats/         # CSV templates
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Backend container
│   └── docker-compose.yml      # Backend services
│
├── 📁 frontend/                  # Next.js Frontend (to be created)
│   ├── 📁 src/
│   │   ├── 📁 components/       # React components
│   │   ├── 📁 pages/           # Next.js pages
│   │   ├── 📁 styles/          # Tailwind CSS
│   │   └── 📁 utils/           # Utility functions
│   ├── package.json            # Node.js dependencies
│   ├── tailwind.config.js      # Tailwind configuration
│   └── next.config.js          # Next.js configuration
│
├── 📁 docs/                      # Documentation
│   ├── README.md               # Main project documentation
│   ├── API_DOCUMENTATION.md    # API reference
│   ├── DEPLOYMENT_GUIDE.md     # Deployment instructions
│   └── USER_GUIDE.md           # User manual
│
├── 📁 scripts/                   # Utility scripts
│   ├── setup.sh                # Project setup
│   ├── deploy.sh               # Deployment script
│   └── test.sh                 # Test runner
│
└── 📁 data_formats/             # Data templates
    ├── csv_templates/          # CSV format examples
    └── json_examples/          # JSON format examples
```

## 🏗️ **Architecture Overview**

### **Backend (FastAPI)**

- **API Server**: FastAPI with automatic documentation
- **AI Model**: Physics-based bioluminescence detection model
- **Data Processing**: Comprehensive validation and conversion
- **Wind Speed Handling**: Multi-unit conversion system
- **Deployment**: Docker containerization

### **Frontend (Next.js + Tailwind)**

- **Modern UI**: React with TypeScript
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React hooks and context
- **API Integration**: Axios for backend communication
- **Build System**: Next.js with optimization

### **Documentation**

- **Technical Docs**: API reference and implementation details
- **User Guides**: Step-by-step usage instructions
- **Deployment**: Production deployment procedures
- **Examples**: Code and data format examples

## 🔧 **Technology Stack**

### **Backend Stack**

- **Python 3.10+**: Core programming language
- **FastAPI**: High-performance web framework
- **Pydantic**: Data validation and serialization
- **NumPy/SciPy**: Scientific computing
- **Docker**: Containerization

### **Frontend Stack**

- **Next.js 14**: React framework with SSR/SSG
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Hook Form**: Form handling
- **Axios**: HTTP client

### **Development Tools**

- **ESLint**: Code linting
- **Prettier**: Code formatting
- **Husky**: Git hooks
- **Jest**: Testing framework

## 🚀 **Development Workflow**

### **Local Development**

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python api/main.py

# Frontend
cd frontend
npm install
npm run dev
```

### **Testing**

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### **Building**

```bash
# Backend
cd backend
docker build -t bioluminescent-backend .

# Frontend
cd frontend
npm run build
```

## 📊 **Project Status**

### **✅ Completed**

- Backend API with FastAPI
- AI model implementation
- Data validation and processing
- Wind speed unit conversion
- Basic documentation
- Docker configuration

### **🔄 In Progress**

- Project structure cleanup
- Next.js frontend setup

### **📋 Planned**

- Modern UI components
- Real-time data visualization
- User authentication
- Advanced analytics
- Mobile app

## 🎯 **Next Steps**

1. **Frontend Development**

   - Set up Next.js project with TypeScript
   - Configure Tailwind CSS
   - Create responsive UI components
   - Implement API integration

2. **Enhanced Features**

   - Real-time data visualization
   - User authentication system
   - Advanced form validation
   - Mobile optimization

3. **Production Deployment**
   - CI/CD pipeline setup
   - Production environment configuration
   - Performance optimization
   - Security hardening

---

_Project Structure - Updated: August 7, 2025_
_Status: 🧹 CLEANED UP - READY FOR FRONTEND DEVELOPMENT_
