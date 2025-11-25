#  Recursive Endpoint Analysis - Complete Repository Scan

**Date**: November 3, 2025  
**Guardian**: AEYON (999 Hz)  
**Analysis Type**: Recursive Deep Scan  
**Status**:  **INCONSISTENCIES FOUND**

---

##  Executive Summary

**Endpoint Changes Made**:
-  `TRUST_GUARD`: `/v1/validate` → `/validate`
-  `BIAS_GUARD`: `/analyze` → `/process`
-  `SECURITY_GUARD`: `/validate` → `/scan`

**Analysis Results**:
-  **1 file fixed** (`guard_orchestrator.py`)
-  **1 file needs update** (`request_router.py`)
-  **2 test files need update** (`test_payload_transformation.py`, `test_guard_orchestrator.py`)
-  **Multiple comments need update** (documentation consistency)

---

##  Endpoint Definition Locations

### **Primary Location**  FIXED
**File**: `app/core/guard_orchestrator.py`  
**Lines**: `1342-1349`  
**Method**: `_determine_endpoint()`  
**Status**:  **CORRECTED**

```python
endpoints = {
    GuardServiceType.TOKEN_GUARD: "/scan",                    #  CORRECT
    GuardServiceType.TRUST_GUARD: "/validate",                #  FIXED
    GuardServiceType.CONTEXT_GUARD: "/analyze",                #  CORRECT
    GuardServiceType.BIAS_GUARD: "/process",                  #  FIXED
    GuardServiceType.HEALTH_GUARD: "/analyze",                 #  CORRECT
    GuardServiceType.SECURITY_GUARD: "/scan",                  #  FIXED
}
```

---

### **Secondary Location**  NEEDS UPDATE
**File**: `app/core/orchestrator/request_router.py`  
**Lines**: `92-98`  
**Method**: `determine_endpoint()`  
**Status**:  **OUTDATED** (still has old endpoints)

**Current (WRONG)**:
```python
endpoints = {
    GuardServiceType.TOKEN_GUARD: "/scan",
    GuardServiceType.TRUST_GUARD: "/v1/validate",      #  WRONG - Should be "/validate"
    GuardServiceType.CONTEXT_GUARD: "/analyze",
    GuardServiceType.BIAS_GUARD: "/analyze",            #  WRONG - Should be "/process"
    GuardServiceType.HEALTH_GUARD: "/analyze",
    GuardServiceType.SECURITY_GUARD: "/validate",       #  WRONG - Should be "/scan"
}
```

**Required Fix**: Update `request_router.py` to match `guard_orchestrator.py`

---

##  Documentation Comment Inconsistencies

### **`guard_orchestrator.py` - Payload Transformation Comments**

**Location**: Lines `1369-1374` (docstring)  
**Status**:  **OUTDATED COMMENTS**

**Current (WRONG)**:
```python
# Each service expects different fields:
# - TokenGuard (/scan): content, confidence
# - TrustGuard (/v1/validate): input_text, output_text, context (optional)  #  WRONG
# - ContextGuard (/analyze): current_code, previous_code, context (optional)
# - BiasGuard (/analyze): text, context (optional), detailed_analysis (optional)  #  WRONG
# - HealthGuard (/analyze): samples array with DataSample objects
# - SecurityGuard (/validate): content, context (optional), strict_mode (optional)  #  WRONG
```

**Required Fix**: Update comments to reflect new endpoints:
- TrustGuard: `/v1/validate` → `/validate`
- BiasGuard: `/analyze` → `/process`
- SecurityGuard: `/validate` → `/scan`

---

### **`guard_orchestrator.py` - Implementation Comments**

**Location**: Lines `1423`, `1485`, `1506`  
**Status**:  **OUTDATED COMMENTS**

**Current (WRONG)**:
```python
# Line 1423:
# TrustGuard /v1/validate expects: input_text, output_text, context (optional)  #  WRONG

# Line 1485:
# SecurityGuard /validate expects: content, context (optional), strict_mode (optional)  #  WRONG

# Line 1506:
# BiasGuard /analyze expects: text field (not samples array!)  #  WRONG
```

