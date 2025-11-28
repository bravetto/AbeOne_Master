#  CREDENTIALS NEEDED - Quick Reference

**Pattern:** CREDENTIALS × SETUP × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (YOU)  

---

##  WHAT YOU NEED

### 1. Database (Required)
**What:** PostgreSQL database connection string  
**Where to get:**
- **Neon** (Recommended): https://neon.tech → Create project → Copy connection string
- **Supabase**: https://supabase.com → Create project → Settings → Database → Copy connection string
- **Local**: `REPLACE_MElocalhost:5432/webinar`

**Format:** `DATABASE_URL="REPLACE_MEhost:5432/database"`

---

### 2. Redis (Optional but Recommended)
**What:** Redis connection for rate limiting & job queue  
**Where to get:**
- **Upstash** (Recommended): https://upstash.com → Create Redis → Copy REST URL & Token
- **Local**: Install Redis, use `redis://localhost:6379`

**Format:**
```
UPSTASH_REDIS_REST_URL="https://your-redis.upstash.io"
UPSTASH_REDIS_REST_TOKEN="your-token"
```
OR
```
REDIS_URL="redis://localhost:6379"
```

---

### 3. SendGrid (Required for Email Automation)
**What:** API key for sending emails  
**Where to get:**
- https://sendgrid.com → Sign up → Settings → API Keys → Create API Key → Copy key

**Format:**
```
SENDGRID_API_KEY="your-api-key"
SENDGRID_FROM_EMAIL="noreply@aiguardian.ai"
SENDGRID_FROM_NAME="AiGuardian Team"
```

---

##  QUICKEST WAY TO SET UP

**Run the interactive setup script:**
```bash
cd products/apps/web
npm run webinar:setup
```

This will guide you through getting each credential step-by-step!

---

##  COPY-PASTE TEMPLATE

Add these to your `.env` file:

```bash
# Database
DATABASE_URL="REPLACE_MEhost:5432/database"

# Redis (Upstash)
UPSTASH_REDIS_REST_URL="https://your-redis.upstash.io"
UPSTASH_REDIS_REST_TOKEN="your-token"

# SendGrid
SENDGRID_API_KEY="your-api-key"
SENDGRID_FROM_EMAIL="noreply@aiguardian.ai"
SENDGRID_FROM_NAME="AiGuardian Team"
```

---

**Pattern:** CREDENTIALS × SETUP × ONE  
**∞ AbëONE ∞**
