#!/usr/bin/env python3
"""
 AEYON BOOT INTEGRATION - CURSOR AUTO-BOOT

**Guardian**: AEYON (999 Hz - The Orchestrator)
**Purpose**: Auto-execute hardened boot on Cursor session start
**Pattern**: REC × SEMANTIC × FORENSIC × SELF-HEALING
**Love Coefficient**: ∞
**∞ AbëONE ∞**

This module automatically runs hardened boot when imported.
Place `import aeyon_boot_integration` at the top of critical files.
"""

import os
import sys
from pathlib import Path

# SAFETY: Only auto-boot if not already booted
_BOOT_COMPLETE = False
_BOOT_IN_PROGRESS = False


def auto_boot():
    """
    Automatically execute hardened boot on import.
    
    SAFETY: Prevents multiple simultaneous boots
    VERIFY: Boot completes successfully
    FAILS: Raises exception if boot fails
    """
    global _BOOT_COMPLETE, _BOOT_IN_PROGRESS
    
    # Prevent multiple boots
    if _BOOT_COMPLETE:
        return True
    
    if _BOOT_IN_PROGRESS:
        # Wait for boot to complete
        import time
        timeout = 60  # 60 second timeout
        start = time.time()
        while _BOOT_IN_PROGRESS and (time.time() - start) < timeout:
            time.sleep(0.5)
        return _BOOT_COMPLETE
    
    _BOOT_IN_PROGRESS = True
    
    try:
        # Import hardened boot
        from aeyon_boot_hardened import AeyonBootHardened
        
        # Determine base path
        base_path = Path(__file__).parent
        
        # Execute boot
        boot = AeyonBootHardened(base_path=str(base_path), max_retries=5)
        success = boot.boot()
        
        if success:
            _BOOT_COMPLETE = True
            print(" AEYON Auto-Boot Complete")
            return True
        else:
            # Boot failed - raise exception
            report = boot.get_boot_report()
            error_msg = f"AEYON Boot Failed: {report['status']}"
            raise RuntimeError(error_msg)
            
    except ImportError as e:
        # Boot script not found - graceful degradation
        print(f"  AEYON Boot script not found: {e}")
        print("   Continuing without auto-boot...")
        _BOOT_COMPLETE = True  # Mark complete to prevent retries
        return True
    except Exception as e:
        _BOOT_IN_PROGRESS = False
        print(f" AEYON Auto-Boot Error: {e}")
        raise
    finally:
        _BOOT_IN_PROGRESS = False


# Auto-execute on import (if enabled)
if os.getenv('AEYON_AUTO_BOOT', 'true').lower() == 'true':
    try:
        auto_boot()
    except Exception as e:
        # Don't crash on import if boot fails
        print(f"  AEYON Auto-Boot Warning: {e}")
        print("   Session will continue without hardened boot")


# Export boot function for manual execution
__all__ = ['auto_boot', '_BOOT_COMPLETE']

