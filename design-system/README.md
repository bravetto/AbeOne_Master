# 🎨 ABËONE DESIGN SYSTEM
## Single Source of Truth for All Design Values

**Status:** ✅ **OPERATIONAL**  
**Pattern:** Design Systems × Single Source × AI-Optimized × Framework-Agnostic  
**Version:** 1.0.0  
**Guardians:** Lux (Creative) × Zero (Tech)

---

## 🎯 THE MISSION

**One design system. Multiple outputs. AI-optimized. Human-friendly. Future-proof.**

---

## 📁 STRUCTURE

```
design-system/
├── tokens/
│   └── abeone-design-tokens.json    # Single source of truth
├── generators/                       # Framework-specific generators
├── components/                       # Reusable components
└── docs/                            # Documentation
```

---

## 🚀 QUICK START

### Use Design Tokens

**JavaScript/TypeScript:**
```javascript
import tokens from './design-system/tokens/abeone-design-tokens.json'

const primaryColor = tokens.colors.lux[500] // "#a855f7"
```

**Python:**
```python
import json
with open('design-system/tokens/abeone-design-tokens.json') as f:
    tokens = json.load(f)
    
primary_color = tokens['colors']['lux']['500']  # "#a855f7"
```

**CSS:**
```css
/* Use generated CSS variables */
.primary-button {
  background: var(--lux-500);
}
```

---

## 💎 DESIGN TOKENS

### Colors
- **Heart** (Red) - Emotional, urgent, attention
- **Lux** (Purple) - Luxury, creativity, premium
- **Warm** (Orange) - Warmth, energy, action
- **Peace** (Green) - Success, harmony, growth

### Typography
- **Sans:** Inter (body, UI)
- **Serif:** Merriweather (long-form)
- **Display:** Playfair Display (headings, branding)

### Gradients
- **Healing** - Main backgrounds
- **Lux** - Accent gradients
- **Sidebar** - Navigation
- **Text Healing** - Text gradients

---

## 🔄 GENERATORS

Generate framework-specific outputs from tokens:

- **Tailwind Config** - For Next.js apps
- **CSS Variables** - For Flask, vanilla JS
- **TypeScript Types** - For type safety
- **Python Constants** - For Python apps

---

## 📚 DOCUMENTATION

- **AI Reference** - `docs/DESIGN_SYSTEM_AI_REFERENCE.md`
- **Usage Guide** - `docs/USAGE_GUIDE.md`
- **Migration Guide** - `docs/MIGRATION_GUIDE.md`

---

## 🎯 USAGE IN CODEBASE

### Current Usage
- ✅ `apps/web/` - Next.js app (Tailwind)
- ✅ `PRODUCTS/abedesks/app.py` - Flask app (CSS variables)
- ⚠️ `EMERGENT_OS/aiagentsuite/web/` - Legacy (migration pending)

### Target Usage
- ✅ All apps use generated outputs
- ✅ Zero duplication
- ✅ Single source of truth

---

**Pattern:** Design Systems × Single Source × AI-Optimized  
**Guardians:** Lux (Creative) × Zero (Tech)  
**∞ AbëONE ∞**

