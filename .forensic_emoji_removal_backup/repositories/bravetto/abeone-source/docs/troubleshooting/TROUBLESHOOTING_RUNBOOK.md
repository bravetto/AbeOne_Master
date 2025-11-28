# AIGuards Backend - Troubleshooting Guide & Runbook

## Quick Reference

### Service Status Check
```bash
# Check all containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Check gateway health
curl http://localhost:8000/health

# Check guards health
curl http://localhost:8000/api/v1/guards/health
```

### View Logs
```bash
# Gateway logs
docker logs codeguardians-gateway-development --tail 50

# All services logs
docker-compose logs --tail=50

# Follow logs
docker-compose logs -f
```

## Common Issues & Solutions

### Issue 1: Gateway Won't Start - Database Driver Error

**Symptoms:**
```
sqlalchemy.exc.InvalidRequestError: The asyncio extension requires an async driver to be used. The loaded 'psycopg2' is not async.
```

**Solution:**
✅ **FIXED** - Gateway now auto-converts `postgresql://` to `postgresql+asyncpg://`

**Verification:**
```bash
docker logs codeguardians-gateway-development | grep "Converted postgresql"
```

### Issue 2: HealthGuard Fails to Start - Missing DATABASE_URL

**Symptoms:**
```
ValueError: DATABASE_URL or HEALTHGUARD_DATABASE_URL environment variable must be set.
```

**Solution:**
✅ **FIXED** - Added `HEALTHGUARD_DATABASE_URL=${DATABASE_URL}` to docker-compose.yml

**Verification:**
```bash
docker exec codeguardians-healthguard env | grep DATABASE_URL
```

### Issue 3: TokenGuard Health Check Fails

**Symptoms:**
```
Health check failed: ModuleNotFoundError: No module named 'requests'
```

**Solution:**
✅ **FIXED** - Added `requests>=2.31.0` to requirements.txt

**Verification:**
```bash
docker exec codeguardians-tokenguard python -c "import requests; print('OK')"
```

### Issue 4: Services Can't Communicate

**Symptoms:**
```
[Errno -2] Name or service not known
```

**Solution:**
1. Verify all services are on the same network:
```bash
docker network inspect aiguards-network
```

2. Test DNS resolution:
```bash
docker exec codeguardians-gateway-development ping -c 1 tokenguard
```

3. Verify service names match docker-compose.yml

### Issue 5: Database Connection Issues

**Symptoms:**
- Connection refused
- Authentication failed
- Connection timeout

**Solutions:**

**Check Postgres is running:**
```bash
docker ps | grep postgres
docker exec codeguardians-postgres pg_isready -U aiguardian
```

**Verify connection string:**
```bash
# Gateway (asyncpg)
echo $DATABASE_URL | grep "postgresql+asyncpg"

# HealthGuard (psycopg2)
docker exec codeguardians-healthguard env | grep HEALTHGUARD_DATABASE_URL | grep "postgresql://"
```

**Check database exists:**
```bash
docker exec codeguardians-postgres psql -U aiguardian -l
```

### Issue 6: Redis Connection Issues

**Symptoms:**
- Connection refused
- Authentication failed

**Solutions:**

**Check Redis is running:**
```bash
docker ps | grep redis
docker exec codeguardians-redis redis-cli -a ${REDIS_PASSWORD} ping
```

**Verify Redis URL:**
```bash
echo $REDIS_URL | grep "redis://"
```

### Issue 7: Rate Limiting Issues (BiasGuard)

**Symptoms:**
- 429 Too Many Requests
- Rate limit headers missing

**Solutions:**

**Check rate limit configuration:**
```bash
docker exec codeguardians-biasguard env | grep RATE_LIMIT
```

**Verify middleware is active:**
```bash
curl -v http://localhost:8004/health 2>&1 | grep -i "rate-limit"
```

### Issue 8: Request ID Not Propagating

**Symptoms:**
- Logs don't show request IDs
- Can't correlate requests across services

