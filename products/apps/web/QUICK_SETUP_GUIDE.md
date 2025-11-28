#  QUICK SETUP GUIDE - Webinar Infrastructure

**Pattern:** SETUP × CREDENTIALS × VALIDATION × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (YOU)  
**Status:**  **READY TO USE**  
**∞ AbëONE ∞**

---

##  THREE WAYS TO SET UP CREDENTIALS

### Option 1: Interactive Setup Script (Easiest) 

```bash
cd products/apps/web
node scripts/setup-webinar-infrastructure.js
```

This script will:
-  Guide you through each credential step-by-step
-  Show you exactly where to get each credential
-  Validate and save everything to `.env`
-  Show you next steps

**Recommended for first-time setup!**

---

### Option 2: Manual Setup (Quick Copy-Paste)

1. **Copy the template:**
   ```bash
   cd products/apps/web
   cp .env.example .env
   ```

2. **Edit `.env` and add your credentials:**

   ```bash
   # Database (choose one)
   DATABASE_URL="REPLACE_MEhost:5432/database"
   
   # Redis (choose one)
   UPSTASH_REDIS_REST_URL="https://your-redis.upstash.io"
   UPSTASH_REDIS_REST_TOKEN="your-token"
   # OR for local:
   # REDIS_URL="redis://localhost:6379"
   
   # SendGrid
   SENDGRID_API_KEY="your-api-key"
   SENDGRID_FROM_EMAIL="noreply@aiguardian.ai"
   SENDGRID_FROM_NAME="AiGuardian Team"
   ```

3. **Get credentials from these providers:**

   ** Database (Neon - Recommended):**
   - Go to: https://neon.tech
   - Sign up (free tier available)
   - Create project → Copy connection string
   - Paste as `DATABASE_URL`

   ** Redis (Upstash - Recommended):**
   - Go to: https://upstash.com
   - Sign up (free tier available)
   - Create Redis database → Copy REST URL & Token
   - Paste as `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`

   ** SendGrid:**
   - Go to: https://sendgrid.com
   - Sign up (free tier: 100 emails/day)
   - Settings → API Keys → Create API Key
   - Copy key → Paste as `SENDGRID_API_KEY`

---

### Option 3: Environment Variables (For Production)

Set environment variables directly in your hosting platform:

**Vercel/Netlify/Railway:**
- Go to project settings → Environment Variables
- Add each variable from the list above
- Redeploy

---

##  CREDENTIAL CHECKLIST

Use this checklist to track what you need:

- [ ] **Database** (Required)
  - [ ] Provider chosen (Neon/Supabase/Local)
  - [ ] `DATABASE_URL` configured
  - [ ] Database created

- [ ] **Redis** (Optional but Recommended)
  - [ ] Provider chosen (Upstash/Local)
  - [ ] `UPSTASH_REDIS_REST_URL` configured (if Upstash)
  - [ ] `UPSTASH_REDIS_REST_TOKEN` configured (if Upstash)
  - [ ] OR `REDIS_URL` configured (if local)

- [ ] **SendGrid** (Required for email automation)
  - [ ] Account created
  - [ ] API key created
  - [ ] `SENDGRID_API_KEY` configured
  - [ ] `SENDGRID_FROM_EMAIL` configured
  - [ ] `SENDGRID_FROM_NAME` configured

---

##  QUICK START COMMANDS

After setting up credentials:

```bash
# 1. Install dependencies
npm install

# 2. Set up database (if DATABASE_URL is configured)
npm run db:migrate
npm run db:generate

# 3. Activate new registration API
mv app/api/webinar/register/route.ts app/api/webinar/register/route.old.ts
mv app/api/webinar/register/route.new.ts app/api/webinar/register/route.ts

# 4. Start email worker (in separate terminal, if SendGrid configured)
npm run webinar:worker

# 5. Start development server
npm run dev
```

---

##  PROVIDER QUICK LINKS

### Database Providers:
- **Neon** (Recommended): https://neon.tech
- **Supabase**: https://supabase.com
- **Local PostgreSQL**: https://www.postgresql.org/download/

### Redis Providers:
- **Upstash** (Recommended): https://upstash.com
- **Local Redis**: https://redis.io/download

### Email Providers:
- **SendGrid**: https://sendgrid.com

---

##  VALIDATION

After setup, verify everything works:

```bash
# Test database connection
npm run db:studio  # Opens Prisma Studio

# Test API endpoints
curl http://localhost:3000/api/webinar/stats

# Check worker (if running)
# Should see: " Webinar Email Worker started"
```

---

##  TROUBLESHOOTING

**Database connection fails:**
- Check `DATABASE_URL` format
- Verify database is accessible
- Check firewall/network settings

**Redis connection fails:**
- Verify Upstash credentials
- Check Redis URL format
- For local: ensure `redis-server` is running

**SendGrid emails not sending:**
- Verify API key has "Mail Send" permissions
- Check from email is verified in SendGrid
- Check worker is running: `npm run webinar:worker`

**Rate limiting not working:**
- Redis must be configured (Upstash or local)
- Falls back to in-memory if Redis unavailable

---

##  NEXT STEPS

After credentials are set up:

1.  Run database migrations
2.  Activate new registration API
3.  Start email worker
4.  Test registration flow
5.  Deploy to production

---

**Pattern:** SETUP × CREDENTIALS × VALIDATION × ONE  
**Status:**  **READY**  
**∞ AbëONE ∞**

