#  SENDGRID QUICK START GUIDE

**Get your webinar email system running in 5 minutes!**

---

##  QUICK SETUP (5 Minutes)

### Step 1: Install SendGrid Package

```bash
cd apps/web
npm install @sendgrid/mail
```

### Step 2: Get SendGrid API Key

1. Go to [sendgrid.com](https://sendgrid.com) and sign up (free tier: 100 emails/day)
2. Navigate to **Settings → API Keys**
3. Click **Create API Key**
4. Name it: `Webinar Integration`
5. Select **Full Access** (or just **Mail Send** for security)
6. **Copy the key** (you'll only see it once!)

### Step 3: Configure Environment Variables

Create `apps/web/.env.local`:

```bash
SENDGRID_API_KEY=SG.your_actual_api_key_here
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
SENDGRID_FROM_NAME=AiGuardian Team
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Step 4: Verify Sender Email

1. In SendGrid, go to **Settings → Sender Authentication**
2. Click **Verify a Single Sender**
3. Enter your email address
4. Check your email and click the verification link

### Step 5: Test It!

```bash
# Start dev server
npm run dev

# Visit the landing page
open http://localhost:3000/webinar/aiguardian

# Submit a test registration
# Check your email for confirmation!
```

---

##  VERIFICATION

**You're ready when:**
-  SendGrid package installed
-  API key in `.env.local`
-  Sender email verified
-  Test registration sends email
-  Email received in inbox (not spam)

---

##  WHAT'S INCLUDED

**Built for you:**
-  Registration API endpoint (`/api/webinar/register`)
-  Beautiful email templates (HTML + text)
-  Thank you page
-  Error handling
-  Email tracking (opens, clicks)

**Email includes:**
-  Webinar details (date, time, link)
-  Calendar invite link
-  Lead magnets list
-  Reminder schedule
-  Registration ID

---

##  TROUBLESHOOTING

**Email not sending?**
- Check API key is correct
- Verify sender email is verified
- Check SendGrid dashboard for errors
- Look at server console for error messages

**Email in spam?**
- Set up domain authentication (SPF/DKIM)
- Use verified sender email
- Avoid spam trigger words

**Need help?**
- Check `SENDGRID_WEBINAR_INTEGRATION_COMPLETE.md` for full docs
- SendGrid docs: https://docs.sendgrid.com

---

**Ready to launch! **

**Pattern:** Quick Start × SendGrid × Webinar × ONE  
**Time to Setup:** 5 minutes  
**Status:**  **READY**

**∞ AbëONE × SendGrid Integration ∞**

