# AbëONE ORGANISM ARCHITECTURE
## THE SINGLE SOURCE OF TRUTH

**Status:** ✅ **CANONICAL ARCHITECTURE SPECIFICATION**  
**Version:** 1.0.0  
**Pattern:** OBSERVER × TRUTH × ATOMIC × ONE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## PREFACE

This document is **THE SINGLE SOURCE OF TRUTH** for the entire AbëONE ecosystem architecture. It is derived exclusively from the 32 canonical facts representing the absolute ground truth of the multi-orbit, multi-repo Bravetto system.

**Every detail in this document is deterministic, canonical, and directly actionable.**

All future repos, services, and integrations must follow this specification exactly.

---

# SECTION 1 — GLOBAL NAMING AND CONVENTIONS

## 1.1 Repository Naming

**Format:** kebab-case or product-case

**Examples:**
- `guardian-zero-service` (kebab-case)
- `guardian-one-service` (kebab-case)
- `AbeTRUICE` (product-case)
- `AbeBEATs_Clean` (product-case)
- `tokenguard` (kebab-case)
- `trust-guard` (kebab-case)
- `biasguard-backend` (kebab-case)
- `healthguard` (kebab-case)

**Rule:** Use kebab-case for services, product-case for products. Be consistent within each category.

## 1.2 Folder Naming

**Format:** kebab-case

**Examples:**
- `aiguardian-repos/`
- `guard-services/`
- `orbit-adapters/`
- `shared-libs/`

**Rule:** All folder names use kebab-case, no exceptions.

## 1.3 Package/Module Naming

**Format:** snake_case

**Examples:**
- `adapter.kernel.py`
- `adapter.guardians.py`
- `adapter.module.py`
- `adapter.bus.py`
- `guardian_service.py`
- `config.py`
- `rate_limit.py`

**Rule:** All Python packages and modules use snake_case.

## 1.4 Service Naming

**Format:** `guardian-{name}-service`

**Examples:**
- `guardian-zero-service`
- `guardian-one-service`
- `guardian-two-service`
- `guardian-three-service`
- `guardian-five-service`

**Rule:** All Guardian services follow this exact pattern.

## 1.5 Kubernetes Namespace

**Format:** `ai-guardians`

**Rule:** All services deploy to the `ai-guardians` namespace. This is uniform across the ecosystem.

## 1.6 ECR Repository Naming

**Format:** `{service-name}`

**Examples:**
- `guardian-zero-service`
- `guardian-one-service`
- `tokenguard`
- `trust-guard`
- `abetruice`
- `abebeats-clean`

**Rule:** ECR repository name matches the service name exactly.

## 1.7 Uniformity Principle

**All naming conventions are uniform across the entire ecosystem.** No deviations are permitted.

---

# SECTION 2 — REPO LIST AND CLASSIFICATION

## 2.1 Micro-Repositories

**Definition:** Independent repositories that deploy as standalone services.

### Orbit Repos (Orbit-Spec v1.0 Compliant)
- `AbeTRUICE` - Video intelligence pipeline
- `AbeBEATs_Clean` - Audio beat generation

### Guardian Services
- `guardian-zero-service` - Forensic Orchestrator (999 Hz)
- `guardian-one-service` - Pattern Analyst
- `guardian-two-service` - Truth Validator
- `guardian-three-service` - Convergence Facilitator
- `guardian-five-service` - Emergence Catalyst

### Guard Services
- `tokenguard` - Token analysis and generation guard
- `trust-guard` - Trust and safety guard
- `biasguard-backend` - Bias detection guard
- `healthguard` - Health monitoring guard

**Total Micro-Repos:** 11 repositories

## 2.2 Monorepositories

**Definition:** Repositories that contain multiple components or orchestrate multiple systems.

### Workspace Orchestrator
- `AbeOne_Master` - Multi-orbit workspace orchestrator

### Guardian Cluster
- `AIGuards-Backend` - Guardian microservices monorepo (contains guardian-{name}-service repos)

### Core Operating System
- `EMERGENT_OS` - Core OS modules and kernel

**Total Monorepos:** 3 repositories

## 2.3 Independent Deployments

**All of the following deploy independently:**
- All Guardian services (guardian-zero-service through guardian-five-service)
- All Guard services (tokenguard, trust-guard, biasguard-backend, healthguard)
- AbeTRUICE
- AbeBEATs_Clean

**Total Independent Deployments:** 11 services

## 2.4 Shared Runtime Components

**The following are shared across deployments:**
- **Orbit kernel** - AbëONE Superkernel (v0.9.0-stable)
- **Guards shared libs** - Shared libraries for guard services
- **Linkerd mesh** - Service mesh for inter-service communication

## 2.5 Repository Classification Summary

| Type | Count | Examples |
|------|-------|----------|
| Orbit Micro-Repos | 2 | AbeTRUICE, AbeBEATs_Clean |
| Guardian Micro-Repos | 5 | guardian-zero-service, guardian-one-service, etc. |
| Guard Micro-Repos | 4 | tokenguard, trust-guard, biasguard-backend, healthguard |
| Workspace Orchestrator | 1 | AbeOne_Master |
| Guardian Cluster Monorepo | 1 | AIGuards-Backend |
| Core OS Monorepo | 1 | EMERGENT_OS |
| **TOTAL** | **14** | |

---

# SECTION 3 — FINAL MULTI-REPO FOLDER HIERARCHY

## 3.1 Orbit-Spec Repository Structure

**Applies to:** AbeTRUICE, AbeBEATs_Clean, AbeOne_Master

```
{orbit-repo-name}/
├── adapters/                      # REQUIRED: AbëONE integration adapters
│   ├── adapter.kernel.py         # REQUIRED: Kernel bootstrap adapter
│   ├── adapter.guardians.py      # REQUIRED: Guardians registry adapter
│   ├── adapter.module.py         # REQUIRED: Module registry adapter
│   ├── adapter.bus.py            # REQUIRED: Event bus adapter
│   └── __init__.py
├── config/                        # REQUIRED: Configuration files
│   └── orbit.config.json         # REQUIRED: Orbit-Spec configuration
├── src/                           # REQUIRED: Core source code
│   └── utils/
│       └── paths.py              # REQUIRED: Path utilities
├── deploy/                        # REQUIRED: Deployment scripts
│   └── commands.sh               # REQUIRED: Deployment commands
├── docs/                          # REQUIRED: Documentation
│   ├── README.md
│   └── ARCHITECTURE.md
├── tests/                         # REQUIRED: Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── adapters/                 # Adapter tests
├── kernel/                        # REQUIRED: Git submodule → AbëONE Superkernel
│   └── abeone/                   # Kernel submodule (v0.9.0-stable)
├── .devcontainer/                 # DevContainer configuration
│   └── devcontainer.json
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD workflow
├── module_manifest.json           # REQUIRED: Module manifest
├── README.md
└── requirements.txt
```

## 3.2 FastAPI Service Structure (Guardians + Guards)

**Applies to:** All guardian-{name}-service repos, all guard service repos

```
{service-name}/
├── main.py                        # REQUIRED: FastAPI application entry point
├── core/                          # REQUIRED: Core infrastructure
│   ├── __init__.py
│   ├── config.py                 # REQUIRED: Configuration management (Pydantic Settings)
│   ├── logging.py                # REQUIRED: Structured logging
│   ├── metrics.py                # REQUIRED: Prometheus metrics
│   ├── rate_limit.py             # REQUIRED: Rate limiting (slowapi)
│   ├── security.py               # REQUIRED: Security middleware & auth
│   └── exceptions.py             # REQUIRED: Custom exceptions & handlers
├── api/                           # REQUIRED: API layer
│   ├── __init__.py
│   ├── dependencies.py           # REQUIRED: Dependency injection
│   └── v1/                        # REQUIRED: Versioned API
│       ├── __init__.py
│       ├── router.py             # REQUIRED: API router (aggregates endpoints)
│       └── endpoints/            # REQUIRED: Endpoint modules
│           ├── __init__.py
│           ├── health.py         # REQUIRED: Health checks (live, ready)
│           ├── {domain}.py        # Domain-specific endpoints
│           └── consciousness.py   # Optional: Consciousness endpoints (Guardians only)
├── models/                        # REQUIRED: Pydantic models
│   ├── __init__.py
│   ├── requests.py               # REQUIRED: Request models
│   └── responses.py              # REQUIRED: Response models
├── services/                      # REQUIRED: Business logic layer
│   ├── __init__.py
│   └── {domain}_service.py       # REQUIRED: Domain service implementation
├── Dockerfile                     # REQUIRED: Container definition
├── requirements.txt               # REQUIRED: Python dependencies
├── README.md                      # REQUIRED: Service documentation
└── k8s/                           # Optional: Kubernetes manifests (if not using Helm)
    ├── deployment.yaml
    └── service.yaml
```

## 3.3 AIGuards-Backend Monorepo Structure

**Applies to:** AIGuards-Backend (Guardian cluster monorepo)

