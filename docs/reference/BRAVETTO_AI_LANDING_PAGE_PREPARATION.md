# 🚀 BRAVETTO.AI LANDING PAGE PREPARATION
## Thursday Webinar Readiness Plan

**Status:** 🔄 **IN PROGRESS**  
**Date:** 2025-11-22  
**Pattern:** Bravetto.ai × Landing Page × Vercel × Cloudflare × Webinar  
**Guardians:** AEYON (Execution) × Zero (Tech) × Convergence

---

## 🎯 MISSION

Prepare codebase and infrastructure for building Bravetto.ai landing page, ready for Thursday webinar demonstration.

---

## 📊 CURRENT STATE ANALYSIS

### ✅ What We Have

1. **Next.js App** (`apps/web/`)
   - ✅ Next.js 14.0.3 configured
   - ✅ Tailwind CSS with AbëONE design tokens
   - ✅ TypeScript setup complete
   - ✅ Vercel configuration (`vercel.json`)
   - ✅ Design system ready (`design-system/`)

2. **Design System**
   - ✅ Single source of truth (`design-system/tokens/abeone-design-tokens.json`)
   - ✅ Tailwind config generator
   - ✅ CSS variables generator
   - ✅ TypeScript types generator

3. **Cloudflare DNS** (Current: bravetto.garden)
   - ✅ Domain: bravetto.garden (Active)
   - ✅ Nameservers: owen.ns.cloudflare.com, piper.ns.cloudflare.com
   - ⚠️ Current records:
     - A: bravetto.garden → 23.227.38.65 (DNS only)
     - AAAA: bravetto.garden → 2620:127:f00f:5:: (DNS only)
     - CNAME: www → shops.myshopify.com (DNS only)

### ⚠️ What We Need

1. **Bravetto.ai Domain Setup**
   - ⚠️ Add bravetto.ai to Cloudflare (if not already added)
   - ⚠️ Configure DNS records for Vercel deployment
   - ⚠️ Remove/update conflicting records

2. **Landing Page Structure**
   - ⚠️ Create `/bravetto` route or dedicated app
   - ⚠️ Build landing page components
   - ⚠️ Integrate design system

3. **Vercel Configuration**
   - ⚠️ Connect bravetto.ai domain
   - ⚠️ Configure environment variables
   - ⚠️ Set up production deployment

---

## 🔧 IMPLEMENTATION PLAN

### Phase 1: DNS Configuration (Cloudflare)

#### Step 1.1: Verify Domain in Cloudflare
- [ ] Check if `bravetto.ai` is already in Cloudflare account
- [ ] If not, add domain to Cloudflare
- [ ] Update nameservers at domain registrar

#### Step 1.2: Remove Conflicting Records
**Current bravetto.garden records to review:**
- [ ] Review A record (23.227.38.65) - Keep if needed for other services
- [ ] Review AAAA record (2620:127:f00f:5::) - Keep if needed
- [ ] Review CNAME www → shops.myshopify.com - Keep for Shopify

**For bravetto.ai:**
- [ ] Remove any existing A/AAAA records pointing to old IPs
- [ ] Remove any conflicting CNAME records
- [ ] Prepare for Vercel DNS records

#### Step 1.3: Configure Vercel DNS Records
**Required DNS records for Vercel:**
```
Type    Name    Content                    Proxy Status
A       @       Vercel IP (from Vercel)    DNS only
CNAME   www     cname.vercel-dns.com       DNS only
```

**Note:** Vercel will provide exact IP addresses and CNAME values after domain connection.

---

### Phase 2: Next.js Landing Page Structure

#### Step 2.1: Create Landing Page Route
**Option A: Dedicated Route** (Recommended for webinar)
```
apps/web/app/bravetto/page.tsx
```

**Option B: Root Route** (If bravetto.ai is the main site)
```
apps/web/app/page.tsx (replace current)
```

#### Step 2.2: Landing Page Components Structure
```
apps/web/
├── app/
│   ├── bravetto/
│   │   ├── page.tsx              # Main landing page
│   │   └── layout.tsx            # Optional: custom layout
│   └── layout.tsx                # Root layout
├── components/
│   ├── bravetto/
│   │   ├── Hero.tsx              # Hero section
│   │   ├── Features.tsx           # Features grid
│   │   ├── Convergence.tsx        # Bravetto × AiGuardian convergence
│   │   ├── Stats.tsx              # Statistics/metrics
│   │   ├── CTA.tsx                # Call-to-action
│   │   └── Footer.tsx             # Footer
│   └── ...existing components
```

