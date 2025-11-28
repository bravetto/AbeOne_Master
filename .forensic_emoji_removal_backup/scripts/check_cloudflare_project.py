#!/usr/bin/env python3
"""
🔍 CHECK CLOUDFLARE PAGES PROJECT STATUS
Quick verification script to check if project exists and is accessible
"""

import sys
import requests
from pathlib import Path

# Import AbeKEYs reader
sys.path.insert(0, str(Path(__file__).parent))
try:
    from read_abekeys import AbeKeysReader
    ABEKEYS_AVAILABLE = True
except ImportError:
    ABEKEYS_AVAILABLE = False


def check_project_status(project_name: str = "abeone-web") -> dict:
    """
    SAFETY: Checks if Cloudflare Pages project exists and is accessible
    VERIFY: python scripts/check_cloudflare_project.py
    """
    results = {
        'project_name': project_name,
        'pages_url': f'https://{project_name}.pages.dev',
        'exists': False,
        'accessible': False,
        'status_code': None,
        'error': None
    }
    
    print(f"🔍 CHECKING CLOUDFLARE PAGES PROJECT: {project_name}")
    print("=" * 60)
    
    # Check 1: Try to access the pages.dev URL
    print(f"\n📋 Check 1: Testing {results['pages_url']}...")
    try:
        response = requests.get(results['pages_url'], timeout=10, allow_redirects=True)
        results['status_code'] = response.status_code
        results['accessible'] = response.status_code < 500
        
        if response.status_code == 200:
            print(f"✅ Project is LIVE and accessible!")
            print(f"   Status: {response.status_code}")
            results['exists'] = True
        elif response.status_code == 404:
            print(f"⚠️  Project URL returns 404 (not found)")
            print(f"   Project may not exist yet or not deployed")
        elif response.status_code in [403, 401]:
            print(f"⚠️  Project URL returns {response.status_code} (access denied)")
            print(f"   Project may exist but is private or not configured")
        else:
            print(f"⚠️  Project URL returns {response.status_code}")
            print(f"   Project may exist but has issues")
            results['exists'] = True  # Assume exists if not 404
    except requests.exceptions.RequestException as e:
        results['error'] = str(e)
        print(f"❌ Error accessing project URL: {e}")
    
    # Check 2: Try API check (if credentials available)
    if ABEKEYS_AVAILABLE:
        print(f"\n📋 Check 2: Checking via Cloudflare API...")
        try:
            reader = AbeKeysReader()
            creds = reader.get_credential("cloudflare")
            if creds:
                import os
                token = creds.get("api_token") or creds.get("api_key")
                if token:
                    print("   ✅ Credentials found")
                    print("   ⚠️  Need Account ID to check via API")
                    print("   💡 Get Account ID from: https://dash.cloudflare.com")
                    print("      (Look in top right corner)")
        except Exception as e:
            print(f"   ⚠️  Could not check via API: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if results['exists'] and results['accessible']:
        print(f"✅ Project '{project_name}' EXISTS and is ACCESSIBLE")
        print(f"🌐 URL: {results['pages_url']}")
        return results
    elif results['exists']:
        print(f"⚠️  Project '{project_name}' may EXIST but has issues")
        print(f"🌐 URL: {results['pages_url']} (Status: {results['status_code']})")
    else:
        print(f"❌ Project '{project_name}' does NOT appear to exist yet")
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Check Cloudflare dashboard: https://dash.cloudflare.com/?to=/:account/pages")
        print(f"   2. If project doesn't exist, create it manually:")
        print(f"      - Go to: https://dash.cloudflare.com/?to=/:account/pages/new")
        print(f"      - Connect GitHub repository: AbeOne_Master")
        print(f"      - Build command: cd apps/web && npm install && npm run build")
        print(f"      - Output directory: apps/web/out")
        print(f"   3. Or try API automation with Account ID:")
        print(f"      python3 scripts/automate_cloudflare_pages_setup.py --account-id YOUR_ACCOUNT_ID")
    
    return results


if __name__ == "__main__":
    project_name = sys.argv[1] if len(sys.argv) > 1 else "abeone-web"
    check_project_status(project_name)