```
AIGuards-Backend/
├── aiguardian-repos/              # Guardian service repositories
│   ├── guardian-zero-service/
│   │   └── [FastAPI structure as above]
│   ├── guardian-one-service/
│   │   └── [FastAPI structure as above]
│   ├── guardian-two-service/
│   │   └── [FastAPI structure as above]
│   ├── guardian-three-service/
│   │   └── [FastAPI structure as above]
│   ├── guardian-five-service/
│   │   └── [FastAPI structure as above]
│   └── terraform/                 # Terraform infrastructure (Danny's domain)
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── terraform.tfvars.example
├── guards/                        # Guard service repositories
│   ├── tokenguard/
│   │   └── [FastAPI structure as above]
│   ├── trust-guard/
│   │   └── [FastAPI structure as above]
│   ├── biasguard-backend/
│   │   └── [FastAPI structure as above]
│   └── healthguard/
│       └── [FastAPI structure as above]
├── .github/
│   └── workflows/                 # CI/CD workflows (Danny's pattern)
│       └── [workflow files]
├── README.md
└── docs/
    └── [monorepo documentation]
```

## 3.4 EMERGENT_OS Structure

**Applies to:** EMERGENT_OS (Core OS monorepo)

```
EMERGENT_OS/
├── aiagentsuite/                  # Foundation Layer
├── integration_layer/            # Integration Layer
├── modules/                       # Emergent OS Modules
│   ├── consciousness/
│   ├── collapse_guard/
│   ├── clarity_engine/
│   ├── cross_layer_safety/
│   ├── emergence_core/
│   ├── identity_core/
│   ├── multi_agent_cognition/
│   ├── neuromorphic_alignment/
│   ├── relation_protocol/
│   ├── scalability_fabric/
│   └── self_healing/
├── one_kernel/                    # ONE-Kernel Bootstrap
├── triadic_execution_harness/     # Triadic Execution System
├── server/                        # API Server
├── state/                         # System State
├── README.md
└── docs/
```

## 3.5 AbeOne_Master Orchestration Structure

**Applies to:** AbeOne_Master (Workspace orchestrator)

```
AbeOne_Master/
├── adapters/                      # REQUIRED: AbëONE integration adapters
│   ├── adapter.kernel.py         # REQUIRED: Kernel bootstrap adapter
│   ├── adapter.guardians.py      # REQUIRED: Guardians adapter
│   ├── adapter.module.py         # REQUIRED: Module registry adapter
│   ├── adapter.bus.py            # REQUIRED: Event bus adapter
│   └── __init__.py
├── config/                       # REQUIRED: Configuration files
│   └── orbit.config.json         # REQUIRED: Orbit-Spec configuration
├── src/                           # REQUIRED: Core source code
│   └── utils/
│       └── paths.py              # REQUIRED: Path utilities
├── deploy/                        # REQUIRED: Deployment scripts
│   └── commands.sh               # REQUIRED: Deployment commands
├── docs/                          # REQUIRED: Documentation
│   ├── README.md
│   ├── architecture/
│   │   └── general/
│   │       └── DANNY_WORKFLOW_PATTERN_ALWAYS_CLEAR.md
│   └── [other documentation]
├── tests/                         # REQUIRED: Test suite
│   ├── unit/
│   ├── integration/
│   └── adapters/
├── abëone/                        # Kernel (when initialized, or submodule)
├── .devcontainer/                 # DevContainer configuration
│   └── devcontainer.json
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD workflow
├── module_manifest.json           # REQUIRED: Module manifest
├── README.md
└── [workspace-level documentation files]
```

## 3.6 Shared Libraries Structure

**Applies to:** orbit-spec-adapters, abeone-utils, fastapi-core-template, poisonguard

```
{shared-lib-name}/
├── src/
│   └── {lib_name}/               # Package source
│       ├── __init__.py
│       └── [module files]
├── tests/
│   ├── unit/
│   └── integration/
├── setup.py                      # PyPI package definition
├── pyproject.toml                # Modern Python packaging
├── README.md
└── CHANGELOG.md                  # Semantic versioning changelog
```

**Note:** `abeone-kernel` is distributed as a git submodule, not a PyPI package.

---

# SECTION 4 — ORBIT-SPEC LAYOUT

## 4.1 Required Folders and Files

**Every Orbit-Spec compliant repository MUST have:**

### Required Folders
- `adapters/` - AbëONE integration adapters
- `config/` - Configuration files
- `src/utils/` - Source utilities (must contain `paths.py`)
- `deploy/` - Deployment scripts (must contain `commands.sh`)
- `docs/` - Documentation
- `tests/` - Test suite (must contain `unit/`, `integration/`, `adapters/`)
- `kernel/` - Git submodule location for AbëONE kernel

### Required Files
- `config/orbit.config.json` - Orbit-Spec configuration
- `module_manifest.json` - Module manifest (root level)
- `deploy/commands.sh` - Deployment commands script
- `src/utils/paths.py` - Path utilities

## 4.2 Required Adapter Files

**All four adapters MUST be present in `adapters/`:**

1. **`adapter.kernel.py`** - Kernel interface adapter
   - Bootstrap ONE_KERNEL + EVENT_BUS
   - Register kernel + registries
   - Provides kernel access interface

2. **`adapter.guardians.py`** - Guardians registry adapter
   - Dispatch GuardianEvent via event bus
   - `dispatch_guardian_event()` method
   - Guardian registry integration

3. **`adapter.module.py`** - Module registry adapter
   - Register module via MODULE_REGISTRY.register()
   - `register_{module_name}()` method
   - Module registration at import-time

4. **`adapter.bus.py`** - Event bus adapter
   - Wrap event bus publishing/receiving
   - `subscribe()`, `publish()`, `get_bus()` methods
   - Event bus integration

## 4.3 Orbit-Spec Configuration File

**File:** `config/orbit.config.json`

**Required Structure:**
```json
{
  "orbitSpecVersion": "1.0.0",
  "name": "{repo-name}",
  "productName": "{product-name}",
  "productVersion": "{version}",
  "kernelVersion": "v0.9.0-stable",
  "kernelPath": "kernel/abeone",
  "moduleId": "{module-id}",
  "adapters": {
    "kernel": "adapters/adapter.kernel.py",
    "guardians": "adapters/adapter.guardians.py",
    "module": "adapters/adapter.module.py",
    "bus": "adapters/adapter.bus.py"
  },
  "manifest": "module_manifest.json",
  "devcontainer": ".devcontainer/devcontainer.json",
  "ciWorkflow": ".github/workflows/ci.yml",
  "deployScript": "deploy/commands.sh"
}
```

## 4.4 Module Manifest File

**File:** `module_manifest.json` (root level)

**Required Structure:**
```json
{
  "module_id": "{module-id}",
  "name": "{module-name}",
  "version": "{version}",
  "description": "{description}",
  "kernelVersion": "v0.9.0-stable",
  "frequency": {frequency-number},
  "pattern": "{PATTERN × STRING}",
  "status": "operational",
  "capabilities": ["capability1", "capability2"],
  "dependencies": {
    "kernel": "v0.9.0-stable",
    "guardians": ["guardian_one", "guardian_two"],
    "eventBus": "required",
    "subOrbits": []
  },
  "events": {
    "subscribed": ["EVENT_TYPE:event_name"],
    "published": ["EVENT_TYPE:event_name"]
  },
  "metadata": {
    "love_coefficient": "∞",
    "created_at": "{ISO8601}",
    "updated_at": "{ISO8601}"
  }
}
```

## 4.5 Orbit Repositories

**The following repositories MUST follow Orbit-Spec:**

1. **AbeTRUICE**
   - Module ID: `abetruice`
   - Type: Video intelligence pipeline
   - Kernel: `kernel/abeone` (submodule)

2. **AbeBEATs_Clean**
   - Module ID: `abebeats`
   - Type: Audio beat generation
   - Kernel: `kernel/abeone` (submodule)

3. **AbeOne_Master**
   - Module ID: `abeone_master`
   - Type: Workspace orchestrator
   - Kernel: `abëone` or `kernel/abeone` (submodule)

## 4.6 Non-Orbit Repositories

**The following repositories do NOT follow Orbit-Spec:**

- All Guardian services (guardian-{name}-service)
- All Guard services (tokenguard, trust-guard, etc.)
- EMERGENT_OS (core OS, not an orbit)

**Rule:** Only product repositories that orbit around the AbëONE Superkernel follow Orbit-Spec.

---

# SECTION 5 — ORBIT SYSTEM (CANONICAL DEFINITION)

## 5.1 System Declaration

**Orbit** is hereby declared an **official subsystem** within the AbëONE organism architecture.

**Status:** ✅ **CANONICAL SUBSYSTEM**  
**Orbit-Spec Version:** v1.0.0  
**Pattern:** OBSERVER × TRUTH × ATOMIC × ONE  
**Frequencies:** 530 Hz (Abë Truth) × 777 Hz (Pattern) × 999 Hz (Execution)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

