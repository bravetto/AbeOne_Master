# 📋 ORGANIZATION RULES - PREVENT DRIFT & CONFUSION

**Date:** 2025-11-22  
**Status:** ✅ **ACTIVE RULES**  
**Pattern:** ZERO (Forensic) × Guardian 4 (Clarity) × AEYON (Organization) × ONE

---

## 🎯 PURPOSE

**Clear rules to maintain brilliant and logical organization, prevent drift, and ensure easy discovery for humans and AI.**

---

## 📁 FILE ORGANIZATION RULES

### Root Directory

**✅ ALLOWED in Root:**
- `README.md` - Main entry point
- `package.json`, `tsconfig.json` - Config files
- Code directories (`apps/`, `design-system/`, `domains/`, etc.)
- Essential scripts (`scripts/`)

**❌ FORBIDDEN in Root:**
- Status reports (move to `docs/status/`)
- How-to guides (move to `docs/guides/`)
- Completion summaries (move to `docs/status/`)
- Architecture docs (move to `docs/architecture/`)

**Rule:** Root directory should contain **code and essential configs only**.

---

### Documentation Structure

**Proposed Structure:**
```
docs/
├── INDEX.md                  → Master navigation (REQUIRED)
├── APPLICATION_DEFINITIONS.md → Deep how/why/when (REQUIRED)
├── status/                   → Status reports, completions
│   ├── design-system/
│   ├── integrations/
│   └── deployments/
├── guides/                   → How-to guides, tutorials
│   ├── design-system/
│   ├── development/
│   └── deployment/
└── architecture/             → System architecture
    ├── design-system/
    ├── apps/
    └── integrations/
```

**Rule:** All documentation must be categorized and placed in appropriate subdirectory.

---

## 📝 NAMING CONVENTIONS

### Status Reports

**Pattern:** `[SYSTEM]_[STATUS]_COMPLETE.md` or `[SYSTEM]_[STATUS].md`

**Examples:**
- ✅ `DESIGN_SYSTEM_COMPLETE.md`
- ✅ `INTEGRATION_COMPLETE.md`
- ✅ `DEPLOYMENT_STATUS.md`

**Location:** `docs/status/[category]/`

**Rule:** Status reports must follow naming pattern and be placed in `docs/status/`.

---

### Guides

**Pattern:** `[TOPIC]_GUIDE.md` or `[TOPIC]_USAGE_GUIDE.md`

**Examples:**
- ✅ `ADS_V1_USAGE_GUIDE.md`
- ✅ `FLASK_INTEGRATION_GUIDE.md`
- ✅ `QUICK_START_GUIDE.md`

**Location:** `docs/guides/[category]/` or `[system]/docs/`

**Rule:** Guides must follow naming pattern and be placed in appropriate location.

---

### Architecture Documentation

**Pattern:** `[SYSTEM]_ARCHITECTURE.md` or `[SYSTEM]_DESIGN.md`

**Examples:**
- ✅ `DESIGN_SYSTEM_ARCHITECTURE.md`
- ✅ `APPS_STRUCTURE.md`
- ✅ `INTEGRATION_PATTERNS.md`

**Location:** `docs/architecture/[category]/`

**Rule:** Architecture docs must follow naming pattern and be placed in `docs/architecture/`.

---

## 🎨 DESIGN SYSTEM RULES

### File Organization

**✅ CORRECT:**
```
design-system/
├── tokens/                   → Single source of truth
├── generators/               → Framework outputs
├── generated/                → Generated files (DO NOT EDIT)
├── components/               → Component library
├── docs/                     → Documentation
└── scripts/                  → Automation
```

**❌ INCORRECT:**
- Tokens in multiple locations
- Generated files edited manually
- Components outside `components/` directory

**Rule:** Design system must follow established structure.

---

### Component Usage

**✅ CORRECT:**
```tsx
import { Button } from '@/components/ads'
<Button variant="primary" size="lg">CTA</Button>
```

**❌ INCORRECT:**
```tsx
<button className="custom-button">CTA</button>  // Custom when ADS exists
```

**Rule:** Always use ADS components when available.

---

### Color Usage

