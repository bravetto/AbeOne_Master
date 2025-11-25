# 🛡️ ABËONE DESIGN SYSTEM - DESIGN GUARDRAILS

**Status:** ✅ **ACTIVE PROTECTION**  
**Pattern:** ADS × GUARDRAILS × DRIFT PREVENTION × ONE  
**Version:** 1.0.0  
**Guardians:** ZERO (Forensic) + Guardian 8 (Trust) + Guardian 4 (Clarity)

---

## 🎯 PURPOSE

Prevent design drift and maintain consistency across 1,000+ domains.

---

## 🚫 FORBIDDEN PATTERNS

### ❌ Hardcoded Colors

**FORBIDDEN:**
```tsx
className="bg-purple-500"           // ❌ Hardcoded
className="text-gray-800"           // ❌ Hardcoded
style={{ color: '#667eea' }}        // ❌ Hardcoded
```

**REQUIRED:**
```tsx
className="bg-primary-500"          // ✅ Design token
className="text-neutral-800"        // ✅ Design token
```

---

### ❌ Arbitrary Spacing

**FORBIDDEN:**
```tsx
className="p-20px"                  // ❌ Hardcoded pixels
className="gap-7"                   // ❌ Not in scale
style={{ padding: '30px' }}         // ❌ Hardcoded
```

**REQUIRED:**
```tsx
className="p-6 md:p-10"             // ✅ Scale + responsive
className="gap-4 md:gap-8"          // ✅ Scale + responsive
```

---

### ❌ Inline Styles

**FORBIDDEN:**
```tsx
<div style={{ padding: '20px' }}>   // ❌ Inline styles
<div style={{ color: '#333' }}>     // ❌ Inline styles
```

**REQUIRED:**
```tsx
<div className="p-5 text-neutral-700">  // ✅ Tailwind classes
```

---

### ❌ Custom Components (When ADS Exists)

**FORBIDDEN:**
```tsx
// Don't create custom buttons when Button component exists
<button className="custom-button">  // ❌ Custom
```

**REQUIRED:**
```tsx
import { Button } from '@/components/ads'
<Button variant="primary">            // ✅ ADS component
```

---

### ❌ Inconsistent Typography

**FORBIDDEN:**
```tsx
<h1 style={{ fontSize: '3em' }}>   // ❌ Hardcoded
<h1 className="text-5xl md:text-7xl lg:text-8xl">  // ❌ Too many breakpoints
```

**REQUIRED:**
```tsx
<h1 className="text-4xl md:text-6xl font-display font-bold">  // ✅ Scale + responsive
```

---

## ✅ REQUIRED PATTERNS

### ✅ Mobile-First Design

**ALWAYS START WITH MOBILE:**
```tsx
// Mobile first, then add breakpoints
className="text-4xl md:text-6xl"    // ✅ Mobile → Desktop
className="p-6 md:p-10"              // ✅ Mobile → Desktop
```

**NEVER DESKTOP-FIRST:**
```tsx
className="text-6xl md:text-4xl"      // ❌ Desktop → Mobile
```

---

### ✅ Semantic Colors

**USE SEMANTIC COLORS:**
```tsx
className="bg-primary-500"            // ✅ Semantic
className="text-secondary-600"       // ✅ Semantic
```

**AVOID RAW TOKENS (unless necessary):**
```tsx
className="bg-lux-500"                // ⚠️ Legacy alias (okay but prefer primary)
```

---

### ✅ Consistent Spacing

**USE SPACING SCALE:**
```tsx
className="p-4 md:p-6"               // ✅ Scale
className="gap-4 md:gap-8"           // ✅ Scale
```

**USE SEMANTIC SPACING:**
```tsx
className="py-12 md:py-24"           // ✅ Section spacing
className="p-6 md:p-10"              // ✅ Component spacing
```

---

### ✅ Component Variants

**USE COMPONENT VARIANTS:**
```tsx
<Button variant="primary" size="lg">  // ✅ Variants
<Card variant="default">              // ✅ Variants
```

**DON'T OVERRIDE COMPONENT STYLES:**
```tsx
<Button className="bg-red-500">     // ❌ Override
```

---

## 🔍 VALIDATION CHECKLIST

Before deploying any landing page, verify:

- [ ] No hardcoded colors (use design tokens)
- [ ] No arbitrary spacing (use spacing scale)
- [ ] No inline styles (use Tailwind classes)
- [ ] Mobile-first responsive design
- [ ] Uses ADS components (Button, Card, Hero, etc.)
- [ ] Consistent typography scale
- [ ] Proper semantic colors (primary/secondary/accent)
- [ ] Conversion-optimized CTAs above fold
- [ ] Trust elements present (badges, social proof)
- [ ] Accessibility (focus states, ARIA attributes)

---

## 🚨 DRIFT DETECTION

### Automated Checks

Run these commands before committing:

```bash
# Check for hardcoded colors
grep -r "bg-purple\|text-gray\|#[0-9a-fA-F]" apps/web/components

# Check for inline styles
grep -r "style=" apps/web/components

# Check for custom components when ADS exists
grep -r "className.*button" apps/web/components | grep -v "Button"
```

### Manual Review

Before merging PRs, check:

1. **Colors** - All using design tokens?
2. **Spacing** - All using spacing scale?
3. **Components** - Using ADS components?
4. **Typography** - Consistent scale?
5. **Responsive** - Mobile-first?
6. **Conversion** - CTAs optimized?

---

## 📋 COMPONENT USAGE RULES

### Button

✅ **DO:**
```tsx
import { Button } from '@/components/ads'
<Button variant="primary" size="lg">CTA</Button>
```

❌ **DON'T:**
```tsx
<button className="custom-button">CTA</button>
<a className="btn-primary">CTA</a>
```

---

### Card

✅ **DO:**
```tsx
import { Card, CardHeader, CardTitle } from '@/components/ads'
<Card variant="default">
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
</Card>
```

❌ **DON'T:**
```tsx
<div className="custom-card">...</div>
```

---

### Hero

✅ **DO:**
```tsx
import { Hero } from '@/components/ads'
<Hero headline="..." primaryCTA={{...}} />
```

❌ **DON'T:**
```tsx
<section className="hero">...</section>  // Custom hero
```

---

## 🎨 BRAND OVERRIDE RULES

### Domain Rebranding

✅ **ALLOWED:**
- Override primary/secondary/accent colors via Tailwind config
- Custom logo and brand assets
- Domain-specific content

❌ **FORBIDDEN:**
- Changing spacing scale
- Changing typography scale
- Changing component structure
- Breaking responsive breakpoints

---

## 📊 METRICS TO TRACK

Monitor these to detect drift:

1. **Color Consistency** - % using design tokens
2. **Component Usage** - % using ADS components
3. **Spacing Consistency** - % using spacing scale
4. **Mobile Performance** - Lighthouse scores
5. **Conversion Rate** - CTA click-through rates

---

## 🔧 TOOLS

### Linting

Add to `.eslintrc.js`:
```js
rules: {
  'no-inline-styles': 'error',
  // Add custom rules for design tokens
}
```

### Pre-commit Hooks

Add to `.husky/pre-commit`:
```bash
# Check for hardcoded colors
npm run lint:design-tokens
```

---

**Pattern:** ADS × GUARDRAILS × DRIFT PREVENTION × ONE  
**Status:** ✅ **ACTIVE**  
**Enforcement:** Manual review + automated checks