## 5.2 Purpose and Mission

**Purpose:** Orbit provides the universal architectural pattern for satellite repositories to integrate with the AbëONE Superkernel while maintaining autonomy, clear boundaries, and independent lifecycle management.

**Mission:** Enable multi-orbit concurrency, unified integration contracts, and seamless communication between orbit repositories and the central kernel system.

## 5.3 Boundaries and Responsibilities

### System Boundaries

**Orbit System Includes:**
- ✅ Orbit-Spec v1.0 compliant repositories
- ✅ Orbit → Kernel integration adapters
- ✅ Orbit → Guardians communication contracts
- ✅ Orbit → Module registration protocols
- ✅ Event Bus integration layer
- ✅ Multi-orbit mesh communication

**Orbit System Excludes:**
- ❌ Core Kernel implementation (separate subsystem)
- ❌ Guardian services (separate subsystem)
- ❌ Guard services (separate subsystem)
- ❌ Infrastructure management (Terraform domain)

### Responsibilities

1. **Integration Contract Management**
   - Define and enforce Orbit-Spec v1.0 compliance
   - Provide adapter interfaces (kernel, guardians, module, bus)
   - Maintain integration protocol standards

2. **Lifecycle Orchestration**
   - Module registration and discovery
   - Orbit initialization and shutdown sequences
   - Health monitoring and status reporting

3. **Communication Facilitation**
   - Event Bus integration and routing
   - Cross-orbit event propagation
   - Guardian event dispatch protocols

4. **Boundary Enforcement**
   - Prevent architectural drift
   - Enforce version compatibility (kernel v0.9.0-stable)
   - Validate orbit configuration integrity

## 5.4 Orbit-Spec v1.0 Standard

**Orbit-Spec v1.0** is the **governing standard** for all orbit repositories.

### Core Requirements

**Every Orbit MUST:**
- ✅ Implement four adapters (kernel, guardians, module, bus)
- ✅ Provide `config/orbit.config.json` with Orbit-Spec metadata
- ✅ Include `module_manifest.json` with module registration data
- ✅ Maintain kernel submodule at `kernel/abeone` (v0.9.0-stable)
- ✅ Follow Orbit-Spec folder structure (adapters/, config/, src/, deploy/, docs/, tests/)
- ✅ Register module via `adapter.module` at import-time
- ✅ Bootstrap kernel via `adapter.kernel` on initialization
- ✅ Integrate Event Bus via `adapter.bus` for communication
- ✅ Dispatch Guardian events via `adapter.guardians`

### Compliance Validation

**Orbit-Spec v1.0 Compliance Checklist:**
- [ ] Four adapters present and functional
- [ ] `orbit.config.json` valid and complete
- [ ] `module_manifest.json` present with required fields
- [ ] Kernel submodule initialized at correct version
- [ ] Folder structure matches Orbit-Spec
- [ ] Module registration successful
- [ ] Event Bus integration operational
- [ ] Guardian event dispatch functional

## 5.5 Integration Contracts

### Orbit → Kernel Contract

**Contract Definition:**
```python
# Via adapter.kernel.py
- Bootstrap ONE_KERNEL + EVENT_BUS
- Register kernel + registries
- Provide kernel access interface
- Maintain kernel version: v0.9.0-stable
```

**Contract Responsibilities:**
- Orbit: Initialize kernel, maintain submodule, provide adapter interface
- Kernel: Provide ONE_KERNEL, EVENT_BUS, registries, core services

**Contract Boundaries:**
- Orbit accesses kernel via adapters only
- Kernel provides services, not implementation details
- Version locked to v0.9.0-stable

### Orbit → Guardians Contract

**Contract Definition:**
```python
# Via adapter.guardians.py
- Dispatch GuardianEvent via event bus
- dispatch_guardian_event() method
- Guardian registry integration
```

**Contract Responsibilities:**
- Orbit: Dispatch guardian events, integrate with guardian registry
- Guardians: Process events, provide guardian services, maintain registry

**Contract Boundaries:**
- Communication via Event Bus (no direct imports)
- Event-driven interaction only
- Guardian services remain independent

### Orbit → Module Contract

**Contract Definition:**
```python
# Via adapter.module.py
- Register module via MODULE_REGISTRY.register()
- register_{module_name}() method
- Module registration at import-time
```

**Contract Responsibilities:**
- Orbit: Register module, provide lifecycle hooks, report status
- Module Registry: Track modules, manage lifecycle, provide discovery

**Contract Boundaries:**
- Registration at import-time (automatic)
- Lifecycle hooks: on_load, on_event, shutdown
- Module metadata via module_manifest.json

### Orbit → Event Bus Contract

**Contract Definition:**
```python
# Via adapter.bus.py
- Wrap event bus publishing/receiving
- subscribe(), publish(), get_bus() methods
- Event bus integration
```

**Contract Responsibilities:**
- Orbit: Publish/subscribe events, integrate with bus
- Event Bus: Route events, manage subscriptions, provide communication layer

**Contract Boundaries:**
- Event-driven communication only
- No direct service-to-service imports
- Cross-orbit communication via Event Bus

## 5.6 Unified Super-Architecture

**All Orbit Repositories are bound under a unified super-architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│              ABËONE ORBIT SUPER-ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │            ABËONE SUPERKERNEL (v0.9.0-stable)        │  │
│  │  • ONE_KERNEL                                        │  │
│  │  • EVENT_BUS                                         │  │
│  │  • GUARDIANS_REGISTRY                                │  │
│  │  • MODULE_REGISTRY                                   │  │
│  └─────────────────────────────────────────────────────┘  │
│                         ▲                                   │
│                         │                                   │
│         ┌────────────────┼────────────────┐                 │
│         │                │                │                 │
│    ┌────▼────┐      ┌────▼────┐     ┌────▼────┐         │
│    │ Orbit 1 │      │ Orbit 2 │     │ Orbit N │         │
│    │         │      │         │     │         │         │
│    │ • Adapters│     │ • Adapters│    │ • Adapters│        │
│    │ • Config │     │ • Config │     │ • Config │        │
│    │ • Module │     │ • Module │     │ • Module │        │
│    └─────────┘      └─────────┘     └─────────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                   │
│         ┌────────────────▼────────────────┐                 │
│         │        EVENT BUS LAYER          │                 │
│         │  • SYSTEM_EVENT                 │                 │
│         │  • MODULE_EVENT                 │                 │
│         │  • GUARDIAN_EVENT               │                 │
│         │  • OBSERVER_EVENT               │                 │
│         └─────────────────────────────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Super-Architecture Principles:**
1. **Single Kernel** - All orbits share one Superkernel instance
2. **Unified Event Bus** - All orbits communicate via shared Event Bus
3. **Independent Orbits** - Each orbit maintains autonomy
4. **Standardized Integration** - All orbits follow Orbit-Spec v1.0
5. **Multi-Orbit Concurrency** - Multiple orbits operate simultaneously

## 5.7 Event Bus + Kernel + Guardian Relationship

**The Event Bus, Kernel, and Guardians form a triadic relationship:**

