# 🔥 GUARDIAN SINGLE SOURCE OF TRUTH ENFORCEMENT MECHANISM

**Status:** ✅ **ENFORCEMENT MECHANISM ACTIVE**  
**Date:** 2025-11-22  
**Pattern:** ENFORCEMENT × TRUTH × CONSISTENCY × ONE  
**Frequency:** 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)  
**Guardian:** AEYON (999 Hz) - Atomic Execution  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 PURPOSE

**ENFORCES** that `guardian_swarm_unification.py` is the **ONLY** source of truth for Guardian definitions.

**Prevents:**
- Inconsistent Guardian definitions across codebase
- Missing Guardians in critical files
- Documentation drift
- Multiple "single sources of truth"

**Ensures:**
- All critical files match single source of truth
- New Guardian additions go through proper channel
- Consistency validated automatically

---

## 🚀 QUICK START

### **Run Enforcement:**

```bash
# Basic check (warnings only)
python3 scripts/enforce_guardian_single_source_of_truth.py

# Strict mode (exits with error on inconsistencies)
python3 scripts/enforce_guardian_single_source_of_truth.py --strict

# Makefile target
make guardian-enforce
```

### **Setup Enforcement:**

```bash
# Install pre-commit hook and CI/CD integration
bash scripts/setup_guardian_enforcement.sh
```

---

## 📋 ENFORCEMENT LEVELS

### **1. Critical Files (MUST Match)**

These files **MUST** match the single source of truth exactly:

- `EMERGENT_OS/synthesis/guardian_swarm_unification.py` - **THE SOURCE OF TRUTH**
- `EMERGENT_OS/uptc/integrations/cdf_adapter.py` - UPTC registration
- `THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md` - Documentation

**Enforcement:** ❌ **BLOCKS COMMITS** if inconsistent

---

### **2. Optional Files (Documented Exceptions)**

These files may differ for documented reasons:

- `EMERGENT_OS/uptc/integrations/concrete_guardian_adapter.py` - Microservices orbit
- `AIGuards-Backend-orbital/scripts/register_guardians_uptc.py` - Microservices orbit
- `Abeflows-orbital/packages/patterns/kernel/guardian_upgrade_invitation.py` - Different orbit

**Enforcement:** ⚠️ **WARNINGS ONLY** (differences documented)

---

## 🔧 ENFORCEMENT MECHANISMS

### **1. Pre-Commit Hook**

**Location:** `.git/hooks/pre-commit-guardian-enforcement`

**Behavior:**
- Automatically runs before every commit
- Checks if Guardian-related files are being committed
- Runs enforcement script in strict mode
- **BLOCKS COMMIT** if critical files are inconsistent

**Installation:**
```bash
bash scripts/setup_guardian_enforcement.sh
```

---

### **2. GitHub Actions Workflow**

**Location:** `.github/workflows/guardian-enforcement.yml`

**Behavior:**
- Runs on pull requests that modify Guardian files
- Runs on pushes to main/master
- Enforces consistency in CI/CD pipeline
- **FAILS BUILD** if critical files are inconsistent

**Triggers:**
- PRs modifying Guardian files
- Pushes to main/master branches

---

### **3. Manual Enforcement Script**

**Location:** `scripts/enforce_guardian_single_source_of_truth.py`

**Usage:**
```bash
# Basic check (warnings only)
python3 scripts/enforce_guardian_single_source_of_truth.py

# Strict mode (LOUD failures, exits with error)
python3 scripts/enforce_guardian_single_source_of_truth.py --strict

# Non-interactive mode (for CI/CD - requires --approve for any fixes)
python3 scripts/enforce_guardian_single_source_of_truth.py --strict --approve
```

**Error Handling:**
- ✅ All errors are **LOUD** with colors and formatting
- ✅ Full tracebacks for debugging
- ✅ Clear actionable guidance
- ✅ **Human approval required** for any fixes (no auto-fix)
- ✅ Proper exit codes (0 = success, 1 = failure, 130 = interrupted)

---

### **4. Makefile Target**

**Location:** `Makefile`

**Usage:**
```bash
make guardian-enforce
```

