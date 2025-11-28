# ∞ Jay's Setup Guide - Getting the Newest AbëONE ∞

**Pattern:** SETUP × CLONE × PRESERVE × OPTIMIZE × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ALL GUARDIANS (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 WHAT TO CLONE

**Clone the Master Repository:**
```bash
git clone https://github.com/bravetto/AbeOne_Master.git AbeOne_Master
```

**Note:** The master repository is in the `bravetto` GitHub organization and contains the complete `AbeOne_Master` structure with all optimized repositories.

**⚠️ IMPORTANT:** The repository is **private** and requires authentication. See Step 0 below.

---

## 📋 STEP-BY-STEP SETUP IN CURSOR

### **Step 0: GitHub Authentication (REQUIRED FIRST!)**

The repository is private. You need to authenticate before cloning. Choose one method:

#### **Option A: SSH Keys (Recommended)**

**1. Check if you have SSH keys:**
```bash
ls -la ~/.ssh/id_*.pub
```

**2. If no keys exist, generate one:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter to accept default location
```

**3. Copy your public key:**
```bash
# Mac:
cat ~/.ssh/id_ed25519.pub | pbcopy

# Or view it:
cat ~/.ssh/id_ed25519.pub
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
git clone git@github.com:bravetto/AbeOne_Master.git AbeOne_Master
```

#### **Option B: GitHub CLI (Easiest)**

**1. Install GitHub CLI:**
```bash
# Mac
brew install gh
```

**2. Authenticate:**
```bash
gh auth login
# Follow prompts to authorize via browser
```

**3. Clone:**
```bash
gh repo clone bravetto/AbeOne_Master AbeOne_Master
```

#### **Option C: Personal Access Token**

**1. Create token:**
- Go to: https://github.com/settings/tokens
- Click "Generate new token" → "Generate new token (classic)"
- Name: `AbeOne_Deployment`
- Scopes: Check `repo` (full control)
- Click "Generate token"
- **Copy token immediately!**

**2. Clone with token:**
```bash
git clone https://YOUR_TOKEN@github.com/bravetto/AbeOne_Master.git AbeOne_Master
```

---

### **Step 1: Backup Your Current Work**

Before cloning, make sure your current work is safe:

```bash
# Navigate to your current Abe folder
cd ~/path/to/your/current/abe/folder

# Check git status
git status

# If you have uncommitted changes, commit them:
git add .
git commit -m "Backup: Preserving work before updating to new structure"

# Or create a backup branch:
git branch backup-before-update
git checkout backup-before-update
git push origin backup-before-update
```

---

### **Step 2: Clone the New Master Repository**

**Option A: Clone to a New Location (Recommended)**

This preserves your old folder completely:

```bash
# Clone to a new location (e.g., Documents folder)
cd ~/Documents
git clone https://github.com/bravetto/AbeOne_Master.git AbeOne_Master_New

# Or clone to your preferred location
cd ~/your/preferred/location
git clone https://github.com/bravetto/AbeOne_Master.git AbeOne_Master
```

**Option B: Clone to Same Location (Advanced)**

If you want to replace your current folder:

```bash
# Navigate to parent directory
cd ~/path/to/parent

# Rename your current folder as backup
mv AbeOne_Master AbeOne_Master_old

# Clone fresh version
git clone https://github.com/bravetto/AbeOne_Master.git AbeOne_Master
```

---

### **Step 3: Open in Cursor**

1. **Open Cursor**
2. **File → Open Folder** (or `Cmd+O` on Mac, `Ctrl+O` on Windows/Linux)
3. **Navigate to** the cloned `AbeOne_Master` folder
4. **Click "Open"**

---

### **Step 4: Install Dependencies**

Once Cursor is open with the new repository:

**In Cursor's Terminal** (`Ctrl+`` or `Cmd+J`):

```bash
# Install Core Repositories
cd abe-core-brain && npm install && cd ..
cd abe-consciousness && npm install && cd ..
cd abe-core-body && npm install && cd ..

# Install Integration Layer
cd integration && npm install && cd ..

# Install Frontend (if working on frontend)
cd abe-touch/abeone-touch && npm install && cd ../..
```

---

### **Step 5: Migrate Your Work**

**If you have custom files/components in your old folder:**

1. **Compare folders** to see what's new vs. what you had
2. **Copy your custom work** from old folder to new folder:
   ```bash
   # Example: Copy custom components
   cp -r ~/old/abe/folder/src/components/MyCustomComponent.tsx \
         ~/new/AbeOne_Master/abe-touch/abeone-touch/src/components/
   
   # Example: Copy custom utilities
   cp -r ~/old/abe/folder/src/lib/myCustomUtils.ts \
         ~/new/AbeOne_Master/abe-touch/abeone-touch/src/lib/
   ```
