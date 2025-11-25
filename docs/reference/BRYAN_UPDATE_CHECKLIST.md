# 📋 BRYAN UPDATE CHECKLIST
## Replace Placeholder Content with Real Information

**Status:** ⚠️ **PENDING UPDATES**  
**Date:** 2025-11-22  
**Pattern:** Content Update × Truth × Accuracy × ONE  
**Guardians:** ZERO (777 Hz) × AEYON (999 Hz)  
**Priority:** 🔴 **CRITICAL** - Must update before launch

---

## 🎯 EXECUTIVE SUMMARY

**Complete list of placeholder/fake content that needs to be replaced with real information.**

**Files to Update:**
1. `apps/web/app/api/webinar/register/route.ts` - Webinar details, email content
2. `apps/web/app/webinar/aiguardian/page.tsx` - Testimonials, company logos, contact info
3. `apps/web/lib/sendgrid.ts` - Email sender information
4. Environment variables (`.env.local`)

---

## 🔴 CRITICAL UPDATES (Must Fix Before Launch)

### 1. WEBINAR DETAILS ⚠️ PLACEHOLDER

**Location:** `apps/web/app/api/webinar/register/route.ts` (Lines 30-37)

**Current (Placeholder):**
```typescript
const WEBINAR_DETAILS = {
  topic: 'AiGuardian Validation System',
  scheduled_date: '2025-02-15', // Update with actual date
  scheduled_time: '2:00 PM EST', // Update with actual time
  duration: '60 minutes',
  zoom_link: 'https://zoom.us/j/your-webinar-id', // Update with actual link
  replay_link: 'https://aiguardian.ai/webinar/replay', // Update with actual replay link
}
```

**Bryan Needs to Provide:**
- ✅ **Actual webinar date** (format: YYYY-MM-DD)
- ✅ **Actual webinar time** (include timezone: e.g., "2:00 PM EST" or "11:00 AM PST")
- ✅ **Actual Zoom link** (full join URL)
- ✅ **Actual replay link** (where replay will be hosted)
- ✅ **Webinar duration** (confirm 60 minutes or update)

**Action:** Update `WEBINAR_DETAILS` constant in `route.ts`

---

### 2. EMAIL SENDER INFORMATION ⚠️ PLACEHOLDER

**Location:** `apps/web/app/api/webinar/register/route.ts` (Line 114-115)

**Current (Placeholder):**
```typescript
const fromEmail = process.env.SENDGRID_FROM_EMAIL || 'noreply@aiguardian.ai'
const fromName = process.env.SENDGRID_FROM_NAME || 'AiGuardian Team'
```

**Bryan Needs to Provide:**
- ✅ **Verified sender email** (must be verified in SendGrid)
  - Example: `noreply@aiguardian.ai` or `michael@aiguardian.ai`
  - Must match SendGrid verified sender
- ✅ **Sender name** (how you want to appear in emails)
  - Example: `"Michael from AiGuardian"` or `"AiGuardian Team"` or `"Michael Mataluni"`

**Action:** 
1. Set in `.env.local`: `SENDGRID_FROM_EMAIL` and `SENDGRID_FROM_NAME`
2. Verify sender email in SendGrid dashboard

---

### 3. CONTACT/SUPPORT EMAIL ⚠️ PLACEHOLDER

**Location:** `apps/web/app/webinar/thank-you/page.tsx` (Line ~630)

**Current (Placeholder):**
```typescript
<a href="mailto:support@aiguardian.ai">Contact Support</a>
```

**Bryan Needs to Provide:**
- ✅ **Actual support email address**
  - Example: `support@aiguardian.ai` or `hello@aiguardian.ai` or `michael@aiguardian.ai`
  - Must be monitored/checked regularly

**Action:** Update support email link in thank you page

---

### 4. TESTIMONIALS ⚠️ FAKE/PLACEHOLDER

**Location:** `apps/web/app/webinar/aiguardian/page.tsx` (Lines 184-234)

**Current (Fake Testimonials):**

**Developer Testimonials:**
- ❌ Mike Chen, Senior Engineer, DataFlow (fake)
- ❌ Sarah Kim, Engineering Lead, Stripe (fake)
- ❌ Alex Rodriguez, CTO, Shopify (fake)

**Creative Testimonials:**
- ❌ Sarah Johnson, Creator, @sarahcreates (fake)
- ❌ Marcus Williams, AI Creator, @marcusai (fake)
- ❌ Emma Davis, Founder, @emmadavis (fake)

**Bryan Needs to Provide:**

**Option A: Real Testimonials (Best)**
- ✅ **3+ real developer testimonials** with:
  - Real name
  - Real role/title
  - Real company (or "Independent Developer" if freelance)
  - Real GitHub username (if applicable)
  - Real quote (specific, technical, proof-driven)
  - Permission to use

