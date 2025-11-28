#  CLOUDFLARE AUTOMATION QUICK START
## One-Command DNS Configuration

**Status:**  **READY TO USE**  
**Pattern:** Cloudflare × Automation × AbëKEYS × ONE

---

##  QUICK START (30 Seconds)

### Step 1: Get Cloudflare API Token
1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Click **Create Token**
3. Use template: **Edit zone DNS**
4. Select zone: `bravetto.ai`
5. Copy token

### Step 2: Store Credentials
**Option A: AbëKEYS (Recommended)**
```bash
cat > ~/.abekeys/credentials/cloudflare.json << EOF
{
  "service": "cloudflare",
  "api_token": "YOUR_TOKEN_HERE",
  "source": "manual"
}
EOF
```

**Option B: 1Password**
- Create item: "Cloudflare"
- Add field: "API Token" → paste token

**Option C: Environment Variable**
```bash
export CLOUDFLARE_API_TOKEN="YOUR_TOKEN_HERE"
```

### Step 3: Run Automation
```bash
cd /Users/michaelmataluni/Documents/AbeOne_Master
./scripts/bravetto_ai_dns_setup.sh
```

**That's it!** 

---

##  COMMON COMMANDS

### List DNS Records
```bash
python3 scripts/cloudflare_dns_automation.py bravetto.ai --list
```

### Configure for Vercel
```bash
python3 scripts/cloudflare_dns_automation.py bravetto.ai \
  --configure-vercel \
  --vercel-ip "76.76.21.21" \
  --vercel-cname "cname.vercel-dns.com"
```

### Remove Conflicting Records
```bash
python3 scripts/cloudflare_dns_automation.py bravetto.ai --remove-conflicting
```

### Add Single DNS Record
```bash
python3 scripts/cloudflare_dns_automation.py bravetto.ai \
  --add --type A --name "@" --content "76.76.21.21"
```

---

##  AUTHENTICATION METHODS

### Method 1: AbëKEYS 
```bash
# Check if credentials exist
python3 scripts/read_abekeys.py cloudflare

# If not, create:
cat > ~/.abekeys/credentials/cloudflare.json << EOF
{
  "service": "cloudflare",
  "api_token": "your-token",
  "source": "manual"
}
EOF
```

### Method 2: 1Password 
```bash
# Sign in
eval $(op signin)

# Pull credentials
python3 scripts/unlock_all_credentials.py

# Or get directly
export CLOUDFLARE_API_TOKEN=$(op item get "Cloudflare" --field "API Token")
```

### Method 3: Environment Variables 
```bash
export CLOUDFLARE_API_TOKEN="your-token"
# OR
export CLOUDFLARE_EMAIL="your-email"
export CLOUDFLARE_API_KEY="your-key"
```

---

##  TYPICAL WORKFLOW

### For Bravetto.ai Vercel Deployment

1. **Get Vercel DNS Info**
   - Go to Vercel Dashboard → Project → Domains
   - Add `bravetto.ai`
   - Copy IP address and CNAME

2. **Run Automation**
   ```bash
   ./scripts/bravetto_ai_dns_setup.sh
   ```
   - Enter Vercel IP when prompted
   - Enter Vercel CNAME when prompted

3. **Verify**
   ```bash
   python3 scripts/cloudflare_dns_automation.py bravetto.ai --list
   ```

4. **Wait & Test**
   - Wait 5-60 minutes for DNS propagation
   - Check: https://dnschecker.org
   - Test: https://bravetto.ai

---

##  TROUBLESHOOTING

### "Authentication failed"
- Check credentials: `python3 scripts/read_abekeys.py cloudflare`
- Try 1Password: `eval $(op signin) && python3 scripts/unlock_all_credentials.py`
- Set env var: `export CLOUDFLARE_API_TOKEN="..."`

### "Domain not found"
- Verify domain is in Cloudflare account
- Check domain spelling
- Ensure API token has zone access

### "Record already exists"
- Remove conflicting: `--remove-conflicting`
- Or use `--configure-vercel` (handles automatically)

---

##  FULL DOCUMENTATION

See `CLOUDFLARE_AUTOMATION_COMPLETE.md` for:
- Complete API reference
- Advanced usage examples
- Security best practices
- Integration details

---

**Pattern:** Cloudflare × Automation × AbëKEYS × ONE  
**Status:**  **READY**

**∞ LOVE AUTOMATED ∞**

