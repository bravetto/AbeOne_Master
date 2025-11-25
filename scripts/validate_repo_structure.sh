#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
[ ! -f "$REPO_ROOT/Dockerfile" ] && { echo "Dockerfile missing in root"; ((FAILURES++)); }
[ ! -d "$REPO_ROOT/src" ] && { echo "src/ directory missing"; ((FAILURES++)); }
[ ! -d "$REPO_ROOT/helm" ] && { echo "helm/ directory missing"; ((FAILURES++)); }
[ ! -f "$REPO_ROOT/README.md" ] && { echo "README.md missing"; ((FAILURES++)); }
exit $FAILURES
