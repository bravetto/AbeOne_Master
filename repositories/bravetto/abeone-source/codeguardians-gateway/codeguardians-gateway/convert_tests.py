#!/usr/bin/env python3
"""Script to convert async tests to sync TestClient tests."""
import re

file_path = "tests/integration/test_all_endpoints.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove @pytest.mark.asyncio decorators
content = re.sub(r'@pytest\.mark\.asyncio\s*\n', '', content)

# Convert async def test_* to def test_*
content = re.sub(
    r'async def (test_\w+)\(self, async_client: AsyncClient\):',
    r'def \1(self, client: TestClient):',
    content
)

# Convert await async_client. to client.
content = re.sub(r'response = await async_client\.', r'response = client.', content)
content = re.sub(r'response = await async_client\.', r'response = client.', content)

# Remove AsyncClient import and ensure TestClient is imported
if 'from httpx import AsyncClient' in content:
    content = content.replace('from httpx import AsyncClient', '')

if 'from fastapi.testclient import TestClient' not in content:
    # Add import after existing imports
    import_line = 'from fastapi.testclient import TestClient'
    # Find first import statement and add after it
    content = re.sub(
        r'(import pytest\n)',
        r'\1' + import_line + '\n',
        content
    )

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Converted {file_path}")

