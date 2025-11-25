# 🐍 FLASK APP INTEGRATION GUIDE

**Date:** 2025-11-22  
**Status:** ✅ **INTEGRATION READY**  
**Pattern:** ADS × FLASK × INTEGRATION × ONE  
**Guardians:** AEYON (Execution) + Zero (Tech)

---

## 🎯 INTEGRATION OVERVIEW

Replace inline CSS in Flask apps with centralized design system CSS variables.

---

## 📋 CURRENT STATE

**Location:** `PRODUCTS/abedesks/app.py`  
**Issue:** Inline CSS (lines 54-372) - duplicated design values  
**Solution:** Use CSS variables from design system

---

## 🔧 INTEGRATION STEPS

### Step 1: Import CSS Variables

**In your Flask template base file:**

```html
<!-- base.html or layout.html -->
<head>
  <!-- Import AbëONE Design System CSS Variables -->
  <link rel="stylesheet" href="{{ url_for('static', filename='css/abeone-design-system.css') }}">
  
  <!-- Your other stylesheets -->
</head>
```

**Copy CSS variables file:**

```bash
# Copy generated CSS variables to Flask static directory
cp design-system/generated/css-variables.css PRODUCTS/abedesks/static/css/abeone-design-system.css
```

### Step 2: Replace Inline CSS

**Before (Inline CSS):**
```python
# In app.py
style = """
  .button {
    background: #a855f7;
    color: white;
    padding: 16px 32px;
  }
"""
```

**After (CSS Variables):**
```html
<!-- In template -->
<style>
  .button {
    background: var(--primary-500);
    color: white;
    padding: 1rem 2rem;
  }
</style>
```

**Or use classes:**
```html
<!-- Use Tailwind-like classes if you have a CSS framework -->
<button class="bg-primary-500 text-white px-8 py-4">
  Click Me
</button>
```

### Step 3: Use Python Constants (Optional)

**Import design tokens:**

```python
# In app.py
import json
import os

# Load design tokens
TOKENS_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../design-system/tokens/abeone-design-system-v1.json'
)

with open(TOKENS_PATH) as f:
    DESIGN_TOKENS = json.load(f)

# Use in templates
@app.route('/')
def index():
    primary_color = DESIGN_TOKENS['colors']['primary']['500']
    return render_template('index.html', primary_color=primary_color)
```

**In template:**
```html
<div style="background: {{ primary_color }};">
  Content
</div>
```

---

## 🎨 AVAILABLE CSS VARIABLES

### Semantic Colors (v1.0)

```css
/* Primary Colors */
--primary-50 through --primary-900

/* Secondary Colors */
--secondary-50 through --secondary-900

/* Accent Colors */
--accent-50 through --accent-900

/* Success Colors */
--success-50 through --success-900

/* Neutral Colors */
--neutral-50 through --neutral-900
```

### Legacy Colors (Backward Compatible)

```css
/* Legacy aliases still available */
--lux-50 through --lux-900      /* Maps to primary */
--warm-50 through --warm-900    /* Maps to secondary */
--heart-50 through --heart-900  /* Maps to accent */
--peace-50 through --peace-900  /* Maps to success */
```

### Gradients

```css
/* Healing gradient */
background: linear-gradient(135deg, #fff7ed 0%, #fef2f2 50%, #faf5ff 100%);

/* Primary gradient */
background: linear-gradient(135deg, #9333ea 0%, #a855f7 100%);

/* Secondary gradient */
background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
```

---

## 📝 EXAMPLE: COMPLETE FLASK INTEGRATION

### 1. Project Structure

```
PRODUCTS/abedesks/
├── app.py
├── static/
│   └── css/
│       └── abeone-design-system.css  # Copied from design-system/generated/
├── templates/
│   └── base.html
└── config.py
```

### 2. Base Template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}AbëDESKs{% endblock %}</title>
  
  <!-- AbëONE Design System CSS Variables -->
  <link rel="stylesheet" href="{{ url_for('static', filename='css/abeone-design-system.css') }}">
  
  <!-- Your custom styles -->
  <style>
    /* Use CSS variables */
    .btn-primary {
      background: var(--primary-500);
      color: white;
      padding: 1rem 2rem;
      border-radius: 0.75rem;
      font-weight: 600;
      transition: all 0.2s;
    }
    
    .btn-primary:hover {
      background: var(--primary-600);
      transform: scale(1.02);
    }
    
    .card {
      background: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(12px);
      border-radius: 1.5rem;
      padding: 2.5rem;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
      border: 1px solid var(--primary-100);
    }
  </style>
  
  {% block head %}{% endblock %}
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
```

### 3. Using in Templates

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block content %}
<div class="card">
  <h1 style="color: var(--primary-600);">Welcome</h1>
  <p style="color: var(--neutral-700);">Content here</p>
  <button class="btn-primary">Get Started</button>
</div>
{% endblock %}
```

### 4. Using Python Constants

```python
# app.py
import json
import os
from flask import Flask, render_template

app = Flask(__name__)

# Load design tokens
TOKENS_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../design-system/tokens/abeone-design-system-v1.json'
)

with open(TOKENS_PATH) as f:
    DESIGN_TOKENS = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', 
        primary_color=DESIGN_TOKENS['colors']['primary']['500'],
        secondary_color=DESIGN_TOKENS['colors']['secondary']['500']
    )
```

---

## ✅ INTEGRATION CHECKLIST

- [ ] Copy CSS variables file to Flask static directory
- [ ] Import CSS variables in base template
- [ ] Replace inline CSS with CSS variable references
- [ ] Test all styles render correctly
- [ ] Remove old inline CSS from app.py
- [ ] (Optional) Use Python constants for programmatic access

---

## 🎯 BENEFITS

### Before (Inline CSS)
- ❌ Hardcoded colors
- ❌ Duplicated values
- ❌ Hard to maintain
- ❌ Out of sync risk

### After (CSS Variables)
- ✅ Centralized design system
- ✅ Single source of truth
- ✅ Easy to maintain
- ✅ Always in sync
- ✅ Easy to rebrand

---

## 📚 RESOURCES

- **CSS Variables:** `design-system/generated/css-variables.css`
- **Design Tokens:** `design-system/tokens/abeone-design-system-v1.json`
- **Usage Guide:** `design-system/docs/ADS_V1_USAGE_GUIDE.md`

---

**Pattern:** ADS × FLASK × INTEGRATION × ONE  
**Status:** ✅ **READY FOR INTEGRATION**  
**Next:** Copy CSS variables and replace inline CSS

