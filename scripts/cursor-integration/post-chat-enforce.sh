#!/bin/bash
# Post-chat enforcement wrapper
cd "$(dirname "$0")/../../AIGuards-Backend-orbital"
python3 scripts/ENFORCE_ETERNAL_INTEGRATION.py --output "${1:-}" 2>&1 | grep -v "^$" || true
