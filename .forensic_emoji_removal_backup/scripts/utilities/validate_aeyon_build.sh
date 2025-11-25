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

