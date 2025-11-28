#!/bin/bash
set -e

echo " Generating ignore-pattern lockfile..."

# Generate lockfile from computation script
node scripts/compute-ignore-lock.js > .ignore-pattern-lock.json

echo " Lockfile generated"

# Verify lockfile integrity
echo " Verifying lockfile..."
if node scripts/verify-ignore-lock.js; then
  echo " Lockfile verified - SEALED"
  exit 0
else
  echo " Lockfile verification failed"
  exit 1
fi

