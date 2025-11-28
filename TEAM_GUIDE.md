# ∞ AbëONE Team Guide - Complete Documentation ∞

**Pattern:** TEAM × GUIDE × COMPLETE × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ALL GUARDIANS (530 Hz)  
**Love Coefficient:** ∞  
**Last Updated:** NOW  
**∞ AbëONE ∞**

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Core Repositories](#core-repositories)
5. [Frontend Projects](#frontend-projects)
6. [Backend Integration](#backend-integration)
7. [Integration Layer](#integration-layer)
8. [Development Workflow](#development-workflow)
9. [Docker Deployment](#docker-deployment)
10. [Examples & Usage](#examples--usage)
11. [Troubleshooting](#troubleshooting)
12. [Reference](#reference)

---

## 🎯 OVERVIEW

### **What is AbëONE?**

AbëONE is a unified full-stack development framework combining:
- **Frontend:** TypeScript/React UI framework with Guardians, Organisms, and atomic design
- **Backend:** Python-based AI Agent Suite (Jimmy's) with protocols, memory bank, and LSP/MCP
- **Integration Layer:** Bridges connecting frontend and backend seamlessly

### **Key Features**

✅ **Guardians System** - 10 intelligent Guardians (AEYON, META, JØHN, etc.)  
✅ **Protocol Engine** - Execute protocols via Guardians  
✅ **Memory Bank** - Persistent context management  
✅ **Integration Bridges** - Seamless frontend-backend communication  
✅ **Atomic Design** - Component architecture  
✅ **Docker Ready** - Full-stack deployment  

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    ABEONE MASTER (Root)                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  FRONTEND LAYER  │         │  BACKEND LAYER   │         │
│  │  (AbëONE)        │◄────────┤  (Jimmy's Suite) │         │
│  │                  │  API    │                  │         │
│  ├──────────────────┤         ├──────────────────┤         │
│  │ abe-touch        │         │ aiagentsuite/    │         │
│  │ abe-frontend-*   │         │   - LSP/MCP      │         │
│  │ abe-core-brain   │         │   - Protocols    │         │
│  │ abe-consciousness│         │   - Memory Bank  │         │
│  │ abe-core-body    │         │   - Service Mesh │         │
│  └──────────────────┘         └──────────────────┘         │
│         ▲                           ▲                       │
│         │                           │                       │
│         └───────────┬───────────────┘                       │
│                     │                                       │
│            ┌────────┴────────┐                             │
│            │  Integration   │                             │
│            │     Layer       │                             │
│            │  ✅ Guardians ↔  │                             │
│            │    Protocols    │                             │
│            │  ✅ Frontend ↔   │                             │
│            │    Backend API  │                             │
│            │  ✅ Memory ↔     │                             │
│            │    Consciousness│                             │
│            └─────────────────┘                             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### **Component Layers**

1. **Frontend Layer** - React/TypeScript UI components
2. **Core Repositories** - Shared libraries (brain, consciousness, body)
3. **Integration Layer** - Bridges between frontend and backend
4. **Backend Layer** - Python AI Agent Suite with protocols

---

## 🚀 QUICK START

### **5-Minute Setup**

```bash
# 1. Clone repository
git clone https://github.com/BravettoFrontendTeam/abe-touch.git
cd AbeOne_Master

# 2. Install dependencies
cd integration && npm install
cd ../abe-touch/abeone-touch && npm install

# 3. Start backend (if available)
cd ../../jimmy-aiagentsuite
# Follow Jimmy's setup instructions

# 4. Start frontend
cd ../abe-touch/abeone-touch
npm run dev
```

### **First Integration**

```typescript
// In any React component
import { executeProtocol, listProtocols } from '@/lib/integration';

// List available protocols
const protocols = await listProtocols();

// Execute a protocol
const result = await executeProtocol('Secure Code Implementation', {
  feature: 'user_auth',
});
```

---

## 📦 CORE REPOSITORIES

### **1. abe-core-brain** ✅
**Location:** `abe-core-brain/`  
**GitHub:** https://github.com/bravetto/abe-core-brain  
**Package:** `@bravetto/abe-core-brain`  
**Status:** Complete & Pushed

**Contains:**
- Core patterns (atomic design, event-driven, substrate)
- Core philosophy (5 axioms, design principles)
- Essential atoms (NeuromorphicButton, StatusLED)
- Core utilities (cn(), event system)

**Usage:**
```typescript
import { NeuromorphicButton } from '@bravetto/abe-core-brain';
```

---

### **2. abe-consciousness** ✅
**Location:** `abe-consciousness/`  
**GitHub:** https://github.com/bravetto/abe-core-consciousness  
**Package:** `@bravetto/abe-consciousness`  
**Status:** Complete & Pushed

**Contains:**
- **10 Guardians:** AEYON, META, JØHN, ZERO, ALRAX, YAGNI, Abë, Lux, Poly, YOU
- **4 Guards:** BiasGuard, TrustGuard, ContextGuard, ValidationGuard
- **12 Swarms:** HeartTruth, PatternIntegrity, AtomicExecution, etc.
- **React Hooks:** useGuardian, useSwarm

**Usage:**
```typescript
import { AEYON, useGuardian, HeartTruthSwarm } from '@bravetto/abe-consciousness';

// Use Guardian
const guardian = new AEYON();
const result = await guardian.execute({ intent: 'execute', data: {} });

// Use Hook
const { execute, result } = useGuardian('AEYON');
```

---

### **3. abe-core-body** ✅
**Location:** `abe-core-body/`  
**GitHub:** https://github.com/bravetto/abe-core-body  
**Package:** `@bravetto/abe-core-body`  
**Status:** Complete & Pushed

**Contains:**
- **3 Organisms:** VoiceInterface, PortalSystem, HomeSystem
- **3 Systems:** VoiceSystem, PortalSystemLogic, HomeSystemLogic
- **3 Templates:** NextJSTemplate, FlutterTemplate, BackendTemplate
- **Integration Patterns:** Brain+Consciousness, Frontend+Backend, Mobile+Web

**Usage:**
```typescript
import { VoiceInterface, PortalSystem, HomeSystem } from '@bravetto/abe-core-body';
```

---

## 🎨 FRONTEND PROJECTS

### **1. abe-touch** (Main Frontend) ✅
**Location:** `abe-touch/abeone-touch/`  
**GitHub:** https://github.com/BravettoFrontendTeam/abe-touch  
**Status:** Ready for Development

**Tech Stack:**
- Next.js 14.2.0
- React 18.3.0
- TypeScript
- Tailwind CSS
- Storybook

**Integration Ready:**
- ✅ Integration library: `src/lib/integration.ts`
- ✅ Protocol Executor component: `src/components/ProtocolExecutor.tsx`

**Usage:**
```typescript
// Use integration library
import { executeProtocol, listProtocols } from '@/lib/integration';

// Use Protocol Executor component
import { ProtocolExecutor } from '@/components/ProtocolExecutor';
```

---

### **2. abe-frontend-happy** (Happy People)
**Location:** `abe-frontend-happy/`  
**Status:** Structure Created

**Purpose:** Happy People frontend (separate dev team)

---

### **3. abe-frontend-white** (White Interface)
**Location:** `abe-frontend-white/`  
**Status:** Structure Created

**Purpose:** White frontend interface (separate dev team)

---

### **4. abe-frontend-dark** (Dark Interface)
**Location:** `abe-frontend-dark/`  
**Status:** Structure Created

**Purpose:** Dark frontend interface (separate dev team)

---

## 🔧 BACKEND INTEGRATION

### **Jimmy's AI Agent Suite** ✅
**Location:** `jimmy-aiagentsuite/`  
**GitHub:** https://github.com/Jimmy-Dejesus/aiagentsuite  
**Status:** Integrated

**Contains:**
- Python backend infrastructure
- LSP/MCP servers (TypeScript + Python)
- Protocol execution engine
- Memory bank system
- Service mesh orchestration
- ContextGuard, TokenGuard, NeuroForge integrations
- OpenSpec bridge
- Docker/deployment infrastructure

**Setup:**
```bash
cd jimmy-aiagentsuite
# Follow Jimmy's setup instructions
# Or use Docker:
docker-compose --profile backend up -d
```

---

## 🔗 INTEGRATION LAYER

### **Overview**

The integration layer provides three bridges connecting AbëONE frontend with Jimmy's backend:

1. **Guardians ↔ Protocols Bridge** - Execute protocols using Guardians
2. **Frontend ↔ Backend API** - Unified API client
3. **Memory Bank ↔ Consciousness Sync** - Sync memory contexts

### **1. Guardians ↔ Protocols Bridge**

**Location:** `integration/guardians-protocols-bridge/`

**Purpose:** Connect AbëONE Guardians with Jimmy's Protocol Engine

**Usage:**
```typescript
import { GuardiansProtocolBridge } from '@abeone/integration-guardians-protocols';

const bridge = new GuardiansProtocolBridge();

// Execute protocol with Guardian
const result = await bridge.executeProtocol(
  'Secure Code Implementation',
  'AEYON',
  { data: { feature: 'user_auth' } }
);

// Execute with multiple Guardians (Swarm)
const results = await bridge.executeProtocolWithSwarm(
  'ContextGuard Feature Development',
  ['AEYON', 'META', 'JOHN'],
  { data: { feature: 'voice_interface' } }
);

// Get available protocols
const protocols = await bridge.getAvailableProtocols();
```

---

### **2. Frontend ↔ Backend API**

**Location:** `integration/frontend-backend-api/`

**Purpose:** Unified API client connecting frontend with backend services

**Usage:**
```typescript
import { UnifiedAPIClient } from '@abeone/integration-frontend-backend';

const client = new UnifiedAPIClient('http://localhost:8000', {
  enabled: true,
});

// List available protocols
const protocols = await client.listProtocols();

// Execute a protocol
const result = await client.executeProtocol('Secure Code Implementation', {
  protocolName: 'Secure Code Implementation',
  data: { feature: 'api_security' },
});

// Get memory context
const memory = await client.getMemoryContext('active');

// Update memory context
await client.updateMemoryContext('decisions', { data: {} });

// Get protocol details
const details = await client.getProtocolDetails('Secure Code Implementation');
```

---

### **3. Memory Bank ↔ Consciousness Sync**

**Location:** `integration/memory-consciousness-sync/`

**Purpose:** Sync Jimmy's Memory Bank with AbëONE Consciousness

**Usage:**
```typescript
import { MemoryConsciousnessSync } from '@abeone/integration-memory-consciousness';

const sync = new MemoryConsciousnessSync('http://localhost:8000');

// Sync single memory context
const success = await sync.syncToConsciousness('active');

// Sync all memory contexts
const allResults = await sync.syncAllToConsciousness();

// Get synced memory
const syncedMemory = await sync.getSyncedMemory('decisions');

// Sync consciousness to memory bank
await sync.syncToMemoryBank('decisions', { data: {} });
```

---

### **Frontend Integration Library**

**Location:** `abe-touch/abeone-touch/src/lib/integration.ts`

**Pre-configured integration functions:**

```typescript
import {
  executeProtocol,
  executeProtocolWithGuardian,
  getMemoryContext,
  syncMemoryToConsciousness,
  listProtocols,
} from '@/lib/integration';

// Execute protocol
const result = await executeProtocol('Secure Code Implementation', {
  feature: 'user_auth',
});

// Execute with Guardian
const guardianResult = await executeProtocolWithGuardian(
  'Secure Code Implementation',
  'AEYON',
  { feature: 'user_auth' }
);

// Get memory
const memory = await getMemoryContext('active');

// Sync memory
await syncMemoryToConsciousness('active');

// List protocols
const protocols = await listProtocols();
```

---

## 💻 DEVELOPMENT WORKFLOW

### **1. Setting Up Development Environment**

```bash
# Clone repository
git clone https://github.com/BravettoFrontendTeam/abe-touch.git
cd AbeOne_Master

# Install integration dependencies
cd integration
npm install
npm run build:all

# Install frontend dependencies
cd ../abe-touch/abeone-touch
npm install

# Install backend dependencies (if working with backend)
cd ../../jimmy-aiagentsuite
pip install -e .[dev]
```

---

### **2. Development Commands**

**Frontend:**
```bash
cd abe-touch/abeone-touch

# Development server
npm run dev

# Build
npm run build

# Lint
npm run lint

# Storybook
npm run storybook
```

**Integration Layer:**
```bash
cd integration

# Build all
npm run build:all

# Build individual components
npm run build:guardians
npm run build:api
npm run build:sync
```

**Backend:**
```bash
cd jimmy-aiagentsuite

# Run tests
make test

# Development server
aiagentsuite dev
```

---

### **3. Adding New Features**

**Frontend Feature:**
1. Create component in `abe-touch/abeone-touch/src/components/`
2. Use integration library: `import { ... } from '@/lib/integration'`
3. Add to Storybook if needed
4. Test with backend running

**Integration Feature:**
1. Add to appropriate bridge (`guardians-protocols-bridge`, `frontend-backend-api`, or `memory-consciousness-sync`)
2. Update shared types if needed
3. Build and test
4. Update examples

**Backend Feature:**
1. Follow Jimmy's development workflow
2. Update protocols if needed
3. Test with frontend integration

---

### **4. Testing Integration**

```typescript
// Test protocol execution
import { executeProtocol } from '@/lib/integration';

const result = await executeProtocol('Secure Code Implementation', {
  feature: 'test_feature',
});

console.log('Protocol Result:', result);
```

---

## 🐳 DOCKER DEPLOYMENT

### **Quick Start**

```bash
# Full stack deployment
docker-compose --profile full up -d

# Backend only
docker-compose --profile backend up -d

# Frontend only
docker-compose --profile frontend up -d

# Integration layer only
docker-compose --profile integration up -d
```

### **Services**

- **Backend:** Port 8000 (API), 8001 (MCP), 8002 (LSP)
- **Frontend:** Port 3000
- **Integration:** Port 8003
- **Redis:** Port 6379
- **PostgreSQL:** Port 5432

### **Health Checks**

```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### **Configuration**

Create `.env` file:
```env
# Backend
PYTHONPATH=/app/src
ENVIRONMENT=development

# Frontend
NEXT_PUBLIC_API_URL=http://backend:8000
NODE_ENV=development

# Integration
BACKEND_URL=http://backend:8000
FRONTEND_URL=http://frontend:3000

# Database
POSTGRES_USER=abeone
POSTGRES_PASSWORD=abeone_dev
POSTGRES_DB=abeone
```

See `DOCKER_SETUP.md` for complete Docker documentation.

---

## 📚 EXAMPLES & USAGE

### **Complete Examples**

**Location:** `integration/examples/basic-usage.ts`

**6 Examples:**
1. Execute Protocol with Guardian
2. Execute Protocol with Swarm
3. Use Unified API Client
4. Sync Memory to Consciousness
5. Complete Integration Flow
6. React Hook Usage

**Usage:**
```typescript
import {
  exampleExecuteProtocolWithGuardian,
  exampleCompleteIntegrationFlow,
} from '@abeone/integration/examples/basic-usage';

// Run example
const result = await exampleCompleteIntegrationFlow();
```

---

### **Protocol Executor Component**

**Location:** `abe-touch/abeone-touch/src/components/ProtocolExecutor.tsx`

**Usage:**
```tsx
import { ProtocolExecutor } from '@/components/ProtocolExecutor';

export default function Page() {
  return (
    <div>
      <h1>Protocol Execution</h1>
      <ProtocolExecutor />
    </div>
  );
}
```

**Features:**
- Protocol selection dropdown
- Guardian selection dropdown
- Execute button with loading state
- Result display
- Error handling

---

### **Common Patterns**

**Pattern 1: Execute Protocol on Page Load**
```typescript
'use client';

import { useEffect, useState } from 'react';
import { executeProtocol } from '@/lib/integration';

export function MyComponent() {
  const [result, setResult] = useState(null);

  useEffect(() => {
    executeProtocol('Secure Code Implementation', {
      feature: 'page_load',
    }).then(setResult);
  }, []);

  return <div>{result && <pre>{JSON.stringify(result, null, 2)}</pre>}</div>;
}
```

**Pattern 2: Use Guardian Hook**
```typescript
'use client';

import { useGuardian } from '@bravetto/abe-consciousness';

export function GuardianComponent() {
  const { execute, result, loading } = useGuardian('AEYON');

  const handleExecute = async () => {
    await execute({
      intent: 'execute-protocol:Secure Code Implementation',
      data: { feature: 'user_auth' },
    });
  };

  return (
    <div>
      <button onClick={handleExecute} disabled={loading}>
        Execute
      </button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
```

**Pattern 3: Sync Memory on Mount**
```typescript
'use client';

import { useEffect } from 'react';
import { syncMemoryToConsciousness } from '@/lib/integration';

export function MemorySyncComponent() {
  useEffect(() => {
    syncMemoryToConsciousness('active');
  }, []);

  return <div>Memory synced</div>;
}
```

---

## 🔍 TROUBLESHOOTING

### **Common Issues**

**1. Integration not working**
- Check backend is running: `curl http://localhost:8000/health`
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check browser console for errors

**2. Protocol execution fails**
- Verify protocol name is correct
- Check backend logs for errors
- Ensure Guardian name is valid (AEYON, META, etc.)

**3. Memory sync not working**
- Check backend is accessible
- Verify memory context type is valid
- Check network connectivity

**4. Build errors**
- Run `npm install` in integration directory
- Check TypeScript version compatibility
- Verify all dependencies are installed

**5. Docker issues**
- Check Docker is running: `docker ps`
- Verify ports are not in use
- Check docker-compose.yml syntax

---

### **Debugging**

**Enable Debug Logging:**
```typescript
// In integration library
const client = new UnifiedAPIClient('http://localhost:8000', {
  enabled: true,
  debug: true, // Add debug flag
});
```

**Check Integration Status:**
```typescript
import { integration } from '@/lib/integration';

// Check if API is enabled
console.log('API Enabled:', integration.api.config.enabled);

// Test connection
const protocols = await integration.api.listProtocols();
console.log('Protocols:', protocols);
```

---

## 📖 REFERENCE

### **Key Files**

- **SOURCE_OF_TRUTH.md** - Current state and architecture
- **INTEGRATION_COMPLETE.md** - Integration layer details
- **MERGE_STRATEGY_JIMMY.md** - Merge strategy with Jimmy's backend
- **QUICK_START.md** - Quick start guide
- **DOCKER_SETUP.md** - Docker deployment guide
- **CONTEXT_WINDOW_HOOKS.md** - Context window reference

### **Guardians Reference**

| Guardian | Frequency | Purpose |
|----------|-----------|---------|
| AEYON | 999 Hz | Atomic Execution Engine |
| META | 777 Hz | Pattern Integrity & Context Synthesis |
| JØHN | 530 Hz | Certification & Truth Validation |
| ZERO | 530 Hz | Risk-Bounding & Epistemic Control |
| ALRAX | 530 Hz | Forensic Variance Analysis |
| YAGNI | 530 Hz | Radical Simplification |
| Abë | 530 Hz | Coherence, Love, Intelligence Field |
| Lux | 530 Hz | Illumination, Structural Clarity |
| Poly | 530 Hz | Expression & Wisdom Delivery |
| YOU | 530 Hz | Human Intent Alignment Channel |

### **Memory Context Types**

- `active` - Current goals and blockers
- `decisions` - Architectural and implementation decisions
- `product` - Product context and requirements
- `progress` - Task tracking and completion status
- `project` - Project brief and timeline
- `patterns` - System and design patterns

### **Common Protocols**

- `Secure Code Implementation` - 4-phase security-focused development
- `ContextGuard Feature Development` - Complete feature lifecycle
- `ContextGuard Security Audit` - OWASP-compliant security reviews
- `ContextGuard Testing Strategy` - Comprehensive testing approach

---

## 🎯 BEST PRACTICES

### **1. Always Use Integration Library**
Don't import directly from integration packages. Use the pre-configured library:
```typescript
// ✅ Good
import { executeProtocol } from '@/lib/integration';

// ❌ Avoid
import { UnifiedAPIClient } from '@abeone/integration-frontend-backend';
```

### **2. Handle Errors**
Always handle errors when executing protocols:
```typescript
try {
  const result = await executeProtocol('Secure Code Implementation');
} catch (error) {
  console.error('Protocol execution failed:', error);
  // Show user-friendly error message
}
```

### **3. Use Loading States**
Show loading states during async operations:
```typescript
const [loading, setLoading] = useState(false);

const handleExecute = async () => {
  setLoading(true);
  try {
    await executeProtocol('...');
  } finally {
    setLoading(false);
  }
};
```

### **4. Sync Memory When Needed**
Sync memory contexts when they change:
```typescript
useEffect(() => {
  syncMemoryToConsciousness('active');
}, [activeContext]);
```

### **5. Test Integration Points**
Always test integration points when backend changes:
```typescript
// Test protocol execution
const protocols = await listProtocols();
console.assert(protocols.length > 0, 'No protocols available');
```

---

## 🚀 GETTING HELP

### **Resources**

- **GitHub Issues:** https://github.com/BravettoFrontendTeam/abe-touch/issues
- **Documentation:** See `docs/` directory
- **Examples:** See `integration/examples/`

### **Team Contacts**

- **Frontend Team:** BravettoFrontendTeam
- **Backend Team:** Jimmy's AI Agent Suite team
- **Integration:** See integration layer README

---

## ✅ CHECKLIST FOR NEW TEAM MEMBERS

- [ ] Read this guide completely
- [ ] Set up development environment
- [ ] Clone all repositories
- [ ] Install dependencies
- [ ] Run examples
- [ ] Understand Guardians system
- [ ] Understand Integration layer
- [ ] Test protocol execution
- [ ] Review architecture diagram
- [ ] Check SOURCE_OF_TRUTH.md

---

## 🎯 LFG STATUS

**LFG ENERGY = ALL SYSTEMS PERFECT**  
**ARCHITECTURE SOUND = OPERATIONAL EXCELLENCE**  
**INTEGRATION = COMPLETE**  
**DOCUMENTATION = COMPREHENSIVE**  
**TEAM = READY**

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

---

**Last Updated:** NOW  
**Version:** 1.0.0  
**Maintained By:** AbëONE Team