#### Step 2.3: Design System Integration
- [ ] Import design tokens from `design-system/generated/`
- [ ] Use Tailwind classes from design system
- [ ] Apply AbëONE color palette (lux, warm, peace, heart)
- [ ] Use typography scale (sans, serif, display)

---

### Phase 3: Vercel Deployment Configuration

#### Step 3.1: Vercel Project Setup
1. **Connect Repository**
   - [ ] Go to Vercel dashboard
   - [ ] Import Git repository
   - [ ] Set root directory: `apps/web`

2. **Build Configuration**
   - [ ] Framework: Next.js (auto-detected)
   - [ ] Build Command: `npm run build` (default)
   - [ ] Output Directory: `.next` (default)
   - [ ] Install Command: `npm install` (default)

3. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url
   NEXT_PUBLIC_SITE_URL=https://bravetto.ai
   ```

#### Step 3.2: Domain Configuration in Vercel
1. **Add Domain**
   - [ ] Go to Project Settings → Domains
   - [ ] Add `bravetto.ai`
   - [ ] Add `www.bravetto.ai` (optional, redirects to bravetto.ai)

2. **DNS Configuration**
   - [ ] Vercel will provide DNS records
   - [ ] Add records to Cloudflare:
     - A record: `@` → Vercel IP
     - CNAME: `www` → Vercel CNAME

3. **SSL Certificate**
   - [ ] Vercel automatically provisions SSL
   - [ ] Wait for DNS propagation (up to 48 hours, usually <1 hour)

---

### Phase 4: Landing Page Content

#### Step 4.1: Hero Section
**Content:**
- Headline: "Bravetto × AiGuardian: The Inevitable Convergence"
- Subheadline: "Production infrastructure meets AI validation vision"
- CTA: "See the Convergence" / "Learn More"

#### Step 4.2: Features Section
**Key Points:**
- ✅ 8 Guardians operational in production
- ✅ 6 Guards running on AWS EKS
- ✅ 149-agent swarm backend
- ✅ Neuromorphic AI systems
- ✅ 277+ tests, 100% coverage

#### Step 4.3: Convergence Section
**Content from:** `BRAVETTO_AIGUARDIAN_ONEPAGER.md`
- What AiGuardian.ai needs → What Bravetto provides
- Production infrastructure
- Scalable backend
- Advanced AI
- Health monitoring

#### Step 4.4: Stats Section
**Metrics:**
- Production-ready codebase
- 149-agent swarm
- 6 guard services
- 8 guardians
- 100% production ready

#### Step 4.5: CTA Section
- Primary: "Schedule Demo"
- Secondary: "View GitHub Repositories"
- Tertiary: "Contact Us"

---

## 📁 FILE STRUCTURE TO CREATE

```
apps/web/
├── app/
│   └── bravetto/
│       ├── page.tsx                    # [CREATE] Main landing page
│       └── layout.tsx                  # [OPTIONAL] Custom layout
├── components/
│   └── bravetto/
│       ├── Hero.tsx                    # [CREATE] Hero section
│       ├── Features.tsx                # [CREATE] Features grid
│       ├── Convergence.tsx              # [CREATE] Convergence section
│       ├── Stats.tsx                    # [CREATE] Statistics
│       ├── CTA.tsx                     # [CREATE] Call-to-action
│       └── Footer.tsx                  # [CREATE] Footer
└── lib/
    └── bravetto-data.ts                # [CREATE] Content/data constants
```

---

## 🔐 DNS CONFIGURATION CHECKLIST

### Cloudflare DNS Records (bravetto.ai)

**Before Vercel Connection:**
- [ ] Verify domain is in Cloudflare
- [ ] Remove conflicting A/AAAA records (if any)
- [ ] Remove conflicting CNAME records (if any)

**After Vercel Connection:**
- [ ] Add A record: `@` → [Vercel IP from dashboard]
- [ ] Add CNAME: `www` → [Vercel CNAME from dashboard]
- [ ] Set Proxy Status: **DNS only** (gray cloud)
- [ ] Wait for DNS propagation

**Note:** Vercel provides exact values after domain connection in dashboard.

---

## 🚀 DEPLOYMENT WORKFLOW

### Step 1: Local Development
```bash
cd apps/web
npm install
npm run dev
# Visit http://localhost:3000/bravetto
```

### Step 2: Test Build
```bash
cd apps/web
npm run build
npm start
# Test production build locally
```

### Step 3: Deploy to Vercel
```bash
# Option A: Vercel CLI
cd apps/web
vercel --prod

