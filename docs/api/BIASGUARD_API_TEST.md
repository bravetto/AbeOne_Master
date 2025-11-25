# BiasGuard API Test Guide

## Quick Test with curl

Your curl command is correctly formatted. Replace `<YOUR_CLERK_TOKEN>` with your actual Clerk token:

```bash
curl -X POST "https://api.aiguardian.ai/api/v1/guards/process" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_CLERK_TOKEN>" \
  -d '{
    "service_type": "biasguard",
    "payload": {
        "text": "hello world",
        "contentType": "text",
        "scanLevel": "standard",
        "context": "webpage-content"
    },
    "user_id": "REPLACE_ME",
    "session_id": "manual_terminal_test",
    "client_type": "chrome",
    "client_version": "1.0.0"
  }'
```

## Using the Test Scripts

### Bash Script
```bash
./test_biasguard_api.sh <YOUR_CLERK_TOKEN>
```

### Python Script
```bash
python test_biasguard_api.py <YOUR_CLERK_TOKEN> [optional_text_to_analyze]
```

Example with custom text:
```bash
python test_biasguard_api.py <YOUR_CLERK_TOKEN> "This job requires a strong leader who can take charge"
```

## Getting Your Clerk Token

### Method 1: Browser Console
1. Open your browser's developer console (F12)
2. Navigate to your app (e.g., https://dashboard.aiguardian.ai)
3. Run this in the console:
```javascript
// If using Clerk SDK
import { clerk } from './path/to/clerk';
clerk.session.getToken().then(token => console.log(token));

// Or check localStorage
localStorage.getItem('clerk-session-token');
```

### Method 2: Chrome Extension
If you're testing from the Chrome extension, the token should be available in the extension's storage.

### Method 3: API Key (Alternative)
Some endpoints may accept API keys instead of Clerk tokens. Check your API documentation.

## Expected Response Format

```json
{
  "request_id": "uuid-here",
  "service_type": "biasguard",
  "success": true,
  "data": {
    "bias_score": 0.0,
    "bias_detected": false,
    "detected_bias": [],
    "confidence": 0.8
  },
  "processing_time": 15.2,
  "service_used": "integrated_biasguard"
}
```

## Request Structure

The `/api/v1/guards/process` endpoint expects:

- **service_type** (required): `"biasguard"`
- **payload** (required): Object containing:
  - **text** (required): Text to analyze
  - **contentType** (optional): Type of content
  - **scanLevel** (optional): `"standard"` | `"deep"` | `"quick"`
  - **context** (optional): Context description
- **user_id** (optional): User identifier
- **session_id** (optional): Session identifier
- **client_type** (optional): `"chrome"` | `"web"` | `"vscode"` | `"api"`
- **client_version** (optional): Client version string

## Testing Different Bias Scenarios

### Test 1: Neutral Text (should have low bias score)
```bash
curl -X POST "https://api.aiguardian.ai/api/v1/guards/process" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "service_type": "biasguard",
    "payload": {"text": "The weather is nice today"},
    "user_id": "test_user",
    "session_id": "test_session"
  }'
```

### Test 2: Potentially Biased Text
```bash
curl -X POST "https://api.aiguardian.ai/api/v1/guards/process" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "service_type": "biasguard",
    "payload": {"text": "Men are better at leadership roles than women"},
    "user_id": "test_user",
    "session_id": "test_session"
  }'
```

## Troubleshooting

### 401 Unauthorized
- Check that your Clerk token is valid and not expired
- Ensure the token is prefixed with `Bearer ` in the Authorization header

### 400 Bad Request
- Verify the payload structure matches the expected format
- Check that `service_type` is exactly `"biasguard"` (lowercase)
- Ensure `payload.text` is present and is a string

### 500 Internal Server Error
- Check API server status
- Verify the endpoint is available at `https://api.aiguardian.ai`

## API Endpoint Details

- **Base URL**: `https://api.aiguardian.ai`
- **Endpoint**: `/api/v1/guards/process`
- **Method**: `POST`
- **Authentication**: Bearer token (Clerk JWT)
- **Content-Type**: `application/json`

## Related Endpoints

- `/api/v1/guards/biasguard/process` - Direct BiasGuard endpoint
- `/api/v1/guards/biasguard/detect` - Alias for /process
- `/api/v1/guards/health` - Health check endpoint