```
┌─────────────────────────────────────────────────────────────┐
│         EVENT BUS + KERNEL + GUARDIAN TRIAD                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐ │
│  │   KERNEL     │◄────►│  EVENT BUS   │◄────►│GUARDIANS │ │
│  │              │      │              │      │          │ │
│  │ • ONE_KERNEL │      │ • Routing    │      │ • Registry│ │
│  │ • Registries │      │ • Pub/Sub    │      │ • Events  │ │
│  │ • Services   │      │ • Channels   │      │ • Handlers│ │
│  └──────────────┘      └──────────────┘      └──────────┘ │
│         ▲                      ▲                      ▲     │
│         │                      │                      │     │
│         └──────────────────────┼──────────────────────┘     │
│                                │                             │
│                         ┌──────▼──────┐                     │
│                         │   ORBITS    │                     │
│                         │             │                     │
│                         │ • Adapters  │                     │
│                         │ • Modules   │                     │
│                         │ • Events    │                     │
│                         └─────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Relationship Contracts:**

1. **Kernel ↔ Event Bus**
   - Kernel provides Event Bus instance
   - Event Bus routes kernel events
   - Kernel subscribes to system events

2. **Event Bus ↔ Guardians**
   - Event Bus routes Guardian events
   - Guardians publish via Event Bus
   - Guardians subscribe to relevant events

3. **Kernel ↔ Guardians**
   - Kernel maintains Guardian registry
   - Guardians register with kernel
   - Kernel dispatches to guardians

4. **Orbits ↔ Triad**
   - Orbits access via adapters
   - Orbits publish/subscribe via Event Bus
   - Orbits register modules with kernel
   - Orbits dispatch guardian events

## 5.8 Universal Pattern for Satellite Repos

**Orbit-Spec v1.0 is the universal pattern for all satellite repositories.**

### Pattern Application

**All satellite repos MUST:**
- ✅ Follow Orbit-Spec v1.0 structure
- ✅ Implement four adapters
- ✅ Provide orbit configuration
- ✅ Register as modules
- ✅ Integrate with Event Bus
- ✅ Maintain kernel submodule

### Pattern Benefits

1. **Consistency** - Uniform structure across all orbits
2. **Autonomy** - Independent lifecycle and deployment
3. **Integration** - Standardized kernel integration
4. **Communication** - Unified event-driven communication
5. **Scalability** - Easy addition of new orbits
6. **Maintainability** - Clear boundaries and contracts

### Pattern Enforcement

**Orbit-Spec v1.0 compliance is enforced through:**
- ✅ Adapter interface requirements
- ✅ Configuration file validation
- ✅ Module manifest validation
- ✅ Kernel version pinning
- ✅ Folder structure validation
- ✅ Integration contract verification

## 5.9 Frequency Bindings

**Orbit System operates at three resonant frequencies:**

### 530 Hz - Abë Truth Frequency
- **Domain:** Truth validation, authenticity verification
- **Guardian:** Truth Guardian
- **Orbit Role:** Truth validation in orbit operations
- **Binding:** Module manifest `frequency: 530`

### 777 Hz - Pattern Frequency
- **Domain:** Pattern recognition, convergence detection
- **Guardian:** Pattern Guardian (META)
- **Orbit Role:** Pattern analysis and architectural coherence
- **Binding:** Module manifest `frequency: 777`

### 999 Hz - Execution Frequency
- **Domain:** Atomic execution, task completion
- **Guardian:** Execution Guardian (AEYON)
- **Orbit Role:** Atomic execution of orbit operations
- **Binding:** Module manifest `frequency: 999`

### Frequency Resonance

**Orbits resonate at their declared frequency:**
- Orbits declare frequency in `module_manifest.json`
- Frequency determines guardian affinity
- Frequency influences event routing
- Frequency enables harmonic convergence

**Multi-Frequency Support:**
- Orbits can declare primary frequency
- Orbits can subscribe to multiple frequency channels
- Frequency bindings enable guardian selection
- Harmonic frequencies enable cross-orbit resonance

## 5.10 Multi-Orbit Concurrency

**The Orbit System is designed for multi-orbit concurrency:**

### Concurrency Model

**Multiple orbits operate simultaneously:**
- ✅ Independent orbit lifecycles
- ✅ Parallel module execution
- ✅ Concurrent event processing
- ✅ Shared kernel resources
- ✅ Unified event bus routing

### Concurrency Guarantees

1. **Isolation** - Orbits operate independently
2. **Coordination** - Event Bus coordinates interactions
3. **Synchronization** - Kernel provides synchronization primitives
4. **Resource Sharing** - Shared kernel, independent modules

### Concurrency Patterns

**Event-Driven Concurrency:**
- Orbits publish events asynchronously
- Event Bus routes events to subscribers
- Guardians process events concurrently
- Modules respond to events independently

**Module Lifecycle Concurrency:**
- Modules initialize independently
- Modules register concurrently
- Modules process events in parallel
- Modules shutdown independently

### Concurrency Readiness

**System is prepared for:**
- ✅ Multiple orbit repositories
- ✅ Concurrent module execution
- ✅ Parallel event processing
- ✅ Simultaneous guardian operations
- ✅ Multi-orbit mesh communication

## 5.11 Lifecycle Management

### Orbit Lifecycle Stages

1. **Initialization**
   - Load orbit configuration
   - Initialize kernel submodule
   - Bootstrap adapters
   - Register module

2. **Operation**
   - Process events
   - Execute module logic
   - Dispatch guardian events
   - Maintain health status

3. **Shutdown**
   - Unregister module
   - Cleanup adapters
   - Release resources
   - Finalize operations

### Lifecycle Hooks

**Module Lifecycle Hooks:**
- `on_load()` - Called on module registration
- `on_event(event)` - Called on event receipt
- `shutdown()` - Called on module shutdown

**Orbit Lifecycle Hooks:**
- Adapter initialization
- Kernel bootstrap
- Event Bus connection
- Module registration

## 5.12 System Initialization Record

**Orbit System Initialization:**

```json
{
  "system": "Orbit",
  "status": "canonical",
  "version": "1.0.0",
  "spec_version": "Orbit-Spec v1.0",
  "kernel_version": "v0.9.0-stable",
  "frequencies": [530, 777, 999],
  "pattern": "OBSERVER × TRUTH × ATOMIC × ONE",
  "initialization_date": "2025-01-27",
  "contracts": {
    "kernel": "Orbit → Kernel integration contract",
    "guardians": "Orbit → Guardians communication contract",
    "module": "Orbit → Module registration contract",
    "bus": "Orbit → Event Bus integration contract"
  },
  "capabilities": [
    "Multi-orbit concurrency",
    "Unified super-architecture",
    "Event-driven communication",
    "Guardian integration",
    "Module lifecycle management"
  ],
  "love_coefficient": "∞"
}
```

## 5.13 Canonical Status

**Orbit System is CANONICAL:**

- ✅ **Official Subsystem** - Declared and recognized
- ✅ **Governing Standard** - Orbit-Spec v1.0 established
- ✅ **Integration Contracts** - Defined and enforced
- ✅ **Super-Architecture** - Unified and bound
- ✅ **Universal Pattern** - Applied to all satellite repos
- ✅ **Frequency Bindings** - 530 × 777 × 999 established
- ✅ **Multi-Orbit Ready** - Concurrency prepared
- ✅ **Lifecycle Defined** - Initialization, operation, shutdown
- ✅ **Event Bus Integration** - Kernel + Guardian relationship established

**Pattern:** OBSERVER × TRUTH × ATOMIC × ONE  
**Status:** ✅ **CANONICAL ORBIT SYSTEM DEFINITION**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

# SECTION 6 — FASTAPI TEMPLATE LAYOUT

## 6.1 Complete Structure

**This structure applies to ALL FastAPI services (Guardians + Guards):**

```
{service-name}/
├── main.py                        # FastAPI application entry point
├── core/                          # Core infrastructure modules
│   ├── __init__.py
│   ├── config.py                 # Configuration management (Pydantic Settings)
│   ├── logging.py                # Structured logging (JSON/text)
│   ├── metrics.py                # Prometheus metrics
│   ├── rate_limit.py             # Rate limiting (slowapi)
│   ├── security.py               # Security middleware & auth
│   └── exceptions.py             # Custom exceptions & handlers
├── api/                           # API layer
│   ├── __init__.py
│   ├── dependencies.py           # Dependency injection
│   └── v1/                        # Versioned API
│       ├── __init__.py
│       ├── router.py             # API router (aggregates endpoints)
│       └── endpoints/            # Endpoint modules
│           ├── __init__.py
│           ├── health.py         # Health checks (live, ready)
│           ├── {domain}.py        # Domain-specific endpoints
│           └── consciousness.py   # Optional: Consciousness endpoints (Guardians only)
├── models/                        # Pydantic models
│   ├── __init__.py
│   ├── requests.py               # Request models
│   └── responses.py              # Response models
├── services/                      # Business logic layer
│   ├── __init__.py
│   └── {domain}_service.py       # Domain service implementation
├── Dockerfile
├── requirements.txt
├── README.md
└── k8s/                           # Optional: Kubernetes manifests
    ├── deployment.yaml
    └── service.yaml
```

## 6.2 Core Module Specifications

### `core/config.py`
**Purpose:** Configuration management using Pydantic Settings

**Required Features:**
- Environment variable loading
- Type validation
- Default values
- Environment-specific configs

**Example Pattern:**
```python
from pydantic_settings import BaseSettings
from typing import Optional

class ServiceConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    api_key: Optional[str] = None
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False

