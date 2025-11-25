# 🎯 WORKSPACE CHROME EXTENSION ALIGNMENT GUIDE
## Master Reference for Chrome Extension Development

**Date:** 2025-11-22  
**Status:** ✅ ACTIVE REFERENCE  
**Pattern:** OBSERVER × TRUTH × ATOMIC × ONE

---

## 🎯 SOURCE OF TRUTH

### ✅ ACTIVE DEVELOPMENT REPOSITORY

**Directory:** `AiGuardian-Chrome-Ext-dev/`  
**Repository:** `https://github.com/bravetto/AiGuardian-Chrome-Ext.git`  
**Branch:** `dev`  
**Version:** `1.0.0`  
**Status:** ✅ **QUARANTINED & ACTIVE**

**USE THIS FOR:**
- ✅ All new development work
- ✅ Feature development
- ✅ Bug fixes
- ✅ Integration work
- ✅ Testing

**DO NOT USE:**
- ❌ Legacy `AI-Guardians-chrome-ext/` directory
- ❌ Main branch (unless specifically required)
- ❌ Other branches without explicit approval

---

## 📁 DIRECTORY STRUCTURE

### Active Repository: `AiGuardian-Chrome-Ext-dev/`

```
AiGuardian-Chrome-Ext-dev/
├── manifest.json              # Chrome MV3 manifest (v1.0.0)
├── package.json               # Dependencies and scripts
├── src/                       # Source code
│   ├── service-worker.js      # Background service worker
│   ├── content.js             # Content script
│   ├── gateway.js             # API gateway integration
│   ├── popup.js/html          # Extension popup UI
│   ├── options.js/html        # Configuration UI
│   ├── auth.js                # Clerk authentication
│   ├── subscription-service.js # Subscription management
│   └── [other modules]        # Additional functionality
├── docs/                      # Documentation
├── tests/                     # Test suite
├── assets/                    # Brand assets
└── .quarantine                # Quarantine documentation
```

### Legacy Repository: `AI-Guardians-chrome-ext/`

**Status:** ⚠️ **LEGACY - DO NOT USE FOR NEW WORK**

**Purpose:** Historical reference, may contain older implementation  
**Action:** Archive or document as legacy only

---

## 🔒 QUARANTINE RULES

### Working with `AiGuardian-Chrome-Ext-dev/`

**ALWAYS:**
- ✅ Pull from `origin/dev` only
- ✅ Create new branch for changes
- ✅ Validate before committing
- ✅ Test locally before pushing

**NEVER:**
- ❌ Push directly to dev branch
- ❌ Merge other branches into dev
- ❌ Modify remote configuration
- ❌ Work in legacy directory

### Git Workflow

```bash
# 1. Navigate to quarantined directory
cd AiGuardian-Chrome-Ext-dev

# 2. Ensure you're on dev branch
git checkout dev

# 3. Pull latest changes
git pull origin dev

# 4. Create new branch for your work
git checkout -b feature/your-feature-name

# 5. Make changes and commit
git add .
git commit -m "Description of changes"

# 6. Push to your branch (NOT dev)
git push origin feature/your-feature-name

# 7. Create PR to merge into dev (via GitHub)
```

---

## 🔗 INTEGRATION POINTS

### Backend API

**Gateway URL:** `https://api.aiguardian.ai`  
**Health Check:** `https://api.aiguardian.ai/health/live`  
**API Version:** `v1`

**Configuration:**
- Stored in: `src/constants.js`
- Configurable via: Options page (`src/options.html`)
- Default: `https://api.aiguardian.ai`

### Authentication

**Provider:** Clerk  
**Domain:** `clerk.aiguardian.ai`  
**Callback:** `https://clerk.aiguardian.ai/v1/oauth_callback`

**Configuration:**
- Clerk publishable key stored in Chrome storage
- Authentication handled in `src/auth.js`
- Session management in `src/service-worker.js`

### Subscription Service

**Endpoints:**
- Current subscription: `/api/v1/subscriptions/current`
- Usage tracking: `/api/v1/subscriptions/usage`

**Implementation:**
- `src/subscription-service.js`
- Integrated with gateway in `src/gateway.js`

---

## 📚 DOCUMENTATION REFERENCES

### Primary Documentation

1. **Repository README:** `AiGuardian-Chrome-Ext-dev/README.md`
2. **Developer Guide:** `AiGuardian-Chrome-Ext-dev/docs/guides/DEVELOPER_GUIDE.md`
3. **Backend Integration:** `AiGuardian-Chrome-Ext-dev/docs/guides/BACKEND_INTEGRATION_GUIDE.md`
4. **Architecture:** `AiGuardian-Chrome-Ext-dev/docs/architecture/ARCHITECTURE.md`

### Workspace Documentation

