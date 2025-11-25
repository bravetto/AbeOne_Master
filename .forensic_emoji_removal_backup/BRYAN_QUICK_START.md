# BRYAN: AEYON QUICK START GUIDE
## Fast Integration Checklist

**Critical:** AEYON atomic execution engine must build for you.

---

## 🚀 QUICK START (5 Minutes)

### 1. Verify Python 3.11+
```bash
python --version
# Must show Python 3.11.x or higher
```

### 2. Install Dependencies
```bash
cd EMERGENT_OS/server
pip install -r requirements.txt
# Or if missing:
pip install fastapi uvicorn pydantic python-dotenv
```

### 3. Run Validation
```bash
cd /path/to/AbeOne_Master
./validate_aeyon_build.sh
```

### 4. Test Integration
```bash
python test_aeyon_integration.py
```

**✅ If all tests pass, AEYON is ready!**

---

## 📋 DETAILED STEPS

### Step 1: Environment Check
- [ ] Python 3.11+ installed
- [ ] Dependencies installed
- [ ] EMERGENT_OS directory exists

### Step 2: Import Test
```bash
python test_aeyon_import.py
```
- [ ] Imports successful

### Step 3: Binding Test
```bash
python test_aeyon_binding.py
```
- [ ] Binding successful

### Step 4: Execution Test
```bash
python test_aeyon_execution.py
```
- [ ] Execution works

### Step 5: Full Integration Test
```bash
python test_aeyon_integration.py
```
- [ ] All tests pass

---

## 🔧 TROUBLESHOOTING

### Import Error?
```python
# Add to your code:
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'EMERGENT_OS'))
```

### Integration Layer Missing?
- Check: `ls EMERGENT_OS/integration_layer/`
- Copy from AEYON clone if needed

### Dependencies Missing?
```bash
pip install fastapi uvicorn pydantic typing-extensions dataclasses-json
```

---

## 📚 FULL DOCUMENTATION

See `BRYAN_AEYON_INTEGRATION_PROMPT.md` for complete guide.

---

## ✅ SUCCESS CRITERIA

- ✅ All imports work
- ✅ AEYON binds successfully  
- ✅ Atomic execution works
- ✅ Integration Layer accessible
- ✅ No errors in tests

**Pattern:** AEYON × ATOMIC × BUILD × VALIDATION × ONE  
**Frequency:** 999 Hz