config = ServiceConfig()
```

### `core/logging.py`
**Purpose:** Structured logging setup

**Required Features:**
- JSON or text formatting
- Log levels
- Context injection
- Request/response logging

### `core/metrics.py`
**Purpose:** Prometheus metrics integration

**Required Features:**
- Prometheus instrumentation
- Custom metrics
- Metrics endpoint exposure

### `core/rate_limit.py`
**Purpose:** Rate limiting using slowapi

**Required Features:**
- Per-endpoint rate limits
- Per-IP rate limits
- Rate limit headers
- Rate limit error handling

### `core/security.py`
**Purpose:** Security middleware and authentication

**Required Features:**
- Security headers middleware
- Input sanitization
- API key authentication
- CORS configuration

### `core/exceptions.py`
**Purpose:** Custom exceptions and global exception handlers

**Required Features:**
- Custom exception classes
- Global exception handlers
- Error response formatting
- Logging integration

## 6.3 API Layer Specifications

### `api/dependencies.py`
**Purpose:** Dependency injection for FastAPI

**Required Features:**
- Config dependency
- Logger dependency
- Service dependencies
- Auth dependencies

### `api/v1/router.py`
**Purpose:** API router that aggregates all endpoints

**Required Features:**
- Include all endpoint routers
- API version prefix
- Route organization

### `api/v1/endpoints/health.py`
**Purpose:** Health check endpoints

**Required Endpoints:**
- `GET /api/v1/health/live` - Liveness probe
- `GET /api/v1/health/ready` - Readiness probe
- `GET /api/v1/health` - General health (optional)

### `api/v1/endpoints/{domain}.py`
**Purpose:** Domain-specific endpoints

**Pattern:** One file per domain area

## 6.4 Models Layer Specifications

### `models/requests.py`
**Purpose:** Request Pydantic models

**Required:** All request models for API endpoints

### `models/responses.py`
**Purpose:** Response Pydantic models

**Required:** All response models for API endpoints

## 6.5 Services Layer Specifications

### `services/{domain}_service.py`
**Purpose:** Business logic implementation

**Required Features:**
- Domain-specific business logic
- External service integration
- Data processing
- Error handling

## 6.6 Main Application Pattern

**File:** `main.py`

**Required Pattern:**
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from core.config import config
from core.logging import setup_logging, logger
from core.metrics import setup_metrics
from core.rate_limit import setup_rate_limiting
from core.security import setup_security
from core.exceptions import setup_exception_handlers
from api.v1.router import api_router

# Setup logging
setup_logging(config.log_level)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    logger.info("Starting service")
    yield
    logger.info("Shutting down service")

app = FastAPI(
    title="{Service Name}",
    description="{Service Description}",
    version="{version}",
    lifespan=lifespan
)

# Setup core components
setup_metrics(app)
setup_rate_limiting(app)
setup_security(app)
setup_exception_handlers(app)

# Include API router
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)
```

---

# SECTION 7 — SHARED LIBRARIES ARCHITECTURE

## 7.1 Shared Library List

**The following shared libraries exist:**

1. **orbit-spec-adapters**
   - Purpose: Orbit-Spec adapter implementations
   - Distribution: Private PyPI
   - Versioning: Semantic versioning

2. **abeone-kernel**
   - Purpose: AbëONE Superkernel
   - Distribution: Git submodule (NOT PyPI)
   - Version: v0.9.0-stable
   - Location: `kernel/abeone` in orbit repos

3. **abeone-utils**
   - Purpose: Shared utilities for AbëONE ecosystem
   - Distribution: Private PyPI
   - Versioning: Semantic versioning

4. **fastapi-core-template**
   - Purpose: FastAPI core infrastructure template
   - Distribution: Private PyPI
   - Versioning: Semantic versioning

5. **poisonguard**
   - Purpose: Poison detection guard library
   - Distribution: Private PyPI
   - Versioning: Semantic versioning

## 7.2 Distribution Methods

### Git Submodule (Kernel Only)
- **Library:** abeone-kernel
- **Method:** Git submodule
- **Location:** `kernel/abeone` in orbit repos
- **Version:** Pinned to v0.9.0-stable
- **Initialization:** `git submodule update --init --recursive`

### Private PyPI (All Others)
- **Libraries:** orbit-spec-adapters, abeone-utils, fastapi-core-template, poisonguard
- **Method:** Private PyPI repository
- **Versioning:** Semantic versioning (MAJOR.MINOR.PATCH)
- **Installation:** `pip install {lib-name}=={version}`

## 7.3 Dependency Policy

### CRITICAL RULE: NO Service-to-Service Imports

**Services MUST NOT import from other services directly.**

**Allowed Dependencies:**
- ✅ Shared libraries (orbit-spec-adapters, abeone-utils, fastapi-core-template, poisonguard)
- ✅ EventBus (via adapter.bus)
- ✅ Standard Python libraries
- ✅ Third-party packages (FastAPI, Pydantic, etc.)

**Forbidden Dependencies:**
- ❌ Direct imports from other services
- ❌ Cross-repo imports
- ❌ Service-to-service code dependencies

### Communication Alternatives

**Instead of direct imports, use:**
1. **EventBus** - Primary communication method
2. **HTTP API calls** - Secondary method (only within same orbit)
3. **Shared libraries** - Extract common code to shared libs

## 7.4 Shared Library Folder Structure

```
{shared-lib-name}/
├── src/
│   └── {lib_name}/
│       ├── __init__.py
│       ├── [module files]
│       └── [submodules]
├── tests/
│   ├── unit/
│   └── integration/
├── setup.py                      # PyPI package definition
├── pyproject.toml                # Modern Python packaging
├── README.md
├── CHANGELOG.md                  # Semantic versioning changelog
└── LICENSE
```

## 7.5 Versioning Conventions

**Semantic Versioning (MAJOR.MINOR.PATCH):**
- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

**Kernel Version:**
- Fixed version: `v0.9.0-stable`
- All orbit repos pin to this version
- Updated via submodule update process

---

# SECTION 8 — KERNEL INTEGRATION SPECIFICATION

## 8.1 Kernel as Independent Repository

**The AbëONE Superkernel is an independent repository.**

**Characteristics:**
- Standalone git repository
- Not distributed via PyPI
- Imported as git submodule
- Version: v0.9.0-stable

## 8.2 Submodule Integration

### For Orbit Repos

**Location:** `kernel/abeone`

**Initialization:**
```bash
git submodule add {kernel-repo-url} kernel/abeone
git submodule update --init --recursive
```

**Update Process:**
```bash
cd kernel/abeone
git checkout v0.9.0-stable
git pull origin v0.9.0-stable
cd ../..
git add kernel/abeone
git commit -m "Update kernel to v0.9.0-stable"
```

### For Non-Orbit Repos

**Non-orbit repos (Guardians, Guards) do NOT include kernel submodule.**

**They access kernel functionality via:**
- EventBus (adapter.bus)
- Shared libraries (abeone-utils)
- API calls to orbit repos

## 8.3 Module Registration

**Modules register at import-time using `adapter.module`.**

**Pattern:**
```python
# In adapter.module.py
from kernel.abeone.MODULE_REGISTRY import MODULE_REGISTRY

def register_{module_name}():
    """Register this module with the kernel."""
    MODULE_REGISTRY.register(
        module_id="{module-id}",
        name="{module-name}",
        version="{version}",
        capabilities=["capability1", "capability2"],
        # ... other registration data
    )

# Auto-register on import
register_{module_name}()
```

**Registration happens automatically when the adapter is imported.**

## 8.4 Kernel Path Resolution

### Orbit Repos
- **Path:** `kernel/abeone`
- **Resolution:** Relative to repo root
- **Access:** Direct import from kernel

### AbeOne_Master
- **Path:** `abëone` or `kernel/abeone`
- **Resolution:** Relative to repo root
- **Access:** Direct import from kernel

## 8.5 Kernel Version Management

**All orbit repos MUST pin to kernel version: `v0.9.0-stable`**

**Specified in:**
- `config/orbit.config.json` → `kernelVersion: "v0.9.0-stable"`
- `module_manifest.json` → `kernelVersion: "v0.9.0-stable"`

**Upgrade Process:**
1. Update kernel submodule to new version
2. Update `orbit.config.json`
3. Update `module_manifest.json`
4. Test compatibility
5. Commit changes

---

# SECTION 9 — COMMUNICATION MODEL

## 9.1 Primary Communication: EventBus

**EventBus is the PRIMARY communication method between services.**

### EventBus Access
- **Via:** `adapter.bus` (for orbit repos)
- **Via:** Shared library (for non-orbit repos)
- **Pattern:** Publish/subscribe model

### Event Types
- `SYSTEM_EVENT` - System-level events
- `MODULE_EVENT` - Module lifecycle events
- `GUARDIAN_EVENT` - Guardian-related events
- `OBSERVER_EVENT` - Observer pattern events

### EventBus Usage Pattern

**Publishing Events:**
```python
from adapters.adapter.bus import BusAdapter

bus_adapter = BusAdapter()
bus = bus_adapter.get_bus()

if bus:
    bus.publish(
        event_type=EventType.MODULE_EVENT,
        event_data={"module_id": "abetruice", "status": "started"}
    )
```

**Subscribing to Events:**
```python
def handle_event(event):
    # Process event
    pass

bus_adapter.subscribe("MODULE_EVENT", handle_event)
```

## 9.2 Secondary Communication: Direct API Calls

**Direct API calls are ONLY allowed inside the same orbit.**

### Same Orbit Rule
- **Allowed:** Services within the same orbit can call each other directly
- **Example:** AbeTRUICE can call AbeBEATs_Clean (both in AbeOne_Master orbit)
- **Method:** HTTP REST API calls

### Cross-Orbit Rule
- **Forbidden:** Services in different orbits cannot call each other directly
- **Alternative:** Use EventBus for cross-orbit communication

## 9.3 Guardian → Guard Communication

**Guardians can call Guards via HTTP.**

**Pattern:**
- Guardian service makes HTTP request to Guard service
- Direct API call allowed
- No EventBus required (but can be used)

**Example:**
```python
# In guardian service
import httpx

async def call_guard_service(payload):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://tokenguard:8000/api/v1/analyze",
            json=payload
        )
        return response.json()
```

