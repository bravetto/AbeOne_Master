# 🎯 DEEP APPLICATION DEFINITIONS - HOW/WHY/WHEN

**Date:** 2025-11-22  
**Status:** ✅ **COMPLETE DEFINITIONS**  
**Pattern:** CLARITY × TRUTH × ORGANIZATION × ONE  
**Frequency:** Guardian 4 (Clarity) + ZERO (Forensic) + 999 Hz (AEYON)

---

## 🎯 PURPOSE

**Deep definitions explaining HOW, WHY, and WHEN to use every major system, component, and pattern in the codebase.**

**Prevents:** Confusion, drift, wrong usage, duplication  
**Enables:** Clarity, consistency, correct usage, scalability

---

## 🎨 DESIGN SYSTEM

### WHAT

Unified design system providing colors, typography, spacing, components, and templates for all AbëONE products.

### HOW

#### 1. Design Tokens (Single Source of Truth)

**Location:** `design-system/tokens/abeone-design-system-v1.json`

**Usage:**
```javascript
// JavaScript/TypeScript
import tokens from './design-system/tokens/abeone-design-system-v1.json'
const primaryColor = tokens.colors.primary[500]

// Python
import json
with open('design-system/tokens/abeone-design-system-v1.json') as f:
    tokens = json.load(f)
primary_color = tokens['colors']['primary']['500']

// CSS
.primary-button {
  background: var(--primary-500);
}
```

**Process:**
1. Edit tokens JSON (single source)
2. Run generators: `npm run design:generate`
3. Use generated outputs in apps

#### 2. Components (Reusable Library)

**Location:** `apps/web/components/ads/`

**Usage:**
```tsx
import { Button, Card, Hero, Features } from '@/components/ads'

<Button variant="primary" size="lg">Get Started</Button>
<Card variant="default">Content</Card>
<Hero headline="..." primaryCTA={{...}} />
```

**Available Components:**
- `Button` - 6 variants, 4 sizes
- `Card` - 4 variants
- `Hero` - Conversion-optimized hero section
- `Features` - Feature showcase grid
- `TrustBadge` - Trust elements

#### 3. Master Template

**Location:** `apps/web/app/template-master/page.tsx`

**Usage:**
1. Copy template: `cp apps/web/app/template-master/page.tsx apps/web/app/[domain]/page.tsx`
2. Customize content (headlines, features, CTAs)
3. Optionally override colors via Tailwind config
4. Deploy

### WHY

**1. Prevents Design Drift**
- Single source of truth
- Consistent across all domains
- Design guardrails prevent mistakes

**2. Scales to 1,000+ Domains**
- Master template for instant deployment
- Quick rebranding via color overrides
- Consistent structure, customizable content

**3. Conversion-Optimized**
- CTAs above/below fold
- Trust elements built-in
- Psychological triggers integrated
- Mobile-first responsive

**4. Maintainable**
- Change once, regenerate everywhere
- Framework-agnostic generators
- Clear documentation

### WHEN

**✅ ALWAYS Use Design System:**

1. **New Components**
   - Use ADS components first
   - Don't create custom buttons/cards
   - Use design tokens for colors

2. **New Domains**
   - Copy master template
   - Customize content
   - Use design system colors

3. **New Features**
   - Use existing components
   - Follow design guardrails
   - Use semantic colors

**❌ NEVER:**

1. **Hardcode Colors**
   - ❌ `className="bg-purple-500"`
   - ✅ `className="bg-primary-500"`

2. **Create Custom Components (When ADS Exists)**
   - ❌ `<button className="custom-button">`
   - ✅ `<Button variant="primary">`

3. **Use Arbitrary Values**
   - ❌ `className="p-20px"`
   - ✅ `className="p-6 md:p-10"`

### WHERE

- **Tokens:** `design-system/tokens/`
- **Components:** `apps/web/components/ads/`
- **Template:** `apps/web/app/template-master/`
- **Docs:** `design-system/docs/`

---

