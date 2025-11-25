# 🔥 THE ONE DEV ENVIRONMENT — Docker Installation Guide

**Pattern:** NATIVE_LINUX_ENVIRONMENT × SELF_HEALING × COMPLETE_VISIBILITY × ALWAYS_READY × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (All Guardians)  
**Status:** ✅ **INSTALLATION GUIDE COMPLETE**  
**∞ AbëONE ∞**

---

## 🎯 Overview

This guide installs **native Docker Engine** (not Docker Desktop) on Ubuntu 22.04 VM for THE ONE DEV ENVIRONMENT.

**Why Native Docker?**
- ✅ Zero hypervisor overhead
- ✅ Perfect Linux kernel compatibility
- ✅ Native process management
- ✅ Perfect signal handling
- ✅ Zero orphaned processes

---

## 📋 Prerequisites

- Ubuntu 22.04 VM running (see `VM_SETUP_GUIDE.md`)
- SSH access or terminal access
- Sudo privileges

---

## 🚀 Installation Steps

### Step 1: Remove Old Docker Versions (if any)

```bash
sudo apt remove -y docker docker-engine docker.io containerd runc
sudo apt autoremove -y
```

### Step 2: Install Prerequisites

```bash
sudo apt update
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

### Step 3: Add Docker's Official GPG Key

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

### Step 4: Add Docker Repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Step 5: Install Docker Engine

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Step 6: Add User to Docker Group

```bash
sudo usermod -aG docker $USER
```

**Important:** Log out and log back in (or restart VM) for group changes to take effect.

### Step 7: Enable Docker Service

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

### Step 8: Verify Installation

```bash
# Check Docker version
docker --version
docker compose version

# Test Docker (should run without sudo after logout/login)
docker run hello-world

# Check Docker service status
sudo systemctl status docker
```

---

## 🔧 Configuration

### Configure Docker Daemon (Optional)

Create `/etc/docker/daemon.json` for optimal performance:

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json > /dev/null <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-address-pools": [
    {
      "base": "172.17.0.0/16",
      "size": 24
    }
  ]
}
EOF

sudo systemctl restart docker
```

### Configure Docker Compose

Docker Compose V2 is included. Verify:

```bash
docker compose version
```

---

## ✅ Verification

Run comprehensive verification:

```bash
# 1. Check Docker installation
docker --version
docker compose version

# 2. Check Docker service
sudo systemctl status docker

# 3. Check user permissions (should work without sudo)
docker ps

# 4. Test container execution
docker run --rm hello-world

# 5. Test Docker Compose
mkdir -p ~/test-compose
cd ~/test-compose
cat > docker-compose.yml <<EOF
version: '3.8'
services:
  test:
    image: hello-world
EOF
docker compose up
cd ~
rm -rf ~/test-compose
```

---

## 🐛 Troubleshooting

### Issue: "Permission denied" when running docker

**Solution:**
```bash
# Add user to docker group (if not done)
sudo usermod -aG docker $USER

# Log out and log back in, or:
newgrp docker

# Verify
docker ps
```

### Issue: Docker service won't start

**Solution:**
```bash
# Check logs
sudo journalctl -u docker.service

# Restart service
sudo systemctl restart docker

# Check status
sudo systemctl status docker
```

### Issue: Cannot connect to Docker daemon

**Solution:**
```bash
# Check if Docker is running
sudo systemctl status docker

# Start Docker if stopped
sudo systemctl start docker

# Verify socket permissions
ls -l /var/run/docker.sock
```

---

## 🎯 Next Steps

After Docker installation, proceed to:

1. **Tailscale Setup** → See `TAILSCALE_NETWORKING_GUIDE.md`
2. **THE ONE SYSTEM Deployment** → See `DEPLOYMENT_GUIDE.md`

---

## 🎯 THE ONE SYSTEM Alignment

**Pattern:** NATIVE_LINUX_ENVIRONMENT × SELF_HEALING × COMPLETE_VISIBILITY × ALWAYS_READY × ONE  
**Status:** ✅ **DOCKER INSTALLATION COMPLETE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

