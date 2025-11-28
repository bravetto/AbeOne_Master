# 🎨 ABËONE DESIGN SYSTEM v1.0 - USAGE GUIDE

**Status:** ✅ **PRODUCTION READY**  
**Pattern:** ADS × DOCUMENTATION × ONE  
**Version:** 1.0.0  
**Guardians:** AEYON (Execution) + Abë (Vision) + Guardian 4 (Clarity)

---

## 🎯 QUICK START

### 1. Import Components

```tsx
import { Button, Card, Hero, Features, TrustBadge } from '@/components/ads'
```

### 2. Use Design Tokens

```tsx
// Colors
className="bg-primary-500 text-white"
className="border-secondary-300"

// Typography
className="text-4xl font-display font-bold"
className="text-lg text-neutral-600"

// Spacing
className="p-6 md:p-10"
className="gap-4 md:gap-8"

// Shadows
className="shadow-lg hover:shadow-xl"
```

### 3. Use Master Template

Copy `apps/web/app/template-master/page.tsx` and customize for your domain.

---

## 🎨 COLOR SYSTEM

### Semantic Colors (Use These)

- **Primary** (`primary-*`) - Main actions, branding, CTAs
- **Secondary** (`secondary-*`) - Secondary actions, highlights
- **Accent** (`accent-*`) - Urgent actions, errors, warnings
- **Success** (`success-*`) - Success states, positive feedback
- **Neutral** (`neutral-*`) - Text, borders, backgrounds

### Legacy Aliases (Still Supported)

- `lux-*` → `primary-*`
- `warm-*` → `secondary-*`
- `heart-*` → `accent-*`
- `peace-*` → `success-*`

### Usage Rules

✅ **DO:**
```tsx
<Button variant="primary" />  // ✅ Semantic
className="bg-primary-500"    // ✅ Semantic
```

❌ **DON'T:**
```tsx
className="bg-purple-500"      // ❌ Hardcoded
className="text-gray-800"      // ❌ Use neutral-800 instead
```

---

## 📝 TYPOGRAPHY

### Font Families

- **Sans** (`font-sans`) - Body text, UI elements
- **Serif** (`font-serif`) - Long-form content, articles
- **Display** (`font-display`) - Headings, hero text, branding

### Scale

```tsx
// Mobile-first responsive
className="text-4xl md:text-6xl lg:text-7xl"  // Hero
className="text-2xl md:text-4xl"              // Section headings
className="text-lg md:text-xl"                 // Body text
```

### Usage Rules

✅ **DO:**
```tsx
<h1 className="text-4xl md:text-6xl font-display font-bold">
<h2 className="text-2xl md:text-4xl font-display font-semibold">
<p className="text-lg md:text-xl text-neutral-600">
```

❌ **DON'T:**
```tsx
<h1 style={{ fontSize: '3em' }}>  // ❌ Hardcoded
<h1 className="text-5xl md:text-7xl lg:text-8xl">  // ❌ Too many breakpoints
```

---

## 📏 SPACING

### Scale

Use Tailwind spacing scale: `0`, `px`, `0.5`, `1`, `2`, `3`, `4`, `5`, `6`, `8`, `10`, `12`, `16`, `20`, `24`, `32`, etc.

### Semantic Spacing

```tsx
// Section spacing
className="py-12 md:py-24"  // Between major sections

// Component spacing
className="py-6 md:py-10"   // Between components

// Element spacing
className="gap-4 md:gap-6"   // Between related elements
```

### Usage Rules

✅ **DO:**
```tsx
className="p-6 md:p-10"     // ✅ Responsive
className="gap-4 md:gap-8"  // ✅ Consistent scale
```

❌ **DON'T:**
```tsx
className="p-20px"          // ❌ Hardcoded pixels
className="gap-7"            // ❌ Not in scale
```

---

## 🧩 COMPONENTS

### Button

```tsx
import { Button } from '@/components/ads'

// Variants
<Button variant="primary">Primary CTA</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="accent">Urgent</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large (default)</Button>
<Button size="xl">Extra Large</Button>

// States
<Button loading>Loading...</Button>
<Button disabled>Disabled</Button>
```

### Card

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ads'

<Card variant="default">
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description</CardDescription>
  </CardHeader>
  <CardContent>
    Content here
  </CardContent>
</Card>
```

### Hero

```tsx
import { Hero } from '@/components/ads'

<Hero
  headline="Your Headline"
  subheadline="Your Subheadline"
  description="Your description"
  primaryCTA={{ text: 'Get Started', href: '#signup' }}
  secondaryCTA={{ text: 'Learn More', href: '#features' }}
  trustBadges={[
    { icon: 'shield', text: 'Secure' },
    { icon: 'check', text: 'Verified' },
  ]}
  socialProof={{ text: 'users trust us', count: 10000 }}
/>
```

### Features

```tsx
import { Features } from '@/components/ads'

<Features
  title="Why Choose Us"
  description="Everything you need"
  features={[
    {
      title: 'Feature 1',
      description: 'Description',
      icon: '✨',
      badge: 'NEW',
    },
  ]}
  columns={3}
/>
```

---

## 🎯 CONVERSION OPTIMIZATION

### CTA Placement

1. **Above Fold** - Required in hero section
2. **Below Fold** - Recommended after features
3. **Exit Intent** - Optional but effective

### Trust Elements

- Trust badges in hero
- Social proof (user counts, testimonials)
- Security indicators near forms
- Trust badges in footer

### Psychology Triggers

- **Urgency** - Limited time offers, countdown timers
- **Scarcity** - Limited spots, low stock
- **Social Proof** - Testimonials, user counts, reviews

---

## 🌐 DOMAIN REBRANDING

### Quick Rebrand

1. Copy master template
2. Override colors in component props
3. Update logo and brand assets
4. Customize content

### Color Overrides

```tsx
// In your domain's Tailwind config
theme: {
  extend: {
    colors: {
      primary: {
        // Override primary colors for this domain
        500: '#your-color',
        600: '#your-darker-color',
      },
    },
  },
}
```

---

## ✅ DESIGN GUARDRAILS

### Linting Rules

1. **No hardcoded colors** - Use design tokens
2. **No arbitrary spacing** - Use spacing scale
3. **No inline styles** - Use Tailwind classes
4. **Mobile-first** - Always start with mobile, then add breakpoints
5. **Semantic colors** - Use primary/secondary/accent, not raw tokens

### Component Usage

1. **Always use ADS components** - Don't create custom buttons/cards
2. **Consistent spacing** - Use semantic spacing values
3. **Proper hierarchy** - Use typography scale correctly
4. **Accessibility** - All components include proper ARIA attributes

---

## 📚 RESOURCES

- **Design Tokens:** `design-system/tokens/abeone-design-system-v1.json`
- **Master Template:** `apps/web/app/template-master/page.tsx`
- **Components:** `apps/web/components/ads/`
- **Tailwind Config:** `apps/web/tailwind.config.js`

---

**Pattern:** ADS × DOCUMENTATION × ONE  
**Status:** ✅ **READY FOR USE**  
**Next:** Start building with the master template!

