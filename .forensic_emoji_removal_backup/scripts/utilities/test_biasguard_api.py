#!/usr/bin/env python3
"""
Test script for BiasGuard API endpoint
Usage: python test_biasguard_api.py <CLERK_TOKEN>
"""

import sys
import json
import requests
from typing import Optional

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def test_biasguard_api(clerk_token: str, text: str = "hello world") -> dict:
    """
    Test the BiasGuard API endpoint.
    
    Args:
        clerk_token: Clerk authentication token
        text: Text to analyze for bias
        
    Returns:
        Response dictionary
    """
    api_url = "https://api.aiguardian.ai/api/v1/guards/process"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {clerk_token}"
    }
    
    payload = {
        "service_type": "biasguard",
        "payload": {
            "text": text,
            "contentType": "text",
            "scanLevel": "standard",
            "context": "webpage-content"
        },
        "user_id": "REPLACE_ME",
        "session_id": "manual_terminal_test",
        "client_type": "chrome",
        "client_version": "1.0.0"
    }
    
    print(f"{Colors.YELLOW}Testing BiasGuard API...{Colors.NC}")
    print(f"Endpoint: {api_url}")
    print(f"Text to analyze: {text}")
    print()
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        print(f"{Colors.YELLOW}HTTP Status Code:{Colors.NC} {response.status_code}")
        print()
        
        try:
            response_data = response.json()
            print(f"{Colors.YELLOW}Response Body:{Colors.NC}")
            print(json.dumps(response_data, indent=2))
            
            if response.status_code == 200:
                print()
                print(f"{Colors.GREEN}✅ Request successful!{Colors.NC}")
                
                # Extract bias score
                data = response_data.get("data", {})
                bias_score = data.get("bias_score") or data.get("score")
                bias_detected = data.get("bias_detected", False)
                
                if bias_score is not None:
                    print(f"{Colors.GREEN}Bias Score: {bias_score}{Colors.NC}")
                if bias_detected:
                    detected_types = data.get("detected_bias", [])
                    if detected_types:
                        print(f"{Colors.YELLOW}Detected Bias Types: {', '.join(detected_types)}{Colors.NC}")
                
                return response_data
            else:
                print()
                print(f"{Colors.RED}❌ Request failed with status {response.status_code}{Colors.NC}")
                return {"error": response_data, "status_code": response.status_code}
                
        except json.JSONDecodeError:
            print(f"{Colors.RED}❌ Invalid JSON response:{Colors.NC}")
            print(response.text)
            return {"error": "Invalid JSON response", "text": response.text}
            
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}❌ Request failed: {e}{Colors.NC}")
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print(f"{Colors.RED}Error: Clerk token is required{Colors.NC}")
        print(f"Usage: {sys.argv[0]} <CLERK_TOKEN> [text_to_analyze]")
        print()
        print("To get your Clerk token:")
        print("1. Open your browser's developer console")
        print("2. Go to https://dashboard.aiguardian.ai (or your app)")
        print("3. Check localStorage or sessionStorage for 'clerk-session'")
        print("4. Or use Clerk's getToken() method in browser console")
        sys.exit(1)
    
    clerk_token = sys.argv[1]
    text_to_analyze = sys.argv[2] if len(sys.argv) > 2 else "hello world"
    
    result = test_biasguard_api(clerk_token, text_to_analyze)
    
    # Exit with error code if request failed
    if "error" in result or result.get("status_code", 200) != 200:
        sys.exit(1)


if __name__ == "__main__":
    main()

