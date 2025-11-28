# Clone Instructions for Bryan - Complete Guide

## 📋 Summary

This repository is ready to be cloned on Bryan's Mac via ethernet connection.

**Network Info:**
- **Michael's Mac (Local IP):** `192.168.6.252` (for same network/ethernet)
- **Bryan's IP Address:** `67.233.164.239`
- Repository: `/Users/michaelmataluni/Documents/AbeOne_Master`
- GitHub: `https://github.com/bravetto/abe-one-source.git`
- Git Bundle: Created at `/tmp/AbeOne_Master.bundle` (201MB)

---

## 🚀 Recommended: GitHub Clone (Easiest)

**If Bryan has access to the GitHub repository**, this is the fastest method:

```bash
cd ~/Documents
git clone https://github.com/bravetto/abe-one-source.git AbeOne_Master
cd AbeOne_Master
```

**Done!** Skip to "Post-Clone Verification" below.

---

## 🔌 Method 2: Direct File Transfer via Ethernet

### On Your Mac (Michael):

1. **Enable File Sharing:**
   ```bash
   ./scripts/enable_file_sharing.sh
   ```
   
   Or manually:
   - System Settings → General → Sharing
   - Turn ON "File Sharing"
   - Click "Options" → Enable "Share files and folders using SMB"
   - Add your user account

2. **IP Addresses:**
   - **Michael's Mac (local):** `192.168.6.252` (use if Bryan is on same network)
   - **Bryan's IP:** `67.233.164.239` (for reference/connection from Michael's side)
   
   Bryan should connect to `192.168.6.252` if on the same network.

### On Bryan's Mac:

1. **Connect to your Mac:**
   - Open Finder
   - Press `Cmd+K` (Connect to Server)
   - Enter: `smb://192.168.6.252` (local) or `smb://67.233.164.239` (remote)
   - Authenticate with your credentials

2. **Copy the repository:**
   - Navigate to: `Documents/AbeOne_Master`
   - Drag the entire folder to Bryan's `~/Documents/` folder

3. **Setup Git:**
   ```bash
   cd ~/Documents/AbeOne_Master
   git remote add origin https://github.com/bravetto/abe-one-source.git
   git fetch origin
   git status
   ```

---

## 📦 Method 3: Git Bundle (Portable Backup)

A git bundle has been created at `/tmp/AbeOne_Master.bundle` (201MB).

### Transfer the bundle:
- **Option A:** AirDrop it to Bryan's Mac
- **Option B:** Copy via File Sharing (see Method 2)
- **Option C:** Use USB drive

### On Bryan's Mac:
```bash
cd ~/Documents
git clone /path/to/AbeOne_Master.bundle AbeOne_Master
cd AbeOne_Master
git remote add origin https://github.com/bravetto/abe-one-source.git
```

---

## 🛠️ Method 4: Automated Setup Script

Transfer `scripts/setup_bryan_clone.sh` to Bryan's Mac, then:

```bash
chmod +x setup_bryan_clone.sh
./setup_bryan_clone.sh
```

The script will guide Bryan through the cloning process.

---

## ✅ Post-Clone Verification

After cloning, Bryan should verify everything works:

```bash
cd ~/Documents/AbeOne_Master

# Check git setup
git remote -v
git status

# Check repository structure
ls -la

# Install dependencies (if needed)
if [ -f "package.json" ]; then
    npm install
fi

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
fi
```

---

## 🔍 Network Connection Test

Before starting, Bryan should test connectivity:

```bash
# From Bryan's Mac
ping 192.168.6.252
```

If ping works, proceed with your chosen method.

---

## 📚 Additional Resources

- **Quick Start:** `BRYAN_QUICK_START.md`
- **Detailed Options:** `BRYAN_CLONE_SETUP.md`
- **Setup Script:** `scripts/setup_bryan_clone.sh`

---

## 🆘 Troubleshooting

### Can't connect via ethernet?
- Verify both Macs are on the same network
- Check firewall settings (System Settings → Network → Firewall)
- Try WiFi if ethernet isn't working
- Use GitHub clone method instead

### Git issues after file transfer?
- Run: `git remote -v` to check remotes
- If origin missing: `git remote add origin https://github.com/bravetto/abe-one-source.git`
- If branches missing: `git fetch origin && git branch -u origin/main main`

### Bundle won't clone?
- Verify bundle file isn't corrupted
- Check disk space: `df -h`
- Try GitHub clone as alternative

---

## 📞 Quick Reference

**Your Mac IPs:**
- **Local (same network):** `192.168.6.252`
- **Public (internet):** `67.233.164.239`

**GitHub Repo:** `https://github.com/bravetto/abe-one-source.git`  
**Bundle Location:** `/tmp/AbeOne_Master.bundle` (201MB)  
**Share Paths:**
- Local: `smb://192.168.6.252`
- Remote: `smb://67.233.164.239`

---

**Ready to clone!** Choose the method that works best for your setup.

