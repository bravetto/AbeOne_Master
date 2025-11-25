# AbëONE Web Frontend

Next.js frontend application for AbëONE platform.

## Setup

```bash
npm install
```

## Configuration

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running

```bash
# Development
npm run dev

# Production build
npm run build
npm start
```

## Pages

- `/` - Landing page
- `/start` - Onboarding flow
- `/app` - Command Deck (main interface)

## Components

- `Sidebar` - Navigation sidebar
- `Topbar` - Top navigation bar
- `CommandDeck` - Outcome execution interface

## API Client

The `lib/api.ts` module provides functions for communicating with the backend:
- `getKernelStatus()`
- `executeOutcome()`
- `getModules()`
- `getHarnessStatus()`