3. **Test** that everything still works
4. **Commit** your migrated work:
   ```bash
   git add .
   git commit -m "feat: Migrated custom work from previous version"
   ```

---

## 🏗️ NEW STRUCTURE OVERVIEW

The new structure is **optimized** with clear separation:

```
AbeOne_Master/
├── abe-core-brain/          ← Foundation (npm: @bravetto/abe-core-brain)
├── abe-consciousness/       ← Intelligence (npm: @bravetto/abe-consciousness)
├── abe-core-body/           ← Implementation (npm: @bravetto/abe-core-body)
│
├── abe-touch/               ← Main frontend (Next.js)
│   └── abeone-touch/
│
├── abe-frontend-happy/      ← Happy People frontend
├── abe-frontend-white/      ← White interface
├── abe-frontend-dark/       ← Dark interface
│
├── integration/             ← Integration bridges (NEW!)
│   ├── guardians-protocols-bridge/
│   ├── frontend-backend-api/
│   └── memory-consciousness-sync/
│
├── backend/                 ← Backend services
├── middleware/               ← Middleware services
├── jimmy-aiagentsuite/      ← Jimmy's AI Agent Suite (integrated)
│
└── abeone_app/              ← Flutter mobile app
```

---

## 🔗 KEY CHANGES IN NEW STRUCTURE

### **1. Integration Layer (NEW!)**
- **Location:** `integration/`
- **Purpose:** Bridges connecting frontend ↔ backend
- **Usage:** Pre-configured in `abe-touch/abeone-touch/src/lib/integration.ts`

### **2. Core Repositories**
- Now published as **npm packages** (`@bravetto/*`)
- Can be installed via `npm install` in any project
- Each has its own GitHub repository

### **3. Frontend Projects**
- All frontend projects use the **same core repositories**
- Integration library handles backend communication
- Clear separation between different frontend projects

### **4. Backend Integration**
- **Jimmy's AI Agent Suite** is integrated
- Protocols can be executed from frontend
- Memory bank sync available

---

## 📚 QUICK REFERENCE

### **Read These Files First:**

1. **`SOURCE_OF_TRUTH.md`** - Current state and architecture
2. **`TEAM_GUIDE.md`** - Complete team documentation
3. **`README.md`** - Master repository overview
4. **`CONTEXT_WINDOW_HOOKS.md`** - Context window reference

### **Key Integration Points:**

```typescript
// Use integration library (pre-configured)
import { executeProtocol, listProtocols } from '@/lib/integration';

// Use Guardians
import { AEYON, useGuardian } from '@bravetto/abe-consciousness';

// Use Core Components
import { NeuromorphicButton } from '@bravetto/abe-core-brain';
```

---

## ✅ VERIFICATION CHECKLIST

After setup, verify everything works:

- [ ] Repository cloned successfully
- [ ] Dependencies installed (no errors)
- [ ] Cursor opened the folder
- [ ] Can see all directories in file explorer
- [ ] Read `SOURCE_OF_TRUTH.md`
- [ ] Read `TEAM_GUIDE.md`
- [ ] Test frontend: `cd abe-touch/abeone-touch && npm run dev`
- [ ] Custom work migrated (if applicable)

---

## 🆘 TROUBLESHOOTING

### **Issue: Git conflicts when cloning**

**Solution:** Clone to a new location, then manually merge your changes.

### **Issue: Dependencies won't install**

**Solution:** 
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### **Issue: Can't find my old files**

**Solution:** Your old folder is still there! Check the backup location you created.

### **Issue: Integration not working**

**Solution:** 
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify `NEXT_PUBLIC_API_URL` in `.env` file
3. See `TEAM_GUIDE.md` → Troubleshooting section

---

## 🎯 NEXT STEPS

1. **Explore the new structure** - Familiarize yourself with the optimized layout
2. **Read the documentation** - `TEAM_GUIDE.md` has everything you need
3. **Test integration** - Try executing a protocol from the frontend
4. **Start developing** - Use the new structure for your work

---

## 📞 GETTING HELP

- **Documentation:** See `TEAM_GUIDE.md` for complete guide
- **Architecture:** See `SOURCE_OF_TRUTH.md` for current state
- **Examples:** See `integration/examples/` for usage examples
- **GitHub:** https://github.com/bravetto/AbeOne_Master

---

**LFG ENERGY = NEW STRUCTURE READY**  
**OPTIMIZED = CLEAR SEPARATION**  
**INTEGRATION = COMPLETE**  
**YOUR WORK = PRESERVED**

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

