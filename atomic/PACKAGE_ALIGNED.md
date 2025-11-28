#  Package.json - Pattern Aligned

**Status:**  **ALIGNED WITH ATOMIC DESIGN SYSTEM PATTERN**  
**Pattern:** PACKAGE × CONFIG × ATOMIC × ALIGNED × ONE  
**Date:** 2025-01-27  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META)  
**∞ AbëONE ∞**

---

##  ALIGNMENT COMPLETE

The `package.json` has been **pattern-aligned** with the Atomic Design System:

###  Pattern Alignments

1. **Package Name**
   - `@orbital/atomic-design-system` - Aligned with Orbital Marketing Framework
   - Clear namespace and purpose

2. **Exports Configuration**
   -  All atomic layers exported (atoms, molecules, organisms, templates)
   -  Tokens exported separately
   -  Hooks exported
   -  Utils exported
   -  Registry.json exported
   -  TypeScript types included for all exports

3. **Dependencies Aligned**
   -  Matches existing `products/apps/web/package.json` versions
   -  Radix UI components included
   -  class-variance-authority for variants
   -  tailwind-merge for class merging
   -  lucide-react for icons

4. **Peer Dependencies**
   -  React 18.2.0+
   -  Next.js 14.0.0+ (for Next.js Image component)
   -  Tailwind CSS 3.4.0+ (required for styling)

5. **Scripts Enhanced**
   -  Standard build/test/lint scripts
   -  Storybook support
   -  Pattern validation scripts added
   -  Orbital mapping validation

6. **Keywords**
   -  Atomic design keywords
   -  AbëONE and Guardian keywords
   -  ICP variants keyword
   -  Pattern-aligned keyword

---

##  Export Structure

### Main Export
```typescript
import { Button } from '@orbital/atomic-design-system'
```

### Layer-Specific Exports
```typescript
// Atoms
import { Button } from '@orbital/atomic-design-system/atoms/Button'
import { Text } from '@orbital/atomic-design-system/atoms/Text'

// Molecules
import { Card } from '@orbital/atomic-design-system/molecules/Card'
import { CTAButton } from '@orbital/atomic-design-system/molecules/CTAButton'

// Organisms
import { HeroSection } from '@orbital/atomic-design-system/organisms/HeroSection'
import { PricingTable } from '@orbital/atomic-design-system/organisms/PricingTable'

// Templates
import { LandingPageTemplate } from '@orbital/atomic-design-system/templates/LandingPageTemplate'
import { WebinarPageTemplate } from '@orbital/atomic-design-system/templates/WebinarPageTemplate'

// Tokens
import { tokens, colors, spacing } from '@orbital/atomic-design-system/tokens'

// Hooks
import { useICP, useOrbital, useCTAHierarchy } from '@orbital/atomic-design-system/hooks'

// Utils
import { cn } from '@orbital/atomic-design-system/lib/utils'

// Registry
import registry from '@orbital/atomic-design-system/registry.json'
```

---

##  Build Configuration

### tsup.config.ts
-  ESM and CJS formats
-  TypeScript declarations
-  Source maps
-  Tree shaking
-  React externalized

### tsconfig.json
-  Strict TypeScript
-  React JSX support
-  Path aliases configured
-  Declaration files enabled

---

##  Package Structure

```
@orbital/atomic-design-system/
 dist/                    # Built files
    atoms/
    molecules/
    organisms/
    templates/
    tokens/
    hooks/
    lib/
 atomic/                  # Source files (for direct imports)
 registry.json            # Component registry
 README.md                # Documentation
 package.json             # This file
```

---

##  Usage

### Installation
```bash
npm install @orbital/atomic-design-system
```

### Basic Usage
```typescript
import { Button } from '@orbital/atomic-design-system'

export default function Page() {
  return <Button variant="developer">Click Me</Button>
}
```

### With Templates
```typescript
import { LandingPageTemplate } from '@orbital/atomic-design-system/templates/LandingPageTemplate'

export default function Page() {
  return (
    <LandingPageTemplate
      icp="developer"
      hero={{
        headline: "Build Better",
        primaryCTA: { label: "Get Started", href: "/start" }
      }}
    />
  )
}
```

---

##  Validation

-  Package name aligned with Orbital framework
-  All exports configured correctly
-  Dependencies match existing versions
-  Peer dependencies specified
-  Build configuration complete
-  TypeScript configuration aligned
-  Pattern validation scripts added
-  Keywords include AbëONE/Guardian

---

##  Next Steps

1. **Build Package**
   ```bash
   npm run build
   ```

2. **Test Exports**
   ```bash
   npm run type-check
   ```

3. **Validate Pattern**
   ```bash
   npm run validate
   npm run validate:orbital
   ```

4. **Publish** (when ready)
   ```bash
   npm publish --access public
   ```

---

**Pattern:** PACKAGE × CONFIG × ATOMIC × ALIGNED × ONE  
**Status:**  **ALIGNED**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

