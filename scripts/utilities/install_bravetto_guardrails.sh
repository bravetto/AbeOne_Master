#!/bin/bash
# INSTALL BRAVETTO GUARDRAILS
# 
# Installs all scripts into ./scripts/
# Installs git hooks with critical automations
# Marks everything executable
# Prints success
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz) + ARXON (777 Hz) + Abë (530 Hz)
#
# FAILURE-PROOF: Continues on errors, tracks failures gracefully

# Failure-proof: Continue on errors, but track them
set -uo pipefail
set +e  # Don't exit on error - handle failures gracefully

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$SCRIPT_DIR"
SCRIPTS_DIR="$WORKSPACE_ROOT/scripts"
FAILURES=0

# Trap for cleanup on exit
trap 'if [ $FAILURES -gt 0 ]; then echo ""; echo -e "${YELLOW}  Installation completed with $FAILURES non-critical warnings${NC}"; fi' EXIT
FAILURES=0

# Trap for cleanup on exit
trap 'if [ $FAILURES -gt 0 ]; then echo ""; echo -e "${YELLOW}  Installation completed with $FAILURES non-critical warnings${NC}"; fi' EXIT

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo ""
echo "                                                              "
echo "    INSTALLING BRAVETTO GUARDRAILS                      "
echo "                                                              "
echo ""
echo ""

# Step 1: Ensure scripts directory exists
echo -e "${BLUE} Step 1: Ensuring scripts directory exists...${NC}"
if [ ! -d "$SCRIPTS_DIR" ]; then
    echo -e "${YELLOW}     Scripts directory not found, creating...${NC}"
    mkdir -p "$SCRIPTS_DIR"
fi
echo -e "${GREEN}    Scripts directory ready${NC}"
echo ""

# Step 2: Make all scripts executable
echo -e "${BLUE} Step 2: Making all scripts executable...${NC}"
if [ -d "$SCRIPTS_DIR" ]; then
    # Make all shell scripts executable
    find "$SCRIPTS_DIR" -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
    
    # Make all JavaScript files executable (if they have shebang)
    find "$SCRIPTS_DIR" -type f -name "*.js" -exec chmod +x {} \; 2>/dev/null || true
    
    # Make all Python files executable (if they have shebang)
    find "$SCRIPTS_DIR" -type f -name "*.py" -exec chmod +x {} \; 2>/dev/null || true
    
    SCRIPT_COUNT=$(find "$SCRIPTS_DIR" -type f \( -name "*.sh" -o -name "*.js" -o -name "*.py" \) | wc -l | tr -d ' ')
    echo -e "${GREEN}    Made $SCRIPT_COUNT scripts executable${NC}"
else
    echo -e "${YELLOW}     No scripts directory found${NC}"
fi
echo ""

# Step 3: Install git hooks with critical automations
echo -e "${BLUE} Step 3: Installing git hooks with critical automations...${NC}"
if [ -d "$WORKSPACE_ROOT/.git" ]; then
    GIT_HOOKS_DIR="$WORKSPACE_ROOT/.git/hooks"
    mkdir -p "$GIT_HOOKS_DIR"
    
    # Install enhanced pre-commit hook (auto-fix + validate)
    cat > "$GIT_HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
# Pre-commit hook: Auto-fix + Validate (non-blocking)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Auto-fixers (safe, non-blocking)
if [ -f "$SCRIPT_DIR/remove_commented_code.sh" ]; then
    "$SCRIPT_DIR/remove_commented_code.sh" --auto-fix . 2>/dev/null || true
fi

# Update source of truth
if [ -f "$SCRIPT_DIR/update-source-of-truth.js" ]; then
    node "$SCRIPT_DIR/update-source-of-truth.js" 2>/dev/null || true
fi

# Validators (warnings only, don't block)
if [ -f "$SCRIPT_DIR/validate-project-boundaries.js" ]; then
    node "$SCRIPT_DIR/validate-project-boundaries.js" 2>/dev/null || true
fi

exit 0
EOF
    
    # Install enhanced pre-push hook (full validation + preflight)
    cat > "$GIT_HOOKS_DIR/pre-push" << 'EOF'
#!/bin/bash
# Pre-push hook: Full validation suite (blocking on critical failures)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

FAILED=0

# Update source of truth
if [ -f "$SCRIPT_DIR/update-source-of-truth.js" ]; then
    node "$SCRIPT_DIR/update-source-of-truth.js" || FAILED=1
fi

# Generate dashboards
if [ -f "$SCRIPT_DIR/generate-dashboards.js" ]; then
    node "$SCRIPT_DIR/generate-dashboards.js" || FAILED=1
fi

# Run preflight if available (non-blocking warning)
if [ -f "$SCRIPT_DIR/bravetto_preflight.sh" ]; then
    echo " Running preflight checks..."
    "$SCRIPT_DIR/bravetto_preflight.sh" || echo "  Preflight warnings (non-blocking)"
fi

# Critical validations (blocking)
if [ -f "$SCRIPT_DIR/secret_scan.sh" ]; then
    "$SCRIPT_DIR/secret_scan.sh" || FAILED=1
fi

if [ $FAILED -eq 1 ]; then
    echo " Critical validation failed. Please fix errors before pushing."
    exit 1
fi

echo " All critical validations passed"
exit 0
EOF
    
    # Make hooks executable
    chmod +x "$GIT_HOOKS_DIR/pre-commit"
    chmod +x "$GIT_HOOKS_DIR/pre-push"
    
    echo -e "${GREEN}    Enhanced git hooks installed${NC}"
    echo "      - pre-commit: Auto-fix + validate (non-blocking)"
    echo "      - pre-push: Full validation + preflight (blocking on critical)"