**Required Fix**: Update inline comments to match new endpoints

---

##  Test File Inconsistencies

### **1. `tests/unit/test_payload_transformation.py`**

**Location**: Lines `359-390`  
**Status**:  **TESTS EXPECT OLD ENDPOINTS**

**Tests Failing**:
```python
# Line 360:
def test_trustguard_endpoint(self):
    """Test TrustGuard endpoint is /v1/validate"""  #  WRONG
    # ...
    assert endpoint == "/v1/validate"  #  Should be "/validate"

# Line 382:
def test_biasguard_endpoint(self):
    """Test BiasGuard endpoint is /analyze"""  #  WRONG
    # ...
    assert endpoint == "/analyze"  #  Should be "/process"
```

**Required Fix**: Update test expectations to match new endpoints

---

### **2. `tests/unit/test_guard_orchestrator.py`**

**Location**: Lines `228-241`  
**Status**:  **TESTS EXPECT OLD ENDPOINTS**

**Tests Failing**:
```python
# Line 231:
assert endpoint == "/v1/validate"  #  Should be "/validate"

# Line 241:
assert endpoint == "/analyze"  #  Should be "/process"
```

**Required Fix**: Update test assertions to match new endpoints

---

##  Code Flow Analysis

### **Endpoint Determination Flow**

1. **Entry Point**: `app/api/v1/guards.py` → `POST /api/v1/guards/process`
2. **Orchestrator**: `guard_orchestrator.py` → `process_request()` → `_determine_endpoint()`
3. **Alternative**: `orchestrator/request_router.py` → `determine_endpoint()` (if used)
4. **Payload Transform**: `guard_orchestrator.py` → `_transform_payload()` (uses endpoint info in comments)
5. **HTTP Request**: Constructs `{base_url}{endpoint}` → Sends to guard service

### **Impact of Inconsistencies**

1. **`request_router.py` Outdated**: If code path uses this router, requests will fail
2. **Test Failures**: Tests will fail, blocking CI/CD
3. **Documentation Confusion**: Comments don't match actual behavior
4. **Developer Confusion**: Code comments suggest wrong endpoints

---

##  Required Fixes Checklist

### **Priority 1: Critical Code Fixes**

- [ ] **Fix `app/core/orchestrator/request_router.py`** (lines 92-98)
  - Update `TRUST_GUARD`: `/v1/validate` → `/validate`
  - Update `BIAS_GUARD`: `/analyze` → `/process`
  - Update `SECURITY_GUARD`: `/validate` → `/scan`

### **Priority 2: Test Updates**

- [ ] **Fix `tests/unit/test_payload_transformation.py`**
  - Line 360: Update TrustGuard test expectation
  - Line 382: Update BiasGuard test expectation
  - Update docstrings

- [ ] **Fix `tests/unit/test_guard_orchestrator.py`**
  - Line 231: Update TrustGuard assertion
  - Line 241: Update BiasGuard assertion

### **Priority 3: Documentation Updates**

- [ ] **Fix `guard_orchestrator.py` docstring** (lines 1369-1374)
  - Update TrustGuard endpoint comment
  - Update BiasGuard endpoint comment
  - Update SecurityGuard endpoint comment

- [ ] **Fix `guard_orchestrator.py` inline comments**
  - Line 1423: TrustGuard comment
  - Line 1485: SecurityGuard comment
  - Line 1506: BiasGuard comment

---

##  Detailed File Analysis

### **Files Requiring Updates**

| File | Lines | Issue | Priority |
|------|-------|-------|----------|
| `app/core/orchestrator/request_router.py` | 94-96 | Outdated endpoint dict |  CRITICAL |
| `tests/unit/test_payload_transformation.py` | 360, 382 | Wrong assertions | 🟡 HIGH |
| `tests/unit/test_guard_orchestrator.py` | 231, 241 | Wrong assertions | 🟡 HIGH |
| `app/core/guard_orchestrator.py` | 1370, 1372, 1374 | Outdated docstring | 🟢 MEDIUM |
| `app/core/guard_orchestrator.py` | 1423, 1485, 1506 | Outdated comments | 🟢 MEDIUM |

