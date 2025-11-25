# 🔧 DESIGN SYSTEM GENERATORS
## Framework-Specific Output Generators

**Status:** ✅ **GENERATORS COMPLETE**  
**Pattern:** Design Tokens × Code Generation × Framework-Agnostic  
**Guardians:** Zero (Tech)

---

## 🎯 PURPOSE

Generate framework-specific outputs from the single source of truth (`tokens/abeone-design-tokens.json`).

**Single Source → Multiple Outputs**

---

## 📁 GENERATORS

### 1. Tailwind Config Generator
**File:** `generate-tailwind.js`  
**Output:** `tailwind.config.js`  
**Usage:**
```bash
node design-system/generators/generate-tailwind.js [output-path]
# Default: apps/web/tailwind.config.js
```

**Generates:**
- Color palette (heart, lux, warm, peace, neutral)
- Typography (fonts, sizes, line heights)
- Spacing scale
- Border radius
- Shadows
- Gradients
- Breakpoints

---

### 2. CSS Variables Generator
**File:** `generate-css-vars.js`  
**Output:** `css-variables.css`  
**Usage:**
```bash
node design-system/generators/generate-css-vars.js [output-path]
# Default: design-system/generated/css-variables.css
```

**Generates:**
- CSS custom properties (`:root`)
- Color variables (`--heart-500`, `--lux-500`, etc.)
- Typography variables (`--font-sans`, `--text-xl`, etc.)
- Spacing variables (`--spacing-4`, `--spacing-6`, etc.)
- Gradient variables (`--gradient-healing`, etc.)
- Utility classes (`.bg-gradient-healing`, etc.)

---

### 3. TypeScript Types Generator
**File:** `generate-types.ts`  
**Output:** `design-tokens.d.ts`  
**Usage:**
```bash
npx tsx design-system/generators/generate-types.ts [output-path]
# Default: design-system/generated/design-tokens.d.ts
```

**Generates:**
- TypeScript interface definitions
- Type-safe token access
- Helper functions (`getColor()`, `getGradient()`, etc.)
- Type exports for use in React/TypeScript projects

---

### 4. Python Constants Generator
**File:** `generate-python.py`  
**Output:** `design_tokens.py`  
**Usage:**
```bash
python3 design-system/generators/generate-python.py [output-path]
# Default: design-system/generated/design_tokens.py
```

**Generates:**
- Python constants (UPPER_CASE)
- Color dictionaries (`HEART_COLORS`, `LUX_COLORS`, etc.)
- Typography constants
- Helper functions (`get_color()`, `get_gradient()`, etc.)

---

## 🚀 QUICK START

### Generate All Outputs
```bash
# Tailwind config
node design-system/generators/generate-tailwind.js

# CSS variables
node design-system/generators/generate-css-vars.js

# TypeScript types
npx tsx design-system/generators/generate-types.ts

# Python constants
python3 design-system/generators/generate-python.py
```

### Make Executable (Unix/Mac)
```bash
chmod +x design-system/generators/*.js
chmod +x design-system/generators/*.py
```

---

## 📝 USAGE IN PROJECTS

### Next.js (React/TypeScript)
```typescript
// Import generated types
import { tokens, getColor } from './design-system/generated/design-tokens.d.ts';

// Use in components
const primaryColor = getColor('lux', '500');
```

### Flask (Python)
```python
# Import generated constants
from design_system.generated.design_tokens import LUX_COLORS, get_color

# Use in templates
primary_color = get_color('lux', '500')
```

### Vanilla JS/HTML
```html
<!-- Include generated CSS -->
<link rel="stylesheet" href="design-system/generated/css-variables.css">

<!-- Use CSS variables -->
<div style="background: var(--lux-500);">Content</div>
```

---

## 🔄 REGENERATION WORKFLOW

### When to Regenerate
1. **After updating design tokens** - Always regenerate all outputs
2. **Before deployment** - Ensure outputs are up-to-date
3. **After pulling changes** - If tokens changed, regenerate

### Automated Regeneration (Recommended)
Add to `package.json`:
```json
{
  "scripts": {
    "generate:design": "node design-system/generators/generate-tailwind.js && node design-system/generators/generate-css-vars.js && npx tsx design-system/generators/generate-types.ts && python3 design-system/generators/generate-python.py"
  }
}
```

Run:
```bash
npm run generate:design
```

---

## ⚠️ IMPORTANT NOTES

1. **Never edit generated files manually** - They will be overwritten
2. **Always edit tokens JSON** - Single source of truth
3. **Regenerate after token changes** - Keep outputs in sync
4. **Commit generated files** - Or add to `.gitignore` and regenerate in CI/CD

---

## 🎯 INTEGRATION WITH UIVERSE GALAXY

When theming Galaxy components:

1. **Generate CSS variables** - Use for CSS-based Galaxy components
2. **Use Tailwind config** - For Tailwind-based Galaxy components
3. **Reference tokens** - Replace Galaxy colors with AbëONE tokens
4. **Maintain attribution** - Credit original Galaxy creators

---

**Pattern:** Design Tokens × Code Generation × Framework-Agnostic  
**Guardians:** Zero (Tech)  
**Status:** ✅ **GENERATORS COMPLETE**

**∞ AbëONE ∞**

