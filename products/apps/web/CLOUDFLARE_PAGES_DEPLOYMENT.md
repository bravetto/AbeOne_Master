#  CLOUDFLARE PAGES DEPLOYMENT GUIDE
## Static Export → Cloudflare Pages → Global Deployment

**Status:**  READY FOR EXECUTION  
**Pattern:** YOU × META × AEYON × DNS × STATIC  
**Frequency:** 2222 × 777 × 999

---

##  PREREQUISITES

###  What You Need Ready

1. **Repository** with landing pages
   -  Next.js 14+ configured
   -  Static export enabled (`output: "export"` in next.config.js)
   -  Build produces `/out` directory

2. **Domain** in Cloudflare
   - Domain added to Cloudflare account
   - Nameservers pointed to Cloudflare (propagation < 5 minutes)

---

##  PART 1: BUILD CONFIGURATION

###  Next.js Config (Already Updated)

```1:10:apps/web/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  images: {
    unoptimized: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
}
```

###  Build Command

```bash
cd apps/web
npm run build
```

**Expected Output:**
```
./out/
  index.html
  _next/
  static/
  assets/
```

---

##  PART 2: CLOUDFLARE PAGES UI DEPLOYMENT

### Step 2.1: Create Project

1. Navigate to: **Cloudflare Dashboard → Pages → Create Project**
2. Choose: **Connect to GitHub**
3. Select repository: `AbeOne_Master`
4. Select branch: `main`

### Step 2.2: Build Configuration

**Framework preset:** `Next.js` (or `None` for custom)

**Build command:**
```bash
cd apps/web && npm install && npm run build
```

**Build output directory:**
```
apps/web/out
```

**Root directory:** (leave empty or set to `apps/web`)

**Environment variables:**
```
NODE_VERSION=18
NEXT_PUBLIC_API_URL=https://your-api-url
NEXT_PUBLIC_SITE_URL=https://bravetto.ai
```

### Step 2.3: Deploy

Click **Deploy** → First build: 30-60 seconds → Subsequent builds: ~10 seconds

**Project URL:** `https://your-project-name.pages.dev`

---

##  PART 3: DOMAIN BINDING

### Step 3.1: Add Custom Domain

1. Cloudflare Pages → Your Project → **Custom Domains** → **Add Domain**
2. Enter: `bravetto.ai`
3. Click **Add**

### Step 3.2: Add Subdomain (Optional)

1. **Custom Domains** → **Add Domain**
2. Enter: `live.bravetto.ai`
3. Click **Add**

**Cloudflare auto-generates:**
-  DNS records (CNAME)
-  SSL certificate (30-120 seconds)
-  HTTPS redirect

---

##  PART 4: DNS RECORDS (Auto-Generated)

Cloudflare Pages **automatically creates** DNS records. Verify in:

**Cloudflare Dashboard → DNS → Records**

**Auto-created records:**
```
Type: CNAME
Name: @ (or bravetto.ai)
Target: your-project-name.pages.dev
Proxy: ON (orange cloud)
TTL: Auto
```

**For subdomain:**
```
Type: CNAME
Name: live
Target: your-project-name.pages.dev
Proxy: ON (orange cloud)
TTL: Auto
```

**Manual override (if needed):**
- If auto-creation fails, manually add CNAME records above
- Ensure Proxy is **ON** (orange cloud) for DDoS protection

---

##  PART 5: BUILD COMMANDS (EXACT)

### Local Build Test

```bash
cd apps/web
npm install
npm run build
ls -la out/
```

### Cloudflare Pages Build (Production)

```bash
cd apps/web && npm install && npm run build
```

**Output:** `apps/web/out/`

---

##  PART 6: AEYON AUTO-BIND MICROSERVICE

See: `scripts/cloudflare_pages_auto_bind.py`

**Usage:**
```bash
python scripts/cloudflare_pages_auto_bind.py \
  --domain bravetto.ai \
  --subdomain live \
  --project-name abeone-web \
  --token YOUR_CLOUDFLARE_API_TOKEN
```

**Features:**
-  Auto-creates DNS records
-  Binds domain to Pages project
-  Verifies SSL certificate
-  Reports deployment status

---

##  PART 7: CI/CD AUTOMATION (GitHub Actions)

See: `.github/workflows/cloudflare-pages.yml`

**Triggers:**
- Push to `main` branch
- Pull request to `main`

**Actions:**
1. Install dependencies
2. Build static export
3. Deploy to Cloudflare Pages
4. Verify deployment

---

##  VERIFICATION CHECKLIST

### Pre-Deployment
- [ ] `next.config.js` has `output: 'export'`
- [ ] `next.config.js` has `images: { unoptimized: true }`
- [ ] Local build produces `/out` directory
- [ ] Domain added to Cloudflare account

### Deployment
- [ ] Cloudflare Pages project created
- [ ] GitHub repository connected
- [ ] Build command configured
- [ ] Build output directory set to `apps/web/out`
- [ ] First deployment successful

### Domain Binding
- [ ] Custom domain added (`bravetto.ai`)
- [ ] DNS records auto-created (or manually added)
- [ ] SSL certificate active (30-120 seconds)
- [ ] HTTPS redirect working

### Post-Deployment
- [ ] `https://bravetto.ai` loads correctly
- [ ] `https://live.bravetto.ai` loads correctly (if configured)
- [ ] All pages render correctly
- [ ] Images load correctly
- [ ] No console errors

---

##  TROUBLESHOOTING

### Build Fails

**Error:** `Error: Image Optimization requires Next.js Image component`
**Fix:** Ensure `images: { unoptimized: true }` in `next.config.js`

**Error:** `Error: output: 'export' requires static pages`
**Fix:** Remove any API routes or server-side rendering from pages

### DNS Not Propagating

**Wait:** 30-90 seconds for DNS propagation  
**Check:** `dig bravetto.ai` or use [dnschecker.org](https://dnschecker.org)  
**Verify:** Cloudflare DNS records are correct

### SSL Certificate Not Active

**Wait:** 30-120 seconds after DNS propagation  
**Check:** Cloudflare Pages → Custom Domains → SSL status  
**Verify:** Domain is properly bound to Pages project

### Pages Not Loading

**Check:** Build logs in Cloudflare Pages dashboard  
**Verify:** Build output directory is correct (`apps/web/out`)  
**Test:** Visit `https://your-project-name.pages.dev` directly

---

##  PERFORMANCE METRICS

**Expected Results:**
-  **Build time:** ~10 seconds (after first build)
-  **Deploy time:** ~30 seconds
-  **Global CDN:** 200+ edge locations
-  **SSL:** Automatic (Let's Encrypt)
-  **DDoS Protection:** Included (Cloudflare proxy)
-  **Cache:** Automatic edge caching

---

##  NEXT STEPS

1.  Deploy to Cloudflare Pages
2.  Bind domain (`bravetto.ai`)
3.  Verify SSL certificate
4.  Test all pages
5.  Monitor performance

**Pattern:** STATIC × PAGES × DNS × SSL × ONE  
**Status:**  READY FOR EXECUTION

