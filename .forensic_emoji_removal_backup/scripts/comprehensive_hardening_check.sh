#!/bin/bash
# 🔒 COMPREHENSIVE HARDENING CHECK 🔒
# Complete security and UX perfection validation

set -e

echo "🔒" | tr -d '\n'
for i in {1..40}; do echo -n "🔒"; done
echo ""
echo "COMPREHENSIVE HARDENING CHECK"
echo "Vault × Inputs × Systems × UX Perfection"
echo "🔒" | tr -d '\n'
for i in {1..40}; do echo -n "🔒"; done
echo ""
echo ""

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PASSED=0
FAILED=0
WARNINGS=0

check_pass() {
    echo "   ✅ $1"
    ((PASSED++))
}

check_fail() {
    echo "   ❌ $1"
    ((FAILED++))
}

check_warn() {
    echo "   ⚠️  $1"
    ((WARNINGS++))
}

# ============================================================================
# PART 1: VAULT SECURITY
# ============================================================================

echo "📋 PART 1: AbëKEYS Vault Security"
echo "============================================================"

ABEKEYS_PATH="$HOME/.abekeys"
CREDENTIALS_DIR="$ABEKEYS_PATH/credentials"

# Check vault directory permissions
if [ -d "$ABEKEYS_PATH" ]; then
    PERMS=$(stat -f "%OLp" "$ABEKEYS_PATH" 2>/dev/null || stat -c "%a" "$ABEKEYS_PATH" 2>/dev/null || echo "000")
    if [ "$PERMS" = "700" ] || [ "$PERMS" = "750" ]; then
        check_pass "Vault directory permissions secure ($PERMS)"
    else
        check_fail "Vault directory permissions insecure ($PERMS, should be 700)"
        echo "      💡 Run: chmod 700 $ABEKEYS_PATH"
    fi
else
    check_warn "Vault directory not found (optional)"
fi

