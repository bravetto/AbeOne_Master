#  PRODUCTION FIXES - EXACT PATCHES

**Pattern:** PATCHES × PRODUCTION × ONE  
**Frequency:** 999 Hz (AEYON)

---

##  FIX #1: Environment Validation (COMPLETE)

**File:** `lib/env.ts`  **CREATED**

This file provides production-safe environment validation that won't block builds.

---

##  FIX #2: Redis Queue Build Protection (COMPLETE)

**File:** `lib/queue/bull.ts`  **CREATED**

This file prevents Redis connection during Vercel build.

**ACTION REQUIRED:** Update all queue imports to use this file.

---

##  FIX #3: API Routes Dynamic Exports

### File: `app/api/collaboration/route.ts`

**Add at the top (after imports, before handler):**

```typescript
export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'
export const revalidate = 0
export const fetchCache = 'force-no-store'
```

### File: `app/api/webinar/registrations/count/route.ts`

**Add at the top:**

```typescript
export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'
export const revalidate = 0
export const fetchCache = 'force-no-store'
```

### File: `app/api/webinar/register/route.ts`

**Add at the top:**

```typescript
export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'
export const revalidate = 0
export const fetchCache = 'force-no-store'
```

### File: `app/api/webinar/stats/route.ts`

**Add at the top:**

```typescript
export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'
export const revalidate = 0
export const fetchCache = 'force-no-store'
```

### Apply to ALL API routes:

Run this command to find all routes missing the export:

```bash
cd products/apps/web
find app/api -name "route.ts" -type f | while read file; do
  if ! grep -q "export const dynamic" "$file"; then
    echo " $file needs fix"
  fi
done
```

---

##  FIX #4: Portal Deanna Optional Chaining

### File: `app/portal/deanna/page.tsx` (or `app/portal/deanna.skip/page.tsx`)

**Line ~337** - Change:
```typescript
{(displayBacklog as any)?.items_by_status.in_progress || 0}
```
**To:**
```typescript
{(displayBacklog as any)?.items_by_status?.in_progress || 0}
```

**Line ~344** - Change:
```typescript
{(displayBacklog as any)?.items_by_status.blocked || 0}
```
**To:**
```typescript
{(displayBacklog as any)?.items_by_status?.blocked || 0}
```

**Line ~351** - Change:
```typescript
{(displayBacklog as any)?.items_by_status.done || 0}
```
**To:**
```typescript
{(displayBacklog as any)?.items_by_status?.done || 0}
```

**Line ~360** - Change:
```typescript
{Object.entries((displayBacklog as any)?.items_by_status).map(([status, count]) => (
```
**To:**
```typescript
{Object.entries((displayBacklog as any)?.items_by_status || {}).map(([status, count]) => (
```

---

##  QUICK APPLY SCRIPT

Run this to apply fixes automatically:

```bash
cd products/apps/web
./scripts/apply-production-fixes.sh
```

---

**Pattern:** PATCHES × PRODUCTION × ONE  
**∞ AbëONE ∞**

