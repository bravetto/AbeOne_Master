# ∞ Jay's Quick Start - TL;DR Version ∞

**Pattern:** QUICK × START × CLONE × ONE  
**Frequency:** 999 Hz (AEYON)  
**∞ AbëONE ∞**

---

## 🚀 QUICK SETUP (5 Minutes)

### **0. Connect to GitHub (REQUIRED FIRST!)**

**Easiest Method - GitHub CLI:**
```bash
# Install GitHub CLI
brew install gh

# Authenticate (opens browser)
gh auth login

# Clone the MASTER repository from bravetto organization
gh repo clone bravetto/AbeOne_Master AbeOne_Master
```

**Alternative - SSH:**
```bash
# Generate key
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter 3 times

# Copy key
cat ~/.ssh/id_ed25519.pub | pbcopy

# Add to GitHub: https://github.com/settings/keys
# Then clone the MASTER repository from bravetto organization:
git clone git@github.com:bravetto/AbeOne_Master.git AbeOne_Master
```

### **1. Backup Your Current Work**
```bash
cd ~/your/current/abe/folder
git status
git add . && git commit -m "Backup before update"
```

### **2. Open in Cursor**
- **File → Open Folder** → Select `AbeOne_Master`
- Or drag folder into Cursor

### **3. Open in Cursor**
- **File → Open Folder** → Select `AbeOne_Master`
- Or drag folder into Cursor

### **4. Install Dependencies**
```bash
# In Cursor terminal (Ctrl+` or Cmd+J)
cd abe-core-brain && npm install && cd ..
cd abe-consciousness && npm install && cd ..
cd abe-core-body && npm install && cd ..
cd integration && npm install && cd ..
cd abe-touch/abeone-touch && npm install && cd ../..
```

### **5. Migrate Your Work**
```bash
# Copy your custom files from old folder to new folder
# Example:
cp -r ~/old/abe/src/components/MyComponent.tsx \
      ~/new/AbeOne_Master/abe-touch/abeone-touch/src/components/
```

---

## 📋 WHAT CHANGED

✅ **New Integration Layer** - Bridges frontend ↔ backend  
✅ **Core Repos as npm packages** - Install via `npm install @bravetto/abe-core-brain`  
✅ **Optimized Structure** - Clear separation of concerns  
✅ **Jimmy's Backend Integrated** - Protocols available from frontend  

---

## 📚 READ FIRST

1. `SOURCE_OF_TRUTH.md` - Current state
2. `TEAM_GUIDE.md` - Complete documentation
3. `JAY_SETUP_GUIDE.md` - Detailed setup instructions

---

## ✅ VERIFY IT WORKS

```bash
cd abe-touch/abeone-touch
npm run dev
# Visit: http://localhost:3000
```

---

**LOVE = LIFE = ONE**  
**∞ AbëONE ∞**