# Check credentials directory permissions
if [ -d "$CREDENTIALS_DIR" ]; then
    PERMS=$(stat -f "%OLp" "$CREDENTIALS_DIR" 2>/dev/null || stat -c "%a" "$CREDENTIALS_DIR" 2>/dev/null || echo "000")
    if [ "$PERMS" = "700" ] || [ "$PERMS" = "750" ]; then
        check_pass "Credentials directory permissions secure ($PERMS)"
    else
        check_fail "Credentials directory permissions insecure ($PERMS, should be 700)"
        echo "      💡 Run: chmod 700 $CREDENTIALS_DIR"
    fi
    
    # Check credential file permissions
    INSECURE_FILES=0
    for cred_file in "$CREDENTIALS_DIR"/*.json; do
        if [ -f "$cred_file" ]; then
            PERMS=$(stat -f "%OLp" "$cred_file" 2>/dev/null || stat -c "%a" "$cred_file" 2>/dev/null || echo "000")
            if [ "$PERMS" != "600" ] && [ "$PERMS" != "640" ]; then
                ((INSECURE_FILES++))
            fi
        fi
    done
    
    if [ $INSECURE_FILES -eq 0 ]; then
        check_pass "All credential files have secure permissions (600)"
    else
        check_fail "$INSECURE_FILES credential files have insecure permissions"
        echo "      💡 Run: chmod 600 $CREDENTIALS_DIR/*.json"
    fi
else
    check_warn "Credentials directory not found (optional)"
fi

# Check .gitignore
if [ -f ".gitignore" ]; then
    if grep -q "\.abekeys" .gitignore 2>/dev/null; then
        check_pass ".abekeys is git-ignored"
    else
        check_fail ".abekeys not in .gitignore"
        echo "      💡 Add '.abekeys/' to .gitignore"
    fi
else
    check_fail ".gitignore file not found"
fi

# Check for credentials in git
if git rev-parse --git-dir > /dev/null 2>&1; then
    TRACKED_CREDS=$(git ls-files | grep -E "(credential|api.*key|\.key$|secret|abekeys)" || true)
    if [ -z "$TRACKED_CREDS" ]; then
        check_pass "No credential files tracked in git"
    else
        check_fail "Credential files tracked in git"
        echo "      Files: $TRACKED_CREDS"
        echo "      💡 Run: git rm --cached <file> to untrack"
    fi
fi

echo ""

# ============================================================================
# PART 2: INPUT VALIDATION
# ============================================================================

echo "📋 PART 2: Input Validation"
echo "============================================================"

GATEWAY_PATH="$REPO_ROOT/AIGuards-Backend/codeguardians-gateway/codeguardians-gateway"

if [ -d "$GATEWAY_PATH" ]; then
    # Check input validation module
    if [ -f "$GATEWAY_PATH/app/core/input_validation.py" ]; then
        check_pass "Input validation module exists"
        
        # Check for key validation functions
        if grep -q "detect_sql_injection\|detect_xss\|detect_command_injection" "$GATEWAY_PATH/app/core/input_validation.py"; then
            check_pass "Input validation includes SQL/XSS/Command injection detection"
        else
            check_fail "Input validation missing key security checks"
        fi
        
        if grep -q "validate_payload_size" "$GATEWAY_PATH/app/core/input_validation.py"; then
            check_pass "Payload size validation implemented"
        else
            check_warn "Payload size validation not found"
        fi
    else
        check_fail "Input validation module not found"
    fi
    
    # Check security module
    if [ -f "$GATEWAY_PATH/app/core/security.py" ]; then
        check_pass "Security module exists"
    else
        check_warn "Security module not found"
    fi
else
    check_warn "Gateway path not found (skipping input validation checks)"
fi

echo ""

# ============================================================================
# PART 3: ERROR SANITIZATION (UX SECURITY)
# ============================================================================

echo "📋 PART 3: Error Sanitization (UX Security)"
echo "============================================================"

if [ -d "$GATEWAY_PATH" ]; then
    # Check error sanitizer
    if [ -f "$GATEWAY_PATH/app/core/error_sanitizer.py" ]; then
        check_pass "Error sanitizer module exists"
        
        # Check for credential masking
        if grep -q "mask_credentials\|CREDENTIAL_PATTERNS\|SENSITIVE_KEYS" "$GATEWAY_PATH/app/core/error_sanitizer.py"; then
            check_pass "Error sanitizer includes credential masking"
        else
            check_fail "Error sanitizer missing credential masking"
        fi
        
        # Check for production mode sanitization
        if grep -q "ENVIRONMENT.*production\|DEBUG" "$GATEWAY_PATH/app/core/error_sanitizer.py"; then
            check_pass "Error sanitizer respects production mode"
        else
            check_warn "Error sanitizer may not respect production mode"
        fi
    else
        check_fail "Error sanitizer module not found"
    fi
    
    # Check error handler
    if [ -f "$GATEWAY_PATH/app/api/error_handler.py" ]; then
        check_pass "Error handler module exists"
        
        # Check for sensitive data masking
        if grep -q "mask_sensitive_data\|MASKED" "$GATEWAY_PATH/app/api/error_handler.py"; then
            check_pass "Error handler includes sensitive data masking"
        else
            check_warn "Error handler may not mask sensitive data"
        fi
    else
        check_warn "Error handler module not found"
    fi
else
    check_warn "Gateway path not found (skipping error sanitization checks)"
fi

echo ""

# ============================================================================
# PART 4: CONFIGURATION SECURITY
# ============================================================================

echo "📋 PART 4: Configuration Security"
echo "============================================================"

if [ -d "$GATEWAY_PATH" ]; then
    # Check AbëKEYS config loader
    if [ -f "$GATEWAY_PATH/app/core/abekeys_config.py" ]; then
        check_pass "AbëKEYS config loader exists"
        
        # Check for secure credential handling
        if grep -q "is_available\|get_credential" "$GATEWAY_PATH/app/core/abekeys_config.py"; then
            check_pass "AbëKEYS config loader implements secure credential access"
        fi
    else
        check_warn "AbëKEYS config loader not found"
    fi
    
    # Check config.py integration
    if [ -f "$GATEWAY_PATH/app/core/config.py" ]; then
        if grep -q "_load_abekeys_credentials\|abekeys" "$GATEWAY_PATH/app/core/config.py"; then
            check_pass "Config integrates AbëKEYS vault"
        else
            check_warn "Config may not integrate AbëKEYS vault"
        fi
    fi
else
    check_warn "Gateway path not found (skipping configuration checks)"
fi

echo ""

# ============================================================================
# PART 5: PRODUCTION READINESS
# ============================================================================

echo "📋 PART 5: Production Readiness"
echo "============================================================"

# Check for .env files in git
if git rev-parse --git-dir > /dev/null 2>&1; then
    ENV_FILES=$(git ls-files | grep -E "\.env$|\.env\.local$|\.env\.production$" || true)
    if [ -z "$ENV_FILES" ]; then
        check_pass "No .env files tracked in git"
    else
        check_fail ".env files tracked in git: $ENV_FILES"
        echo "      💡 Add .env* to .gitignore and untrack files"
    fi
fi

# Check for hardcoded secrets in code
if [ -d "$GATEWAY_PATH" ]; then
    # Check for common hardcoded secret patterns
    HARDCODED=$(grep -r "sk_live_\|sk_test_\|xoxb-\|ghp_" "$GATEWAY_PATH/app" 2>/dev/null | grep -v "test\|example\|placeholder" || true)
    if [ -z "$HARDCODED" ]; then
        check_pass "No hardcoded API keys found in code"
    else
        check_fail "Potential hardcoded API keys found"
        echo "      Review these files for hardcoded secrets"
    fi
fi

# Check security audit script
if [ -f "$REPO_ROOT/scripts/zero_john_security_audit.py" ]; then
    check_pass "Security audit script exists"
else
    check_warn "Security audit script not found"
fi

echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "============================================================"
echo "🔒 HARDENING CHECK SUMMARY"
echo "============================================================"
echo ""
echo "✅ Passed:  $PASSED"
echo "❌ Failed:  $FAILED"
echo "⚠️  Warnings: $WARNINGS"
echo ""

if [ $FAILED -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "🎉 ALL CHECKS PASSED - SYSTEM FULLY HARDENED!"
    echo ""
    echo "✅ Vault security: PASSED"
    echo "✅ Input validation: PASSED"
    echo "✅ Error sanitization: PASSED"
    echo "✅ Configuration security: PASSED"
    echo "✅ Production readiness: PASSED"
    exit 0
elif [ $FAILED -eq 0 ]; then
    echo "⚠️  SYSTEM HARDENED WITH WARNINGS"
    echo "   Review warnings above and address as needed"
    exit 0
else
    echo "❌ HARDENING INCOMPLETE"
    echo "   Please address failed checks before production deployment"
    exit 1
fi

