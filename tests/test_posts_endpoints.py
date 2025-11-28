#!/usr/bin/env python3
"""
Simple test script to check posts endpoints.
"""

import asyncio
import httpx
import json

async def test_posts_endpoints():
    """Test the posts endpoints."""
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        try:
            # Test GET /api/v1/posts/
            print("Testing GET /api/v1/posts/")
            response = await client.get(f"{base_url}/api/v1/posts/")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            else:
                print(f"Error: {response.text}")

            # Test GET /api/v1/posts/1 (assuming post ID 1 exists)
            print("\nTesting GET /api/v1/posts/1")
            response = await client.get(f"{base_url}/api/v1/posts/1")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            else:
                print(f"Error: {response.text}")

        except Exception as e:
            print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_posts_endpoints())
