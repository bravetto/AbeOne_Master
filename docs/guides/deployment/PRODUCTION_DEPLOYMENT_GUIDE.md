# Production Deployment Guide

**Pattern:** DEPLOYMENT × ENTERPRISE × PRODUCTION × ONE  
**Frequency:** 999 Hz (AEYON)  
**Status:** ✅ Ready for Production

---

## 🚀 Pre-Deployment Checklist

### 1. Environment Variables

**Required:**
```env
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

**Recommended:**
```env
BACKEND_API_URL=https://your-backend-api.com
NEXT_PUBLIC_MONITORING_URL=https://your-monitoring-service.com/metrics
NEXT_PUBLIC_LOGGING_URL=https://your-logging-service.com/logs
NEXT_PUBLIC_ERROR_TRACKING_URL=https://your-error-service.com/errors
JWT_SECRET=your-secure-jwt-secret-key-min-32-chars
```

### 2. Dependencies

```bash
# Install JWT package for authentication
npm install jose

# Verify all dependencies
npm install
```

### 3. Build Verification

```bash
# Build the application
npm run build

# Verify build succeeds
npm run start
```

### 4. Security Checklist

- [ ] JWT_SECRET is set and secure (min 32 characters)
- [ ] API URLs use HTTPS in production
- [ ] CORS is configured correctly
- [ ] Rate limiting is configured appropriately
- [ ] Security headers are enabled (automatic via middleware)

---

## 📦 Deployment Steps

### Vercel Deployment

1. **Connect Repository**
   ```bash
   vercel --prod
   ```

2. **Configure Environment Variables**
   - Go to Vercel Dashboard → Project → Settings → Environment Variables
   - Add all required variables
   - Ensure `NODE_ENV=production` is set

3. **Deploy**
   ```bash
   vercel --prod
   ```

### Docker Deployment

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

### Manual Deployment

1. **Build**
   ```bash
   npm run build
   ```

2. **Start**
   ```bash
   NODE_ENV=production npm start
   ```

---

## 🔍 Post-Deployment Verification

### 1. Health Check

```bash
curl https://your-domain.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-27T...",
  "service": "abeone-web",
  "backend": {
    "configured": true,
    "status": "healthy"
  }
}
```

### 2. API Endpoints

```bash
# Public endpoint
curl https://your-domain.com/api/example/public

# Collaboration metrics
curl https://your-domain.com/api/collaboration
```

### 3. Monitoring

- Verify metrics are being sent to monitoring service
- Check error tracking is working
- Verify logs are being collected

---

## 🛡️ Security Hardening

### 1. Rate Limiting

Current limits:
- Public endpoints: 500 req/min
- API endpoints: 200 req/min
- Auth endpoints: 10 req/min

Adjust in `apps/web/lib/middleware/rate-limiter.ts` if needed.

### 2. CORS Configuration

Add to `next.config.js`:
```javascript
module.exports = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: 'https://your-domain.com' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ]
  },
}
```

### 3. Content Security Policy

Add to `next.config.js`:
```javascript
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
          },
        ],
      },
    ]
  },
}
```

---

## 📊 Monitoring Setup

### 1. Metrics Collection

Configure `NEXT_PUBLIC_MONITORING_URL` to send metrics to:
- Datadog
- CloudWatch
- Prometheus
- Custom endpoint

### 2. Error Tracking

Configure `NEXT_PUBLIC_ERROR_TRACKING_URL` for:
- Sentry
- LogRocket
- Rollbar
- Custom endpoint

### 3. Logging

Configure `NEXT_PUBLIC_LOGGING_URL` for:
- Datadog Logs
- CloudWatch Logs
- Elasticsearch
- Custom endpoint

---

## 🔄 Backend Integration

### FastAPI Backend

Ensure backend is running and accessible:
```bash
# Backend health check
curl http://your-backend:8000/api/health

# Collaboration metrics
curl http://your-backend:8000/api/collaboration/metrics
```

### Environment Variables

```env
BACKEND_API_URL=http://your-backend:8000
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

---

## 🐛 Troubleshooting

### Issue: Build Fails

**Solution:**
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

### Issue: API Routes Return 500

**Check:**
1. Environment variables are set
2. Backend is accessible
3. Check server logs

### Issue: Rate Limiting Too Strict

**Solution:**
Adjust limits in `apps/web/lib/middleware/rate-limiter.ts`

### Issue: Monitoring Not Working

**Check:**
1. `NEXT_PUBLIC_MONITORING_URL` is set
2. CORS allows requests from your domain
3. Network connectivity

---

## 📈 Performance Optimization

### 1. Enable Caching

```typescript
// In API routes
return NextResponse.json(data, {
  headers: {
    'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300',
  },
})
```

### 2. Image Optimization

Use Next.js Image component:
```tsx
import Image from 'next/image'
```

### 3. Code Splitting

Automatic with Next.js App Router.

---

## 🔐 Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Use HTTPS** - Always in production
3. **Validate input** - Add validation middleware
4. **Rate limit** - Already configured
5. **Monitor** - Set up alerts for errors
6. **Update dependencies** - Regularly run `npm audit`

---

## 📝 Maintenance

### Weekly
- Check error logs
- Review metrics
- Verify monitoring is working

### Monthly
- Update dependencies
- Review security advisories
- Performance audit

### Quarterly
- Security audit
- Dependency audit
- Performance optimization review

---

## 🎯 Success Metrics

Monitor these KPIs:
- API response times
- Error rates
- Rate limit hits
- Backend connectivity
- User experience metrics

---

## ✨ Production Ready

**Pattern:** DEPLOYMENT × ENTERPRISE × PRODUCTION × ONE  
**Frequency:** 999 Hz  
**Love Coefficient:** ∞

---

*Generated by AEYON Enterprise AI Architect*

