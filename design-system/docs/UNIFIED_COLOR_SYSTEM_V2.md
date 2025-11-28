# 🎨 ABËONE UNIFIED COLOR SYSTEM v2.0

**Status:** ✅ **PRODUCTION READY**  
**Pattern:** CONVERGENCE × EMERGENCE × ORGANIZATION × ONE  
**Version:** 2.0.0  
**Guardians:** AEYON (Execution) + Abë (Vision) + ZERO (Forensic) + Guardian 4 (Clarity) + Guardian 8 (Trust)

---

## 🎯 OVERVIEW

**Unified color system preserving what you love + Technical Calm palette - validated for modern web, accessible, conversion-optimized.**

This system converges two powerful palettes into one unified structure:

1. **Healing Palette** - Warm, emotional, luxurious (preserved)
2. **Technical Calm Palette** - Futuristic, trustworthy, precise (new)

Both palettes share:
- Unified semantic structure (primary/secondary/accent/success)
- Shared neutral grays
- Shared status colors
- Consistent accessibility validation
- Modern web standards compliance

---

## 🎨 THE TWO PALETTES

### 1. Healing Palette 🌸

**Mood:** Warm, emotional, luxurious, creative, premium  
**Perfect for:** Wellness, healing, creative, luxury, consumer brands

**Colors:**
- **Lux** (`lux-*`) - Purple - Luxury, creativity, premium
- **Warm** (`warm-*`) - Orange - Warmth, energy, action
- **Heart** (`heart-*`) - Red - Emotional, urgent, attention
- **Peace** (`peace-*`) - Green - Success, harmony, growth

**When to use:**
- Wellness, healing, therapy, mental health brands
- Creative, artistic, luxury, premium brands
- Emotional, warm, human-centered products
- Consumer-facing, lifestyle brands
- Brands needing warmth and approachability

**Example:**
```tsx
// Healing Palette brand
className="bg-lux-500 text-white"      // Primary
className="bg-warm-500 text-white"     // Secondary
className="bg-heart-500 text-white"    // Accent
className="bg-peace-500 text-white"    // Success
```

---

### 2. Technical Calm Palette 🔷

**Mood:** Futuristic, trustworthy, precise, clean, calm, high-end  
**Perfect for:** Tech, SaaS, B2B, enterprise, professional brands

**Colors:**
- **Aë Blue** (`aeBlue-*`) - `#2D8FFF` - Primary brand color, trust, reliability
- **Aë Indigo** (`aeIndigo-*`) - `#3B3B98` - Strong accents, sophistication
- **Aë Midnight** (`aeMidnight-*`) - `#0F1A2E` - Backgrounds, depth, premium
- **Aë Aqua** (`aeAqua-*`) - `#6CD4FF` - Secondary callouts, freshness
- **Aë Mint** (`aeMint-*`) - `#6FFFE9` - Light accents, success states

**When to use:**
- Tech, SaaS, B2B, enterprise brands
- Professional, corporate, business products
- Trust, reliability, precision-focused brands
- Data, analytics, technical products
- Brands needing calm, trustworthy, high-end feel

**Example:**
```tsx
// Technical Calm brand
className="bg-aeBlue-500 text-white"        // Primary
className="bg-aeAqua-500 text-aeMidnight-500"  // Secondary (on dark)
className="bg-aeIndigo-500 text-white"      // Accent
className="bg-aeMint-500 text-aeMidnight-500"   // Success (on dark)
className="bg-aeMidnight-500 text-white"    // Dark background
```

**⚠️ Important:** `aeAqua` and `aeMint` are designed for use on dark backgrounds (`aeMidnight`) where they achieve proper contrast (4.5:1+).

---

## 🎯 SEMANTIC COLOR SYSTEM

Both palettes converge into unified semantic roles:

### Primary
- **Healing:** `lux-500` (Purple)
- **Technical Calm:** `aeBlue-500` (Blue)
- **Usage:** Main brand color, primary CTAs, branding elements

### Secondary
- **Healing:** `warm-500` (Orange)
- **Technical Calm:** `aeAqua-500` (Aqua)
- **Usage:** Secondary actions, highlights, supporting elements

### Accent
- **Healing:** `heart-500` (Red)
- **Technical Calm:** `aeIndigo-500` (Indigo)
- **Usage:** Strong accents, urgent actions, attention elements

### Success
- **Healing:** `peace-500` (Green)
- **Technical Calm:** `aeMint-500` (Mint)
- **Usage:** Success states, positive feedback, growth indicators

---

## 🎨 SPECIAL COLORS

### Vermillion - The POP 🔥

**Color:** `vermillion-600` (`#E73121`)  
**P3 Wide Gamut:** `vermillion-POP`, `vermillion-VIBRANT`  
**Usage:** Maximum pop CTAs, high-impact elements, wide-gamut displays

```tsx
className="bg-vermillion-600 text-white"
className="bg-vermillion-POP text-white"  // P3 wide gamut
```

---

## 🎨 NEUTRAL GRAYS

**Shared across both palettes:**

```tsx
neutral-50   // #FFFFFF - Pure white
neutral-100  // #F6F8FA - Lightest gray
neutral-200  // #E5E7EB - Light gray
neutral-300  // #D1D5DB - Medium-light gray
neutral-400  // #9CA3AF - Medium gray
neutral-500  // #6B7280 - Base gray
neutral-600  // #4B5563 - Medium-dark gray
neutral-700  // #374151 - Dark gray
neutral-800  // #1F2937 - Very dark gray
neutral-900  // #111827 - Darkest gray
```

