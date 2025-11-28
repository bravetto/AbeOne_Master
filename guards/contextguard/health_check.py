#!/usr/bin/env python3
"""
Health check script for ContextGuard service
"""

import asyncio
import httpx
import sys
import os

async def check_health():
    """Check if the service is healthy"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    return True
    except Exception:
        pass
    return False

if __name__ == "__main__":
    result = asyncio.run(check_health())
    sys.exit(0 if result else 1)
