# AbëONE Deployment Guide

This directory contains deployment configurations for the AbëONE platform.

## Architecture

- **Backend**: FastAPI service (Render/Fly.io)
- **Frontend**: Next.js app (Vercel)
- **Database**: Supabase (PostgreSQL + Auth)
- **Cache**: Upstash Redis

## Backend Deployment (Render/Fly.io)

### Render Deployment

1. Connect your repository to Render
2. Create a new Web Service
3. Set build command: `cd EMERGENT_OS/server && pip install -r requirements.txt`
4. Set start command: `cd EMERGENT_OS/server && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables (see `.env.example`)

### Fly.io Deployment

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Initialize: `fly launch` (in `EMERGENT_OS/server/`)
4. Deploy: `fly deploy`

## Frontend Deployment (Vercel)

1. Connect your repository to Vercel
2. Set root directory: `apps/web`
3. Set build command: `npm run build`
4. Set output directory: `.next`
5. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL

## Supabase Setup

1. Create a new Supabase project
2. Get your project URL and anon key
3. Add to backend environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
4. Configure authentication in Supabase dashboard

## Upstash Redis Setup

1. Create a new Upstash Redis database
2. Get your Redis URL and token
3. Add to backend environment variables:
   - `UPSTASH_REDIS_URL`
   - `UPSTASH_REDIS_TOKEN`

## Environment Variables

### Backend (.env)

```
PORT=8000
ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
UPSTASH_REDIS_URL=your_redis_url
UPSTASH_REDIS_TOKEN=your_redis_token
LOG_LEVEL=INFO
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

## Local Development

### Backend

```bash
cd EMERGENT_OS/server
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd apps/web
npm install
npm run dev
```

## Health Checks

- Backend: `GET /health`
- Frontend: Built-in Next.js health check