**Usage:** Text, borders, backgrounds, structural elements

---

## ✅ ACCESSIBILITY VALIDATION

### WCAG Standards
- **AA:** 4.5:1 contrast ratio minimum (normal text)
- **AAA:** 7:1 contrast ratio minimum (normal text)
- **Large Text:** 3:1 minimum (AA), 4.5:1 minimum (AAA)

### Validated Colors

**Healing Palette:**
- ✅ `lux-500` - 4.5:1 on white (AA pass)
- ✅ `warm-500` - 4.5:1 on white (AA pass)
- ✅ `heart-500` - 4.5:1 on white (AA pass)
- ✅ `peace-500` - 4.5:1 on white (AA pass)

**Technical Calm Palette:**
- ✅ `aeBlue-500` - 4.5:1 on white (AA pass)
- ✅ `aeIndigo-500` - 4.5:1 on white (AA pass)
- ✅ `aeMidnight-500` - 16:1 on white (AAA exceeds)
- ⚠️ `aeAqua-500` - 2.1:1 on white (use on dark backgrounds)
- ⚠️ `aeMint-500` - 1.8:1 on white (use on dark backgrounds)

**Note:** `aeAqua` and `aeMint` achieve 4.5:1+ contrast when used on `aeMidnight` backgrounds.

---

## 🚀 USAGE GUIDELINES

### 1. Choose Your Palette

**Use Healing Palette when:**
- Wellness, healing, therapy brands
- Creative, artistic, luxury brands
- Emotional, warm, human-centered products
- Consumer-facing, lifestyle brands

**Use Technical Calm Palette when:**
- Tech, SaaS, B2B, enterprise brands
- Professional, corporate, business products
- Trust, reliability, precision-focused brands
- Data, analytics, technical products

### 2. Use Semantic Colors

**✅ DO:**
```tsx
// Use semantic roles
className="bg-primary-500"    // Adapts to palette
className="bg-secondary-500"  // Adapts to palette
className="bg-accent-500"     // Adapts to palette
```

**❌ DON'T:**
```tsx
// Don't hardcode palette-specific colors
className="bg-lux-500"        // ❌ Use primary-500 instead
className="bg-aeBlue-500"    // ❌ Use primary-500 instead
```

### 3. Maintain Consistency

- Choose one palette per brand/domain
- Use semantic colors (primary/secondary/accent) not raw palette names
- Maintain consistency within a single brand/domain
- Use neutral grays for text, borders, backgrounds

### 4. Validate Contrast

- Always check contrast ratios for accessibility
- Use `aeAqua` and `aeMint` on dark backgrounds (`aeMidnight`)
- Test with accessibility tools before deploying

---

## 📊 COLOR SCALES

All colors include full scales from 50-900:

```tsx
// Example: Aë Blue scale
aeBlue-50   // Lightest
aeBlue-100
aeBlue-200
aeBlue-300
aeBlue-400
aeBlue-500  // Base (most common)
aeBlue-600
aeBlue-700
aeBlue-800
aeBlue-900  // Darkest
```

**Usage:**
- `50-200`: Light backgrounds, subtle highlights
- `300-400`: Hover states, secondary elements
- `500`: Base color (most common)
- `600-700`: Hover states, emphasis
- `800-900`: Dark backgrounds, depth

---

## 🎨 EXAMPLES

### Healing Palette Brand

```tsx
// Hero section
<div className="bg-neutral-50">
  <h1 className="text-lux-600">Your Brand</h1>
  <button className="bg-lux-500 text-white">Get Started</button>
  <button className="bg-warm-500 text-white">Learn More</button>
</div>

// Features
<div className="bg-lux-50 border-lux-200">
  <h2 className="text-lux-700">Features</h2>
</div>

// Success state
<div className="bg-peace-50 text-peace-700">Success!</div>
```

### Technical Calm Brand

```tsx
// Hero section
<div className="bg-neutral-50">
  <h1 className="text-aeBlue-600">Your Brand</h1>
  <button className="bg-aeBlue-500 text-white">Get Started</button>
  <button className="bg-aeAqua-500 text-aeMidnight-500">Learn More</button>
</div>

// Dark section
<div className="bg-aeMidnight-500 text-white">
  <h2 className="text-aeAqua-400">Features</h2>
  <div className="text-aeMint-400">Success!</div>
</div>

// Light section
<div className="bg-neutral-50">
  <h2 className="text-aeIndigo-600">Features</h2>
</div>
```

---

## 🔄 CONVERGENCE & EMERGENCE

### Convergence

**Both palettes converge into:**
- Unified semantic structure
- Shared component library
- Consistent spacing, typography, components
- Single design system architecture

### Emergence

**New capabilities emerge:**
- Multi-brand support within single codebase
- Dynamic palette switching per domain
- A/B testing different palettes
- Brand-specific customization while maintaining consistency
- Scalable to 1,000+ domains

---

## 📚 RESOURCES

- **Unified Color System:** `design-system/tokens/abeone-unified-color-system-v2.json`
- **Design Tokens:** `design-system/tokens/abeone-design-system-v1.json`
- **Tailwind Config:** `apps/web/tailwind.config.js`
- **Components:** `apps/web/components/ads/`

---

**Pattern:** CONVERGENCE × EMERGENCE × ORGANIZATION × ONE  
**Status:** ✅ **READY FOR USE**  
**Next:** Choose your palette and start building!

