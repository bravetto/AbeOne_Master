# ⚡ VERCEL DEPLOYMENT - QUICK START
## Alternative to Cloudflare Pages (During Outage)

**Status:** ✅ **READY FOR IMMEDIATE DEPLOYMENT**  
**Time Required:** ~5 minutes  
**Pattern:** VERCEL × DEPLOY × FAST × ONE

---

## 🚀 3-STEP DEPLOYMENT

### Step 1: Sign Up & Import (2 minutes)

1. **Go to Vercel:**
   👉 https://vercel.com/signup

2. **Sign up with GitHub:**
   - Click: **Continue with GitHub**
   - Authorize Vercel

3. **Import Repository:**
   - Click: **Add New Project**
   - Select: **`AbeOne_Master`**
   - Click: **Import**

### Step 2: Configure Build (1 minute)

**Project Settings:**
- **Framework Preset:** `Other` (we're using static export)
- **Root Directory:** `apps/web`
- **Build Command:** `cd apps/web && npm install && npm run build`
- **Output Directory:** `apps/web/out`
- **Install Command:** `npm install` (default)

**Environment Variables (optional):**
```
NEXT_PUBLIC_API_URL=https://your-api-url
NEXT_PUBLIC_SITE_URL=https://bravetto.ai
```

### Step 3: Deploy & Add Domain (2 minutes)

1. **Deploy:**
   - Click: **Deploy**
   - Wait: ~30 seconds
   - ✅ Live at: `https://your-project.vercel.app`

2. **Add Custom Domain:**
   - Go to: Project → Settings → Domains
   - Add: `bravetto.ai`
   - Follow DNS instructions (add CNAME record)

**Done!** 🎉

---

## 🔗 DIRECT LINKS

- **Sign Up:** https://vercel.com/signup
- **Dashboard:** https://vercel.com/dashboard
- **New Project:** https://vercel.com/new
- **Documentation:** https://vercel.com/docs

---

## 📋 BUILD CONFIGURATION SUMMARY

```
Root Directory: apps/web
Build Command: cd apps/web && npm install && npm run build
Output Directory: apps/web/out
Framework: Other (static export)
Node Version: 18
```

---

## ✅ ADVANTAGES OF VERCEL

- ✅ **Fast:** ~30 second deployments
- ✅ **Next.js Optimized:** Made by Next.js creators
- ✅ **Free Tier:** Generous limits
- ✅ **Auto SSL:** Automatic HTTPS
- ✅ **Global CDN:** Fast worldwide
- ✅ **Easy Domain:** Simple custom domain setup

---

**Status:** ✅ **READY - DEPLOY IN 5 MINUTES**

