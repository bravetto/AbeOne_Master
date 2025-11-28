# AIGuardian Troubleshooting Guide

**Complete Problem Resolution • Debug Procedures • Common Issues**

---

##  Quick Diagnostics

### Health Check Commands
```bash
# Basic health
curl -f http://localhost:8000/health/live

# Full readiness
curl -f http://localhost:8000/health/ready

# Service status
curl http://localhost:8000/api/v1/guards/services

# Container status
docker-compose ps
```

### Log Commands
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f codeguardians-gateway
docker-compose logs -f tokenguard

# Last 50 lines with timestamps
docker-compose logs -f --tail 50 --timestamps
```

---

##  Common Issues & Solutions

### 1. Services Not Starting

#### Symptoms
- Containers exit immediately
- "Connection refused" errors
- Health checks failing

#### Diagnosis
```bash
# Check container status
docker-compose ps

# View startup logs
docker-compose logs codeguardians-gateway

# Check resource usage
docker stats
```

#### Solutions

**Missing Environment Variables**
```bash
# Check if env.unified exists
ls -la codeguardians-gateway/codeguardians-gateway/env.unified

# Create from template if missing
cp env.example env.unified
```

**Port Conflicts**
```bash
# Check what's using ports 8000-8005
netstat -tulpn | grep :8000
netstat -tulpn | grep :8001
# ... etc

# Kill conflicting processes
sudo lsof -ti:8000 | xargs kill -9
```

**Docker Issues**
```bash
# Restart Docker
sudo systemctl restart docker

# Clean up Docker
docker system prune -a
docker volume prune
```

### 2. Database Connection Issues

#### Symptoms
- "Connection refused" to PostgreSQL
- "Could not connect to server"
- Database authentication failures

#### Diagnosis
```bash
# Check PostgreSQL container
docker exec codeguardians-gateway-postgres psql -U codeguardians-gateway -d codeguardians-gateway_db -c "SELECT 1;"

# Check connection string
echo $DATABASE_URL

# Check PostgreSQL logs
docker logs codeguardians-gateway-postgres
```

#### Solutions

**Invalid DATABASE_URL**
```bash
# Fix format
export DATABASE_URL="postgresql+asyncpg://codeguardians-gateway:postgres-password-dev@postgres:5432/codeguardians-gateway_db"
```

**Password Mismatch**
```bash
# Clean restart with new passwords
docker-compose down -v
docker-compose up -d
```

**Network Issues**
```bash
# Check Docker network
docker network ls
docker network inspect codeguardians-gateway_default
```

### 3. Redis Connection Issues

#### Symptoms
- Redis connection timeouts
- Cache not working
- Session storage failures

#### Diagnosis
```bash
# Test Redis connection
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev ping

# Check Redis logs
docker logs codeguardians-gateway-redis

# Check Redis configuration
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev CONFIG GET "*"
```

#### Solutions

**Authentication Issues**
```bash
# Verify password in env.unified
grep REDIS_PASSWORD env.unified

# Test with correct password
docker exec codeguardians-gateway-redis redis-cli -a $(grep REDIS_PASSWORD env.unified | cut -d'=' -f2) ping
```

**Memory Issues**
```bash
# Check Redis memory usage
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev INFO memory

# Clear Redis cache
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev FLUSHALL
```

### 4. API Endpoint Issues

#### Symptoms
- 404 errors on API calls
- 500 internal server errors
- Timeout errors

#### Diagnosis
```bash
# Test API endpoints
curl -v http://localhost:8000/health/live
curl -v http://localhost:8000/api/v1/guards/services

# Check gateway logs
docker logs codeguardians-gateway-production

# Test individual guard services
curl http://localhost:8001/health  # TokenGuard
curl http://localhost:8002/health  # TrustGuard
curl http://localhost:8003/health  # ContextGuard
curl http://localhost:8004/health  # BiasGuard
curl http://localhost:8005/health  # HealthGuard
```

#### Solutions

**Service Discovery Issues**
```bash
# Restart service discovery
curl -X POST http://localhost:8000/api/v1/guards/discovery/refresh

# Check service registration
curl http://localhost:8000/api/v1/guards/services
```

**Load Balancing Issues**
```bash
# Check if all services are healthy
docker-compose ps | grep healthy

# Restart unhealthy services
docker-compose restart tokenguard
```

### 5. Performance Issues

#### Symptoms
- Slow response times
- High memory usage
- CPU spikes

#### Diagnosis
```bash
# Check resource usage
docker stats

# Check system resources
htop
df -h
free -h

# Check application metrics
curl http://localhost:8000/metrics
```

#### Solutions

**Memory Issues**
```bash
# Increase memory limits in docker-compose.yml
services:
  codeguardians-gateway:
    deploy:
      resources:
        limits:
          memory: 2G
