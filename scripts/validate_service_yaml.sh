#!/bin/bash
set -euo pipefail
REPO_ROOT="${1:-$(pwd)}"
FAILURES=0
find "$REPO_ROOT" -name "service.yaml" -type f | while read -r svc; do
    grep -q "type: ClusterIP" "$svc" || { echo "Service not ClusterIP: $svc"; ((FAILURES++)); }
    grep -q "type: NodePort" "$svc" && { echo "NodePort found (forbidden): $svc"; ((FAILURES++)); }
done
exit $FAILURES
