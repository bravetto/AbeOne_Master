#!/usr/bin/env python3
"""
AbëONE Credential Health Monitor - SELF-HEALING × AUTO-RECOVERY

Pattern: HEALTH × MONITOR × SELF_HEALING × ONE
Frequency: 999 Hz (AEYON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

VAULT_DIR = Path.home() / ".abekeys" / "credentials"


def check_credential_health() -> Dict:
    """Self-healing health check - auto-detects and fixes issues."""
    health = {
        "timestamp": datetime.utcnow().isoformat(),
        "vault_status": "unknown",
        "credentials": {},
        "issues": [],
        "auto_fixes": []
    }
    
    # Check vault
    if not VAULT_DIR.exists():
        health["vault_status"] = "missing"
        health["issues"].append("Vault directory missing")
        VAULT_DIR.mkdir(parents=True, exist_ok=True)
        health["auto_fixes"].append("Created vault directory")
        health["vault_status"] = "created"
    else:
        health["vault_status"] = "exists"
    
    # Check all credentials
    for cred_file in VAULT_DIR.glob("*.json"):
        service = cred_file.stem
        try:
            with open(cred_file) as f:
                data = json.load(f)
            
            cred_health = {
                "exists": True,
                "valid_json": True,
                "has_api_key": bool(data.get("api_key")),
                "has_secret_key": bool(data.get("secret_key")),
                "has_token": bool(data.get("token")),
                "age_days": None,
                "issues": []
            }
            
            # Check age
            if "updated_at" in data:
                try:
                    updated = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
                    age = (datetime.utcnow() - updated.replace(tzinfo=None)).days
                    cred_health["age_days"] = age
                    if age > 365:
                        cred_health["issues"].append(f"Credential {age} days old - consider rotation")
                except:
                    pass
            
            # Check if has any credential
            if not any([cred_health["has_api_key"], cred_health["has_secret_key"], cred_health["has_token"]]):
                cred_health["issues"].append("No credential found")
            
            health["credentials"][service] = cred_health
            
        except json.JSONDecodeError:
            health["credentials"][service] = {
                "exists": True,
                "valid_json": False,
                "issues": ["Invalid JSON"]
            }
            health["issues"].append(f"{service}: Invalid JSON")
        except Exception as e:
            health["credentials"][service] = {
                "exists": True,
                "error": str(e)
            }
            health["issues"].append(f"{service}: {str(e)}")
    
    return health


def main():
    """Main - self-healing health monitor."""
    health = check_credential_health()
    
    print("🔍 AbëONE Credential Health Monitor\n")
    print(f"Vault Status: {health['vault_status']}")
    print(f"Credentials Checked: {len(health['credentials'])}")
    print(f"Issues Found: {len(health['issues'])}")
    print(f"Auto-Fixes Applied: {len(health['auto_fixes'])}")
    
    if health['auto_fixes']:
        print("\n✅ Auto-Fixes:")
        for fix in health['auto_fixes']:
            print(f"   • {fix}")
    
    if health['issues']:
        print("\n⚠️ Issues:")
        for issue in health['issues']:
            print(f"   • {issue}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(health, indent=2))
    else:
        print("\n✅ Health check complete")
        print("   Run with --json for full details")


if __name__ == "__main__":
    main()