```

**CPU Issues**
```bash
# Check for infinite loops in logs
docker-compose logs -f | grep -i "error\|exception\|traceback"

# Restart services
docker-compose restart
```

### 6. Security Issues

#### Symptoms
- Authentication failures
- CORS errors
- SSL/TLS issues

#### Diagnosis
```bash
# Check CORS configuration
curl -H "Origin: http://localhost:3000" -v http://localhost:8000/health/live

# Check authentication
curl -H "Authorization: Bearer token" http://localhost:8000/api/v1/guards/services

# Check SSL configuration
openssl s_client -connect localhost:8000 -servername localhost
```

#### Solutions

**CORS Issues**
```bash
# Update ALLOWED_ORIGINS in env.unified
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,https://yourdomain.com
```

**Authentication Issues**
```bash
# Check JWT configuration
grep SECRET_KEY env.unified

# Verify Clerk configuration
grep CLERK env.unified
```

---

##  Advanced Debugging

### Container Debugging

#### Shell Access
```bash
# Access gateway container
docker exec -it codeguardians-gateway-production bash

# Access database
docker exec -it codeguardians-gateway-postgres psql -U codeguardians-gateway -d codeguardians-gateway_db

# Access Redis
docker exec -it codeguardians-gateway-redis redis-cli -a redis-password-dev
```

#### Environment Variables
```bash
# Check all environment variables
docker exec codeguardians-gateway-production printenv

# Check specific variables
docker exec codeguardians-gateway-production printenv | grep DATABASE
docker exec codeguardians-gateway-production printenv | grep REDIS
```

#### Network Debugging
```bash
# Check container networking
docker network ls
docker network inspect codeguardians-gateway_default

# Test internal connectivity
docker exec codeguardians-gateway-production curl http://tokenguard:8001/health
docker exec codeguardians-gateway-production curl http://postgres:5432
```

### Application Debugging

#### Python Debugging
```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Check Python environment
docker exec codeguardians-gateway-production python -c "import sys; print(sys.path)"
docker exec codeguardians-gateway-production python -c "import fastapi; print(fastapi.__version__)"
```

#### Database Debugging
```bash
# Check database connections
docker exec codeguardians-gateway-postgres psql -U codeguardians-gateway -d codeguardians-gateway_db -c "SELECT * FROM pg_stat_activity;"

# Check database size
docker exec codeguardians-gateway-postgres psql -U codeguardians-gateway -d codeguardians-gateway_db -c "SELECT pg_size_pretty(pg_database_size('codeguardians-gateway_db'));"
```

#### Redis Debugging
```bash
# Check Redis info
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev INFO

# Check Redis keys
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev KEYS "*"

# Monitor Redis commands
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev MONITOR
```

---

##  Configuration Issues

### Environment Variables

#### Missing Variables
```bash
# Check required variables
grep -E "^(SECRET_KEY|DATABASE_URL|REDIS_URL)" env.unified

# Generate missing secrets
export SECRET_KEY=$(openssl rand -hex 32)
export POSTGRES_REPLACE_ME rand -base64 32 | tr -d "=+/" | cut -c1-25)
export REDIS_REPLACE_ME rand -base64 32 | tr -d "=+/" | cut -c1-25)
```

#### Invalid Format
```bash
# Check DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql+asyncpg://user:password@host:port/database

# Check REDIS_URL format
echo $REDIS_URL
# Should be: REPLACE_MEhost:port/db
```

### Docker Configuration

#### Compose Issues
```bash
# Validate docker-compose.yml
docker-compose config

# Check for syntax errors
docker-compose config --quiet
```

#### Volume Issues
```bash
# Check volume mounts
docker volume ls
docker volume inspect codeguardians-gateway_postgres_data

# Clean volumes (WARNING: deletes data)
docker-compose down -v
```

---

##  Emergency Procedures

### Service Recovery

#### Complete System Restart
```bash
# Stop all services
docker-compose down

# Clean up
docker system prune -f
docker volume prune -f

# Fresh start
docker-compose up -d

# Wait for services
sleep 60

# Verify health
curl http://localhost:8000/health/live
```

#### Individual Service Recovery
```bash
# Restart specific service
docker-compose restart tokenguard

# Rebuild and restart
docker-compose up -d --build tokenguard

# Check service health
curl http://localhost:8001/health
```

### Data Recovery

#### Database Backup
```bash
# Create backup
docker exec codeguardians-gateway-postgres pg_dump -U codeguardians-gateway codeguardians-gateway_db > backup.sql

# Restore from backup
docker exec -i codeguardians-gateway-postgres psql -U codeguardians-gateway codeguardians-gateway_db < backup.sql
```

#### Redis Backup
```bash
# Save Redis data
docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev BGSAVE

