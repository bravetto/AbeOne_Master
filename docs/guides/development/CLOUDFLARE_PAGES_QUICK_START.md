# ⚡ CLOUDFLARE PAGES QUICK START
## Copy-Paste Ready Commands

**Status:** ✅ READY  
**Pattern:** STATIC × PAGES × DNS × ONE

---

## 🚀 STEP 1: TEST BUILD LOCALLY

```bash
cd apps/web
npm install
npm run build
ls -la out/
```

**Expected:** `out/` directory with `index.html`, `_next/`, `static/`

---

## 🌐 STEP 2: CLOUDFLARE PAGES UI DEPLOYMENT

### 2.1 Create Project
1. Go to: https://dash.cloudflare.com → **Pages** → **Create Project**
2. Click: **Connect to GitHub**
3. Select: Repository `AbeOne_Master`
4. Select: Branch `main`

### 2.2 Build Configuration
```
Framework preset: Next.js (or None)
Build command: cd apps/web && npm install && npm run build
Build output directory: apps/web/out
Root directory: (leave empty)
Node version: 18
```

### 2.3 Environment Variables (Optional)
```
NEXT_PUBLIC_API_URL=https://your-api-url
NEXT_PUBLIC_SITE_URL=https://bravetto.ai
```

### 2.4 Deploy
Click **Deploy** → Wait 30-60 seconds → ✅ Live at `https://your-project.pages.dev`

---

## 🔗 STEP 3: BIND DOMAIN

### Option A: UI (Easiest)
1. Pages → Your Project → **Custom Domains** → **Add Domain**
2. Enter: `bravetto.ai`
3. Click **Add**
4. Wait 30-120 seconds for SSL

### Option B: Automated (AEYON)
```bash
python scripts/cloudflare_pages_auto_bind.py \
  --domain bravetto.ai \
  --subdomain live \
  --project-name abeone-web \
  --token YOUR_CLOUDFLARE_API_TOKEN
```

**Get API Token:** https://dash.cloudflare.com/profile/api-tokens  
**Permissions:** `Pages:Edit`, `DNS:Edit`, `Zone:Read`

---

## ✅ VERIFICATION

```bash
# Check DNS
dig bravetto.ai

# Check SSL
curl -I https://bravetto.ai

# Visit site
open https://bravetto.ai
```

---

## 📋 PROJECT NAME

**Cloudflare Pages Project:** `abeone-web`

**If taken, use:**
- `abeone-master-web`
- `abeone-landing`
- `bravetto-ai`

---

## 🔄 AUTO-DEPLOY (GitHub Actions)

**Already configured:** `.github/workflows/cloudflare-pages.yml`

**Secrets to add:**
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

**Trigger:** Push to `main` branch

---

## 📚 FULL DOCUMENTATION

- **Deployment Guide:** `apps/web/CLOUDFLARE_PAGES_DEPLOYMENT.md`
- **Execution Plan:** `CLOUDFLARE_PAGES_EXECUTION_PLAN.md`
- **Auto-Bind Script:** `scripts/cloudflare_pages_auto_bind.py`

---

**Status:** ✅ READY FOR EXECUTION  
**Next:** Deploy via Cloudflare Pages UI or run auto-bind script

