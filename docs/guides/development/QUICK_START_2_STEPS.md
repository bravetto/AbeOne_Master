# ⚡ QUICK START - 2 STEPS
## The Absolute Minimum You Need

**Time:** 10 minutes total  
**Difficulty:** Easy (copy-paste ready)

---

## STEP 1: Fix Token (5 min)

### 1. Get Token
👉 https://dash.cloudflare.com/profile/api-tokens
- Click "Create Token"
- Use template "Edit zone DNS"
- Select zone: bravetto.ai
- Copy token

### 2. Set Token
```bash
# Python version (recommended)
python3 scripts/set_cloudflare_token.py YOUR_TOKEN_HERE

# OR bash version
bash scripts/set_cloudflare_token.sh YOUR_TOKEN_HERE
```

### 3. Verify
```bash
python3 scripts/validate_cloudflare_credentials.py
```
**Done when:** ✅ ALL VALIDATIONS PASSED

---

## STEP 2: Create Project (AUTOMATED - 30 seconds)

### Option A: Automated (Recommended)
```bash
# Try automation first
python3 scripts/automate_cloudflare_pages_setup.py

# If it asks for Account ID, get it:
python3 scripts/get_cloudflare_account_id.py

# Then run with Account ID:
python3 scripts/automate_cloudflare_pages_setup.py --account-id YOUR_ACCOUNT_ID
```

**Done when:** ✅ Project created and deployment triggered

### Option B: Manual (If automation fails)
👉 https://dash.cloudflare.com/?to=/:account/pages/new
- Click "Connect to Git" → GitHub
- Select: AbeOne_Master
- Build command: `cd apps/web && npm install && npm run build`
- Output directory: `apps/web/out`
- Click "Save and Deploy"

---

## 🎉 THAT'S IT!

After these 2 steps:
- ✅ Site is live
- ✅ Auto-deploys on every push
- ✅ Everything else is automatic

---

## 🚀 BONUS: Bind Domain (Optional)

```bash
python3 scripts/cloudflare_pages_auto_bind.py \
  --domain bravetto.ai \
  --project-name abeone-web
```

Wait 2 minutes → Visit https://bravetto.ai

---

**That's literally it. 2 steps. 10 minutes. Done forever.**

