#!/bin/bash
# PRE-WORK VALIDATION HOOK
# 
# Run this before starting any work session
# Validates project boundaries and prevents drift
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "🛡️  PRE-WORK VALIDATION"
echo "============================================================"
echo ""

# Run context boot validation
node "$SCRIPT_DIR/context-boot-validation.js"

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo ""
  echo "🚨 VALIDATION FAILED - DO NOT PROCEED"
  echo "   Fix issues above before starting work"
  echo ""
  exit 1
else
  echo ""
  echo "✅ VALIDATION PASSED - SAFE TO PROCEED"
  echo ""
fi

exit $EXIT_CODE