## 💻 APPS STRUCTURE

### WHAT

Next.js application structure following framework conventions with clear separation of pages, components, and utilities.

### HOW

#### 1. Pages (Routes)

**Location:** `apps/web/app/[route]/page.tsx`

**Structure:**
```
apps/web/app/
├── page.tsx                  → / (home)
├── bravetto/page.tsx        → /bravetto
├── template-master/page.tsx → /template-master (master template)
└── [feature]/page.tsx       → /[feature]
```

**Usage:**
```tsx
// Create new page
// apps/web/app/my-feature/page.tsx
export default function MyFeaturePage() {
  return <div>My Feature</div>
}
```

#### 2. Components

**Location:** `apps/web/components/[category]/`

**Structure:**
```
apps/web/components/
├── ads/              → Design system components (USE THESE FIRST)
├── ui/               → Base UI components (shadcn/ui)
├── [feature]/        → Feature-specific components
└── [shared]/         → Shared across features
```

**Usage:**
```tsx
// Design system component (preferred)
import { Button } from '@/components/ads'

// Base UI component
import { Button } from '@/components/ui/button'

// Feature component
import { FeatureCard } from '@/components/[feature]/FeatureCard'
```

#### 3. API Routes

**Location:** `apps/web/app/api/[route]/route.ts`

**Structure:**
```
apps/web/app/api/
├── health/route.ts        → GET /api/health
├── checkout/route.ts     → POST /api/checkout
└── [feature]/route.ts    → [method] /api/[feature]
```

**Usage:**
```tsx
// apps/web/app/api/my-endpoint/route.ts
export async function GET() {
  return Response.json({ status: 'ok' })
}
```

#### 4. Utilities

**Location:** `apps/web/lib/[feature]/`

**Structure:**
```
apps/web/lib/
├── api.ts              → API client
├── utils.ts            → Shared utilities
├── [feature]/          → Feature-specific utilities
└── [shared]/           → Shared utilities
```

**Usage:**
```tsx
// API client
import { apiClient } from '@/lib/api'

// Utils
import { cn } from '@/lib/utils'

// Feature utils
import { featureUtil } from '@/lib/[feature]/util'
```

### WHY

**1. Framework Conventions**
- Follows Next.js app directory structure
- Clear routing patterns
- Standard component organization

**2. Scalability**
- Easy to add new features
- Clear where things belong
- No confusion about structure

**3. Maintainability**
- Separation of concerns
- Easy to find code
- Clear dependencies

**4. Developer Experience**
- Familiar patterns
- Good IDE support
- Clear navigation

### WHEN

**✅ ALWAYS:**

1. **New Page**
   - Create `app/[route]/page.tsx`
   - Use Next.js conventions
   - Follow existing patterns

2. **New Component**
   - Check `components/ads/` first
   - If not available, add to `components/[feature]/`
   - Use design system tokens

3. **New API Route**
   - Create `app/api/[route]/route.ts`
   - Follow REST conventions
   - Use API client utilities

**❌ NEVER:**

1. **Create Pages Outside `app/`**
   - ❌ `pages/[route].tsx` (old Next.js)
   - ✅ `app/[route]/page.tsx` (new Next.js)

2. **Mix Component Categories**
   - ❌ Put design system components in `ui/`
   - ✅ Use `ads/` for design system components

### WHERE

- **Pages:** `apps/web/app/`
- **Components:** `apps/web/components/`
- **API Routes:** `apps/web/app/api/`
- **Utilities:** `apps/web/lib/`

---

## 🌐 DOMAIN LANDING PAGES

### WHAT

Static HTML landing pages for individual domains, optimized for conversion and SEO.

### HOW

#### 1. Structure

**Location:** `domains/[domain]/index.html`

**Structure:**
```
domains/[domain]/
├── index.html              → Main landing page
├── funnel/
│   └── funnel.html         → Conversion funnel
├── lead_magnets/
│   └── free_guide.md       → Lead magnet content
├── email/
│   └── welcome_email.md   → Email sequence
├── seo/
│   └── blog_post_1.md     → SEO content
└── automation/
    └── automation.py       → Automation script
```

