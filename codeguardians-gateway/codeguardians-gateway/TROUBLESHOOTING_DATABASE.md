# Database Troubleshooting Guide

## Overview

This guide helps diagnose and resolve common database issues in the AI Guardians platform.

## Prerequisites

- Docker and Docker Compose
- PostgreSQL client tools (optional)
- Database access credentials

## Common Issues

### 1. Database Connection Failed

#### Symptoms
- Application fails to start
- "Connection refused" errors
- Database connection timeouts

#### Diagnosis
```bash
# Check if PostgreSQL container is running
docker-compose ps postgres

# Check container logs
docker-compose logs postgres

# Test connection
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "SELECT 1;"
```

#### Solutions

**Container not running:**
```bash
# Start PostgreSQL container
docker-compose up postgres -d

# Check if container starts successfully
docker-compose logs postgres
```

**Connection configuration:**
```bash
# Check environment variables
cat .env | grep DATABASE

# Verify database URL format
# Should be: REPLACE_MEhost:port/database
```

**Network issues:**
```bash
# Check Docker network
docker network ls
docker network inspect aiguardian_default

# Restart Docker network
docker-compose down
docker-compose up -d
```

### 2. Migration Failures

#### Symptoms
- "Migration failed" errors
- Database schema inconsistencies
- Table not found errors

#### Diagnosis
```bash
# Check migration status
docker-compose exec gateway alembic current

# Check migration history
docker-compose exec gateway alembic history

# Check database schema
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "\dt"
```

#### Solutions

**Reset migrations:**
```bash
# Rollback to base
docker-compose exec gateway alembic downgrade base

# Run migrations
docker-compose exec gateway alembic upgrade head
```

**Manual migration:**
```bash
# Create new migration
docker-compose exec gateway alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec gateway alembic upgrade head
```

**Fix migration conflicts:**
```bash
# Edit migration file
docker-compose exec gateway nano alembic/versions/XXXX_migration.py

# Re-run migration
docker-compose exec gateway alembic upgrade head
```

### 3. Database Performance Issues

#### Symptoms
- Slow query responses
- High CPU usage
- Connection pool exhaustion

#### Diagnosis
```bash
# Check database statistics
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables;"

# Check active connections
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    query
FROM pg_stat_activity
WHERE state = 'active';"

# Check slow queries
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;"
```

#### Solutions

**Optimize queries:**
```sql
-- Add indexes
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY idx_requests_created_at ON requests(created_at);

-- Analyze tables
ANALYZE users;
ANALYZE requests;
```

**Increase connection pool:**
```python
# In .env file
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30
```

**Database maintenance:**
```bash
# Vacuum database
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "VACUUM ANALYZE;"

# Reindex database
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "REINDEX DATABASE aiguardian_db;"
```

### 4. Data Corruption

#### Symptoms
- Inconsistent data
- Foreign key constraint violations
- Checksum errors

#### Diagnosis
```bash
# Check database integrity
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE schemaname = 'public';"

# Check for orphaned records
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "
SELECT COUNT(*) FROM requests r
LEFT JOIN users u ON r.user_id = u.id
WHERE u.id IS NULL;"
```

#### Solutions

**Data repair:**
```sql
-- Fix orphaned records
DELETE FROM requests 
WHERE user_id NOT IN (SELECT id FROM users);

-- Update corrupted data
UPDATE users 
SET email = LOWER(email) 
WHERE email != LOWER(email);
```

**Restore from backup:**
```bash
# Stop application
docker-compose down

# Restore database
docker-compose exec postgres pg_restore -U aiguardian -d aiguardian_db /backup/backup.sql

# Start application
docker-compose up -d
```

### 5. Authentication Issues

#### Symptoms
- "Authentication failed" errors
- Permission denied errors
- User creation failures

#### Diagnosis
```bash
# Check user permissions
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "
SELECT 
    rolname,
    rolsuper,
    rolinherit,
    rolcreaterole,
    rolcreatedb,
    rolcanlogin
FROM pg_roles
WHERE rolname = 'aiguardian';"

# Check database permissions
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "
SELECT 
    grantee,
    privilege_type,
    is_grantable
FROM information_schema.role_table_grants
WHERE table_name = 'users';"
```

#### Solutions

**Fix user permissions:**
```sql
-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE aiguardian_db TO aiguardian;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO aiguardian;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO aiguardian;
```

**Reset user password:**
```bash
# Change password
docker-compose exec postgres psql -U postgres -c "
ALTER USER aiguardian PASSWORD 'new_password';"

# Update .env file
echo "DATABASE_REPLACE_ME >> .env
```

### 6. Backup and Recovery

#### Create Backup
```bash
# Full database backup
docker-compose exec postgres pg_dump -U aiguardian -d aiguardian_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Compressed backup
docker-compose exec postgres pg_dump -U aiguardian -d aiguardian_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Schema only backup
docker-compose exec postgres pg_dump -U aiguardian -d aiguardian_db --schema-only > schema_backup.sql

# Data only backup
docker-compose exec postgres pg_dump -U aiguardian -d aiguardian_db --data-only > data_backup.sql
```

#### Restore Backup
```bash
# Stop application
docker-compose down

# Drop and recreate database
docker-compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS aiguardian_db;"
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE aiguardian_db OWNER aiguardian;"

# Restore backup
docker-compose exec -T postgres psql -U aiguardian -d aiguardian_db < backup.sql

# Start application
docker-compose up -d
```

### 7. Monitoring and Logging

#### Enable Query Logging
```bash
# Edit PostgreSQL configuration
docker-compose exec postgres psql -U postgres -c "
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();"
```

#### Monitor Database Metrics
```bash
# Check database size
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "
SELECT 
    pg_size_pretty(pg_database_size('aiguardian_db')) as database_size;"

# Check table sizes
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;"
```

### 8. Production Considerations

#### Connection Pooling
```python
# In database configuration
DATABASE_POOL_SIZE = 20
DATABASE_MAX_OVERFLOW = 30
DATABASE_POOL_TIMEOUT = 30
DATABASE_POOL_RECYCLE = 3600
```

#### Read Replicas
```python
# Configure read replicas
DATABASE_READ_REPLICA_URL = "REPLACE_MEread-replica:5432/db"
```

#### Backup Strategy
```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U aiguardian -d aiguardian_db | gzip > "$BACKUP_DIR/backup_$DATE.sql.gz"
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +7 -delete
```

## Prevention

### Regular Maintenance
```bash
# Weekly maintenance script
#!/bin/bash
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "VACUUM ANALYZE;"
docker-compose exec postgres psql -U aiguardian -d aiguardian_db -c "REINDEX DATABASE aiguardian_db;"
```

### Monitoring
- Set up database monitoring
- Configure alerts for connection failures
- Monitor disk space and performance
- Regular backup verification

### Documentation
- Document database schema changes
- Keep migration history
- Document recovery procedures
- Maintain backup schedules

## Getting Help

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Discord Community](https://discord.gg/aiguardian)
- [GitHub Issues](https://github.com/bravetto/AI-Guardians/issues)

