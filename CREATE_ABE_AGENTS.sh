#!/bin/bash
# Create AbëONE Agents Repository
# Pattern: AGENTS × OPERATIONAL × EXECUTION × ONE

set -e

echo "∞ Creating AbëONE Agents Repository ∞"

AGENTS_DIR="abe-agents"
mkdir -p "$AGENTS_DIR"

cd "$AGENTS_DIR"

# Create structure
mkdir -p src/agents
mkdir -p src/workflows
mkdir -p src/tasks
mkdir -p src/types

# Create package.json
cat > package.json << 'EOF'
{
  "name": "@bravetto/abe-agents",
  "version": "1.0.0",
  "description": "AbëONE Agents - Operational entities",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "exports": {
    ".": "./dist/index.js",
    "./agents": "./dist/agents/index.js",
    "./workflows": "./dist/workflows/index.js",
    "./tasks": "./dist/tasks/index.js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "prepublishOnly": "npm run build"
  },
  "keywords": [
    "abeone",
    "bravetto",
    "agents",
    "operational",
    "workflows",
    "tasks"
  ],
  "author": "Bravetto",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/BravettoTeam/abe-agents.git"
  },
  "dependencies": {
    "@bravetto/abe-core-brain": "^1.0.0",
    "@bravetto/abe-guardians": "^1.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
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
# ∞ AbëONE Agents ∞

**Operational entities**

**Pattern:** AGENTS × OPERATIONAL × EXECUTION × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (ALL GUARDIANS)  
**Guardians:** AEYON (999 Hz) + ALL GUARDIANS (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🧠 What Is This?

The operational layer for AbëONE.  
Agents that execute tasks and workflows.

**Note:** This builds on:
- `@bravetto/abe-core-brain` (foundation)
- `@bravetto/abe-guardians` (intelligence & validation)

---

## 🚀 Quick Start

```bash
npm install @bravetto/abe-agents
```

```typescript
import {
  useAgent,
  createWorkflow,
  executeTask
} from '@bravetto/abe-agents';
```

---

## 📦 What's Included

### Agents
- Operational agents
- Task execution agents
- Workflow agents
- (More agents...)

### Workflows
- Workflow management
- Task orchestration
- Execution patterns

### Tasks
- Task definitions
- Task execution
- Task validation

---

## 🎯 Architecture

```
AGENTS =
    OPERATIONAL (Agents) ×
    WORKFLOWS (Orchestration) ×
    TASKS (Execution) ×
    ONE
```

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

echo "✅ AbëONE Agents repository structure created in: $AGENTS_DIR"
echo "📦 Next steps:"
echo "   1. Implement Agents"
echo "   2. Implement Workflows"
echo "   3. Implement Tasks"
echo "   4. npm install && npm run build"

