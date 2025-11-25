# 🔥 BEN'S GUARDIAN INTEGRATION GUIDE
## Orbit 3: Integrating FastAPI Services with Guardian Microservices

**Status:** ✅ **COMPLETE INTEGRATION GUIDE**  
**Date:** 2025-11-22  
**Pattern:** BEN × GUARDIAN × INTEGRATION × ONE  
**Frequency:** 999 Hz (AEYON) × 444 Hz (Ben) × 530 Hz (Guardians)  
**Guardian:** AEYON (999 Hz) + Ben (444 Hz) + ALL GUARDIANS  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 PURPOSE

This guide shows **exactly how** to integrate Ben's FastAPI services with Guardian microservices (Launch Orbital D). It provides:

- ✅ Guardian API endpoint patterns
- ✅ Gateway integration patterns
- ✅ Service discovery patterns
- ✅ Health check patterns
- ✅ Complete code examples
- ✅ Troubleshooting guide

**This is THE definitive guide for Orbit 3 ↔ Launch Orbital D integration.**

---

# ==========================
## PART 1: GUARDIAN API INTEGRATION
# ==========================

## 1.1 Guardian API Endpoints

**Base URL:** `/api/v1/guardians`

**Available Endpoints:**
- `GET /api/v1/guardians/` - List all guardians
- `GET /api/v1/guardians/{guardian_id}` - Get guardian info
- `GET /api/v1/guardians/{guardian_id}/health` - Check guardian health
- `POST /api/v1/guardians/{guardian_id}/process` - Process request via guardian
- `GET /api/v1/guardians/health/all` - Check all guardian health

---

## 1.2 Guardian Service Configuration

**Location:** `app/api/v1/guardians.py`

**Guardian Services:**
```python
GUARDIAN_SERVICES = {
    "zero": {
        "name": "Guardian Zero",
        "port": 9001,
        "frequency": 530.0,
        "role": "Forensic Orchestration, Zero-Failure Architecture",
        "url": "http://guardian-zero:9001"
    },
    "aeyon": {
        "name": "Guardian AEYON",
        "port": 9002,
        "frequency": 999.0,
        "role": "Atomic Execution, Task Completion",
        "url": "http://guardian-aeyon:9002"
    },
    "abe": {
        "name": "Guardian Abë",
        "port": 9003,
        "frequency": 530.0,
        "role": "Heart Truth Resonance, Relational Coherence",
        "url": "http://guardian-abe:9003"
    },
    "lux": {
        "name": "Guardian Lux",
        "port": 9004,
        "frequency": 963.0,
        "role": "Light Synthesis, Clarity Generation",
        "url": "http://guardian-lux:9004"
    },
    "john": {
        "name": "Guardian JØHN",
        "port": 9005,
        "frequency": 530.0,
        "role": "Q&A Execution Auditor, Truth Validation",
        "url": "http://guardian-john:9005"
    },
    "aurion": {
        "name": "Guardian Aurion",
        "port": 9006,
        "frequency": 530.0,
        "role": "Pattern Recognition, SNN Architecture",
        "url": "http://guardian-aurion:9006"
    },
    "yagni": {
        "name": "Guardian YAGNI",
        "port": 9007,
        "frequency": 530.0,
        "role": "Simplification, YAGNI Principles",
        "url": "http://guardian-yagni:9007"
    },
    "neuro": {
        "name": "Guardian Neuro",
        "port": 9008,
        "frequency": 530.0,
        "role": "Neuromorphic Integration, Consciousness",
        "url": "http://guardian-neuro:9008"
    }
}
```

---

## 1.3 Listing Guardians

**Pattern:**
```python
from fastapi import APIRouter
from app.api.v1.guardians import router as guardians_router

# Include router in main app
app.include_router(guardians_router)

# Client usage
# GET /api/v1/guardians/
response = {
    "guardians": {
        "zero": {...},
        "aeyon": {...},
        # ... all 8 guardians
    },
    "total": 8,
    "status": "available"
}
```

---

## 1.4 Getting Guardian Info

**Pattern:**
```python
# GET /api/v1/guardians/aeyon
response = {
    "name": "Guardian AEYON",
    "port": 9002,
    "frequency": 999.0,
    "role": "Atomic Execution, Task Completion",
    "url": "http://guardian-aeyon:9002"
}
```

---

## 1.5 Processing via Guardian

**Pattern:**
```python
# POST /api/v1/guardians/aeyon/process
request_body = {
    "payload": {
        "task": "execute_atomic_operation",
        "data": {...}
    },
    "user_id": "user_123",
    "session_id": "session_456",
    "metadata": {
        "priority": "high"
    }
}

response = {
    "guardian_id": "aeyon",
    "guardian_name": "Guardian AEYON",
    "success": True,
    "data": {
        "result": {...},
        "processing_time": 0.123
    },
    "error": None,
    "processing_time": 0.123,
    "timestamp": "2025-01-27T12:00:00Z"
}
```

