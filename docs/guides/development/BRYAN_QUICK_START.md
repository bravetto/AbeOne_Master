# Quick Start: Clone AbeOne_Master for Bryan

## 🎯 Fastest Method (Recommended)

### If Bryan has GitHub access:
```bash
cd ~/Documents
git clone https://github.com/bravetto/abe-one-source.git AbeOne_Master
cd AbeOne_Master
```

---

## 🔌 Ethernet Direct Transfer

### Step 1: Enable File Sharing (Michael's Mac)
1. System Settings → General → Sharing
2. Turn ON "File Sharing"
3. Click "Options" → Enable "SMB"
4. Your IPs:
   - **Local (same network):** `192.168.6.252`
   - **Public (internet):** `67.233.164.239`

### Step 2: Connect from Bryan's Mac
1. Finder → Go → Connect to Server (`Cmd+K`)
2. Enter: `smb://192.168.6.252` (local) or `smb://67.233.164.239` (remote)
3. Login with Michael's credentials
4. Copy `Documents/AbeOne_Master` folder

### Step 3: Setup Git (Bryan's Mac)
```bash
cd ~/Documents/AbeOne_Master
git remote add origin https://github.com/bravetto/abe-one-source.git
git fetch origin
git status
```

---

## 📦 Alternative: Use Setup Script

Transfer `scripts/setup_bryan_clone.sh` to Bryan's Mac, then:
```bash
chmod +x setup_bryan_clone.sh
./setup_bryan_clone.sh
```

---

## ✅ Verify Setup

```bash
cd ~/Documents/AbeOne_Master
git remote -v
git status
ls -la
```

---

## 🆘 Troubleshooting

**Can't connect?**
- **Same network:** Test `ping 192.168.6.252` from Bryan's Mac
- **Remote:** Test `ping 67.233.164.239` from Bryan's Mac
- Verify File Sharing is ON
- Check firewall settings if connecting remotely

**Git issues?**
- Run: `git remote -v` to check remotes
- If missing: `git remote add origin https://github.com/bravetto/abe-one-source.git`

---

**📞 Need help?** See `BRYAN_CLONE_SETUP.md` for detailed options.
