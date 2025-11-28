# Internal Testing Setup Guide

This guide explains how to set up internal testing for Chrome and VS Code extensions using Clerk JWT tokens.

## Overview

The internal testing system provides a simple way to test extensions without requiring individual user authentication. It uses a pre-configured JWT token from Clerk that can be used by your development team.

## AWS Secrets Manager Configuration

### Step 1: Create Internal Testing Secret

Create a new secret in AWS Secrets Manager for internal testing:

```bash
aws secretsmanager create-secret \
  --name "codeguardians-gateway/internal-testing" \
  --description "Internal testing configuration for Chrome and VS Code extensions" \
  --secret-string '{
    "SECRET_KEY": "REPLACE_ME",
    "ENVIRONMENT": "testing",
    "CLERK_ENABLED": "true",
    "CLERK_SECRET_KEY": "sk_test_your_clerk_test_key_here",
    "CLERK_PUBLISHABLE_KEY": "pk_test_your_clerk_publishable_key_here",
    "INTERNAL_TESTING_ENABLED": "true",
    "INTERNAL_TESTING_JWT_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "RATE_LIMIT_REQUESTS": "1000",
    "DEBUG": "true"
  }' \
  --region us-east-1
```

### Step 2: Update Environment Configuration

Set the AWS secret name in your environment:

```bash
# In your .env file or environment variables
AWS_SECRETS_NAME=codeguardians-gateway/internal-testing
AWS_SECRETS_ENABLED=true
AWS_REGION=us-east-1
```

## Clerk Setup

### Step 1: Create Internal Testing User

1. **Go to your Clerk Dashboard**
2. **Navigate to Users section**
3. **Create a new user:**
   - Email: `internal-testing@yourcompany.com`
   - REPLACE_ME
   - Role: `admin` (or appropriate role for testing)

### Step 2: Generate JWT Token

You have two options for getting the JWT token:

#### Option A: Use Clerk Dashboard
1. Go to your Clerk Dashboard
2. Navigate to the user you created
3. Generate a session token
4. Copy the JWT token

#### Option B: Use Clerk API
```bash
# Get JWT token via Clerk API
curl -X POST https://api.clerk.com/v1/sessions \
  -H "Authorization: Bearer sk_test_your_clerk_secret_key" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123456789",
    "expire_in_seconds": 86400
  }'
```

### Step 3: Update AWS Secret

Update your AWS secret with the JWT token:

```bash
aws secretsmanager update-secret \
  --secret-id "codeguardians-gateway/internal-testing" \
  --secret-string '{
    "SECRET_KEY": "REPLACE_ME",
    "ENVIRONMENT": "testing",
    "CLERK_ENABLED": "true",
    "CLERK_SECRET_KEY": "sk_test_your_clerk_test_key_here",
    "CLERK_PUBLISHABLE_KEY": "pk_test_your_clerk_publishable_key_here",
    "INTERNAL_TESTING_ENABLED": "true",
    "INTERNAL_TESTING_JWT_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "RATE_LIMIT_REQUESTS": "1000",
    "DEBUG": "true"
  }' \
  --region us-east-1
```

## Usage

### Step 1: Get Internal Testing Token

```bash
# Get the internal testing token
curl http://localhost:8000/api/v1/internal-testing/token
```

Response:
```json
{
  "jwt_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "api_url": "http://localhost:8000",
  "expires_at": "Never (internal testing token)",
  "usage_instructions": {
    "chrome_extension": "Use as Authorization: Bearer <token> header",
    "vscode_extension": "Use as Authorization: Bearer <token> header",
    "curl_example": "curl -H 'Authorization: Bearer <token>' http://localhost:8000/api/v1/guards/process"
  }
}
```

### Step 2: Test API with JWT Token

```bash
# Test the API with the JWT token
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "biasguard",
    "payload": {
      "text": "This is a test message for bias detection"
    },
    "client_type": "chrome"
  }'
```

## Extension Integration

### Chrome Extension

Update your Chrome extension to use JWT authentication:

```javascript
// background.js
class AIGuardianBackground {
  constructor() {
    this.jwtToken = null;
    this.apiUrl = 'http://localhost:8000';
    this.init();
  }

  async init() {
    // Get JWT token from internal testing endpoint
    try {
      const response = await fetch('http://localhost:8000/api/v1/internal-testing/token');
      const data = await response.json();
      this.jwtToken = data.jwt_token;
      console.log('Internal testing JWT token loaded');
    } catch (error) {
      console.error('Failed to get JWT token:', error);
    }
  }

  async analyzeText(text, serviceType = 'biasguard') {
    if (!this.jwtToken) {
      throw new Error('JWT token not available');
    }

    const response = await fetch(`${this.apiUrl}/api/v1/guards/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.jwtToken}`
      },
      body: JSON.stringify({
        service_type: serviceType,
        payload: { text },
        client_type: 'chrome'
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  }
}
```

### VS Code Extension

Update your VS Code extension to use JWT authentication:

```typescript
// src/services/apiService.ts
export class APIService {
  private jwtToken: string | null = null;
  private apiUrl = 'http://localhost:8000';

  async init() {
    // Get JWT token from internal testing endpoint
    try {
      const response = await fetch('http://localhost:8000/api/v1/internal-testing/token');
      const data = await response.json();
      this.jwtToken = data.jwt_token;
      console.log('Internal testing JWT token loaded');
    } catch (error) {
      console.error('Failed to get JWT token:', error);
    }
  }

  async analyzeText(text: string, serviceType: string): Promise<GuardResponse> {
    if (!this.jwtToken) {
      throw new Error('JWT token not available');
    }

    const response = await fetch(`${this.apiUrl}/api/v1/guards/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.jwtToken}`
      },
      body: JSON.stringify({
        service_type: serviceType,
        payload: { text },
        client_type: 'vscode'
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  }
}
```

## Security Considerations

1. **Token Rotation**: Regularly rotate the JWT token in Clerk
2. **Access Control**: Limit access to the internal testing endpoint
3. **Monitoring**: Monitor usage of the internal testing token
4. **Environment Separation**: Use different tokens for different environments

## Troubleshooting

### Common Issues

1. **"Internal testing not enabled"**
   - Check that `INTERNAL_TESTING_ENABLED=true` in AWS secret
   - Verify `INTERNAL_TESTING_JWT_TOKEN` is set

2. **"Invalid token"**
   - Verify the JWT token is valid in Clerk
   - Check token expiration
   - Ensure token has proper permissions

3. **"Authentication required"**
   - Verify the Authorization header format: `Bearer <token>`
   - Check that the token is not expired

### Debug Commands

```bash
# Check if internal testing is enabled
curl http://localhost:8000/api/v1/internal-testing/token

# Test JWT token validity
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/guards/health

# Check AWS secret configuration
aws secretsmanager get-secret-value \
  --secret-id "codeguardians-gateway/internal-testing" \
  --region us-east-1
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `INTERNAL_TESTING_ENABLED` | Enable internal testing | `false` | Yes |
| `INTERNAL_TESTING_JWT_TOKEN` | JWT token for internal testing | `null` | Yes |
| `CLERK_ENABLED` | Enable Clerk authentication | `false` | Yes |
| `CLERK_SECRET_KEY` | Clerk secret key | `null` | Yes |
| `CLERK_PUBLISHABLE_KEY` | Clerk publishable key | `null` | Yes |
| `AWS_SECRETS_ENABLED` | Enable AWS Secrets Manager | `true` | No |
| `AWS_SECRETS_NAME` | AWS secret name | `codeguardians-gateway/production` | No |
| `AWS_REGION` | AWS region | `us-east-1` | No |
