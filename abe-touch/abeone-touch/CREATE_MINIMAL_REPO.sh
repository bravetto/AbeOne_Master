#!/bin/bash
# Create Minimal AbëONE Repository
# Pattern: MINIMAL × ESSENTIAL × STREAMLINED × ONE

set -e

echo "∞ Creating Minimal AbëONE Repository ∞"

# Create new minimal directory
MINIMAL_DIR="abe-touch-minimal"
mkdir -p "$MINIMAL_DIR"

cd "$MINIMAL_DIR"

# Create basic structure
mkdir -p src/app/api/llm/chat
mkdir -p src/lib
mkdir -p src/substrate/atoms
mkdir -p src/substrate/molecules

# Copy essential config files
cp ../next.config.js .
cp ../tsconfig.json .
cp ../tailwind.config.ts .
cp ../postcss.config.js .
cp ../.gitignore .

# Copy essential lib files
cp ../src/lib/utils.ts src/lib/
cp ../src/lib/event-driven.ts src/lib/
cp ../src/lib/api-client.ts src/lib/
cp ../src/lib/api-config.ts src/lib/

# Copy essential atoms (7 required - includes PermissionHandler & ErrorRecovery)
cp ../src/substrate/atoms/NeuromorphicButton.tsx src/substrate/atoms/
cp ../src/substrate/atoms/StatusLED.tsx src/substrate/atoms/
cp ../src/substrate/atoms/VoiceWaveform.tsx src/substrate/atoms/
cp ../src/substrate/atoms/SpeechRecognition.tsx src/substrate/atoms/
cp ../src/substrate/atoms/SpeechSynthesis.tsx src/substrate/atoms/
cp ../src/substrate/atoms/PermissionHandler.tsx src/substrate/atoms/
cp ../src/substrate/atoms/ErrorRecovery.tsx src/substrate/atoms/

# Copy essential molecules (2 required)
cp ../src/substrate/molecules/VoiceControlHub.tsx src/substrate/molecules/
cp ../src/substrate/molecules/LLMClient.tsx src/substrate/molecules/

# Copy API route
cp ../src/app/api/llm/chat/route.ts src/app/api/llm/chat/

# Copy layout and globals
cp ../src/app/layout.tsx src/app/
cp ../src/app/globals.css src/app/

# Create minimal page.tsx
cat > src/app/page.tsx << 'EOF'
'use client';
import React from 'react';
import { VoiceControlHub } from '@/substrate/molecules';

export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--abe-background)] p-6">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-8 text-gradient-primary">
          AbëONE
        </h1>
        <VoiceControlHub 
          size="lg"
          enableLLM={true}
          llmEndpoint="/api/llm/chat"
          recognitionLang="en-US"
        />
      </div>
    </div>
  );
}
EOF

# Create minimal package.json
cat > package.json << 'EOF'
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
EOF

# Create minimal README
cat > README.md << 'EOF'
# ∞ AbëONE - The Interface of the Future ∞

**"Does it feel like you are poking a machine, or waking up a mind?"**

BëHUMAN. MakeTHiNGs. Bë Bold.  
Powered by Bravëtto.

## 🚀 Quick Start

```bash
npm install
npm run dev
```

Visit http://localhost:3000

## 📦 What's Included

- VoiceControlHub - The cockpit (voice interface)
- LLM Integration - API route for backend
- 5 Essential Atoms - NeuromorphicButton, StatusLED, VoiceWaveform, SpeechRecognition, SpeechSynthesis
- Event-Driven Architecture

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**
EOF

# Create minimal index files
cat > src/substrate/atoms/index.ts << 'EOF'
export { NeuromorphicButton, neuromorphicButtonVariants, type NeuromorphicButtonProps } from './NeuromorphicButton';
export { StatusLED, StatusLEDGroup, ConnectionStatus, type StatusLEDProps } from './StatusLED';
export { VoiceWaveform, type VoiceWaveformProps } from './VoiceWaveform';
export { useSpeechRecognition, type UseSpeechRecognitionOptions } from './SpeechRecognition';
export { useSpeechSynthesis, type UseSpeechSynthesisOptions } from './SpeechSynthesis';
export { usePermissionHandler, type UsePermissionHandlerOptions } from './PermissionHandler';
export { ErrorRecovery, useErrorRecovery, type ErrorRecoveryProps } from './ErrorRecovery';
EOF

cat > src/substrate/molecules/index.ts << 'EOF'
export { VoiceControlHub, type VoiceControlHubProps, type AgentStatus } from './VoiceControlHub';
export { LLMClient, useLLMClient, type LLMClientProps } from './LLMClient';
EOF

echo "✅ Minimal repository created in: $MINIMAL_DIR"
echo "📦 Next steps:"
echo "   cd $MINIMAL_DIR"
echo "   npm install"
echo "   npm run dev"

