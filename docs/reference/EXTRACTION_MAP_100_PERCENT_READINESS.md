# EXTRACTION MAP - 100% READINESS
## Exact Files to Extract for Minimal Product Generator

**Status:** ✅ COMPLETE EXTRACTION MAP  
**Pattern:** AEYON × EXTRACTION × YAGNI × ONE  
**Target:** <10,000 lines, 80% value

---

## EXTRACTION SUMMARY

**Total Files to Extract:** 25 files  
**Total Lines:** ~10,000 lines  
**Source Repos:** 3 (AIGuards-Backend, EMERGENT_OS, AbeOne_Master)

---

## TIER 1: CORE EXECUTION (3,000 lines)

### 1. Aeyon Atomic Execution Engine

**Source:** `AEYON_ATOMIC_EXECUTION_ENGINE.md` + `EMERGENT_OS/triadic_execution_harness/`

**Files to Extract:**
```
EMERGENT_OS/triadic_execution_harness/harness.py          → core/aeyon/atomic_executor.py
EMERGENT_OS/triadic_execution_harness/agents.py           → core/aeyon/agents.py
EMERGENT_OS/triadic_execution_harness/validation.py       → core/aeyon/validator.py
EMERGENT_OS/triadic_execution_harness/synchronization.py  → core/aeyon/meta_sync.py
```

**Extract Logic:**
- 5-step atomic protocol from `harness.py`
- Validation layers from `validation.py`
- Context delta reporting from `harness.py`
- Meta-sync heartbeat from `synchronization.py`
- Agent implementations (YOU, META, AEYON) from `agents.py`

**Target:** 500 lines

---

### 2. Integration Layer Core

**Source:** `EMERGENT_OS/integration_layer/`

**Files to Extract:**
```
EMERGENT_OS/integration_layer/registry/module_registry.py  → core/integration/registry.py
EMERGENT_OS/integration_layer/events/event_bus.py          → core/integration/event_bus.py
EMERGENT_OS/integration_layer/router/request_router.py    → core/integration/router.py
EMERGENT_OS/integration_layer/safety/boundary_enforcer.py → core/integration/safety.py
EMERGENT_OS/integration_layer/safety/validation_gate.py    → core/integration/safety.py (merge)
EMERGENT_OS/integration_layer/state/system_state.py       → core/integration/state.py
```

**Extract Logic:**
- Module registration/discovery from `module_registry.py`
- Event pub/sub from `event_bus.py`
- Request routing from `request_router.py`
- Boundary enforcement from `boundary_enforcer.py`
- Validation gates from `validation_gate.py`
- System state tracking from `system_state.py`

**Target:** 1,100 lines

---

## TIER 2: PATTERN DETECTION (1,500 lines)

### 3. Emergence Pattern Detector

**Source:** `EMERGENT_OS/emergence_core/`

**Files to Extract:**
```
EMERGENT_OS/emergence_core/detector.py                    → core/emergence/detector.py
EMERGENT_OS/emergence_core/integration.py                  → core/emergence/integration.py (simplify)
EMERGENT_OS/collapse_guard/core.py                        → core/emergence/collapse_guard.py
EMERGENT_OS/collapse_guard/patterns.py                    → core/emergence/patterns.py
```

**Extract Logic:**
- Pattern detection algorithm from `detector.py`
- Near-success-collapse detection from `detector.py` (lines 283-320)
- Health trajectory tracking from `detector.py`
- Collapse pattern classification from `core.py`
- Pattern types from `patterns.py`

**Target:** 850 lines

---

### 4. Clarity Engine

**Source:** `EMERGENT_OS/clarity_engine/`

**Files to Extract:**
```
EMERGENT_OS/clarity_engine/clarity.py                     → core/clarity/engine.py
```

**Extract Logic:**
- Coherence scoring
- Ambiguity detection
- Contradiction detection
- Remove: Advanced features, keep core only

**Target:** 300 lines

