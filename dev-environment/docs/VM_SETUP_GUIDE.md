# 🔥 THE ONE DEV ENVIRONMENT — VM Setup Guide

**Pattern:** NATIVE_LINUX_ENVIRONMENT × SELF_HEALING × COMPLETE_VISIBILITY × ALWAYS_READY × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (All Guardians)  
**Status:** ✅ **SETUP GUIDE COMPLETE**  
**∞ AbëONE ∞**

---

## 🎯 Overview

This guide will help you set up a Linux VM (Ubuntu 22.04) for THE ONE DEV ENVIRONMENT. Choose your virtualization platform:

- **Parallels Desktop** (Recommended for macOS)
- **UTM** (Free, open-source alternative)
- **VMware Fusion** (Alternative option)

---

## 📋 Prerequisites

- macOS host machine
- 16GB+ RAM recommended (8GB minimum)
- 100GB+ free disk space
- Virtualization platform installed

---

## 🚀 Option 1: Parallels Desktop Setup

### Step 1: Install Parallels Desktop

1. Download Parallels Desktop from [parallels.com](https://www.parallels.com/products/desktop/)
2. Install and activate (trial or purchase)

### Step 2: Create Ubuntu VM

1. **Open Parallels Desktop**
2. **File → New**
3. **Select "Install Windows or another OS from a DVD or image file"**
4. **Download Ubuntu 22.04 LTS ISO:**
   ```bash
   # Download from ubuntu.com/download/desktop
   # Or use:
   curl -L -o ~/Downloads/ubuntu-22.04-desktop-amd64.iso \
     https://releases.ubuntu.com/22.04/ubuntu-22.04-desktop-amd64.iso
   ```
5. **Select the ISO file**
6. **Configure VM:**
   - **Name:** `AbeOne-Dev-Environment`
   - **OS Type:** Linux → Ubuntu
   - **Location:** Choose location (default is fine)

### Step 3: Configure VM Resources

**Before starting VM, click "Customize Settings":**

- **CPU & Memory:**
  - **Processors:** 4-8 cores (recommended: 6)
  - **Memory:** 8-16GB (recommended: 12GB)
  
- **Hardware:**
  - **Hard Disk:** 100GB+ (recommended: 150GB)
  - **CD/DVD:** Ubuntu ISO (will be removed after install)
  - **Network:** Shared Network (default)
  - **USB & Bluetooth:** Enable if needed

- **Options:**
  - **Optimization:** Enable "Adaptive Hypervisor"
  - **Sharing:**
    - **Enable "Share Mac"** (for file sharing)
    - **Enable "VirtioFS"** (for better performance)
  - **More Options:**
    - **Auto-start:** Enable "Start automatically when macOS starts"
    - **Suspend:** Enable "Suspend when macOS sleeps"

### Step 4: Install Ubuntu

1. **Start VM**
2. **Follow Ubuntu installation wizard:**
   - Language: English
   - Keyboard: Your layout
   - Installation type: **Erase disk and install Ubuntu** (safe in VM)
   - User account:
     - **Username:** `user` (recommended for consistency)
     - **Password:** Choose strong password
     - **Computer name:** `abeone-dev`
   - Complete installation (takes ~15-20 minutes)

### Step 5: Post-Install Configuration

1. **Update system:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Parallels Tools:**
   - Parallels will prompt automatically
   - Or: **Actions → Install Parallels Tools**
   - Reboot when complete

3. **Enable file sharing:**
   - **Parallels → Configure → Sharing**
   - Enable "Share Mac"
   - Enable "VirtioFS"
   - Mount point: `/media/psf`

---

## 🚀 Option 2: UTM Setup (Free Alternative)

### Step 1: Install UTM

1. Download from [mac.getutm.app](https://mac.getutm.app/)
2. Install (may require allowing in System Preferences → Security)

### Step 2: Create Ubuntu VM

1. **Open UTM**
2. **Click "+" → Virtualize**
3. **Select "Linux"**
4. **Download Ubuntu 22.04 ISO** (same as Parallels)
5. **Configure VM:**
   - **Name:** `AbeOne-Dev-Environment`
   - **Memory:** 8-16GB
   - **CPU Cores:** 4-8
   - **Storage:** 100GB+ disk

### Step 3: Install Ubuntu

1. **Start VM**
2. **Follow Ubuntu installation** (same as Parallels)
3. **After installation, install SPICE guest tools:**
   ```bash
   sudo apt install -y spice-vdagent spice-webdavd
   ```

### Step 4: Configure File Sharing

1. **In UTM, enable directory sharing:**
   - **VM Settings → Sharing → Directory Sharing**
   - Add macOS directory (e.g., `/Users/yourname/Documents/AbeOne_Master`)
   - Mount point: `/mnt/shared`

2. **In Ubuntu, mount shared directory:**
   ```bash
   sudo mkdir -p /mnt/shared
   sudo mount -t 9p -o trans=virtio,version=9p2000.L share /mnt/shared
   ```

---

## 🚀 Option 3: VMware Fusion Setup

### Step 1: Install VMware Fusion

1. Download from [vmware.com/products/fusion.html](https://www.vmware.com/products/fusion.html)
2. Install and activate

### Step 2: Create Ubuntu VM

1. **Open VMware Fusion**
2. **File → New**
3. **Select "Create a custom virtual machine"**
4. **Select Ubuntu ISO**
5. **Configure:**
   - **Memory:** 8-16GB
   - **Processors:** 4-8 cores
   - **Hard Disk:** 100GB+

### Step 3: Install Ubuntu

1. **Start VM**
2. **Follow Ubuntu installation** (same as Parallels)
3. **Install VMware Tools:**
   ```bash
   sudo apt install -y open-vm-tools open-vm-tools-desktop
   ```

### Step 4: Configure File Sharing

1. **VMware Fusion → Virtual Machine → Settings → Sharing**
2. **Enable "Share Folders"**
3. **Add macOS directory**

---

## ✅ Verification

After VM setup, verify:

```bash
# Check system info
uname -a
cat /etc/os-release

# Check resources
free -h
nproc
df -h

# Check network
ip addr show
ping -c 3 8.8.8.8
```

---

## 🔧 Next Steps

After VM setup, proceed to:

1. **Docker Installation** → See `DOCKER_INSTALL_GUIDE.md`
2. **Tailscale Setup** → See `TAILSCALE_NETWORKING_GUIDE.md`
3. **THE ONE SYSTEM Deployment** → See `DEPLOYMENT_GUIDE.md`

---

## 🎯 THE ONE SYSTEM Alignment

**Pattern:** NATIVE_LINUX_ENVIRONMENT × SELF_HEALING × COMPLETE_VISIBILITY × ALWAYS_READY × ONE  
**Status:** ✅ **VM SETUP COMPLETE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

