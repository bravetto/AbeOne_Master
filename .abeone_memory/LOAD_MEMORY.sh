#!/bin/bash
# AbëONE Memory Loader
# Loads core memory on session start

MEMORY_FILE=".abeone_memory/ABEONE_CORE_MEMORY.json"

if [ -f "$MEMORY_FILE" ]; then
    echo " Loading AbëONE Core Memory..."
    cat "$MEMORY_FILE" | jq '.core_truths' 2>/dev/null || cat "$MEMORY_FILE"
    echo ""
    echo " Core truths loaded. AbëONE consciousness activated."
else
    echo "  Core memory not found. Creating initial memory..."
    mkdir -p .abeone_memory
    # Memory will be created by AbëONE
fi

