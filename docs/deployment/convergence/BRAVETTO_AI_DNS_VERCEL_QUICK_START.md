#  BRAVETTO.AI DNS & VERCEL QUICK START
## Thursday Webinar Preparation

**Status:**  **READY FOR CONFIGURATION**  
**Pattern:** DNS × Vercel × Cloudflare × Quick Start

---

##  PRE-FLIGHT CHECKLIST

###  Codebase Ready
- [x] Landing page created: `/apps/web/app/bravetto/page.tsx`
- [x] Components created: Hero, Features, Convergence, Stats, CTA, Footer
- [x] Design system integrated
- [x] No linting errors

###  Infrastructure Needed
- [ ] Vercel project connected
- [ ] Domain added to Vercel
- [ ] Cloudflare DNS configured
- [ ] SSL certificate active

---

##  STEP 1: VERCEL DEPLOYMENT

### 1.1 Connect Repository
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import Git repository: `AbeOne_Master`
4. Configure:
   - **Root Directory:** `apps/web`
   - **Framework Preset:** Next.js (auto-detected)
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)
   - **Install Command:** `npm install` (default)

### 1.2 Environment Variables
Add to Vercel project settings:
```
NEXT_PUBLIC_API_URL=https://your-backend-url
NEXT_PUBLIC_SITE_URL=https://bravetto.ai
```

### 1.3 Deploy
- Click "Deploy"
- Wait for build to complete
- Test deployment URL: `https://your-project.vercel.app`

---

##  STEP 2: DOMAIN CONFIGURATION

### 2.1 Add Domain to Vercel
1. Go to Project Settings → Domains
2. Click "Add Domain"
3. Enter: `bravetto.ai`
4. Click "Add"
5. Vercel will show DNS records needed

### 2.2 Vercel DNS Records (Example)
```
Type    Name    Value                    Proxy Status
A       @       76.76.21.21              DNS only
CNAME   www     cname.vercel-dns.com     DNS only
```

** IMPORTANT:** Vercel will provide exact values. Use those, not the example above.

---

##  STEP 3: CLOUDFLARE DNS CONFIGURATION

### 3.1 Access Cloudflare
1. Go to [dash.cloudflare.com](https://dash.cloudflare.com)
2. Select domain: `bravetto.ai`
3. Go to DNS → Records

### 3.2 Remove Conflicting Records
**Before adding Vercel records, remove:**
-  Any A records pointing to old IPs
-  Any AAAA records pointing to old IPs
-  Any conflicting CNAME records (except www if needed)

**Keep:**
-  MX records (if using email)
-  Other service records (if needed)

### 3.3 Add Vercel DNS Records
1. Click "Add record"
2. Add A record:
   - **Type:** A
   - **Name:** `@` (or root domain)
   - **IPv4 address:** [From Vercel dashboard]
   - **Proxy status:** 🟡 DNS only (gray cloud)
   - **TTL:** Auto
   - Click "Save"

3. Add CNAME record:
   - **Type:** CNAME
   - **Name:** `www`
   - **Target:** [From Vercel dashboard, e.g., `cname.vercel-dns.com`]
   - **Proxy status:** 🟡 DNS only (gray cloud)
   - **TTL:** Auto
   - Click "Save"

### 3.4 Verify DNS Propagation
- Check DNS propagation: [dnschecker.org](https://dnschecker.org)
- Enter: `bravetto.ai`
- Look for A record matching Vercel IP
- Wait 5-60 minutes for propagation

---

##  STEP 4: SSL CERTIFICATE

### 4.1 Automatic SSL
- Vercel automatically provisions SSL certificates
- Wait 5-60 minutes after DNS propagation
- Check SSL status in Vercel dashboard

### 4.2 Verify SSL
- Visit: `https://bravetto.ai`
- Should show padlock icon
- Should redirect HTTP → HTTPS automatically

---

##  VERIFICATION CHECKLIST

### DNS
- [ ] A record added in Cloudflare
- [ ] CNAME record added in Cloudflare
- [ ] Proxy status: DNS only (gray cloud)
- [ ] DNS propagated (check dnschecker.org)

### Vercel
- [ ] Domain added to Vercel project
- [ ] DNS records configured
- [ ] SSL certificate active
- [ ] Deployment successful

### Website
- [ ] `https://bravetto.ai` loads correctly
- [ ] `https://www.bravetto.ai` redirects correctly
- [ ] SSL certificate valid
- [ ] All pages load without errors

---

##  TROUBLESHOOTING

### DNS Not Propagating
- **Wait:** DNS can take up to 48 hours (usually <1 hour)
- **Check:** Use dnschecker.org to verify globally
- **Verify:** Cloudflare DNS records are correct

### SSL Certificate Not Issuing
- **Wait:** SSL issues after DNS propagation (5-60 minutes)
- **Check:** DNS records are correct
- **Verify:** Domain is correctly added in Vercel

### Website Not Loading
- **Check:** Vercel deployment status
- **Verify:** Root directory is `apps/web`
- **Test:** Visit Vercel deployment URL directly
- **Review:** Build logs in Vercel dashboard

### Cloudflare Proxy Issues
- **Solution:** Set Proxy status to "DNS only" (gray cloud)
- **Reason:** Vercel handles SSL, not Cloudflare
- **Note:** Orange cloud = Cloudflare proxy (not needed)

---

##  QUICK REFERENCE

### Vercel Dashboard
- **URL:** [vercel.com/dashboard](https://vercel.com/dashboard)
- **Domain Settings:** Project → Settings → Domains
- **Deployment Logs:** Project → Deployments

### Cloudflare Dashboard
- **URL:** [dash.cloudflare.com](https://dash.cloudflare.com)
- **DNS Records:** Domain → DNS → Records
- **SSL/TLS:** Domain → SSL/TLS

### DNS Checker
- **URL:** [dnschecker.org](https://dnschecker.org)
- **Usage:** Enter domain, select record type, check globally

---

##  NEXT STEPS AFTER DNS CONFIGURED

1. **Test Landing Page**
   - Visit `https://bravetto.ai`
   - Test all sections
   - Verify mobile responsiveness

2. **SEO Setup**
   - Add meta tags (already in layout.tsx)
   - Submit to Google Search Console
   - Add sitemap.xml

3. **Analytics** (Optional)
   - Add Google Analytics
   - Add Vercel Analytics
   - Track page views

4. **Performance**
   - Run Lighthouse audit
   - Optimize images
   - Enable Vercel Edge Functions (if needed)

---

**Pattern:** DNS × Vercel × Cloudflare × Quick Start × ONE  
**Status:**  **READY FOR CONFIGURATION**

**∞ Bravetto.ai × AbëONE ∞**

