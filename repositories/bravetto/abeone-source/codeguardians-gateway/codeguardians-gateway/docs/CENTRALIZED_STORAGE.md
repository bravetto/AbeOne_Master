# Centralized Storage Architecture

This document describes the centralized storage architecture for the CodeGuardians Gateway, which enables full horizontal scaling by eliminating all local storage dependencies.

## Overview

The application has been migrated from local file storage to a centralized storage architecture using:

- **PostgreSQL**: Shared database for all services
- **Redis**: Distributed caching and session storage
- **AWS S3**: Cloud-based file storage
- **Environment Variables**: Configuration management

This architecture enables:
- **Horizontal Scaling**: Multiple replicas can run simultaneously
- **High Availability**: No single point of failure
- **Consistency**: All replicas share the same data
- **Performance**: Distributed caching with Redis
- **Scalability**: Cloud-native storage solutions

## Architecture Diagram

```
        
   Load Balancer        FastAPI App          Shared Storage
                        (Multiple                          
          Replicas)          
     Replica 1      PostgreSQL 
           Replica 2         Database  
              
     Replica 3             
           Replica N           Redis    
               Cache     
                             
                                                
                                                   AWS S3    
                                                File Storage 
                                                
                                              
```

## Storage Components

### 1. PostgreSQL Database

**Purpose**: Primary data storage for all services
**Services Using**: Main Gateway, HealthGuard, all Guard services

**Configuration**:
```bash
# Database connection
DATABASE_URL=postgresql+psycopg2://codeguardians-gateway:password@postgres:5432/codeguardians-gateway_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=codeguardians-gateway_db
POSTGRES_USER=codeguardians-gateway
POSTGRES_REPLACE_ME
```

**Tables**:
- `users` - User accounts and profiles
- `sessions` - User sessions (legacy, being migrated to Redis)
- `organizations` - Organization data
- `subscriptions` - Subscription management
- `biasguard_audit_logs` - BiasGuard audit logs
- `biasguard_policy_violations` - Policy violations
- `poisonguard_analysis_results` - HealthGuard analysis results
- `poisonguard_health_metrics` - Health metrics

### 2. Redis Cache

**Purpose**: Distributed caching and session storage
**Services Using**: Main Gateway, ContextGuard, all Guard services

**Configuration**:
```bash
# Redis connection
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_REPLACE_ME
```

**Usage Patterns**:
- **Rate Limiting**: Dynamic rate limit storage
- **A/B Testing**: Experiment assignments and configurations
- **Usage Tracking**: Real-time API usage metrics
- **ContextGuard Memory**: Distributed conversational memory
- **User Sessions**: Session data and metadata
- **Dynamic Config**: Runtime configuration management

### 3. AWS S3 File Storage

**Purpose**: Cloud-based file storage for uploads
**Services Using**: Main Gateway

**Configuration**:
```bash
# S3 configuration
S3_ENABLED=true
S3_BUCKET_NAME=codeguardians-gateway-uploads
S3_REGION=us-east-1
S3_ACCESS_KEY_ID=your-access-key
S3_SECRET_ACCESS_KEY=your-secret-key
S3_ENDPOINT_URL=  # Optional: for local testing with MinIO
```

**Features**:
- **Direct Upload**: Presigned URLs for client-side uploads
- **File Management**: Upload, download, delete, metadata
- **Security**: Private ACLs, signed URLs
- **Scalability**: Unlimited storage capacity

## Service-Specific Changes

### Main Gateway

**Changes Made**:
-  S3 file storage integration
-  Redis session management
-  Dynamic configuration via Redis
-  Rate limiting with Redis
-  A/B testing with Redis

**Storage Dependencies**:
- PostgreSQL: User data, organizations, subscriptions
- Redis: Sessions, cache, rate limiting, A/B testing
- S3: File uploads and downloads

### HealthGuard

**Changes Made**:
-  Migrated from SQLite to PostgreSQL
-  Removed local file storage dependencies
-  Added connection pooling for PostgreSQL

