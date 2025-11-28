# 🔥 DANNY'S WORKFLOW PATTERN - ALWAYS REFERENCE THIS FIRST
## Before Creating ANY New Workflow

**⚠️ CRITICAL: ALWAYS CHECK THIS BEFORE CREATING NEW WORKFLOWS ⚠️**

**Source:** https://github.com/bravetto/AIGuards-Backend/tree/main/.github/workflows  
**Reference Doc:** `DANNY_WORKFLOW_PATTERN_ALWAYS_CLEAR.md`  
**Validator:** `python scripts/validate_danny_workflow_pattern.py`

---

## 🎯 QUICK CHECKLIST

**Before creating ANY workflow, verify:**

1. ✅ Uses `runs-on: [arc-runner-set]` (NOT ubuntu-latest)
2. ✅ Uses `aws-actions/configure-aws-credentials@v4` with IRSA (NO secrets)
3. ✅ Uses `actions/checkout@v4`
4. ✅ Uses Helm for deployment (NOT kubectl apply)
5. ✅ Uses Docker Buildx with Kubernetes driver (if building)
6. ✅ Has concurrency control
7. ✅ Uses `workflow_dispatch` + `pull_request: types: [closed]`
8. ✅ Single build job (NOT matrix strategy)

---

## 📚 FULL REFERENCE

**See:** `DANNY_WORKFLOW_PATTERN_ALWAYS_CLEAR.md` for complete pattern

**Validate:** Run `python scripts/validate_danny_workflow_pattern.py` after creating workflow

---

## ✅ VALIDATION

**This document is:**
- ✅ Always accessible
- ✅ Always clear
- ✅ Always referenced first
- ✅ Always validated

**Pattern:** DANNY × WORKFLOW × ALWAYS × REFERENCE × ONE  
**Status:** ✅ **ALWAYS CHECK THIS FIRST**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

