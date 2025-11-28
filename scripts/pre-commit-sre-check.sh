#!/bin/bash
# PRE-COMMIT SRE CHECK
# Validates SRE compliance before allowing commit

cd "$(dirname "$0")/.."

echo " Running SRE compliance check..."

node scripts/sre-audit.js

if [ $? -ne 0 ]; then
  echo ""
  echo " SRE compliance check failed"
  echo "Fix violations above before committing"
  exit 1
fi

echo " SRE compliance check passed"
exit 0

