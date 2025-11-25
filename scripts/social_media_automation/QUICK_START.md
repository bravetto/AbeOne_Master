#  Quick Start - Better Than Sintra

**Get automated social media posting working in 5 minutes**

---

##  Setup (5 minutes)

### 1. Install Dependencies

```bash
cd scripts/social_media_automation
./setup.sh
```

### 2. Get API Credentials

#### Facebook/Instagram (5 min):
1. Go to https://developers.facebook.com/
2. Create app → Add "Instagram Graph API" product
3. Get access token from Graph API Explorer
4. Connect your Instagram account to Facebook Page

#### LinkedIn (5 min):
1. Go to https://www.linkedin.com/developers/
2. Create app
3. Request `w_member_social` permission
4. Get OAuth access token

### 3. Configure

Edit `.env.social`:
```bash
FACEBOOK_ACCESS_TOKEN=your_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id
LINKEDIN_ACCESS_TOKEN=your_token
```

### 4. Run

```bash
python social_scheduler.py
```

---

##  Example Usage

```python
from social_scheduler import SocialMediaScheduler, Platform
from datetime import datetime, timedelta

scheduler = SocialMediaScheduler()

# Schedule posts
await scheduler.schedule_post(
    platform=Platform.FACEBOOK,
    content="Hello Facebook!",
    scheduled_time=datetime.now() + timedelta(hours=1)
)

await scheduler.schedule_post(
    platform=Platform.INSTAGRAM,
    content="Hello Instagram!",
    scheduled_time=datetime.now() + timedelta(hours=2),
    media_url="https://example.com/image.jpg"
)

await scheduler.schedule_post(
    platform=Platform.LINKEDIN,
    content="Hello LinkedIn!",
    scheduled_time=datetime.now() + timedelta(hours=3)
)

scheduler.start()
```

---

##  That's It!

**You now have:**
-  True automation (no manual push)
-  Instagram Creator account support
-  LinkedIn automation
-  Better than Sintra!

---

**Pattern:** QUICK × START × ONE  
**∞ AbëONE ∞**