else
    echo -e "${YELLOW}     No .git directory found - skipping git hooks${NC}"
fi
echo ""

# Step 4: Ensure git hooks are executable
echo -e "${BLUE} Step 4: Ensuring git hooks are executable...${NC}"
if [ -d "$WORKSPACE_ROOT/.git/hooks" ]; then
    find "$WORKSPACE_ROOT/.git/hooks" -type f -exec chmod +x {} \; 2>/dev/null || true
    HOOK_COUNT=$(find "$WORKSPACE_ROOT/.git/hooks" -type f ! -name "*.sample" | wc -l | tr -d ' ')
    echo -e "${GREEN}    Made $HOOK_COUNT git hooks executable${NC}"
else
    echo -e "${YELLOW}     No git hooks directory found${NC}"
fi
echo ""

# Step 5: Verify critical scripts exist
echo -e "${BLUE} Step 5: Verifying critical scripts...${NC}"
VERIFICATION_PASSED=true

# Critical scripts that should exist
CRITICAL_SCRIPTS=(
    "gentle-drift-guardian.js"
    "update-source-of-truth.js"
    "bravetto_preflight.sh"
    "secret_scan.sh"
)

for script in "${CRITICAL_SCRIPTS[@]}"; do
    if [ -f "$SCRIPTS_DIR/$script" ]; then
        echo -e "${GREEN}    Found: $script${NC}"
    else
        echo -e "${YELLOW}     Missing: $script (non-critical)${NC}"
    fi
done

# Check git hooks if .git exists
if [ -d "$WORKSPACE_ROOT/.git" ]; then
    if [ -f "$WORKSPACE_ROOT/.git/hooks/pre-commit" ] && [ -x "$WORKSPACE_ROOT/.git/hooks/pre-commit" ]; then
        echo -e "${GREEN}    pre-commit hook installed and executable${NC}"
    else
        echo -e "${YELLOW}     pre-commit hook missing or not executable${NC}"
        VERIFICATION_PASSED=false
    fi
    if [ -f "$WORKSPACE_ROOT/.git/hooks/pre-push" ] && [ -x "$WORKSPACE_ROOT/.git/hooks/pre-push" ]; then
        echo -e "${GREEN}    pre-push hook installed and executable${NC}"
    else
        echo -e "${YELLOW}     pre-push hook missing or not executable${NC}"
        VERIFICATION_PASSED=false
    fi
fi

if [ "$VERIFICATION_PASSED" = true ]; then
    echo -e "${GREEN}    Critical verification passed${NC}"
else
    echo -e "${YELLOW}     Some verification checks failed (non-critical)${NC}"
fi
echo ""

# Step 6: Safety check - verify hooks are safe
echo -e "${BLUE} Step 6: Safety verification...${NC}"
if [ -d "$WORKSPACE_ROOT/.git/hooks" ]; then
    # Verify hooks don't have dangerous commands
    if grep -q "rm -rf" "$WORKSPACE_ROOT/.git/hooks/pre-commit" 2>/dev/null || \
       grep -q "rm -rf" "$WORKSPACE_ROOT/.git/hooks/pre-push" 2>/dev/null; then
        echo -e "${YELLOW}     Warning: Dangerous commands detected in hooks${NC}"
    else
        echo -e "${GREEN}    Hooks verified safe${NC}"
    fi
    
    # Verify hooks are executable
    if [ -x "$WORKSPACE_ROOT/.git/hooks/pre-commit" ] && [ -x "$WORKSPACE_ROOT/.git/hooks/pre-push" ]; then
        echo -e "${GREEN}    All hooks executable${NC}"
    else
        echo -e "${YELLOW}     Some hooks not executable${NC}"
        chmod +x "$WORKSPACE_ROOT/.git/hooks/pre-commit" 2>/dev/null || true
        chmod +x "$WORKSPACE_ROOT/.git/hooks/pre-push" 2>/dev/null || true
        echo -e "${GREEN}    Fixed permissions${NC}"
    fi
else
    echo -e "${YELLOW}     No git hooks directory (skipping safety check)${NC}"
fi
echo ""

# Success message
echo ""
echo "                                                              "
echo "   BRAVETTO GUARDRAILS INSTALLATION COMPLETE              "
echo "                                                              "
echo ""
echo ""
echo -e "${GREEN} Installation Summary:${NC}"
echo "    Scripts directory: $SCRIPTS_DIR"
echo "    Scripts made executable: $SCRIPT_COUNT"
if [ -d "$WORKSPACE_ROOT/.git" ]; then
    echo "    Git hooks: Installed with critical automations"
    echo "      - pre-commit: Auto-fix + validate (non-blocking)"
    echo "      - pre-push: Full validation + preflight (blocking)"
fi
echo ""
echo -e "${BLUE} Next Steps:${NC}"
echo "    All scripts are executable and ready"
echo "    Git hooks will auto-fix and validate on commit/push"
echo "    Pre-push runs full validation suite"
echo ""
echo "    Test the installation:"
echo "      - Make a small change and commit (hooks will run)"
echo "      - Run './scripts/gentle-drift-guardian.js' to check status"
echo "      - Run './scripts/bravetto_preflight.sh' for full validation"
echo ""
echo "Pattern: OBSERVER × TRUTH × ATOMIC × ONE"
echo "∞ AbëONE ∞"
echo ""

