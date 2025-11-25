#!/bin/bash
# Cursor Command Handler
# Routes Cursor commands to their respective execution scripts
# Pattern: COMMAND × ROUTE × EXECUTE × ONE

set -euo pipefail

COMMAND_NAME="$1"
shift  # Remove command name from arguments

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Route commands to their handlers
case "$COMMAND_NAME" in
    "manifest")
        exec python3 "$SCRIPT_DIR/manifest-engine.py" "$@"
        ;;
    "path-health")
        exec python3 "$SCRIPT_DIR/path-health-restore.py" "$@"
        ;;
    "converge")
        exec python3 "$SCRIPT_DIR/converge-engine.py" "$@"
        ;;
    "ae")
        exec python3 "$SCRIPT_DIR/ae-engine.py" "$@"
        ;;
    "prime")
        exec python3 "$SCRIPT_DIR/prime-engine.py" "$@"
        ;;
    "create")
        exec python3 "$SCRIPT_DIR/create-engine.py" "$@"
        ;;
    "aeon")
        exec python3 "$SCRIPT_DIR/aeon.py" "$@"
        ;;
    "val")
        exec python3 "$SCRIPT_DIR/val-engine.py" "$@"
        ;;
    "revenue")
        exec python3 "$SCRIPT_DIR/revenue-engine.py" "$@"
        ;;
    "push-suite")
        exec bash "$SCRIPT_DIR/git-push-complete-suite.sh" "$@"
        ;;
    "trigger")
        exec python3 "$SCRIPT_DIR/trigger-engine.py" "$@"
        ;;
    "flow")
        exec python3 "$SCRIPT_DIR/abeone-flow-engine.py" "$@"
        ;;
    "axiom")
        exec python3 "$SCRIPT_DIR/axiom-engine.py" "$@"
        ;;
    "epistemic")
        exec python3 "$SCRIPT_DIR/abeone-epistemic-search.py" "$@"
        ;;
    "pattern")
        exec python3 "$SCRIPT_DIR/pattern-engine.py" "$@"
        ;;
    "sync")
        exec python3 "$SCRIPT_DIR/sync-engine.py" "$@"
        ;;
    "memory")
        exec python3 "$SCRIPT_DIR/memory-engine.py" "$@"
        ;;
    "kernel")
        exec python3 "$SCRIPT_DIR/kernel-engine.py" "$@"
        ;;
    "validate")
        exec python3 "$SCRIPT_DIR/abeone-validator.py" "$@"
        ;;
    "disk-onboard")
        exec python3 "$SCRIPT_DIR/disk-epistemic-onboarding.py" "$@"
        ;;
    *)
        echo "❌ Unknown command: $COMMAND_NAME"
        echo "Available commands: manifest, path-health, converge, ae, prime, create, aeon, val, revenue, push-suite, trigger, flow, axiom, epistemic, pattern, sync, memory, kernel, validate, disk-onboard"
        exit 1
        ;;
esac

