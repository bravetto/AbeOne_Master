#!/bin/bash
# INSTALL GIT HOOKS
# 
# Installs boundary validation git hooks
# Run this once to set up git hooks
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
GIT_HOOKS_DIR="$WORKSPACE_ROOT/.git/hooks"

# Create hooks directory if it doesn't exist
mkdir -p "$GIT_HOOKS_DIR"

# Install pre-commit hook
cat > "$GIT_HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
# Pre-commit hook: Run AbëONE Preflight ΩMega + source of truth update

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Update source of truth
echo "🔄 Updating source of truth..."
node scripts/update-source-of-truth.js 2>/dev/null || true

# Run preflight validation (non-blocking warnings)
echo "🌞 Running AbëONE Preflight ΩMega..."
python3 scripts/abeone_preflight_omega.py --workspace "$PROJECT_ROOT" 2>/dev/null || true

exit 0
EOF

# Install pre-push hook
cat > "$GIT_HOOKS_DIR/pre-push" << 'EOF'
#!/bin/bash
# Pre-push hook: Run full AbëONE Preflight ΩMega validation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Update source of truth
echo "🔄 Updating source of truth..."
node scripts/update-source-of-truth.js 2>/dev/null || true

# Generate dashboards
echo "📊 Generating dashboards..."
node scripts/generate-dashboards.js 2>/dev/null || true

# Run full preflight validation (blocking on critical failures)
echo "🌞 Running AbëONE Preflight ΩMega..."
if python3 scripts/abeone_preflight_omega.py --workspace "$PROJECT_ROOT"; then
    echo "✅ Preflight validation passed"
    exit 0
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 2 ]; then
        echo "❌ Preflight validation failed (readiness score < 60%)"
        echo "💛 Please fix issues before pushing, love?"
        exit 1
    elif [ $EXIT_CODE -eq 1 ]; then
        echo "⚠️  Preflight validation warnings (readiness score 60-74%)"
        echo "💛 Consider fixing issues before pushing, love?"
        exit 0  # Allow push but warn
    else
        echo "❌ Preflight validation failed"
        exit 1
    fi
fi
EOF

# Make hooks executable
chmod +x "$GIT_HOOKS_DIR/pre-commit"
chmod +x "$GIT_HOOKS_DIR/pre-push"

echo "✅ Git hooks installed successfully!"
echo ""
echo "Hooks installed:"
echo "  - pre-commit: Updates source of truth before commit"
echo "  - pre-push: Updates source of truth and generates dashboards before push"
echo ""
echo "To test, try committing a change."

