#!/usr/bin/env python3
"""Generate all preflight enforcement scripts"""
import os

scripts_dir = os.path.dirname(os.path.abspath(__file__))

scripts = {
    'bravetto_preflight.sh': '''#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FAILURES=0
RED='\\033[0;31m'
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
NC='\\033[0m'
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}${NC} $1"; }
log_error() { echo -e "${RED}${NC} $1"; ((FAILURES++)) || true; }
echo " BRAVETTO PREFLIGHT - Danny Rules Enforcement"
"$SCRIPT_DIR/check_env.sh" "$REPO_ROOT" || log_error "Environment check failed"
"$SCRIPT_DIR/validate_repo_structure.sh" "$REPO_ROOT" || log_error "Repo structure validation failed"
"$SCRIPT_DIR/secret_scan.sh" "$REPO_ROOT" || log_error "Secret scan failed"
"$SCRIPT_DIR/validate_dockerfile.sh" "$REPO_ROOT" || log_error "Dockerfile validation failed"
"$SCRIPT_DIR/validate_helm.sh" "$REPO_ROOT" || log_error "Helm validation failed"
"$SCRIPT_DIR/validate_service_yaml.sh" "$REPO_ROOT" || log_error "Service YAML validation failed"
"$SCRIPT_DIR/remove_commented_code.sh" "$REPO_ROOT" || log_error "Commented code removal failed"
if [ $FAILURES -eq 0 ]; then log_success "All checks passed!"; exit 0; else exit 1; fi
''',
    'check_env.sh': '''#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
check_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing: $1"; ((FAILURES++)); }; }
check_cmd helm
check_cmd docker
check_cmd kubectl
[ -z "${AWS_PROFILE:-}" ] && [ -z "${AWS_ACCESS_KEY_ID:-}" ] && { echo "AWS credentials not configured"; ((FAILURES++)); }
tailscale status >/dev/null 2>&1 || { echo "Tailscale not logged in"; ((FAILURES++)); }
exit $FAILURES
''',
    'validate_repo_structure.sh': '''#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
[ ! -f "$REPO_ROOT/Dockerfile" ] && { echo "Dockerfile missing in root"; ((FAILURES++)); }
[ ! -d "$REPO_ROOT/src" ] && { echo "src/ directory missing"; ((FAILURES++)); }
[ ! -d "$REPO_ROOT/helm" ] && { echo "helm/ directory missing"; ((FAILURES++)); }
[ ! -f "$REPO_ROOT/README.md" ] && { echo "README.md missing"; ((FAILURES++)); }
exit $FAILURES
''',
    'secret_scan.sh': '''#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
PATTERNS=("AKIA[0-9A-Z]{16}" "arn:aws:iam::[0-9]{12}" "ghp_[A-Za-z0-9]{36}" "sk_live_[0-9A-Za-z]{32}")
for pattern in "${PATTERNS[@]}"; do
    if grep -r "$pattern" "$REPO_ROOT" --exclude-dir=.git 2>/dev/null; then
        echo "Found secret pattern: $pattern"; ((FAILURES++))
    fi
done
[ -f "$REPO_ROOT/.env" ] && { echo ".env file found (should not be committed)"; ((FAILURES++)); }
exit $FAILURES
''',
    'validate_dockerfile.sh': '''#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
find "$REPO_ROOT" -name "Dockerfile" -type f | while read -r df; do
    grep -q "^FROM" "$df" || { echo "Invalid Dockerfile: $df"; ((FAILURES++)); }
    grep -q "RUN.*--no-cache" "$df" || echo "Warning: Dockerfile may use cache: $df"
done
exit $FAILURES
''',
    'validate_helm.sh': '''#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
find "$REPO_ROOT" -path "*/helm/*" -name "values.yaml" -o -path "*/helm/*" -name "Chart.yaml" | while read -r f; do
    [ -f "$f" ] || continue
    dir=$(dirname "$f")
    helm lint "$dir" >/dev/null 2>&1 || { echo "Helm lint failed: $dir"; ((FAILURES++)); }
done
exit $FAILURES
''',
    'validate_service_yaml.sh': '''#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
find "$REPO_ROOT" -name "service.yaml" -type f | while read -r svc; do
    grep -q "type: ClusterIP" "$svc" || { echo "Service not ClusterIP: $svc"; ((FAILURES++)); }
    grep -q "type: NodePort" "$svc" && { echo "NodePort found (forbidden): $svc"; ((FAILURES++)); }
done
exit $FAILURES
''',
    'remove_commented_code.sh': '''#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
WARNINGS=0
find "$REPO_ROOT" -type f \\( -name "*.py" -o -name "*.js" -o -name "*.ts" \\) -not -path "*/.git/*" | while read -r f; do
    lines=$(grep -n "^[[:space:]]*#[[:space:]]*[a-zA-Z]" "$f" 2>/dev/null | wc -l)
    [ "$lines" -gt 10 ] && echo "Warning: Many commented lines in $f"
done
exit 0
'''
}

for name, content in scripts.items():
    path = os.path.join(scripts_dir, name)
    with open(path, 'w') as f:
        f.write(content)
    os.chmod(path, 0o755)
    print(f"Created {path}")

print("\n All preflight scripts created!")

