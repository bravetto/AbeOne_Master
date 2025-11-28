# Installation Guide

**Pattern:** INSTALL × SETUP × QUICKSTART × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (YAGNI)  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## ⚡ Quick Start (5 Minutes)

### 1. Prerequisites Check

```bash
# Python 3.11+
python --version

# Node.js 22+
node --version

# Docker & Docker Compose
docker --version
docker-compose --version
```

### 2. Clone Repository

```bash
git clone <repository-url>
cd AbeOne_Master
```

### 3. Setup Credentials

```bash
# Unlock AbëKEYS vault (if using 1Password)
op signin
python3 scripts/unlock_all_credentials.py

# OR create credentials manually
mkdir -p ~/.abekeys/credentials
# See AbëKEYS_README.md for credential file format
```

### 4. Start Services

```bash
docker-compose up -d
```

### 5. Verify Installation

```bash
# Check gateway health
curl http://localhost:8000/health/live

# Should return: {"status": "healthy"}
```

**✅ Installation Complete!**

---

## 📋 Detailed Installation

### Step 1: Install Prerequisites

#### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11+
brew install python@3.11

# Install Node.js 22+
brew install node@22

# Install Docker Desktop
brew install --cask docker
```

#### Linux (Ubuntu/Debian)

```bash
# Python 3.11+
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Node.js 22+
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### Windows

1. Install Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. Install Node.js 22+ from [nodejs.org](https://nodejs.org/)
3. Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

---

### Step 2: Clone Repository

```bash
git clone <repository-url>
cd AbeOne_Master
```

---

### Step 3: Setup AbëKEYS Vault

#### Option A: From 1Password (Recommended)

```bash
# Install 1Password CLI (if not installed)
brew install 1password-cli  # macOS
# OR download from: https://developer.1password.com/docs/cli/get-started

# Sign in to 1Password
op signin

# Pull credentials
python3 scripts/unlock_all_credentials.py
```

#### Option B: Manual Setup

```bash
# Create credential directory
mkdir -p ~/.abekeys/credentials

# Create Stripe credentials
cat > ~/.abekeys/credentials/stripe.json << EOF
{
  "service": "stripe",
  "api_key": "sk_test_...",
  "publishable_key": "pk_test_...",
  "webhook_secret": "whsec_..."
}
EOF

# Create Clerk credentials
cat > ~/.abekeys/credentials/clerk.json << EOF
{
  "service": "clerk",
  "api_key": "sk_live_...",
  "publishable_key": "pk_live_...",
  "webhook_secret": "whsec_..."
}
EOF

# Set secure permissions
chmod 600 ~/.abekeys/credentials/*.json
```

See [AbëKEYS_README.md](AbëKEYS_README.md) for complete credential setup.

---

### Step 4: Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

---

### Step 5: Verify Installation

```bash
# Gateway health check
curl http://localhost:8000/health/live

# Expected response:
# {"status": "healthy"}

# Check services
curl http://localhost:8000/api/v1/health
```

---

## 🔧 Configuration

### Environment Variables

**NO .env files required.** All credentials come from AbëKEYS vault.

However, you can override non-sensitive settings via environment variables:

```bash
# Development mode
export ENVIRONMENT=development
export DEBUG=true
export LOG_LEVEL=DEBUG

# Start services
docker-compose up -d
```

### Docker Compose Configuration

Edit `docker-compose.yml` to customize:

- Ports
- Resource limits
- Service dependencies
- Network configuration

---

## 🚨 Troubleshooting

### Issue: Credentials Not Loading

```bash
# Check AbëKEYS vault exists
ls -la ~/.abekeys/credentials/

# Verify credentials
python3 scripts/read_abekeys.py

# Check file permissions
chmod 600 ~/.abekeys/credentials/*.json
```

### Issue: Services Not Starting

```bash
# Check Docker is running
docker ps

# Check logs
docker-compose logs

# Rebuild services
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Port Already in Use

```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

### Issue: Docker Permission Denied

```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Restart Docker Desktop (macOS/Windows)
```

---

## 📚 Next Steps

- **Developers:** See [DEVS_README.md](DEVS_README.md) for development workflow
- **Services:** See [SERVICES_README.md](SERVICES_README.md) for service overview
- **AbëKEYS:** See [AbëKEYS_README.md](AbëKEYS_README.md) for credential management

---

## ✅ Installation Checklist

- [ ] Prerequisites installed (Python 3.11+, Node.js 22+, Docker)
- [ ] Repository cloned
- [ ] AbëKEYS vault configured
- [ ] Services started (`docker-compose up -d`)
- [ ] Health checks passing (`curl http://localhost:8000/health/live`)
- [ ] Credentials verified (`python3 scripts/read_abekeys.py`)

---

**Pattern:** INSTALL × SETUP × QUICKSTART × ONE  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