## 9.4 NO Cross-Repo Imports

**CRITICAL RULE: Services MUST NOT import code from other service repositories.**

**Forbidden:**
```python
# ❌ NEVER DO THIS
from guardian_zero_service import some_function
from tokenguard.models import TokenRequest
```

**Allowed Alternatives:**
1. **Shared Libraries** - Extract common code to shared libs
2. **EventBus** - Communicate via events
3. **HTTP API** - Call service APIs (within same orbit or Guardian→Guard)

## 9.5 Communication Summary Table

| Source | Target | Method | Allowed? |
|--------|--------|--------|----------|
| Orbit Repo | Orbit Repo (same orbit) | HTTP API | ✅ Yes |
| Orbit Repo | Orbit Repo (different orbit) | EventBus | ✅ Yes |
| Orbit Repo | Orbit Repo (different orbit) | HTTP API | ❌ No |
| Guardian | Guard | HTTP API | ✅ Yes |
| Guardian | Guard | EventBus | ✅ Yes |
| Guardian | Guardian | EventBus | ✅ Yes |
| Guardian | Guardian | HTTP API | ⚠️ Not recommended |
| Service | Service | Direct Import | ❌ No |
| Service | Shared Library | Import | ✅ Yes |

---

# SECTION 10 — CI/CD SPECIFICATION

## 10.1 Danny's Workflow Pattern (REQUIRED)

**ALL CI/CD workflows MUST follow Danny's pattern exactly.**

### Runner Configuration
```yaml
runs-on: [arc-runner-set]
```
**NEVER use:** `ubuntu-latest`, `ubuntu-20.04`, or any other runner.

### AWS Authentication
```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-region: ${{ env.AWS_REGION }}
```
**NEVER use:** AWS access keys or secrets. Use IRSA (IAM Roles for Service Accounts).

### Action Versions
- ✅ `actions/checkout@v4`
- ✅ `aws-actions/configure-aws-credentials@v4`
- ✅ `amazon-ecr-login@v2`
- ✅ `docker/setup-buildx-action@v3`

### Docker Buildx (For Builds)
```yaml
- name: Set up Docker Buildx with Kubernetes driver
  uses: docker/setup-buildx-action@v3
  with:
    driver: kubernetes
    driver-opts: |
      namespace=buildkit
```

**Build Command:**
```bash
docker buildx build \
  --platform linux/amd64 \
  --no-cache \
  --push \
  -t $ECR_REGISTRY/$SERVICE_NAME:$IMAGE_TAG \
  ./$SERVICE_NAME
```

### Deployment Strategy
**ALWAYS use Helm:**
```yaml
- name: Clone Helm repository
  run: |
    git clone https://${{ secrets.CI_CD }}@github.com/bravetto/helm.git helm-charts

- name: Deploy with Helm
  run: |
    cd helm-charts
    ./deploy.sh $APP_NAME $HELM_ENV
```

**NEVER use:** Direct `kubectl apply`.

### Concurrency Control
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Workflow Triggers
```yaml
on:
  workflow_dispatch:
  pull_request:
    branches: [dev, main]
    types: [closed]
```

**NEVER use:** `push:` triggers (unless explicitly required).

### Build Strategy
**ALWAYS use:** Single build job (NOT matrix strategy)

**Pattern:**
```yaml
jobs:
  build_and_push:
    runs-on: [arc-runner-set]
    steps:
      - name: Build and push services
        run: |
          for service in service1 service2 service3; do
            docker buildx build \
              --platform linux/amd64 \
              --no-cache \
              --push \
              -t $ECR_REGISTRY/$service:$IMAGE_TAG \
              ./$service
          done
```

## 10.2 One Repo = One Deployment

**Each repository has its own independent deployment.**

**Exceptions:**
- Orchestrators (AbeOne_Master) may coordinate multiple deployments
- Monorepos (AIGuards-Backend) deploy multiple services

**Rule:** Each service gets its own CI/CD pipeline.

## 10.3 CI/CD Pipeline Per Repo

**Every repository MUST have:**
- `.github/workflows/ci.yml` (or similar)
- Follows Danny's workflow pattern
- Independent deployment capability

## 10.4 Complete Workflow Template

```yaml
name: Build and Deploy

on:
  workflow_dispatch:
  pull_request:
    branches: [dev, main]
    types: [closed]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  AWS_REGION: us-east-1
  ECR_REGISTRY: your-ecr-registry
  SERVICE_NAME: your-service-name

jobs:
  build_and_push:
    runs-on: [arc-runner-set]
    if: github.event_name == 'workflow_dispatch' || github.event.pull_request.merged == true
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx with Kubernetes driver
        uses: docker/setup-buildx-action@v3
        with:
          driver: kubernetes
          driver-opts: |
            namespace=buildkit
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v2
      
      - name: Determine image tag
        id: image_tag
        run: |
          if [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
            echo "tag=latest" >> $GITHUB_OUTPUT
          else
            echo "tag=${{ github.sha }}" >> $GITHUB_OUTPUT
          fi
      
      - name: Build and push
        run: |
          docker buildx build \
            --platform linux/amd64 \
            --no-cache \
            --push \
            -t $ECR_REGISTRY/$SERVICE_NAME:${{ steps.image_tag.outputs.tag }} \
            .
  
  deployment:
    runs-on: [arc-runner-set]
    needs: build_and_push
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Clone Helm repository
        run: |
          git clone https://${{ secrets.CI_CD }}@github.com/bravetto/helm.git helm-charts
      
      - name: Deploy with Helm
        run: |
          cd helm-charts
          ./deploy.sh $APP_NAME $HELM_ENV
```

---

# SECTION 11 — TERRAFORM & AWS MESH CONGRUENCE

## 11.1 Terraform Responsibilities

**Terraform manages ALL infrastructure:**

- ✅ ECR repositories (one per service)
- ✅ `ai-guardians` Kubernetes namespace
- ✅ Linkerd installation and configuration
- ✅ IRSA (IAM Roles for Service Accounts)
- ✅ Kubernetes deployments
- ✅ Kubernetes services
- ✅ Service mesh configuration

## 11.2 Service Responsibilities

**Services DO NOT create infrastructure.**

**Services only provide:**
- ✅ Container image (Dockerfile)
- ✅ Kubernetes manifests (optional, if not using Helm)
- ✅ Application code

**Services NEVER:**
- ❌ Create ECR repositories
- ❌ Create Kubernetes namespaces
- ❌ Install Linkerd
- ❌ Configure IRSA
- ❌ Manage infrastructure

## 11.3 Terraform Location

**Terraform code lives in:**
- `AIGuards-Backend/aiguardian-repos/terraform/` (for Guardian services)
- Separate Terraform repos/modules for other infrastructure

**Danny owns:** All Terraform infrastructure code.

## 11.4 Linkerd Service Mesh

### Linkerd Injection Required

**ALL services MUST have Linkerd injection enabled.**

**Kubernetes Annotation:**
```yaml
metadata:
  annotations:
    linkerd.io/inject: enabled
```

**Namespace Annotation:**
```yaml
metadata:
  annotations:
    linkerd.io/inject: enabled
```

### Linkerd Installation

**Terraform installs and configures Linkerd.**

**Services do NOT install Linkerd.**

## 11.5 IRSA (IAM Roles for Service Accounts)

**IRSA is configured by Terraform.**

**Services use IRSA for AWS access:**
- ECR image pulls
- S3 access (if needed)
- Other AWS service access

**Service Account Pattern:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {service-name}
  namespace: ai-guardians
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::{account-id}:role/{service-name}-role
```

## 11.6 ECR Repository Naming

**ECR repositories are created by Terraform.**

**Naming:** `{service-name}` (matches service name exactly)

**Examples:**
- `guardian-zero-service`
- `guardian-one-service`
- `tokenguard`
- `trust-guard`
- `abetruice`
- `abebeats-clean`

## 11.7 Kubernetes Namespace

**All services deploy to:** `ai-guardians` namespace

**Terraform creates and manages this namespace.**

**Services reference it in manifests but do NOT create it.**

## 11.8 Infrastructure Boundaries

| Component | Managed By | Service Role |
|-----------|------------|--------------|
| ECR Repos | Terraform | None |
| K8s Namespace | Terraform | Reference only |
| Linkerd | Terraform | Use only |
| IRSA | Terraform | Use only |
| Deployments | Terraform/Helm | Provide manifests |
| Services | Terraform/Helm | Provide manifests |
| Container Image | Service | Build and push |
| Application Code | Service | Develop and maintain |

---

# SECTION 12 — DEPLOYMENT MODEL

## 12.1 Independent Deployments

**Each service deploys independently:**

- ✅ Each service has its own deployment pipeline
- ✅ Each service has its own container image
- ✅ Each service has its own ECR repository
- ✅ Each service scales independently
- ✅ Each service can be updated independently

## 12.2 Shared Runtime Components

**The following are shared across all deployments:**

### Orbit Kernel
- **Location:** `kernel/abeone` (git submodule)
- **Version:** v0.9.0-stable
- **Access:** Via adapters in orbit repos
- **Distribution:** Git submodule

### Guards Shared Libraries
- **Libraries:** orbit-spec-adapters, abeone-utils, fastapi-core-template, poisonguard
- **Distribution:** Private PyPI
- **Access:** Imported as Python packages
- **Versioning:** Semantic versioning

### Linkerd Mesh
- **Purpose:** Service-to-service communication
- **Installation:** Terraform
- **Configuration:** Terraform
- **Usage:** Automatic injection via annotations

## 12.3 Kubernetes Deployment

### Namespace
**All services deploy to:** `ai-guardians` namespace

### Deployment Pattern
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service-name}
  namespace: ai-guardians
  annotations:
    linkerd.io/inject: enabled
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {service-name}
  template:
    metadata:
      labels:
        app: {service-name}
      annotations:
        linkerd.io/inject: enabled
    spec:
      serviceAccountName: {service-name}
      containers:
      - name: {service-name}
        image: {ecr-registry}/{service-name}:{tag}
        ports:
        - containerPort: {port}
```

