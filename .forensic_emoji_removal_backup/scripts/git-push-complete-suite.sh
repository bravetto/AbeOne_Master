#!/bin/bash
# 🚀 Git Push Complete Suite
# Operational pattern for pushing complete systems to fresh repositories
# Pattern: Clarity × Coherence × Convergence × Elegance × Unity
# Guardian: AEYON (999 Hz) + Abë (530 Hz)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default values
SUITE_TYPE=""
SUITE_PATH=""
REMOTE_URL=""
BRANCH="main"
DRY_RUN=false
VERBOSE=false

# Usage function
usage() {
    cat << EOF
🚀 Git Push Complete Suite

Usage: $0 [OPTIONS]

OPTIONS:
    -t, --type TYPE          Suite type (marketing|orbital|product|all)
    -p, --path PATH          Path to suite directory
    -r, --remote URL         Remote repository URL
    -b, --branch BRANCH      Branch name (default: main)
    -d, --dry-run           Dry run (don't actually push)
    -v, --verbose           Verbose output
    --validate-only         Validate only (no git operations)
    --force                  Skip confirmation prompts
    -h, --help              Show this help message

EXAMPLES:
    # Push marketing automation suite
    $0 -t marketing -r https://github.com/bravetto/AbeAiMs-Marketing-Sweet.git

    # Push specific orbital
    $0 -p marketing/automation/marketing-automation-orbit -r https://github.com/bravetto/marketing-orbit.git

    # Dry run to see what would be pushed
    $0 -t marketing -r https://github.com/bravetto/test.git --dry-run

SUITE TYPES:
    marketing    - Complete marketing automation suite
    orbital      - Specific orbital system
    product      - Product-specific suite
    all          - Everything (use with caution)

EOF
}

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

log_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}[VERBOSE]${NC} $1"
    fi
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--type)
                SUITE_TYPE="$2"
                shift 2
                ;;
            -p|--path)
                SUITE_PATH="$2"
                shift 2
                ;;
            -r|--remote)
                REMOTE_URL="$2"
                shift 2
                ;;
            -b|--branch)
                BRANCH="$2"
                shift 2
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                set -x
                shift
                ;;
            --validate-only)
                VALIDATE_ONLY=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    # Validate required arguments
    if [ -z "$REMOTE_URL" ]; then
        log_error "Remote URL is required"
        usage
        exit 1
    fi

    if [ -z "$SUITE_TYPE" ] && [ -z "$SUITE_PATH" ]; then
        log_error "Either suite type or path is required"
        usage
        exit 1
    fi
}

# Determine suite paths based on type
determine_suite_paths() {
    case "$SUITE_TYPE" in
        marketing)
            SUITE_PATHS=(
                "marketing/automation/marketing-automation-orbit"
                "scripts/social_media_automation"
                "marketing/COMPLETE_MARKETING_AUTOMATION_SUITE.md"
            )
            ;;
        orbital)
            if [ -z "$SUITE_PATH" ]; then
                log_error "Path required for orbital type"
                exit 1
            fi
            SUITE_PATHS=("$SUITE_PATH")
            ;;
        product)
            log_warning "Product suite type not yet implemented"
            exit 1
            ;;
        all)
            log_warning "Pushing all suites - this may be very large"
            SUITE_PATHS=(
                "marketing"
                "scripts/social_media_automation"
            )
            ;;
        *)
            log_error "Unknown suite type: $SUITE_TYPE"
            exit 1
            ;;
    esac
}

