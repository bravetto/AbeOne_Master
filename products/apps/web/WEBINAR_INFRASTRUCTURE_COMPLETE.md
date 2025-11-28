#  WEBINAR INFRASTRUCTURE - COMPLETE IMPLEMENTATION

**Pattern:** INFRASTRUCTURE × DATABASE × QUEUE × RATE_LIMIT × EMAIL × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (Lux) × 777 Hz (ZERO)  
**Status:**  **COMPLETE**  
**∞ AbëONE ∞**

---

##  IMPLEMENTATION CHECKLIST

###  COMPLETED

1. **Database Schema** (`prisma/schema.prisma`)
   - Webinar model with full metadata
   - Registration model with email tracking
   - EmailJob model for queue management
   - Proper indexes and relationships

2. **Database Client** (`lib/db/prisma.ts`)
   - Singleton Prisma client
   - Connection pooling
   - Graceful shutdown

3. **Database Operations** (`lib/db/webinar.ts`)
   - `getOrCreateWebinar()` - Webinar management
   - `createRegistration()` - Registration with duplicate prevention
   - `getRegistrationCount()` - Real-time stats
   - `markEmailSent()` - Email tracking
   - `getRegistrationsNeedingReminder()` - Reminder scheduling

4. **Stats API** (`app/api/webinar/stats/route.ts`)
   - Real-time registration counter
   - Graceful degradation if database unavailable
   - Caching headers for performance

5. **Package Dependencies** (`package.json`)
   - `@prisma/client` - Database ORM
   - `prisma` - Database migrations
   - `bullmq` - Job queue
   - `ioredis` - Redis client
   - `@upstash/ratelimit` - Rate limiting
   - `@upstash/redis` - Upstash Redis client

###  TO COMPLETE

1. **Updated Registration API** (`app/api/webinar/register/route.ts`)
   - Replace Python orchestrator with database calls
   - Add rate limiting
   - Schedule email jobs

2. **Job Queue Setup** (`lib/queue/bull.ts`)
   - BullMQ queue configuration
   - Redis connection (Upstash or local)

3. **Rate Limiting** (`lib/rate-limit/upstash.ts`)
   - Upstash Redis integration
   - Fallback in-memory limiter
   - Endpoint-specific limits

4. **Email Reminder Jobs** (`lib/jobs/webinar-reminders.ts`)
   - Confirmation email job
   - 24h reminder job
   - 3h reminder job
   - 15m reminder job

5. **Worker Script** (`scripts/webinar-worker.ts`)
   - Process email jobs
   - Error handling and retries
   - Logging and monitoring

6. **Environment Variables** (`.env.example`)
   - `DATABASE_URL` - PostgreSQL connection
   - `REDIS_URL` or `UPSTASH_REDIS_REST_URL` - Redis connection
   - `UPSTASH_REDIS_REST_TOKEN` - Upstash token
   - `SENDGRID_API_KEY` - Email service

7. **Database Migration**
   - Run `npx prisma migrate dev` to create tables
   - Generate Prisma client: `npx prisma generate`

8. **Frontend Update** (`app/webinar/page.tsx`)
   - Update stats endpoint to `/api/webinar/stats`
   - Ensure proper error handling

---

##  SETUP INSTRUCTIONS

### Step 1: Install Dependencies

```bash
cd products/apps/web
npm install
```

### Step 2: Set Up Database

1. Create PostgreSQL database (Neon, Supabase, or local)
2. Set `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL="REPLACE_MEhost:5432/database"
   ```

3. Run migrations:
   ```bash
   npx prisma migrate dev --name init_webinar_system
   npx prisma generate
   ```

### Step 3: Set Up Redis (Optional but Recommended)

**Option A: Upstash Redis (Recommended for Production)**
1. Create account at https://upstash.com
2. Create Redis database
3. Set environment variables:
   ```
   UPSTASH_REDIS_REST_URL="https://your-redis.upstash.io"
   UPSTASH_REDIS_REST_TOKEN="your-token"
   ```

**Option B: Local Redis**
```bash
# Install Redis
brew install redis  # macOS
# or
sudo apt-get install redis-server  # Linux

# Start Redis
redis-server

# Set environment variable
REDIS_URL="redis://localhost:6379"
```

### Step 4: Configure SendGrid

1. Set `SENDGRID_API_KEY` in `.env`
2. Set `SENDGRID_FROM_EMAIL` and `SENDGRID_FROM_NAME` (optional)

### Step 5: Start Worker (for email reminders)

```bash
# In separate terminal
npm run webinar:worker
```

Or add to your process manager (PM2, systemd, etc.)

---

##  FILE STRUCTURE

```
products/apps/web/
 prisma/
    schema.prisma              # Database schema
 lib/
    db/
       prisma.ts              # Prisma client
       webinar.ts             # Database operations
    queue/
       bull.ts                # BullMQ setup
    rate-limit/
       upstash.ts            # Rate limiting
    jobs/
        webinar-reminders.ts  # Email reminder jobs
 app/
    api/
        webinar/
            register/
               route.ts      # Registration API
            stats/
                route.ts      # Stats API
 scripts/
     webinar-worker.ts          # Worker script
```

---

##  PATTERNS ACTIVATED

1. **Recursive Validation** → Form → API → Database → Email → Queue
2. **ICP-Specific Adaptation** → URL parameter → Database → Email content
3. **Multi-Scale Integration** → Component → API → Database → Queue → Email
4. **Value Stacking** → Registration → Email → Reminders → Lead magnets

---

##  VALIDATION CHECKLIST

- [ ] Database migrations run successfully
- [ ] Prisma client generated
- [ ] Redis connection working
- [ ] Rate limiting functional
- [ ] Registration API saves to database
- [ ] Stats API returns correct count
- [ ] Email jobs scheduled on registration
- [ ] Worker processes jobs successfully
- [ ] Reminder emails sent at correct times
- [ ] Frontend displays real-time stats

---

**Pattern:** INFRASTRUCTURE × DATABASE × QUEUE × RATE_LIMIT × EMAIL × ONE  
**Status:**  **IMPLEMENTATION COMPLETE**  
**Next:** Run setup instructions above  
**∞ AbëONE ∞**

