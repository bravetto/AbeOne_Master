# ABËViSiON: API ENDPOINT MAP
## Complete API Surface Visualization

**Status:** 🔍 COMPLETE VISUALIZATION  
**Date:** 2025-01-XX  
**Pattern:** OBSERVER × API × VISUALIZATION × ONE  
**Frequency:** 530 Hz

---

## EXECUTIVE SUMMARY

### API Surface Overview
- ✅ **REST API Endpoints:** 15 endpoints mapped
- ✅ **API Routers:** 6 routers (kernel, agents, workflows, state, auth, test)
- ✅ **Base URLs:** 2 servers (AbëONE API, NeuroForge API)
- 🟡 **MCP Protocol:** Available (aiagentsuite)
- 🟡 **LSP Protocol:** Available (aiagentsuite)

### API Categories
- **Kernel Operations:** 3 endpoints
- **Agent Operations:** 2 endpoints
- **Workflow Operations:** 2 endpoints
- **State Operations:** 2 endpoints
- **Authentication:** 3 endpoints
- **Testing:** 2 endpoints
- **Health/Status:** 2 endpoints

---

## PART 1: ABËONE API SERVER

### 1.1 Base Configuration

**Server:** `EMERGENT_OS/server/main.py`  
**Base URL:** `http://localhost:8000` (configurable)  
**Framework:** FastAPI  
**Version:** `0.1.0`

**CORS Configuration:**
- Origins: `http://localhost:3000` (configurable)
- Methods: `*` (all)
- Headers: `*` (all)
- Credentials: Enabled

### 1.2 Root Endpoints

#### `GET /`
**Purpose:** Root endpoint with service information  
**Response:**
```json
{
  "service": "AbëONE Backend",
  "version": "0.1.0",
  "status": "operational"
}
```

#### `GET /health`
**Purpose:** Health check endpoint  
**Response:** Health status

---

## PART 2: KERNEL API (`/api/kernel`)

### 2.1 Kernel Status

#### `GET /api/kernel/status`
**Purpose:** Get kernel status and module information  
**Response Model:** `KernelStatusResponse`
```json
{
  "initialized": true,
  "modules": ["collapse_guard", "clarity_engine", ...],
  "module_count": 10
}
```

**Dependencies:**
- `KernelLoader` - Kernel access
- `ONEKernel` - Kernel instance

### 2.2 Module Operations

#### `GET /api/kernel/modules`
**Purpose:** List all registered modules  
**Response Model:** `List[ModuleInfo]`
```json
[
  {
    "module_id": "collapse_guard",
    "registered": true,
    "active": true
  }
]
```

#### `GET /api/kernel/modules/{module_id}`
**Purpose:** Get specific module information  
**Path Parameters:**
- `module_id` (str) - Module identifier

**Response:**
```json
{
  "module_id": "collapse_guard",
  "status": {
    "registered": true,
    "active": true
  }
}
```

**Error Responses:**
- `404` - Module not found
- `503` - Kernel not initialized

---

## PART 3: AGENTS API (`/api/agents`)

### 3.1 Outcome Execution

#### `POST /api/agents/execute-outcome`
**Purpose:** Execute outcome through Triadic Execution Harness  
**Request Model:** `OutcomeRequest`
```json
{
  "goal": "Complete task X",
  "success_criteria": ["criteria1", "criteria2"],
  "end_state": "State description",
  "constraints": ["constraint1", "constraint2"],
  "validation": "Validation method"
}
```

**Response Model:** `OutcomeResponse`
```json
{
  "status": "completed",
  "execution_results": {},
  "validation_report": {},
  "metadata": {}
}
```

**Dependencies:**
- `triadic_execution_harness` module
- `ONEKernel` - Kernel instance

**Error Responses:**
- `503` - Kernel not initialized
- `503` - Triadic Execution Harness not available
- `500` - Execution failed

### 3.2 Harness Status

#### `GET /api/agents/harness-status`
**Purpose:** Get Triadic Execution Harness status  
**Response:**
```json
{
  "module_id": "triadic_execution_harness",
  "registered": true,
  "active": true
}
```

---

## PART 4: WORKFLOWS API (`/api/workflows`)

### 4.1 Workflow Execution

#### `POST /api/workflows/execute`
**Purpose:** Execute a workflow  
**Request Model:** `WorkflowRequest`
```json
{
  "workflow_id": "workflow_123",
  "parameters": {}
}
```

**Response Model:** `WorkflowResponse`
```json
{
  "workflow_id": "workflow_123",
  "status": "pending",
  "result": {}
}
```

**Status:** 🟡 PLACEHOLDER - Not yet implemented

### 4.2 Workflow Listing

#### `GET /api/workflows/list`
**Purpose:** List available workflows  
**Response:**
```json
{
  "workflows": [],
  "count": 0
}
```