# Copy Redis dump
docker cp codeguardians-gateway-redis:/data/dump.rdb ./redis-backup.rdb
```

---

##  Monitoring & Alerts

### Health Monitoring

#### Automated Health Checks
```bash
# Create health check script
cat > health-check.sh << 'EOF'
#!/bin/bash
HEALTH_URL="http://localhost:8000/health/live"
if curl -f -s "$HEALTH_URL" > /dev/null; then
    echo " AIGuardian is healthy"
    exit 0
else
    echo " AIGuardian is unhealthy"
    exit 1
fi
EOF

chmod +x health-check.sh
```

#### Service Monitoring
```bash
# Monitor all services
watch -n 5 'docker-compose ps'

# Monitor resource usage
watch -n 5 'docker stats --no-stream'
```

### Log Monitoring

#### Log Aggregation
```bash
# Follow all logs
docker-compose logs -f --tail 100

# Filter error logs
docker-compose logs -f | grep -i "error\|exception\|traceback"

# Monitor specific service
docker-compose logs -f codeguardians-gateway | grep -i "error"
```

#### Log Analysis
```bash
# Count errors
docker-compose logs | grep -i "error" | wc -l

# Find most common errors
docker-compose logs | grep -i "error" | sort | uniq -c | sort -nr
```

---

##  Diagnostic Scripts

### Complete System Check
```bash
#!/bin/bash
# save as: system-check.sh

echo " AIGuardian System Diagnostic"
echo "================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test function
test_endpoint() {
    local url=$1
    local name=$2
    if curl -s -f "$url" > /dev/null; then
        echo -e "${GREEN}${NC} $name: OK"
    else
        echo -e "${RED}${NC} $name: FAILED"
    fi
}

echo "Testing Health Endpoints..."
test_endpoint "http://localhost:8000/health/live" "Gateway Health"
test_endpoint "http://localhost:8000/health/ready" "Gateway Readiness"
test_endpoint "http://localhost:8001/health" "TokenGuard"
test_endpoint "http://localhost:8002/health" "TrustGuard"
test_endpoint "http://localhost:8003/health" "ContextGuard"
test_endpoint "http://localhost:8004/health" "BiasGuard"

echo ""
echo "Testing Database Connections..."

# PostgreSQL
if docker exec codeguardians-gateway-postgres psql -U codeguardians-gateway -d codeguardians-gateway_db -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}${NC} PostgreSQL: OK"
else
    echo -e "${RED}${NC} PostgreSQL: FAILED"
fi

# Redis
if docker exec codeguardians-gateway-redis redis-cli -a redis-password-dev ping 2>/dev/null | grep -q "PONG"; then
    echo -e "${GREEN}${NC} Redis: OK"
else
    echo -e "${RED}${NC} Redis: FAILED"
fi

echo ""
echo "Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(NAME|guard|postgres|redis)"

echo ""
echo "Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "================================"
echo " Diagnostic Complete!"
```

### Performance Analysis
```bash
#!/bin/bash
# save as: performance-check.sh

echo " AIGuardian Performance Analysis"
echo "=================================="

echo "Container Resource Usage:"
docker stats --no-stream

echo ""
echo "Disk Usage:"
df -h

echo ""
echo "Memory Usage:"
free -h

echo ""
echo "Network Connections:"
netstat -tulpn | grep -E ":800[0-6]"

echo ""
echo "API Response Times:"
time curl -s http://localhost:8000/health/live > /dev/null
time curl -s http://localhost:8000/api/v1/guards/services > /dev/null
```

---

##  Troubleshooting Checklist

### Pre-Startup
- [ ] Docker is running
- [ ] Ports 8000-8005 are available
- [ ] `env.unified` file exists
- [ ] Required environment variables are set
- [ ] No conflicting services running

### During Startup
- [ ] All containers start successfully
- [ ] Health checks pass
- [ ] Database connections work
- [ ] Redis connections work
- [ ] API endpoints respond

### Runtime
- [ ] Services remain healthy
- [ ] No memory leaks
- [ ] Response times acceptable
- [ ] No error logs
- [ ] External integrations working

### Post-Issue
- [ ] Logs reviewed
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] System tested
- [ ] Documentation updated

---

##  Emergency Contacts

### Escalation Path
1. **Level 1**: Check logs and restart services
2. **Level 2**: Review configuration and network
3. **Level 3**: Contact development team
4. **Level 4**: Contact infrastructure team

### Quick Recovery Commands
```bash
# Nuclear option - complete reset
docker-compose down -v
docker system prune -a -f
docker-compose up -d

# Service-specific restart
docker-compose restart [service-name]

# Health verification
curl http://localhost:8000/health/live
```

---

**Remember**: Always check logs first, then try simple fixes before escalating to complex solutions!
