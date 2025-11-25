# Debug Startup Guide

## Overview

This guide helps diagnose and resolve startup issues in the AI Guardians platform.

## Prerequisites

- Docker and Docker Compose
- Access to application logs
- Basic understanding of containerized applications

## Common Startup Issues

### 1. Container Startup Failures

#### Symptoms
- Containers fail to start
- "Exit code 1" errors
- Container keeps restarting

#### Diagnosis
```bash
# Check container status
docker-compose ps

# Check container logs
docker-compose logs

# Check specific service logs
docker-compose logs gateway
docker-compose logs postgres
docker-compose logs redis
```

#### Solutions

**Port conflicts:**
```bash
# Check for port conflicts
netstat -tulpn | grep :8000
netstat -tulpn | grep :5432
netstat -tulpn | grep :6379

# Kill conflicting processes
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:5432 | xargs kill -9
sudo lsof -ti:6379 | xargs kill -9
```

**Resource constraints:**
```bash
# Check system resources
docker system df
docker system prune

# Increase Docker resources
# Edit Docker Desktop settings
# Memory: 4GB+
# CPU: 2+ cores
```

**Configuration errors:**
```bash
# Validate docker-compose.yml
docker-compose config

# Check environment variables
docker-compose config --services
```

### 2. Database Connection Issues

#### Symptoms
- "Database connection failed" errors
- Application waits for database
- Migration failures

#### Diagnosis
```bash
# Check database container
docker-compose logs postgres

# Test database connection
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "SELECT 1;"

# Check database readiness
docker-compose exec postgres pg_isready -U aiguardian -d aiguardian_db
```

#### Solutions

**Wait for database:**
```yaml
# In docker-compose.yml
services:
  gateway:
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "aiguardian", "-d", "aiguardian_db"]
      interval: 5s
      timeout: 5s
      retries: 5
```

**Fix connection string:**
```bash
# Check environment variables
cat .env | grep DATABASE

# Verify database URL format
# Should be: REPLACE_MEhost:port/database
```

### 3. Redis Connection Issues

#### Symptoms
- "Redis connection failed" errors
- Cache operations fail
- Session storage issues

#### Diagnosis
```bash
# Check Redis container
docker-compose logs redis

# Test Redis connection
docker-compose exec redis redis-cli ping

# Check Redis memory
docker-compose exec redis redis-cli info memory
```

#### Solutions

**Redis configuration:**
```bash
# Check Redis configuration
docker-compose exec redis redis-cli config get "*"

# Reset Redis
docker-compose down
docker volume rm aiguardian_redis_data
docker-compose up -d
```

### 4. Environment Variable Issues

#### Symptoms
- "Environment variable not set" errors
- Configuration validation failures
- Service initialization errors

#### Diagnosis
```bash
# Check environment file
cat .env

# Validate environment variables
docker-compose config

# Check service environment
docker-compose exec gateway env | grep -E "(DATABASE|REDIS|API)"
```

#### Solutions

**Missing environment variables:**
```bash
# Copy from example
cp .env.example .env

# Edit environment file
nano .env

# Required variables:
# DATABASE_URL
# REDIS_URL
# SECRET_KEY
# API_KEYS
```

**Invalid environment values:**
```bash
# Check variable format
echo $DATABASE_URL
echo $REDIS_URL

# Fix format issues
# DATABASE_URL should be: REPLACE_MEhost:port/db
# REDIS_URL should be: redis://host:port/db
```

### 5. Service Dependencies

#### Symptoms
- Services start in wrong order
- Dependency not ready errors
- Circular dependency issues

#### Diagnosis
```bash
# Check service dependencies
docker-compose config | grep -A 10 "depends_on"

# Check startup order
docker-compose up --no-start
docker-compose start postgres
docker-compose start redis
docker-compose start gateway
```

#### Solutions

**Fix dependency order:**
```yaml
# In docker-compose.yml
services:
  gateway:
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
```

