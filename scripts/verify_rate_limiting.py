#!/usr/bin/env python3
"""
Rate Limiting Verification Script

Verifies Upstash Redis rate limiting setup and integration.

Pattern: VERIFY × RATE_LIMIT × UPSTASH × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN)
Guardians: AEYON (999 Hz) + JØHN (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
from pathlib import Path
from typing import Dict, Any

def verify_rate_limiting() -> Dict[str, Any]:
    """Verify rate limiting setup"""
    result = {
        "success": False,
        "message": "",
        "details": {}
    }
    
    # Check if we're in the web app directory
    web_dir = Path(__file__).parent.parent / "products" / "apps" / "web"
    
    if not web_dir.exists():
        result["message"] = "Web app directory not found"
        return result
    
    # Check for rate limiting implementation
    rate_limit_impl = web_dir / "lib" / "rate-limit" / "upstash.ts"
    if not rate_limit_impl.exists():
        result["message"] = "Rate limiting implementation not found"
        return result
    
    # Check for Upstash configuration in .env
    env_file = web_dir / ".env"
    upstash_configured = False
    if env_file.exists():
        env_content = env_file.read_text()
        if "UPSTASH_REDIS" in env_content:
            upstash_configured = True
    
    if not upstash_configured:
        result["message"] = "Upstash Redis not configured in .env"
        result["details"]["action"] = "Add UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN to .env"
        return result
    
    # Check if package.json has required dependencies
    package_json = web_dir / "package.json"
    if package_json.exists():
        package_content = package_json.read_text()
        if "@upstash/ratelimit" not in package_content:
            result["message"] = "@upstash/ratelimit package not installed"
            result["details"]["action"] = "cd products/apps/web && npm install @upstash/ratelimit @upstash/redis"
            return result
    
    result["success"] = True
    result["message"] = "Rate limiting setup verified. Ready to test."
    result["details"]["next_step"] = "cd products/apps/web && npm run test:rate-limit"
    
    return result


def main():
    """Main execution"""
    print("\n⚡ RATE LIMITING VERIFICATION")
    print("=" * 70)
    
    result = verify_rate_limiting()
    
    if result["success"]:
        print("✅ Rate limiting setup verified!")
        print(f"\n{result['message']}")
        if "next_step" in result["details"]:
            print(f"\nNext step: {result['details']['next_step']}")
    else:
        print("❌ Rate limiting setup incomplete")
        print(f"\n{result['message']}")
        if "action" in result["details"]:
            print(f"\nAction required: {result['details']['action']}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("Pattern: VERIFY × RATE_LIMIT × UPSTASH × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞\n")


if __name__ == "__main__":
    main()