**Storage Dependencies**:
- PostgreSQL: Analysis results, health metrics
- Redis: Caching (if implemented)

### ContextGuard

**Changes Made**:
-  Redis-backed memory storage
-  Distributed conversational memory
-  Fallback to in-memory storage
-  TTL support for memory items

**Storage Dependencies**:
- Redis: Distributed memory storage
- Local Memory: Fallback and caching

### TokenGuard, TrustGuard, BiasGuard

**Current Status**: Using shared PostgreSQL and Redis
**Storage Dependencies**:
- PostgreSQL: Audit logs, policy violations
- Redis: Caching and session data

## Environment Configuration

### Required Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql+psycopg2://codeguardians-gateway:password@postgres:5432/codeguardians-gateway_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=codeguardians-gateway_db
POSTGRES_USER=codeguardians-gateway
POSTGRES_REPLACE_ME

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_REPLACE_ME

# S3 Configuration
S3_ENABLED=true
S3_BUCKET_NAME=codeguardians-gateway-uploads
S3_REGION=us-east-1
S3_ACCESS_KEY_ID=your-access-key
S3_SECRET_ACCESS_KEY=your-secret-key

# Session Management
SESSION_TTL=3600
SESSION_CLEANUP_INTERVAL=300
SESSION_STORAGE_TYPE=redis

# ContextGuard Configuration
CONTEXTGUARD_USE_REDIS=true
CONTEXTGUARD_REDIS_URL=redis://redis:6379/0
CONTEXTGUARD_KEY_PREFIX=contextguard:
CONTEXTGUARD_DEFAULT_TTL=3600

# HealthGuard Configuration
HEALTHGUARD_DATABASE_URL=postgresql+psycopg2://codeguardians-gateway:password@postgres:5432/codeguardians-gateway_db
```

## Docker Compose Configuration

### Shared Services

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=codeguardians-gateway_db
      - POSTGRES_USER=codeguardians-gateway
      - POSTGRES_REPLACE_ME
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - codeguardians-gateway_network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - codeguardians-gateway_network
```

### Service Dependencies

All services now depend on shared storage:

```yaml
services:
  codeguardians-gateway:
    depends_on:
      - postgres
      - redis
    environment:
      - DATABASE_URL=postgresql+psycopg2://codeguardians-gateway:${POSTGRES_PASSWORD}@postgres:5432/codeguardians-gateway_db
      - REDIS_HOST=redis
      - REDIS_PORT=6379

  healthguard:
    depends_on:
      - postgres
    environment:
      - HEALTHGUARD_DATABASE_URL=postgresql+psycopg2://codeguardians-gateway:${POSTGRES_PASSWORD}@postgres:5432/codeguardians-gateway_db

  contextguard:
    depends_on:
      - redis
    environment:
      - CONTEXTGUARD_USE_REDIS=true
      - CONTEXTGUARD_REDIS_URL=redis://redis:6379/0
```

## Migration Guide

### From Local Storage to Centralized Storage

1. **Database Migration**:
   ```bash
   # HealthGuard SQLite to PostgreSQL
   # Data migration scripts provided
   python scripts/migrate_healthguard_to_postgres.py
   ```

2. **Session Migration**:
   ```bash
   # Database sessions to Redis
   python scripts/migrate_sessions_to_redis.py
   ```

3. **Configuration Migration**:
   ```bash
   # File-based config to Redis
   python scripts/migrate_config_to_redis.py
   ```

### Rollback Strategy

Each component includes fallback mechanisms:

- **HealthGuard**: Falls back to SQLite if PostgreSQL unavailable
- **ContextGuard**: Falls back to in-memory storage if Redis unavailable
- **Sessions**: Falls back to database storage if Redis unavailable
- **File Storage**: Falls back to local storage if S3 unavailable

## Performance Considerations

### Redis Caching Strategy

