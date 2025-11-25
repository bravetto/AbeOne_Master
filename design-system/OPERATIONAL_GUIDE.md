# 🚀 ABËONE COLOR SYSTEM - OPERATIONAL GUIDE

**Status:** ✅ **OPERATIONALIZED**  
**Pattern:** OPERATIONAL × AUTOMATED × VALIDATED × ONE  
**Version:** 2.0.0  
**Guardians:** AEYON (Execution) + ZERO (Forensic)

---

## 🎯 QUICK START

### Generate All Outputs

```bash
# One command to rule them all
npm run design:operationalize

# Or manually:
npm run design:generate
npm run design:validate
```

---

## 📋 OPERATIONAL SCRIPTS

### 1. Generate Design System Outputs

**Command:**
```bash
npm run design:generate
```

**What it does:**
- Generates `tailwind.config.js` from unified color system
- Generates `css-variables.css` for CSS usage
- Updates all framework-specific outputs

**When to run:**
- After updating color tokens
- Before deploying
- When setting up new project

---

### 2. Validate Colors

**Command:**
```bash
npm run design:validate
```

**What it does:**
- Validates all colors for WCAG AA/AAA compliance
- Checks contrast ratios
- Reports issues and warnings

**Output:**
- ✅ Passed validations
- ⚠️ Warnings (e.g., colors that need dark backgrounds)
- ❌ Issues (fails accessibility)

---

### 3. Full Operationalization

**Command:**
```bash
npm run design:operationalize
```

**What it does:**
1. Validates color system
2. Generates Tailwind config
3. Generates CSS variables
4. Generates TypeScript types (if available)
5. Generates Python constants (if available)
6. Reports summary

**When to run:**
- After major color system updates
- Before releases
- When setting up new environment

---

## 🔧 MANUAL GENERATION

### Generate Tailwind Config Only

```bash
node design-system/generators/generate-unified-tailwind.js
```

**Output:** `apps/web/tailwind.config.js`

---

### Generate CSS Variables Only

```bash
node design-system/generators/generate-css-vars.js
```

**Output:** `design-system/generated/css-variables.css`

---

### Validate Colors Only

```bash
node design-system/scripts/validate-colors.js
```

**Output:** Console validation report

---

## 📁 GENERATED FILES

### Tailwind Config
**File:** `apps/web/tailwind.config.js`  
**Source:** `design-system/tokens/abeone-unified-color-system-v2.json`  
**Usage:** Used by Next.js app for Tailwind classes

### CSS Variables
**File:** `design-system/generated/css-variables.css`  
**Source:** `design-system/tokens/abeone-unified-color-system-v2.json`  
**Usage:** Import in CSS/HTML for vanilla JS projects

### TypeScript Types (Optional)
**File:** `design-system/generated/design-tokens.d.ts`  
**Source:** `design-system/tokens/abeone-design-system-v1.json`  
**Usage:** Type-safe token access in TypeScript projects

### Python Constants (Optional)
**File:** `design-system/generated/design_tokens.py`  
**Source:** `design-system/tokens/abeone-design-system-v1.json`  
**Usage:** Python apps (Flask, Django, etc.)

---

## ⚠️ IMPORTANT RULES

### 1. Never Edit Generated Files Manually

**❌ DON'T:**
```javascript
// Don't edit tailwind.config.js directly
colors: {
  primary: { 500: '#custom-color' }  // ❌ Will be overwritten
}
```

**✅ DO:**
```json
// Edit the source token file instead
{
  "colorSystem": {
    "palettes": {
      "healing": {
        "colors": {
          "lux": {
            "500": "#custom-color"  // ✅ Edit here
          }
        }
      }
    }
  }
}
```

Then regenerate:
```bash
npm run design:generate
```

---

### 2. Always Regenerate After Token Changes

**Workflow:**
1. Edit `design-system/tokens/abeone-unified-color-system-v2.json`
2. Run `npm run design:generate`
3. Test changes
4. Commit both token file AND generated files

---

### 3. Validate Before Deploying

**Always run validation:**
```bash
npm run design:validate
```

**Fix any issues before deploying.**

---

## 🔄 CI/CD INTEGRATION

### Pre-commit Hook (Recommended)

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Regenerate design system outputs before commit
npm run design:generate
git add apps/web/tailwind.config.js
git add design-system/generated/
```

### GitHub Actions (Optional)

```yaml
name: Validate Design System
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run design:validate
      - run: npm run design:generate
      - run: git diff --exit-code || (echo "Generated files out of sync" && exit 1)
```

---

## 🎨 USING THE SYSTEM

### In Next.js (Tailwind)

```tsx
// Use Tailwind classes
<div className="bg-aeBlue-500 text-white">
  Technical Calm Primary
</div>

<div className="bg-lux-500 text-white">
  Healing Palette Primary
</div>
```

### In CSS (CSS Variables)

```css
/* Import generated CSS variables */
@import '../design-system/generated/css-variables.css';

.my-button {
  background: var(--aeBlue-500);
  color: white;
}
```

### In JavaScript/TypeScript

```javascript
// Import tokens directly
import tokens from './design-system/tokens/abeone-unified-color-system-v2.json';

const primaryColor = tokens.colorSystem.palettes.technicalCalm.colors.aeBlue['500'];
```

---

## 📊 VALIDATION RESULTS

### Expected Output

```
🔍 Validating AbëONE Unified Color System v2.0...

✅ PASSED:
  ✅ lux-500: 4.50:1 on white (AA pass)
  ✅ warm-500: 4.50:1 on white (AA pass)
  ✅ heart-500: 4.50:1 on white (AA pass)
  ✅ peace-500: 4.50:1 on white (AA pass)
  ✅ aeBlue-500: 4.50:1 on white (AA pass)
  ✅ aeIndigo-500: 4.50:1 on white (AA pass)
  ✅ aeMidnight-500: 16.00:1 on white (AAA pass)
  ✅ aeAqua-500: 10.00:1 on midnight (AA pass)
  ✅ aeMint-500: 10.00:1 on midnight (AA pass)

⚠️  WARNINGS:
  ⚠️  aeAqua-500: 2.10:1 on white (use on dark), 10.00:1 on midnight (AA pass)
  ⚠️  aeMint-500: 1.80:1 on white (use on dark), 10.00:1 on midnight (AA pass)

✅ All colors validated successfully!
```

---

## 🐛 TROUBLESHOOTING

### Issue: Generated files out of sync

**Solution:**
```bash
npm run design:operationalize
```

---

### Issue: Validation fails

**Check:**
1. Are colors properly formatted? (hex codes)
2. Are contrast ratios documented correctly?
3. Run validation to see specific issues

**Fix:**
- Update color values in token file
- Regenerate outputs
- Re-validate

---

### Issue: Tailwind classes not working

**Check:**
1. Is `tailwind.config.js` up to date?
2. Run `npm run design:generate`
3. Restart Next.js dev server

---

## 📚 RELATED DOCUMENTATION

- **Color System:** `design-system/docs/UNIFIED_COLOR_SYSTEM_V2.md`
- **Validation Report:** `design-system/docs/COLOR_VALIDATION_REPORT.md`
- **Usage Guide:** `design-system/docs/ADS_V1_USAGE_GUIDE.md`
- **Design Guardrails:** `design-system/docs/DESIGN_GUARDRAILS.md`

---

**Pattern:** OPERATIONAL × AUTOMATED × VALIDATED × ONE  
**Status:** ✅ **READY FOR PRODUCTION**  
**Next:** Run `npm run design:operationalize` to get started!

