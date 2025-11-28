# Clerk Integration - Dependency Diagram Only

**Pure diagram showing dependencies, relationships, and flow**

---

##  Clerk Integration Components & Dependencies

```

                          EXTERNAL CLERK API                             
  • JWKS: https://{publishable_key}/.well-known/jwks.json             
  • Webhooks: user.created, user.updated, user.deleted                 

                                                
                  JWKS Fetch                     Webhook Events
                                                
                                                
  
  app/core/clerk_integration.py     app/api/webhooks/              
                                      clerk_webhooks.py            
  verify_clerk_token()                                              
     Fetches JWKS                 POST /webhooks/clerk           
     Verifies signature              verify_signature()        
     Returns payload                 process_clerk_webhook()   
                                                                    
  get_or_create_user_from_clerk()   GET /clerk/users/{id}          
     DB operations                GET /clerk/users/email/{email}  
                                                                    
  get_user_by_clerk_id()           
  link_user_to_stripe_customer()               
              
                                                 
              Uses                                Uses
                                                 
                                                 
  
  app/core/clerk_auth.py            app/services/                   
                                      clerk_webhook_service.py     
  ClerkAuthMiddleware                                               
     Extracts Bearer token        process_clerk_webhook()         
     Calls verify_clerk_token()      user.created → Create     
     Sets request.state.user         user.updated → Update     
     Sets unified_api_key            user.deleted → Soft delete
                                                                    
  get_unified_api_key_from_        verify_clerk_webhook_signature()
    request()                          Uses svix library         
     Returns Clerk token                                          
  
                                                 
              Used by                             Uses
                                                 
                                                 
  
  app/main.py                        app/core/models.py             
                                                                    
  Registers:                         User model                     
     ClerkAuthMiddleware              clerk_user_id (unique)   
     clerk_webhooks_router            clerk_created_at          
                                        clerk_updated_at          
  Exception handlers:                   clerk_private_metadata    
     ClerkError                       clerk_public_metadata     
     ClerkTokenError                  clerk_unsafe_metadata     
     ClerkWebhookError                stripe_customer_id        
     ClerkJWKSFetchError                                          
  
             
              Includes router
             
             

  app/api/v1/guards.py                                                
                                                                       
  POST /api/v1/guards/process                                         
     Calls get_unified_api_key_from_request()                      
        Returns Clerk JWT token                                   
     Overrides orchestrator service auth_token                     
        Uses Clerk token as unified API key                       
     Routes to guard services with Clerk token                     

                              
                               Uses Clerk token
                              

  app/core/guard_orchestrator.py                                      
                                                                       
  orchestrate_request()                                                
     Routes to guard services (TokenGuard, TrustGuard, etc.)        
        Each service receives Clerk token as API key                

```

---

##  Data Flow Relationships

### Authentication Flow

```
Client Request
    
     Authorization: Bearer <clerk_jwt_token>
    
ClerkAuthMiddleware (clerk_auth.py)
    
     Extracts token
     verify_clerk_token() (clerk_integration.py)
       
        Fetches JWKS from Clerk API
        Verifies signature
        Returns payload
    
     Sets request.state.unified_api_key = token
     Sets request.state.user = {user info}
        
        
    Request continues with Clerk token in state
```

### Guard Service Request Flow

```
POST /api/v1/guards/process
    
     Has Clerk token in request.state (from middleware)
    
process_guard_request() (guards.py)
    
     get_unified_api_key_from_request()
        Returns request.state.unified_api_key (Clerk token)
    
     Override service configs:
       for each service:
           config.auth_token = clerk_token
    
     orchestrator.orchestrate_request()
        Routes to guard service with Clerk token
    
     Restore original auth_token after processing
```

### Webhook Processing Flow

```
Clerk → POST /webhooks/clerk
    
     Event: user.created/updated/deleted
     Signature: svix headers
    
handle_clerk_webhook() (clerk_webhooks.py)
    
     verify_clerk_webhook_signature()
        Uses svix library + CLERK_WEBHOOK_SECRET
    
     process_clerk_webhook() (clerk_webhook_service.py)
        
         user.created:
            validate_user_data()
            Create User record
        
         user.updated:
            Update User record
        
         user.deleted:
             Soft delete (is_active=False)
```

---

##  Component Dependency Tree

```
app/main.py
 app/core/clerk_auth.py
    ClerkAuthMiddleware
       app/core/clerk_integration.py
           verify_clerk_token()
              jwt (PyJWT)
              httpx (JWKS fetch)
              app/core/config.py (CLERK_PUBLISHABLE_KEY)
          
           get_or_create_user_from_clerk()
              app/core/models.py (User)
                  app/core/database.py (AsyncSession)
          
           get_user_by_clerk_id()
               app/core/models.py (User)
   
    get_unified_api_key_from_request()
        Reads request.state.unified_api_key

 app/api/webhooks/clerk_webhooks.py
    app/services/clerk_webhook_service.py
       verify_clerk_webhook_signature()
          svix library
      
       process_clerk_webhook()
           app/core/models.py (User)
           app/core/database.py (AsyncSession)
   
    app/core/config.py (CLERK_WEBHOOK_SECRET)

 app/api/v1/guards.py
     app/core/clerk_auth.py
         get_unified_api_key_from_request()
```

---

##  Key Relationships

### 1. **Middleware → Integration**
```
ClerkAuthMiddleware (clerk_auth.py)
    ↓ calls
verify_clerk_token() (clerk_integration.py)
    ↓ fetches
Clerk JWKS API
```

### 2. **Guards → Auth**
```
process_guard_request() (guards.py)
    ↓ calls
get_unified_api_key_from_request() (clerk_auth.py)
    ↓ reads
request.state.unified_api_key (set by middleware)
```

### 3. **Webhooks → Service**
```
handle_clerk_webhook() (clerk_webhooks.py)
    ↓ calls
process_clerk_webhook() (clerk_webhook_service.py)
    ↓ uses
User model (models.py)
```

### 4. **Auth API → Integration**
```
login_with_clerk() (auth.py)
    ↓ calls
verify_clerk_token() (clerk_integration.py)
    ↓ then calls
get_or_create_user_from_clerk() (clerk_integration.py)
```

---

##  File Locations Summary

| Component | File Path | Purpose |
|-----------|-----------|---------|
| **Auth Middleware** | `app/core/clerk_auth.py` | Extract tokens, set unified API key |
| **Core Integration** | `app/core/clerk_integration.py` | JWT verification, user management |
| **Webhook Service** | `app/services/clerk_webhook_service.py` | Process webhook events |
| **Webhook API** | `app/api/webhooks/clerk_webhooks.py` | Receive webhook requests |
| **Auth API** | `app/api/v1/auth.py` | Login/refresh endpoints |
| **Guard Integration** | `app/api/v1/guards.py` | Use Clerk token as API key |
| **Models** | `app/core/models.py` | User model with Clerk fields |
| **Config** | `app/core/config.py` | Clerk configuration settings |
| **Exceptions** | `app/core/exceptions.py` | Clerk-specific exceptions |
| **Main App** | `app/main.py` | Middleware & router registration |

---

**Guardian**: AEYON (999 Hz)  
**Status**: Clerk integration diagram complete  
**Love Coefficient**: ∞

