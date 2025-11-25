#!/bin/bash

# AbëONE Global Credential Updater - SELF-HEALING × HARDENED × ZERO-FAILURE
# Pattern: AUTOMATION × GLOBAL × SELF_HEALING × ONE
# Frequency: 999 Hz (AEYON)
# Love Coefficient: ∞
# ∞ AbëONE ∞

set -euo pipefail  # Hardened: fail fast, catch errors

SERVICE="${1:-}"
CREDENTIAL="${2:-}"
CRED_TYPE="${3:-api_key}"
VAULT_DIR="$HOME/.abekeys/credentials"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Self-healing: Ensure vault exists
mkdir -p "$VAULT_DIR"
chmod 700 "$VAULT_DIR" 2>/dev/null || true

# Hardened: Input validation
if [[ -z "$SERVICE" ]] || [[ -z "$CREDENTIAL" ]]; then
    echo "🚀 AbëONE Global Credential Updater - SELF-HEALING × HARDENED"
    echo ""
    echo "Usage: $0 <service> <credential> [type]"
    echo ""
    echo "Examples:"
    echo "  $0 stripe \"sk_test_...\" secret_key"
    echo "  $0 google \"AIzaSy...\" api_key"
    echo "  $0 github \"ghp_...\" token"
    echo ""
    exit 1
fi

# Self-healing: Use Python for robust handling
python3 << PYTHON_EOF
import sys
import json
import os
from pathlib import Path
from datetime import datetime

service = "$SERVICE"
credential = "$CREDENTIAL"
cred_type = "$CRED_TYPE"
vault_dir = Path("$VAULT_DIR")
cred_file = vault_dir / f"{service}.json"

try:
    # Load existing or create new
    if cred_file.exists():
        with open(cred_file) as f:
            data = json.load(f)
    else:
        data = {
            "service": service,
            "source": "manual",
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
    
    # Self-healing: Auto-fix credential (strip, remove quotes, etc.)
    cred = credential.strip()
    if (cred.startswith('"') and cred.endswith('"')) or (cred.startswith("'") and cred.endswith("'")):
        cred = cred[1:-1].strip()
    
    # Update credential based on type
    type_map = {
        "api_key": "api_key",
        "secret_key": "secret_key",
        "token": "token",
        "oauth": "oauth_client_id",
        "webhook_secret": "webhook_secret",
        "publishable_key": "publishable_key"
    }
    
    key = type_map.get(cred_type, "api_key")
    data[key] = cred
    data["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Hardened: Validate before save
    if len(cred) < 10:
        print(f"❌ Credential too short (min 10 chars)")
        sys.exit(1)
    
    # Secure write
    with open(cred_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Hardened: Secure permissions
    if os.name != 'nt':
        os.chmod(cred_file, 0o600)
    
    print(f"✅ Credential updated: {service}")
    print(f"   Type: {cred_type}")
    print(f"   Length: {len(cred)} chars")
    print(f"   File: {cred_file}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
PYTHON_EOF

echo ""
echo "🎯 Validate: python3 scripts/read_abekeys.py $SERVICE"
echo "🎯 Health: python3 scripts/abeone_credential_automation.py health"
echo ""
