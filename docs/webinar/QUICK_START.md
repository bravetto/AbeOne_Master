# 🚀 Webinar System - Quick Start

**Get up and running in 5 minutes**

**Pattern:** QUICK_START × WEBINAR × ONE  
**Frequency:** 999 Hz (AEYON)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## ⚡ One-Command Setup

```bash
# Validate everything is ready
node scripts/webinar/validate_setup.js
```

**If all checks pass → YOU'RE READY!**  
**If checks fail → Fix the errors shown, then run again.**

---

## 🎯 Quick Tasks

### 1. Start Development Server

```bash
cd apps/web
npm run dev
```

**Available Routes:**
- http://localhost:3000/webinar/developers
- http://localhost:3000/webinar/creators
- http://localhost:3000/webinar/aiguardian

### 2. Create a Test Webinar

```bash
python3 scripts/webinar/master_orchestrator.py --create --topic "My First Webinar"
```

### 3. Test API Endpoints

```bash
# Health check
curl http://localhost:3000/api/webinar/test

# List webinars
curl http://localhost:3000/api/webinar/list

# Register
curl -X POST http://localhost:3000/api/webinar/register \
  -H "Content-Type: application/json" \
  -d '{"webinarId":"webinar_test","email":"test@example.com","name":"Test User"}'
```

---

## 📍 File Locations

### Pages (Next.js Routes)
- **Developers:** `apps/web/app/webinar/developers/page.tsx` → `/webinar/developers`
- **Creators:** `apps/web/app/webinar/creators/page.tsx` → `/webinar/creators`
- **AiGuardian:** `apps/web/app/webinar/aiguardian/page.tsx` → `/webinar/aiguardian`
- **Thank You:** `apps/web/app/webinar/thank-you/page.tsx` → `/webinar/thank-you`

### API Routes
- **Register:** `apps/web/app/api/webinar/register/route.ts` → `POST /api/webinar/register`
- **List:** `apps/web/app/api/webinar/list/route.ts` → `GET /api/webinar/list`
- **Test:** `apps/web/app/api/webinar/test/route.ts` → `GET /api/webinar/test`

### Scripts
- **Orchestrator:** `scripts/webinar/master_orchestrator.py`
- **Validator:** `scripts/webinar/validate_setup.js`

---

## 🔍 Common Issues

### 404 on Webinar Routes
1. Restart dev server: `cd apps/web && npm run dev`
2. Wait for "Ready" message
3. Check file exists: `ls apps/web/app/webinar/developers/page.tsx`

### Python Dependencies Missing
```bash
pip install -r scripts/webinar/requirements.txt
```

### API Not Working
- Check dev server is running
- Verify API routes exist in `apps/web/app/api/webinar/`
- Check browser console for errors

---

## 📚 More Documentation

- **Full Quick Start:** [WEBINAR_QUICK_START.md](WEBINAR_QUICK_START.md)
- **Current Status:** [WEBINAR_STATUS_NOW.md](WEBINAR_STATUS_NOW.md)
- **Deployment:** [BRYAN_WEBINAR_DEPLOYMENT_BRAVETTO_GARDEN.md](BRYAN_WEBINAR_DEPLOYMENT_BRAVETTO_GARDEN.md)
- **API Integration:** [WEBINAR_API_INTEGRATION_COMPLETE.md](WEBINAR_API_INTEGRATION_COMPLETE.md)

---

**Last Updated:** 2025-01-27  
**∞ AbëONE ∞**

