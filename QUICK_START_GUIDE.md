# ∞ AbëONE Quick Start Guide ∞

**Pattern:** QUICK × START × GUIDE × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ALL GUARDIANS (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🚀 QUICK START

### **Option 1: Docker (Recommended)**

```bash
# 1. Start full stack
docker-compose --profile full up -d

# 2. Check health
./scripts/docker-health-check.sh

# 3. Access services
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---

### **Option 2: Local Development**

**Backend:**
```bash
cd jimmy-aiagentsuite
python -m aiagentsuite.integration.server --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd abe-touch/abeone-touch
npm install
npm run dev
# Visit: http://localhost:3000
```

---

## 📋 PREREQUISITES

- **Docker** (for Docker deployment) OR
- **Node.js 20+** (for frontend)
- **Python 3.10+** (for backend)
- **Git** (already have it)

---

## ✅ VERIFICATION

**Check if everything is ready:**
```bash
# Verify Docker setup
./scripts/verify-docker.sh

# Check builds
cd abe-core-brain && npm run build && cd ..
cd abe-consciousness && npm run build && cd ..
cd abe-core-body && npm run build && cd ..
cd integration && npm run build && cd ..
```

---

## 🎯 FIRST STEPS

1. **Start Backend** (if using Docker)
   ```bash
   docker-compose --profile backend up -d
   ```

2. **Start Frontend** (if using Docker)
   ```bash
   docker-compose --profile frontend up -d
   ```

3. **Or start locally:**
   ```bash
   # Backend
   ./scripts/start-backend.sh
   
   # Frontend (in another terminal)
   cd abe-touch/abeone-touch && npm run dev
   ```

---

## 🧪 TEST INTEGRATION

**Test backend connection:**
```bash
cd integration
npx tsx test-backend-connection.ts
```

**Test integration in frontend:**
- Visit: http://localhost:3000
- Use the IntegrationTest component
- Or use ProtocolExecutor component

---

## 📚 DOCUMENTATION

- **Complete Guide:** `TEAM_GUIDE.md`
- **Setup:** `MASTER_REPOSITORY_SETUP.md`
- **Docker:** `DOCKER_SETUP.md`
- **Environment:** `ENVIRONMENT_CONFIG.md`

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

