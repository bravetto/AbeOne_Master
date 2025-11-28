# 📋 PROJECT MASTER INDEX

**Last Updated**: 2025-01-18  
**Purpose**: Single source of truth for all projects in workspace  
**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE

---

## 🎯 **ACTIVE PROJECTS**

### **1. AiGuardian Chrome Extension**
- **Status**: ✅ **ACTIVE**
- **Active Directory**: `AiGuardian-Chrome-Ext-dev/`
- **Legacy Directories**: `_ARCHIVE/legacy-projects/AI-Guardians-chrome-ext/` (ARCHIVED - DO NOT USE)
- **Version**: 1.0.0
- **Repository**: `https://github.com/bravetto/AiGuardian-Chrome-Ext.git`
- **Branch**: `dev`
- **Last Updated**: 2025-01-18
- **Source of Truth**: `AiGuardian-Chrome-Ext-dev/PROJECT_STATUS.md`
- **Related Projects**: AIGuards-Backend (backend services)
- **Purpose**: Chrome extension for AI content analysis with guard services

**⚠️ CRITICAL**: Always use `AiGuardian-Chrome-Ext-dev/` for all work. Legacy folder is for reference only.

---

### **2. AIGuards Backend**
- **Status**: ✅ **ACTIVE**
- **Active Directory**: `AIGuards-Backend/`
- **Version**: Latest
- **Last Updated**: 2025-01-18
- **Source of Truth**: `AIGuards-Backend/README.md`
- **Related Projects**: AiGuardian-Chrome-Ext-dev (frontend)
- **Purpose**: Backend guard services (BiasGuard, TrustGuard, ContextGuard, etc.)

---

### **3. Emergent OS**
- **Status**: ✅ **ACTIVE**
- **Active Directory**: `EMERGENT_OS/`
- **Version**: Latest
- **Last Updated**: 2025-01-18
- **Source of Truth**: `EMERGENT_OS/README.md`
- **Purpose**: Core operating system and agent framework

---

## ⚠️ **LEGACY PROJECTS**

### **1. AI Guardians Chrome Extension (Legacy)**
- **Status**: 📦 **ARCHIVED - DO NOT USE**
- **Archived Directory**: `_ARCHIVE/legacy-projects/AI-Guardians-chrome-ext/`
- **Active Replacement**: `AiGuardian-Chrome-Ext-dev/`
- **Version**: 0.1.0
- **Purpose**: Historical reference only (archived)
- **Archive Date**: 2025-01-27
- **Do Not Use**: YES
- **Reason**: Superseded by dev branch with Clerk auth and subscription service

**⚠️ WARNING**: This directory has been ARCHIVED. All fixes and development must go to `AiGuardian-Chrome-Ext-dev/`.

---

## 📁 **PROJECT RELATIONSHIPS**

```
AiGuardian-Chrome-Ext-dev (Frontend)
    ↓
    ├──→ AIGuards-Backend (Backend API)
    │       ├──→ BiasGuard
    │       ├──→ TrustGuard
    │       ├──→ ContextGuard
    │       └──→ Other Guard Services
    │
    └──→ EMERGENT_OS (Core Framework)
            └──→ Agent Suite
```

---

## 🔍 **DRIFT DETECTION RULES**

### **Rule 1: Chrome Extension Projects**
- ✅ **ACTIVE**: `AiGuardian-Chrome-Ext-dev/`
- ⚠️ **LEGACY**: `AI-Guardians-chrome-ext/`
- **Action**: If working in legacy, redirect to active

### **Rule 2: Version Validation**
- Active version: 1.0.0+
- Legacy version: 0.1.0
- **Action**: If version < 1.0.0, check for active directory

### **Rule 3: Feature Detection**
- Active has: Clerk auth, subscription service
- Legacy has: Basic implementation
- **Action**: If missing features, check active directory

---

## ✅ **VALIDATION PROTOCOL**

### **Before Work**
1. Check current directory against this index
2. Verify status is ACTIVE (not LEGACY/ARCHIVE)
3. Confirm active directory matches current location
4. Report any mismatches

### **During Work**
1. No modifications to LEGACY directories
2. No imports from LEGACY directories
3. All changes in ACTIVE directory only

### **After Work**
1. Verify changes in correct directory
2. Update last updated date if needed
3. Report any drift detected

---

## 📊 **PROJECT STATUS SUMMARY**

| Project | Status | Active Directory | Legacy Directories |
|---------|--------|------------------|-------------------|
| AiGuardian Chrome Ext | ✅ ACTIVE | `AiGuardian-Chrome-Ext-dev/` | `_ARCHIVE/legacy-projects/AI-Guardians-chrome-ext/` (ARCHIVED) |
| AIGuards Backend | ✅ ACTIVE | `AIGuards-Backend/` | None |
| Emergent OS | ✅ ACTIVE | `EMERGENT_OS/` | None |

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**: ✅ **MASTER INDEX ACTIVE**

