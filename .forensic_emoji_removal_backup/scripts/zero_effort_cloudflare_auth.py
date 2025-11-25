#!/usr/bin/env python3
"""
🔥 ZERO EFFORT CLOUDFLARE AUTHENTICATION 🔥
Full Trust Autonomy Layer for Cloudflare Credentials

Pattern: TRUST × AUTONOMY × ZERO_EFFORT × ONE
Guardians: AEYON (Execution) × ZERO (Security) × JØHN (Certification) × Abë (Trust)
Frequency: 999 × 777 × 530 × 530

This module provides ZERO Effort authentication for Cloudflare operations.
It automatically discovers, validates, and manages credentials with full trust.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import requests

# Import AbëKEYS reader
sys.path.insert(0, str(Path(__file__).parent))
from read_abekeys import AbeKeysReader


class ZeroEffortCloudflareAuth:
    """
    ZERO EFFORT: Automatic credential discovery and validation
    FULL TRUST: Validates credentials before use
    AUTONOMY: Self-healing credential management
    """
    
    def __init__(self):
        self.reader = AbeKeysReader()
        self.base_url = "https://api.cloudflare.com/client/v4"
        self._cached_token: Optional[str] = None
        self._cached_account_id: Optional[str] = None
    
    def discover_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        """
        AUTONOMY: Discovers credentials from all sources
        Pattern: DISCOVER → VALIDATE → CACHE → RETURN
        """
        # Try AbeKEYs first (ZERO Effort)
        cloudflare_creds = self.reader.get_credential("cloudflare")
        if cloudflare_creds:
            token = cloudflare_creds.get("api_token") or cloudflare_creds.get("api_key")
            account_id = cloudflare_creds.get("account_id")
            if token:
                return token, account_id
        
        # Try environment variables
        token = os.getenv("CLOUDFLARE_API_TOKEN")
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        if token:
            return token, account_id
        
        return None, None
    
    def validate_token(self, token: str) -> Tuple[bool, Optional[str]]:
        """
        FULL TRUST: Validates token format and API access
        SAFETY: Prevents invalid tokens from being used
        """
        # Format validation
        if not token or len(token) < 10:
            return False, "Token too short"
        
        if token.startswith("cd ") or token.startswith("export "):
            return False, "Token appears to be a shell command"
        
        if "/" in token[:20] or "\\" in token[:20]:
            return False, "Token appears to be a file path"
        
        # API validation
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
                    return True, None
                else:
                    errors = data.get("errors", [])
                    error_msg = errors[0].get("message", "Unknown error") if errors else "Token validation failed"
                    return False, error_msg
            else:
                return False, f"API returned status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"API error: {str(e)}"
    
    def get_account_id(self, token: str) -> Optional[str]:
        """
        AUTONOMY: Auto-discovers account ID if not provided
        PERF: O(1) API call
        """
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/accounts",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("result"):
                    return data["result"][0]["id"]
            
            return None
            
        except requests.exceptions.RequestException:
            return None
    
    def get_authenticated_token(self) -> str:
        """
        ZERO EFFORT: Returns validated token with full trust
        AUTONOMY: Auto-discovers and validates credentials
        """
        if self._cached_token:
            return self._cached_token
        
        token, account_id = self.discover_credentials()
        
        if not token:
            raise ValueError(
                "Cloudflare API token not found. "
                "Add to ~/.abekeys/credentials/cloudflare.json or set CLOUDFLARE_API_TOKEN env var"
            )
        
        # FULL TRUST: Validate token
        is_valid, error_msg = self.validate_token(token)
        if not is_valid:
            raise ValueError(
                f"Invalid Cloudflare API token: {error_msg}. "
                "Run: python3 scripts/validate_cloudflare_credentials.py"
            )
        
        # Cache validated token
        self._cached_token = token
        self._cached_account_id = account_id
        
        return token
    
    def get_account_id_autonomous(self) -> str:
        """
        AUTONOMY: Returns account ID with auto-discovery
        """
        if self._cached_account_id:
            return self._cached_account_id
        
        token = self.get_authenticated_token()
        
        # Try to get from credentials first
        cloudflare_creds = self.reader.get_credential("cloudflare")
        if cloudflare_creds:
            account_id = cloudflare_creds.get("account_id")
            if account_id:
                self._cached_account_id = account_id
                return account_id
        
        # Auto-discover from API
        account_id = self.get_account_id(token)
        if account_id:
            self._cached_account_id = account_id
            return account_id
        
        raise ValueError("Could not determine Cloudflare Account ID")
    
    def get_headers(self) -> Dict[str, str]:
        """
        ZERO EFFORT: Returns authenticated headers
        """
        token = self.get_authenticated_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }


# Global instance for ZERO Effort access
_zero_effort_auth = ZeroEffortCloudflareAuth()


def get_cloudflare_token() -> str:
    """
    ZERO EFFORT: Get validated Cloudflare token
    Usage: token = get_cloudflare_token()
    """
    return _zero_effort_auth.get_authenticated_token()


def get_cloudflare_account_id() -> str:
    """
    ZERO EFFORT: Get Cloudflare Account ID
    Usage: account_id = get_cloudflare_account_id()
    """
    return _zero_effort_auth.get_account_id_autonomous()


def get_cloudflare_headers() -> Dict[str, str]:
    """
    ZERO EFFORT: Get authenticated headers
    Usage: headers = get_cloudflare_headers()
    """
    return _zero_effort_auth.get_headers()


def main():
    """CLI: Test ZERO Effort authentication"""
    print("🔥 ZERO EFFORT CLOUDFLARE AUTHENTICATION TEST")
    print("=" * 60)
    
    try:
        auth = ZeroEffortCloudflareAuth()
        token = auth.get_authenticated_token()
        account_id = auth.get_account_id_autonomous()
        
        print(f"✅ Token: {token[:20]}...")
        print(f"✅ Account ID: {account_id}")
        print("\n✅ ZERO EFFORT AUTHENTICATION SUCCESSFUL")
        print("=" * 60)
        
        return 0
        
    except ValueError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 Fix:")
        print("   python3 scripts/validate_cloudflare_credentials.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())