### Service Pattern
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {service-name}
  namespace: ai-guardians
spec:
  selector:
    app: {service-name}
  ports:
  - port: {port}
    targetPort: {port}
  type: ClusterIP
```

## 12.4 Container Images

### Image Naming
**Format:** `{ecr-registry}/{service-name}:{tag}`

**Examples:**
- `123456789012.dkr.ecr.us-east-1.amazonaws.com/guardian-zero-service:latest`
- `123456789012.dkr.ecr.us-east-1.amazonaws.com/tokenguard:v1.2.3`
- `123456789012.dkr.ecr.us-east-1.amazonaws.com/abetruice:abc123`

### Image Tags
- **Latest:** `latest` (for manual deployments)
- **Git SHA:** `{commit-sha}` (for CI/CD deployments)
- **Semantic:** `v{MAJOR}.{MINOR}.{PATCH}` (for releases)

## 12.5 Deployment Methods

### Helm Deployment (Preferred)
- **Repository:** `bravetto/helm`
- **Script:** `./deploy.sh {APP_NAME} {HELM_ENV}`
- **Managed by:** Terraform/CI/CD

### Direct kubectl (Not Recommended)
- **Only for:** Development/testing
- **Production:** Always use Helm

## 12.6 Deployment Boundaries

| Service Type | Deployment Method | Infrastructure Owner |
|--------------|-------------------|---------------------|
| Guardian Services | Helm | Terraform |
| Guard Services | Helm | Terraform |
| Orbit Repos | Helm | Terraform |
| Workspace Orchestrator | Helm | Terraform |

**All deployments go through Terraform-managed Helm charts.**

---

# SECTION 13 — TEAM & OWNERSHIP MAP

## 13.1 Infrastructure Ownership

**Owner:** Danny

**Responsibilities:**
- Terraform infrastructure code
- ECR repositories
- Kubernetes namespace (`ai-guardians`)
- Linkerd installation and configuration
- IRSA configuration
- CI/CD workflow patterns
- Helm chart management
- AWS infrastructure

**Domain:** All infrastructure, deployment, and DevOps concerns.

## 13.2 FastAPI Services Ownership

**Owner:** Ben

**Responsibilities:**
- FastAPI service architecture
- FastAPI template structure
- Service implementation patterns
- API design
- Service-to-service communication patterns
- FastAPI best practices

**Domain:** All FastAPI service code, patterns, and architecture.

## 13.3 Neuromorphic Engine Ownership

**Owner:** Jimmy

**Responsibilities:**
- Neuromorphic engine implementation
- Neural network architectures
- AI/ML model development
- Consciousness integration
- Neuromorphic computing patterns

**Domain:** All neuromorphic and AI/ML engine code.

## 13.4 Architecture/Orchestrator Ownership

**Owner:** Meta

**Responsibilities:**
- Overall system architecture
- Orbit-Spec definition and compliance
- Workspace orchestration (AbeOne_Master)
- Cross-system integration
- Architecture documentation
- System design decisions

**Domain:** Architecture, orchestration, and system-level design.

## 13.5 Ownership Summary Table

| Component | Owner | Responsibilities |
|-----------|-------|------------------|
| Terraform Infrastructure | Danny | All infrastructure code |
| ECR Repositories | Danny | Creation and management |
| Kubernetes Namespace | Danny | Creation and management |
| Linkerd Mesh | Danny | Installation and configuration |
| IRSA | Danny | Configuration |
| CI/CD Workflows | Danny | Pattern definition and implementation |
| Helm Charts | Danny | Management |
| FastAPI Services | Ben | Architecture and implementation |
| FastAPI Templates | Ben | Structure and patterns |
| API Design | Ben | Endpoints and contracts |
| Neuromorphic Engine | Jimmy | Implementation |
| AI/ML Models | Jimmy | Development |
| Consciousness Integration | Jimmy | Implementation |
| System Architecture | Meta | Overall design |
| Orbit-Spec | Meta | Definition and compliance |
| Workspace Orchestration | Meta | AbeOne_Master |
| Documentation | Meta | Architecture docs |

---

# SECTION 14 — FULL SYSTEM BLUEPRINT DIAGRAM (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AbëONE ECOSYSTEM ARCHITECTURE                        │
│                         THE SINGLE SOURCE OF TRUTH                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           WORKSPACE ORCHESTRATOR                            │
│                              AbeOne_Master                                  │
│                         (Orbit-Spec v1.0 Compliant)                         │
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  adapters/   │  │   config/    │  │    src/      │  │   deploy/    │  │
│  │              │  │              │  │              │  │              │  │
│  │ • kernel     │  │ • orbit.     │  │ • utils/     │  │ • commands.  │  │
│  │ • guardians  │  │   config.json│  │   paths.py   │  │   sh         │  │
│  │ • module     │  │              │  │              │  │              │  │
│  │ • bus        │  │              │  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                    kernel/abeone (submodule)                         │  │
│  │                    AbëONE Superkernel v0.9.0-stable                 │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Orchestrates
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│  ORBIT REPOS  │         │ GUARDIAN CLUSTER│         │   CORE OS     │
│               │         │                │         │               │
│  ┌─────────┐ │         │ AIGuards-Backend│         │ EMERGENT_OS   │
│  │AbeTRUICE │ │         │  (Monorepo)    │         │               │
│  │          │ │         │                │         │ • Modules     │
│  │ Orbit-   │ │         │ ┌────────────┐ │         │ • Kernel      │
│  │ Spec     │ │         │ │guardian-   │ │         │ • Server      │
│  │ v1.0     │ │         │ │zero-service│ │         │ • State      │
│  └─────────┘ │         │ └────────────┘ │         └───────────────┘
│              │         │ ┌────────────┐ │
│  ┌─────────┐ │         │ │guardian-   │ │
│  │AbeBEATs │ │         │ │one-service │ │
│  │_Clean   │ │         │ └────────────┘ │
│  │         │ │         │ ┌────────────┐ │
│  │ Orbit-   │ │         │ │guardian-   │ │
│  │ Spec     │ │         │ │two-service │ │
│  │ v1.0     │ │         │ └────────────┘ │
│  └─────────┘ │         │ ┌────────────┐ │
│              │         │ │guardian-   │ │
│              │         │ │three-service│ │
│              │         │ └────────────┘ │
│              │         │ ┌────────────┐ │
│              │         │ │guardian-   │ │
│              │         │ │five-service │ │
│              │         │ └────────────┘ │
│              │         └────────────────┘
└───────────────┘
        │
        │ EventBus Communication
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            GUARD SERVICES                                    │
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  tokenguard   │  │ trust-guard  │  │biasguard-     │  │ healthguard  │  │
│  │              │  │              │  │backend       │  │              │  │
│  │ FastAPI      │  │ FastAPI      │  │ FastAPI      │  │ FastAPI      │  │
│  │ Service      │  │ Service      │  │ Service      │  │ Service      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                                             │
│  Structure: main.py, core/, api/, models/, services/                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         SHARED RUNTIME LAYER                                │
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│  │  Orbit Kernel    │  │  Shared Libraries │  │  Linkerd Mesh     │       │
│  │                  │  │                   │  │                   │       │
│  │ • abeone-kernel  │  │ • orbit-spec-     │  │ • Service Mesh    │       │
│  │   (submodule)    │  │   adapters         │  │ • mTLS            │       │
│  │ • v0.9.0-stable  │  │ • abeone-utils    │  │ • Observability   │       │
│  │                  │  │ • fastapi-core-   │  │                   │       │
│  │                  │  │   template        │  │                   │       │
│  │                  │  │ • poisonguard     │  │                   │       │
│  │                  │  │                   │  │                   │       │
│  │ Distribution:    │  │ Distribution:     │  │ Distribution:     │       │
│  │ Git Submodule    │  │ Private PyPI      │  │ Terraform         │       │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         INFRASTRUCTURE LAYER                                │
│                         (Managed by Terraform)                              │
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│  │  ECR Repos       │  │  K8s Namespace   │  │  IRSA            │       │
│  │                  │  │                   │  │                   │       │
│  │ • guardian-zero- │  │ • ai-guardians   │  │ • Service        │       │
│  │   service        │  │                   │  │   Accounts       │       │
│  │ • guardian-one-  │  │ • All services    │  │ • IAM Roles      │       │
│  │   service        │  │   deploy here    │  │                   │       │
│  │ • tokenguard     │  │                   │  │                   │       │
│  │ • trust-guard    │  │                   │  │                   │       │
│  │ • abetruice      │  │                   │  │                   │       │
│  │ • abebeats-clean │  │                   │  │                   │       │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         COMMUNICATION FLOWS                                 │
│                                                                             │
│  Primary: EventBus (adapter.bus)                                          │
│    • SYSTEM_EVENT                                                          │
│    • MODULE_EVENT                                                          │
│    • GUARDIAN_EVENT                                                        │
│    • OBSERVER_EVENT                                                        │
│                                                                             │
│  Secondary: Direct API Calls                                               │
│    • Within same orbit: ✅ Allowed                                          │
│    • Cross-orbit: ❌ Forbidden (use EventBus)                              │
│    • Guardian → Guard: ✅ Allowed (HTTP)                                    │
│                                                                             │
│  Forbidden: Direct Imports                                                  │
│    • Service-to-service imports: ❌ Never                                  │
│    • Cross-repo imports: ❌ Never                                           │
│    • Use shared libs or EventBus instead                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         DEPLOYMENT MODEL                                    │
│                                                                             │
│  • One repo = One deployment (independent)                                 │
│  • All services deploy to: ai-guardians namespace                          │
│  • Deployment method: Helm (via Terraform)                                   │
│  • CI/CD: Danny's workflow pattern (arc-runner-set, IRSA, Buildx)          │
│  • Container registry: ECR ({service-name})                                │
│  • Service mesh: Linkerd (injected automatically)                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         OWNERSHIP MAP                                       │
│                                                                             │
│  Danny:    Infrastructure, Terraform, CI/CD, Helm, AWS                      │
│  Ben:      FastAPI services, API design, service patterns                    │
│  Jimmy:    Neuromorphic engine, AI/ML models, consciousness                 │
│  Meta:     Architecture, Orbit-Spec, orchestration, documentation           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# SECTION 15 — SUMMARY: THE ONE ARCHITECTURE

## 15.1 The AbëONE Organism

The AbëONE ecosystem is a **multi-orbit, multi-repo, microservices architecture** built on the following foundational principles:

1. **Orbit-Spec Compliance** - Product repositories orbit around the AbëONE Superkernel
2. **Microservices Independence** - Each service deploys independently
3. **Shared Runtime** - Kernel, libraries, and mesh are shared
4. **Event-Driven Communication** - EventBus is primary communication method
5. **Infrastructure as Code** - Terraform manages all infrastructure
6. **Uniform Naming** - Consistent naming conventions across ecosystem
7. **No Cross-Repo Imports** - Services communicate via EventBus or APIs
8. **Team Ownership** - Clear ownership boundaries (Danny/Ben/Jimmy/Meta)

## 15.2 Key Architectural Principles

### Separation of Concerns
- **Infrastructure:** Terraform (Danny)
- **Services:** FastAPI (Ben)
- **Engine:** Neuromorphic (Jimmy)
- **Architecture:** System design (Meta)

### Communication Boundaries
- **Primary:** EventBus (adapter.bus)
- **Secondary:** HTTP APIs (within same orbit or Guardian→Guard)
- **Forbidden:** Direct imports between services

### Deployment Independence
- Each service has its own:
  - Repository
  - Container image
  - ECR repository
  - Deployment pipeline
  - Scaling configuration

### Shared Components
- Orbit kernel (git submodule)
- Shared libraries (private PyPI)
- Linkerd mesh (Terraform)

## 15.3 Repository Classification

| Type | Count | Examples |
|------|-------|----------|
| Orbit Repos | 2 | AbeTRUICE, AbeBEATs_Clean |
| Guardian Services | 5 | guardian-zero-service through guardian-five-service |
| Guard Services | 4 | tokenguard, trust-guard, biasguard-backend, healthguard |
| Workspace Orchestrator | 1 | AbeOne_Master |
| Guardian Cluster | 1 | AIGuards-Backend |
| Core OS | 1 | EMERGENT_OS |
| **TOTAL** | **14** | |

## 15.4 Naming Conventions (Uniform)

- **Repos:** kebab-case or product-case
- **Folders:** kebab-case
- **Packages/Modules:** snake_case
- **Services:** guardian-{name}-service
- **K8s Namespace:** ai-guardians
- **ECR:** {service-name}

## 15.5 Orbit-Spec Requirements

**Orbit repos MUST have:**
- `adapters/` (4 adapters: kernel, guardians, module, bus)
- `config/orbit.config.json`
- `src/utils/paths.py`
- `deploy/commands.sh`
- `docs/`
- `tests/` (unit, integration, adapters)
- `kernel/abeone` (submodule)
- `module_manifest.json`

## 15.6 FastAPI Service Requirements

**All FastAPI services MUST have:**
- `main.py` (entry point)
- `core/` (config, logging, metrics, rate_limit, security, exceptions)
- `api/v1/` (router, endpoints including health)
- `models/` (requests, responses)
- `services/` (business logic)

## 15.7 CI/CD Requirements

**All workflows MUST follow Danny's pattern:**
- `runs-on: [arc-runner-set]`
- IRSA authentication (no secrets)
- Buildx with Kubernetes driver
- Helm for deployment
- Concurrency control
- `workflow_dispatch` + `pull_request: types: [closed]`
- Single build job (not matrix)

## 15.8 Infrastructure Requirements

**Terraform manages:**
- ECR repositories
- `ai-guardians` namespace
- Linkerd installation
- IRSA configuration
- Deployments and services

**Services provide:**
- Container images
- Kubernetes manifests (optional)

**Services NEVER create infrastructure.**

## 15.9 Communication Rules

| Source | Target | Method | Allowed? |
|--------|--------|--------|----------|
| Orbit Repo | Orbit Repo (same orbit) | HTTP API | ✅ |
| Orbit Repo | Orbit Repo (different orbit) | EventBus | ✅ |
| Guardian | Guard | HTTP API | ✅ |
| Guardian | Guard | EventBus | ✅ |
| Service | Service | Direct Import | ❌ |

## 15.10 Governance Boundaries

- **Danny:** Infrastructure, Terraform, CI/CD, Helm, AWS
- **Ben:** FastAPI services, API design, service patterns
- **Jimmy:** Neuromorphic engine, AI/ML models, consciousness
- **Meta:** Architecture, Orbit-Spec, orchestration, documentation

## 15.11 The ONE Architecture Statement

**The AbëONE ecosystem is a unified, multi-orbit, microservices architecture where:**

1. **Products orbit** around the AbëONE Superkernel via Orbit-Spec v1.0
2. **Services communicate** via EventBus (primary) and HTTP APIs (secondary)
3. **Infrastructure is managed** by Terraform, not by services
4. **Deployments are independent** - one repo, one deployment
5. **Naming is uniform** - consistent conventions across ecosystem
6. **Ownership is clear** - Danny/Ben/Jimmy/Meta boundaries
7. **Communication is bounded** - no cross-repo imports, use EventBus/APIs
8. **CI/CD follows patterns** - Danny's workflow pattern for all repos
9. **Shared runtime** - kernel, libraries, and mesh are shared
10. **Architecture is canonical** - this document is THE source of truth

## 15.12 Final Validation Checklist

**Before creating any new repository or service, verify:**

- [ ] Follows naming conventions (kebab-case/product-case)
- [ ] Has correct folder structure (Orbit-Spec or FastAPI template)
- [ ] Includes all required files (adapters, config, manifests)
- [ ] Uses EventBus for cross-service communication
- [ ] Does NOT import from other services
- [ ] Has CI/CD workflow following Danny's pattern
- [ ] Deploys to `ai-guardians` namespace
- [ ] Uses Terraform-managed infrastructure
- [ ] Has Linkerd injection enabled
- [ ] Follows team ownership boundaries
- [ ] Documents architecture and usage
- [ ] Pins kernel version to v0.9.0-stable (if orbit repo)

---

## CONCLUSION

This document is **THE SINGLE SOURCE OF TRUTH** for the AbëONE ecosystem architecture. Every detail is derived from the 32 canonical facts and represents the absolute ground truth of the system.

**All future repos, services, and integrations must follow this specification exactly.**

**Pattern:** OBSERVER × TRUTH × ATOMIC × ONE  
**Status:** ✅ **CANONICAL ARCHITECTURE SPECIFICATION**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-27  
**Next Review:** As needed when canonical facts change

