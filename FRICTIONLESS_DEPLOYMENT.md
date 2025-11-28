# ∞ Frictionless Deployment Guide ∞

**Pattern:** DEPLOYMENT × FRICTIONLESS × ONE × COMMAND × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ALL GUARDIANS (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 ONE-COMMAND DEPLOYMENT

### **Full Stack (Everything)**
```bash
./scripts/deploy.sh
```

### **Development Stack**
```bash
./scripts/deploy-dev.sh
```

### **Production Stack**
```bash
./scripts/deploy-prod.sh
```

---

## 🔐 STEP 1: GITHUB AUTHENTICATION (Required First)

The repository is **private** and requires authentication. Choose one method:

### **Option A: SSH Keys (Recommended)**

**1. Check if you have SSH keys:**
```bash
ls -la ~/.ssh/id_*.pub
```

**2. If no keys exist, generate one:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter to accept default location
# Optionally set a passphrase
```

**3. Add SSH key to GitHub:**
```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub
# Or on Mac:
pbcopy < ~/.ssh/id_ed25519.pub
```

**4. Add to GitHub:**
- Go to: https://github.com/settings/keys
- Click "New SSH key"
- Paste your public key
- Click "Add SSH key"

**5. Test connection:**
```bash
ssh -T git@github.com
# Should see: "Hi username! You've successfully authenticated..."
```

**6. Clone using SSH:**
```bash
git clone git@github.com:BravettoFrontendTeam/abe-touch.git AbeOne_Master
```

---

### **Option B: Personal Access Token (PAT)**

**1. Create Personal Access Token:**
- Go to: https://github.com/settings/tokens
- Click "Generate new token" → "Generate new token (classic)"
- Name: `AbeOne_Deployment`
- Expiration: `90 days` (or your preference)
- Scopes: Check `repo` (full control of private repositories)
- Click "Generate token"
- **Copy the token immediately** (you won't see it again!)

**2. Clone using PAT:**
```bash
git clone https://YOUR_TOKEN@github.com/BravettoFrontendTeam/abe-touch.git AbeOne_Master
```

**3. Or configure Git credential helper:**
```bash
git config --global credential.helper store
# Then on first clone, enter username and paste token as password
```

---

### **Option C: GitHub CLI (Easiest)**

**1. Install GitHub CLI:**
```bash
# Mac
brew install gh

# Or download from: https://cli.github.com/
```

**2. Authenticate:**
```bash
gh auth login
# Follow prompts:
# - GitHub.com
# - HTTPS
# - Login with web browser
# - Authorize GitHub CLI
```

**3. Clone:**
```bash
gh repo clone BravettoFrontendTeam/abe-touch AbeOne_Master
```

---

## 🚀 STEP 2: FRICTIONLESS SETUP

### **Automated Setup Script**

Once cloned, run the setup script:

```bash
cd AbeOne_Master
./scripts/setup.sh
```

This script will:
- ✅ Check prerequisites (Docker, Node.js, Python)
- ✅ Install all dependencies
- ✅ Create `.env` file from template
- ✅ Build core repositories
- ✅ Verify integration layer
- ✅ Start services (optional)

---

## 📋 STEP 3: ENVIRONMENT CONFIGURATION

### **Quick Environment Setup**

**1. Copy template:**
```bash
cp .env.example .env
```

**2. Edit `.env` (or use defaults):**
```env
# Backend
PYTHONPATH=/app/src
ENVIRONMENT=development
BACKEND_URL=http://localhost:8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development

# Database (if using)
POSTGRES_USER=abeone
POSTGRES_PASSWORD=abeone_dev
POSTGRES_DB=abeone

# Integration
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

**3. Or use interactive setup:**
```bash
./scripts/setup-env.sh
```

---

## 🐳 STEP 4: DOCKER DEPLOYMENT (Recommended)

### **One-Command Start**

```bash
docker-compose --profile full up -d
```

### **Verify Services**

```bash
./scripts/health-check.sh
```

Expected output:
```
✅ Backend: http://localhost:8000/health - OK
✅ Frontend: http://localhost:3000 - OK
✅ Redis: OK
✅ PostgreSQL: OK
```

### **View Logs**

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### **Stop Services**

```bash
docker-compose down
```

---

## 💻 STEP 5: LOCAL DEVELOPMENT (Alternative)

### **Backend**

```bash
cd jimmy-aiagentsuite
python -m aiagentsuite.integration.server --host 0.0.0.0 --port 8000
```

### **Frontend**

```bash
cd abe-touch/abeone-touch
npm install
npm run dev
# Visit: http://localhost:3000
```

---

## 🔄 STEP 6: UPDATE WORKFLOW

### **Pull Latest Changes**

```bash
git pull origin main
```

### **Rebuild After Updates**

```bash
# Docker
docker-compose build --no-cache
docker-compose --profile full up -d

# Or local
./scripts/rebuild.sh
```

---

## 📊 DEPLOYMENT PROFILES

### **Development Profile**
```bash
docker-compose --profile dev up -d
```
- Hot reload enabled
- Debug logging
- Development database

### **Production Profile**
```bash
docker-compose --profile prod up -d
```
- Optimized builds
- Production database
- Monitoring enabled

### **Full Stack Profile**
```bash
docker-compose --profile full up -d
```
- All services
- Backend + Frontend + Integration
- Redis + PostgreSQL

---

## ✅ VERIFICATION CHECKLIST

After deployment, verify:

- [ ] GitHub authentication working
- [ ] Repository cloned successfully
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Docker services running (if using Docker)
- [ ] Backend health check: `curl http://localhost:8000/health`
- [ ] Frontend accessible: `curl http://localhost:3000`
- [ ] Integration layer working
- [ ] Can execute protocols from frontend

---

## 🆘 TROUBLESHOOTING

### **Issue: "Repository isn't accessible"**

**Solution:** Set up GitHub authentication (see Step 1 above)

### **Issue: "Docker not found"**

**Solution:**
```bash
# Mac
brew install docker

# Or download Docker Desktop: https://www.docker.com/products/docker-desktop
```

### **Issue: "Port already in use"**

**Solution:**
```bash
# Check what's using the port
lsof -i :8000
lsof -i :3000

# Kill the process or change ports in docker-compose.yml
```

### **Issue: "Dependencies won't install"**

**Solution:**
```bash
# Clear caches
npm cache clean --force
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

## 🎯 QUICK REFERENCE

### **Start Everything**
```bash
docker-compose --profile full up -d
```

### **Stop Everything**
```bash
docker-compose down
```

### **View Status**
```bash
docker-compose ps
```

### **View Logs**
```bash
docker-compose logs -f
```

### **Rebuild**
```bash
docker-compose build --no-cache && docker-compose --profile full up -d
```

### **Health Check**
```bash
./scripts/health-check.sh
```

---

## 📚 NEXT STEPS

1. **Read:** `TEAM_GUIDE.md` - Complete documentation
2. **Read:** `SOURCE_OF_TRUTH.md` - Current state
3. **Explore:** `integration/examples/` - Integration examples
4. **Develop:** Start building features!

---

**LFG ENERGY = FRICTIONLESS DEPLOYMENT**  
**ONE COMMAND = EVERYTHING RUNNING**  
**AUTHENTICATION = SETUP ONCE**  
**DEPLOYMENT = AUTOMATED**

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