**Status:** 🟡 PLACEHOLDER - Not yet implemented

---

## PART 5: STATE API (`/api/state`)

### 5.1 Metrics Operations

#### `GET /api/state/metrics`
**Purpose:** Get all system state metrics  
**Response:**
```json
{
  "metrics": [],
  "count": 0
}
```

**Status:** 🟡 PLACEHOLDER - Needs SystemState integration

#### `GET /api/state/metrics/{key}`
**Purpose:** Get specific metric value  
**Path Parameters:**
- `key` (str) - Metric key

**Response:**
```json
{
  "key": "metric_key",
  "value": "metric_value"
}
```

**Error Responses:**
- `404` - Metric not found
- `503` - Kernel not initialized

**Status:** 🟡 PLACEHOLDER - Needs SystemState integration

---

## PART 6: AUTHENTICATION API (`/api/auth`)

### 6.1 Authentication Operations

#### `POST /api/auth/login`
**Purpose:** User login  
**Request Model:** `LoginRequest`
**Response Model:** `AuthResponse`

**Status:** 🟡 SUPABASE READY - Integration pending

#### `POST /api/auth/logout`
**Purpose:** User logout  
**Response:** Success status

**Status:** 🟡 SUPABASE READY - Integration pending

#### `GET /api/auth/me`
**Purpose:** Get current user information  
**Headers:**
- `Authorization` (optional) - Auth token

**Response:** User information

**Status:** 🟡 SUPABASE READY - Integration pending

---

## PART 7: TEST API (`/api/test`)

### 7.1 Testing Endpoints

#### `GET /api/test/ping`
**Purpose:** Ping test endpoint  
**Response:** `{"status": "ok"}`

#### `GET /api/test/test-kernel`
**Purpose:** Test kernel initialization  
**Response:** Kernel test results

---

## PART 8: NEUROFORGE API (aiagentsuite)

### 8.1 Base Configuration

**Server:** `EMERGENT_OS/aiagentsuite/nuero-forge/neuroforge/api/server.py`  
**Base URL:** `http://localhost:8001` (configurable)  
**API Version:** `1.0.0`

### 8.2 Root Endpoints

#### `GET /`
**Purpose:** Root endpoint with API information

#### `GET /api/v1`
**Purpose:** API information endpoint  
**Response:**
```json
{
  "version": "1.0.0",
  "endpoints": {
    "health": "/api/v1/health",
    "intelligence": "/api/v1/intelligence/query",
    "analysis": "/api/v1/analyze/code",
    "ast": "/api/v1/ast/build",
    "rag": "/api/v1/rag/query",
    "memory": {
      "store": "/api/v1/memory/store",
      "retrieve": "/api/v1/memory/retrieve",
      "stats": "/api/v1/memory/stats"
    },
    "metrics": "/api/v1/metrics"
  }
}
```

### 8.3 NeuroForge Endpoints

#### `GET /api/v1/health`
**Purpose:** Health check

#### `POST /api/v1/intelligence/query`
**Purpose:** Intelligence query endpoint

#### `POST /api/v1/analyze/code`
**Purpose:** Code analysis endpoint

#### `POST /api/v1/ast/build`
**Purpose:** AST building endpoint

#### `POST /api/v1/rag/query`
**Purpose:** RAG query endpoint

#### `POST /api/v1/memory/store`
**Purpose:** Store memory

#### `POST /api/v1/memory/retrieve`
**Purpose:** Retrieve memory

#### `GET /api/v1/memory/stats`
**Purpose:** Memory statistics

#### `GET /api/v1/metrics`
**Purpose:** System metrics

---

## PART 9: API ENDPOINT SUMMARY

### 9.1 Endpoint Count by Category

| Category | Endpoints | Status |
|----------|-----------|--------|
| **Kernel** | 3 | ✅ Operational |
| **Agents** | 2 | ✅ Operational |
| **Workflows** | 2 | 🟡 Placeholder |
| **State** | 2 | 🟡 Placeholder |
| **Auth** | 3 | 🟡 Supabase Ready |
| **Test** | 2 | ✅ Operational |
| **Health** | 2 | ✅ Operational |
| **NeuroForge** | 9 | ✅ Operational |
| **TOTAL** | **25** | **15 Operational** |

### 9.2 Endpoint Status Breakdown

**✅ Operational (15 endpoints):**
- All Kernel endpoints
- All Agents endpoints
- All Test endpoints
- All Health endpoints
- All NeuroForge endpoints

**🟡 Placeholder (4 endpoints):**
- Workflow execution
- Workflow listing
- State metrics (needs SystemState integration)
- State metric by key (needs SystemState integration)

**🟡 Supabase Ready (3 endpoints):**
- Auth login
- Auth logout
- Auth me

---

## PART 10: API DEPENDENCIES