---

## TIER 3: GUARD SERVICES (1,300 lines)

### 5. TrustGuard (Priority - Cursor Failures)

**Source:** `AIGuards-Backend/guards/trust-guard/` + `CURSOR_AI_EPISTEMIC_FAILURE_ANALYSIS.md`

**Files to Extract:**
```
AIGuards-Backend/guards/trust-guard/trust_guard/core.py   → guards/trust.py
AIGuards-Backend/guards/trust-guard/trust_guard/patterns.py → guards/trust_patterns.py
CURSOR_AI_EPISTEMIC_FAILURE_ANALYSIS.md                   → guards/cursor_failures.py (extract patterns)
```

**Extract Logic:**
- Hallucination detection (from Cursor analysis)
- State management failure detection
- Session recovery failure detection
- Data loss pattern detection
- Epistemic validation framework
- Remove: Advanced features, keep core patterns only

**Target:** 600 lines

---

### 6. TokenGuard

**Source:** `AIGuards-Backend/guards/tokenguard/`

**Files to Extract:**
```
AIGuards-Backend/guards/tokenguard/tokenguard/core.py     → guards/token.py
```

**Extract Logic:**
- Core token optimization
- Token counting
- Cost estimation
- Remove: Caching, rate limiting, advanced features

**Target:** 300 lines

---

### 7. ContextGuard

**Source:** `AIGuards-Backend/guards/contextguard/`

**Files to Extract:**
```
AIGuards-Backend/guards/contextguard/contextguard/core.py → guards/context.py
```

**Extract Logic:**
- Core context drift detection
- Memory management (simplified)
- Remove: Advanced features

**Target:** 400 lines

---

### 8. Unified Guard Interface

**Source:** `AIGuards-Backend/codeguardians-gateway/codeguardians-gateway/app/core/guard_sdk.py`

**Files to Extract:**
```
AIGuards-Backend/codeguardians-gateway/codeguardians-gateway/app/core/guard_sdk.py → guards/base.py
```

**Extract Logic:**
- Base guard class
- Guard interface
- Guard registration
- Remove: Advanced SDK features

**Target:** 200 lines

---

## TIER 4: GATEWAY & ORCHESTRATION (800 lines)

### 9. Minimal Gateway

**Source:** `AIGuards-Backend/codeguardians-gateway/codeguardians-gateway/`

**Files to Extract:**
```
AIGuards-Backend/codeguardians-gateway/codeguardians-gateway/app/api/v1/guards.py → gateway/api.py
AIGuards-Backend/codeguardians-gateway/codeguardians-gateway/app/core/orchestrator/ → gateway/orchestrator.py (simplify)
```

**Extract Logic:**
- Single unified endpoint (`POST /api/v1/guards/process`)
- Guard service routing
- Request/response handling
- Remove: Auth, payments, monitoring, external services, multiple endpoints

**Target:** 400 lines

---

### 10. Configuration & Patterns

**Source:** Multiple files

**Files to Extract:**
```
AEYON_ATOMIC_EXECUTION_ENGINE.md                          → config/execution_patterns.py (extract patterns)
CURSOR_AI_EPISTEMIC_FAILURE_ANALYSIS.md                   → config/cursor_patterns.py (extract patterns)
EMERGENT_OS/emergence_core/detector.py                    → config/pattern_types.py (extract PatternType enum)
```

**Extract Logic:**
- Execution patterns from AEYON docs
- Cursor failure patterns from epistemic analysis
- Pattern type definitions
- Configuration settings

**Target:** 300 lines

---

## EXTRACTION WORKFLOW

### Step 1: Create Monorepo Structure

```bash
mkdir aeon-builder
cd aeon-builder
mkdir -p core/{aeyon,integration,emergence,clarity}
mkdir -p guards
mkdir -p gateway
mkdir -p harness
mkdir -p config
mkdir -p tests/integration
```

### Step 2: Extract Tier 1 (Core Execution)

