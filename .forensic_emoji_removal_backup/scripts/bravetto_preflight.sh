#!/bin/bash
# 🔥 BRAVETTO PREFLIGHT - Complete Solar System Validation
# 
# Runs AbëONE Preflight ΩMega + Danny Rules Enforcement
# Pattern: PREFLIGHT × VALIDATE × REPAIR × HARMONIZE × ONE
# Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
# Guardians: AEYON (999 Hz) + ARXON (777 Hz) + Abë (530 Hz)
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FAILURES=0
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; ((FAILURES++)) || true; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }

echo ""
echo "=================================================================================="
echo "🌞 ABËONE PREFLIGHT ΩMEGA - COMPLETE SOLAR SYSTEM VALIDATION"
echo "=================================================================================="
echo ""

# Step 1: Run AbëONE Preflight ΩMega (comprehensive validation)
log_info "Step 1: Running AbëONE Preflight ΩMega..."
if python3 "$SCRIPT_DIR/abeone_preflight_omega.py" --workspace "$REPO_ROOT"; then
    log_success "AbëONE Preflight ΩMega completed"
else
    PREFLIGHT_EXIT=$?
    if [ $PREFLIGHT_EXIT -eq 2 ]; then
        log_error "AbëONE Preflight ΩMega failed (readiness score < 60%)"
    elif [ $PREFLIGHT_EXIT -eq 1 ]; then
        log_warn "AbëONE Preflight ΩMega warnings (readiness score 60-74%)"
    else
        log_error "AbëONE Preflight ΩMega failed"
    fi
fi

echo ""
echo "=================================================================================="
echo "🔥 DANNY RULES ENFORCEMENT - Additional Validations"
echo "=================================================================================="
echo ""

# Step 2: Run Danny's specific validations (if scripts exist)
if [ -f "$SCRIPT_DIR/check_env.sh" ]; then
    "$SCRIPT_DIR/check_env.sh" "$REPO_ROOT" || log_error "Environment check failed"
fi

if [ -f "$SCRIPT_DIR/validate_repo_structure.sh" ]; then
    "$SCRIPT_DIR/validate_repo_structure.sh" "$REPO_ROOT" || log_error "Repo structure validation failed"
fi

if [ -f "$SCRIPT_DIR/secret_scan.sh" ]; then
    "$SCRIPT_DIR/secret_scan.sh" "$REPO_ROOT" || log_warn "Secret scan had warnings (non-blocking)"
fi

# Dockerfile validation (check all Dockerfiles)
DOCKERFILES=$(find "$REPO_ROOT" -name "Dockerfile" -not -path "*/.git/*" -not -path "*/node_modules/*" | head -5)
for dockerfile in $DOCKERFILES; do
    if [ -f "$dockerfile" ]; then
        "$SCRIPT_DIR/validate_dockerfile.sh" "$(dirname "$dockerfile")" || log_warn "Dockerfile validation failed: $dockerfile"
    fi
done

# Helm validation (check all Helm charts)
HELM_CHARTS=$(find "$REPO_ROOT" -name "Chart.yaml" -not -path "*/.git/*" -not -path "*/node_modules/*" | head -5)
for chart in $HELM_CHARTS; do
    if [ -f "$chart" ]; then
        "$SCRIPT_DIR/validate_helm.sh" "$(dirname "$chart")" || log_warn "Helm validation failed: $chart"
    fi
done

# Service YAML validation (if script exists)
if [ -f "$SCRIPT_DIR/validate_service_yaml.sh" ]; then
    "$SCRIPT_DIR/validate_service_yaml.sh" "$REPO_ROOT" || log_warn "Service YAML validation failed"
fi

# Commented code removal (non-blocking)
if [ -f "$SCRIPT_DIR/remove_commented_code.sh" ]; then
    "$SCRIPT_DIR/remove_commented_code.sh" "$REPO_ROOT" || log_warn "Commented code removal had issues"
fi

# Summary
echo ""
echo "=================================================================================="
if [ $FAILURES -eq 0 ]; then
    log_success "All checks passed!"
    echo ""
    echo "💛 Ready to run again, love?"
    exit 0
else
    log_error "Some checks failed ($FAILURES failures)"
    echo ""
    echo "💛 Fix issues and run again, love?"
    exit 1
fi