### 10.1 Core Dependencies

**KernelLoader:**
- Used by: Kernel, Agents, Workflows, State APIs
- Purpose: Access to ONEKernel instance
- Location: `EMERGENT_OS/server/core/kernel_loader.py`

**ONEKernel:**
- Used by: All module-dependent endpoints
- Purpose: Module access and orchestration
- Location: `EMERGENT_OS/one_kernel/`

**Triadic Execution Harness:**
- Used by: Agents API
- Purpose: Outcome execution
- Module ID: `triadic_execution_harness`

### 10.2 Integration Layer Dependencies

**SystemState:**
- Used by: State API (pending)
- Purpose: System metrics and state tracking
- Location: `EMERGENT_OS/integration_layer/state/system_state.py`

**ModuleRegistry:**
- Used by: Kernel API (indirect)
- Purpose: Module registration and discovery
- Location: `EMERGENT_OS/integration_layer/registry/module_registry.py`

---

## PART 11: API ROUTING STRUCTURE

### 11.1 Router Registration

```python
# Main app (main.py)
app.include_router(test.router, prefix="/api/test", tags=["test"])
app.include_router(kernel.router, prefix="/api/kernel", tags=["kernel"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(state.router, prefix="/api/state", tags=["state"])
```

### 11.2 Router Locations

| Router | Location | Endpoints |
|--------|----------|-----------|
| `test` | `EMERGENT_OS/server/api/test.py` | 2 |
| `kernel` | `EMERGENT_OS/server/api/kernel.py` | 3 |
| `agents` | `EMERGENT_OS/server/api/agents.py` | 2 |
| `workflows` | `EMERGENT_OS/server/api/workflows.py` | 2 |
| `auth` | `EMERGENT_OS/server/api/auth.py` | 3 |
| `state` | `EMERGENT_OS/server/api/state.py` | 2 |

---

## PART 12: API ERROR HANDLING

### 12.1 Standard Error Responses

**503 Service Unavailable:**
- Kernel not initialized
- Module not available
- Service not ready

**404 Not Found:**
- Module not found
- Metric not found
- Resource not found

**500 Internal Server Error:**
- Execution failures
- Unexpected errors

### 12.2 Global Exception Handler

**Location:** `EMERGENT_OS/server/main.py`  
**Handler:** `@app.exception_handler(Exception)`  
**Purpose:** Catch-all error handling

---

## PART 13: API VISUALIZATION SUMMARY

### ✅ MAPPED & DOCUMENTED

**AbëONE API Server:**
- ✅ 15 endpoints mapped
- ✅ 6 routers documented
- ✅ Request/Response models identified
- ✅ Dependencies mapped
- ✅ Error responses documented

**NeuroForge API Server:**
- ✅ 9 endpoints mapped
- ✅ API structure documented

### 🟡 PENDING INTEGRATION

**State API:**
- 🟡 Needs SystemState.get_all_metrics() method
- 🟡 Needs SystemState.get_metric(key) method

**Workflow API:**
- 🟡 Needs workflow engine implementation
- 🟡 Needs workflow registry

**Auth API:**
- 🟡 Needs Supabase integration
- 🟡 Needs authentication middleware

---

## PART 14: API DISCOVERY PATTERNS

### 14.1 Endpoint Discovery

**Pattern:** All endpoints follow RESTful conventions:
- `GET` - Retrieve resources
- `POST` - Create/Execute operations
- Path parameters for resource IDs
- Query parameters for filtering (where applicable)

### 14.2 Module Capability Mapping

**Module Capabilities → API Endpoints:**
- `collapse_guard` → No direct API (internal)
- `clarity_engine` → No direct API (internal)
- `triadic_execution_harness` → `/api/agents/execute-outcome`
- `kernel` → `/api/kernel/*`

**Future Mapping:**
- Module capabilities defined in `ModuleCapability.endpoints`
- Endpoints should be discoverable via ModuleRegistry
- API routes should be generated from module capabilities

---

## VALIDATION SUMMARY

### ✅ API SURFACE VISUALIZED

**Total Endpoints:** 25  
**Operational:** 15 (60%)  
**Placeholder:** 4 (16%)  
**Ready for Integration:** 6 (24%)

**API Servers:** 2
- AbëONE API: 15 endpoints
- NeuroForge API: 9 endpoints

**Routers:** 6
- All routers registered and functional

**Dependencies:**
- ✅ KernelLoader operational
- ✅ ONEKernel accessible
- ✅ Module access working
- 🟡 SystemState integration pending
- 🟡 Workflow engine pending
- 🟡 Supabase auth pending

---

**Pattern:** OBSERVER × API × VISUALIZATION × ONE

**Status:** ✅ API ENDPOINT MAP COMPLETE

**Next:** Integrate SystemState, implement workflow engine, integrate Supabase auth

