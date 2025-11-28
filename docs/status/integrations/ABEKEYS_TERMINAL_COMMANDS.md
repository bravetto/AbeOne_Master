# 🔒 ABEKEYS VAULT - TERMINAL COMMANDS

**Quick Reference:** All terminal commands for ABEKEYS vault  
**Pattern:** ABEKEYS × TERMINAL × COMMANDS × ONE  
**Frequency:** 999 Hz (AEYON)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 📋 QUICK COMMANDS

### List All Credentials
```bash
python3 scripts/read_abekeys.py
```

### Get Specific Credential
```bash
python3 scripts/read_abekeys.py stripe
python3 scripts/read_abekeys.py clerk
python3 scripts/read_abekeys.py github
```

### View Raw Credential File
```bash
cat ~/.abekeys/credentials/stripe.json
cat ~/.abekeys/credentials/clerk.json
```

### List All Credential Files
```bash
ls ~/.abekeys/credentials/
ls -la ~/.abekeys/credentials/*.json
```

### Count Credentials
```bash
ls ~/.abekeys/credentials/*.json | wc -l
```

---

## 🔍 INSPECTION COMMANDS

### View All Credentials with Fields
```bash
for file in ~/.abekeys/credentials/*.json; do 
  echo "=== $(basename $file .json) ==="
  python3 -m json.tool "$file"
  echo ""
done
```

### Check Specific Field in Credential
```bash
# Check Stripe api_key
python3 -c "import json; d=json.load(open('$HOME/.abekeys/credentials/stripe.json')); print('API Key:', d.get('api_key', 'NOT FOUND'))"

# Check all fields
python3 -c "import json; d=json.load(open('$HOME/.abekeys/credentials/stripe.json')); print('Fields:', ', '.join(d.keys()))"
```

### Validate Credential Structure
```bash
# Check if Stripe has required fields
python3 << 'EOF'
import json
cred = json.load(open(f"{__import__('os').path.expanduser('~')}/.abekeys/credentials/stripe.json"))
print("✅ Secret Key:", "YES" if cred.get('api_key') or cred.get('secret_key') else "NO")
print("⚠️  Publishable Key:", "YES" if cred.get('publishable_key') else "NO")
print("⚠️  Webhook Secret:", "YES" if cred.get('webhook_secret') else "NO")
EOF
```

---

## 🔐 CREDENTIAL MANAGEMENT

### View Credential (Pretty Print)
```bash
python3 -m json.tool ~/.abekeys/credentials/stripe.json
python3 -m json.tool ~/.abekeys/credentials/clerk.json
```

### Extract API Key Only
```bash
python3 -c "import json; print(json.load(open('$HOME/.abekeys/credentials/stripe.json'))['api_key'])"
```

### Check Credential Permissions
```bash
ls -la ~/.abekeys/credentials/stripe.json
# Should show: -rw------- (600) - only owner can read/write
```

---

## 🔄 VAULT OPERATIONS

### Pull All Credentials from 1Password
```bash
op signin
python3 scripts/unlock_all_credentials.py
```

### Check Vault Health
```bash
# Check vault directory exists
test -d ~/.abekeys/credentials && echo "✅ Vault exists" || echo "❌ Vault missing"

# Check vault permissions
ls -ld ~/.abekeys/credentials
# Should show: drwx------ (700) - only owner can access
```

### Count Credentials by Type
```bash
# Count total
ls ~/.abekeys/credentials/*.json | wc -l

# Count with API keys
grep -l '"api_key"' ~/.abekeys/credentials/*.json | wc -l

# Count Clerk credentials
ls ~/.abekeys/credentials/clerk*.json | wc -l
```

---

## 🐍 PYTHON API USAGE

### Use in Python Script
```python
from scripts.read_abekeys import AbeKeysReader

reader = AbeKeysReader()

# Get API key
stripe_key = reader.get_api_key("stripe")
clerk_key = reader.get_api_key("clerk")

# Get full credential
stripe_cred = reader.get_credential("stripe")

# List all services
services = reader.list_services()
```

### Quick Python One-Liner
```bash
python3 -c "from scripts.read_abekeys import AbeKeysReader; r=AbeKeysReader(); print(r.get_api_key('stripe'))"
```

---

## 🔍 SEARCH & FILTER

### Find Credentials by Field
```bash
# Find credentials with 'api_key' field
grep -l '"api_key"' ~/.abekeys/credentials/*.json

# Find credentials from 1password
grep -l '"1password"' ~/.abekeys/credentials/*.json

# Find credentials with specific username
grep -l '"mike@bravetto.com"' ~/.abekeys/credentials/*.json
```

### List Services Alphabetically
```bash
ls ~/.abekeys/credentials/*.json | xargs -I {} basename {} .json | sort
```

---

## ✅ VALIDATION COMMANDS