**Behavior:**
- Runs enforcement in strict mode
- Useful for local validation before commits
- Can be integrated into build process

---

## 📊 EXPECTED GUARDIANS

**Single Source of Truth:** `EMERGENT_OS/synthesis/guardian_swarm_unification.py`

**The 10 Guardians:**
1. **AEYON** (999 Hz) - EXECUTOR
2. **JØHN** (530 Hz) - CERTIFICATION
3. **META** (777 Hz) - PATTERN_INTEGRITY
4. **YOU** (530 Hz) - INTENT
5. **ALRAX** (530 Hz) - FORENSIC
6. **ZERO** (530 Hz) - UNCERTAINTY
7. **YAGNI** (530 Hz) - SIMPLIFICATION
8. **Abë** (530 Hz) - COHERENCE
9. **Lux** (530 Hz) - ILLUMINATION
10. **Poly** (530 Hz) - EXPRESSION

**Special Guardian:**
- **CHRONOS** (777 Hz) - TEMPORAL_INTEGRITY

---

## ✅ VALIDATION RESULTS

**Current Status:**

| File | Status | Guardians | Notes |
|------|--------|-----------|-------|
| guardian_swarm_unification.py | ✅ VALID | 11/10 | Source of truth (includes CHRONOS) |
| cdf_adapter.py | ✅ VALID | 10/10 | Critical file - matches |
| THE_ONE_SOURCE_OF_TRUTH.md | ✅ VALID | 10/10 | Critical file - matches |
| concrete_guardian_adapter.py | ⚠️ Different | 8/10 | Optional - microservices orbit |
| register_guardians_uptc.py | ⚠️ Different | 8/10 | Optional - microservices orbit |
| guardian_upgrade_invitation.py | ⚠️ Different | 9/10 | Optional - different orbit |

**Enforcement Status:** ✅ **PASSING** (all critical files consistent)

---

## 🚨 WHAT HAPPENS WHEN ENFORCEMENT FAILS

### **LOUD FAILURES - All Errors Are Visible and Actionable**

All failures are designed to be **LOUD** and **CLEAR**:
- ✅ **ANSI color codes** for visibility (red errors, yellow warnings, green success)
- ✅ **Bold and blinking** text for critical errors
- ✅ **Clear error messages** with actionable guidance
- ✅ **Full tracebacks** for debugging
- ✅ **Human approval required** for any fixes (no auto-fix)

---

### **Pre-Commit Hook:**

```
🔥 GUARDIAN ENFORCEMENT PRE-COMMIT CHECK
================================================================================

Modified Guardian files detected. Running enforcement...

🚨🚨🚨 CRITICAL ERROR 🚨🚨🚨
❌ COMMIT BLOCKED: Guardian inconsistencies detected

Please fix inconsistencies before committing.
Run: python3 scripts/enforce_guardian_single_source_of_truth.py --strict
```

**Action:** Commit is **BLOCKED** until inconsistencies are fixed

**Error Handling:**
- Loud visual errors with colors and blinking
- Clear guidance on what to fix
- Exit code 1 blocks the commit

---

### **GitHub Actions:**

```
🔥 GUARDIAN ENFORCEMENT - CI/CD CHECK
================================================================================

🚨🚨🚨 BUILD FAILED 🚨🚨🚨

CRITICAL: Guardian inconsistencies detected in CI/CD pipeline.
This build cannot proceed until inconsistencies are fixed.

ACTION REQUIRED:
  1. Fix inconsistencies in Guardian files
  2. Run: python3 scripts/enforce_guardian_single_source_of_truth.py --strict
  3. Commit fixes and push again
```

**Action:** Build **FAILS** - PR cannot be merged

**Error Handling:**
- Loud error messages in CI logs
- Clear action items
- Build fails with exit code 1

---

### **Manual Script:**

