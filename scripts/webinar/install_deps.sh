#!/bin/bash
# Install webinar system dependencies
# Pattern: INSTALL × DEPENDENCIES × SEAMLESS × ONE

echo " Installing webinar system dependencies..."

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "  Virtual environment not activated"
    echo "   Activating: source .venv/bin/activate"
    source .venv/bin/activate 2>/dev/null || {
        echo " Cannot activate virtual environment"
        echo "   Create it: python3 -m venv .venv"
        exit 1
    }
fi

echo " Installing Python packages..."
pip install -r "$(dirname "$0")/requirements.txt"

echo " Dependencies installed!"
echo ""
echo "Quick test:"
echo "  python3 scripts/webinar/master_orchestrator.py --help"

