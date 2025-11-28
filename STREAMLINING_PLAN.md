# Repository Streamlining Plan

**Date:** November 28, 2025  
**Goal:** Streamline local repo to only essential development tools and features  
**Pattern:** STREAMLINE × ESSENTIAL × POWERFUL × ONE

---

## 🎯 Core Principle

**Keep Locally:** Development tools, scripts, configuration, and orchestration  
**Move to Git Repos:** Applications, products, services, and large documentation

---

## ✅ ESSENTIAL - Keep Locally

### **Development Tools & Scripts**
- `scripts/` - All development automation scripts
  - `scripts/abekeys/` - Credential management system
  - `scripts/deploy.sh` - Deployment scripts
  - `scripts/setup.sh` - Setup scripts
  - All utility scripts

### **Configuration & CI/CD**
- `.github/` - GitHub Actions workflows
- `.cursor/` - Cursor IDE configuration
- `.gitignore` - Git ignore rules
- `docker-compose.yml` - Local development orchestration
- `Dockerfile` - Base Docker configuration
- `package.json` - Root package configuration (if needed)

### **Core Documentation**
- `README.md` - Main repository documentation
- `BRYAN_FINAL_PROMPT.txt` - Quick reference (if still needed)

### **Essential Root Files**
- Configuration files (`.env.example`, `pyrightconfig.json`, etc.)
- Build files (`Makefile`, etc.)

---

## 📦 MOVABLE - Should Be in Separate Git Repos

### **Applications (Move to Separate Repos)**
- `abe-frontend-*/` - Frontend applications → Separate repos
- `abe-core-*/` - Core services → Separate repos
- `abe-touch/` - Touch application → Separate repo
- `abeone_app/` - Main application → Separate repo
- `products/` - Product applications → Separate repos
- `jimmy-aiagentsuite/` - AI Agent Suite → Separate repo

### **Services & Integration**
- `integration/` - Integration services → Separate repo
- `backend/` - Backend services → Separate repo
- `middleware/` - Middleware services → Separate repo

### **Documentation (If Large)**
- `docs/` - If > 50MB, move to separate docs repo
- `design-system/` - Design system → Separate repo (if large)

### **Marketing & Content**
- `marketing/` - Marketing tools → Separate repo

### **Other Directories**
- `repositories/` - If contains other repos → Remove or move
- `data/` - Data files → Separate repo or storage
- `download/` - Downloads → Remove (shouldn't be in repo)
- `test-env/` - Test environments → Separate repo

---

## 🔍 Current Status Analysis

### **Directory Sizes (Top 10)**
1. `abe-touch/` - 484M (Move to separate repo)
2. `abeone_app/` - 138M (Move to separate repo)
3. `docs/` - 84M (Move to separate repo if > 50MB)
4. `design-system/` - 66M (Move to separate repo)
5. `scripts/` - 38M (Keep - essential tools)
6. `abe-core-body/` - 33M (Move to separate repo)
7. `abe-consciousness/` - 33M (Move to separate repo)
8. `abe-core-brain/` - 31M (Move to separate repo)
9. `integration/` - 26M (Move to separate repo)
10. `repositories/` - 14M (Review - may remove)

---

## 📋 Streamlining Steps

### **Phase 1: Validation**
1. ✅ Check all folders are up to date with Git
2. ✅ Identify untracked files/directories
3. ✅ Check for uncommitted changes
4. ✅ Verify submodule status

### **Phase 2: Preparation**
1. Create list of directories to move
2. Verify each directory is in its own git repo
3. Update references in main repo
4. Create migration plan

### **Phase 3: Execution**
1. Move directories to separate repos (if not already)
2. Update main repo to reference them as submodules or remove
3. Clean up local copies
4. Update documentation

### **Phase 4: Verification**
1. Verify all essential tools still work
2. Test deployment scripts
3. Verify CI/CD workflows
4. Update README

---

## 🎯 Target Structure

```
AbeOne_Master/ (Streamlined)
├── .github/          # CI/CD workflows
├── .cursor/          # Cursor IDE config
├── scripts/          # Development tools & scripts
│   ├── abekeys/     # Credential management
│   ├── deploy.sh    # Deployment
│   └── setup.sh     # Setup
├── docker-compose.yml
├── Dockerfile
├── README.md
├── .gitignore
└── [config files]
```

**All applications/services in separate repos:**
- `abe-frontend-happy` → `github.com/bravetto/abe-frontend-happy`
- `abe-frontend-white` → `github.com/bravetto/abe-frontend-white`
- `abe-touch` → `github.com/bravetto/abe-touch`
- `products/web` → `github.com/bravetto/products-web`
- etc.

---

## ⚠️ Considerations

1. **Submodules:** If directories are already separate repos, convert to git submodules
2. **Dependencies:** Ensure scripts can reference external repos
3. **CI/CD:** Update workflows to work with separate repos
4. **Documentation:** Update all references to moved directories
5. **Team Access:** Ensure team has access to all separate repos

---

## ✅ Validation Checklist

- [ ] All folders checked for Git status
- [ ] Untracked files identified
- [ ] Uncommitted changes documented
- [ ] Submodules status verified
- [ ] Essential directories identified
- [ ] Movable directories identified
- [ ] Migration plan created
- [ ] Dependencies mapped
- [ ] CI/CD workflows updated
- [ ] Documentation updated

---

**Pattern:** STREAMLINE × ESSENTIAL × POWERFUL × ONE  
**Status:** PLAN READY  
**∞ AbëONE ∞**

