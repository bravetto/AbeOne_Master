#!/usr/bin/env python3
"""
🔐 CLOUDFLARE CREDENTIAL VALIDATION
Validates Cloudflare API credentials and fixes invalid tokens

Pattern: VALIDATE → FIX → VERIFY → TRUST
Guardians: AEYON (Execution) × ZERO (Security) × JØHN (Certification)
"""

import sys
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any

# Import AbëKEYS reader
sys.path.insert(0, str(Path(__file__).parent))
from read_abekeys import AbeKeysReader


class CloudflareCredentialValidator:
    """
    SAFETY: Validates credential format and API access
    ASSUMES: Credentials stored in AbeKEYs vault
    VERIFY: python scripts/validate_cloudflare_credentials.py
    """
    
    def __init__(self):
        self.reader = AbeKeysReader()
        self.base_url = "https://api.cloudflare.com/client/v4"
    
    def validate_token_format(self, token: str) -> tuple[bool, str]:
        """
        SAFETY: Validates token format before API call
        """
        if not token:
            return False, "Token is empty"
        
        if len(token) < 10:
            return False, f"Token too short (length: {len(token)})"
        
        # Check for common mistakes (shell commands, paths, etc.)
        if token.startswith("cd ") or token.startswith("export "):
            return False, "Token appears to be a shell command, not an API token"
        
        if "/" in token[:20] or "\\" in token[:20]:
            return False, "Token appears to be a file path, not an API token"
        
        if " " in token.strip()[:30]:
            return False, "Token contains spaces (likely invalid)"
        
        # Cloudflare tokens are typically alphanumeric with some special chars
        if not any(c.isalnum() for c in token[:10]):
            return False, "Token doesn't appear to be a valid API token format"
        
        return True, "Format valid"
    
    def validate_token_api(self, token: str) -> tuple[bool, str]:
        """
        SAFETY: Validates token with Cloudflare API
        PERF: O(1) API call
        """
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/user/tokens/verify",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    user_info = data.get("result", {})
                    email = user_info.get("email", "Unknown")
                    return True, f"Token valid (User: {email})"
                else:
                    errors = data.get("errors", [])
                    error_msg = errors[0].get("message", "Unknown error") if errors else "Token validation failed"
                    return False, error_msg
            else:
                return False, f"API returned status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"API error: {str(e)}"
    
    def validate_credential_file(self) -> tuple[bool, Optional[str], Optional[str]]:
        """
        SAFETY: Validates credential file exists and contains valid token
        """
        cred_file = Path.home() / ".abekeys" / "credentials" / "cloudflare.json"
        
        if not cred_file.exists():
            return False, None, "Credential file not found"
        
        try:
            with open(cred_file, 'r') as f:
                cred_data = json.load(f)
            
            token = cred_data.get("api_token") or cred_data.get("api_key")
            if not token:
                return False, None, "No api_token or api_key found in credential file"
            
            return True, token, None
            
        except json.JSONDecodeError as e:
            return False, None, f"Invalid JSON in credential file: {e}"
        except IOError as e:
            return False, None, f"Error reading credential file: {e}"
    
    def fix_invalid_token(self, new_token: Optional[str] = None) -> bool:
        """
        SAFETY: Fixes invalid token in credential file
        ASSUMES: User provides valid token
        """
        cred_file = Path.home() / ".abekeys" / "credentials" / "cloudflare.json"
        cred_dir = cred_file.parent
        
        # Create directory if needed
        cred_dir.mkdir(parents=True, exist_ok=True)
        
        if not new_token:
            print("\n📝 To fix invalid token:")
            print("   1. Get token from: https://dash.cloudflare.com/profile/api-tokens")
            print("   2. Use template: 'Edit zone DNS'")
            print("   3. Select zone: bravetto.ai")
            print("   4. Copy token")
            print("\n   Then run:")
            print(f"   python3 scripts/set_cloudflare_token.sh YOUR_TOKEN")
            return False
        
        # Validate new token format
        format_valid, format_msg = self.validate_token_format(new_token)
        if not format_valid:
            print(f"❌ Invalid token format: {format_msg}")
            return False
        
        # Validate new token with API
        api_valid, api_msg = self.validate_token_api(new_token)
        if not api_valid:
            print(f"❌ Token validation failed: {api_msg}")
            return False
        
        # Save valid token
        cred_data = {
            "service": "cloudflare",
            "api_token": new_token,
            "source": "validated",
            "validated_at": str(Path(__file__).stat().st_mtime)  # Use script modification time as proxy
        }
        
        with open(cred_file, 'w') as f:
            json.dump(cred_data, f, indent=2)
        
        # Set secure permissions
        cred_file.chmod(0o600)
        cred_dir.chmod(0o700)
        
        print(f"✅ Token fixed and saved to: {cred_file}")
        return True
    
    def validate(self) -> bool:
        """
        MAIN VALIDATION FLOW
        SAFETY: Validates format and API access
        """
        print("🔐 VALIDATING CLOUDFLARE CREDENTIALS...")
        print("=" * 60)
        
        # Check credential file
        file_valid, token, error_msg = self.validate_credential_file()
        if not file_valid:
            print(f"❌ Credential file issue: {error_msg}")
            print("\n💡 Fix:")
            print("   python3 scripts/setup_cloudflare_credentials.sh")
            return False
        
        print(f"✅ Credential file found: {Path.home() / '.abekeys' / 'credentials' / 'cloudflare.json'}")
        
        # Validate token format
        format_valid, format_msg = self.validate_token_format(token)
        if not format_valid:
            print(f"❌ Invalid token format: {format_msg}")
            print(f"   Current token (first 20 chars): {token[:20]}...")
            print("\n💡 This token appears to be invalid (may be a shell command or path)")
            self.fix_invalid_token()
            return False
        
        print(f"✅ Token format valid: {format_msg}")
        
        # Validate token with API
        print("\n🔍 Validating token with Cloudflare API...")
        api_valid, api_msg = self.validate_token_api(token)
        if not api_valid:
            print(f"❌ API validation failed: {api_msg}")
            return False
        
        print(f"✅ API validation successful: {api_msg}")
        
        print("\n" + "=" * 60)
        print("✅ ALL VALIDATIONS PASSED - CREDENTIALS TRUSTED")
        print("=" * 60)
        
        return True


def main():
    """CLI Entry Point"""
    validator = CloudflareCredentialValidator()
    success = validator.validate()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