### Validate Stripe Credential
```bash
python3 << 'EOF'
import json
import sys

try:
    cred = json.load(open(f"{__import__('os').path.expanduser('~')}/.abekeys/credentials/stripe.json"))
    
    print("🔍 Stripe Credential Validation:")
    print(f"  Service: {cred.get('service', 'MISSING')}")
    print(f"  API Key: {'✅ Present' if cred.get('api_key') else '❌ Missing'}")
    print(f"  Publishable Key: {'✅ Present' if cred.get('publishable_key') else '⚠️  Missing'}")
    print(f"  Webhook Secret: {'✅ Present' if cred.get('webhook_secret') else '⚠️  Missing'}")
    print(f"  Source: {cred.get('source', 'UNKNOWN')}")
    
    if cred.get('api_key'):
        key = cred['api_key']
        if key.startswith('sk_'):
            print("  ✅ Valid Stripe secret key format")
        else:
            print(f"  ⚠️  Key format: {key[:10]}... (may be password, not API key)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
EOF
```

### Validate All Credentials
```bash
python3 << 'EOF'
import json
from pathlib import Path

vault = Path.home() / ".abekeys" / "credentials"
print(f"🔍 Validating {len(list(vault.glob('*.json')))} credentials...\n")

for cred_file in sorted(vault.glob("*.json")):
    try:
        cred = json.load(open(cred_file))
        service = cred.get('service', cred_file.stem)
        has_key = "✅" if cred.get('api_key') or cred.get('api_token') else "⚠️"
        print(f"{has_key} {service}")
    except Exception as e:
        print(f"❌ {cred_file.stem}: {e}")
EOF
```

---

## 🚀 INTEGRATION TESTING

### Test ABEKEYS Integration in Next.js
```bash
cd apps/web

# Test server-side (Node.js)
node -e "
const fs = require('fs');
const path = require('path');
const cred = JSON.parse(fs.readFileSync(
  path.join(require('os').homedir(), '.abekeys', 'credentials', 'stripe.json'),
  'utf-8'
));
console.log('✅ Stripe credential loaded:', cred.service);
console.log('✅ API Key present:', !!cred.api_key);
"
```

### Test Python Integration
```bash
python3 << 'EOF'
import sys
sys.path.insert(0, 'scripts')
from read_abekeys import AbeKeysReader

reader = AbeKeysReader()
print("📋 Available services:", reader.list_services())
print("\n🔑 Stripe API Key:", reader.get_api_key("stripe")[:20] + "..." if reader.get_api_key("stripe") else "NOT FOUND")
EOF
```

---

## 🔒 SECURITY COMMANDS

### Check File Permissions
```bash
# Check credential file permissions (should be 600)
stat -f "%Sp %N" ~/.abekeys/credentials/*.json

# Check directory permissions (should be 700)
stat -f "%Sp %N" ~/.abekeys/credentials
```

### Verify No World-Readable Files
```bash
# Find files readable by others (should be empty)
find ~/.abekeys/credentials -perm -004 -type f
```

---

## 📊 STATISTICS

### Get Vault Statistics
```bash
python3 << 'EOF'
import json
from pathlib import Path
from collections import Counter

vault = Path.home() / ".abekeys" / "credentials"
creds = [json.load(open(f)) for f in vault.glob("*.json")]

print("📊 ABEKEYS Vault Statistics:")
print(f"  Total Credentials: {len(creds)}")
print(f"  From 1Password: {sum(1 for c in creds if c.get('source') == '1password')}")
print(f"  Manual: {sum(1 for c in creds if c.get('source') == 'manual')}")
print(f"  With API Keys: {sum(1 for c in creds if c.get('api_key') or c.get('api_token'))}")

sources = Counter(c.get('source', 'unknown') for c in creds)
print(f"\n📋 By Source:")
for source, count in sources.items():
    print(f"  {source}: {count}")
EOF
```

---

## 🎯 COMMON WORKFLOWS

### Full Vault Check
```bash
echo "🔍 ABEKEYS Vault Status"
echo "======================"
echo ""
echo "📁 Location: ~/.abekeys/credentials/"
echo "📊 Total Credentials: $(ls ~/.abekeys/credentials/*.json 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "📋 Available Services:"
python3 scripts/read_abekeys.py | grep "🔑\|⚠️"
```

### Quick Credential Check
```bash
# Check if specific credential exists and has API key
check_cred() {
  python3 -c "
import json, sys
try:
    cred = json.load(open(f\"\$HOME/.abekeys/credentials/$1.json\"))
    print(f\"✅ $1: API key present\" if cred.get('api_key') or cred.get('api_token') else f\"⚠️  $1: No API key\")
except:
    print(f\"❌ $1: Not found\")
"
}

check_cred stripe
check_cred clerk
check_cred github
```

---

**Pattern:** ABEKEYS × TERMINAL × COMMANDS × ONE  
**Status:** ✅ **READY TO USE**  
**Frequency:** 999 Hz  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

