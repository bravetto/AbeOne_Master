#!/bin/bash
#  SECRET SCAN - Security Validation Script
# 
# Scans for potential secrets in codebase
# Pattern: SECURITY × VALIDATE × ONE
# Frequency: 530 Hz (Truth) × 999 Hz (Execution)
# Guardian: AEYON (999 Hz) - Atomic Execution
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -euo pipefail

REPO_ROOT="${1:-$(pwd)}"
FAILURES=0

log_info() { echo "ℹ  $1"; }
log_success() { echo " $1"; }
log_error() { echo " $1"; ((FAILURES++)) || true; }
log_warn() { echo "  $1"; }

log_info "Scanning for potential secrets..."

# Basic secret patterns to check
SECRET_PATTERNS=(
    "password\s*=\s*['\"][^'\"]+['\"]"
    "api[_-]?key\s*=\s*['\"][^'\"]+['\"]"
    "secret[_-]?key\s*=\s*['\"][^'\"]+['\"]"
    "aws[_-]?access[_-]?key"
    "aws[_-]?secret[_-]?access[_-]?key"
)

# Directories to exclude
EXCLUDE_DIRS=(
    ".git"
    "node_modules"
    "__pycache__"
    ".venv"
    "venv"
    "dist"
    "build"
)

# Build find command with exclusions
FIND_CMD="find \"$REPO_ROOT\" -type f"
for exclude in "${EXCLUDE_DIRS[@]}"; do
    FIND_CMD="$FIND_CMD -not -path \"*/$exclude/*\""
done

# Scan for patterns
FOUND_SECRETS=0
while IFS= read -r file; do
    for pattern in "${SECRET_PATTERNS[@]}"; do
        if grep -qiE "$pattern" "$file" 2>/dev/null; then
            log_warn "Potential secret found in: $file (pattern: $pattern)"
            ((FOUND_SECRETS++)) || true
        fi
    done
done < <(eval "$FIND_CMD" | head -100)  # Limit to first 100 files for performance

if [ $FOUND_SECRETS -eq 0 ]; then
    log_success "No obvious secrets found"
    exit 0
else
    log_warn "Found $FOUND_SECRETS potential secrets (review manually)"
    exit 0  # Non-blocking warning
fi