**Add health checks:**
```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U aiguardian -d aiguardian_db"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### 6. Network Issues

#### Symptoms
- "Connection refused" errors
- Services can't communicate
- DNS resolution failures

#### Diagnosis
```bash
# Check Docker networks
docker network ls
docker network inspect aiguardian_default

# Test service connectivity
docker-compose exec gateway ping postgres
docker-compose exec gateway ping redis

# Check port bindings
docker-compose port gateway 8000
docker-compose port postgres 5432
```

#### Solutions

**Network configuration:**
```yaml
# In docker-compose.yml
services:
  gateway:
    networks:
      - aiguardian_network
  postgres:
    networks:
      - aiguardian_network

networks:
  aiguardian_network:
    driver: bridge
```

**Port mapping:**
```yaml
services:
  gateway:
    ports:
      - "8000:8000"
  postgres:
    ports:
      - "5432:5432"
```

### 7. Application Code Issues

#### Symptoms
- Import errors
- Syntax errors
- Module not found errors

#### Diagnosis
```bash
# Check application logs
docker-compose logs gateway

# Test Python imports
docker-compose exec gateway python -c "import app"

# Check Python path
docker-compose exec gateway python -c "import sys; print(sys.path)"
```

#### Solutions

**Fix import issues:**
```bash
# Check file structure
docker-compose exec gateway ls -la app/

# Fix relative imports
# Use absolute imports: from app.core.config import get_settings
```

**Fix syntax errors:**
```bash
# Validate Python syntax
docker-compose exec gateway python -m py_compile app/main.py

# Check for syntax errors
docker-compose exec gateway python -m flake8 app/
```

### 8. Resource Exhaustion

#### Symptoms
- Out of memory errors
- Container killed
- Slow startup times

#### Diagnosis
```bash
# Check system resources
docker stats

# Check container resource usage
docker-compose exec gateway top

# Check disk space
df -h
docker system df
```

#### Solutions

**Increase resources:**
```yaml
# In docker-compose.yml
services:
  gateway:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

**Clean up resources:**
```bash
# Clean Docker system
docker system prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune
```

## Debugging Steps

### 1. Check Container Status
```bash
# List all containers
docker-compose ps

# Check container logs
docker-compose logs --tail=100

# Follow logs in real-time
docker-compose logs -f
```

### 2. Validate Configuration
```bash
# Validate docker-compose.yml
docker-compose config

# Check environment variables
docker-compose config --services
```

### 3. Test Individual Services
```bash
# Start services one by one
docker-compose up postgres -d
docker-compose up redis -d
docker-compose up gateway -d

# Test service connectivity
docker-compose exec gateway curl http://localhost:8000/health
```

### 4. Check Logs
```bash
# Application logs
docker-compose logs gateway

# Database logs
docker-compose logs postgres

# Redis logs
docker-compose logs redis
```

### 5. Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
docker-compose up

# Run with debug flags
docker-compose run --rm gateway python -m debugpy --listen 0.0.0.0:5678 app/main.py
```

## Common Solutions

### Quick Fixes
```bash
# Restart all services
docker-compose restart

# Rebuild and restart
docker-compose up --build

# Clean restart
docker-compose down
docker-compose up -d

# Reset everything
docker-compose down -v
docker-compose up --build
```

### Environment Reset
```bash
# Reset environment
rm .env
cp .env.example .env
nano .env

# Regenerate secrets
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Database Reset
```bash
# Reset database
docker-compose down
docker volume rm aiguardian_postgres_data
docker-compose up -d

# Run migrations
docker-compose exec gateway alembic upgrade head
```

## Prevention

### Health Checks
```yaml
# Add health checks to all services
services:
  gateway:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Monitoring
```bash
# Monitor resource usage
docker stats

# Monitor logs
docker-compose logs -f

# Monitor health
curl http://localhost:8000/health
```

### Documentation
- Document all configuration changes
- Keep startup procedures updated
- Document common issues and solutions
- Maintain troubleshooting runbooks

## Getting Help

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Discord Community](https://discord.gg/aiguardian)
- [GitHub Issues](https://github.com/bravetto/AI-Guardians/issues)