- **Session Data**: TTL-based expiration
- **Rate Limiting**: Sliding window counters
- **A/B Testing**: Cached experiment assignments
- **ContextGuard**: TTL-based memory management

### Database Optimization

- **Connection Pooling**: Configured for all services
- **Indexes**: Optimized for common queries
- **Partitioning**: For large audit log tables

### S3 Performance

- **Presigned URLs**: Direct client uploads
- **CDN Integration**: Optional CloudFront setup
- **Compression**: Automatic file compression

## Monitoring and Health Checks

### Health Check Endpoints

- **Main Gateway**: `/health` - Overall system health
- **HealthGuard**: `/health` - Service and database health
- **ContextGuard**: `/health` - Service and Redis health
- **Redis**: `redis-cli ping` - Redis connectivity
- **PostgreSQL**: `pg_isready` - Database connectivity

### Metrics

- **Database**: Connection pool metrics, query performance
- **Redis**: Memory usage, hit/miss ratios, connection count
- **S3**: Upload/download metrics, error rates
- **Sessions**: Active sessions, expiration rates

## Security Considerations

### Database Security

- **Connection Encryption**: TLS for database connections
- **Access Control**: Role-based database permissions
- **Audit Logging**: All database operations logged

### Redis Security

- **Authentication**: Redis AUTH configuration
- **Network Security**: Internal network only
- **Data Encryption**: TLS for Redis connections

### S3 Security

- **IAM Roles**: Least privilege access
- **Bucket Policies**: Restrictive access controls
- **Encryption**: Server-side encryption enabled
- **Presigned URLs**: Time-limited access

## Troubleshooting

### Common Issues

1. **Redis Connection Failed**:
   ```bash
   # Check Redis service
   docker-compose logs redis
   
   # Test Redis connectivity
   docker-compose exec redis redis-cli ping
   ```

2. **PostgreSQL Connection Failed**:
   ```bash
   # Check PostgreSQL service
   docker-compose logs postgres
   
   # Test database connectivity
   docker-compose exec postgres pg_isready -U codeguardians-gateway
   ```

3. **S3 Upload Failed**:
   ```bash
   # Check S3 configuration
   echo $S3_BUCKET_NAME
   echo $S3_ACCESS_KEY_ID
   
   # Test S3 connectivity
   aws s3 ls s3://$S3_BUCKET_NAME
   ```

### Log Analysis

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f codeguardians-gateway
docker-compose logs -f healthguard
docker-compose logs -f contextguard
```

## Scaling Guidelines

### Horizontal Scaling

1. **Load Balancer**: Configure multiple replicas
2. **Database**: Read replicas for read-heavy workloads
3. **Redis**: Redis Cluster for high availability
4. **S3**: Global distribution with CloudFront

### Resource Requirements

**Minimum**:
- PostgreSQL: 2GB RAM, 20GB storage
- Redis: 1GB RAM, 5GB storage
- S3: Pay-per-use storage

**Recommended**:
- PostgreSQL: 4GB RAM, 100GB storage
- Redis: 2GB RAM, 20GB storage
- S3: 1TB storage with CloudFront

## Future Enhancements

### Planned Improvements

1. **Redis Cluster**: High availability Redis setup
2. **Database Read Replicas**: Improved read performance
3. **S3 CloudFront**: Global CDN for file delivery
4. **Monitoring**: Prometheus/Grafana integration
5. **Backup**: Automated backup strategies

### Migration Scripts

- `scripts/migrate_healthguard_to_postgres.py`
- `scripts/migrate_sessions_to_redis.py`
- `scripts/migrate_config_to_redis.py`
- `scripts/validate_centralized_storage.py`

## Conclusion

The centralized storage architecture enables full horizontal scaling of the CodeGuardians Gateway while maintaining high availability and performance. All local storage dependencies have been eliminated, and the system now uses cloud-native storage solutions that can scale independently.

For questions or issues, refer to the troubleshooting section or contact the development team.