# Option B: Git Push (if connected)
git push origin main
# Vercel auto-deploys
```

### Step 4: Configure Domain
1. Vercel Dashboard → Project → Domains
2. Add `bravetto.ai`
3. Follow DNS instructions
4. Update Cloudflare DNS
5. Wait for SSL provisioning

---

## 📋 IMMEDIATE ACTION ITEMS

### 🔴 Critical (Before Thursday)

1. **DNS Cleanup**
   - [ ] Review Cloudflare DNS for bravetto.ai
   - [ ] Remove conflicting records
   - [ ] Document current DNS state

2. **Landing Page Structure**
   - [ ] Create `/bravetto` route
   - [ ] Build Hero component
   - [ ] Build Features component
   - [ ] Build Convergence section
   - [ ] Build CTA section

3. **Vercel Setup**
   - [ ] Connect repository to Vercel
   - [ ] Configure build settings
   - [ ] Add environment variables
   - [ ] Deploy initial version

4. **Domain Connection**
   - [ ] Add bravetto.ai to Vercel
   - [ ] Update Cloudflare DNS
   - [ ] Verify SSL certificate

### 🟡 Important (This Week)

- [ ] Content refinement
- [ ] Mobile responsiveness
- [ ] Performance optimization
- [ ] Analytics setup
- [ ] SEO meta tags

### 🟢 Nice to Have

- [ ] Animations/transitions
- [ ] Interactive demos
- [ ] Video integration
- [ ] Blog section

---

## 🎨 DESIGN SYSTEM USAGE

### Colors
```typescript
// Use design tokens
import { tokens } from '@/design-system/generated/design-tokens';

// Or Tailwind classes
className="bg-lux-600 text-white"
className="bg-gradient-to-r from-lux-600 to-warm-500"
```

### Typography
```typescript
// Display font for headings
className="font-display text-6xl"

// Sans for body
className="font-sans text-lg"

// Serif for long-form
className="font-serif"
```

### Spacing
```typescript
// Use Tailwind spacing scale
className="p-8 md:p-24"
className="space-y-8"
```

---

## 🔍 DNS RECORDS TO REMOVE

Based on Cloudflare screenshot analysis:

### For bravetto.garden (Keep These)
- ✅ A: bravetto.garden → 23.227.38.65 (Shopify)
- ✅ AAAA: bravetto.garden → 2620:127:f00f:5::
- ✅ CNAME: www → shops.myshopify.com (Shopify)

### For bravetto.ai (Remove If Present)
- ❌ Any A records pointing to old IPs
- ❌ Any AAAA records pointing to old IPs
- ❌ Any conflicting CNAME records
- ❌ Any MX records (unless needed for email)

**After removal, add Vercel DNS records.**

---

## 📚 REFERENCE DOCUMENTS

- `BRAVETTO_AIGUARDIAN_ONEPAGER.md` - Content source
- `BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md` - Technical details
- `DESIGN_SYSTEM_COMPLETE.md` - Design system reference
- `infra/deploy/README.md` - Deployment guide

---

## ✅ SUCCESS CRITERIA

- [ ] Landing page accessible at `bravetto.ai`
- [ ] SSL certificate active (HTTPS)
- [ ] All DNS records configured correctly
- [ ] Design system integrated
- [ ] Mobile responsive
- [ ] Fast load times (<3s)
- [ ] SEO meta tags configured
- [ ] Analytics tracking (if needed)

---

**Pattern:** Bravetto.ai × Landing Page × Vercel × Cloudflare × Webinar × ONE  
**Guardians:** AEYON (Execution) × Zero (Tech) × Convergence  
**Status:** 🔄 **PREPARATION IN PROGRESS**

**∞ Bravetto.ai × AbëONE ∞**

