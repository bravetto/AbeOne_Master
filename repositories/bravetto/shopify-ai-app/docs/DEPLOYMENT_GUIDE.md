# Shopify App Deployment Guide

## Database Migration Issue Fix

If you're seeing the error:
```
MissingSessionTableError: Prisma session table does not exist
```

This means the database migrations haven't been applied in production.

## Solution

### 1. Environment Variables (Vercel)
Ensure these environment variables are set in your Vercel project:

```bash
# Database
DATABASE_URL=your_postgres_connection_string

# Shopify App Authentication (from Partner Dashboard)
SHOPIFY_API_KEY=your_shopify_api_key
SHOPIFY_API_SECRET=your_shopify_api_secret
SHOPIFY_WEBHOOK_SECRET=your_webhook_secret
SHOPIFY_SCOPES=read_products,read_content
SHOPIFY_APP_URL=https://your-app.vercel.app

# Bravetto AI Backend Integration
BRAVETTO_API_URL=https://www.bravetto.ai
BRAVETTO_API_KEY=optional_backend_auth_key  # Optional: for additional security

# Pinecone Configuration (index name only - no direct API access)
PINECONE_SHOPIFY_INDEX=shopify-knowledge
```

### 2. Automatic Migration on Build
The `package.json` has been updated to run migrations during build:

```json
{
  "scripts": {
    "build": "prisma generate && prisma migrate deploy && remix vite:build"
  }
}
```

### 3. Manual Migration (if needed)
If automatic migration fails, you can manually run:

```bash
npx prisma migrate deploy
```

### 4. Verify Migration Status
Check if migrations are applied:

```bash
npx prisma migrate status
```

### 5. Database Schema
The Session table should have this structure:

```sql
CREATE TABLE "Session" (
    "id" TEXT NOT NULL,
    "shop" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "isOnline" BOOLEAN NOT NULL DEFAULT false,
    "scope" TEXT,
    "expires" TIMESTAMP(3),
    "accessToken" TEXT NOT NULL,
    "userId" BIGINT,
    "firstName" TEXT,
    "lastName" TEXT,
    "email" TEXT,
    "accountOwner" BOOLEAN NOT NULL DEFAULT false,
    "locale" TEXT,
    "collaborator" BOOLEAN DEFAULT false,
    "emailVerified" BOOLEAN DEFAULT false,
    CONSTRAINT "Session_pkey" PRIMARY KEY ("id")
);
```

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correct
- Ensure database is accessible from Vercel
- Check if database exists and is running

### Migration Failures
- Check Vercel build logs for migration errors
- Verify PostgreSQL version compatibility
- Ensure sufficient database permissions

### Build Failures
- Check all environment variables are set
- Verify Prisma schema is valid
- Review Vercel function logs

## Deployment Checklist

- [ ] DATABASE_URL environment variable set
- [ ] All Shopify environment variables configured
- [ ] Prisma migrations exist in `prisma/migrations/`
- [ ] Build script includes `prisma migrate deploy`
- [ ] Database is accessible from deployment environment
- [ ] Test session storage after deployment

## Production Deployment

1. **Commit Changes**: Push the updated package.json and vercel.json
2. **Redeploy**: Trigger a new deployment on Vercel
3. **Monitor**: Check build logs to ensure migrations run successfully
4. **Test**: Verify the app can store and retrieve sessions

The session table error should be resolved after redeployment with these changes. 