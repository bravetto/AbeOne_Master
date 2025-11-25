#!/bin/bash
# Pre-chat enforcement wrapper
cd "$(dirname "$0")/../../AIGuards-Backend-orbital"
python3 scripts/ENFORCE_ETERNAL_INTEGRATION.py --input "${1:-}" 2>&1 | grep -v "^$" || true
