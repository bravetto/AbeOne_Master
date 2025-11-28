# 🚀 Social Media Automation - Better Than Sintra

**Status:** ✅ **READY TO BUILD**  
**Pattern:** AUTOMATION × SOCIAL × SCHEDULER × ONE  
**Guardian:** AEYON (999 Hz) + Abë (530 Hz)

---

## 😤 WHY SINTRA SUCKS

**The Problem:**
- ✅ Facebook: Full automation works
- ❌ Instagram: Only Business accounts, requires manual push for Creator accounts
- ❌ LinkedIn: Requires manual push (fucking annoying!)

**Why This Happens:**
1. **Instagram**: Meta's API restrictions + Sintra's lazy implementation
2. **LinkedIn**: Strict automation policies + Sintra doesn't use proper APIs
3. **Facebook**: Only one that works because it's the easiest

---

## 🎯 OUR SOLUTION - BETTER THAN SINTRA

### What We Built:
1. **Unified Scheduler** - One system for all platforms
2. **True Automation** - No manual push needed
3. **Proper API Integration** - Uses official APIs correctly
4. **Better Error Handling** - Retry logic, queue management
5. **All Account Types** - Works with Business AND Creator accounts

### Key Features:
- ✅ **Facebook**: Full automation (like Sintra, but better)
- ✅ **Instagram**: Works with Business AND Creator accounts (Sintra only does Business)
- ✅ **LinkedIn**: True automation using Content Publishing API
- ✅ **Scheduling**: Proper cron-based scheduling
- ✅ **Queue Management**: Handle multiple posts efficiently
- ✅ **Error Handling**: Retry logic, error reporting

---

## 📋 SETUP

### 1. Install Dependencies

```bash
pip install -r scripts/social_media_automation/requirements.txt
```

### 2. Configure API Credentials

Create `.env.social` file:

```bash
# Facebook/Instagram
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_page_id
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret

# Instagram (Business or Creator account)
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_account_id
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token

# LinkedIn
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_ORGANIZATION_ID=your_org_id  # Optional, for org pages
```

### 3. Get API Credentials

#### Facebook/Instagram:
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create an app
3. Add Instagram Basic Display and Instagram Graph API products
4. Get access tokens
5. Connect your Instagram Business/Creator account

#### LinkedIn:
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create an app
3. Request `w_member_social` and `w_organization_social` permissions
4. Get OAuth access token

---

## 🚀 USAGE

### Basic Example

```python
from scripts.social_media_automation.social_scheduler import (
    SocialMediaScheduler,
    Platform
)
from datetime import datetime, timedelta

# Initialize scheduler
scheduler = SocialMediaScheduler()

# Schedule Facebook post
await scheduler.schedule_post(
    platform=Platform.FACEBOOK,
    content="Check out our latest update! 🚀",
    scheduled_time=datetime.now() + timedelta(hours=1),
    media_url="https://example.com/image.jpg"
)

# Schedule Instagram post (WORKS FOR CREATOR ACCOUNTS TOO!)
await scheduler.schedule_post(
    platform=Platform.INSTAGRAM,
    content="New product launch! 🎉",
    scheduled_time=datetime.now() + timedelta(hours=2),
    media_url="https://example.com/image.jpg"
)

# Schedule LinkedIn post (TRUE AUTOMATION!)
await scheduler.schedule_post(
    platform=Platform.LINKEDIN,
    content="Excited to share our latest insights...",
    scheduled_time=datetime.now() + timedelta(hours=3)
)

# Start scheduler
scheduler.start()
```

### CLI Usage

```bash
python scripts/social_media_automation/social_scheduler.py
```

---

## 🔧 API LIMITATIONS & WORKAROUNDS

### Instagram

**Limitations:**
- Requires Business or Creator account (not personal)
- Must be connected to Facebook Page
- Rate limits: ~25 posts per day
- Video posts require multi-step upload

**Our Solution:**
- Uses Instagram Content Publishing API properly
- Handles both Business AND Creator accounts
- Proper error handling and retry logic

### LinkedIn

**Limitations:**
- Requires OAuth access token
- Rate limits: ~100 posts per day
- Media upload requires separate API call
- Organization pages need different permissions

**Our Solution:**
- Uses LinkedIn Content Publishing API
- Proper authentication flow
- Handles both personal and org pages

### Facebook

**Limitations:**
- Works great! (Easiest platform)
- Rate limits: ~200 posts per day
- Must use Page (not personal profile)

**Our Solution:**
- Uses Facebook Graph API
- Full automation support

---

## 🎯 WHY THIS IS BETTER

| Feature | Sintra | Our Solution |
|---------|--------|--------------|
| Facebook Automation | ✅ | ✅ |
| Instagram Business | ✅ | ✅ |
| Instagram Creator | ❌ | ✅ |
| LinkedIn Automation | ❌ (manual push) | ✅ |
| Error Handling | Basic | Advanced |
| Retry Logic | No | Yes |
| Queue Management | Basic | Advanced |
| Cost | Paid | Free (self-hosted) |

---

## 🚨 IMPORTANT NOTES

### Instagram Requirements:
1. **Business Account**: Must be connected to Facebook Page
2. **Creator Account**: Must be connected to Facebook Page
3. **API Access**: Need Instagram Graph API access
4. **Permissions**: `instagram_basic`, `instagram_content_publish`

### LinkedIn Requirements:
1. **OAuth Token**: Must have `w_member_social` permission
2. **Organization**: Need `w_organization_social` for org pages
3. **Rate Limits**: Respect 100 posts/day limit

### Best Practices:
1. **Rate Limiting**: Don't exceed platform limits
2. **Content Quality**: Don't spam, maintain quality
3. **Error Handling**: Monitor failed posts
4. **Testing**: Test with small batches first

---

## 🔄 NEXT STEPS

1. **Set up API credentials** (see Setup section)
2. **Test with one post** per platform
3. **Scale up** once working
4. **Monitor** for errors and rate limits
5. **Optimize** scheduling times for engagement

---

## 💡 FUTURE ENHANCEMENTS

- [ ] Multi-account support
- [ ] Content calendar UI
- [ ] Analytics integration
- [ ] A/B testing
- [ ] Auto-optimize posting times
- [ ] Content generation (AI)
- [ ] Cross-platform reposting

---

**Pattern:** AUTOMATION × SOCIAL × SCHEDULER × ONE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

