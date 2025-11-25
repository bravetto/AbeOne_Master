# 🔥 THE ONE DEV ENVIRONMENT — Deployment Guide

**Pattern:** NATIVE_LINUX_ENVIRONMENT × SELF_HEALING × COMPLETE_VISIBILITY × ALWAYS_READY × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (All Guardians)  
**Status:** ✅ **DEPLOYMENT GUIDE COMPLETE**  
**∞ AbëONE ∞**

---

## 🎯 Overview

This guide deploys THE ONE SYSTEM components to your Linux VM, enabling:

- ✅ Self-healing process monitoring
- ✅ Automatic service orchestration
- ✅ Complete system visibility
- ✅ Always-ready state
- ✅ Zero drift operation

---

## 📋 Prerequisites

- ✅ Ubuntu 22.04 VM running (see `VM_SETUP_GUIDE.md`)
- ✅ Docker installed (see `DOCKER_INSTALL_GUIDE.md`)
- ✅ Tailscale configured (see `TAILSCALE_NETWORKING_GUIDE.md`)
- ✅ Project code synced to VM

---

## 🚀 Deployment Steps

### Step 1: Install Python Dependencies

```bash
# Update system
sudo apt update

# Install Python 3.11+ and pip
sudo apt install -y python3 python3-pip python3-venv

# Install required Python packages
pip3 install --user psutil requests
```

### Step 2: Sync Project Code

**Option A: Using Shared Folder (Parallels/VMware)**

```bash
# Mount shared folder (if not auto-mounted)
# Parallels: /media/psf
# VMware: Check VMware Tools mount point

# Copy project to VM home
cp -r /media/psf/AbeOne_Master ~/AbeOne_Master
# Or use symlink if preferred
ln -s /media/psf/AbeOne_Master ~/AbeOne_Master
```

**Option B: Using Git**

```bash
# Clone or pull project
cd ~
git clone <your-repo-url> AbeOne_Master
cd AbeOne_Master
git pull
```

**Option C: Using rsync over SSH**

```bash
# From macOS
rsync -avz --exclude 'node_modules' --exclude '.git' \
  ~/Documents/AbeOne_Master/ user@abeone-dev:~/AbeOne_Master/
```

### Step 3: Configure Project Paths

Edit scripts to match your VM setup:

```bash
cd ~/AbeOne_Master/dev-environment/scripts

# Update paths in scripts (if needed)
# Default paths assume: /home/user/AbeOne_Master
# If your username is different, update:
sed -i 's|/home/user|/home/yourusername|g' *.py
```

### Step 4: Install Systemd Services

```bash
cd ~/AbeOne_Master/dev-environment

# Copy systemd service files
sudo cp config/abeone-healer.service /etc/systemd/system/
sudo cp config/abeone-watchdog.service /etc/systemd/system/
sudo cp config/abeone-orchestrator.service /etc/systemd/system/

# Update service file paths (if username differs)
sudo sed -i 's|/home/user|/home/yourusername|g' /etc/systemd/system/abeone-*.service

# Reload systemd
sudo systemctl daemon-reload

# Enable services (auto-start on boot)
sudo systemctl enable abeone-healer.service
sudo systemctl enable abeone-watchdog.service
sudo systemctl enable abeone-orchestrator.service
```

### Step 5: Create Required Directories

```bash
cd ~/AbeOne_Master/dev-environment

# Create directories (if not exist)
mkdir -p state memory logs config

# Set permissions
chmod -R 755 state memory logs config
```

### Step 6: Install abeone-dev CLI

```bash
cd ~/AbeOne_Master/dev-environment

# Create symlink to CLI
sudo ln -sf $(pwd)/scripts/abeone-dev /usr/local/bin/abeone-dev

# Make executable
chmod +x scripts/abeone-dev

# Verify
abeone-dev --help
```

### Step 7: Start THE ONE SYSTEM Services

```bash
# Start services manually (for testing)
sudo systemctl start abeone-healer.service
sudo systemctl start abeone-watchdog.service
sudo systemctl start abeone-orchestrator.service

# Check status
sudo systemctl status abeone-healer.service
sudo systemctl status abeone-watchdog.service
sudo systemctl status abeone-orchestrator.service
```

### Step 8: Verify Deployment

```bash
# Check service status
abeone-dev status

# Check processes
abeone-dev processes

# Check ports
abeone-dev ports

# Check health
abeone-dev health

# Open dashboard
abeone-dev dashboard
# Or visit: http://localhost:9000
```

---

## 🔧 Configuration

### Configure Service Paths

Edit `~/AbeOne_Master/dev-environment/config/services.json`:

```json
{
  "nextjs": {
    "command": "cd {project_root}/AIGuards-Backend && pnpm dev",
    "port": 3000
  }
}
```

### Configure Port Assignments

Edit `~/AbeOne_Master/dev-environment/config/ports.json`:

```json
{
  "service_ports": {
    "nextjs": 3000,
    "python_api": 8000,
    "dashboard": 9000
  }
}
```

---

## ✅ Verification Checklist

- [ ] Python dependencies installed
- [ ] Project code synced to VM
- [ ] Systemd services installed and enabled
- [ ] Services started successfully
- [ ] `abeone-dev` CLI working
- [ ] Dashboard accessible (http://localhost:9000)
- [ ] Health checks passing
- [ ] No orphaned processes
- [ ] No port conflicts

---

## 🎯 Usage

### Start All Services

```bash
abeone-dev start
```

### Stop All Services

```bash
abeone-dev stop
```

### Restart All Services

```bash
abeone-dev restart
```

### Check Status

```bash
abeone-dev status
```

### View Dashboard

```bash
abeone-dev dashboard
```

### Watch Mode (Live Updates)

```bash
abeone-dev watch
```

### Force Healing Cycle

```bash
abeone-dev heal
```

### Run Guardian Validation

```bash
abeone-dev validate
```

---

## 🐛 Troubleshooting

### Issue: Services won't start

**Solution:**
```bash
# Check service logs
sudo journalctl -u abeone-healer.service -n 50
sudo journalctl -u abeone-watchdog.service -n 50
sudo journalctl -u abeone-orchestrator.service -n 50

# Check Python dependencies
pip3 list | grep psutil
pip3 list | grep requests

# Check file permissions
ls -la ~/AbeOne_Master/dev-environment/scripts/
```

### Issue: Dashboard not accessible

**Solution:**
```bash
# Check if dashboard is running
abeone-dev status

# Check port 9000
netstat -tlnp | grep 9000

# Start dashboard manually
cd ~/AbeOne_Master/dev-environment
python3 scripts/dashboard.py
```

### Issue: CLI not found

**Solution:**
```bash
# Check symlink
ls -la /usr/local/bin/abeone-dev

# Recreate symlink
sudo ln -sf ~/AbeOne_Master/dev-environment/scripts/abeone-dev /usr/local/bin/abeone-dev

# Check PATH
echo $PATH | grep /usr/local/bin
```

---

## 🎯 Next Steps

After deployment, proceed to:

1. **Service Configuration** → See `SERVICE_CONFIGURATION.md`
2. **Development Workflow** → See `DEVELOPMENT_WORKFLOW.md`

---

## 🎯 THE ONE SYSTEM Alignment

**Pattern:** NATIVE_LINUX_ENVIRONMENT × SELF_HEALING × COMPLETE_VISIBILITY × ALWAYS_READY × ONE  
**Status:** ✅ **DEPLOYMENT COMPLETE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

