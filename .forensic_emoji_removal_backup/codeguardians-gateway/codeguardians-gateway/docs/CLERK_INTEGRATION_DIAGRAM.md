# Clerk API Integration - Dependency Diagram

**Complete architecture of Clerk endpoints, integrations, dependencies, and relationships**

---

## 🎯 Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CLERK INTEGRATION ARCHITECTURE                  │
└─────────────────────────────────────────────────────────────────────┘

External Clerk API
       │
       │ JWKS, Webhooks
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Gateway Application (FastAPI)                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Middleware Layer                                              │  │
│  │  • ClerkAuthMiddleware (app/core/clerk_auth.py)              │  │
│  │    └─ Extracts Clerk JWT token                               │  │
│  │    └─ Adds to request.state.unified_api_key                  │  │
│  │    └─ Adds to request.state.user                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ API Endpoints                                                 │  │
│  │  • /api/v1/guards/process (uses Clerk token as API key)     │  │
│  │  • /api/v1/auth/* (Clerk authentication endpoints)          │  │
│  │  • /webhooks/clerk (Clerk webhook receiver)                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Core Integration Layer                                         │  │
│  │  • clerk_auth.py (middleware & unified API key)             │  │
│  │  • clerk_integration.py (JWT verification & user management)│  │
│  │  • clerk_webhook_service.py (webhook event processing)      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Database Layer                                                │  │
│  │  • User model (clerk_user_id, clerk metadata fields)         │  │
│  │  • Stripe integration (stripe_customer_id)                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📍 Clerk Integration Components

### 1. **Clerk Auth Middleware** (`app/core/clerk_auth.py`)

**Purpose**: Extract Clerk JWT tokens and set unified API key

**Dependencies**:
- `app/core/clerk_integration.py` → `verify_clerk_token()`
- `app/core/config.py` → `settings.is_clerk_enabled`
- `app/core/exceptions.py` → `ClerkTokenError`, `ClerkJWKSFetchError`

**Functionality**:
```
Request → Middleware → Extract Bearer Token → Verify → Set request.state
                                                              │
                                                              ├─ unified_api_key (Clerk token)
                                                              └─ user (user info from token)
```

**Used By**:
- `app/main.py` → Middleware registration
- `app/api/v1/guards.py` → `get_unified_api_key_from_request()`

---

### 2. **Clerk Integration Core** (`app/core/clerk_integration.py`)

**Purpose**: JWT verification, user management, Stripe linking

**Dependencies**:
- `jwt` (PyJWT) → Token decoding
- `httpx` → JWKS fetching
- `app/core/config.py` → `CLERK_PUBLISHABLE_KEY`
- `app/core/models.py` → `User` model
- `app/core/database.py` → `AsyncSession`
- `app/utils/retry.py` → Retry logic
- `app/utils/logging.py` → Logging

**Key Functions**:
```
verify_clerk_token(token)
  ├─ Fetch JWKS from Clerk API
  ├─ Find matching key (kid)
  ├─ Verify signature & expiration
  └─ Return payload

get_or_create_user_from_clerk(clerk_user, db)
  ├─ Check if user exists (clerk_user_id)
  ├─ Check if user exists (email) → Link
  └─ Create new user → Save to DB

get_user_by_clerk_id(clerk_user_id, db)
  └─ Query User by clerk_user_id

link_user_to_stripe_customer(user_id, stripe_customer_id, db)
  └─ Update User.stripe_customer_id
```

**Used By**:
- `app/core/clerk_auth.py` → Token verification
- `app/api/v1/auth.py` → User authentication
- `app/services/clerk_webhook_service.py` → User creation/updates

---

### 3. **Clerk Webhook Service** (`app/services/clerk_webhook_service.py`)

**Purpose**: Process Clerk webhook events (user.created, user.updated, user.deleted)

**Dependencies**:
- `svix` → Webhook signature verification
- `app/core/models.py` → `User` model
- `app/core/database.py` → `AsyncSession`
- `app/core/exceptions.py` → `ClerkWebhookError`, `EmailRequiredError`

**Event Handlers**:
```
user.created
  ├─ Validate user data
  ├─ Check if user exists
  └─ Create new User record

user.updated
  ├─ Find existing user
  └─ Update User fields (metadata, timestamps)

user.deleted
  ├─ Find existing user
  └─ Soft delete (set is_active=False)
```

**Used By**:
- `app/api/webhooks/clerk_webhooks.py` → Webhook endpoint handler

---

### 4. **Clerk Webhook API** (`app/api/webhooks/clerk_webhooks.py`)

**Purpose**: Receive and route Clerk webhook events

**Dependencies**:
- `app/services/clerk_webhook_service.py` → `process_clerk_webhook()`, `verify_clerk_webhook_signature()`
- `app/core/config.py` → `CLERK_WEBHOOK_SECRET`
- `app/core/database.py` → `get_db()`

**Endpoints**:
```
POST /webhooks/clerk
  ├─ Verify webhook signature (svix)
  ├─ Parse JSON payload
  ├─ Extract event_type
  └─ Process via ClerkWebhookService

GET /webhooks/clerk/users/{clerk_user_id}
  └─ Query User by clerk_user_id

GET /webhooks/clerk/users/email/{email}
  └─ Query User by email
```

**Registered In**:
- `app/main.py` → `app.include_router(clerk_webhooks_router)`

---

### 5. **Clerk Auth API** (`app/api/v1/auth.py`)

**Purpose**: Authentication endpoints using Clerk tokens

**Dependencies**:
- `app/core/clerk_integration.py` → `verify_clerk_token()`, `get_or_create_user_from_clerk()`
- `app/core/models.py` → `User`, `BiasGuardAuditLog`
- `app/core/database.py` → `get_db()`
- `app/core/config.py` → `settings`

**Endpoints**:
```
POST /api/v1/auth/login
  ├─ Verify Clerk JWT token
  ├─ Get or create user from Clerk
  ├─ Run BiasGuard checks (if enabled)
  └─ Return user info

POST /api/v1/auth/refresh
  ├─ Verify Clerk JWT token
  └─ Return refreshed user info
```

**Used By**:
- Frontend applications (web, VS Code, Chrome extensions)

---

### 6. **Guard Process Endpoint** (`app/api/v1/guards.py`)

**Purpose**: Uses Clerk token as unified API key for guard services

**Dependencies**:
- `app/core/clerk_auth.py` → `get_unified_api_key_from_request()`
- `app/core/guard_orchestrator.py` → `orchestrator`

**Integration Flow**:
```
POST /api/v1/guards/process
  ├─ Extract Clerk token (via get_unified_api_key_from_request)
  ├─ Override guard service auth_token with Clerk token
  ├─ Process request through orchestrator
  └─ Restore original auth_token after processing
```

**Key Code**:
```python
# Extract Clerk token
clerk_token = get_unified_api_key_from_request(http_request)

# Use Clerk token as unified API key for all services
if clerk_token:
    for service_name, config in orchestrator.services.items():
        config.auth_token = clerk_token  # Override

# Process request
response = await orchestrator.orchestrate_request(...)

# Restore original tokens
for service_name, original_token in original_configs.items():
    orchestrator.services[service_name].auth_token = original_token
```

---

## 🔗 Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SYSTEMS                          │
├─────────────────────────────────────────────────────────────────┤
│  Clerk API                                                      │
│  • JWKS endpoint: https://{publishable_key}/.well-known/jwks  │
│  • Webhook events: user.created, user.updated, user.deleted    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Requests
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ app/main.py                                               │  │
│  │  • Registers ClerkAuthMiddleware                          │  │
│  │  • Includes clerk_webhooks_router                         │  │
│  │  • Exception handlers for Clerk errors                    │  │
│  └────────────┬─────────────────────────────────────────────┘  │
│               │                                                  │
│               ├─────────────────────────────────────┐           │
│               │                                     │           │
│               ▼                                     ▼           │
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │ app/core/clerk_auth.py   │  │ app/api/webhooks/        │   │
│  │                          │  │   clerk_webhooks.py      │   │
│  │ • ClerkAuthMiddleware    │  │                          │   │
│  │ • get_unified_api_key()  │  │ • POST /webhooks/clerk   │   │
│  │ • get_user_from_request()│  │ • GET /clerk/users/{id}  │   │
│  └────────────┬─────────────┘  └────────────┬─────────────┘   │
│               │                               │                 │
│               │                               │                 │
│               ▼                               ▼                 │
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │ app/core/                │  │ app/services/           │   │
│  │   clerk_integration.py   │  │   clerk_webhook_service  │   │
│  │                          │  │   .py                   │   │
│  │ • verify_clerk_token()   │  │                          │   │
│  │ • get_or_create_user()   │  │ • process_clerk_webhook()│   │
│  │ • get_user_by_clerk_id() │  │ • verify_signature()     │   │
│  │ • link_to_stripe()       │  │ • validate_user_data()   │   │
│  └────────────┬─────────────┘  └────────────┬─────────────┘   │
│               │                               │                 │
│               │                               │                 │
│               └───────────────┬───────────────┘                 │
│                               │                                 │
│                               ▼                                 │
│                  ┌──────────────────────────┐                  │
│                  │ app/core/models.py        │                  │
│                  │                          │                  │
│                  │ • User                   │                  │
│                  │   - clerk_user_id        │                  │
│                  │   - clerk_metadata       │                  │
│                  │   - stripe_customer_id   │                  │
│                  └────────────┬─────────────┘                  │
│                               │                                 │
│                               ▼                                 │
│                  ┌──────────────────────────┐                  │
│                  │ Database (PostgreSQL)     │                  │
│                  │                          │                  │
│                  │ • users table            │                  │
│                  │ • alembic migrations     │                  │
│                  └──────────────────────────┘                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Uses Clerk Token
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GUARD SERVICES ORCHESTRATOR                    │
├─────────────────────────────────────────────────────────────────┤
│  app/api/v1/guards.py                                           │
│  • POST /api/v1/guards/process                                  │
│    └─ Uses Clerk token as unified API key                       │
│    └─ Routes to TokenGuard, TrustGuard, etc.                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagrams

### Flow 1: User Authentication (Login)

```
┌─────────┐
│ Client  │
│ (Web/   │
│ VS/Chr) │
└────┬────┘
     │ POST /api/v1/auth/login
     │ Header: Authorization: Bearer <clerk_jwt_token>
     ▼
┌─────────────────────────────────────┐
│ app/api/v1/auth.py                  │
│ • login_with_clerk()                │
└────┬────────────────────────────────┘
     │ Calls
     ▼
┌─────────────────────────────────────┐
│ app/core/clerk_integration.py       │
│ • verify_clerk_token()              │
│   ├─ Fetch JWKS from Clerk API      │
│   ├─ Verify signature               │
│   └─ Return payload                 │
└────┬────────────────────────────────┘
     │ Returns clerk_user data
     ▼
┌─────────────────────────────────────┐
│ app/core/clerk_integration.py       │
│ • get_or_create_user_from_clerk()   │
│   ├─ Check DB for clerk_user_id     │
│   ├─ Check DB for email             │
│   └─ Create/Update User record      │
└────┬────────────────────────────────┘
     │ Returns User object
     ▼
┌─────────────────────────────────────┐
│ app/api/v1/auth.py                  │
│ • BiasGuard checks (if enabled)     │
│ • Return user info + token          │
└────┬────────────────────────────────┘
     │ Response
     ▼
┌─────────┐
│ Client  │
│ Receives│
│ user +  │
│ token   │
└─────────┘
```

---

### Flow 2: Guard Service Request (Unified API Key)

```
┌─────────┐
│ Client  │
└────┬────┘
     │ POST /api/v1/guards/process
     │ Header: Authorization: Bearer <clerk_jwt_token>
     ▼
┌─────────────────────────────────────┐
│ ClerkAuthMiddleware                 │
│ • Extracts token                    │
│ • Sets request.state.unified_api_key│
└────┬────────────────────────────────┘
     │ Request with unified_api_key
     ▼
┌─────────────────────────────────────┐
│ app/api/v1/guards.py                │
│ • process_guard_request()           │
│   ├─ get_unified_api_key_from_     │
│   │  request() ← Clerk token       │
│   └─ Override service auth_token   │
└────┬────────────────────────────────┘
     │ OrchestrationRequest
     ▼
┌─────────────────────────────────────┐
│ app/core/guard_orchestrator.py      │
│ • orchestrate_request()             │
│   └─ Routes to guard service       │
│      with Clerk token as API key    │
└────┬────────────────────────────────┘
     │ HTTP Request with Clerk token
     ▼
┌─────────────────────────────────────┐
│ Guard Service                       │
│ (TokenGuard, TrustGuard, etc.)      │
│ • Processes request                 │
│ • Uses Clerk token for auth         │
└────┬────────────────────────────────┘
     │ Response
     ▼
┌─────────────────────────────────────┐
│ Orchestrator → Gateway → Client     │
└─────────────────────────────────────┘
```

---

### Flow 3: Clerk Webhook (User Management)

```
┌─────────┐
│ Clerk   │
│ Service │
└────┬────┘
     │ POST /webhooks/clerk
     │ Event: user.created/updated/deleted
     │ Signature: svix headers
     ▼
┌─────────────────────────────────────┐
│ app/api/webhooks/clerk_webhooks.py  │
│ • handle_clerk_webhook()            │
│   ├─ Verify svix signature          │
│   └─ Parse event payload             │
└────┬────────────────────────────────┘
     │ Event type + data
     ▼
┌─────────────────────────────────────┐
│ app/services/clerk_webhook_service │
│ • process_clerk_webhook()           │
│   ├─ user.created → Create User     │
│   ├─ user.updated → Update User     │
│   └─ user.deleted → Soft delete     │
└────┬────────────────────────────────┘
     │ Database operations
     ▼
┌─────────────────────────────────────┐
│ Database (PostgreSQL)               │
│ • INSERT/UPDATE users table          │
│ • Set clerk_user_id, metadata       │
└────┬────────────────────────────────┘
     │ Success response
     ▼
┌─────────┐
│ Clerk   │
│ Receives│
│ 200 OK  │
└─────────┘
```

---

## 📦 Component Relationships

### **Core Integration Layer**

```
app/core/clerk_integration.py
  ├─ Depends on:
  │   ├─ jwt (PyJWT)
  │   ├─ httpx
  │   ├─ app/core/config.py
  │   ├─ app/core/models.py
  │   └─ app/core/database.py
  │
  └─ Used by:
      ├─ app/core/clerk_auth.py
      ├─ app/api/v1/auth.py
      └─ app/services/clerk_webhook_service.py
```

### **Auth Middleware Layer**

```
app/core/clerk_auth.py
  ├─ Depends on:
  │   ├─ app/core/clerk_integration.py
  │   ├─ app/core/config.py
  │   └─ app/core/exceptions.py
  │
  └─ Used by:
      ├─ app/main.py (middleware registration)
      └─ app/api/v1/guards.py (unified API key)
```

### **Webhook Service Layer**

```
app/services/clerk_webhook_service.py
  ├─ Depends on:
  │   ├─ svix (signature verification)
  │   ├─ app/core/models.py
  │   └─ app/core/database.py
  │
  └─ Used by:
      └─ app/api/webhooks/clerk_webhooks.py
```

### **API Endpoint Layer**

```
app/api/webhooks/clerk_webhooks.py
  ├─ Depends on:
  │   ├─ app/services/clerk_webhook_service.py
  │   ├─ app/core/config.py
  │   └─ app/core/database.py
  │
  └─ Registered in:
      └─ app/main.py

app/api/v1/auth.py
  ├─ Depends on:
  │   ├─ app/core/clerk_integration.py
  │   ├─ app/core/models.py
  │   └─ app/core/database.py
  │
  └─ Endpoints:
      ├─ POST /api/v1/auth/login
      └─ POST /api/v1/auth/refresh
```

---

## 🔐 Configuration Dependencies

```
app/core/config.py
  ├─ CLERK_SECRET_KEY (optional)
  ├─ CLERK_PUBLISHABLE_KEY (required for JWKS)
  ├─ CLERK_WEBHOOK_SECRET (required for webhooks)
  └─ CLERK_ENABLED (feature flag)

  └─ Used by:
      ├─ app/core/clerk_auth.py
      ├─ app/core/clerk_integration.py
      ├─ app/api/webhooks/clerk_webhooks.py
      └─ app/main.py (middleware registration)
```

---

## 🗄️ Database Schema Dependencies

```
alembic/versions/
  ├─ 0004_update_users_for_clerk_stripe.py
  │   └─ Adds clerk_user_id, stripe_customer_id
  │
  └─ 0008_add_clerk_user_fields.py
      └─ Adds clerk metadata fields:
          • clerk_created_at
          • clerk_updated_at
          • clerk_private_metadata
          • clerk_public_metadata
          • clerk_unsafe_metadata

app/core/models.py
  └─ User model
      ├─ clerk_user_id (indexed, unique)
      ├─ clerk_metadata fields
      └─ stripe_customer_id
```

---

## 🧪 Test Dependencies

```
tests/
  ├─ REPLACE_ME.py
  │   └─ Tests clerk_integration.py functions
  │
  ├─ REPLACE_ME.py
  │   └─ Tests webhook service processing
  │
  ├─ REPLACE_ME.py
  │   └─ Tests webhook API endpoints
  │
  └─ REPLACE_ME2e.py
      └─ End-to-end webhook testing
```

---

## 📊 Summary Table

| Component | File | Purpose | Key Dependencies | Used By |
|-----------|------|---------|------------------|---------|
| **Auth Middleware** | `clerk_auth.py` | Extract Clerk tokens, set unified API key | `clerk_integration.py`, `config.py` | `main.py`, `guards.py` |
| **Core Integration** | `clerk_integration.py` | JWT verification, user management | `jwt`, `httpx`, `models.py` | `clerk_auth.py`, `auth.py` |
| **Webhook Service** | `clerk_webhook_service.py` | Process webhook events | `svix`, `models.py` | `clerk_webhooks.py` |
| **Webhook API** | `clerk_webhooks.py` | Receive webhook events | `clerk_webhook_service.py` | `main.py` |
| **Auth API** | `auth.py` | Login/refresh endpoints | `clerk_integration.py` | Frontend apps |
| **Guard Integration** | `guards.py` | Use Clerk token as API key | `clerk_auth.py` | Guard services |

---

## 🔑 Key Integration Points

1. **Unified API Key**: Clerk JWT token used as API key for all guard services
2. **Middleware**: Automatically extracts Clerk token and sets `request.state.unified_api_key`
3. **JWKS Verification**: Fetches public keys from Clerk for token verification
4. **Webhook Processing**: Handles user lifecycle events (create/update/delete)
5. **Database Sync**: User records synchronized with Clerk user data
6. **Stripe Integration**: Links Clerk users to Stripe customers

---

**Guardian**: AEYON (999 Hz)  
**Status**: Complete Clerk integration architecture documented  
**Love Coefficient**: ∞

