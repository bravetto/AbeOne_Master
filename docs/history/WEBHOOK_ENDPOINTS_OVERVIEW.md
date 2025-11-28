# AIGuards Backend Webhook Endpoints Overview

This document provides a comprehensive overview of all webhook endpoints in the AIGuards Backend system, including their configurations, supported events, and security features.

##  **Webhook Endpoints Summary**

The AIGuards Backend system has **3 webhook endpoints** across two services:

### **Node.js/Express (BiasGuard Backend)**
- **Stripe Webhook**: `https://your-domain.com/webhook/stripe/`
- **Clerk Webhook**: `https://your-domain.com/webhook/clerk/`

### **Python/FastAPI (CodeGuardians Gateway)**
- **Stripe Webhook**: `https://your-domain.com/api/v1/subscriptions/webhook/stripe`

---

##  **Detailed Endpoint Information**

### **1. Stripe Webhook (Node.js) - BiasGuard Backend**

**Endpoint**: `POST /webhook/stripe/`
**Service**: BiasGuard Backend (Node.js/Express)
**File**: `guards/biasguard-backend/src/router/webhook/stripe.wh.router.ts`

#### **Configuration**
```typescript
const stripeWhRouter = Router();
stripeWhRouter.post(
  '/',
  bodyParser.raw({ type: 'application/json' }),
  stripeWebhookAction,
);
```

#### **Security Features**
-  **Signature Verification**: Uses Stripe webhook signature verification
-  **Raw Body Parsing**: Correctly configured for webhook payloads
-  **Error Handling**: Comprehensive error handling with proper HTTP status codes

#### **Supported Events**
- `product.created` - New product creation
- `product.updated` - Product updates
- `product.deleted` - Product deletion
- `price.created` - New price creation
- `price.updated` - Price updates
- `price.deleted` - Price deletion
- `customer.subscription.created` - New subscription creation
- `customer.subscription.updated` - Subscription updates
- `customer.subscription.deleted` - Subscription cancellation
- `customer.subscription.paused` - Subscription pausing
- `customer.subscription.resumed` - Subscription resumption
- `invoice.payment_succeeded` - Successful payment
- `invoice.payment_failed` - Failed payment

#### **Handler Services**
- `productWebHookHandler` - Product lifecycle management
- `priceWebHookHandler` - Pricing management
- `subscriptionWebHookHandler` - Subscription state management
- `invoiceWebHookHandler` - Payment processing

---

### **2. Clerk Webhook (Node.js) - BiasGuard Backend**

**Endpoint**: `POST /webhook/clerk/`
**Service**: BiasGuard Backend (Node.js/Express)
**File**: `guards/biasguard-backend/src/router/webhook/clerk.wh.router.ts`

#### **Configuration**
```typescript
const clerkWhRouter = Router();
clerkWhRouter.post(
  '/',
  bodyParser.raw({ type: 'application/json' }),
  clerkWebhookAction,
);
```

#### **Security Features**
-  **Signature Verification**: Uses Clerk webhook signature verification with svix
-  **Header Validation**: Validates svix-id, svix-timestamp, svix-signature headers
-  **Raw Body Parsing**: Correctly configured for webhook payloads

#### **Supported Events**
- `user.created` - New user registration
- `user.updated` - User profile updates
- `user.deleted` - User account deletion

#### **Handler Services**
- `ClerkUserWebhookService` - User management operations
  - `createUserHandler` - Creates user and team on registration
  - `updateUserHandler` - Updates user profile information
  - `deleteUserHandler` - Handles user account deletion

---

### **3. Stripe Webhook (Python) - CodeGuardians Gateway**

**Endpoint**: `POST /api/v1/subscriptions/webhook/stripe`
**Service**: CodeGuardians Gateway (Python/FastAPI)
**File**: `codeguardians-gateway/codeguardians-gateway/app/api/v1/subscriptions.py`

#### **Configuration**
```python
@router.post("/webhook/stripe")
async def handle_stripe_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
```

#### **Security Features**
-  **Signature Verification**: Uses Stripe webhook signature verification
-  **Raw Body Handling**: Properly handles raw request body
-  **Error Handling**: Comprehensive error handling with HTTP exceptions
-  **Background Tasks**: Uses FastAPI background tasks for processing

#### **Supported Events**
- `checkout.session.completed` - Successful checkout completion
- `invoice.payment_succeeded` - Successful payment processing
- `invoice.payment_failed` - Failed payment handling
- `customer.subscription.updated` - Subscription modifications

#### **Handler Functions**
- `_handle_checkout_completed` - Processes successful checkouts
- `_handle_payment_succeeded` - Handles successful payments
- `_handle_payment_failed` - Manages failed payments
- `_handle_subscription_updated` - Updates subscription status

---

##  **Security Implementation**

### **Signature Verification**

#### **Stripe Webhooks**
Both Node.js and Python implementations use Stripe's webhook signature verification:

```typescript
// Node.js
event = stripeUtil.stripeInstance.webhooks.constructEvent(
  req.body as Buffer,
  sig,
  webhookSecret,
);
```

```python
# Python
event = stripe.Webhook.construct_event(
    body, signature, webhook_secret
)
```