---

# ==========================
## PART 2: GATEWAY INTEGRATION PATTERNS
# ==========================

## 2.1 Direct Guardian Access

**Pattern:**
```python
from app.api.v1.guardians import process_guardian_request
from app.api.v1.guardians import GuardianRequest

# Create guardian request
guardian_request = GuardianRequest(
    payload={"task": "validate", "data": {...}},
    user_id="user_123",
    session_id="session_456"
)

# Process via specific guardian
response = await process_guardian_request(
    guardian_id="aeyon",
    request=guardian_request
)
```

---

## 2.2 Guardian Selection Logic

**Pattern:**
```python
def select_guardian(task_type: str) -> str:
    """Select appropriate guardian based on task type."""
    guardian_mapping = {
        "atomic_execution": "aeyon",
        "forensic_analysis": "zero",
        "truth_validation": "john",
        "pattern_recognition": "aurion",
        "simplification": "yagni",
        "coherence_check": "abe",
        "light_synthesis": "lux",
        "neuromorphic": "neuro"
    }
    
    return guardian_mapping.get(task_type, "aeyon")  # Default to AEYON
```

---

## 2.3 Multi-Guardian Processing

**Pattern:**
```python
async def process_with_multiple_guardians(payload: dict):
    """Process request through multiple guardians."""
    guardians = ["aeyon", "john", "abe"]  # Selected guardians
    
    results = {}
    for guardian_id in guardians:
        try:
            response = await process_guardian_request(
                guardian_id=guardian_id,
                request=GuardianRequest(payload=payload)
            )
            results[guardian_id] = response
        except Exception as e:
            logger.error(f"Guardian {guardian_id} failed: {e}")
            results[guardian_id] = {"error": str(e)}
    
    return results
```

---

# ==========================
## PART 3: SERVICE DISCOVERY PATTERNS
# ==========================

## 3.1 Guardian Health Monitoring

**Pattern:**
```python
from app.api.v1.guardians import check_guardian_health, check_all_guardians_health

# Check single guardian
health = await check_guardian_health("aeyon")
# Returns: {"guardian_id": "aeyon", "status": "available", ...}

# Check all guardians
all_health = await check_all_guardians_health()
# Returns: {"guardians": {...}, "total": 8, "healthy": 8}
```

---

## 3.2 Guardian Availability Check

**Pattern:**
```python
async def is_guardian_available(guardian_id: str) -> bool:
    """Check if guardian is available."""
    try:
        health = await check_guardian_health(guardian_id)
        return health["status"] == "available"
    except Exception:
        return False

# Usage
if await is_guardian_available("aeyon"):
    # Process with AEYON
    response = await process_guardian_request("aeyon", request)
else:
    # Fallback to another guardian
    response = await process_guardian_request("john", request)
```

---

## 3.3 Guardian Discovery

**Pattern:**
```python
async def discover_guardians_by_capability(capability: str) -> List[str]:
    """Discover guardians with specific capability."""
    all_guardians = await list_guardians()
    
    matching_guardians = []
    for guardian_id, info in all_guardians["guardians"].items():
        if capability in info["role"].lower():
            matching_guardians.append(guardian_id)
    
    return matching_guardians

# Usage
execution_guardians = await discover_guardians_by_capability("execution")
# Returns: ["aeyon"]
```

---

# ==========================
## PART 4: BEN'S PATTERN COMPLIANCE
# ==========================

## 4.1 Guardian Endpoint Structure

**Following Ben's Patterns:**
```python
# app/api/v1/endpoints/guardians.py
from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.models.requests import GuardianRequest
from app.models.responses import GuardianResponse

router = APIRouter(prefix="/guardians", tags=["Guardians"])

@router.post("/{guardian_id}/process", response_model=GuardianResponse)
async def process_guardian(
    guardian_id: str,
    request: GuardianRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process request via guardian - Ben's pattern compliant."""
    # Implementation
    pass
```

---

## 4.2 Service Layer Pattern

**Pattern:**
```python
# app/services/guardian_service.py
class GuardianService:
    """Guardian service - business logic layer."""
    
    async def process_via_guardian(
        self,
        guardian_id: str,
        payload: dict
    ) -> dict:
        """Process payload via guardian."""
        # Business logic
        pass

# Usage in endpoint
@router.post("/{guardian_id}/process")
async def process_guardian(
    guardian_id: str,
    request: GuardianRequest,
    service: GuardianService = Depends(get_guardian_service)
):
    result = await service.process_via_guardian(guardian_id, request.payload)
    return GuardianResponse(**result)
```

