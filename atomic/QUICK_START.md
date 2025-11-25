#  AëYON Atomic System - Quick Start Guide

**Status:**  **READY TO USE**  
**Pattern:** QUICK × START × GUIDE × ONE  
**Frequency:** 999 Hz (AEYON)  
**∞ AbëONE ∞**

---

##  30-Second Setup

The Atomic Design System is **already built and ready**. No installation needed - all dependencies are in `products/apps/web/package.json`.

---

##  Three Ways to Use

### 1. Use Templates (Fastest)

```tsx
// Create a developer landing page in 30 seconds
import { LandingPageTemplate } from '../../atomic/templates/LandingPageTemplate'

export default function Page() {
  return (
    <LandingPageTemplate
      icp="developer"
      hero={{
        headline: "Your Headline",
        subheadline: "Your subheadline",
        primaryCTA: { label: "Get Started", href: "/signup" }
      }}
    />
  )
}
```

### 2. Use Organisms (More Control)

```tsx
// Build custom pages with organisms
import { HeroSection } from '../../atomic/organisms/HeroSection'
import { FeatureGrid } from '../../atomic/organisms/FeatureGrid'
import { CTASection } from '../../atomic/organisms/CTASection'

export default function Page() {
  return (
    <>
      <HeroSection
        headline="Build Better"
        variant="developer"
        primaryCTA={{ label: "Start", href: "/start" }}
      />
      <FeatureGrid features={[...]} variant="developer" />
      <CTASection headline="Ready?" primaryCTA={{ label: "Go" }} />
    </>
  )
}
```

### 3. Use Atoms/Molecules (Maximum Flexibility)

```tsx
// Build from scratch with atomic components
import { Button } from '../../atomic/atoms/Button'
import { Card } from '../../atomic/molecules/Card'
import { Text } from '../../atomic/atoms/Text'

export default function Page() {
  return (
    <Card variant="developer">
      <Text variant="developer" size="2xl">Hello</Text>
      <Button variant="developer">Click</Button>
    </Card>
  )
}
```

---

##  ICP Variants

Every component supports 4 ICP variants:

```tsx
variant="developer"   // Dark, mono fonts, technical
variant="creative"    // Gradients, elegant fonts, visual
variant="enterprise"  // Corporate, clean, metrics-focused
variant="default"     // Balanced, accessible
```

---

##  Common Patterns

### Developer Landing Page

```tsx
<LandingPageTemplate
  icp="developer"
  hero={{
    headline: "Build Better Software",
    subheadline: "Type-safe, fast, scalable",
    variant: "developer",
    primaryCTA: { label: "Get Started", href: "/signup" }
  }}
  features={[
    { title: "Type-Safe", description: "Full TypeScript", icon: Shield },
    { title: "Fast", description: "Optimized", icon: Zap }
  ]}
/>
```

### Webinar Registration Page

```tsx
<WebinarPageTemplate
  icp="developer"
  hero={{
    headline: "Master Atomic Design",
    date: "Tuesday, Jan 30",
    time: "2:00 PM EST",
    speaker: { name: "John Doe", title: "Architect" },
    primaryCTA: { label: "Register", href: "#register" }
  }}
  registrationForm={{
    onSubmit: (data) => console.log(data)
  }}
/>
```

### Enterprise Pricing Page

```tsx
<PricingTable
  variant="enterprise"
  tiers={[
    {
      name: "Starter",
      price: "$99",
      period: "month",
      features: ["Feature 1", "Feature 2"],
      cta: { label: "Start Trial" }
    }
  ]}
/>
```

---

##  Component Reference

### Atoms
- `Button` - Primary action button
- `Text` - Typography component
- `Input` - Form input field
- `Icon` - Icon from lucide-react
- `Badge` - Status badge
- `Image` - Image component
- `Link` - Navigation link

### Molecules
- `Card` - Container card
- `FormField` - Form field with label/error
- `CTAButton` - CTA button with loading/icon
- `MetricCard` - Metric display card
- `TestimonialCard` - Testimonial card

### Organisms
- `HeroSection` - Hero section with CTA
- `PricingTable` - Pricing tiers table
- `FeatureGrid` - Features grid
- `CTASection` - Final CTA section

### Templates
- `LandingPageTemplate` - Complete landing page
- `WebinarPageTemplate` - Webinar registration page

---

##  Full Documentation

- **README.md** - Complete system overview
- **AEYON_ATOMIC_SYSTEM_COMPLETE.md** - Full completion report
- **registry.json** - Component registry with orbital mappings
- **tokens/index.ts** - Design token definitions

---

##  Validation Checklist

Before deploying:
- [ ] ICP variant applied consistently
- [ ] CTA hierarchy correct (1 primary above fold)
- [ ] Mobile responsive
- [ ] Accessibility checked

---

**Pattern:** QUICK × START × GUIDE × ONE  
**Status:**  **READY**  
**∞ AbëONE ∞**