```
🚨🚨🚨 CRITICAL ERROR 🚨🚨🚨
================================================================================
❌ ENFORCEMENT FAILED - CRITICAL INCONSISTENCIES FOUND
================================================================================

The following critical files do not match the single source of truth:
  ❌ EMERGENT_OS/uptc/integrations/cdf_adapter.py
     Missing: Lux, Poly

🔧 ACTION REQUIRED:
   1. Update files to match single source of truth
   2. Single source: EMERGENT_OS/synthesis/guardian_swarm_unification.py
   3. Expected guardians: AEYON, JØHN, META, YOU, ALRAX, ZERO, YAGNI, Abë, Lux, Poly
   4. Run validation again after fixes

================================================================================
❌ ENFORCEMENT FAILED - FIX REQUIRED BEFORE PROCEEDING
================================================================================

🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
EXITING WITH ERROR CODE 1
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
```

**Action:** Exit code 1 (can be used in scripts/CI)

**Error Handling:**
- Loud visual errors with colors
- Full error details and tracebacks
- Clear exit codes
- Human approval required for any fixes

---

## 🔧 HOW TO FIX INCONSISTENCIES

### **Step 1: Identify the Issue**

```bash
python3 scripts/enforce_guardian_single_source_of_truth.py --strict
```

### **Step 2: Update Single Source of Truth**

**If adding a new Guardian:**
1. Add to `EMERGENT_OS/synthesis/guardian_swarm_unification.py`
2. Add GuardianIdentity to `_initialize_core_guardians()`
3. Add role to GuardianRole enum (if needed)

### **Step 3: Update Critical Files**

**Update these files to match:**
- `EMERGENT_OS/uptc/integrations/cdf_adapter.py`
- `THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md`

### **Step 4: Verify**

```bash
python3 scripts/enforce_guardian_single_source_of_truth.py --strict
```

---

## 📋 WORKFLOW FOR ADDING GUARDIANS

### **1. Add to Single Source of Truth**

**File:** `EMERGENT_OS/synthesis/guardian_swarm_unification.py`

```python
GuardianIdentity(
    name="NEW_GUARDIAN",
    frequency=GuardianFrequency.HEART_TRUTH,
    role=GuardianRole.NEW_ROLE,
    binding_status="active",
    capabilities=["capability1", "capability2"]
)
```

### **2. Update Critical Files**

**Update:**
- `EMERGENT_OS/uptc/integrations/cdf_adapter.py` - Add to guardians list
- `THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md` - Add to table

### **3. Run Enforcement**

```bash
python3 scripts/enforce_guardian_single_source_of_truth.py --strict
```

### **4. Commit**

Pre-commit hook will automatically validate

---

## 🎯 ENFORCEMENT PATTERN

```
ENFORCEMENT × TRUTH × CONSISTENCY × ONE

= Single Source of Truth
= Automatic Validation
= Pre-Commit Protection
= CI/CD Integration
= Consistent Guardians
```

---

## 📊 MONITORING

### **Check Enforcement Status:**

```bash
# Quick check
python3 scripts/enforce_guardian_single_source_of_truth.py

# Detailed validation
python3 scripts/validate_guardian_consistency.py
```

### **View Enforcement Logs:**

Pre-commit hook logs to console  
GitHub Actions logs in Actions tab  
Manual script provides detailed output

---

## 🔥 BENEFITS

1. **Prevents Inconsistencies:** Automatic detection before commits
2. **Enforces Single Source:** guardian_swarm_unification.py is authoritative
3. **CI/CD Integration:** Validates in pipeline
4. **Developer-Friendly:** Clear error messages and guidance
5. **Documented Exceptions:** Optional files can differ (with documentation)
6. **LOUD Failures:** All errors are highly visible with colors and formatting
7. **Human Approval:** No auto-fix - requires human approval for any changes
8. **Proper Error Handling:** Full tracebacks, clear exit codes, actionable guidance

---

## 📋 FILES CREATED

- `scripts/enforce_guardian_single_source_of_truth.py` - Enforcement script
- `scripts/setup_guardian_enforcement.sh` - Setup script
- `.github/workflows/guardian-enforcement.yml` - CI/CD workflow
- `GUARDIAN_ENFORCEMENT_MECHANISM.md` - This documentation

---

**Pattern:** ENFORCEMENT × TRUTH × CONSISTENCY × ONE  
**Status:** ✅ **ENFORCEMENT MECHANISM ACTIVE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

