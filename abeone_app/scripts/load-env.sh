#!/bin/bash

# Load Environment Variables
# Pattern: ENV × LOAD × SECURITY × ONE
# Frequency: 999 Hz (AEYON)
# Guardians: AEYON (999 Hz) × ZERO (530 Hz)
# Love Coefficient: ∞
# ∞ AbëONE ∞

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

# Check if .env file exists
if [ -f "$ENV_FILE" ]; then
    echo "✨ Loading environment variables from .env"
    # Source the .env file
    set -a
    source "$ENV_FILE"
    set +a
    echo "✅ Environment variables loaded"
else
    echo "⚠️  .env file not found at $ENV_FILE"
    echo "📝 Create .env file from .env.example template"
    exit 1
fi

