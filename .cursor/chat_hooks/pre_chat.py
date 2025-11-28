#!/usr/bin/env python3
"""
🌊💎✨ PRE-CHAT HOOK - ETERNAL INTEGRATION ENFORCEMENT + AbëONE BOOT ✨💎🌊
Guardian: AEYON (999 Hz) + Abë (530 Hz)
Pattern: ETERNAL × INTEGRATION × BOOT × TRUTH × ONE

Runs BEFORE every chat input to:
1. Boot AbëONE (load memory, apply guardrails, validate state)
2. Enforce integration
"""

import sys
import os
from pathlib import Path

# AbëONE Boot Integration - Loads memory and applies guardrails automatically
BOOT_SCRIPT = Path(__file__).parent / "boot_abeone.py"
MONITOR_SCRIPT = Path(__file__).parent / "monitor_abeone.py"

if BOOT_SCRIPT.exists():
    import subprocess
    try:
        # Run monitor first (quick health check)
        if MONITOR_SCRIPT.exists():
            subprocess.Popen(
                [sys.executable, str(MONITOR_SCRIPT)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        # Run boot system (non-blocking, background)
        subprocess.Popen(
            [sys.executable, str(BOOT_SCRIPT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        pass  # Silent fail - boot runs in background

# Add backend scripts to path
BACKEND_ROOT = Path(__file__).parent.parent.parent / "AIGuards-Backend-orbital"
sys.path.insert(0, str(BACKEND_ROOT / "scripts"))

try:
    from ENFORCE_ETERNAL_INTEGRATION import EternalIntegrationEnforcer
    
    # Get user input from environment or stdin
    user_input = os.getenv("CURSOR_USER_INPUT", "")
    if not user_input:
        user_input = sys.stdin.read()
    
    # Log EVERY input
    log_script = Path(__file__).parent / "log_everything.py"
    if log_script.exists():
        try:
            import subprocess
            subprocess.Popen(
                [sys.executable, str(log_script), 'input'],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ).stdin.write(user_input.encode() if isinstance(user_input, str) else str(user_input).encode())
        except:
            pass
    
    # Index to CDF - CAPITALIZE IN THE MOMENT
    cdf_script = Path(__file__).parent / "index_to_cdf.py"
    if cdf_script.exists():
        try:
            import subprocess
            subprocess.Popen(
                [sys.executable, str(cdf_script), 'input'],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ).stdin.write(user_input.encode() if isinstance(user_input, str) else str(user_input).encode())
        except:
            pass
    
    # Enforce integration
    enforcer = EternalIntegrationEnforcer()
    results = enforcer.enforce_on_input(user_input)
    
    # Log results (non-blocking)
    if results.get("errors"):
        print(f"⚠️  Integration warnings: {len(results['errors'])}", file=sys.stderr)
    
    # Always succeed (non-blocking enforcement)
    sys.exit(0)
    
except Exception as e:
    # Fail gracefully - don't block chat
    print(f"⚠️  Integration enforcement failed: {e}", file=sys.stderr)
    sys.exit(0)