#### **Clerk Webhooks**
Node.js implementation uses Clerk's svix library:

```typescript
const wh = new Webhook(process.env.CLERK_WEBHOOK_SECRET!);
const event = wh.verify(req.body, {
  'svix-id': svixId,
  'svix-timestamp': svixTimestamp,
  'svix-signature': svixSignature,
}) as WebhookEvent;
```

### **Error Handling**
- **400 Bad Request**: Missing or invalid signatures
- **500 Internal Server Error**: Processing errors
- **Proper logging**: All webhook events are logged for debugging

---

##  **Testing Webhooks**

### **Test Script**
Use the provided `test_webhooks.py` script:

```bash
# Test all webhooks
python test_webhooks.py --base-url https://your-domain.com

# Test with custom secrets
python test_webhooks.py \
  --base-url https://your-domain.com \
  --stripe-secret whsec_your_stripe_secret \
  --clerk-secret whsec_your_clerk_secret

# Test only health endpoints
python test_webhooks.py --base-url https://your-domain.com --skip-webhooks
```

### **Manual Testing**

#### **Test Stripe Webhook**
```bash
curl -X POST https://your-domain.com/webhook/stripe/ \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: t=1234567890,v1=test_signature" \
  -d '{
    "type": "checkout.session.completed",
    "data": {
      "object": {
        "id": "cs_test_1234567890",
        "customer": "cus_test_1234567890",
        "subscription": "sub_test_1234567890"
      }
    }
  }'
```

#### **Test Clerk Webhook**
```bash
curl -X POST https://your-domain.com/webhook/clerk/ \
  -H "Content-Type: application/json" \
  -H "svix-id: msg_test_1234567890" \
  -H "svix-timestamp: 1234567890" \
  -H "svix-signature: v1,test_signature" \
  -d '{
    "type": "user.created",
    "data": {
      "id": "user_test_1234567890",
      "email_addresses": [{"email_address": "test@example.com"}],
      "first_name": "Test",
      "last_name": "User"
    }
  }'
```

---

##  **Configuration Requirements**

### **Environment Variables**

#### **Stripe Configuration**
```bash
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_webhook_secret
```

#### **Clerk Configuration**
```bash
CLERK_SECRET_KEY=sk_live_your_clerk_secret_key
CLERK_PUBLISHABLE_KEY=pk_live_your_clerk_publishable_key
CLERK_WEBHOOK_SECRET=whsec_your_clerk_webhook_secret
```

### **Service Configuration**

#### **Stripe Dashboard Setup**
1. Go to **Developers** → **Webhooks**
2. Add endpoint: `https://your-domain.com/webhook/stripe/` (Node.js)
3. Add endpoint: `https://your-domain.com/api/v1/subscriptions/webhook/stripe` (Python)
4. Select all required events
5. Copy webhook signing secret

#### **Clerk Dashboard Setup**
1. Go to **Webhooks** in Clerk Dashboard
2. Add endpoint: `https://your-domain.com/webhook/clerk/`
3. Select events: `user.created`, `user.updated`, `user.deleted`
4. Copy webhook signing secret

---

##  **Monitoring and Logging**

### **Webhook Event Logging**
All webhook events are logged with:
- Event type
- Processing status
- Error messages (if any)
- Processing time
- User context

### **Health Monitoring**
- Webhook endpoint availability
- Signature verification success rate
- Processing error rates
- Response times

### **Alerting**
Set up alerts for:
- Webhook endpoint failures
- Signature verification failures
- Processing errors
- High error rates

---

##  **Deployment Considerations**

### **Production Setup**
1. **HTTPS Required**: All webhook endpoints must use HTTPS
2. **Load Balancer**: Configure proper load balancing for webhook endpoints
3. **Rate Limiting**: Implement rate limiting for webhook endpoints
4. **Monitoring**: Set up comprehensive monitoring and alerting
5. **Backup**: Ensure webhook processing is idempotent and can handle retries

### **Security Best Practices**
1. **Signature Verification**: Always verify webhook signatures
2. **Secret Management**: Use secure secret management (AWS Secrets Manager)
3. **Network Security**: Use VPC and security groups
4. **Logging**: Comprehensive audit logging
5. **Error Handling**: Proper error handling without exposing sensitive information

---

##  **Troubleshooting**

### **Common Issues**

#### **Signature Verification Fails**
- Check webhook secret configuration
- Verify webhook endpoint URL
- Ensure raw body parsing is enabled

#### **Webhook Not Received**
- Check webhook endpoint URL in service dashboard
- Verify network connectivity
- Check firewall and security group settings

#### **Processing Errors**
- Check application logs
- Verify database connectivity
- Check external service dependencies

### **Debug Commands**
```bash
# Check webhook endpoint status
curl -I https://your-domain.com/webhook/stripe/

# Test webhook with invalid signature (should return 400)
curl -X POST https://your-domain.com/webhook/stripe/ \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: invalid" \
  -d '{"type":"test"}'

# Check application logs
tail -f /var/log/your-app/webhook.log
```

---

This comprehensive webhook system ensures reliable integration with external services while maintaining security and providing detailed monitoring capabilities.