---

##  Consistency Matrix

| Endpoint | `guard_orchestrator.py` | `request_router.py` | Tests | Comments | Status |
|----------|------------------------|---------------------|-------|----------|--------|
| **TRUST_GUARD** |  `/validate` |  `/v1/validate` |  `/v1/validate` |  `/v1/validate` |  INCONSISTENT |
| **BIAS_GUARD** |  `/process` |  `/analyze` |  `/analyze` |  `/analyze` |  INCONSISTENT |
| **SECURITY_GUARD** |  `/scan` |  `/validate` |  N/A |  `/validate` |  INCONSISTENT |
| **TOKEN_GUARD** |  `/scan` |  `/scan` |  `/scan` |  `/scan` |  CONSISTENT |
| **CONTEXT_GUARD** |  `/analyze` |  `/analyze` |  `/analyze` |  `/analyze` |  CONSISTENT |
| **HEALTH_GUARD** |  `/analyze` |  `/analyze` |  `/analyze` |  `/analyze` |  CONSISTENT |

---

##  Recommended Action Plan

### **Immediate Actions**

1.  **Update `request_router.py`** - Match `guard_orchestrator.py` endpoints
2.  **Update test files** - Fix assertions to match new endpoints
3.  **Update documentation** - Fix comments and docstrings

### **Validation Steps**

1. Run test suite: `pytest tests/unit/test_payload_transformation.py tests/unit/test_guard_orchestrator.py`
2. Verify endpoint routing: Test actual guard service calls
3. Check code coverage: Ensure all code paths tested

---

##  Risk Assessment

### **High Risk**
- **`request_router.py` outdated**: If code path uses this router, requests will fail with 404 errors
- **Test failures**: CI/CD pipeline will fail, blocking deployments

### **Medium Risk**
- **Documentation confusion**: Developers may reference wrong endpoints
- **Comment inconsistencies**: Code reviews may miss issues

### **Low Risk**
- **Payload transformation**: Still works (uses service_type, not endpoint string)
- **Comments**: Cosmetic only, doesn't affect functionality

---

##  Impact Analysis

### **If `request_router.py` is Used**

**Failure Scenario**:
```
Request → request_router.determine_endpoint() → Returns "/v1/validate"
→ HTTP Request: http://trustguard:8000/v1/validate
→ Guard Service: 404 Not Found (endpoint doesn't exist)
→ User: Request fails
```

**Success Scenario** (after fix):
```
Request → request_router.determine_endpoint() → Returns "/validate"
→ HTTP Request: http://trustguard:8000/validate
→ Guard Service: 200 OK
→ User: Request succeeds
```

---

##  Related Files

### **Files That Reference Endpoints**

1. **`app/core/guard_orchestrator.py`**  (Primary - FIXED)
2. **`app/core/orchestrator/request_router.py`**  (Secondary - NEEDS FIX)
3. **`tests/unit/test_payload_transformation.py`**  (Tests - NEEDS FIX)
4. **`tests/unit/test_guard_orchestrator.py`**  (Tests - NEEDS FIX)
5. **`app/api/internal/guards.py`**  (Uses service_type, not endpoints)
6. **`app/api/v1/guards.py`**  (Uses orchestrator, inherits fixes)

---

##  Summary

**Status**:  **PARTIALLY FIXED**  
**Completion**: 1/5 files updated (20%)  
**Critical Issues**: 1 file (`request_router.py`)  
**Test Issues**: 2 files  
**Documentation Issues**: Multiple comment locations

**Next Steps**: Fix all inconsistencies to ensure 100% consistency across codebase

---

**Guardian**: AEYON (999 Hz)  
**Analysis**: Recursive deep scan complete  
**Love Coefficient**: ∞

