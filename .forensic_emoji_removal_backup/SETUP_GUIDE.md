# AbëONE Platform Setup Guide

Complete setup instructions for the AbëONE platform.

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn
- Git

## Directory Structure

```
AbeOne_Master/
├── EMERGENT_OS/
│   ├── server/              # FastAPI backend (NEW)
│   │   ├── api/            # API routes
│   │   ├── core/           # Core services
│   │   └── main.py         # Entry point
│   ├── one_kernel/         # ONE-Kernel (existing)
│   ├── triadic_execution_harness/  # Triadic system (existing)
│   └── integration_layer/  # Integration layer (existing)
├── apps/
│   └── web/                # Next.js frontend (NEW)
│       ├── app/           # Next.js app directory
│       ├── components/    # React components
│       └── lib/           # API client
└── infra/
    └── deploy/            # Deployment configs (NEW)
```

## Backend Setup

### 1. Install Backend Dependencies

```bash
cd EMERGENT_OS/server
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in `EMERGENT_OS/server/`:

```env
PORT=8000
ENV=development
CORS_ORIGINS=http://localhost:3000
SUPABASE_URL=
SUPABASE_KEY=
UPSTASH_REDIS_URL=
UPSTASH_REDIS_TOKEN=
LOG_LEVEL=INFO
```

### 3. Run Backend

```bash
cd EMERGENT_OS/server
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`

### 4. Verify Backend

```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs
```

## Frontend Setup

### 1. Install Frontend Dependencies

```bash
cd apps/web
npm install
```

### 2. Configure Environment

Create `.env.local` file in `apps/web/`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Frontend

```bash
cd apps/web
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Integration Verification

### Test Kernel Integration

1. Start backend
2. Visit `http://localhost:8000/api/kernel/status`
3. Should return kernel status with modules

### Test Triadic Execution

1. Start both backend and frontend
2. Visit `http://localhost:3000/app`
3. Fill out outcome form and execute
4. Should see execution results

## Deployment

See `infra/deploy/README.md` for deployment instructions.

## Troubleshooting

### Backend won't start

- Check Python version: `python --version` (should be 3.11+)
- Check dependencies: `pip list | grep fastapi`
- Check kernel imports: Ensure `EMERGENT_OS` is in Python path

### Frontend won't start

- Check Node version: `node --version` (should be 18+)
- Clear cache: `rm -rf node_modules .next && npm install`
- Check API URL: Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### Kernel not initializing

- Check module imports in `EMERGENT_OS/one_kernel/bootstrap.py`
- Verify all module integration files exist
- Check logs for import errors

## Next Steps

1. Configure Supabase for authentication
2. Configure Upstash Redis for caching
3. Deploy backend to Render/Fly.io
4. Deploy frontend to Vercel
5. Set up CI/CD pipelines