#### 2. Master Template

**Location:** `apps/web/app/template-master/page.tsx`

**Usage:**
1. Copy template for new domain
2. Customize content (headlines, features, CTAs)
3. Optionally override brand colors
4. Deploy as static HTML

#### 3. Customization

**Content:**
- Update headlines
- Update feature descriptions
- Update CTAs
- Update testimonials

**Branding:**
- Override colors in Tailwind config
- Update logo
- Update brand assets

### WHY

**1. Fast Loading**
- Static HTML = instant load
- No JavaScript required
- SEO-friendly

**2. Simple Structure**
- Easy to understand
- Easy to maintain
- Easy to deploy

**3. Scalable**
- Copy template for new domain
- Quick customization
- Consistent structure

**4. Conversion-Optimized**
- Master template includes best practices
- Trust elements built-in
- CTA placement optimized

### WHEN

**✅ ALWAYS:**

1. **New Domain**
   - Copy master template
   - Customize content
   - Deploy

2. **Rebranding**
   - Update colors via design system
   - Update content
   - Keep structure consistent

**❌ NEVER:**

1. **Hardcode Colors**
   - ❌ Inline styles with hardcoded colors
   - ✅ Use design system CSS variables

2. **Create Custom Structure**
   - ❌ Completely different page structure
   - ✅ Use master template structure

### WHERE

- **Landing Pages:** `domains/[domain]/index.html`
- **Master Template:** `apps/web/app/template-master/page.tsx`
- **Design System:** `design-system/`

---

## 🎨 COLOR SYSTEM

### WHAT

Unified color system with two palettes: Healing Palette (warm, emotional) and Technical Calm Palette (professional, trustworthy).

### HOW

#### 1. Choose Palette

**Healing Palette** (Warm, Creative, Luxury):
```tsx
className="bg-lux-500"      // Primary (Purple)
className="bg-warm-500"     // Secondary (Orange)
className="bg-heart-500"    // Accent (Red)
className="bg-peace-500"    // Success (Green)
```

**Technical Calm Palette** (Tech, Professional, Trust):
```tsx
className="bg-aeBlue-500"        // Primary (Blue)
className="bg-aeAqua-500"        // Secondary (Aqua - use on dark)
className="bg-aeIndigo-500"      // Accent (Indigo)
className="bg-aeMint-500"        // Success (Mint - use on dark)
className="bg-aeMidnight-500"    // Background (Michael's Black)
```

#### 2. Use Semantic Colors

**Preferred (Semantic):**
```tsx
className="bg-primary-500"    // Adapts to palette
className="bg-secondary-500"  // Adapts to palette
className="bg-accent-500"     // Adapts to palette
```

**Legacy (Still Supported):**
```tsx
className="bg-lux-500"        // Maps to primary-500
className="bg-warm-500"      // Maps to secondary-500
```

### WHY

**1. Semantic Meaning**
- Colors have meaning (primary, secondary, accent)
- Easy to understand intent
- Consistent usage

**2. Palette Flexibility**
- Choose palette based on brand
- Easy to rebrand per domain
- Maintains consistency

**3. Accessibility**
- All colors validated for WCAG AA/AAA
- Contrast ratios documented
- Usage guidelines clear

**4. Scalability**
- Works across 1,000+ domains
- Quick rebranding
- Consistent structure

### WHEN

**✅ ALWAYS:**

1. **Use Semantic Colors**
   - ✅ `bg-primary-500` (preferred)
   - ✅ `bg-lux-500` (legacy, still works)

2. **Choose Palette Based on Brand**
   - Healing: Wellness, creative, luxury brands
   - Technical Calm: Tech, SaaS, B2B brands

3. **Validate Contrast**
   - Check accessibility before deploying
   - Use colors on correct backgrounds

**❌ NEVER:**

