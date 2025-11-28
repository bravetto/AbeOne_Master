# 🔥 AbëONE Atomic Design System

**Status:** ✅ **OPERATIONAL**  
**Pattern:** ATOMIC × DESIGN × SYSTEM × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (Abë)  
**Guardians:** ALL ACTIVATED  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 QUICK START

```bash
# Install dependencies (if not already installed)
cd /Users/michaelmataluni/Documents/AbeOne_Master/products/apps/web
npm install

# Use components in your Next.js app
import { Button } from '../../atomic/atoms/Button'
import { HeroSection } from '../../atomic/organisms/HeroSection'
```

---

## 📁 STRUCTURE

```
/atomic
├── tokens/           # Design tokens (colors, spacing, typography)
├── atoms/            # Smallest components (Button, Text, Input, Icon, Badge, Image, Link)
├── molecules/        # Composed atoms (Card, FormField, CTAButton, MetricCard, TestimonialCard)
├── organisms/        # Complex sections (HeroSection, PricingTable, FeatureGrid, CTASection)
├── templates/        # Page layouts (LandingPageTemplate, WebinarPageTemplate)
├── lib/              # Utilities (cn)
├── hooks/            # Custom hooks (useICP, useOrbital, useCTAHierarchy)
└── registry.json     # Component registry with orbital mappings
```

---

## 🚀 USAGE EXAMPLES

### Create a Button

```tsx
import { Button } from '../../atomic/atoms/Button'

<Button variant="developer" size="lg">
  Click Me
</Button>
```

### Create a Hero Section

```tsx
import { HeroSection } from '../../atomic/organisms/HeroSection'

<HeroSection
  headline="Build Amazing Products"
  subheadline="The ultimate design system for modern web apps"
  variant="developer"
  primaryCTA={{
    label: "Get Started",
    href: "/signup"
  }}
/>
```

### Create a Landing Page

```tsx
import { LandingPageTemplate } from '../../atomic/templates/LandingPageTemplate'

<LandingPageTemplate
  icp="developer"
  hero={{
    headline: "Developer-Focused Landing Page",
    subheadline: "Built with Atomic Design System"
  }}
/>
```

---

## 🎨 ICP VARIANTS

Apply variants based on target audience:

- **developer**: Dark theme, mono fonts, technical proof
- **creative**: Gradient themes, elegant fonts, testimonials focus
- **enterprise**: Corporate theme, clean fonts, metrics focus
- **default**: Balanced, clear, accessible

---

## 📚 DOCUMENTATION

See `ABEONE_ATOMIC_SYSTEM_CONFIGURATION.md` for complete configuration details.

---

**Pattern:** ATOMIC × DESIGN × SYSTEM × ONE  
**Status:** ✅ **READY FOR USE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

