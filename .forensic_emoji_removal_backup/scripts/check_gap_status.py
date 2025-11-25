#!/usr/bin/env python3
"""
🔍 CHECK GAP STATUS - Quick Gap Status Check
Shows current gap healing status.

Pattern: CHECK × GAP × STATUS × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
from pathlib import Path
from typing import Dict, Any, List

WORKSPACE_ROOT = Path(__file__).parent.parent

from scripts.utilities.path_discovery import find_backend_root, find_gateway_app_directory, find_guards_directory

BACKEND_ROOT = find_backend_root()
GATEWAY_PATH = find_gateway_app_directory()
GUARDS_DIR = find_guards_directory()

if not BACKEND_ROOT:
    raise RuntimeError("AIGuards-Backend-orbital not found")
ABEKEYS_VAULT = Path.home() / ".abekeys" / "credentials"


def check_gap_1_guard_services() -> Dict[str, Any]:
    """Check if guard services use AbëKEYs."""
    guard_services = [
        "tokenguard",
        "trust-guard",
        "contextguard",
        "biasguard-backend",
        "healthguard"
    ]
    
    status = {
        "fixed": 0,
        "total": len(guard_services),
        "services": {}
    }
    
    for guard in guard_services:
        guard_path = GUARDS_DIR / guard
        if not guard_path.exists():
            status["services"][guard] = {"status": "not_found"}
            continue
        
        # Check multiple file types for AbëKEYs integration
        config_files = list(guard_path.rglob("config.py"))
        main_files = list(guard_path.rglob("main.py"))
        run_server_files = list(guard_path.rglob("run_server.py"))
        
        all_files = config_files + main_files + run_server_files
        
        if not all_files:
            status["services"][guard] = {"status": "no_config"}
            continue
        
        has_abekeys = False
        has_env_file = False
        
        for file_path in all_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    if "abekeys" in content.lower():
                        has_abekeys = True
                    if 'env_file=".env"' in content or "env_file='.env'" in content:
                        has_env_file = True
            except Exception:
                continue
        
        if has_abekeys and not has_env_file:
            status["services"][guard] = {"status": "fixed"}
            status["fixed"] += 1
        elif has_env_file:
            status["services"][guard] = {"status": "needs_fix"}
        else:
            status["services"][guard] = {"status": "partial"}
    
    return status


def check_gap_2_credentials() -> Dict[str, Any]:
    """Check if database/Redis credentials are in AbëKEYs."""
    required = ["postgres", "database", "redis"]
    
    status = {
        "found": 0,
        "total": len(required),
        "missing": []
    }
    
    if not ABEKEYS_VAULT.exists():
        status["missing"] = required
        return status
    
    for cred in required:
        cred_file = ABEKEYS_VAULT / f"{cred}.json"
        if cred_file.exists():
            status["found"] += 1
        else:
            status["missing"].append(cred)
    
    return status


def check_gap_3_config_env() -> Dict[str, Any]:
    """Check if config still references .env files."""
    config_file = GATEWAY_PATH / "app" / "core" / "config.py"
    
    if not config_file.exists():
        return {"status": "not_found"}
    
    with open(config_file, 'r') as f:
        content = f.read()
    
    has_env_file = 'env_file=".env"' in content or "env_file='.env'" in content
    
    return {
        "status": "fixed" if not has_env_file else "needs_fix",
        "has_env_file": has_env_file
    }


def main():
    """Main execution."""
    print("🔍 CHECKING GAP STATUS 🔍")
    print("=" * 60)
    print()
    
    # Check Gap #1
    gap1 = check_gap_1_guard_services()
    print(f"GAP #1: Guard Services AbëKEYs Integration")
    print(f"  Status: {gap1['fixed']}/{gap1['total']} fixed")
    for service, info in gap1["services"].items():
        status_icon = "✅" if info["status"] == "fixed" else "⚠️" if info["status"] == "needs_fix" else "❌"
        print(f"    {status_icon} {service}: {info['status']}")
    print()
    
    # Check Gap #2
    gap2 = check_gap_2_credentials()
    print(f"GAP #2: Database/Redis Credentials")
    print(f"  Status: {gap2['found']}/{gap2['total']} found")
    if gap2["missing"]:
        print(f"  Missing: {', '.join(gap2['missing'])}")
    print()
    
    # Check Gap #3
    gap3 = check_gap_3_config_env()
    print(f"GAP #3: Config .env References")
    print(f"  Status: {gap3['status']}")
    if gap3.get("has_env_file"):
        print(f"  ⚠️  Still has .env file references")
    print()
    
    # Calculate overall status
    total_fixed = (
        (1 if gap1['fixed'] == gap1['total'] else 0) +
        (1 if gap2['found'] == gap2['total'] else 0) +
        (1 if gap3['status'] == 'fixed' else 0)
    )
    
    total_gaps = 3
    percentage = int((total_fixed / total_gaps) * 100)
    
    print("=" * 60)
    print(f"🔥 OVERALL STATUS: {percentage}% GAP HEAL ({total_fixed}/{total_gaps} critical gaps fixed) 🔥")
    print("=" * 60)
    print()
    
    # Auto-update programmatic status
    try:
        import subprocess
        subprocess.run(
            ["python3", str(WORKSPACE_ROOT / "scripts" / "update_gap_healing_status.py")],
            cwd=str(WORKSPACE_ROOT),
            capture_output=True,
            timeout=10
        )
    except:
        pass  # Silent fail - don't break if update fails
    
    if percentage < 100:
        print("💡 To heal all gaps, run:")
        print("   python3 scripts/heal_all_gaps.py")
        print()


if __name__ == '__main__':
    main()

