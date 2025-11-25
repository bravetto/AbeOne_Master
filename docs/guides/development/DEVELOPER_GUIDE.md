# 🚀 DEVELOPER GUIDE - Drift Protection System

**For**: Developers who want to code with confidence  
**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Guardian**: AEYON (999 Hz)

---

## 🎯 QUICK START

### 1. First Time Setup

```bash
# Install git hooks (one time)
./scripts/install-git-hooks.sh

# Setup always-visible status (one time)
./scripts/setup-always-visible.sh

# Quick reference
./scripts/dev-quick-start.sh
```

### 2. Daily Workflow

```bash
# Check status anytime
node scripts/gentle-drift-guardian.js

# Pre-work validation (optional but recommended)
./scripts/pre-work-validation.sh

# Watch status (keep visible)
./scripts/watch-drift-status.sh
```

---

## 📋 ESSENTIAL COMMANDS

### Drift Protection

| Command | Purpose |
|---------|---------|
| `node scripts/gentle-drift-guardian.js` | Quick, friendly status check |
| `node scripts/validate-project-boundaries.js` | Full boundary validation |
| `node scripts/enhanced-import-validator.js` | Check imports for bleed |
| `node scripts/context-boot-validation.js` | Context validation |
| `./scripts/watch-drift-status.sh` | Watch status (auto-updates) |

### Project Setup

| Command | Purpose |
|---------|---------|
| `./scripts/install-git-hooks.sh` | Install git hooks (pre-commit/pre-push) |
| `./scripts/setup-always-visible.sh` | Setup always-visible status |
| `./scripts/dev-quick-start.sh` | Show quick reference |

### Documentation

| File | Purpose |
|------|---------|
| `PROJECT_MASTER_INDEX.md` | Master registry of all projects |
| `PROJECT_STATUS.md` | Current project status (in each project) |
| `.project-boundary` | Machine-readable boundaries |
| `DRIFT_STATUS_ALWAYS_VISIBLE.md` | Always-visible status guide |

---

## 🛡️ PROTECTION LAYERS

### Layer 1: Always-On Guardian ✅
- Runs on every chat interaction
- Non-blocking, informative
- Shows current project context

### Layer 2: Pre-Work Validation ✅
- Context boot validation
- Manual or automatic
- Informative guidance

### Layer 3: Pre-Commit ✅
- Git hooks validate before commit
- Blocks if critical issues
- Clear error messages

### Layer 4: Pre-Push ✅
- Git hooks validate before push
- Full boundary validation
- Blocks if issues found

### Layer 5: CI/CD ✅
- Automated validation on push/PR
- Runs in GitHub Actions
- Reports issues automatically

---

## 💡 BEST PRACTICES

### Before Starting Work

1. **Check Status** (optional but helpful):
   ```bash
   node scripts/gentle-drift-guardian.js
   ```

2. **Verify Project Context**:
   - Read `PROJECT_STATUS.md` in current directory
   - Check you're in the active directory (not legacy)

3. **Keep Status Visible** (recommended):
   - Open `.drift-status.txt` in Cursor
   - Pin the tab
   - Run watch script for auto-updates

### During Work

- ✅ Work in active directories only
- ✅ No imports from legacy directories
- ✅ All changes in correct project
- ✅ Validation scripts available if needed

### After Work

- ✅ Verify changes in correct directory
- ✅ Run validation if you want to double-check
- ✅ Celebrate good work! 🎉

---

## 🚨 TROUBLESHOOTING

### "Drift Detected" Warning

**What it means**: You're working in a legacy directory

**Fix**:
1. Check `PROJECT_STATUS.md` for active directory
2. Navigate to active directory
3. Continue work there

### Git Hook Not Working

**Fix**:
```bash
# Reinstall hooks
./scripts/install-git-hooks.sh

# Verify hooks exist
ls -la .git/hooks/pre-commit
ls -la .git/hooks/pre-push
```

### Status Not Updating

**Fix**:
```bash
# Manual update
node scripts/update-drift-status.js

# Check watch script is running
ps aux | grep watch-drift-status
```

---

## 📚 PROJECT STRUCTURE

```
AbeOne_Master/
├── PROJECT_MASTER_INDEX.md          # Master registry
├── .drift-status.txt                # Always-visible status
├── .drift-status.json               # JSON status
├── scripts/
│   ├── gentle-drift-guardian.js     # Always-on guardian
│   ├── validate-project-boundaries.js  # Full validation
│   ├── enhanced-import-validator.js    # Import checking
│   ├── update-drift-status.js         # Update status
│   ├── watch-drift-status.sh           # Watch status
│   ├── install-git-hooks.sh            # Install hooks
│   └── dev-quick-start.sh              # Quick reference
├── AiGuardian-Chrome-Ext-dev/       # Active project
│   ├── PROJECT_STATUS.md
│   └── .project-boundary
├── AIGuards-Backend/                # Active project
│   ├── PROJECT_STATUS.md
│   └── .project-boundary
└── EMERGENT_OS/                     # Active project
    ├── PROJECT_STATUS.md
    └── .project-boundary
```

---

## ✅ CHECKLIST

### First Time Setup
- [ ] Install git hooks: `./scripts/install-git-hooks.sh`
- [ ] Setup always-visible status: `./scripts/setup-always-visible.sh`
- [ ] Read `PROJECT_MASTER_INDEX.md`
- [ ] Familiarize yourself with validation scripts

### Daily Workflow
- [ ] Check status: `node scripts/gentle-drift-guardian.js`
- [ ] Verify you're in active directory
- [ ] Keep `.drift-status.txt` open (optional)
- [ ] Code with confidence!

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**: ✅ **READY FOR DEVELOPERS**