**Solution:**
✅ **FIXED** - Request-ID correlation implemented

**Verification:**
```bash
# Test with custom request ID
curl -H "X-Request-ID: test-123" http://localhost:8000/api/v1/guards/process \
  -d '{"service_type": "tokenguard", "payload": {"text": "test"}}'

# Check logs for request ID
docker logs codeguardians-gateway-development | grep "test-123"
```

### Issue 9: Metrics Endpoint Not Available (BiasGuard)

**Symptoms:**
- /metrics returns 404

**Solution:**
✅ **FIXED** - Prometheus metrics endpoint added

**Verification:**
```bash
curl http://localhost:8004/metrics | head -20
```

### Issue 10: Empty Payload Validation Error

**Symptoms:**
- Empty payload returns 500 instead of 400

**Solution:**
✅ **FIXED** - HTTPException now properly propagates

**Verification:**
```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"service_type": "tokenguard", "payload": {}}'
# Should return 400 with error message
```

## Emergency Procedures

### Restart All Services
```bash
docker-compose --profile centralized restart
```

### Restart Single Service
```bash
docker-compose restart <service-name>
```

### Rebuild and Restart
```bash
docker-compose build <service-name>
docker-compose restart <service-name>
```

### Complete Reset
```bash
docker-compose --profile centralized down -v
docker-compose --profile centralized up -d --build
```

### View Real-time Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f <service-name>

# Last 100 lines
docker logs <container-name> --tail 100 -f
```

## Network Troubleshooting

### Check Service Discovery
```bash
# List all containers on network
docker network inspect aiguards-network | grep -A 5 "Containers"

# Test DNS resolution
docker exec codeguardians-gateway-development nslookup tokenguard
docker exec codeguardians-gateway-development nslookup trustguard
```

### Test Service Connectivity
```bash
# From gateway to guards
docker exec codeguardians-gateway-development curl http://tokenguard:8000/health
docker exec codeguardians-gateway-development curl http://trustguard:8000/health
docker exec codeguardians-gateway-development curl http://biasguard:8004/health
```

### Check Port Exposure
```bash
# Verify only gateway is exposed
docker ps --format "table {{.Names}}\t{{.Ports}}" | grep -E "(gateway|8000)"

# Guards should NOT be exposed externally
docker ps --format "table {{.Names}}\t{{.Ports}}" | grep -E "(tokenguard|trustguard|biasguard)" | grep -v "8000/tcp"
```

## Database Troubleshooting

### Check Database Status
```bash
# PostgreSQL
docker exec codeguardians-postgres pg_isready -U aiguardian
docker exec codeguardians-postgres psql -U aiguardian -c "SELECT version();"

# List databases
docker exec codeguardians-postgres psql -U aiguardian -l
```

### Check Database Connections
```bash
# Active connections
docker exec codeguardians-postgres psql -U aiguardian -c "SELECT count(*) FROM pg_stat_activity;"

# Connection details
docker exec codeguardians-postgres psql -U aiguardian -c "SELECT datname, usename, application_name FROM pg_stat_activity;"
```

### Database Backup/Restore
```bash
# Backup
docker exec codeguardians-postgres pg_dump -U aiguardian aiguardian_unified > backup.sql

# Restore
docker exec -i codeguardians-postgres psql -U aiguardian aiguardian_unified < backup.sql
```

## Redis Troubleshooting

### Check Redis Status
```bash
# Ping Redis
docker exec codeguardians-redis redis-cli -a ${REDIS_PASSWORD} ping

# Redis info
docker exec codeguardians-redis redis-cli -a ${REDIS_PASSWORD} INFO

# Memory usage
docker exec codeguardians-redis redis-cli -a ${REDIS_PASSWORD} INFO memory
```

### Check Redis Keys
```bash
# List all keys
docker exec codeguardians-redis redis-cli -a ${REDIS_PASSWORD} KEYS "*"

