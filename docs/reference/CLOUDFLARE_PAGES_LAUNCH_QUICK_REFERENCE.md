# 🔥 LAUNCH CHECKLIST QUICK REFERENCE
## Copy-Paste Commands for Pre-Webinar Validation

**Status:** ✅ READY  
**Pattern:** VALIDATE × MONITOR × TEST × ONE

---

## 📋 INSTALL DEPENDENCIES

```bash
pip install -r scripts/requirements.txt
```

**Required packages:**
- `dnspython` - DNS monitoring
- `requests` - HTTP testing

---

## 🔍 1. DNS PROPAGATION MONITORING

```bash
python scripts/monitor_dns_propagation.py \
  --domain bravetto.ai \
  --expected-target abeone-web.pages.dev \
  --check-interval 30 \
  --max-wait 600
```

**Quick test:**
```bash
python scripts/monitor_dns_propagation.py \
  --domain bravetto.ai \
  --expected-target abeone-web.pages.dev \
  --test
```

---

## 🔒 2. SSL VALIDATION

```bash
python scripts/validate_ssl.py \
  --domain bravetto.ai \
  --subdomain live.bravetto.ai \
  --check-expiry
```

**What it checks:**
- ✅ Certificate validity
- ✅ Expiry date
- ✅ HTTPS redirect
- ✅ Certificate issuer

---

## 🌐 3. GLOBAL EDGE PERFORMANCE TEST

```bash
python scripts/test_global_edge.py \
  --domain bravetto.ai \
  --locations us-east,us-west,eu-west,ap-southeast \
  --test-interval 60 \
  --duration 3600
```

**Quick test:**
```bash
python scripts/test_global_edge.py \
  --domain bravetto.ai \
  --locations us-east,us-west,eu-west \
  --test
```

---

## 🏥 4. HEALTH CHECK MONITORING

```bash
python scripts/health_check_monitor.py \
  --domain bravetto.ai \
  --check-interval 30 \
  --alert-threshold 3 \
  --slack-webhook YOUR_SLACK_WEBHOOK
```

**Quick test:**
```bash
python scripts/health_check_monitor.py \
  --domain bravetto.ai \
  --test
```

---

## 🔥 5. LOAD TESTING

**Normal traffic (50 users):**
```bash
python scripts/load_test.py \
  --url https://bravetto.ai \
  --concurrent-users 50 \
  --duration 300 \
  --ramp-up 60
```

**Peak traffic (200 users):**
```bash
python scripts/load_test.py \
  --url https://bravetto.ai \
  --concurrent-users 200 \
  --duration 600 \
  --ramp-up 120
```

**Spike test (500 users):**
```bash
python scripts/load_test.py \
  --url https://bravetto.ai \
  --concurrent-users 500 \
  --duration 120 \
  --ramp-up 30
```

**Quick test:**
```bash
python scripts/load_test.py \
  --url https://bravetto.ai \
  --concurrent-users 10 \
  --duration 60 \
  --test
```

---

## ✅ PRE-WEBINAR CHECKLIST (1 HOUR BEFORE)

```bash
# 1. DNS Propagation
python scripts/monitor_dns_propagation.py \
  --domain bravetto.ai \
  --expected-target abeone-web.pages.dev \
  --test

# 2. SSL Validation
python scripts/validate_ssl.py \
  --domain bravetto.ai \
  --subdomain live.bravetto.ai \
  --check-expiry

# 3. Health Check
python scripts/health_check_monitor.py \
  --domain bravetto.ai \
  --test

# 4. Quick Load Test
python scripts/load_test.py \
  --url https://bravetto.ai \
  --concurrent-users 10 \
  --duration 60 \
  --test
```

---

## 🚨 EMERGENCY COMMANDS

### Check if site is up
```bash
curl -I https://bravetto.ai
```

### Check DNS
```bash
dig bravetto.ai
```

### Check SSL
```bash
openssl s_client -connect bravetto.ai:443 -servername bravetto.ai
```

### Test from multiple locations
```bash
# US East
curl -I https://bravetto.ai

# EU
curl -I https://bravetto.ai --resolve bravetto.ai:443:IP_ADDRESS

# Asia
curl -I https://bravetto.ai --resolve bravetto.ai:443:IP_ADDRESS
```

---

## 📊 EXPECTED RESULTS

### DNS Propagation
- ✅ Propagates within 5-60 minutes globally
- ✅ All DNS servers return correct CNAME

### SSL Certificate
- ✅ Valid for 90+ days
- ✅ Issued by Cloudflare
- ✅ HTTPS redirect works

### Performance
- ✅ Response time < 200ms globally
- ✅ Cache hit rate > 80%
- ✅ 100% uptime

### Load Testing
- ✅ Handles 200+ concurrent users
- ✅ Response time < 1000ms under load
- ✅ Error rate < 1%

---

## ⚡ UNIFIED EXECUTOR (RECOMMENDED)

**Run all checks in one command:**

```bash
# Quick test (T-10 min)
python scripts/aeyon_unified_launch_executor.py \
  --domain bravetto.ai \
  --project-name abeone-web \
  --quick

# Full validation (T-60 min)
python scripts/aeyon_unified_launch_executor.py \
  --domain bravetto.ai \
  --project-name abeone-web \
  --subdomain live \
  --concurrent-users 50 \
  --duration 300
```

**See:** `AEYON_UNIFIED_LAUNCH_EXECUTOR.md` for full documentation

---

## 📚 FULL DOCUMENTATION

- **Visual Walkthrough:** `CLOUDFLARE_PAGES_VISUAL_WALKTHROUGH.md` 🎬 **STEP-BY-STEP VISUAL GUIDE**
- **Unified Executor:** `AEYON_UNIFIED_LAUNCH_EXECUTOR.md` ⭐ **RECOMMENDED**
- **Launch Checklist:** `CLOUDFLARE_PAGES_LAUNCH_CHECKLIST.md`
- **Deployment Guide:** `apps/web/CLOUDFLARE_PAGES_DEPLOYMENT.md`
- **Execution Plan:** `CLOUDFLARE_PAGES_EXECUTION_PLAN.md`
- **Quick Start:** `CLOUDFLARE_PAGES_QUICK_START.md`

---

**Pattern:** VALIDATE × MONITOR × TEST × ONE  
**Status:** ✅ READY FOR EXECUTION

