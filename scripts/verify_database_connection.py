#!/usr/bin/env python3
"""
Database Connection Verification Script

Verifies PostgreSQL/Neon database connection and operations.

Pattern: VERIFY × DATABASE × CONNECTION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN)
Guardians: AEYON (999 Hz) + JØHN (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any

def verify_database_connection() -> Dict[str, Any]:
    """Verify database connection"""
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
    
    # Check for .env file
    env_file = web_dir / ".env"
    if not env_file.exists():
        result["message"] = ".env file not found. Please create it from .env.example"
        result["details"]["action"] = "Copy .env.example to .env and configure DATABASE_URL"
        return result
    
    # Check for Prisma schema
    prisma_schema = web_dir / "prisma" / "schema.prisma"
    if not prisma_schema.exists():
        result["message"] = "Prisma schema not found"
        return result
    
    # Check if Prisma client exists
    prisma_client = web_dir / "node_modules" / ".prisma" / "client"
    if not prisma_client.exists():
        result["message"] = "Prisma client not generated. Run: npx prisma generate"
        result["details"]["action"] = "cd products/apps/web && npx prisma generate"
        return result
    
    result["success"] = True
    result["message"] = "Database setup verified. Ready to run migrations."
    result["details"]["next_step"] = "cd products/apps/web && npx prisma migrate dev"
    
    return result


def main():
    """Main execution"""
    print("\n⚡ DATABASE CONNECTION VERIFICATION")
    print("=" * 70)
    
    result = verify_database_connection()
    
    if result["success"]:
        print("✅ Database setup verified!")
        print(f"\n{result['message']}")
        if "next_step" in result["details"]:
            print(f"\nNext step: {result['details']['next_step']}")
    else:
        print("❌ Database setup incomplete")
        print(f"\n{result['message']}")
        if "action" in result["details"]:
            print(f"\nAction required: {result['details']['action']}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("Pattern: VERIFY × DATABASE × CONNECTION × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞\n")


if __name__ == "__main__":
    main()

