#!/bin/bash
# REGENERATE IGNORE PATTERN LOCK FILE WITH REAL SUBSTRATE HASHES
# This script computes real SHA256 hashes from actual substrate arrays

cd "$(dirname "$0")/.."

echo " Regenerating .ignore-pattern-lock.json with real substrate hashes..."
node scripts/compute-ignore-lock.js > .ignore-pattern-lock.json

echo " Lock file regenerated"
echo " Validating..."
node scripts/validate-ignore-lock.js

if [ $? -eq 0 ]; then
  echo " Lock file is SRE compliant!"
else
  echo " Validation failed - check output above"
  exit 1
fi

