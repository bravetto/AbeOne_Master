# ∞ Environment Configuration Guide ∞

**Pattern:** ENV × CONFIG × GUIDE × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ALL GUARDIANS (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🔧 ENVIRONMENT CONFIGURATION

### **Development Environment**

Create `.env` file in root directory:

```env
# Backend Configuration
PYTHONPATH=/app/src
ENVIRONMENT=development

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development

# Integration Layer Configuration
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# Database Configuration
POSTGRES_USER=abeone
POSTGRES_PASSWORD=abeone_dev
POSTGRES_DB=abeone

# Redis Configuration
REDIS_URL=redis://localhost:6379
```

---

### **Production Environment**

Create `.env.production` file:

```env
# Backend Configuration
PYTHONPATH=/app/src
ENVIRONMENT=production

# Frontend Configuration
NEXT_PUBLIC_API_URL=https://api.abeone.com
NODE_ENV=production

# Integration Layer Configuration
BACKEND_URL=https://api.abeone.com
FRONTEND_URL=https://abeone.com

# Database Configuration
POSTGRES_USER=abeone_prod
POSTGRES_PASSWORD=change_me_in_production
POSTGRES_DB=abeone_prod
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379

# Security
SESSION_SECRET=change_me_in_production
JWT_SECRET=change_me_in_production

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
LOG_LEVEL=info
```

---

## 📋 ENVIRONMENT VARIABLES

### **Backend Variables**
- `PYTHONPATH` - Python path
- `ENVIRONMENT` - Environment (development/production)

### **Frontend Variables**
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NODE_ENV` - Node environment

### **Database Variables**
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name
- `POSTGRES_HOST` - Database host
- `POSTGRES_PORT` - Database port

### **Redis Variables**
- `REDIS_URL` - Redis connection URL

---

## 🚀 USAGE

### **Development**
```bash
# Copy example
cp .env.example .env

# Edit as needed
nano .env
```

### **Production**
```bash
# Copy production example
cp .env.production.example .env.production

# Edit with production values
nano .env.production
```

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

