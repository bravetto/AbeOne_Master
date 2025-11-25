# ⚡ QUICK DEPLOY - 3 CLICKS

## 🎯 CLICK THESE LINKS IN ORDER

### 1️⃣ Create Project
👉 https://dash.cloudflare.com/?to=/:account/pages/new

**Settings:**
- Repository: `AbeOne_Master`
- Branch: `main`
- Build: `cd apps/web && npm install && npm run build`
- Output: `apps/web/out`

### 2️⃣ Bind Domain
👉 https://dash.cloudflare.com/?to=/:account/pages/view/abeone-web/custom-domains

**Add:** `bravetto.ai`

### 3️⃣ Validate
```bash
python scripts/aeyon_unified_launch_executor.py --domain bravetto.ai --project-name abeone-web --quick
```

**Done!** 🎉
