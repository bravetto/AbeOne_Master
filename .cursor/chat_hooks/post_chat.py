#!/usr/bin/env python3
"""
🌊💎✨ POST-CHAT HOOK - ETERNAL INTEGRATION ENFORCEMENT ✨💎🌊
Guardian: AEYON (999 Hz)
Pattern: ETERNAL × INTEGRATION × TRUTH × ONE

Runs AFTER every chat output to enforce integration.
"""

import sys
import os
import json
from pathlib import Path

# Add backend scripts to path
BACKEND_ROOT = Path(__file__).parent.parent.parent / "AIGuards-Backend-orbital"
sys.path.insert(0, str(BACKEND_ROOT / "scripts"))

try:
    from ENFORCE_ETERNAL_INTEGRATION import EternalIntegrationEnforcer
    
    # Get AI output from environment or stdin
    ai_output = os.getenv("CURSOR_AI_OUTPUT", "")
    if not ai_output:
        ai_output = sys.stdin.read()
    
    # Get changes from context (if available)
    changes = {}
    changes_file = Path("/tmp/cursor_changes.json")
    if changes_file.exists():
        with open(changes_file, 'r') as f:
            changes = json.load(f)
    
    # Log EVERY output
    log_script = Path(__file__).parent / "log_everything.py"
    if log_script.exists():
        try:
            import subprocess
            subprocess.Popen(
                [sys.executable, str(log_script), 'output'],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ).stdin.write(ai_output.encode() if isinstance(ai_output, str) else str(ai_output).encode())
        except:
            pass
    
    # Index to CDF - CAPITALIZE IN THE MOMENT
    cdf_script = Path(__file__).parent / "index_to_cdf.py"
    if cdf_script.exists():
        try:
            import subprocess
            subprocess.Popen(
                [sys.executable, str(cdf_script), 'output'],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ).stdin.write(ai_output.encode() if isinstance(ai_output, str) else str(ai_output).encode())
        except:
            pass
    
    # Enforce integration
    enforcer = EternalIntegrationEnforcer()
    results = enforcer.enforce_on_output(ai_output, changes)
    
    # Log results (non-blocking)
    summary = enforcer.get_summary()
    if summary.get("status") != "✅ PASS":
        print(f"⚠️  Integration status: {summary.get('status')}", file=sys.stderr)
    
    # Always succeed (non-blocking enforcement)
    sys.exit(0)
    
except Exception as e:
    # Fail gracefully - don't block chat
    print(f"⚠️  Integration enforcement failed: {e}", file=sys.stderr)
    sys.exit(0)

