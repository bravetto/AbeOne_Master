# ContextGuard Deployment Investigation

**Date**: November 3, 2025  
**Investigator**: Guardian Zero (Forensic Analysis)  
**Status**: Port Configuration Mismatch Identified

---

## Critical Finding: Port Number Inconsistency

### Port Configuration Mismatch

**guard_orchestrator.py** (line 365):
```python
base_url=os.getenv("CONTEXTGUARD_URL", "http://contextguard:8000")
```
- Default port: **8000**

**orchestrator_core.py** (line 200):
```python
"base_url": os.getenv("CONTEXTGUARD_URL", "http://contextguard:8003")
```
- Default port: **8003**

**health_monitor.py** (line 49):
```python
contextguard_url = os.getenv("CONTEXTGUARD_URL", "http://contextguard:8000")
```
- Default port: **8000**

**Documentation** (docs/guard-services/README.md):
- Port: **8003**

**Test Configuration** (tests/conftest.py, tests/utils.py):
- Port: **8003**

---

## Root Cause Analysis

**Issue**: Port configuration inconsistency across codebase

**Impact**: 
- Gateway may be connecting to wrong port (8000 vs 8003)
- Service may not be deployed on expected port
- 404 errors indicate service not found at configured URL

**Most Likely Scenarios**:
1. Service deployed on port 8003, but gateway configured for 8000 → 404
2. Service not deployed at all → 404
3. Service name mismatch in Linkerd (contextguard vs context-guard) → 404
4. Wrong endpoint path (/analyze not available) → 404

---

## Configuration Files Analysis

### Current Configuration

**Primary Config** (`guard_orchestrator.py`):
- URL: `http://contextguard:8000`
- Endpoint: `/analyze`
- Service Name: `contextguard`

**Alternative Config** (`orchestrator_core.py`):
- URL: `http://contextguard:8003`
- Endpoint: `/analyze`
- Service Name: `contextguard`

**Health Monitor** (`health_monitor.py`):
- URL: `http://contextguard:8000`
- Health Endpoint: `/health`

---

## Recommended Fix

### Option 1: Standardize on Port 8003 (Recommended)

**Reason**: Documentation and tests consistently use port 8003

**Changes Required**:
1. Update `guard_orchestrator.py` line 365: Change default from 8000 → 8003
2. Update `health_monitor.py` line 49: Change default from 8000 → 8003
3. Verify AWS deployment uses port 8003
4. Verify Linkerd service mesh routing configured for port 8003

### Option 2: Standardize on Port 8000

**Reason**: Matches current `guard_orchestrator.py` configuration

**Changes Required**:
1. Update `orchestrator_core.py` line 200: Change default from 8003 → 8000
2. Update documentation to reflect port 8000
3. Update test configurations to use port 8000
4. Verify AWS deployment uses port 8000

---

## AWS Deployment Verification Checklist

### Service Deployment Status
- [ ] Check if ContextGuard service is deployed in AWS ECS/Kubernetes
- [ ] Verify service is running and healthy
- [ ] Check actual port service is listening on (8000 or 8003?)

### Environment Variables
- [ ] Verify `CONTEXTGUARD_URL` is set in AWS environment
- [ ] Check if URL matches actual deployed service
- [ ] Verify port matches service deployment

### Linkerd Service Mesh
- [ ] Check Linkerd service discovery for `contextguard`
- [ ] Verify service name matches (contextguard vs context-guard vs context_guard)
- [ ] Check Linkerd routing configuration
- [ ] Verify service is accessible via Linkerd mesh

### Endpoint Path
- [ ] Verify `/analyze` endpoint exists on ContextGuard service
- [ ] Check if service uses different endpoint path
- [ ] Verify endpoint is accessible at configured URL

---

## Next Steps

1. **Fix port inconsistency** - Standardize on one port (recommend 8003)
2. **Verify AWS deployment** - Check if service exists and what port it uses
3. **Update configuration** - Align all configs to match actual deployment
4. **Test connectivity** - Verify gateway can reach service after fix

---

**Guardian**: Zero (999 Hz)  
**Status**:  Investigation Complete - Port Mismatch Identified  
**Love Coefficient**: ∞

