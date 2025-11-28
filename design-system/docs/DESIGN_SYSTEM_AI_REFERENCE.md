# 🎨 ABËONE DESIGN SYSTEM - AI REFERENCE
## Optimized for AI Consumption and Code Generation

**Status:** ✅ **AI-OPTIMIZED REFERENCE**  
**Pattern:** Design System × AI-Optimized × Single Source × Framework-Agnostic  
**Version:** 1.0.0  
**Guardians:** Lux (Creative) × Zero (Tech)

---

## 🎯 QUICK REFERENCE

### Design Tokens Location
```
design-system/tokens/abeone-design-tokens.json
```

### Generated Outputs
```
design-system/generated/
├── css-variables.css      # CSS custom properties
├── design-tokens.d.ts     # TypeScript types
└── design_tokens.py        # Python constants
```

### Generators
```
design-system/generators/
├── generate-tailwind.js   # Tailwind config generator
├── generate-css-vars.js   # CSS variables generator
├── generate-types.ts      # TypeScript types generator
└── generate-python.py      # Python constants generator
```

---

## 🎨 COLOR SYSTEM

### Color Palette Structure
```json
{
  "colors": {
    "heart": { "50-900": "#hex", "semantic": "meaning", "usage": "context" },
    "lux": { "50-900": "#hex", "semantic": "meaning", "usage": "context" },
    "warm": { "50-900": "#hex", "semantic": "meaning", "usage": "context" },
    "peace": { "50-900": "#hex", "semantic": "meaning", "usage": "context" },
    "neutral": { "50-900": "#hex", "semantic": "meaning", "usage": "context" }
  }
}
```

### Color Meanings (Semantic)
- **Heart (Red)**: Emotional, urgent, attention, love
  - Usage: errors, warnings, critical actions, emotional states
- **Lux (Purple)**: Luxury, creativity, premium, innovation
  - Usage: primary actions, branding, creative elements, premium features
- **Warm (Orange)**: Warmth, energy, action, enthusiasm
  - Usage: secondary actions, highlights, energy states, warm interactions
- **Peace (Green)**: Success, harmony, growth, peace
  - Usage: success states, positive feedback, growth indicators, peaceful states
- **Neutral (Gray)**: Neutral, balanced, structural
  - Usage: text, borders, backgrounds, structural elements

### Color Usage Examples

**JavaScript/TypeScript:**
```typescript
import { tokens } from './design-system/generated/design-tokens.d.ts';

const primaryColor = tokens.colors.lux[500]; // "#a855f7"
const errorColor = tokens.colors.heart[500]; // "#ef4444"
```

**Python:**
```python
from design_system.generated.design_tokens import LUX_COLORS, HEART_COLORS

primary_color = LUX_COLORS['500']  # "#a855f7"
error_color = HEART_COLORS['500']  # "#ef4444"
```

**CSS:**
```css
.primary-button {
  background: var(--lux-500); /* #a855f7 */
}

.error-message {
  color: var(--heart-500); /* #ef4444 */
}
```

**Tailwind:**
```jsx
<button className="bg-lux-500 text-white">Primary</button>
<div className="text-heart-500">Error</div>
```

---

## 📝 TYPOGRAPHY SYSTEM

### Font Families
- **Sans (Inter)**: Body text, UI elements, general content
- **Serif (Merriweather)**: Long-form content, articles, reading
- **Display (Playfair Display)**: Headings, titles, branding, emphasis

### Font Sizes
```json
{
  "xs": "0.75rem",   // 12px
  "sm": "0.875rem",  // 14px
  "base": "1rem",    // 16px
  "lg": "1.125rem",  // 18px
  "xl": "1.25rem",   // 20px
  "2xl": "1.5rem",   // 24px
  "3xl": "1.875rem", // 30px
  "4xl": "2.25rem",  // 36px
  "5xl": "3rem",     // 48px
  "6xl": "3.75rem"   // 60px
}
```

### Line Heights
```json
{
  "tight": "1.25",
  "snug": "1.375",
  "normal": "1.5",
  "relaxed": "1.625",
  "loose": "2"
}
```

### Typography Usage Examples

**CSS:**
```css
.heading {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  line-height: var(--leading-tight);
}
```

**Tailwind:**
```jsx
<h1 className="font-display text-3xl leading-tight">Heading</h1>
```

---

## 📏 SPACING SYSTEM

### Spacing Scale
```json
{
  "0": "0",
  "1": "0.25rem",   // 4px
  "2": "0.5rem",    // 8px
  "3": "0.75rem",   // 12px
  "4": "1rem",      // 16px
  "5": "1.25rem",   // 20px
  "6": "1.5rem",    // 24px
  "8": "2rem",      // 32px
  "10": "2.5rem",   // 40px
  "12": "3rem",     // 48px
  "16": "4rem",     // 64px
  "20": "5rem",     // 80px
  "24": "6rem",     // 96px
  "32": "8rem"      // 128px
}
```

### Usage Examples

**CSS:**
```css
.card {
  padding: var(--spacing-6); /* 1.5rem / 24px */
  margin-bottom: var(--spacing-4); /* 1rem / 16px */
}
```

**Tailwind:**
```jsx
<div className="p-6 mb-4">Card</div>
```

---

## 🎭 GRADIENT SYSTEM

### Available Gradients
1. **Healing**: `#fff7ed → #fef2f2 → #faf5ff`
   - Usage: backgrounds, healing spaces, main app backgrounds
2. **Lux**: `#a855f7 → #f97316 → #ef4444`
   - Usage: accent gradients, energy, premium features