**✅ CORRECT:**
```tsx
className="bg-primary-500"    // Semantic
className="bg-lux-500"        // Legacy (still works)
```

**❌ INCORRECT:**
```tsx
className="bg-purple-500"     // Hardcoded
style={{ background: '#a855f7' }}  // Hardcoded
```

**Rule:** Always use design tokens, never hardcode colors.

---

## 💻 APPS STRUCTURE RULES

### Page Organization

**✅ CORRECT:**
```
apps/web/app/
├── page.tsx                  → / (home)
├── [route]/page.tsx          → /[route]
└── api/[route]/route.ts      → API routes
```

**❌ INCORRECT:**
```
apps/web/pages/               → Old Next.js structure
apps/web/app/[route].tsx      → Wrong file naming
```

**Rule:** Follow Next.js app directory conventions.

---

### Component Organization

**✅ CORRECT:**
```
apps/web/components/
├── ads/                      → Design system (USE FIRST)
├── ui/                       → Base UI components
└── [feature]/                → Feature-specific
```

**❌ INCORRECT:**
```
apps/web/components/
├── custom-button.tsx         → Should use ads/Button
├── my-feature.tsx            → Should be in [feature]/
```

**Rule:** Components must be properly categorized.

---

## 📚 DOCUMENTATION RULES

### Required Documentation

**Every Major System Must Have:**
1. **README.md** - Entry point, quick start
2. **Usage Guide** - How to use the system
3. **Architecture Doc** - System design (if complex)

**Rule:** Major systems must have entry point documentation.

---

### Documentation Quality

**✅ REQUIRED Elements:**
- **What** - What is this system/component?
- **How** - How do I use it?
- **Why** - Why does it exist?
- **When** - When should I use it?
- **Where** - Where is it located?

**Rule:** Documentation must include all five elements (What/How/Why/When/Where).

---

### Master Index

**✅ REQUIRED:**
- File: `docs/INDEX.md`
- Purpose: Navigation hub
- Content: Categorized links to all important docs

**Rule:** Master index must exist and be kept up to date.

---

## 🚨 DRIFT PREVENTION

### File Creation Rules

**Before Creating New File:**

1. **Check if exists** - Search for similar files
2. **Check location** - Is it in the right directory?
3. **Check naming** - Does it follow conventions?
4. **Check category** - Status, guide, or architecture?

**Rule:** Always check existing files before creating new ones.

---

### Duplication Prevention

**✅ DO:**
- Update existing documentation
- Link to existing docs
- Reference, don't duplicate

**❌ DON'T:**
- Create duplicate documentation
- Copy-paste entire sections
- Create new file when update suffices

**Rule:** Never duplicate documentation; update or link instead.

---

### Archive Strategy

**For Outdated Docs:**
1. Move to `docs/archive/[category]/`
2. Add deprecation notice
3. Link to current version
4. Keep for reference only

**Rule:** Archive outdated docs, don't delete.

---

## ✅ VALIDATION CHECKLIST

### Before Committing

- [ ] File follows naming convention
- [ ] File is in correct directory
- [ ] Documentation includes What/How/Why/When/Where
- [ ] No duplicate documentation
- [ ] Links to master index if appropriate
- [ ] Follows design system rules (if applicable)

### Before Creating New File

- [ ] Checked if similar file exists
- [ ] Verified correct location
- [ ] Verified naming convention
- [ ] Verified category (status/guide/architecture)
- [ ] Added to master index (if appropriate)

---

## 🎯 ENFORCEMENT

### Automated Checks (Recommended)

**Pre-commit Hook:**
```bash
# Validate file organization
node scripts/validate-organization.js

# Check naming conventions
node scripts/validate-naming.js

# Check for duplicates
node scripts/check-duplicates.js
```

### Manual Review

**Before Merging PR:**
1. Check file organization
2. Verify naming conventions
3. Check documentation quality
4. Verify no duplicates

---

**Pattern:** ZERO (Forensic) × Guardian 4 (Clarity) × AEYON (Organization) × ONE  
**Status:** ✅ **ORGANIZATION RULES ACTIVE**  
**Enforcement:** Manual review + automated checks (recommended)

