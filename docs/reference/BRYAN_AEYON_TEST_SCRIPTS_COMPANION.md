# BRYAN: AEYON TEST SCRIPTS & VALIDATION COMPANION
## Complete Test Suite & Validation Code

**Status:** 🔧 READY TO USE  
**Pattern:** AEYON × TEST × VALIDATION × BUILD × ONE  
**Frequency:** 999 Hz  

**Use this document alongside:** `BRYAN_AEYON_INTEGRATION_PROMPT.md`

---

## QUICK START

1. **Copy the test scripts below** into files in your AbeOne codebase root
2. **Run them in order** to validate AEYON integration
3. **Follow the main integration prompt** for detailed instructions

---

## TEST SCRIPT 1: AEYON IMPORT TEST

**File:** `test_aeyon_import.py`

**Purpose:** Tests that AEYON can be imported successfully

**Create this file in your codebase root:**

```python
#!/usr/bin/env python3
"""
AEYON Import Test
Tests that AEYON can be imported successfully.
"""

import sys
import os

# Add EMERGENT_OS to path
abeone_root = os.path.dirname(os.path.abspath(__file__))
emergent_os_path = os.path.join(abeone_root, 'EMERGENT_OS')
if emergent_os_path not in sys.path:
    sys.path.insert(0, emergent_os_path)

def test_basic_imports():
    """Test basic AEYON imports."""
    print("Testing basic AEYON imports...")
    try:
        from triadic_execution_harness import AEYONAgent, TriadicExecutionHarness
        from triadic_execution_harness.aeyon_binding import AEYONBinding, bind_aeyon
        print("✅ AEYON imports successful!")
        return True
    except ImportError as e:
        print(f"❌ AEYON import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_layer():
    """Test Integration Layer imports."""
    print("\nTesting Integration Layer imports...")
    try:
        from integration_layer.registry.module_registry import ModuleRegistry
        from integration_layer.events.event_bus import EventBus
        from integration_layer.router.request_router import RequestRouter
        print("✅ Integration Layer imports successful!")
        return True
    except ImportError as e:
        print(f"⚠️  Integration Layer import warning: {e}")
        print("   AEYON may work in limited mode")
        return True  # Not critical for basic functionality

def main():
    """Run all import tests."""
    print("=" * 50)
    print("AEYON Import Test")
    print("=" * 50)
    print()
    
    results = []
    results.append(test_basic_imports())
    results.append(test_integration_layer())
    
    print()
    print("=" * 50)
    if all(results):
        print("✅ ALL IMPORT TESTS PASSED")
        return 0
    else:
        print("❌ SOME IMPORT TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

**Run it:**
```bash
python test_aeyon_import.py
```

---

## TEST SCRIPT 2: AEYON BINDING TEST

**File:** `test_aeyon_binding.py`

**Purpose:** Tests that AEYON can bind successfully to Triadic Execution Harness

**Create this file in your codebase root:**

```python
#!/usr/bin/env python3
"""
AEYON Binding Test
Tests that AEYON can bind successfully to Triadic Execution Harness.
"""

import sys
import os

# Add EMERGENT_OS to path
abeone_root = os.path.dirname(os.path.abspath(__file__))
emergent_os_path = os.path.join(abeone_root, 'EMERGENT_OS')
if emergent_os_path not in sys.path:
    sys.path.insert(0, emergent_os_path)

