# Secrets Configuration Template

This document provides templates for configuring secrets in different environments.

## Local Development (.env file)

```bash
# Basic Configuration
SECRET_KEY=development-secret-key-32-characters-minimum-length
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=REPLACE_ME_WITH_DATABASE_URL
REDIS_URL=redis://localhost:6379/0

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:8000
ALLOWED_HOSTS=localhost,127.0.0.1

# Rate Limiting
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=60

# AWS Secrets Manager (disabled for local development)
AWS_SECRETS_ENABLED=false
AWS_SECRETS_NAME=codeguardians-gateway/development
AWS_REGION=us-east-1
```

## Internal Testing (.env file)

```bash
# Basic Configuration
SECRET_KEY=internal-testing-secret-key-32-characters-minimum-length
ENVIRONMENT=testing
DEBUG=true
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=REPLACE_ME_WITH_DATABASE_URL
REDIS_URL=redis://localhost:6379/1

# CORS (includes extension origins)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:8000,chrome-extension://*,moz-extension://*
ALLOWED_HOSTS=localhost,127.0.0.1

# Rate Limiting (higher limits for testing)
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=60

# AWS Secrets Manager (enabled for internal testing)
AWS_SECRETS_ENABLED=true
AWS_SECRETS_NAME=codeguardians-gateway/internal-testing
AWS_REGION=us-east-1

# Clerk Authentication
CLERK_ENABLED=true
CLERK_SECRET_KEY=sk_test_your_clerk_test_key_here
CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_test_key_here

# Internal Testing
INTERNAL_TESTING_ENABLED=true
INTERNAL_TESTING_JWT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.REPLACE_ME.example_jwt_token_here
```

## AWS Secrets Manager Configuration

### Main Production Secret
```json
{
  "SECRET_KEY": "CHANGE-THIS-TO-A-SECURE-64-CHARACTER-RANDOM-STRING-FOR-PRODUCTION",
  "POSTGRES_PASSWORD": "CHANGE-THIS-TO-A-SECURE-DATABASE-PASSWORD",
  "REDIS_PASSWORD": "CHANGE-THIS-TO-A-SECURE-REDIS-PASSWORD",
  "DATABASE_URL": "REPLACE_ME_WITH_DATABASE_URL",
  "REDIS_URL": "redis://:CHANGE-THIS-PASSWORD@your-elasticache-endpoint:6379/0",
  "ENVIRONMENT": "production",
  "LOG_LEVEL": "INFO",
  "DEBUG": "false",
  "ALLOWED_ORIGINS": "https://your-frontend-domain.com",
  "ALLOWED_HOSTS": "your-alb-dns-name,localhost"
}
```

### Internal Testing Secret
```json
{
  "SECRET_KEY": "REPLACE_ME",
  "ENVIRONMENT": "testing",
  "CLERK_ENABLED": "true",
  "CLERK_SECRET_KEY": "sk_test_your_clerk_test_key_here",
  "CLERK_PUBLISHABLE_KEY": "pk_test_your_clerk_test_key_here",
  "INTERNAL_TESTING_ENABLED": "true",
  "INTERNAL_TESTING_JWT_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.REPLACE_ME.example_jwt_token_here",
  "RATE_LIMIT_REQUESTS": "1000",
  "DEBUG": "true"
}
```

### Database Secret
```json
{
  "username": "codeguardians-gateway",
  "password": "CHANGE-THIS-TO-A-SECURE-DATABASE-PASSWORD",
  "host": "your-rds-endpoint.amazonaws.com",
  "port": "5432",
  "database": "codeguardians_gateway_db",
  "engine": "postgres"
}
```

### Redis Secret
```json
{
  "host": "your-elasticache-endpoint.amazonaws.com",
  "port": "6379",
  "password": "CHANGE-THIS-TO-A-SECURE-REDIS-PASSWORD",
  "database": "0"
}
```

### Optional Services Secret
```json
{
  "CLERK_SECRET_KEY": "sk_live_your_production_clerk_secret_key",
  "CLERK_PUBLISHABLE_KEY": "pk_live_your_production_clerk_publishable_key",
  "STRIPE_SECRET_KEY": "sk_live_your_production_stripe_secret_key",
  "STRIPE_PUBLISHABLE_KEY": "pk_live_your_production_stripe_publishable_key",
  "STRIPE_WEBHOOK_SECRET": "whsec_your_stripe_webhook_secret"
}
```

## Usage Instructions

### 1. Local Development
- Copy the local development configuration to your `.env` file
- Update database and Redis URLs as needed
- No AWS secrets required

### 2. Internal Testing
- Copy the internal testing configuration to your `.env` file
- Set `AWS_SECRETS_NAME=codeguardians-gateway/internal-testing`
- Update Clerk keys with your actual test keys
- Generate a JWT token from Clerk and update `INTERNAL_TESTING_JWT_TOKEN`

### 3. Production
- Use AWS Secrets Manager with the production configuration
- Update all placeholder values with actual secure credentials
- Use the setup script: `./scripts/setup_aws_secrets.sh`

## Security Notes

- Never commit actual secrets to version control
- Use environment variables or AWS Secrets Manager in production
- Rotate secrets regularly
- Use different secrets for different environments
- The JWT token in internal-testing should be generated from your Clerk dashboard
- Update all placeholder values with actual secure credentials before production deployment

## Quick Setup Commands

### Create Internal Testing Secret
```bash
aws secretsmanager create-secret \
  --name "codeguardians-gateway/internal-testing" \
  --description "Internal testing secrets with Clerk JWT tokens for Chrome and VS Code extensions" \
  --secret-string '{
    "SECRET_KEY": "REPLACE_ME",
    "ENVIRONMENT": "testing",
    "CLERK_ENABLED": "true",
    "CLERK_SECRET_KEY": "sk_test_your_clerk_test_key_here",
    "CLERK_PUBLISHABLE_KEY": "pk_test_your_clerk_test_key_here",
    "INTERNAL_TESTING_ENABLED": "true",
    "INTERNAL_TESTING_JWT_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.REPLACE_ME.example_jwt_token_here",
    "RATE_LIMIT_REQUESTS": "1000",
    "DEBUG": "true"
  }' \
  --region us-east-1
```

### Update Internal Testing Secret
```bash
aws secretsmanager update-secret \
  --secret-id "codeguardians-gateway/internal-testing" \
  --secret-string '{
    "SECRET_KEY": "REPLACE_ME",
    "ENVIRONMENT": "testing",
    "CLERK_ENABLED": "true",
    "CLERK_SECRET_KEY": "sk_test_your_actual_clerk_test_key",
    "CLERK_PUBLISHABLE_KEY": "pk_test_your_actual_clerk_test_key",
    "INTERNAL_TESTING_ENABLED": "true",
    "INTERNAL_TESTING_JWT_TOKEN": "your_actual_jwt_token_from_clerk",
    "RATE_LIMIT_REQUESTS": "1000",
    "DEBUG": "true"
  }' \
  --region us-east-1
```
