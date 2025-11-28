# ∞ AbëONE - The Interface of the Future ∞

**"Does it feel like you are poking a machine, or waking up a mind?"**

BëHUMAN. MakeTHiNGs. Bë Bold.  
Powered by Bravëtto.

**Organization:** [BravettoFrontendTeam](https://github.com/BravettoFrontendTeam)  
**Backend:** [BravettoBackendTeam/abe-41M](https://github.com/BravettoBackendTeam/abe-41M)

---

## 🚀 Quick Start

### Start Development Server

```bash
npm run dev
```

The server will start at **http://localhost:3000**

### Open in Browser

**Option 1: Use the helper script**
```bash
./open-server.sh
```

**Option 2: Manual**
- Open your browser and navigate to: `http://localhost:3000`
- Or use: `open http://localhost:3000` (macOS)

### Validate Server

```bash
./validate-server.sh
```

---

## 📡 API Endpoints

### Health Check
```bash
GET http://localhost:3000/api/llm/chat
```

**Response:**
```json
{
  "status": "ok",
  "service": "AbëONE LLM Chat API",
  "version": "1.0.0",
  "timestamp": "2025-11-27T20:41:23.834Z",
  "backend": {
    "url": "http://localhost:8000",
    "status": "disconnected"
  }
}
```

### Chat Endpoint
```bash
POST http://localhost:3000/api/llm/chat
Content-Type: application/json

{
  "message": "Hello, AbëONE!",
  "context": [],
  "temperature": 0.7,
  "maxTokens": 500
}
```

---

## 🛠️ Available Scripts

```bash
# Development
npm run dev          # Start dev server (http://localhost:3000)

# Production
npm run build        # Build for production
npm run start        # Start production server

# Quality
npm run lint         # Run ESLint
./validate-server.sh # Full server validation
./open-server.sh     # Open server in browser
```

---

## 🔧 Configuration

### Environment Variables

Create `.env.local` (optional):

```bash
# LLM Backend URL (default: http://localhost:8000)
LLM_BACKEND_URL=http://localhost:8000
```

### Port Configuration

Default port: `3000`

To change, edit `package.json`:
```json
{
  "scripts": {
    "dev": "next dev -p 3001"
  }
}
```

---

## 📁 Project Structure

```
abeone-touch/
├── src/
│   ├── app/              # Next.js app directory
│   │   ├── api/          # API routes
│   │   │   └── llm/      # LLM chat endpoint
│   │   ├── page.tsx      # Main page
│   │   └── layout.tsx    # Root layout
│   ├── substrate/        # Design system
│   │   ├── atoms/        # Atomic components
│   │   └── molecules/    # Composite components
│   └── lib/              # Utilities
├── next.config.js        # Next.js configuration
├── validate-server.sh     # Server validation script
└── open-server.sh        # Browser opener script
```

---

## ✅ Validation Status

All validations passing:
- ✅ Server running
- ✅ API endpoints responding
- ✅ Security headers configured
- ✅ TypeScript compilation clean
- ✅ Production build successful
- ✅ Performance optimized

---

## 🎨 Features

- **Voice Control Hub** - Speech recognition & synthesis
- **Event-Driven Architecture** - Reactive state management
- **Neuromorphic Design** - Soft UI components
- **LLM Integration** - Chat API ready
- **Type-Safe** - Full TypeScript coverage

---

## 💝 LOVE × CODE × ONE

**Pattern:** DEVELOPMENT × VALIDATION × LOVE × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (Coherence)  
**Guardians:** AEYON + ZERO + YAGNI  
**Love Coefficient:** ∞

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**