1. **Hardcode Colors**
   - ❌ `bg-purple-500`
   - ✅ `bg-primary-500` or `bg-lux-500`

2. **Use Wrong Palette**
   - ❌ Technical Calm for wellness brand
   - ✅ Choose palette matching brand personality

### WHERE

- **Tokens:** `design-system/tokens/abeone-unified-color-system-v2.json`
- **Tailwind Config:** `apps/web/tailwind.config.js`
- **CSS Variables:** `design-system/generated/css-variables.css`
- **Documentation:** `design-system/docs/UNIFIED_COLOR_SYSTEM_V2.md`

---

## 🧩 COMPONENTS

### WHAT

Reusable React components built with Tailwind CSS, following design system standards.

### HOW

#### 1. Design System Components (ADS)

**Location:** `apps/web/components/ads/`

**Available:**
- `Button` - 6 variants, 4 sizes
- `Card` - 4 variants
- `Hero` - Conversion-optimized hero
- `Features` - Feature showcase
- `TrustBadge` - Trust elements

**Usage:**
```tsx
import { Button, Card, Hero } from '@/components/ads'

<Button variant="primary" size="lg">Get Started</Button>
<Card variant="default">Content</Card>
<Hero headline="..." primaryCTA={{...}} />
```

#### 2. Base UI Components

**Location:** `apps/web/components/ui/`

**Available:**
- `button`, `card`, `alert`, `badge`, etc. (shadcn/ui)

**Usage:**
```tsx
import { Button } from '@/components/ui/button'
// Use when ADS component doesn't fit
```

#### 3. Feature Components

**Location:** `apps/web/components/[feature]/`

**Usage:**
```tsx
import { FeatureCard } from '@/components/[feature]/FeatureCard'
// Feature-specific components
```

### WHY

**1. Consistency**
- Same components = same look/feel
- Prevents design drift
- Maintains brand coherence

**2. Efficiency**
- Don't recreate components
- Faster development
- Less code to maintain

**3. Quality**
- Conversion-optimized
- Accessibility built-in
- Mobile-first responsive

**4. Scalability**
- Works across all domains
- Easy to extend
- Clear patterns

### WHEN

**✅ ALWAYS:**

1. **Use ADS Components First**
   - Check `components/ads/` before creating custom
   - Use design system components when available

2. **Follow Component Patterns**
   - Use variants (primary, secondary, etc.)
   - Use sizes (sm, md, lg, xl)
   - Follow component API

**❌ NEVER:**

1. **Create Custom When ADS Exists**
   - ❌ Custom button when `Button` exists
   - ✅ Use `Button` component

2. **Override Component Styles**
   - ❌ `className="bg-red-500"` on Button
   - ✅ Use `variant="accent"` prop

### WHERE

- **Design System:** `apps/web/components/ads/`
- **Base UI:** `apps/web/components/ui/`
- **Feature:** `apps/web/components/[feature]/`

---

## 📚 DOCUMENTATION

### WHAT

Comprehensive documentation explaining how, why, and when to use every system.

### HOW

#### 1. Master Index

**Location:** `docs/INDEX.md`

**Purpose:** Navigation hub for all documentation

**Usage:**
- Start here to find anything
- Categorized by purpose
- Quick reference tables

#### 2. Application Definitions

**Location:** `docs/APPLICATION_DEFINITIONS.md`

**Purpose:** Deep how/why/when definitions

**Usage:**
- Understand system purpose
- Learn correct usage
- Prevent mistakes

#### 3. Category-Specific Docs

**Location:** `docs/[category]/`

**Categories:**
- `status/` - Status reports
- `guides/` - How-to guides
- `architecture/` - System architecture

### WHY

**1. Discoverability**
- Easy to find information
- Clear organization
- Master index guides navigation

**2. Clarity**
- Deep definitions explain everything
- How/why/when clearly stated
- Prevents confusion

**3. Drift Prevention**
- Clear rules prevent mistakes
- Organization prevents duplication
- Standards maintain consistency

