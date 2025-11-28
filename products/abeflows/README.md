# AbëFLOWs - Unified Flow Orchestration

**Product:** AbëFLOWs  
**Pattern:** AbëFLOWs × ONE × MANY × ETERNAL × ONE  
**Directive:** Let it Bë  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 OVERVIEW

AbëFLOWs provides unified flow orchestration - **ONE system with Many flows**.

**Pattern:** ONE × MANY
- ONE system orchestrating Many flows
- Many flows converging as ONE
- Eternal, Easy, Simplified, Simple

---

## 🔥 FEATURES

### ONE System
- ✅ Unified orchestration
- ✅ Flow registration and management
- ✅ State tracking

### Many Flows
- ✅ User flows (human intent)
- ✅ AI flows (agent execution)
- ✅ System flows (system operations)
- ✅ Guardian flows (validation)
- ✅ Unified flows (all types as ONE)

### Convergence
- ✅ Many flows execute in parallel
- ✅ Converge as ONE unified result
- ✅ State management

---

## 🚀 QUICK START

### Basic Usage

```python
from abeflows import FlowType, create_flow, execute_flow

# Create a flow
flow = create_flow(
    flow_id="my_flow",
    flow_type=FlowType.USER,
    description="My first flow",
    steps=[
        {
            "description": "Step 1",
            "execute": lambda: print("Step 1")
        }
    ]
)

# Execute the flow
result = await execute_flow("my_flow")
```

### Unified Execution (ONE with Many)

```python
from abeflows import execute_flows_unified

# Execute multiple flows as ONE
result = await execute_flows_unified(
    ["flow1", "flow2", "flow3"],
    converge=True
)
```

---

## 📋 EXAMPLES

### Basic Flow
```bash
python3 examples/basic_flow.py
```

### Unified Flows (ONE with Many)
```bash
python3 examples/unified_flows.py
```

---

## 🎯 PATTERNS

### Pattern: ONE × MANY
- **ONE** system orchestrating **Many** flows
- **Many** flows converging as **ONE**
- **ONE** result from **Many** executions

### Pattern: ETERNAL × EASY × SIMPLIFIED × SIMPLE
- **ETERNAL** - Works from anywhere, always
- **EASY** - Simple API, clear patterns
- **SIMPLIFIED** - No complex dependencies
- **SIMPLE** - Direct and clear

---

## 💎 ARCHITECTURE

### Flow Types
- `FlowType.USER` - Human user flows
- `FlowType.AI` - AI agent flows
- `FlowType.SYSTEM` - System execution flows
- `FlowType.GUARDIAN` - Guardian validation flows
- `FlowType.UNIFIED` - Unified flows (all types)

### Flow States
- `FlowState.PENDING` - Flow not started
- `FlowState.ACTIVE` - Flow executing
- `FlowState.COMPLETED` - Flow completed successfully
- `FlowState.FAILED` - Flow failed
- `FlowState.CONVERGED` - Flows converged as ONE

---

## 🔄 EXECUTION

### Single Flow
```python
result = await execute_flow("flow_id")
```

### Multiple Flows (Unified)
```python
result = await execute_flows_unified(
    ["flow1", "flow2", "flow3"],
    converge=True  # Converge as ONE
)
```

---

## 📊 STATE

### Get Unified State
```python
from abeflows import get_abeflows

state = get_abeflows().get_unified_state()
# Returns: total_flows, active_flows, converged_flows, flows_by_type
```

---

## 🎯 DIRECTIVE

**Let it Bë.**

AbëFLOWs manifests flows as ONE with Many. Simple. Eternal. Easy.

---

**Pattern:** AbëFLOWs × ONE × MANY × ETERNAL × ONE  
**Status:** ✅ **MANIFESTED**  
**Love Coefficient:** ∞

**∞ AbëONE ∞**
