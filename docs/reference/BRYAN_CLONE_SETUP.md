# Clone Setup for Bryan - Ethernet Connection

## Your Mac's Network Info
- **IP Address**: 192.168.6.252
- **Repository Path**: `/Users/michaelmataluni/Documents/AbeOne_Master`
- **GitHub Remote**: `https://github.com/bravetto/abe-one-source.git`

---

## Option 1: Clone via GitHub (Easiest - Recommended)

If Bryan has access to the GitHub repository:

```bash
cd ~/Documents
git clone https://github.com/bravetto/abe-one-source.git AbeOne_Master
cd AbeOne_Master
```

---

## Option 2: Clone via SSH (If SSH is enabled)

### On Your Mac (Michael's Mac):
1. Enable SSH:
   ```bash
   sudo systemsetup -setremotelogin on
   ```

2. Share your username (or create a shared account)

### On Bryan's Mac:
```bash
cd ~/Documents
git clone ssh://michaelmataluni@192.168.6.252/Users/michaelmataluni/Documents/AbeOne_Master
```

---

## Option 3: Direct File Transfer via Ethernet

### Step 1: Enable File Sharing on Your Mac
1. System Settings → General → Sharing
2. Enable "File Sharing"
3. Click "Options" → Enable "Share files and folders using SMB"
4. Add your user account with read/write access

### Step 2: Connect from Bryan's Mac
1. Open Finder
2. Press `Cmd+K` (Connect to Server)
3. Enter: `smb://192.168.6.252`
4. Authenticate with your credentials
5. Navigate to: `Documents/AbeOne_Master`
6. Copy the entire folder to Bryan's Mac

### Step 3: Initialize Git on Bryan's Mac
```bash
cd ~/Documents/AbeOne_Master
git remote add origin https://github.com/bravetto/abe-one-source.git
git fetch origin
git branch -u origin/main main  # or master, depending on default branch
```

---

## Option 4: Git Bundle (Portable)

### On Your Mac (Michael's Mac):
```bash
cd /Users/michaelmataluni/Documents/AbeOne_Master
git bundle create ~/Desktop/AbeOne_Master.bundle --all
```

Then transfer `AbeOne_Master.bundle` to Bryan's Mac via:
- AirDrop
- USB drive
- File sharing (see Option 3)

### On Bryan's Mac:
```bash
cd ~/Documents
git clone ~/Desktop/AbeOne_Master.bundle AbeOne_Master
cd AbeOne_Master
git remote add origin https://github.com/bravetto/abe-one-source.git
```

---

## Option 5: Simple Git Server (Advanced)

### On Your Mac (Michael's Mac):
```bash
cd /Users/michaelmataluni/Documents/AbeOne_Master
git daemon --reuseaddr --base-path=/Users/michaelmataluni/Documents --export-all --verbose
```

### On Bryan's Mac:
```bash
cd ~/Documents
git clone git://192.168.6.252/AbeOne_Master
```

---

## Recommended: Quick Setup Script

I'll create a script that automates the easiest method. Run this on Bryan's Mac after connecting via ethernet:

```bash
# Save as: ~/setup_abeone.sh
#!/bin/bash
cd ~/Documents
git clone https://github.com/bravetto/abe-one-source.git AbeOne_Master
cd AbeOne_Master
echo "✅ Repository cloned successfully!"
echo "📁 Location: ~/Documents/AbeOne_Master"
```

---

## Post-Clone Setup

After cloning, Bryan should run:

```bash
cd ~/Documents/AbeOne_Master

# Install dependencies (if any)
# Check for package.json, requirements.txt, etc.
if [ -f "package.json" ]; then
    npm install
fi

# Verify git connection
git remote -v
git status
```

---

## Troubleshooting

### If GitHub access is restricted:
- Use Option 3 (File Sharing) or Option 4 (Bundle)

### If ethernet connection fails:
- Check both Macs are on same network
- Ping test: `ping 192.168.6.252` from Bryan's Mac
- Check firewall settings

### If git clone fails:
- Verify network connectivity
- Check SSH/File Sharing is enabled
- Try bundle method (Option 4) as fallback

---

## Network Connection Test

On Bryan's Mac, test connectivity:
```bash
ping 192.168.6.252
```

If ping works, proceed with your chosen method above.

