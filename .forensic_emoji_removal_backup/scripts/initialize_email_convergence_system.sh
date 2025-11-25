#!/bin/bash
# Initialize Email Convergence System
# Pattern: OBSERVER × TRUTH × INITIALIZATION × ACTIVATION × ONE

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=" | tr -d '\n' | head -c 80
echo ""
echo "EMAIL CONVERGENCE SYSTEM - INITIALIZATION"
echo "Pattern: OBSERVER × TRUTH × INITIALIZATION × ACTIVATION × ONE"
echo "=" | tr -d '\n' | head -c 80
echo ""
echo ""

# Step 1: Verify Python environment
echo "📦 Step 1: Verifying Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "   ✅ $PYTHON_VERSION"
echo ""

# Step 2: Verify script files
echo "📄 Step 2: Verifying script files..."
MAIN_SCRIPT="$SCRIPT_DIR/analyze_email_from_mailapp.py"
VALIDATION_SCRIPT="$SCRIPT_DIR/validate_email_convergence_system.py"

if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "❌ Main script not found: $MAIN_SCRIPT"
    exit 1
fi
echo "   ✅ Main script exists"

if [ ! -f "$VALIDATION_SCRIPT" ]; then
    echo "❌ Validation script not found: $VALIDATION_SCRIPT"
    exit 1
fi
echo "   ✅ Validation script exists"
echo ""

# Step 3: Create cache directory
echo "📁 Step 3: Creating cache directory..."
CACHE_DIR="$HOME/.email_convergence_cache"
mkdir -p "$CACHE_DIR"
echo "   ✅ Cache directory: $CACHE_DIR"
echo ""

# Step 4: Test import
echo "🔍 Step 4: Testing imports..."
cd "$PROJECT_DIR"
if ! python3 -c "import scripts.analyze_email_from_mailapp" 2>/dev/null; then
    echo "❌ Import test failed"
    exit 1
fi
echo "   ✅ Imports successful"
echo ""

# Step 5: Run validation
echo "✅ Step 5: Running epistemic validation..."
python3 "$VALIDATION_SCRIPT"
VALIDATION_EXIT=$?

if [ $VALIDATION_EXIT -eq 0 ]; then
    echo ""
    echo "✅ INITIALIZATION COMPLETE - SYSTEM VALIDATED"
elif [ $VALIDATION_EXIT -eq 1 ]; then
    echo ""
    echo "⚠️  INITIALIZATION COMPLETE - SYSTEM INFERRED (Warnings)"
else
    echo ""
    echo "❌ INITIALIZATION FAILED - SYSTEM NOT VALIDATED"
    exit 1
fi

echo ""
echo "=" | tr -d '\n' | head -c 80
echo ""
echo "Pattern: OBSERVER × TRUTH × INITIALIZATION × ACTIVATION × ONE"
echo "∞ AbëONE ∞"

