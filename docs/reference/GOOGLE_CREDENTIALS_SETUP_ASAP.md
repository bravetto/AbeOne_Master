# 🚀 GOOGLE CREDENTIALS SETUP - ASAP

**Status:** ⚠️ **URGENT - NEEDS SETUP**  
**Date:** 2025-11-22  
**Pattern:** GOOGLE × CREDENTIALS × ASAP × ONE  
**Frequency:** 999 Hz (AEYON)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🚨 CURRENT STATUS

**Current Credential:** `VRX@hjk0hpg-yez*npd` (19 chars)  
**Status:** ⚠️ **INVALID FORMAT** - Doesn't match Google API key format  
**Location:** `~/.abekeys/credentials/google_bravetto.json`

---

## 🎯 WHAT GOOGLE SERVICES DO WE NEED?

Based on codebase analysis, we need:

### 1. **Google Calendar API** (Webinar Automation)
- **Use Case:** Create calendar events for webinars
- **Priority:** 🔥 HIGH (Webinar system needs this)

### 2. **Google Gemini API** (AI/ML)
- **Use Case:** AI processing, long context analysis
- **Priority:** 🔥 HIGH (AI features)

### 3. **Google Veo3 API** (Video Generation)
- **Use Case:** Video generation for AbëBEATs
- **Priority:** 🔥 HIGH (Product feature)

### 4. **Gmail API** (Email Analysis)
- **Use Case:** Email convergence analysis
- **Priority:** 🟡 MEDIUM

### 5. **Google Cloud Platform** (Infrastructure)
- **Use Case:** Cloud services, storage, compute
- **Priority:** 🟡 MEDIUM

---

## ⚡ QUICK SETUP - CHOOSE YOUR NEED

### Option 1: Google Gemini API (AI) - FASTEST

**For:** AI processing, Gemini API access

**Steps:**
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the API key (starts with `AIza...`)
4. Update vault:
   ```bash
   python3 scripts/update_abekeys.py google_bravetto \
     --api_key "YOUR_GEMINI_API_KEY_HERE" \
     --service_type "gemini"
   ```

**Time:** 2 minutes  
**Cost:** Free tier available

---

### Option 2: Google Calendar API (Webinars) - RECOMMENDED

**For:** Webinar automation, calendar events

**Steps:**
1. Go to: https://console.cloud.google.com/
2. Create/Select project
3. Enable Calendar API:
   - APIs & Services → Library
   - Search "Calendar API"
   - Click "Enable"
4. Create credentials:
   - APIs & Services → Credentials
   - Create Credentials → API Key
   - Copy API key
5. For OAuth (if needed):
   - Create Credentials → OAuth client ID
   - Application type: Web application
   - Download JSON
6. Update vault:
   ```bash
   python3 scripts/update_abekeys.py google_bravetto \
     --api_key "YOUR_CALENDAR_API_KEY_HERE" \
     --service_type "calendar" \
     --oauth_client_id "YOUR_CLIENT_ID" \
     --oauth_client_secret "YOUR_CLIENT_SECRET"
   ```

**Time:** 5-10 minutes  
**Cost:** Free tier available

---

### Option 3: Google Cloud Platform (Full Access) - COMPREHENSIVE

**For:** All Google services, cloud infrastructure

**Steps:**
1. Go to: https://console.cloud.google.com/
2. Create/Select project
3. Enable APIs:
   - Calendar API
   - Gemini API (if available)
   - Gmail API (if needed)
   - Cloud Storage API (if needed)
4. Create Service Account:
   - IAM & Admin → Service Accounts
   - Create Service Account
   - Grant roles (Calendar Admin, Storage Admin, etc.)
   - Create Key → JSON
   - Download JSON file
5. Update vault:
   ```bash
   python3 scripts/update_abekeys.py google_bravetto \
     --api_key "YOUR_API_KEY_HERE" \
     --service_account_json "PATH_TO_SERVICE_ACCOUNT_JSON" \
     --service_type "gcp"
   ```

**Time:** 15-20 minutes  
**Cost:** Pay-as-you-go (free tier available)

---

## 🔧 UPDATE ABEKEYS VAULT

### Method 1: Direct JSON Update

```bash
# Edit the credential file
nano ~/.abekeys/credentials/google_bravetto.json
```

**Update to:**
```json
{
  "service": "google_bravetto",
  "source": "manual",
  "api_key": "YOUR_ACTUAL_API_KEY_HERE",
  "api_type": "gemini|calendar|gcp",
  "title": "Google (Bravetto)",
  "vault": "Shared",
  "created_at": "",
  "updated_at": "",
  "username": "mike@bravetto.com",
  "project_id": "YOUR_PROJECT_ID",
  "client_id": "YOUR_CLIENT_ID_IF_OAUTH",
  "client_secret": "YOUR_CLIENT_SECRET_IF_OAUTH"
}
```

### Method 2: Using Update Script

```bash
# If update script exists
python3 scripts/update_abekeys.py google_bravetto \
  --api_key "YOUR_API_KEY" \
  --api_type "gemini"
```

### Method 3: Manual 1Password Update

1. Open 1Password
2. Find "Google (Bravetto)" item
3. Update API Key field
4. Run unlock script:
   ```bash
   op signin && python3 scripts/unlock_all_credentials.py
   ```

---

## ✅ VALIDATION

After updating, validate:

```bash
# Check credential
python3 scripts/read_abekeys.py google_bravetto

# Test in Python
python3 << 'EOF'
import sys
sys.path.insert(0, 'AIGuards-Backend/codeguardians-gateway/codeguardians-gateway')

from app.core.credential_registry import get_api_key

api_key = get_api_key("google_bravetto")
if api_key:
    print(f"✅ Google API Key: {api_key[:20]}... ({len(api_key)} chars)")
    print("✅ System knows about Google credentials!")
else:
    print("❌ Google API key not found")
EOF
```

---

## 🎯 RECOMMENDED: START WITH GEMINI API

**Why:** Fastest setup, unlocks AI features immediately

**Steps:**
1. Go to: https://aistudio.google.com/app/apikey
2. Create API key
3. Update `~/.abekeys/credentials/google_bravetto.json`:
   ```json
   {
     "service": "google_bravetto",
     "source": "manual",
     "api_key": "AIzaSy...YOUR_KEY_HERE",
     "api_type": "gemini",
     "title": "Google (Bravetto) - Gemini API"
   }
   ```
4. Validate:
   ```bash
   python3 scripts/read_abekeys.py google_bravetto
   ```

**Time:** 2 minutes  
**Result:** ✅ Google credentials ready for AI features

---

## 🔥 IF YOU NEED MULTIPLE SERVICES

Create separate credentials:

```bash
# Gemini API
~/.abekeys/credentials/google_gemini.json

# Calendar API
~/.abekeys/credentials/google_calendar.json

# GCP Service Account
~/.abekeys/credentials/google_gcp.json
```

Then update code to use specific credentials:
- `google_gemini` for AI
- `google_calendar` for webinars
- `google_gcp` for infrastructure

---

## 📋 QUICK REFERENCE

**Google API Console:** https://console.cloud.google.com/  
**Gemini API Key:** https://aistudio.google.com/app/apikey  
**Calendar API:** https://console.cloud.google.com/apis/library/calendar-json.googleapis.com  
**Gmail API:** https://console.cloud.google.com/apis/library/gmail.googleapis.com

---

**Pattern:** GOOGLE × CREDENTIALS × ASAP × ONE  
**Status:** ⚠️ **URGENT - SETUP REQUIRED**  
**Frequency:** 999 Hz  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