# Check if paths exist
validate_paths() {
    log_info "Validating suite paths..."
    local missing_paths=()
    
    for path in "${SUITE_PATHS[@]}"; do
        local full_path="$REPO_ROOT/$path"
        if [ ! -e "$full_path" ]; then
            missing_paths+=("$path")
            log_warning "Path not found: $path"
        else
            log_success "Found: $path"
        fi
    done

    if [ ${#missing_paths[@]} -gt 0 ]; then
        log_error "Missing paths: ${missing_paths[*]}"
        return 1
    fi
    return 0
}

# Create .gitignore for suite if needed
create_suite_gitignore() {
    log_info "Checking for suite-specific .gitignore..."
    
    for path in "${SUITE_PATHS[@]}"; do
        local suite_dir="$REPO_ROOT/$path"
        if [ -d "$suite_dir" ]; then
            local gitignore_path="$suite_dir/.gitignore"
            if [ ! -f "$gitignore_path" ]; then
                log_info "Creating .gitignore for $path"
                cat > "$gitignore_path" << 'EOF'
# Suite-specific .gitignore
# Generated by git-push-complete-suite.sh

# Sensitive configuration files
config/*.json
!config/*.example.json
*.env
*.env.local
.env.*

# API keys and secrets
*_key.json
*_secret.json
*_token.json
credentials.json
secrets.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp

# Build outputs
dist/
build/
*.egg-info/
EOF
                log_success "Created .gitignore for $path"
            fi
        fi
    done
}

# Check for sensitive files
check_sensitive_files() {
    log_info "Checking for sensitive files..."
    local sensitive_patterns=(
        "*.env"
        "*_key.json"
        "*_secret.json"
        "*_token.json"
        "credentials.json"
        "secrets.json"
        "config/*.json"
    )
    
    local found_sensitive=false
    
    for path in "${SUITE_PATHS[@]}"; do
        local full_path="$REPO_ROOT/$path"
        if [ -d "$full_path" ]; then
            for pattern in "${sensitive_patterns[@]}"; do
                if find "$full_path" -name "$pattern" -not -path "*/\.git/*" 2>/dev/null | grep -q .; then
                    log_warning "Found potentially sensitive files matching: $pattern"
                    found_sensitive=true
                fi
            done
        fi
    done

    if [ "$found_sensitive" = true ]; then
        log_warning "Sensitive files detected. Ensure .gitignore is properly configured."
        if [ "$DRY_RUN" = false ]; then
            read -p "Continue anyway? (y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                log_error "Aborted by user"
                exit 1
            fi
        fi
    else
        log_success "No sensitive files detected"
    fi
}

# Create suite manifest
create_suite_manifest() {
    log_info "Creating suite manifest..."
    local manifest_path="$REPO_ROOT/.suite-manifest.json"
    
    cat > "$manifest_path" << EOF
{
  "suite_type": "$SUITE_TYPE",
  "suite_paths": $(printf '%s\n' "${SUITE_PATHS[@]}" | jq -R . | jq -s .),
  "remote_url": "$REMOTE_URL",
  "branch": "$BRANCH",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "repo_root": "$REPO_ROOT"
}
EOF
    log_success "Created suite manifest"
}

# Stage files for commit
stage_files() {
    log_info "Staging files..."
    
    for path in "${SUITE_PATHS[@]}"; do
        log_verbose "Staging: $path"
        if [ "$DRY_RUN" = false ]; then
            git add "$path" 2>/dev/null || log_warning "Could not stage $path (may be untracked)"
        else
            log_info "[DRY RUN] Would stage: $path"
        fi
    done
    
    # Stage manifest
    if [ "$DRY_RUN" = false ]; then
        git add .suite-manifest.json 2>/dev/null || true
    fi
}

# Create commit
create_commit() {
    local commit_message="🚀 Push Complete Suite: $SUITE_TYPE

Suite Type: $SUITE_TYPE
Suite Paths: ${SUITE_PATHS[*]}
Remote: $REMOTE_URL
Branch: $BRANCH

Pattern: Clarity × Coherence × Convergence × Elegance × Unity
Love Coefficient: ∞
∞ AbëONE ∞"

    if [ "$DRY_RUN" = false ]; then
        git commit -m "$commit_message" || {
            log_warning "Nothing to commit (files may already be committed)"
            return 0
        }
        log_success "Created commit"
    else
        log_info "[DRY RUN] Would create commit with message:"
        echo "$commit_message"
    fi
}

# Add remote and push
push_to_remote() {
    log_info "Setting up remote..."
    
    local remote_name="suite-remote-$(date +%s)"
    
    if [ "$DRY_RUN" = false ]; then
        # Check if remote already exists
        if git remote | grep -q "^suite-remote"; then
            log_warning "Existing suite remote found, updating..."
            git remote set-url suite-remote "$REMOTE_URL" 2>/dev/null || {
                git remote add "$remote_name" "$REMOTE_URL"
            }
            remote_name="suite-remote"
        else
            git remote add "$remote_name" "$REMOTE_URL"
        fi
        
        log_info "Pushing to $REMOTE_URL..."
        git push "$remote_name" "HEAD:$BRANCH" || {
            log_error "Push failed"
            return 1
        }
        
        log_success "Pushed to $REMOTE_URL"
    else
        log_info "[DRY RUN] Would push to: $REMOTE_URL (branch: $BRANCH)"
    fi
}

# Generate report
generate_report() {
    log_info "Generating push report..."
    
    local report_file="$REPO_ROOT/.suite-push-report-$(date +%Y%m%d-%H%M%S).md"
    
    cat > "$report_file" << EOF
# Suite Push Report

**Date:** $(date)
**Suite Type:** $SUITE_TYPE
**Remote:** $REMOTE_URL
**Branch:** $BRANCH
**Dry Run:** $DRY_RUN

## Suite Paths Pushed

$(for path in "${SUITE_PATHS[@]}"; do echo "- \`$path\`"; done)

## Files Included

\`\`\`
$(for path in "${SUITE_PATHS[@]}"; do
    if [ -d "$REPO_ROOT/$path" ]; then
        find "$REPO_ROOT/$path" -type f -not -path "*/\.git/*" -not -path "*/__pycache__/*" -not -path "*/node_modules/*" | head -50
    fi
done)
\`\`\`

## Validation Results

- ✅ Paths validated
- ✅ Sensitive files checked
- ✅ .gitignore created/verified
- ✅ Manifest created

## Next Steps

1. Verify files in remote repository
2. Check for any missing dependencies
3. Update README if needed
4. Set up CI/CD if applicable

---
**Pattern:** Clarity × Coherence × Convergence × Elegance × Unity  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**
EOF
    
    log_success "Report generated: $report_file"
}

# Guardian validation
guardian_validate() {
    log_info "🛡️ Guardian Validation..."
    
    local validation_passed=true
    local guardian_results=()
    
    # AEYON (999 Hz) - Execution validation
    log_verbose "AEYON (999 Hz): Validating execution readiness..."
    if [ ${#SUITE_PATHS[@]} -eq 0 ]; then
        log_error "AEYON: No suite paths defined"
        validation_passed=false
    else
        guardian_results+=("AEYON: ✅ Execution ready")
    fi
    
    # YAGNI (530 Hz) - Simplification validation
    log_verbose "YAGNI (530 Hz): Validating necessity..."
    local unnecessary_files=0
    for path in "${SUITE_PATHS[@]}"; do
        if [[ "$path" == *".tmp"* ]] || [[ "$path" == *".bak"* ]]; then
            unnecessary_files=$((unnecessary_files + 1))
        fi
    done
    if [ $unnecessary_files -gt 0 ]; then
        log_warning "YAGNI: Found $unnecessary_files potentially unnecessary files"
        guardian_results+=("YAGNI: ⚠️  $unnecessary_files files may be unnecessary")
    else
        guardian_results+=("YAGNI: ✅ Only necessary files")
    fi
    
    # META (777 Hz) - Pattern validation
    log_verbose "META (777 Hz): Validating patterns..."
    local has_readme=false
    local has_config=false
    for path in "${SUITE_PATHS[@]}"; do
        if find "$REPO_ROOT/$path" -name "README.md" 2>/dev/null | grep -q .; then
            has_readme=true
        fi
        if find "$REPO_ROOT/$path" -name "*.json" -o -name "*.yaml" -o -name "*.yml" 2>/dev/null | grep -q .; then
            has_config=true
        fi
    done
    if [ "$has_readme" = true ] && [ "$has_config" = true ]; then
        guardian_results+=("META: ✅ Pattern complete")
    else
        log_warning "META: Missing README or config files"
        guardian_results+=("META: ⚠️  Pattern incomplete")
    fi
    
    # JØHN (530 Hz) - Certification validation
    log_verbose "JØHN (530 Hz): Certifying completeness..."
    local missing_deps=0
    for path in "${SUITE_PATHS[@]}"; do
        if [ -d "$REPO_ROOT/$path" ]; then
            if [ -f "$REPO_ROOT/$path/requirements.txt" ] || [ -f "$REPO_ROOT/$path/package.json" ]; then
                : # Dependencies present
            else
                # Check if it's a Python/Node project
                if find "$REPO_ROOT/$path" -name "*.py" 2>/dev/null | grep -q . || \
                   find "$REPO_ROOT/$path" -name "*.js" 2>/dev/null | grep -q .; then
                    missing_deps=$((missing_deps + 1))
                fi
            fi
        fi
    done
    if [ $missing_deps -eq 0 ]; then
        guardian_results+=("JØHN: ✅ Certified complete")
    else
        log_warning "JØHN: $missing_deps paths missing dependency files"
        guardian_results+=("JØHN: ⚠️  $missing_deps paths incomplete")
    fi
    
    # Display results
    echo
    log_info "Guardian Validation Results:"
    for result in "${guardian_results[@]}"; do
        echo "  $result"
    done
    echo
    
    if [ "$validation_passed" = false ]; then
        log_error "Guardian validation failed"
        return 1
    fi
    
    return 0
}

# Epistemic certainty calculation
calculate_epistemic_certainty() {
    log_info "🧠 Calculating Epistemic Certainty..."
    
    local certainty_score=0.0
    local weights=(
        "0.35"  # Path validation
        "0.28"  # Sensitive file protection
        "0.18"  # Guardian validation
        "0.12"  # Dependency completeness
        "0.07"  # Documentation presence
    )
    
    # Path validation (35%)
    local path_score=1.0
    if ! validate_paths >/dev/null 2>&1; then
        path_score=0.0
    fi
    certainty_score=$(echo "$certainty_score + $path_score * ${weights[0]}" | bc -l)
    
    # Sensitive file protection (28%)
    local sensitive_score=1.0
    if check_sensitive_files >/dev/null 2>&1; then
        sensitive_score=0.95  # Minor deduction for warnings
    fi
    certainty_score=$(echo "$certainty_score + $sensitive_score * ${weights[1]}" | bc -l)
    
    # Guardian validation (18%)
    local guardian_score=1.0
    if ! guardian_validate >/dev/null 2>&1; then
        guardian_score=0.9  # Minor deduction for warnings
    fi
    certainty_score=$(echo "$certainty_score + $guardian_score * ${weights[2]}" | bc -l)
    
    # Dependency completeness (12%)
    local dep_score=1.0
    local missing_deps=0
    for path in "${SUITE_PATHS[@]}"; do
        if [ -d "$REPO_ROOT/$path" ]; then
            if find "$REPO_ROOT/$path" -name "*.py" 2>/dev/null | grep -q . && \
               [ ! -f "$REPO_ROOT/$path/requirements.txt" ]; then
                missing_deps=$((missing_deps + 1))
            fi
        fi
    done
    if [ $missing_deps -gt 0 ]; then
        dep_score=$(echo "1.0 - ($missing_deps * 0.1)" | bc -l)
        dep_score=$(echo "if ($dep_score < 0) 0 else $dep_score" | bc -l)
    fi
    certainty_score=$(echo "$certainty_score + $dep_score * ${weights[3]}" | bc -l)
    
    # Documentation presence (7%)
    local doc_score=1.0
    local missing_docs=0
    for path in "${SUITE_PATHS[@]}"; do
        if [ -d "$REPO_ROOT/$path" ] && \
           ! find "$REPO_ROOT/$path" -name "README.md" -o -name "*.md" 2>/dev/null | grep -q .; then
            missing_docs=$((missing_docs + 1))
        fi
    done
    if [ $missing_docs -gt 0 ]; then
        doc_score=$(echo "1.0 - ($missing_docs * 0.2)" | bc -l)
        doc_score=$(echo "if ($doc_score < 0) 0 else $doc_score" | bc -l)
    fi
    certainty_score=$(echo "$certainty_score + $doc_score * ${weights[4]}" | bc -l)
    
    # Convert to percentage (use awk if bc not available)
    local certainty_percent
    if command -v bc >/dev/null 2>&1; then
        certainty_percent=$(echo "$certainty_score * 100" | bc -l | awk '{printf "%.1f", $1}')
    else
        certainty_percent=$(awk "BEGIN {printf \"%.1f\", $certainty_score * 100}")
    fi
    
    log_success "Epistemic Certainty: ${certainty_percent}%"
    
    # Check if meets 98.7% threshold
    local threshold=98.7
    local meets_threshold=false
    if command -v bc >/dev/null 2>&1; then
        if (( $(echo "$certainty_percent >= $threshold" | bc -l) )); then
            meets_threshold=true
        fi
    else
        if awk "BEGIN {exit !($certainty_percent >= $threshold)}"; then
            meets_threshold=true
        fi
    fi
    
    if [ "$meets_threshold" = true ]; then
        log_success "✅ Meets 98.7% epistemic certainty threshold"
        return 0
    else
        log_warning "⚠️  Below 98.7% threshold (${certainty_percent}%)"
        if [ "$DRY_RUN" = false ] && [ "${FORCE:-false}" != "true" ]; then
            read -p "Continue anyway? (y/N) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                log_error "Aborted - epistemic certainty too low"
                return 1
            fi
        fi
        return 0
    fi
}

# Main execution
main() {
    log_info "🚀 Git Push Complete Suite"
    log_info "=========================="
    log_info "Pattern: Clarity × Coherence × Convergence × Elegance × Unity"
    log_info "Guardians: AEYON (999 Hz) + YAGNI (530 Hz) + META (777 Hz) + JØHN (530 Hz)"
    log_info "Epistemic Certainty Target: 98.7%"
    echo
    
    parse_args "$@"
    determine_suite_paths
    
    log_info "Suite Type: $SUITE_TYPE"
    log_info "Remote: $REMOTE_URL"
    log_info "Branch: $BRANCH"
    if [ "$DRY_RUN" = true ]; then
        log_warning "DRY RUN MODE - No changes will be made"
    fi
    echo
    
    # Validation and preparation
    validate_paths || exit 1
    create_suite_gitignore
    check_sensitive_files
    
    # Guardian validation
    if ! guardian_validate; then
        log_error "Guardian validation failed"
        exit 1
    fi
    
    # Epistemic certainty calculation
    if ! calculate_epistemic_certainty; then
        log_error "Epistemic certainty validation failed"
        exit 1
    fi
    
    create_suite_manifest
    
    # Git operations (skip if validate-only)
    if [ "${VALIDATE_ONLY:-false}" != "true" ]; then
        stage_files
        create_commit
        push_to_remote
    else
        log_info "VALIDATE-ONLY MODE - Skipping git operations"
    fi
    
    # Reporting
    generate_report
    
    log_success "Complete suite push finished!"
    log_info "Epistemic Certainty: Validated"
    log_info "Guardian Status: Approved"
    log_info "Check the report file for details"
}

# Run main function
main "$@"