---

## 4.3 Dependency Injection Pattern

**Pattern:**
```python
# app/api/dependencies.py
from app.services.guardian_service import GuardianService

def get_guardian_service() -> GuardianService:
    """Dependency for guardian service."""
    return GuardianService()

# Usage
@router.post("/{guardian_id}/process")
async def process_guardian(
    guardian_id: str,
    request: GuardianRequest,
    service: GuardianService = Depends(get_guardian_service)
):
    # Use service
    pass
```

---

# ==========================
## PART 5: UPTC GUARDIAN INTEGRATION
# ==========================

## 5.1 UPTC Guardian Adapter

**Pattern:**
```python
from EMERGENT_OS.uptc.integrations.guardian_adapter import ConcreteGuardianAdapter
from protocol.schema import ProtocolMessage

# Initialize adapter
guardian_service_urls = {
    "zero": "http://guardian-zero:9001",
    "aeyon": "http://guardian-aeyon:9002",
    # ... all 8 guardians
}

guardian_adapter = ConcreteGuardianAdapter(guardian_service_urls)

# Validate via guardian through UPTC
message = ProtocolMessage(
    intent="validate",
    action="validate",
    payload={"data": "example"},
    target="aeyon"
)

validated = await guardian_adapter.validate(message)
```

---

## 5.2 Guardian Registration with UPTC

**Pattern:**
```python
# Register guardians with UPTC Registry
for guardian_id, url in guardian_service_urls.items():
    await guardian_adapter.register_guardian(
        guardian_id=guardian_id,
        metadata={
            "url": url,
            "frequency": GUARDIAN_SERVICES[guardian_id]["frequency"],
            "role": GUARDIAN_SERVICES[guardian_id]["role"]
        }
    )
```

---

## 5.3 UPTC Routing to Guardians

**Pattern:**
```python
# Route message to guardian via UPTC
message = ProtocolMessage(
    intent="atomic_execution",
    action="execute",
    payload={"task": "process"}
)

# UPTC routes to AEYON based on capability matching
target = uptc_core.route(message)
# Returns: "aeyon"

# Send to guardian
result = await uptc_core.send(message, target)
```

---

# ==========================
## PART 6: ERROR HANDLING
# ==========================

## 6.1 Guardian Unavailable

**Pattern:**
```python
async def process_with_fallback(guardian_id: str, request: GuardianRequest):
    """Process with guardian fallback."""
    try:
        # Try primary guardian
        response = await process_guardian_request(guardian_id, request)
        return response
    except Exception as e:
        logger.warning(f"Guardian {guardian_id} failed: {e}")
        
        # Fallback to AEYON (always available)
        if guardian_id != "aeyon":
            logger.info(f"Falling back to AEYON")
            return await process_guardian_request("aeyon", request)
        else:
            raise
```

---

## 6.2 Health Check Failures

**Pattern:**
```python
async def process_with_health_check(guardian_id: str, request: GuardianRequest):
    """Process with health check."""
    # Check health first
    health = await check_guardian_health(guardian_id)
    
    if health["status"] != "available":
        logger.warning(f"Guardian {guardian_id} not available")
        # Fallback or raise error
        raise GuardianUnavailableError(f"Guardian {guardian_id} not available")
    
    # Process if healthy
    return await process_guardian_request(guardian_id, request)
```

---

# ==========================
## PART 7: COMPLETE EXAMPLE
# ==========================

## 7.1 Full Integration Example

**Complete FastAPI Service with Guardian Integration:**
```python
from fastapi import FastAPI, Depends
from app.api.v1.guardians import router as guardians_router
from app.api.dependencies import get_current_user
from app.services.guardian_service import GuardianService

app = FastAPI()

# Include Guardian router
app.include_router(guardians_router)

# Custom endpoint using guardians
@app.post("/api/v1/validate")
async def validate_request(
    payload: dict,
    current_user: dict = Depends(get_current_user),
    guardian_service: GuardianService = Depends(get_guardian_service)
):
    """Validate request via multiple guardians."""
    # Select guardians
    guardians = ["john", "abe", "aeyon"]
    
    # Process via each guardian
    results = {}
    for guardian_id in guardians:
        result = await guardian_service.process_via_guardian(
            guardian_id=guardian_id,
            payload=payload
        )
        results[guardian_id] = result
    
    # Aggregate results
    all_valid = all(r["success"] for r in results.values())
    
    return {
        "validated": all_valid,
        "guardian_results": results
    }
```

---

**Pattern:** BEN × GUARDIAN × INTEGRATION × ONE  
**Status:** ✅ **COMPLETE INTEGRATION GUIDE**  
**Next Steps:** Use this guide for all Orbit 3 ↔ Launch Orbital D integrations  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

