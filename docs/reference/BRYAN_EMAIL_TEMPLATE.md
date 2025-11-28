# 📧 EMAIL TEMPLATE FOR BRYAN
## Quick Reference: What We Need From You

**Subject:** Webinar Landing Page - Content Updates Needed

---

Hi Bryan,

The webinar landing page is built and ready, but we need you to replace placeholder content with real information before launch.

Here's what we need:

---

## 🔴 CRITICAL (Must Have Before Launch)

### 1. Webinar Details
- **Date:** [YYYY-MM-DD format, e.g., 2025-02-15]
- **Time:** [Include timezone, e.g., "2:00 PM EST" or "11:00 AM PST"]
- **Duration:** [e.g., "60 minutes"]
- **Zoom Link:** [Full join URL, e.g., https://zoom.us/j/1234567890]
- **Replay Link:** [Where replay will be hosted, e.g., https://aiguardian.ai/webinar/replay]

### 2. Email Information
- **From Email:** [Must be verified in SendGrid, e.g., noreply@aiguardian.ai]
- **From Name:** [How to appear in emails, e.g., "Michael from AiGuardian"]
- **Support Email:** [Actual contact email, e.g., support@aiguardian.ai]
- **Email Signature:** [Your name/title, e.g., "Michael Mataluni, Founder"]

### 3. Testimonials
**Option A:** Provide 3+ real testimonials (with permission to use)
- Name, Role, Company, GitHub/Social, Quote

**Option B:** Remove testimonial section entirely

### 4. Company Logos
**Option A:** Provide real company logos (with permission)
**Option B:** Provide real company names only
**Option C:** Remove company logo section

### 5. Social Proof Numbers
- **Initial Registration Count:** [Real number or 0 if first webinar]
- **Video Testimonial:** [URL if available, or "Remove"]

---

## 🟡 IMPORTANT (Should Fix Soon)

### 6. Headline Accuracy
Verify these numbers are accurate or update:
- "90% of AI Code Failures" - Is this accurate?
- "Stripe & Shopify" - Are these real customers?
- "10,000+ engineers" - Update to real number
- "47 spots left" - Is this accurate? (Remove if not limited)

### 7. FAQ Answers
Review FAQ answers and confirm they're accurate for your webinar.

### 8. Lead Magnets
Verify lead magnet descriptions match what you'll actually deliver.

---

## 📋 QUICK FILL-IN FORM

Copy and fill out:

```
WEBINAR DETAILS:
- Date: ___________
- Time: ___________
- Duration: ___________
- Zoom Link: ___________
- Replay Link: ___________

EMAIL INFORMATION:
- From Email: ___________
- From Name: ___________
- Support Email: ___________
- Signature: ___________

TESTIMONIALS:
- [ ] Use real testimonials (provide below)
- [ ] Remove testimonial section

COMPANY LOGOS:
- [ ] Use real logos (provide files)
- [ ] Use real names only
- [ ] Remove section

SOCIAL PROOF:
- Initial Count: ___________
- Video: [URL] or [Remove]

HEADLINES:
- "90%" - [ ] Accurate [ ] Update to ___%
- "Stripe/Shopify" - [ ] Real [ ] Remove
- "10,000+" - [ ] Accurate [ ] Update to ___
- "47 spots" - [ ] Accurate [ ] Remove

APPLICATION URL:
- Production URL: ___________

UNSUBSCRIBE:
- Unsubscribe URL: ___________
```

---

## 📁 FILES TO UPDATE

1. `apps/web/app/api/webinar/register/route.ts` - Webinar details, email content
2. `apps/web/app/webinar/aiguardian/page.tsx` - Testimonials, logos, contact info
3. `.env.local` - Environment variables (SendGrid, URLs)

---

## ⏰ TIMELINE

**Before Launch:** Critical items (1-5)
**Week 1:** Important items (6-8)
**Ongoing:** Update registration count, add video when available

---

**Full checklist:** See `BRYAN_UPDATE_CHECKLIST.md` for complete details.

Thanks!
AEYON