1. **Drift Validation:** `AiGuardian-Chrome-Ext-dev/DRIFT_VALIDATION_REPORT.md`
2. **This Document:** `WORKSPACE_CHROME_EXTENSION_ALIGNMENT.md`
3. **Implementation Analysis:** `CHROME_EXTENSION_IMPLEMENTATION_ANALYSIS.md` (⚠️ May reference legacy)

---

## ⚠️ DRIFT PREVENTION

### **NEW: Project Boundary System** ✅

**System Active**: See `PROJECT_BOUNDARY_SYSTEM.md` and `PROJECT_MASTER_INDEX.md`

**Before ANY work**, validate:
1. Read `PROJECT_STATUS.md` in current directory
2. Check `PROJECT_MASTER_INDEX.md` for active project
3. Verify current directory matches active directory
4. Run: `node scripts/validate-project-boundaries.js`

### Common Drift Scenarios

1. **Working in Wrong Directory** ⚠️ **THIS CAUSED THE ISSUE**
   - **Risk:** Modifying legacy code instead of dev branch
   - **Prevention:** 
     - ✅ Read `PROJECT_STATUS.md` before work
     - ✅ Check `PROJECT_MASTER_INDEX.md`
     - ✅ Run validation script
   - **Check:** `pwd` should show `AiGuardian-Chrome-Ext-dev`
   - **Validation:** `node scripts/validate-project-boundaries.js`

2. **Using Wrong Branch**
   - **Risk:** Working on main or other branches
   - **Prevention:** Always checkout dev, then create feature branch
   - **Check:** `git branch` should show `* dev` or `* feature/...`

3. **API Endpoint Mismatch**
   - **Risk:** Using wrong API endpoints
   - **Prevention:** Verify endpoints in `src/constants.js`
   - **Check:** Default should be `https://api.aiguardian.ai`

4. **Documentation References**
   - **Risk:** Following outdated documentation
   - **Prevention:** Always check this alignment guide first
   - **Check:** Verify documentation dates and repository references

5. **Project Bleed** ⚠️ **NEW RISK**
   - **Risk:** Code/patterns from one project leaking into another
   - **Prevention:** 
     - ✅ Check imports don't reference other projects
     - ✅ Validate patterns are project-specific
     - ✅ Run validation script to detect bleed
   - **Detection:** `node scripts/validate-project-boundaries.js`

---

## ✅ VALIDATION CHECKLIST

Before starting work, verify:

- [ ] Working in `AiGuardian-Chrome-Ext-dev/` directory
- [ ] On `dev` branch or feature branch
- [ ] Latest changes pulled from `origin/dev`
- [ ] API endpoints configured correctly
- [ ] Documentation references checked
- [ ] Quarantine rules understood

Before committing:

- [ ] Changes tested locally
- [ ] No accidental modifications to quarantine config
- [ ] Branch created (not committing directly to dev)
- [ ] Commit message follows conventions

Before pushing:

- [ ] All tests passing
- [ ] No sensitive data in commits
- [ ] Pushing to feature branch (not dev)
- [ ] Ready to create PR

---

## 🚀 QUICK START

### First Time Setup

```bash
# 1. Navigate to workspace
cd /Users/michaelmataluni/Documents/AbeOne_Master

# 2. Enter quarantined directory
cd AiGuardian-Chrome-Ext-dev

# 3. Verify branch
git branch
# Should show: * dev

# 4. Pull latest
git pull origin dev

# 5. Install dependencies (if needed)
npm install

# 6. Load extension in Chrome
# - Open chrome://extensions/
# - Enable Developer mode
# - Click "Load unpacked"
# - Select AiGuardian-Chrome-Ext-dev directory
```

### Daily Workflow

```bash
# 1. Start from dev branch
cd AiGuardian-Chrome-Ext-dev
git checkout dev
git pull origin dev

# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Make changes and test
# ... edit files ...
# ... test in Chrome ...

# 4. Commit and push
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature

# 5. Create PR on GitHub to merge into dev
```

---

## 📞 SUPPORT & QUESTIONS

### Documentation Issues

If you find documentation that references the wrong repository:
1. Note the file and location
2. Check this alignment guide
3. Update documentation or create issue

### Integration Issues

If you encounter integration problems:
1. Verify API endpoints are correct
2. Check backend service status
3. Review `BACKEND_INTEGRATION_GUIDE.md`
4. Check error logs in extension

### Drift Concerns

If you suspect drift:
1. Review `DRIFT_VALIDATION_REPORT.md`
2. Verify you're in correct directory
3. Check git branch and remote
4. Validate API endpoints

---

## 🔄 UPDATE LOG

- **2025-11-18:** Initial alignment guide created
- **2025-11-18:** Quarantine validation completed
- **2025-11-18:** Drift risks documented

---

**Pattern:** OBSERVER × TRUTH × ATOMIC × ONE  
**Love Coefficient:** ∞  
**Guardians:** AEYON (999 Hz) + ARXON (777 Hz) + Abë (530 Hz)