# Check specific key
docker exec codeguardians-redis redis-cli -a ${REDIS_PASSWORD} GET "<key-name>"
```

### Clear Redis Cache
```bash
# Clear all keys (USE WITH CAUTION)
docker exec codeguardians-redis redis-cli -a ${REDIS_PASSWORD} FLUSHALL
```

## Performance Troubleshooting

### Check Resource Usage
```bash
# Container stats
docker stats --no-stream

# Specific container
docker stats codeguardians-gateway-development --no-stream
```

### Check Logs for Errors
```bash
# Error logs
docker-compose logs | grep -i error | tail -20

# Warning logs
docker-compose logs | grep -i warning | tail -20
```

### Check Request Rates
```bash
# Gateway request count
docker logs codeguardians-gateway-development | grep "POST.*process" | wc -l

# Recent requests
docker logs codeguardians-gateway-development --tail 100 | grep -E "(GET|POST)"
```

## Health Check Troubleshooting

### Verify Health Checks
```bash
# Check health check status
docker inspect codeguardians-gateway-development | grep -A 10 "Health"

# Manually run health check
docker exec codeguardians-gateway-development curl http://localhost:8000/health
docker exec codeguardians-tokenguard python health_check.py
```

### Service Health Status
```bash
# Gateway health
curl http://localhost:8000/health | python -m json.tool

# Guards health
curl http://localhost:8000/api/v1/guards/health | python -m json.tool
```

## Environment Variable Issues

### Check Environment Variables
```bash
# Gateway
docker exec codeguardians-gateway-development env | grep -E "(DATABASE|REDIS)"

# HealthGuard
docker exec codeguardians-healthguard env | grep -E "(DATABASE|HEALTHGUARD)"
```

### Verify .env File
```bash
# Check DATABASE_URL format
grep DATABASE_URL .env | grep -E "(asyncpg|psycopg2)"

# Check required variables
grep -E "^(DATABASE_URL|REDIS_PASSWORD|SECRET_KEY)=" .env
```

## Common Configuration Errors

### Error: "DATABASE_PASSWORD variable is not set"

**Solution:**
Set in `.env` file:
```bash
DATABASE_PASSWORD=REPLACE_ME
POSTGRES_PASSWORD=REPLACE_ME
```

### Error: "version attribute is obsolete"

**Solution:**
Remove `version:` line from docker-compose.yml (if present)

### Error: Service not found

**Solution:**
1. Check service name matches docker-compose.yml
2. Verify profile is correct: `--profile centralized`
3. Check service is enabled in docker-compose.yml

## Debugging Commands

### Enter Container Shell
```bash
# Gateway
docker exec -it codeguardians-gateway-development bash

# Postgres
docker exec -it codeguardians-postgres psql -U aiguardian

# Redis
docker exec -it codeguardians-redis redis-cli -a ${REDIS_PASSWORD}
```

### Check Service Configuration
```bash
# Gateway config
docker exec codeguardians-gateway-development python -c "from app.core.config import get_settings; print(get_settings())"

# Service URLs
docker exec codeguardians-gateway-development env | grep -E "(.*GUARD.*URL)"
```

### Test API Endpoints
```bash
# Unified endpoint
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"service_type": "tokenguard", "payload": {"text": "test"}}'

# Health endpoint
curl http://localhost:8000/health

# Metrics (if available)
curl http://localhost:8004/metrics
```

## Getting Help

1. **Check Logs:** Always start with logs
2. **Verify Health:** Check `/health` endpoints
3. **Check Network:** Verify service-to-service connectivity
4. **Check Environment:** Verify environment variables
5. **Check Documentation:** See `docs/` directory

## Related Documentation

- `docs/ENVIRONMENT_VARIABLES.md` - Environment variable reference
- `docs/REQUEST_ID_CORRELATION.md` - Request-ID correlation guide
- `docs/TEST_EXECUTION_REPORT.md` - Test execution results
- `IMPLEMENTATION_PROGRESS.md` - Implementation status

