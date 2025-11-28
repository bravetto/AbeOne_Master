# Environment Variables Documentation
# This file documents all environment variables used across AIGuards Backend services

## Database Configuration

### DATABASE_URL
- **Required**: Yes (for services using database)
- **Format**: `postgresql+asyncpg://user:password@host:port/database` (for Gateway)
- **Format**: `REPLACE_MEhost:port/database` (for HealthGuard)
- **Development**: Use local Postgres: `postgresql+asyncpg://aiguardian:aiguardian-secure-password-2024@postgres:5432/aiguardian_unified`
- **Production**: Use AWS Secrets Manager or environment variables
- **Note**: Gateway automatically converts `postgresql://` to `postgresql+asyncpg://` if needed

### DATABASE_HOST
- **Default**: `postgres` (container name)
- **Purpose**: Database hostname for connection

### DATABASE_PORT
- **Default**: `5432`
- **Purpose**: PostgreSQL port

### DATABASE_USER
- **Default**: `aiguardian`
- **Purpose**: Database username

### DATABASE_PASSWORD
- **Required**: Yes
- **Default**: `aiguardian-secure-password-2024` (development only)
- **Production**: Use AWS Secrets Manager
- **Warning**: Set this value to avoid warnings - use strong passwords in production

### DATABASE_NAME
- **Default**: `aiguardian_unified`
- **Purpose**: Primary database name

### HEALTHGUARD_DATABASE_URL
- **Required**: Yes (for HealthGuard)
- **Format**: `REPLACE_MEhost:port/database`
- **Default**: Same as DATABASE_URL
- **Note**: HealthGuard uses psycopg2, not asyncpg

### POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
- **Legacy variables**: Supported for backward compatibility
- **Purpose**: Alternative database configuration format

## Redis Configuration

### REDIS_URL
- **Format**: `REPLACE_MEhost:port/db`
- **Default**: `REPLACE_MEredis:6379/0`

### REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
- **Purpose**: Individual Redis configuration components
- **Note**: REDIS_URL is constructed from these if not explicitly set

## Rate Limiting

### RATE_LIMIT_MAX
- **Default**: `100`
- **Purpose**: Maximum requests per window (BiasGuard)
- **Format**: Integer

### MAX_REQUEST_SIZE
- **Default**: `1048576` (1MB)
- **Purpose**: Maximum request body size in bytes (BiasGuard)

## Service Configuration

### API_PORT
- **Default**: `3000` (BiasGuard), `8000` (other services)
- **Purpose**: Port for service to listen on

### ENVIRONMENT
- **Values**: `development`, `production`, `test`
- **Default**: `development`
- **Purpose**: Environment identifier

### DEBUG
- **Default**: `false`
- **Production**: Must be `false`
- **Purpose**: Enable debug mode

## Security

### SECRET_KEY
- **Required**: Yes (minimum 32 characters)
- **Production**: Generate with `openssl rand -hex 32`
- **Purpose**: JWT signing and encryption

### UNIFIED_API_KEY
- **Required**: Yes (for gateway-to-guard communication)
- **Production**: Generate secure random key
- **Purpose**: Authentication between gateway and guards

## External Services

### CLERK_ENABLED
- **Default**: `false`
- **Values**: `true`, `false`
- **Purpose**: Enable Clerk authentication

### STRIPE_ENABLED
- **Default**: `false`
- **Values**: `true`, `false`
- **Purpose**: Enable Stripe payments

## Notes

1. **Development**: Use `.env` file with local values
2. **Production**: Use AWS Secrets Manager (AWS_SECRETS_ENABLED=true)
3. **Never commit**: `.env` files to version control
4. **Rotate secrets**: Regularly (at least quarterly)
5. **Database drivers**: Gateway uses asyncpg, HealthGuard uses psycopg2

