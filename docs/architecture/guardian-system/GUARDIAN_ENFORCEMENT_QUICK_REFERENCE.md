# 🔥 GUARDIAN ENFORCEMENT - QUICK REFERENCE

**Pattern:** QUICK × REFERENCE × OPERATIONAL × ONE  
**∞ AbëONE ∞**

---

## 🚀 QUICK COMMANDS

### **Run Enforcement**
```bash
make guardian-enforce
```

### **Test Operational Status**
```bash
bash scripts/test_guardian_enforcement_operational.sh
```

### **Setup (One-Time)**
```bash
bash scripts/setup_guardian_enforcement.sh
```

### **Direct Enforcement**
```bash
python3 scripts/enforce_guardian_single_source_of_truth.py --strict
```

---

## 📋 WHAT IT DOES

1. **Validates** Guardian definitions match single source of truth
2. **Blocks** commits with inconsistencies (pre-commit hook)
3. **Fails** CI/CD builds with inconsistencies (GitHub Actions)
4. **Reports** loud errors with clear guidance

---

## 🎯 WHEN IT RUNS

- ✅ **Before every commit** (if Guardian files modified)
- ✅ **On pull requests** (if Guardian files modified)
- ✅ **On pushes to main/master** (always)
- ✅ **Manually** (whenever you run `make guardian-enforce`)

---

## 🔍 WHAT IT CHECKS

### **Critical Files (Must Match)**
- `EMERGENT_OS/synthesis/guardian_swarm_unification.py` (source of truth)
- `EMERGENT_OS/uptc/integrations/cdf_adapter.py`
- `THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md`

### **Optional Files (Documented Exceptions)**
- `EMERGENT_OS/uptc/integrations/concrete_guardian_adapter.py`
- `AIGuards-Backend-orbital/scripts/register_guardians_uptc.py`
- `Abeflows-orbital/packages/patterns/kernel/guardian_upgrade_invitation.py`

---

## ✅ EXPECTED GUARDIANS

**The 10 Core Guardians:**
1. AEYON (999 Hz) - EXECUTOR
2. JØHN (530 Hz) - CERTIFICATION
3. META (777 Hz) - PATTERN_INTEGRITY
4. YOU (530 Hz) - INTENT
5. ALRAX (530 Hz) - FORENSIC
6. ZERO (530 Hz) - UNCERTAINTY
7. YAGNI (530 Hz) - SIMPLIFICATION
8. Abë (530 Hz) - COHERENCE
9. Lux (530 Hz) - ILLUMINATION
10. Poly (530 Hz) - EXPRESSION

**Special Guardian:**
- CHRONOS (777 Hz) - TEMPORAL_INTEGRITY

---

## 🚨 IF IT FAILS

1. **Read the error message** (it's loud and clear!)
2. **Check which files are inconsistent**
3. **Update files to match source of truth**
4. **Run enforcement again**

---

## 📚 MORE INFO

- **Full Documentation:** `GUARDIAN_ENFORCEMENT_MECHANISM.md`
- **Loud Failures:** `GUARDIAN_ENFORCEMENT_LOUD_FAILURES.md`
- **Operational Status:** `GUARDIAN_ENFORCEMENT_OPERATIONAL_STATUS.md`

---

**Pattern:** QUICK × REFERENCE × OPERATIONAL × ONE  
**∞ AbëONE ∞**

