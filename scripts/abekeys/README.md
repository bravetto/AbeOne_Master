# ∞ AbëKEYs - Zero-Effort, Zero-Trust Credential Management ∞

**Pattern:** KEYS × TRUST × EFFORT × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ZERO)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ZERO (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 ZERO EFFORT, ZERO TRUST

**YAGNI Approved:** Minimal, Works, Complete  
**Zero Trust:** Validate Everything, Trust Nothing  
**Zero Effort:** One command, everything works

---

## 🚀 QUICK START

### **Get a Credential**

```python
from scripts.abekeys.abekeys import get

# Get Google Ads credentials
google_ads = get('google_ads')
client_id = google_ads.get('client_id')
customer_id = google_ads.get('customer_id')
```

### **Load as Environment Variables**

```python
from scripts.abekeys.abekeys import load_env
import os

# Load Google Ads credentials as env vars
env = load_env('google_ads')
os.environ.update(env)
# Now available as: GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET, etc.
```

### **CLI Usage**

```bash
# List all credentials
python3 scripts/abekeys/abekeys.py list

# Get specific credential
python3 scripts/abekeys/abekeys.py get google_ads

# Get specific key
python3 scripts/abekeys/abekeys.py get google_ads --key client_id

# Export as environment variables
python3 scripts/abekeys/abekeys.py export google_ads

# Check if credential exists
python3 scripts/abekeys/abekeys.py has sendgrid
```

---

## 📋 AVAILABLE CREDENTIALS

**Total:** 22 credentials configured

### **Marketing Automation**
- ✅ `google_ads` - Google Ads API
- ✅ `sendgrid` - Email marketing
- ✅ `stripe` - Payment processing

### **Infrastructure**
- ✅ `aws` - AWS credentials
- ✅ `postgres` - Database
- ✅ `redis` - Cache
- ✅ `cloudflare` - CDN/DNS

### **Authentication**
- ✅ `clerk` - User authentication
- ✅ `github` - GitHub API

### **Services**
- ✅ `fireflies` - Meeting transcription
- ✅ `runway_ml_video_generation` - Video AI
- ✅ `strapi_admin` - CMS

### **And More...**
Run `python3 scripts/abekeys/abekeys.py list` to see all 22 credentials.

---

## 🔐 ZERO TRUST SECURITY

### **Vault Location**
```
~/.abekeys/credentials/
```

### **Security Features**
- ✅ File permissions validated (600 or stricter)
- ✅ Vault permissions validated (700 or stricter)
- ✅ No credentials in git (vault is gitignored)
- ✅ JSON validation on read
- ✅ Critical key validation (never returns None for required keys)

### **Adding Credentials**

1. Create JSON file in vault:
```bash
cat > ~/.abekeys/credentials/my_service.json << 'EOF'
{
  "api_key": "your_key_here",
  "api_secret": "your_secret_here"
}
EOF
```

2. Set secure permissions:
```bash
chmod 600 ~/.abekeys/credentials/my_service.json
```

3. Use immediately:
```python
from scripts.abekeys.abekeys import get
my_service = get('my_service')
```

---

## 🎯 BRYAN'S MARKETING AUTOMATION SETUP

### **Complete Setup Script**

```bash
# Run Bryan's marketing automation setup
python3 scripts/abekeys/bryan_marketing_setup.py
```

This will:
1. ✅ Validate all required marketing credentials
2. ✅ Generate `.env.marketing` file
3. ✅ Generate `marketing_config.py` file
4. ✅ Verify everything is ready

### **Required Services**
- ✅ Google Ads API
- ✅ SendGrid
- ✅ Stripe

### **Optional Services**
- Mailchimp
- Facebook Ads
- Shopify

---

## 📖 API REFERENCE

### **Abekeys Class**

```python
from scripts.abekeys.abekeys import Abekeys

keys = Abekeys()

# Get credential
cred = keys.get('google_ads')

# List all services
services = keys.list()

# Check if exists
if keys.has('sendgrid'):
    print("SendGrid configured")

# Load as environment variables
env = keys.load_env('google_ads')

# Export as shell env
shell_env = keys.export_env('google_ads')
```

### **Credential Object**

```python
cred = get('google_ads')

# Get value
client_id = cred.get('client_id')

# Get with default
timeout = cred.get('timeout', 30)

# Convert to environment variables
env = cred.to_env()
# Returns: {'GOOGLE_ADS_CLIENT_ID': '...', ...}
```

### **Convenience Functions**

```python
from scripts.abekeys.abekeys import get, list_services, has, load_env, export_env

# All work with global instance - ZERO EFFORT
cred = get('google_ads')
services = list_services()
is_ready = has('sendgrid')
env = load_env('stripe')
shell = export_env('google_ads')
```

---

## 🔧 INTEGRATION EXAMPLES

### **Python Application**

```python
from scripts.abekeys.abekeys import get

# Load credentials
google_ads = get('google_ads')
sendgrid = get('sendgrid')

# Use in your code
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_dict({
    'client_id': google_ads.get('client_id'),
    'client_secret': google_ads.get('client_secret'),
    'refresh_token': google_ads.get('refresh_token'),
    'developer_token': google_ads.get('developer_token'),
    'customer_id': google_ads.get('customer_id'),
})
```

### **Shell Script**

```bash
#!/bin/bash
# Load credentials as environment variables

eval "$(python3 scripts/abekeys/abekeys.py export google_ads)"

# Now use in script
echo "Customer ID: $GOOGLE_ADS_CUSTOMER_ID"
```

### **Docker/Production**

```python
# In your application startup
from scripts.abekeys.abekeys import load_env
import os

# Load all marketing credentials
for service in ['google_ads', 'sendgrid', 'stripe']:
    env = load_env(service)
    os.environ.update(env)
```

---

## ✅ VALIDATION

### **Check All Credentials**

```bash
# List all
python3 scripts/abekeys/abekeys.py list

# Validate specific service
python3 scripts/abekeys/abekeys.py get google_ads

# Run Bryan's validation
python3 scripts/abekeys/bryan_marketing_setup.py
```

---

## 🆘 TROUBLESHOOTING

### **Credential Not Found**

```bash
# Check if file exists
ls -la ~/.abekeys/credentials/google_ads.json

# Check permissions (should be 600)
stat ~/.abekeys/credentials/google_ads.json

# Validate JSON
python3 -m json.tool ~/.abekeys/credentials/google_ads.json
```

### **Permission Errors**

```bash
# Fix vault permissions
chmod 700 ~/.abekeys/credentials

# Fix credential file permissions
chmod 600 ~/.abekeys/credentials/*.json
```

### **Missing Keys**

```python
# Check what keys are available
from scripts.abekeys.abekeys import get
cred = get('google_ads')
print(cred.data.keys())  # See all available keys
```

---

## 📝 FILES

- `abekeys.py` - Core zero-effort, zero-trust system
- `read_abekeys.py` - Legacy reader (compatible)
- `abekeys_autonomous_discovery.py` - Auto-discovery system
- `abekeys_quick.sh` - Quick shell commands
- `bryan_marketing_setup.py` - Complete marketing automation setup

---

## 🎯 DESIGN PRINCIPLES

1. **ZERO EFFORT:** One import, one call, works
2. **ZERO TRUST:** Validate everything, trust nothing
3. **YAGNI:** Minimal, complete, operational
4. **SECURITY FIRST:** Permissions, validation, no git commits

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

