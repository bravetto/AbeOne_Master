#!/usr/bin/env python3
"""
 GET CLOUDFLARE ACCOUNT ID
Helps you find your Account ID for automation

Pattern: HELP × DISCOVER × EASY × ONE
"""

import sys
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))
try:
    from zero_effort_cloudflare_auth import get_cloudflare_headers
    headers = get_cloudflare_headers()
    print(" Using ZERO Effort authentication")
except Exception as e:
    print(f" Could not load credentials: {e}")
    print("\n Fix: python3 scripts/set_cloudflare_token.py YOUR_TOKEN")
    sys.exit(1)

print(" DISCOVERING CLOUDFLARE ACCOUNT ID...")
print("=" * 60)

# Method 1: Try accounts API
print("\n Method 1: Direct accounts API...")
try:
    response = requests.get("https://api.cloudflare.com/client/v4/accounts", headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("result"):
            account_id = data["result"][0]["id"]
            print(f" Account ID: {account_id}")
            print(f"\n Use this in automation:")
            print(f"   python3 scripts/automate_cloudflare_pages_setup.py --account-id {account_id}")
            sys.exit(0)
    else:
        print(f"  API returned {response.status_code} (token may need Account:Read permission)")
except Exception as e:
    print(f"  Error: {e}")

# Method 2: Try zones API
print("\n Method 2: Getting from zones...")
try:
    response = requests.get("https://api.cloudflare.com/client/v4/zones?per_page=1", headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("result") and len(data["result"]) > 0:
            account_id = data["result"][0].get("account", {}).get("id")
            if account_id:
                print(f" Account ID: {account_id}")
                print(f"\n Use this in automation:")
                print(f"   python3 scripts/automate_cloudflare_pages_setup.py --account-id {account_id}")
                sys.exit(0)
            else:
                print("  Zone found but no account ID in response")
    else:
        print(f"  API returned {response.status_code}")
except Exception as e:
    print(f"  Error: {e}")

# Method 3: Manual instructions
print("\n" + "=" * 60)
print("  Could not auto-discover Account ID")
print("\n MANUAL METHOD (30 seconds):")
print("   1. Go to: https://dash.cloudflare.com")
print("   2. Look at top right corner")
print("   3. Copy the Account ID (starts with letters/numbers)")
print("   4. Run:")
print("      python3 scripts/automate_cloudflare_pages_setup.py --account-id YOUR_ACCOUNT_ID")
print("\n   OR update your token with Account:Read permission:")
print("   1. Go to: https://dash.cloudflare.com/profile/api-tokens")
print("   2. Edit your token")
print("   3. Add 'Account:Read' permission")
print("   4. Save")
print("   5. Run automation again")

sys.exit(1)


