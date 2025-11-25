#!/usr/bin/env python3
"""
🔐 SET CLOUDFLARE TOKEN (Python Version)
Usage: python3 scripts/set_cloudflare_token.py YOUR_TOKEN

Pattern: ZERO_EFFORT × PYTHON × TRUST × ONE
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python3 scripts/set_cloudflare_token.py <cloudflare_api_token>")
        print("")
        print("Example:")
        print("  python3 scripts/set_cloudflare_token.py abc123def456...")
        print("")
        print("Or set as environment variable:")
        print("  export CLOUDFLARE_API_TOKEN='your-token'")
        print("  python3 scripts/set_cloudflare_token.py $CLOUDFLARE_API_TOKEN")
        sys.exit(1)
    
    api_token = sys.argv[1]
    
    if not api_token or len(api_token) < 10:
        print("❌ API Token appears to be invalid (too short)")
        sys.exit(1)
    
    # Setup paths
    abekeys_dir = Path.home() / ".abekeys" / "credentials"
    cred_file = abekeys_dir / "cloudflare.json"
    
    # Create directory if needed
    abekeys_dir.mkdir(parents=True, exist_ok=True)
    
    # Create credential file
    cred_data = {
        "service": "cloudflare",
        "api_token": api_token,
        "source": "manual",
        "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    with open(cred_file, 'w') as f:
        json.dump(cred_data, f, indent=2)
    
    # Set secure permissions
    cred_file.chmod(0o600)
    abekeys_dir.chmod(0o700)
    
    print("✅ Credentials saved to:", cred_file)
    print("✅ Permissions set to 600 (owner read/write only)")
    print("")
    
    # Test authentication
    print("🧪 Testing authentication...")
    print("=" * 60)
    
    # Import validation script
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from validate_cloudflare_credentials import CloudflareCredentialValidator
        validator = CloudflareCredentialValidator()
        if validator.validate():
            print("")
            print("✅ Authentication successful!")
            print("")
            print("You can now use:")
            print("  python3 scripts/cloudflare_pages_auto_bind.py \\")
            print("    --domain bravetto.ai \\")
            print("    --project-name abeone-web")
        else:
            print("")
            print("⚠️  Authentication test failed")
            print("   Please verify:")
            print("   1. Token is correct")
            print("   2. Token has 'Edit zone DNS' permissions")
            print("   3. Token is for bravetto.ai zone")
            sys.exit(1)
    except ImportError:
        print("⚠️  Could not import validation script")
        print("   Token saved, but validation skipped")
        print("   Run: python3 scripts/validate_cloudflare_credentials.py")
    
    print("")

if __name__ == "__main__":
    main()

