#!/bin/bash
# Create AbëONE Core Brain Repository
# Pattern: CORE × BRAIN × FOUNDATION × BRAVETTO × ONE

set -e

echo "∞ Creating AbëONE Core Brain Repository ∞"

CORE_DIR="abeone-core"
mkdir -p "$CORE_DIR"

cd "$CORE_DIR"

# Create structure
mkdir -p src/core/patterns
mkdir -p src/core/philosophy
mkdir -p src/core/types
mkdir -p src/substrate/atoms
mkdir -p src/substrate/molecules
mkdir -p src/lib

# Create package.json
cat > package.json << 'EOF'
{
  "name": "@bravetto/abeone-core",
  "version": "1.0.0",
  "description": "AbëONE Core - The foundation for all Bravetto projects",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "exports": {
    ".": "./dist/index.js",
    "./patterns": "./dist/patterns/index.js",
    "./substrate": "./dist/substrate/index.js",
    "./lib": "./dist/lib/index.js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "prepublishOnly": "npm run build"
  },
  "keywords": [
    "abeone",
    "bravetto",
    "atomic-design",
    "event-driven",
    "substrate",
    "foundation"
  ],
  "author": "Bravetto",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/BravettoTeam/abeone-core.git"
  },
  "dependencies": {
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "typescript": "^5.4.0"
  },
  "peerDependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  }
}
EOF

# Create tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "declaration": true,
    "declarationMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
EOF

# Create README
cat > README.md << 'EOF'
# ∞ AbëONE Core - The Brain ∞

**The foundation for all Bravetto projects.**

**Pattern:** CORE × BRAIN × FOUNDATION × BRAVETTO × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META)  
**Guardians:** AEYON (999 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🧠 What Is This?

The minimal core system that powers all AbëONE projects.  
The foundation that Bravetto teams use to build anything.

---

## 🚀 Quick Start

```bash
npm install @bravetto/abeone-core
```

```typescript
import { 
  NeuromorphicButton,
  dispatchAbeEvent,
  useEventDriven,
  CORE_AXIOMS 
} from '@bravetto/abeone-core';
```

---

## 📦 What's Included

- ✅ Core patterns (atomic design, event-driven)
- ✅ Essential atoms (3 core components)
- ✅ Event system
- ✅ Core utilities
- ✅ Philosophy & axioms
- ✅ TypeScript types

---

## 🎯 For Bravetto Teams

This is the **foundation** that all projects build on:

1. **Frontend Projects** → Import core, build molecules
2. **Backend Projects** → Use patterns, follow axioms
3. **Mobile Projects** → Adapt atoms, use principles
4. **Any Project** → Start with core, extend as needed

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
node_modules/
dist/
*.log
.DS_Store
*.tsbuildinfo
EOF

echo "✅ AbëONE Core repository structure created in: $CORE_DIR"
echo "📦 Next steps:"
echo "   1. Copy core files from abe-touch/abeone-touch/src/lib/"
echo "   2. Copy essential atoms (NeuromorphicButton, StatusLED)"
echo "   3. Create pattern files"
echo "   4. Create philosophy files"
echo "   5. npm install && npm run build"