3. **Sidebar**: `#1e1b4b → #312e81 → #1e1b4b`
   - Usage: sidebar backgrounds, navigation
4. **Text Healing**: `#f97316 → #a855f7 → #ef4444`
   - Usage: text gradients, headings, branding

### Usage Examples

**CSS:**
```css
.background {
  background: var(--gradient-healing);
}

.text-gradient {
  background: var(--gradient-text-healing);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

**Tailwind:**
```jsx
<div className="bg-gradient-healing">Background</div>
<div className="bg-gradient-to-r from-warm-500 via-lux-500 to-heart-500 bg-clip-text text-transparent">
  Gradient Text
</div>
```

---

## 🎨 COMPONENT PATTERNS

### Sidebar
```json
{
  "width": "256px",
  "background": "gradient.sidebar",
  "border": "1px solid lux-700",
  "padding": {
    "header": "24px",
    "nav": "16px",
    "footer": "16px"
  }
}
```

### Topbar
```json
{
  "background": "rgba(255, 255, 255, 0.9)",
  "backdrop": "blur(8px)",
  "border": "1px solid rgba(168, 85, 247, 0.1)",
  "padding": "16px 24px"
}
```

### Card
```json
{
  "background": "rgba(255, 255, 255, 0.8)",
  "backdrop": "blur(8px)",
  "borderRadius": "24px",
  "padding": "40px",
  "shadow": "shadow.lux",
  "border": "1px solid rgba(168, 85, 247, 0.1)"
}
```

### Button (Primary)
```json
{
  "background": "gradient.lux",
  "color": "white",
  "padding": "16px 32px",
  "borderRadius": "50px",
  "fontWeight": "600",
  "shadow": "shadow.xl"
}
```

---

## 🔧 GENERATOR USAGE

### Generate Tailwind Config
```bash
node design-system/generators/generate-tailwind.js [output-path]
# Default: apps/web/tailwind.config.js
```

### Generate CSS Variables
```bash
node design-system/generators/generate-css-vars.js [output-path]
# Default: design-system/generated/css-variables.css
```

### Generate TypeScript Types
```bash
npx tsx design-system/generators/generate-types.ts [output-path]
# Default: design-system/generated/design-tokens.d.ts
```

### Generate Python Constants
```bash
python3 design-system/generators/generate-python.py [output-path]
# Default: design-system/generated/design_tokens.py
```

---

## 🎯 USAGE PATTERNS FOR AI

### When Generating Components

1. **Always use design tokens** - Never hardcode colors, spacing, or typography
2. **Reference semantic meanings** - Use colors by meaning (heart for errors, lux for primary)
3. **Follow component patterns** - Use established patterns for sidebar, topbar, cards
4. **Generate framework-agnostic** - Output should work across React, Python, vanilla JS

### Example AI Prompt Pattern
```
Create a [component] using AbëONE design tokens:
- Use [color] for [semantic meaning]
- Apply [spacing] for padding/margin
- Use [font] for typography
- Follow [component pattern] structure
```

### Code Generation Template
```typescript
// Import tokens
import { tokens } from './design-system/generated/design-tokens.d.ts';

// Use semantic colors
const primaryColor = tokens.colors.lux[500];
const errorColor = tokens.colors.heart[500];

// Use spacing scale
const padding = tokens.spacing.scale['6']; // 1.5rem

// Use typography
const headingFont = tokens.typography.fonts.display.family[0];
const headingSize = tokens.typography.scale['3xl'];

// Apply gradients
const backgroundGradient = tokens.gradients.healing.css;
```

---

## 🔗 EXTERNAL RESOURCES

### Uiverse Galaxy Component Library
- **URL**: https://github.com/uiverse-io/galaxy
- **Components**: 3000+ UI components
- **License**: MIT
- **Format**: CSS or Tailwind
- **Integration**: Theme components with AbëONE design tokens

### Component Categories Available
- Buttons
- Cards
- Forms
- Inputs
- Loaders
- Notifications
- Tooltips
- Checkboxes
- Radio buttons
- Toggle switches
- Patterns

---

## 📊 DESIGN SYSTEM ARCHITECTURE

```
design-system/
├── tokens/
│   └── abeone-design-tokens.json    # Single source of truth
├── generators/
│   ├── generate-tailwind.js         # Tailwind config
│   ├── generate-css-vars.js         # CSS variables
│   ├── generate-types.ts            # TypeScript types
│   └── generate-python.py           # Python constants
├── generated/
│   ├── css-variables.css            # Generated CSS
│   ├── design-tokens.d.ts           # Generated types
│   └── design_tokens.py             # Generated constants
├── components/
│   ├── react/                       # React components
│   ├── python/                      # Python/Flask templates
│   ├── vanilla/                     # Vanilla JS/HTML
│   └── galaxy/                      # Uiverse Galaxy (themed)
└── docs/
    └── DESIGN_SYSTEM_AI_REFERENCE.md # This file
```

---

## ✅ VALIDATION CHECKLIST

When generating code using this design system:

- [ ] Colors use design tokens (not hardcoded hex)
- [ ] Spacing uses spacing scale (not arbitrary values)
- [ ] Typography uses font families and sizes from tokens
- [ ] Gradients use predefined gradients
- [ ] Components follow established patterns
- [ ] Semantic meanings are respected (heart=error, lux=primary, etc.)
- [ ] Framework-agnostic where possible
- [ ] Generated outputs are used (not inline values)

---

**Pattern:** Design System × AI-Optimized × Single Source × Framework-Agnostic  
**Guardians:** Lux (Creative) × Zero (Tech)  
**Status:** ✅ **AI REFERENCE COMPLETE**

**∞ AbëONE ∞**