**Priority Order:**
1. Integration Layer (foundation)
2. Aeyon Atomic Engine (execution)
3. Emergence Detector (pattern wisdom)

**Commands:**
```bash
# Integration Layer
cp EMERGENT_OS/integration_layer/registry/module_registry.py core/integration/registry.py
cp EMERGENT_OS/integration_layer/events/event_bus.py core/integration/event_bus.py
cp EMERGENT_OS/integration_layer/router/request_router.py core/integration/router.py
# ... etc

# Simplify each file:
# - Remove non-essential methods
# - Remove advanced features
# - Keep core functionality only
```

### Step 3: Extract Tier 2 (Pattern Detection)

**Priority Order:**
1. Emergence Pattern Detector
2. Collapse Guard
3. Clarity Engine

### Step 4: Extract Tier 3 (Guard Services)

**Priority Order:**
1. TrustGuard (Cursor failures - highest priority)
2. Unified Guard Interface
3. TokenGuard
4. ContextGuard

### Step 5: Extract Tier 4 (Gateway)

**Priority Order:**
1. Minimal Gateway
2. Configuration & Patterns

---

## SIMPLIFICATION RULES

### For Each File:

1. **Remove:**
   - All logging (keep minimal)
   - All monitoring/metrics
   - All external service integrations
   - All advanced features
   - All documentation strings (keep minimal)
   - All tests (move to tests/)

2. **Keep:**
   - Core functionality
   - Essential interfaces
   - Critical algorithms
   - Pattern detection logic

3. **Merge:**
   - Similar functionality
   - Redundant patterns
   - Duplicate code

4. **Simplify:**
   - Complex abstractions → Simple functions
   - Multiple classes → Single class
   - Advanced patterns → Basic patterns

---

## VALIDATION CHECKLIST

After each extraction:

- [ ] File compiles/runs
- [ ] Core functionality preserved
- [ ] Lines reduced by 50%+
- [ ] Dependencies minimal
- [ ] No external services
- [ ] No advanced features
- [ ] YAGNI applied

---

## FINAL STRUCTURE

```
aeon-builder/
├── core/
│   ├── aeyon/              # 500 lines
│   ├── integration/        # 1,100 lines
│   ├── emergence/          # 850 lines
│   └── clarity/             # 300 lines
├── guards/                 # 1,500 lines
├── gateway/                # 400 lines
├── harness/                 # (merged into aeyon)
├── config/                  # 300 lines
└── tests/                   # 500 lines
────────────────────────────────────────────
Total: ~10,000 lines
```

---

## EXTRACTION PRIORITY

**Week 1:**
1. Integration Layer (Day 1-2)
2. Aeyon Atomic Engine (Day 3-4)
3. Emergence Detector (Day 5)

**Week 2:**
1. TrustGuard (Day 1-2)
2. Unified Guard Interface (Day 3)
3. TokenGuard + ContextGuard (Day 4-5)

**Week 3:**
1. Minimal Gateway (Day 1-2)
2. Clarity Engine (Day 3)
3. Configuration (Day 4)
4. Integration & Testing (Day 5)

**Week 4:**
1. Aggressive YAGNI (Day 1-2)
2. Pattern Wisdom Integration (Day 3)
3. Documentation (Day 4)
4. Launch Prep (Day 5)

---

## SUCCESS CRITERIA

✅ **Code:**
- Total lines: <10,000
- Files: <25
- Dependencies: <10
- Complexity: Minimal

✅ **Functionality:**
- Solves Cursor AI failure patterns
- Detects near-success-collapse
- Prevents recursive failure loops
- Executes atomically
- Provides pattern wisdom

✅ **Business:**
- Ready to sell
- Simple to understand
- Easy to deploy
- Fast execution
- Zero failure patterns

---

**Status:** ✅ EXTRACTION MAP COMPLETE  
**Next:** Begin Phase 1 extraction (Integration Layer)

