# ∞ Deployment Quick Reference ∞

**Pattern:** QUICK × REFERENCE × DEPLOYMENT × ONE  
**Frequency:** 999 Hz (AEYON)  
**∞ AbëONE ∞**

---

## 🚀 ONE COMMAND TO RULE THEM ALL

```bash
./scripts/deploy.sh
```

That's it. Everything starts.

---

## 🔐 GITHUB AUTHENTICATION (Do This First!)

### **Option 1: SSH (Recommended)**
```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub | pbcopy  # Mac
# Or: cat ~/.ssh/id_ed25519.pub

# Add to GitHub: https://github.com/settings/keys
# Then clone:
git clone git@github.com:BravettoFrontendTeam/abe-touch.git AbeOne_Master
```

### **Option 2: GitHub CLI (Easiest)**
```bash
# Install: brew install gh
gh auth login
gh repo clone BravettoFrontendTeam/abe-touch AbeOne_Master
```

### **Option 3: Personal Access Token**
```bash
# Create token: https://github.com/settings/tokens
# Clone with token:
git clone https://YOUR_TOKEN@github.com/BravettoFrontendTeam/abe-touch.git AbeOne_Master
```

---

## 📋 SETUP WORKFLOW

```bash
# 1. Clone (with authentication)
git clone git@github.com:BravettoFrontendTeam/abe-touch.git AbeOne_Master
cd AbeOne_Master

# 2. Setup (installs everything)
./scripts/setup.sh

# 3. Deploy (starts everything)
./scripts/deploy.sh

# 4. Verify
./scripts/health-check.sh
```

---

## 🎯 COMMON COMMANDS

### **Start Everything**
```bash
docker-compose --profile full up -d
```

### **Stop Everything**
```bash
docker-compose down
```

### **View Logs**
```bash
docker-compose logs -f
```

### **Check Status**
```bash
docker-compose ps
```

### **Health Check**
```bash
./scripts/health-check.sh
```

### **Rebuild**
```bash
docker-compose build --no-cache && docker-compose --profile full up -d
```

---

## 🌐 SERVICE URLs

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **MCP:** http://localhost:8001
- **LSP:** http://localhost:8002

---

## 🆘 TROUBLESHOOTING

**"Repository isn't accessible"**  
→ Set up GitHub authentication (see above)

**"Port already in use"**  
→ `lsof -i :8000` → Kill process or change port

**"Docker not found"**  
→ Install Docker Desktop: https://www.docker.com/products/docker-desktop

**"Services won't start"**  
→ `docker-compose logs -f` → Check errors

---

## 📚 FULL DOCUMENTATION

- **Complete Guide:** `FRICTIONLESS_DEPLOYMENT.md`
- **Team Guide:** `TEAM_GUIDE.md`
- **Docker Setup:** `DOCKER_SETUP.md`

---

**LOVE = LIFE = ONE**  
**∞ AbëONE ∞**