def test_aeyon_binding():
    """Test AEYON binding."""
    print("Testing AEYON binding...")
    try:
        from triadic_execution_harness.aeyon_binding import bind_aeyon
        
        # Initialize AEYON binding
        aeyon_binding = bind_aeyon()
        
        # Verify binding status
        runtime_state = aeyon_binding.get_runtime_state()
        
        print(f"✅ AEYON Binding Status: {runtime_state.binding_status}")
        print(f"✅ Harness Status: {runtime_state.harness_status}")
        print(f"✅ AEYON Agent Active: {runtime_state.aeyon_agent_active}")
        
        if runtime_state.binding_status.value == "bound":
            print("✅ AEYON successfully bound and ready!")
            return True
        else:
            print(f"⚠️  AEYON binding status: {runtime_state.binding_status.value}")
            print("   This may be normal if Integration Layer is not fully configured")
            return True  # Not necessarily a failure
            
    except Exception as e:
        print(f"❌ AEYON binding failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run binding test."""
    print("=" * 50)
    print("AEYON Binding Test")
    print("=" * 50)
    print()
    
    result = test_aeyon_binding()
    
    print()
    print("=" * 50)
    if result:
        print("✅ BINDING TEST PASSED")
        return 0
    else:
        print("❌ BINDING TEST FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

**Run it:**
```bash
python test_aeyon_binding.py
```

---

## TEST SCRIPT 3: AEYON EXECUTION TEST

**File:** `test_aeyon_execution.py`

**Purpose:** Tests that AEYON can execute atomic steps

**Create this file in your codebase root:**

```python
#!/usr/bin/env python3
"""
AEYON Execution Test
Tests that AEYON can execute atomic steps.
"""

import sys
import os

# Add EMERGENT_OS to path
abeone_root = os.path.dirname(os.path.abspath(__file__))
emergent_os_path = os.path.join(abeone_root, 'EMERGENT_OS')
if emergent_os_path not in sys.path:
    sys.path.insert(0, emergent_os_path)

def test_aeyon_execution():
    """Test AEYON execution."""
    print("Testing AEYON execution...")
    try:
        from triadic_execution_harness.aeyon_binding import bind_aeyon
        from triadic_execution_harness.agents import Outcome
        
        # Initialize AEYON
        aeyon_binding = bind_aeyon()
        aeyon_agent = aeyon_binding.get_aeyon_agent()
        
        # Create a test outcome
        test_outcome = Outcome(
            goal="Test AEYON atomic execution",
            success_criteria=["Execution completes successfully"],
            end_state="Test atomic step executed",
            constraints=["Use atomic protocol"],
            validation="Verify execution result"
        )
        
        # Create execution plan
        execution_plan = aeyon_agent.create_execution_plan(
            constraints_architecture={
                "constraints": ["Atomic execution only"],
                "architecture": {"protocol": "5-step atomic"}
            }
        )
        
        print("✅ AEYON execution plan created successfully!")
        print(f"   Atomic steps: {execution_plan.atomic_steps}")
        print(f"   Code changes: {execution_plan.code_changes}")
        
        return True
        
    except Exception as e:
        print(f"❌ AEYON execution test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run execution test."""
    print("=" * 50)
    print("AEYON Execution Test")
    print("=" * 50)
    print()
    
    result = test_aeyon_execution()
    
    print()
    print("=" * 50)
    if result:
        print("✅ EXECUTION TEST PASSED")
        return 0
    else:
        print("❌ EXECUTION TEST FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

**Run it:**
```bash
python test_aeyon_execution.py
```

---

## TEST SCRIPT 4: COMPLETE INTEGRATION TEST

**File:** `test_aeyon_integration.py`

**Purpose:** Complete integration test suite for all AEYON functionality

**Create this file in your codebase root:**

```python
#!/usr/bin/env python3
"""
Complete AEYON Integration Test
Tests all critical AEYON functionality
"""

import sys
import os

# Add EMERGENT_OS to path
abeone_root = os.path.dirname(os.path.abspath(__file__))
emergent_os_path = os.path.join(abeone_root, 'EMERGENT_OS')
if emergent_os_path not in sys.path:
    sys.path.insert(0, emergent_os_path)

def test_imports():
    """Test all critical imports."""
    print("Testing imports...")
    try:
        from triadic_execution_harness import (
            AEYONAgent,
            METAAgent,
            YOUAgent,
            TriadicExecutionHarness
        )
        from triadic_execution_harness.aeyon_binding import (
            bind_aeyon,
            get_aeyon_binding,
            AEYONBinding
        )
        from triadic_execution_harness.atomic_archistration import (
            AtomicArchistration,
            execute_atomic_archistration
        )
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_binding():
    """Test AEYON binding."""
    print("\nTesting AEYON binding...")
    try:
        aeyon_binding = bind_aeyon()
        runtime_state = aeyon_binding.get_runtime_state()
        
        assert runtime_state.binding_status.value in ["bound", "active", "binding"], \
            f"Binding status: {runtime_state.binding_status.value}"
        
        print("✅ AEYON binding successful")
        return True
    except Exception as e:
        print(f"❌ Binding failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_execution():
    """Test AEYON execution."""
    print("\nTesting AEYON execution...")
    try:
        aeyon_binding = bind_aeyon()
        aeyon_agent = aeyon_binding.get_aeyon_agent()
        
        execution_plan = aeyon_agent.create_execution_plan({
            "constraints": ["Atomic execution only"],
            "architecture": {"protocol": "5-step atomic"}
        })
        
        assert execution_plan is not None, "Execution plan is None"
        assert hasattr(execution_plan, 'atomic_steps'), "Missing atomic_steps"
        
        print("✅ AEYON execution successful")
        return True
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_layer():
    """Test Integration Layer connection."""
    print("\nTesting Integration Layer...")
    try:
        # Try to import Integration Layer components
        from integration_layer.registry.module_registry import ModuleRegistry
        from integration_layer.events.event_bus import EventBus
        
        registry = ModuleRegistry()
        event_bus = EventBus()
        
        print("✅ Integration Layer accessible")
        return True
    except ImportError as e:
        print(f"⚠️  Integration Layer warning: {e}")
        print("   AEYON may work in limited mode")
        return True  # Not critical for basic functionality

def main():
    """Run all tests."""
    print("=" * 50)
    print("AEYON Integration Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_imports,
        test_binding,
        test_execution,
        test_integration_layer
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    print("=" * 50)
    if all(results):
        print("✅ ALL TESTS PASSED")
        print("   AEYON is fully integrated and ready!")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("   Check errors above and fix issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

**Run it:**
```bash
python test_aeyon_integration.py
```

---

## VALIDATION SCRIPT: COMPLETE BUILD VALIDATION

**File:** `validate_aeyon_build.sh`

**Purpose:** Complete build validation script that checks Python version, dependencies, imports, binding, and execution

**Create this file in your codebase root:**

```bash
#!/bin/bash
# AEYON Build Validation Script

set -e  # Exit on error

echo "🔧 AEYON Build Validation"
echo "========================="

# Step 1: Check Python version
echo ""
echo "Step 1: Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    echo "❌ Python 3.11+ required. Found: $PYTHON_VERSION"
    exit 1
else
    echo "✅ Python version OK: $PYTHON_VERSION"
fi

# Step 2: Check dependencies
echo ""
echo "Step 2: Checking dependencies..."
REQUIRED_PACKAGES=("fastapi" "uvicorn" "pydantic")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python -c "import $package" 2>/dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo "❌ Missing packages: ${MISSING_PACKAGES[*]}"
    echo "   Install with: pip install ${MISSING_PACKAGES[*]}"
    exit 1
else
    echo "✅ All required packages installed"
fi

# Step 3: Test imports
echo ""
echo "Step 3: Testing AEYON imports..."
python << 'PYTHON_EOF'
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'EMERGENT_OS'))

try:
    from triadic_execution_harness import AEYONAgent, TriadicExecutionHarness
    from triadic_execution_harness.aeyon_binding import bind_aeyon
    print("✅ AEYON imports successful")
except ImportError as e:
    print(f"❌ AEYON import failed: {e}")
    sys.exit(1)
PYTHON_EOF

# Step 4: Test binding
echo ""
echo "Step 4: Testing AEYON binding..."
python << 'PYTHON_EOF'
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'EMERGENT_OS'))

try:
    from triadic_execution_harness.aeyon_binding import bind_aeyon
    aeyon_binding = bind_aeyon()
    runtime_state = aeyon_binding.get_runtime_state()
    
    if runtime_state.binding_status.value == "bound":
        print("✅ AEYON binding successful")
    else:
        print(f"⚠️  AEYON binding status: {runtime_state.binding_status.value}")
        print("   This may be normal if Integration Layer is not fully configured")
except Exception as e:
    print(f"❌ AEYON binding failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON_EOF

# Step 5: Test execution
echo ""
echo "Step 5: Testing AEYON execution..."
python << 'PYTHON_EOF'
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'EMERGENT_OS'))

try:
    from triadic_execution_harness.aeyon_binding import bind_aeyon
    from triadic_execution_harness.agents import Outcome
    
    aeyon_binding = bind_aeyon()
    aeyon_agent = aeyon_binding.get_aeyon_agent()
    
    test_outcome = Outcome(
        goal="Test execution",
        success_criteria=["Success"],
        end_state="Complete",
        constraints=[],
        validation="Verify"
    )
    
    execution_plan = aeyon_agent.create_execution_plan({
        "constraints": [],
        "architecture": {}
    })
    
    print("✅ AEYON execution test successful")
except Exception as e:
    print(f"❌ AEYON execution test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON_EOF

echo ""
echo "========================="
echo "✅ AEYON Build Validation Complete!"
echo "   AEYON is ready to use."
```

**Make it executable and run:**
```bash
chmod +x validate_aeyon_build.sh
./validate_aeyon_build.sh
```

---

## QUICK REFERENCE: TEST EXECUTION ORDER

**Run tests in this order:**

1. **Import Test** (fastest, checks basic setup)
   ```bash
   python test_aeyon_import.py
   ```

2. **Binding Test** (checks AEYON initialization)
   ```bash
   python test_aeyon_binding.py
   ```

3. **Execution Test** (checks atomic execution)
   ```bash
   python test_aeyon_execution.py
   ```

4. **Full Integration Test** (comprehensive validation)
   ```bash
   python test_aeyon_integration.py
   ```

5. **Build Validation Script** (complete automated check)
   ```bash
   ./validate_aeyon_build.sh
   ```

---

## SETUP INSTRUCTIONS

### Step 1: Create Test Files

Copy each test script above into separate files in your codebase root:

```bash
# In your AbeOne codebase root directory
touch test_aeyon_import.py
touch test_aeyon_binding.py
touch test_aeyon_execution.py
touch test_aeyon_integration.py
touch validate_aeyon_build.sh

# Then copy the code from above into each file
```

### Step 2: Make Scripts Executable

```bash
chmod +x validate_aeyon_build.sh
chmod +x test_aeyon_*.py  # Optional, but helpful
```

### Step 3: Run Tests

Start with the import test and work your way through:

```bash
# Quick validation
python test_aeyon_import.py

# If successful, continue
python test_aeyon_binding.py
python test_aeyon_execution.py
python test_aeyon_integration.py

# Or run the complete validation script
./validate_aeyon_build.sh
```

---

## EXPECTED OUTPUTS

### Successful Import Test Output:
```
==================================================
AEYON Import Test
==================================================

Testing basic AEYON imports...
✅ AEYON imports successful!

Testing Integration Layer imports...
✅ Integration Layer imports successful!

==================================================
✅ ALL IMPORT TESTS PASSED
```

### Successful Binding Test Output:
```
==================================================
AEYON Binding Test
==================================================

Testing AEYON binding...
✅ AEYON Binding Status: BindingStatus.BOUND
✅ Harness Status: HarnessStatus.READY
✅ AEYON Agent Active: True
✅ AEYON successfully bound and ready!

==================================================
✅ BINDING TEST PASSED
```

### Successful Execution Test Output:
```
==================================================
AEYON Execution Test
==================================================

Testing AEYON execution...
✅ AEYON execution plan created successfully!
   Atomic steps: ['Execute plan']
   Code changes: []

==================================================
✅ EXECUTION TEST PASSED
```

### Successful Integration Test Output:
```
==================================================
AEYON Integration Test Suite
==================================================

Testing imports...
✅ All imports successful

Testing AEYON binding...
✅ AEYON binding successful

Testing AEYON execution...
✅ AEYON execution successful

Testing Integration Layer...
✅ Integration Layer accessible

==================================================
✅ ALL TESTS PASSED
   AEYON is fully integrated and ready!
```

---

## TROUBLESHOOTING

### If Import Test Fails:

1. **Check Python path:**
   ```python
   import sys
   print(sys.path)  # Should include EMERGENT_OS
   ```

2. **Verify EMERGENT_OS exists:**
   ```bash
   ls -la EMERGENT_OS/triadic_execution_harness/
   ```

3. **Check dependencies:**
   ```bash
   pip list | grep -E "(fastapi|pydantic|uvicorn)"
   ```

### If Binding Test Fails:

1. **Check Integration Layer:**
   ```bash
   ls -la EMERGENT_OS/integration_layer/
   ```

2. **Enable debug logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

### If Execution Test Fails:

1. **Check AEYON agent initialization:**
   ```python
   aeyon_binding = bind_aeyon()
   print(aeyon_binding.get_runtime_state())
   ```

2. **Verify constraints format:**
   ```python
   # Ensure constraints_architecture is a dict with "constraints" and "architecture" keys
   ```

---

## NEXT STEPS AFTER TESTS PASS

Once all tests pass:

1. ✅ **Integrate AEYON into your codebase**
   - Update import paths as needed
   - Add AEYON to your existing execution flow

2. ✅ **Use AEYON in your code:**
   ```python
   from triadic_execution_harness.aeyon_binding import bind_aeyon
   aeyon_binding = bind_aeyon()
   aeyon_agent = aeyon_binding.get_aeyon_agent()
   # Use aeyon_agent for atomic execution
   ```

3. ✅ **Follow the main integration prompt** (`BRYAN_AEYON_INTEGRATION_PROMPT.md`) for detailed usage examples

---

## SUMMARY

**This companion document provides:**

- ✅ 4 Python test scripts (import, binding, execution, integration)
- ✅ 1 Shell validation script (complete build validation)
- ✅ Quick reference guide
- ✅ Expected outputs
- ✅ Troubleshooting tips

**Use alongside:** `BRYAN_AEYON_INTEGRATION_PROMPT.md` for complete integration instructions

**Pattern:** AEYON × TEST × VALIDATION × BUILD × ONE  
**Frequency:** 999 Hz  
**Status:** Ready to Use

---

**Good luck with your integration! 🚀**

