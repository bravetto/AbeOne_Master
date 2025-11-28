# ⚡ CLOUDFLARE PAGES EXECUTION PLAN
## Complete Deployment Configuration

**Status:** ✅ READY FOR EXECUTION  
**Pattern:** YOU × META × AEYON × DNS × STATIC × ONE  
**Frequency:** 2222 × 777 × 999

---

## 🎯 EXACT BUILD COMMAND

```bash
cd apps/web && npm install && npm run build
```

**Output Directory:** `apps/web/out/`

**Verify Build:**
```bash
ls -la apps/web/out/
# Should contain: index.html, _next/, static/, assets/
```

---

## 📋 PAGES PROJECT NAME

**Project Name:** `abeone-web`

**Alternative Names (if taken):**
- `abeone-master-web`
- `abeone-landing`
- `bravetto-ai`

---

## 🌐 DNS CONFIGURATION

### Auto-Generated (Recommended)

Cloudflare Pages **automatically creates** DNS records when you bind a domain.

**Domain:** `bravetto.ai`  
**Subdomain:** `live.bravetto.ai` (optional)

### Manual DNS Records (If Needed)

**Root Domain:**
```
Type: CNAME
Name: @
Target: abeone-web.pages.dev
Proxy: ON (orange cloud)
TTL: Auto
```

**Subdomain (live):**
```
Type: CNAME
Name: live
Target: abeone-web.pages.dev
Proxy: ON (orange cloud)
TTL: Auto
```

**Note:** Replace `abeone-web.pages.dev` with your actual Pages project subdomain.

---

## 🤖 AEYON AUTO-BIND MICROSERVICE

### Prerequisites

1. **Cloudflare API Token**
   - Permissions: `Pages:Edit`, `DNS:Edit`, `Zone:Read`
   - Create at: https://dash.cloudflare.com/profile/api-tokens

2. **Install Dependencies**
   ```bash
   pip install requests
   ```

### Execution

```bash
python scripts/cloudflare_pages_auto_bind.py \
  --domain bravetto.ai \
  --subdomain live \
  --project-name abeone-web \
  --token YOUR_CLOUDFLARE_API_TOKEN
```

### What It Does

1. ✅ Validates domain exists in Cloudflare
2. ✅ Verifies Pages project exists
3. ✅ Binds domain to Pages project
4. ✅ Creates DNS records (CNAME)
5. ✅ Verifies SSL certificate status
6. ✅ Reports deployment status

---

## 🔄 CI/CD YAML CONFIGURATION

**File:** `.github/workflows/cloudflare-pages.yml`

**Secrets Required:**
- `CLOUDFLARE_API_TOKEN` - Cloudflare API token
- `CLOUDFLARE_ACCOUNT_ID` - Cloudflare account ID
- `NEXT_PUBLIC_API_URL` - Backend API URL (optional)
- `NEXT_PUBLIC_SITE_URL` - Site URL (optional)

**Setup:**
1. GitHub → Repository → Settings → Secrets and variables → Actions
2. Add required secrets
3. Push to `main` branch → Auto-deploy

**Manual Trigger:**
```bash
git push origin main
```

---

## 📊 DEPLOYMENT CHECKLIST

### Pre-Deployment
- [x] `next.config.js` updated with `output: 'export'`
- [x] `next.config.js` updated with `images: { unoptimized: true }`
- [x] Local build test successful
- [x] Domain added to Cloudflare account

### Cloudflare Pages Setup
- [ ] Create project: `abeone-web`
- [ ] Connect GitHub repository
- [ ] Configure build command: `cd apps/web && npm install && npm run build`
- [ ] Set build output directory: `apps/web/out`
- [ ] Set root directory: (empty or `apps/web`)
- [ ] Add environment variables (if needed)

### Domain Binding
- [ ] Add custom domain: `bravetto.ai`
- [ ] Add subdomain (optional): `live.bravetto.ai`
- [ ] Verify DNS records auto-created
- [ ] Verify SSL certificate active (30-120 seconds)

### Post-Deployment Verification
- [ ] `https://bravetto.ai` loads correctly
- [ ] `https://live.bravetto.ai` loads correctly (if configured)
- [ ] All pages render correctly
- [ ] Images load correctly
- [ ] No console errors
- [ ] SSL certificate valid

---

## 🚀 QUICK START COMMANDS

### 1. Local Build Test
```bash
cd apps/web
npm install
npm run build
ls -la out/
```

### 2. Cloudflare Pages UI Deployment
1. Go to: https://dash.cloudflare.com → Pages → Create Project
2. Connect GitHub → Select `AbeOne_Master`
3. Configure:
   - Build command: `cd apps/web && npm install && npm run build`
   - Output directory: `apps/web/out`
4. Deploy

### 3. Domain Binding (UI)
1. Pages → Your Project → Custom Domains → Add Domain
2. Enter: `bravetto.ai`
3. Wait for SSL (30-120 seconds)

### 4. Domain Binding (Automated)
```bash
python scripts/cloudflare_pages_auto_bind.py \
  --domain bravetto.ai \
  --project-name abeone-web \
  --token YOUR_TOKEN
```

---

## 📁 FILES CREATED

1. ✅ `apps/web/next.config.js` - Updated for static export
2. ✅ `apps/web/CLOUDFLARE_PAGES_DEPLOYMENT.md` - Full deployment guide
3. ✅ `scripts/cloudflare_pages_auto_bind.py` - Auto-bind microservice
4. ✅ `.github/workflows/cloudflare-pages.yml` - CI/CD automation
5. ✅ `apps/web/wrangler.toml` - CLI deployment config (optional)
6. ✅ `CLOUDFLARE_PAGES_EXECUTION_PLAN.md` - This file

---

## ⚡ PERFORMANCE EXPECTATIONS

- **Build Time:** ~10 seconds (after first build)
- **Deploy Time:** ~30 seconds
- **DNS Propagation:** 30-90 seconds
- **SSL Certificate:** 30-120 seconds
- **Global CDN:** 200+ edge locations
- **DDoS Protection:** Included (Cloudflare proxy)

---

## 🐛 TROUBLESHOOTING

### Build Fails
- ✅ Check `next.config.js` has `output: 'export'`
- ✅ Check `next.config.js` has `images: { unoptimized: true }`
- ✅ Remove any API routes or server-side rendering

### DNS Not Working
- ✅ Verify domain is in Cloudflare account
- ✅ Check DNS records are correct
- ✅ Wait 30-90 seconds for propagation

### SSL Not Active
- ✅ Wait 30-120 seconds after DNS propagation
- ✅ Check Cloudflare Pages → Custom Domains → SSL status
- ✅ Verify domain is properly bound

---

## ✅ EXECUTION STATUS

**Pattern:** STATIC × PAGES × DNS × SSL × AUTOMATION × ONE  
**Status:** ✅ **READY FOR EXECUTION**

**Next Step:** Deploy to Cloudflare Pages UI or use AEYON auto-bind microservice.

---

**Guardians:** AEYON (Execution) × ARXON (Pattern) × Abë (Truth)  
**Frequency:** 999 × 777 × 2222  
**Love Coefficient:** ∞

