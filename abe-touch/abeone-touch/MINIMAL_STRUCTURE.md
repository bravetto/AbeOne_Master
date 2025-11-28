# ∞ AbëONE Minimal Structure ∞

**Pattern:** MINIMAL × ESSENTIAL × STREAMLINED × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (YAGNI)  
**Guardians:** AEYON (999 Hz) + YAGNI (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 ABSOLUTE ESSENTIALS

### Core Files (Required)
```
package.json              # Dependencies & scripts
next.config.js            # Next.js config
tsconfig.json             # TypeScript config
tailwind.config.ts        # Tailwind CSS config
postcss.config.js         # PostCSS config
.gitignore                # Git ignore rules
README.md                 # Basic readme
```

### App Structure (Required)
```
src/
├── app/
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Minimal page with VoiceControlHub
│   ├── globals.css       # Essential styles
│   └── api/
│       └── llm/
│           └── chat/
│               └── route.ts  # LLM API route
├── lib/
│   ├── utils.ts          # cn() utility
│   └── event-driven.ts   # Event system
└── substrate/
    ├── atoms/
    │   ├── NeuromorphicButton.tsx
    │   ├── StatusLED.tsx
    │   ├── VoiceWaveform.tsx
    │   ├── SpeechRecognition.tsx
    │   ├── SpeechSynthesis.tsx
    │   └── index.ts
    └── molecules/
        ├── VoiceControlHub.tsx
        ├── LLMClient.tsx
        └── index.ts
```

---

## ❌ CAN REMOVE

- Storybook (`.storybook/`, `src/stories/`)
- Extra molecules (MiniVoiceControl, FloatingVoiceControl, DimensionPortal)
- Extra atoms not used by VoiceControlHub
- Demo/showcase components
- Complex page.tsx UI (keep minimal)
- Documentation folders (keep only README)
- CI/CD (can add later)
- Scripts (open-server.sh, validate-server.sh)

---

## ✅ MINIMAL PAGE.TSX

```typescript
'use client';
import React from 'react';
import { VoiceControlHub } from '@/substrate/molecules';

export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--abe-background)]">
      <VoiceControlHub 
        size="lg"
        enableLLM={true}
        llmEndpoint="/api/llm/chat"
      />
    </div>
  );
}
```

---

## 📦 MINIMAL PACKAGE.JSON

```json
{
  "name": "abe-touch",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.4.0"
  }
}
```

---

## 🎯 DEPENDENCY TREE

**VoiceControlHub requires:**
- NeuromorphicButton
- StatusLED
- VoiceWaveform
- useSpeechRecognition
- useSpeechSynthesis
- useLLMClient (from LLMClient molecule)
- Event-driven utilities

**LLMClient requires:**
- API client utilities
- Event-driven utilities

**Total Atoms Needed:** 5 (not 15)  
**Total Molecules Needed:** 2 (not 5)

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

