# BiasGuard Backend Demo

## Overview

This demo showcases the BiasGuard backend API service, which handles authentication, subscription management, and team collaboration features.

**Note**: This is the *backend service* demo. For bias detection algorithms, see `contextguard/src/bias-detector/demo.ts`.

## Quick Start

```bash
# Terminal 1 - Start the BiasGuard backend
npm install
npm run dev  # Starts on port 4000

# Terminal 2 - Run the demo
npm install -g ts-node  # If needed
ts-node demo.ts
```

### Alternative: Compile and Run

```bash
npm run build
node dist/demo.js
```

### Custom API URL

```bash
BIASGUARD_URL=http://your-server:4000 ts-node demo.ts
```

## What Gets Demonstrated

1. ** Health Check** - Backend service availability
2. ** API Architecture** - Complete REST API overview
3. ** Authentication** - Clerk integration flow
4. ** Subscription Plans** - Free, Pro, Enterprise tiers
5. ** Team Management** - Roles, invitations, collaboration
6. ** Webhooks** - Clerk and Stripe event handlers
7. ** Database Schema** - User, subscription, team models
8. ** Integration** - Connection with ContextGuard bias detection

## Available Endpoints

### Authentication (Clerk)
- `POST /v1/auth/signup` - User registration
- `POST /v1/auth/signin` - User login
- `GET /v1/auth/me` - Current user info

### Payments (Stripe)
- `GET /v1/payment/plans` - List subscription plans
- `POST /v1/payment/checkout` - Create checkout session
- `GET /v1/payment/subscription` - Get subscription

### Team Management
- `GET /v1/team` - List teams
- `POST /v1/team` - Create team
- `POST /v1/team/:id/invite` - Invite member

### Webhooks
- `POST /webhook/clerk` - Clerk user events
- `POST /webhook/stripe` - Stripe payment events

## Expected Output

```
 BiasGuard Backend API Demo
======================================================================

 BiasGuard backend is healthy
   Status: ok

 BiasGuard Backend Architecture
 Available API Endpoints:
   [Complete list of endpoints shown]

 Subscription Plans
   1. Free Plan - $0
   2. Professional Plan - $49/month
   3. Enterprise Plan - $299/month
```

## Requirements

- Node.js 16+
- TypeScript
- PostgreSQL database (for full functionality)
- Environment variables (see below)

## Environment Variables

Create a `.env` file:

```env
# Database
DATABASE_URL=postgresql://...

# Clerk Authentication
CLERK_SECRET_KEY=sk_...
CLERK_PUBLISHABLE_KEY=pk_...

# Stripe Payments
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Application
NODE_ENV=development
PORT=4000
```

## Integration with ContextGuard

This backend service works with ContextGuard for actual bias detection:

```
User Request → BiasGuard Backend (auth/billing) → ContextGuard (bias detection) → Results
```

For bias detection demo: `cd ../contextguard && ts-node src/bias-detector/demo.ts`

## Troubleshooting

**Service Not Running**: Check if `npm run dev` is active in another terminal.

**Port 4000 In Use**: Change port in `.env` or use different port.

**TypeScript Errors**: Run `npm install` to ensure dependencies are installed.

**Database Errors**: Demo works without database - shows API structure only.