- ✅ **3+ real creative testimonials** with:
  - Real name
  - Real role/title
  - Real social handle (Instagram/Twitter)
  - Real follower count (if applicable)
  - Real quote (emotional, aspirational, story-driven)
  - Permission to use

**Option B: Remove Testimonials (If None Available)**
- Remove testimonial section entirely
- Replace with other social proof (company logos, stats, etc.)

**Action:** Replace fake testimonials with real ones OR remove section

---

### 5. COMPANY LOGOS ⚠️ PLACEHOLDER

**Location:** `apps/web/app/webinar/aiguardian/page.tsx` (Lines ~470-475)

**Current (Placeholder Text):**
```typescript
<div className="text-2xl font-bold text-gray-400">Stripe</div>
<div className="text-2xl font-bold text-gray-400">Shopify</div>
<div className="text-2xl font-bold text-gray-400">GitHub</div>
<div className="text-2xl font-bold text-gray-400">DataFlow</div>
```

**Bryan Needs to Provide:**

**Option A: Real Company Logos (If You Have Permission)**
- ✅ **Actual company logos** (PNG/SVG files)
- ✅ **Permission to use logos** (written permission required)
- ✅ **Logo files** (high-res, transparent background preferred)

**Option B: Real Company Names (If Logos Not Available)**
- ✅ **Actual company names** (companies actually using AiGuardian)
- ✅ **Permission to use company names**

**Option C: Remove Company Logos (If None Available)**
- Remove company logo section
- Replace with other social proof (user count, GitHub stars, etc.)

**Action:** Replace placeholder logos with real ones OR remove section

---

### 6. SOCIAL PROOF NUMBERS ⚠️ PLACEHOLDER

**Location:** `apps/web/app/webinar/aiguardian/page.tsx` (Line 26)

**Current (Placeholder):**
```typescript
const [registrations, setRegistrations] = useState(1247) // Real-time social proof
```

**Bryan Needs to Provide:**
- ✅ **Actual registration count** (if this is not the first webinar, use real number)
- ✅ **Or start at 0** (if this is the first webinar)

**Action:** Update initial registration count to real number or 0

---

### 7. VIDEO TESTIMONIAL ⚠️ PLACEHOLDER

**Location:** `apps/web/app/webinar/aiguardian/page.tsx` (Lines ~509-520)

**Current (Placeholder):**
```typescript
<div className="text-6xl mb-4">▶️</div>
<h3 className="text-2xl font-bold mb-2">See It In Action</h3>
<p className="text-lux-200 mb-6">
  Watch how engineers at Stripe use AiGuardian to catch bugs before production
</p>
<button>Watch Demo Video →</button>
```

**Bryan Needs to Provide:**

**Option A: Real Demo Video**
- ✅ **Video URL** (YouTube, Vimeo, or hosted video)
- ✅ **Video thumbnail** (if custom)
- ✅ **Video title/description**

**Option B: Remove Video Section (If Not Available)**
- Remove video testimonial placeholder
- Replace with other content

**Action:** Add real video embed OR remove section

---

### 8. EMAIL SIGNATURE ⚠️ PLACEHOLDER

**Location:** `apps/web/app/api/webinar/register/route.ts` (Email template, Line ~340)

**Current (Placeholder):**
```typescript
— Michael
```

**Bryan Needs to Provide:**
- ✅ **Actual signature name**
  - Example: `"Michael Mataluni"` or `"Michael"` or `"The AiGuardian Team"`
- ✅ **Optional: Title/role**
  - Example: `"Michael Mataluni, Founder"` or `"Michael, CTO"`
- ✅ **Optional: Company name**
  - Example: `"Michael Mataluni\nFounder, AiGuardian"`

**Action:** Update email signature in email template

---

### 9. APPLICATION URL ⚠️ PLACEHOLDER

**Location:** `apps/web/app/api/webinar/register/route.ts` (Email template, Line ~360)

**Current (Placeholder):**
```typescript
process.env.NEXT_PUBLIC_APP_URL || 'https://aiguardian.ai'
```

**Bryan Needs to Provide:**
- ✅ **Actual production URL**
  - Example: `https://aiguardian.ai` or `https://www.aiguardian.ai`
  - Must match your actual domain

**Action:** Set `NEXT_PUBLIC_APP_URL` in `.env.local` (production)

---

### 10. UNSUBSCRIBE LINK ⚠️ PLACEHOLDER

**Location:** `apps/web/app/api/webinar/register/route.ts` (Email template, Line ~365)

**Current (Placeholder):**
```typescript
${process.env.NEXT_PUBLIC_APP_URL || 'https://aiguardian.ai'}/unsubscribe?email=${encodeURIComponent(registration.email)}
```

