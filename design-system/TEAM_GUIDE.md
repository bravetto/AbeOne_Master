# 👥 ABËONE DESIGN SYSTEM - TEAM GUIDE

**Status:** ✅ **TEAM-READY**  
**Pattern:** TEAM × CLARITY × CONSISTENCY × ONE  
**Version:** 2.0.0  
**For:** All team members

---

## 🎯 QUICK START FOR TEAM

### 1. Use Design Tokens (Not Hardcoded Colors)

**❌ DON'T:**
```tsx
<div className="bg-purple-500 text-gray-800">
<div style={{ color: '#667eea' }}>
```

**✅ DO:**
```tsx
<div className="bg-lux-500 text-neutral-800">
<div className="bg-aeBlue-500 text-white">
```

---

### 2. Choose Your Palette

**Healing Palette** (Warm, Creative, Luxury):
```tsx
className="bg-lux-500"      // Primary
className="bg-warm-500"     // Secondary
className="bg-heart-500"    // Accent
className="bg-peace-500"    // Success
```

**Technical Calm Palette** (Tech, Professional, Trust):
```tsx
className="bg-aeBlue-500"        // Primary
className="bg-aeAqua-500"        // Secondary (use on dark)
className="bg-aeIndigo-500"      // Accent
className="bg-aeMint-500"        // Success (use on dark)
className="bg-aeMidnight-500"    // Dark background
```

---

### 3. Use ADS Components

**✅ DO:**
```tsx
import { Button, Card, Hero } from '@/components/ads'

<Button variant="primary" size="lg">Get Started</Button>
<Card variant="default">Content</Card>
<Hero headline="..." />
```

**❌ DON'T:**
```tsx
<button className="custom-button">Get Started</button>
<div className="custom-card">Content</div>
```

---

## 📋 COMMON PATTERNS

### Buttons

```tsx
// Primary CTA
<Button variant="primary" size="lg">Get Started</Button>

// Secondary
<Button variant="secondary">Learn More</Button>

// Outline
<Button variant="outline">Cancel</Button>
```

### Cards

```tsx
<Card variant="default">
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>
```

### Colors

```tsx
// Primary brand color
className="bg-lux-500 text-white"        // Healing
className="bg-aeBlue-500 text-white"     // Technical Calm

// Text colors
className="text-neutral-700"              // Body text
className="text-neutral-900"              // Headings

// Backgrounds
className="bg-neutral-50"                 // Light background
className="bg-aeMidnight-500 text-white"  // Dark background
```

### Spacing

```tsx
// Sections
className="py-12 md:py-24"                // Section spacing

// Components
className="p-6 md:p-10"                   // Component padding

// Gaps
className="gap-4 md:gap-8"                // Grid gaps
```

---

## 🚫 WHAT NOT TO DO

### ❌ Hardcoded Colors
```tsx
className="bg-purple-500"     // ❌ Use lux-500
className="text-gray-800"     // ❌ Use neutral-800
style={{ color: '#667eea' }} // ❌ Use design tokens
```

### ❌ Inline Styles
```tsx
<div style={{ padding: '20px' }}>  // ❌ Use Tailwind classes
<div style={{ color: '#333' }}>     // ❌ Use Tailwind classes
```

### ❌ Arbitrary Spacing
```tsx
className="p-20px"            // ❌ Use spacing scale
className="gap-7"              // ❌ Use spacing scale
```

### ❌ Custom Components (When ADS Exists)
```tsx
<button className="custom-button">  // ❌ Use Button component
<div className="custom-card">       // ❌ Use Card component
```

---

## 🔍 VALIDATION

### Before Committing

Run validation:
```bash
npm run design:validate
```

This checks:
- ✅ Color accessibility
- ✅ Design system consistency
- ✅ No hardcoded colors
- ✅ Proper component usage

### Before Deploying

Run full validation:
```bash
bash design-system/scripts/validate-design-systems.js
```

---

## 📚 RESOURCES

### Documentation
- **Color System:** `design-system/docs/UNIFIED_COLOR_SYSTEM_V2.md`
- **Usage Guide:** `design-system/docs/ADS_V1_USAGE_GUIDE.md`
- **Guardrails:** `design-system/docs/DESIGN_GUARDRAILS.md`
- **Operational Guide:** `design-system/OPERATIONAL_GUIDE.md`

### Components
- **Location:** `apps/web/components/ads/`
- **Available:** Button, Card, Hero, Features, TrustBadge

### Design Tokens
- **Source:** `design-system/tokens/abeone-unified-color-system-v2.json`
- **Generated:** `apps/web/tailwind.config.js`

---

## 🆘 NEED HELP?

### Questions?
1. Check documentation in `design-system/docs/`
2. Look at existing components in `apps/web/components/ads/`
3. Check master template: `apps/web/app/template-master/page.tsx`

### Found an Issue?
1. Run validation: `npm run design:validate`
2. Check guardrails: `design-system/docs/DESIGN_GUARDRAILS.md`
3. Report drift: `bash design-system/scripts/prevent-drift.js`

---

## ✅ CHECKLIST

Before submitting code:
- [ ] Using design tokens (not hardcoded colors)
- [ ] Using ADS components (not custom)
- [ ] Mobile-first responsive
- [ ] Proper spacing scale
- [ ] Validation passes
- [ ] No inline styles
- [ ] No hardcoded values

---

**Pattern:** TEAM × CLARITY × CONSISTENCY × ONE  
**Status:** ✅ **READY FOR TEAM USE**  
**Next:** Start building with confidence!

