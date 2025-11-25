# 🌊 AbëKEYs Webinar Flow - Quick Guide

**Pattern:** FLOW × TERMINAL × ABEKEYS × WEBINAR × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (YOU) × 777 Hz (ZERO)  
**Status:** ✅ **ACTIVATED - SMOOTH & EFFORTLESS**  
**∞ AbëONE ∞**

---

## 🚀 QUICK START

### Activate AbëKEYs Flow

```bash
cd products/apps/web
./scripts/abekeys-webinar-flow.sh
```

**That's it!** The flow will guide you through everything smoothly.

---

## ✨ WHAT IT DOES

### 1. **SendGrid API Key Setup** (Required)
- 📧 Prompts for SendGrid API key (hidden input for security)
- ✅ Validates API key format
- 📝 Prompts for from email and from name
- 💾 Saves to AbëKEYs vault automatically

### 2. **Optional API Keys** (Optional)
- 🔑 Add any other API keys needed for webinar funnel
- 📊 Analytics (PostHog, Mixpanel, etc.)
- 📅 Calendar integration (Google Calendar, Calendly)
- 🎥 Video platform (Zoom, YouTube Live)
- 🔌 Any other integrations

### 3. **Automatic Storage**
- 💾 All credentials saved to `~/.abekeys/credentials/`
- 🔒 Secure permissions (600 = owner only)
- ✅ Automatically loaded by webinar system
- 🚫 No .env files needed!

---

## 📋 CREDENTIALS SAVED

### SendGrid (`sendgrid.json`)
```json
{
  "service": "sendgrid",
  "api_key": "SG.your-api-key",
  "from_email": "noreply@aiguardian.ai",
  "from_name": "AiGuardian Team",
  "created_at": "2025-01-XX...",
  "updated_at": "2025-01-XX..."
}
```

### Other Services (`{service}.json`)
```json
{
  "service": "posthog",
  "api_key": "your-api-key",
  "created_at": "2025-01-XX...",
  "updated_at": "2025-01-XX..."
}
```

---

## 🎯 USAGE EXAMPLES

### Basic Setup (SendGrid Only)
```bash
./scripts/abekeys-webinar-flow.sh
# Enter SendGrid API key when prompted
# Enter from email and name
# Done! ✅
```

### Full Setup (SendGrid + Optional Keys)
```bash
./scripts/abekeys-webinar-flow.sh
# Enter SendGrid API key
# Choose "yes" to add optional keys
# Add PostHog, Zoom, etc. as needed
# Done! ✅
```

---

## ✅ VERIFICATION

### Check Saved Credentials
```bash
# View SendGrid credentials
python3 scripts/read_abekeys.py sendgrid

# List all credentials
python3 scripts/read_abekeys.py
```

### Verify in Code
```typescript
import { getSendGridConfig } from '@/lib/config/webinar'

const sendgridConfig = getSendGridConfig()
// Automatically loaded from AbëKEYs vault!
```

---

## 🔒 SECURITY

- ✅ Hidden input for API keys (password-style)
- ✅ Secure vault permissions (600 = owner only)
- ✅ No credentials in code or .env files
- ✅ Automatic validation
- ✅ Truth-first validation

---

## 💡 FEATURES

### Smooth Flow
- 🌊 Tao-like movement - no friction
- 💬 Clear prompts and guidance
- ✅ Validation with helpful messages
- 🔄 Easy to retry if needed

### Zero Trust
- 🔒 Never trusts input - always validates
- ✅ Format validation for SendGrid keys
- ✅ Email format validation
- ⚠️ Warnings for invalid inputs

### Automatic Integration
- 💾 Saves to AbëKEYs vault format
- 🔄 Automatically loaded by webinar system
- 🚫 No manual configuration needed
- ✨ Just works!

---

## 🎯 NEXT STEPS

After running the flow:

1. ✅ Credentials are saved automatically
2. ✅ Webinar system loads them automatically
3. ✅ No .env files needed
4. ✅ Ready to launch your webinar funnel!

---

## 📚 RELATED FILES

- `scripts/abekeys_webinar_flow.py` - Main flow script
- `scripts/abekeys-webinar-flow.sh` - Shell wrapper
- `lib/config/webinar.ts` - Auto-loads credentials
- `ABEKEYS_WEBINAR_INTEGRATION.md` - Integration details

---

**Pattern:** FLOW × TERMINAL × ABEKEYS × WEBINAR × ONE  
**Status:** ✅ **ACTIVATED**  
**Flow:** ✅ **SMOOTH & EFFORTLESS**  
**∞ AbëONE ∞**