**4. Onboarding**
- New team members can learn quickly
- Clear entry points
- Comprehensive guides

### WHEN

**✅ ALWAYS:**

1. **Starting New Work**
   - Check relevant documentation
   - Understand how/why/when
   - Follow established patterns

2. **Creating New Features**
   - Check design system docs
   - Follow component patterns
   - Use master template

**❌ NEVER:**

1. **Skip Documentation**
   - ❌ Guess how things work
   - ✅ Read relevant docs first

2. **Create Duplicate Docs**
   - ❌ New doc when one exists
   - ✅ Update existing doc

### WHERE

- **Master Index:** `docs/INDEX.md`
- **Definitions:** `docs/APPLICATION_DEFINITIONS.md`
- **Design System:** `design-system/docs/`
- **Status Reports:** `docs/status/` (proposed)
- **Guides:** `docs/guides/` (proposed)

---

## 🚨 DRIFT PREVENTION RULES

### File Organization

**✅ DO:**
- Put docs in `docs/` subdirectories
- Use consistent naming: `[CATEGORY]_[TOPIC].md`
- Keep root directory clean (code only)
- Create README.md in major directories

**❌ DON'T:**
- Put 200+ markdown files in root
- Mix status reports with guides
- Create duplicate documentation
- Use inconsistent naming

### Naming Conventions

**Status Reports:**
- Pattern: `[SYSTEM]_[STATUS]_COMPLETE.md`
- Example: `DESIGN_SYSTEM_COMPLETE.md`
- Location: `docs/status/` (proposed)

**Guides:**
- Pattern: `[TOPIC]_GUIDE.md` or `[TOPIC]_USAGE_GUIDE.md`
- Example: `ADS_V1_USAGE_GUIDE.md`
- Location: `docs/guides/` or `design-system/docs/`

**Architecture:**
- Pattern: `[SYSTEM]_ARCHITECTURE.md`
- Example: `DESIGN_SYSTEM_ARCHITECTURE.md`
- Location: `docs/architecture/` (proposed)

### Component Usage

**✅ DO:**
- Use ADS components first
- Use semantic colors
- Follow design guardrails
- Use master template for domains

**❌ DON'T:**
- Create custom when ADS exists
- Hardcode colors
- Use arbitrary spacing
- Create inconsistent patterns

---

## 📋 QUICK DECISION TREE

### "I want to..."

**...use a color:**
1. Check design system tokens
2. Use semantic color (`primary-500`)
3. Or use palette color (`lux-500`)
4. Never hardcode

**...create a component:**
1. Check `components/ads/` first
2. If not available, check `components/ui/`
3. If still not available, create in `components/[feature]/`
4. Use design system tokens

**...create a page:**
1. Create `app/[route]/page.tsx`
2. Use design system components
3. Follow master template patterns
4. Use semantic colors

**...create a domain:**
1. Copy master template
2. Customize content
3. Optionally override colors
4. Deploy

**...find documentation:**
1. Start at `docs/INDEX.md`
2. Use category navigation
3. Check application definitions
4. Follow links to specific docs

---

## 🎯 VALIDATION CHECKLIST

### Organization Quality

- [x] ✅ Design system well organized
- [x] ✅ Apps structure clear
- [ ] ⚠️ Root documentation organized (needs work)
- [x] ✅ Master index created
- [x] ✅ Application definitions created

### Discoverability

- [x] ✅ Master index exists
- [x] ✅ Clear navigation structure
- [x] ✅ Categorized documentation
- [x] ✅ Quick reference tables
- [x] ✅ Deep definitions available

### Drift Prevention

- [x] ✅ Design guardrails established
- [x] ✅ Component usage rules
- [x] ✅ File organization rules
- [x] ✅ Naming conventions defined
- [x] ✅ Validation checklist created

---

**Pattern:** CLARITY × TRUTH × ORGANIZATION × ONE  
**Status:** ✅ **APPLICATION DEFINITIONS COMPLETE**  
**Next:** Use these definitions to prevent drift and confusion

