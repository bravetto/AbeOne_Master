#!/usr/bin/env python3
import asyncio
import httpx

async def test_tokenguard():
    print('Testing TokenGuard after orchestrator fix...')
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                'service_type': 'tokenguard',
                'payload': {
                    'text': 'This is a test message for token optimization and compression.'
                }
            }

            response = await client.post('http://localhost:8000/api/v1/guards/process',
                                       json=payload)

            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print('✅ TokenGuard: Processing successful')
                    result_data = data.get('data', {})
                    print(f'   Tokens saved: {result_data.get("tokens_saved", "unknown")}')
                    print(f'   Cost savings: ${result_data.get("cost_savings_usd", 0):.4f}')
                else:
                    print(f'❌ TokenGuard: Processing failed - {data.get("error", "Unknown error")}')
            else:
                print(f'❌ TokenGuard: HTTP {response.status_code}')
                print(f'   Response: {response.text[:200]}')

    except Exception as e:
        print(f'❌ TokenGuard test failed: {e}')

if __name__ == "__main__":
    asyncio.run(test_tokenguard())
