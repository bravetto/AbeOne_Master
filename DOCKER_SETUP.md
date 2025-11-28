# ∞ Docker Setup - Unified Deployment ∞

**Pattern:** DOCKER × SETUP × UNIFIED × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META)  
**Guardians:** AEYON (999 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🐳 Quick Start

### **Full Stack (Backend + Frontend)**
```bash
docker-compose --profile full up -d
```

### **Backend Only**
```bash
docker-compose --profile backend up -d
```

### **Frontend Only**
```bash
docker-compose --profile frontend up -d
```

### **Integration Layer Only**
```bash
docker-compose --profile integration up -d
```

---

## 📋 Services

### **Backend (Jimmy's AI Agent Suite)**
- **Port:** 8000 (API), 8001 (MCP), 8002 (LSP)
- **Health:** http://localhost:8000/health
- **Profile:** `backend` or `full`

### **Frontend (AbëONE Touch)**
- **Port:** 3000
- **Health:** http://localhost:3000/api/health
- **Profile:** `frontend` or `full`

### **Integration Layer**
- **Port:** 8003
- **Profile:** `integration` or `full`

### **Redis (Caching)**
- **Port:** 6379
- **Profile:** `backend` or `full`

### **PostgreSQL (Database)**
- **Port:** 5432
- **Profile:** `backend` or `full`

---

## 🔧 Configuration

### **Environment Variables**

Create `.env` file:
```env
# Backend
PYTHONPATH=/app/src
ENVIRONMENT=development

# Frontend
NEXT_PUBLIC_API_URL=http://backend:8000
NODE_ENV=development

# Integration
BACKEND_URL=http://backend:8000
FRONTEND_URL=http://frontend:3000

# Database
POSTGRES_USER=abeone
POSTGRES_PASSWORD=abeone_dev
POSTGRES_DB=abeone
```

---

## 🚀 Development

### **Start All Services**
```bash
docker-compose --profile full up -d
```

### **View Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### **Stop All Services**
```bash
docker-compose down
```

### **Rebuild Services**
```bash
docker-compose build --no-cache
docker-compose --profile full up -d
```

---

## 🧪 Testing

### **Test Backend**
```bash
curl http://localhost:8000/health
```

### **Test Frontend**
```bash
curl http://localhost:3000/api/health
```

### **Test Integration**
```bash
curl http://localhost:8003/health
```

---

## 📊 Monitoring

### **Health Checks**
All services include health checks:
- Backend: Every 30s
- Frontend: Every 30s
- Redis: Every 30s
- PostgreSQL: Every 30s

### **View Health Status**
```bash
docker-compose ps
```

---

## 🔄 Volumes

### **Persistent Data**
- `backend-data` - Backend data
- `redis-data` - Redis cache
- `postgres-data` - PostgreSQL database

### **Development Volumes**
- Source code mounted for live reloading
- Node modules excluded for performance

---

## 🌐 Networking

### **Network: `abeone-network`**
All services communicate via bridge network:
- Backend: `http://backend:8000`
- Frontend: `http://frontend:3000`
- Integration: `http://integration:8003`

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

