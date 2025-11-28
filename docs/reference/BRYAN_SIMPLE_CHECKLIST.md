# 📋 BRYAN - SIMPLE UPDATE CHECKLIST

**What You Need to Do:** Replace placeholder content with real information

**Priority:** 🔴 **CRITICAL** - Must complete before launch

---

## ✅ QUICK CHECKLIST

### 1. Webinar Details
- [ ] **Date:** [Example: February 15, 2025]
- [ ] **Time:** [Example: 2:00 PM EST]
- [ ] **Zoom Link:** [Your actual Zoom meeting URL]
- [ ] **Replay Link:** [Where replay will be hosted]

**Where to Update:** `apps/web/app/api/webinar/register/route.ts` (lines 30-37)

---

### 2. Email Information
- [ ] **From Email:** [Must be verified in SendGrid, e.g., noreply@aiguardian.ai]
- [ ] **From Name:** [How you want to appear, e.g., "Michael from AiGuardian"]
- [ ] **Support Email:** [Email people can contact for help]
- [ ] **Your Signature:** [Your name/title for emails]

**Where to Update:** 
- `apps/web/app/api/webinar/register/route.ts` (line 114-115)
- `apps/web/app/webinar/thank-you/page.tsx` (line ~164)
- `.env.local` file

---

### 3. Testimonials
**Choose ONE:**
- [ ] **Option A:** Provide 3+ real testimonials (with permission)
- [ ] **Option B:** Remove testimonial section

**Where to Update:** `apps/web/app/webinar/aiguardian/page.tsx` (lines 184-234)

**If Option A, provide for each testimonial:**
- Name
- Role/Title
- Company
- GitHub username (for developers) OR Social handle (for creatives)
- Quote (what they said)

---

### 4. Company Logos
**Choose ONE:**
- [ ] **Option A:** Provide real company logo files (with permission)
- [ ] **Option B:** Use real company names only (text)
- [ ] **Option C:** Remove company logo section

**Where to Update:** `apps/web/app/webinar/aiguardian/page.tsx` (lines ~470-475)

---

### 5. Social Proof Numbers
- [ ] **Starting Registration Count:** [Real number or 0 if first webinar]
- [ ] **Video Testimonial:** [URL if you have one, or "Remove"]

**Where to Update:** `apps/web/app/webinar/aiguardian/page.tsx` (line 26, ~517)

---

### 6. Headline Numbers (Verify Accuracy)
- [ ] **"90% of failures"** - Is this accurate? [ ] Yes [ ] No - Update to: ___
- [ ] **"Stripe & Shopify"** - Are these real customers? [ ] Yes [ ] No - [ ] Remove
- [ ] **"10,000+ engineers"** - Is this accurate? [ ] Yes [ ] No - Update to: ___
- [ ] **"47 spots left"** - Is this accurate? [ ] Yes [ ] No - [ ] Remove

**Where to Update:** `apps/web/app/webinar/aiguardian/page.tsx` (lines 37-66)

---

### 7. Application URL
- [ ] **Production Website URL:** [Example: https://aiguardian.ai]

**Where to Update:** `.env.local` file (set `NEXT_PUBLIC_APP_URL`)

---

### 8. Unsubscribe Link
- [ ] **Unsubscribe Page URL:** [Example: https://aiguardian.ai/unsubscribe]
- [ ] **OR:** Use SendGrid's built-in unsubscribe

**Where to Update:** `apps/web/app/api/webinar/register/route.ts` (line ~262)

---

## 📝 FILL THIS OUT AND SEND BACK

```
WEBINAR DETAILS:
Date: _________________________
Time: _________________________
Zoom Link: _________________________
Replay Link: _________________________

EMAIL INFORMATION:
From Email: _________________________
From Name: _________________________
Support Email: _________________________
Signature: _________________________

TESTIMONIALS:
[ ] Use real testimonials (provide below)
[ ] Remove section

COMPANY LOGOS:
[ ] Use real logos (provide files)
[ ] Use real names only
[ ] Remove section

SOCIAL PROOF:
Starting Count: _________________________
Video: [URL] or [Remove]

HEADLINE NUMBERS:
"90%" - [ ] Accurate [ ] Update to: ___
"Stripe/Shopify" - [ ] Real [ ] Remove
"10,000+" - [ ] Accurate [ ] Update to: ___
"47 spots" - [ ] Accurate [ ] Remove

APPLICATION URL:
Production URL: _________________________

UNSUBSCRIBE:
Unsubscribe URL: _________________________
```

---

## 🎯 PRIORITY ORDER

**Do These First (Before Launch):**
1. Webinar details (date, time, Zoom link)
2. Email information (from email, from name, support email)
3. Testimonials (real OR remove)
4. Company logos (real OR remove)

**Do These Next (Week 1):**
5. Social proof numbers
6. Headline accuracy
7. Application URL
8. Unsubscribe link

---

## 📁 FILES TO EDIT

1. **`apps/web/app/api/webinar/register/route.ts`**
   - Webinar details (lines 30-37)
   - Email sender info (lines 114-115)
   - Unsubscribe link (line ~262)

2. **`apps/web/app/webinar/aiguardian/page.tsx`**
   - Testimonials (lines 184-234)
   - Company logos (lines ~470-475)
   - Social proof count (line 26)
   - Headlines (lines 37-66)
   - Video testimonial (lines ~517)

3. **`apps/web/app/webinar/thank-you/page.tsx`**
   - Support email (line ~164)

4. **`.env.local`** (create this file)
   - `SENDGRID_FROM_EMAIL=your-email@domain.com`
   - `SENDGRID_FROM_NAME=Your Name`
   - `NEXT_PUBLIC_APP_URL=https://your-domain.com`

---

## ❓ QUESTIONS?

**If you're not sure about something:**
- Ask before making changes
- It's better to remove placeholder content than use fake information
- We can always add real content later

---

**Status:** ⚠️ **PENDING YOUR UPDATES**  
**Deadline:** Before launch  
**Questions?** Ask AEYON