**Bryan Needs to Provide:**
- ✅ **Actual unsubscribe page URL** (if you have one)
- ✅ **Or SendGrid unsubscribe link** (if using SendGrid's built-in unsubscribe)
- ✅ **Or email address** (if manual unsubscribe: `mailto:unsubscribe@aiguardian.ai`)

**Action:** Update unsubscribe link to real page OR implement unsubscribe page

---

## 🟡 IMPORTANT UPDATES (Should Fix Soon)

### 11. LEAD MAGNET DESCRIPTIONS ⚠️ VERIFY ACCURACY

**Location:** `apps/web/app/webinar/aiguardian/page.tsx` (Lines 99-159)

**Current:** Lead magnet descriptions are generic

**Bryan Needs to Verify:**
- ✅ **Lead magnet titles** match actual assets you'll provide
- ✅ **Lead magnet descriptions** accurately describe what attendees will receive
- ✅ **Lead magnet values** ($147, $97, etc.) are reasonable/accurate
- ✅ **Lead magnet delivery** - How will these be delivered? (Email, download link, etc.)

**Action:** Review and update lead magnet descriptions to match actual assets

---

### 12. FAQ ANSWERS ⚠️ VERIFY ACCURACY

**Location:** `apps/web/app/webinar/aiguardian/page.tsx` (Lines ~595-625)

**Current FAQ:**
- "Is this really free?" - Verify this is accurate
- "What if I can't attend live?" - Verify replay policy
- "How long is the webinar?" - Verify duration
- "Will there be a sales pitch?" - Verify your approach
- "Is this for beginners or experts?" - Verify target audience

**Bryan Needs to Verify:**
- ✅ **All FAQ answers are accurate** for your actual webinar
- ✅ **Update any answers** that don't match your plan
- ✅ **Add any missing FAQs** that are common questions

**Action:** Review and update FAQ answers to match your actual webinar plan

---

### 13. HEADLINE VARIATIONS ⚠️ VERIFY ACCURACY

**Location:** `apps/web/app/webinar/aiguardian/page.tsx` (Lines 37-66)

**Current Headlines:**
- "How to Eliminate 90% of AI Code Failures Before Production"
- "The 3-Step Validation System Used by Stripe & Shopify"
- "Join 10,000+ Senior Engineers Who Catch Bugs Before Production"
- "Join 10,000+ Creators Building AI Products That Actually Work"
- "🔥 Only 47 Spots Left - The AI Validation Masterclass"

**Bryan Needs to Verify:**
- ✅ **"90% of AI Code Failures"** - Is this accurate? Do you have data to support?
- ✅ **"Stripe & Shopify"** - Are these real customers? If not, remove or replace
- ✅ **"10,000+ Senior Engineers"** - Is this accurate? Update to real number
- ✅ **"47 Spots Left"** - Is this accurate? Update to real number or remove if not limited

**Action:** Update headlines to reflect accurate numbers/claims OR remove unsupported claims

---

## 🟢 OPTIONAL UPDATES (Nice to Have)

### 14. BRANDING COLORS ⚠️ VERIFY

**Location:** Throughout landing page (using AbëONE design tokens)

**Current:** Using AbëONE design system colors (lux purple, warm orange)

**Bryan Needs to Verify:**
- ✅ **Colors match AiGuardian brand** (if AiGuardian has specific brand colors)
- ✅ **Or confirm** that AbëONE colors are correct for AiGuardian

**Action:** Verify colors match brand OR update if needed

---

### 15. FAVICON/LOGO ⚠️ VERIFY

**Location:** Browser tab, email templates

**Bryan Needs to Provide:**
- ✅ **AiGuardian favicon** (if you have one)
- ✅ **AiGuardian logo** (for email templates, if desired)

**Action:** Add favicon/logo if available

---

## 📧 EMAIL FOLLOW-UP INFORMATION NEEDED

### Email Sequence Details

**Bryan Needs to Provide:**

#### Confirmation Email (Immediate)
- ✅ **Email subject line** (current: "✅ You're Registered: AiGuardian Validation System")
- ✅ **Email content** - Review and customize
- ✅ **Calendar invite details** - Verify timezone, duration, description

#### 24-Hour Reminder Email
- ✅ **Email subject line**
- ✅ **Email content** (what to expect, preparation tips)
- ✅ **Send time** (24 hours before webinar)

#### 3-Hour Reminder Email
- ✅ **Email subject line**
- ✅ **Email content** (quick reminder, join link)
- ✅ **Send time** (3 hours before webinar)

#### 15-Minute Reminder Email
- ✅ **Email subject line**
- ✅ **Email content** (starting soon, join now)
- ✅ **Send time** (15 minutes before webinar)

#### Follow-Up Email (After Webinar)
- ✅ **Email subject line**
- ✅ **Replay link** (where replay will be hosted)
- ✅ **Bonus download links** (how to deliver lead magnets)
- ✅ **Upsell content** (if applicable)
- ✅ **Send time** (immediately after or next day)

---

## 📋 COMPLETE CHECKLIST FOR BRYAN

### Critical (Must Fix Before Launch)

```
□ Webinar date and time (actual)
□ Zoom link (actual join URL)
□ Replay link (where replay will be hosted)
□ Sender email (verified in SendGrid)
□ Sender name (how to appear in emails)
□ Support email (actual contact email)
□ Testimonials (real OR remove section)
□ Company logos (real OR remove section)
□ Registration count (real number or start at 0)
□ Video testimonial (real video OR remove section)
□ Email signature (actual name/title)
□ Application URL (actual production domain)
□ Unsubscribe link (actual unsubscribe page/email)
```

### Important (Should Fix Soon)

```
□ Lead magnet descriptions (verify accuracy)
□ Lead magnet delivery method (how to deliver)
□ FAQ answers (verify accuracy)
□ Headline numbers (verify accuracy - 90%, 10,000+, etc.)
□ Company names in headlines (verify Stripe/Shopify if not real customers)
```

### Optional (Nice to Have)

```
□ Brand colors (verify match)
□ Favicon/logo (add if available)
□ Email sequence content (customize)
□ Reminder email content (customize)
□ Follow-up email content (customize)
```

---

## 🎯 PRIORITY ORDER

### Week 1 (Before Launch)
1. **Webinar details** (date, time, Zoom link) - 🔴 CRITICAL
2. **Email sender info** (from email, from name) - 🔴 CRITICAL
3. **Support email** - 🔴 CRITICAL
4. **Testimonials** (real OR remove) - 🔴 CRITICAL
5. **Company logos** (real OR remove) - 🔴 CRITICAL

### Week 2 (After Launch)
6. **Headline accuracy** (verify numbers/claims)
7. **FAQ answers** (verify accuracy)
8. **Lead magnet descriptions** (verify accuracy)
9. **Email sequence content** (customize)

### Ongoing
10. **Registration count** (update as real registrations come in)
11. **Video testimonial** (add when available)
12. **Branding** (verify colors, add logo)

---

## 📝 TEMPLATE FOR BRYAN

**Copy this template and fill in:**

```markdown
## WEBINAR DETAILS
- Date: [YYYY-MM-DD]
- Time: [HH:MM AM/PM] [TIMEZONE]
- Duration: [XX] minutes
- Zoom Link: [https://zoom.us/j/...]
- Replay Link: [https://...]

## EMAIL INFORMATION
- From Email: [email@domain.com]
- From Name: [Name]
- Support Email: [email@domain.com]
- Signature: [Name/Title]

## TESTIMONIALS
- [ ] Use real testimonials (provide below)
- [ ] Remove testimonial section

If using real testimonials:
Developer 1:
- Name: 
- Role: 
- Company: 
- GitHub: 
- Quote: 

[Repeat for each testimonial]

## COMPANY LOGOS
- [ ] Use real company logos (provide files)
- [ ] Use real company names only
- [ ] Remove company logo section

## SOCIAL PROOF
- Initial Registration Count: [number]
- Video Testimonial: [URL or "Remove"]

## HEADLINES
- "90% of failures" - [ ] Accurate [ ] Update to [X]%
- "Stripe & Shopify" - [ ] Real customers [ ] Remove/Replace
- "10,000+ engineers" - [ ] Accurate [ ] Update to [X]
- "47 spots left" - [ ] Accurate [ ] Remove if not limited

## APPLICATION URL
- Production URL: [https://...]

## UNSUBSCRIBE
- Unsubscribe URL: [https://.../unsubscribe] OR [mailto:...]
```

---

## ✅ COMPLETION STATUS

**Current Status:** ⚠️ **PLACEHOLDER CONTENT DETECTED**

**Files with Placeholders:**
- ✅ `apps/web/app/api/webinar/register/route.ts` - Webinar details, email content
- ✅ `apps/web/app/webinar/aiguardian/page.tsx` - Testimonials, logos, contact info
- ✅ `apps/web/lib/sendgrid.ts` - Email sender defaults
- ✅ `.env.local` - Environment variables (to be created)

**Ready for Launch:** ❌ **NO** (placeholders must be replaced)

---

**Pattern:** Content Update × Truth × Accuracy × ONE  
**Status:** ⚠️ **PENDING BRYAN'S UPDATES**  
**Priority:** 🔴 **CRITICAL** - Must update before launch

**∞ AbëONE Webinar Landing Page × Content Accuracy × ONE ∞**

