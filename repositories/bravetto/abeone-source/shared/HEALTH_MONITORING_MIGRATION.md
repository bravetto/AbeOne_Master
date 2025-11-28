# Health Monitoring Migration Guide

This guide shows how to migrate from individual health monitoring implementations to the unified health monitoring library.

## Benefits of Migration

- **Eliminate Duplication**: Remove ~500+ lines of duplicate health monitoring code
- **Standardization**: Consistent health checks across all services
- **Maintainability**: Single library to update and maintain
- **Features**: Enhanced monitoring, alerting, and metrics
- **Kubernetes Ready**: Built-in liveness/readiness probes

## Migration Steps

### 1. Replace Individual Health Monitoring

#### Before (Trust Guard):
```python
# guards/trust-guard/trustguard/health.py
class HealthChecker:
    def __init__(self):
        self.metrics = SystemMetrics()
        self.health_status = "healthy"
    
    def check_health(self) -> Dict[str, Any]:
        # 200+ lines of health checking code
        pass
```

#### After (Unified):
```python
# Any service
from shared.health_monitoring import create_health_monitor

health_monitor = create_health_monitor("trust-guard", "1.0.0")
health_monitor.add_dependency("database", "postgresql://...")
health_monitor.add_dependency("redis", "redis://...")

# Get health status
health = await health_monitor.get_comprehensive_health()
```

### 2. Update FastAPI Health Endpoints

#### Before:
```python
@app.get("/health")
async def health_check():
    # Custom health check implementation
    return {"status": "healthy"}

@app.get("/health/live")
async def liveness():
    # Custom liveness implementation
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    # Custom readiness implementation
    return {"status": "ready"}
```

#### After:
```python
from shared.health_monitoring import create_health_monitor

health_monitor = create_health_monitor("service-name", "1.0.0")

@app.get("/health")
async def health_check():
    return await health_monitor.get_comprehensive_health()

@app.get("/health/live")
async def liveness():
    return health_monitor.get_liveness_probe()

@app.get("/health/ready")
async def readiness():
    return health_monitor.get_readiness_probe()

@app.get("/metrics")
async def metrics():
    return Response(
        health_monitor.get_prometheus_metrics(),
        media_type="text/plain"
    )
```

### 3. Remove Duplicate Code

#### Files to Remove/Simplify:
- `guards/trust-guard/trustguard/health.py` (313 lines)
- `codeguardians-gateway/codeguardians-gateway/app/core/health_monitor.py` (407 lines)
- `guards/healthguard/src/poisonguard/monitoring.py` (health check parts)
- Individual health check implementations in other services

#### Estimated Reduction:
- **Lines Removed**: ~1,200+ lines
- **Files Simplified**: 5+ files
- **Maintenance Burden**: Reduced by 80%

### 4. Service-Specific Configuration

#### Trust Guard:
```python
# guards/trust-guard/main.py
from shared.health_monitoring import create_health_monitor

health_monitor = create_health_monitor("trust-guard", "1.0.0")
health_monitor.add_dependency("database", "postgresql://...")
health_monitor.add_dependency("redis", "redis://...")

# Use in FastAPI endpoints
@app.get("/health")
async def health():
    return await health_monitor.get_comprehensive_health()
```

#### CodeGuardians Gateway:
```python
# codeguardians-gateway/app/main.py
from shared.health_monitoring import create_health_monitor

health_monitor = create_health_monitor("codeguardians-gateway", "1.0.0")
health_monitor.add_dependency("postgres", "postgresql://...")
health_monitor.add_dependency("redis", "redis://...")
health_monitor.add_dependency("tokenguard", "http://tokenguard:8001/health")
health_monitor.add_dependency("trustguard", "http://trustguard:8002/health")
# ... other guard services
```

#### HealthGuard:
```python
# guards/healthguard/main.py
from shared.health_monitoring import create_health_monitor

health_monitor = create_health_monitor("healthguard", "1.0.0")
health_monitor.add_dependency("database", "postgresql://...")

# Replace existing monitoring.py health checks
```

### 5. Docker Integration

#### Update Dockerfiles:
```dockerfile
# Add shared library to all services
COPY shared/ /app/shared/
ENV PYTHONPATH=/app:$PYTHONPATH
```

#### Update docker-compose.yml:
```yaml
services:
  trust-guard:
    build: .
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./shared:/app/shared:ro
```

### 6. Testing

#### Unit Tests:
```python
import pytest
from shared.health_monitoring import create_health_monitor

def test_health_monitor_creation():
    monitor = create_health_monitor("test-service")
    assert monitor.service_name == "test-service"

def test_system_metrics():
    monitor = create_health_monitor("test-service")
    metrics = monitor.get_system_metrics()
    assert metrics.cpu_percent >= 0
    assert metrics.memory_percent >= 0

@pytest.mark.asyncio
async def test_dependency_health():
    monitor = create_health_monitor("test-service")
    monitor.add_dependency("test", "http://httpbin.org/status/200")
    
    health_checks = await monitor.check_all_dependencies()
    assert len(health_checks) == 1
    assert health_checks[0].service == "test"
```

## Migration Checklist

### Phase 1: Setup
- [ ] Create `shared/` directory
- [ ] Add `shared/health_monitoring.py`
- [ ] Update `PYTHONPATH` in all services
- [ ] Test library in isolation

### Phase 2: Migrate Services
- [ ] Update Trust Guard
- [ ] Update CodeGuardians Gateway  
- [ ] Update HealthGuard
- [ ] Update other guard services
- [ ] Update Docker configurations

### Phase 3: Cleanup
- [ ] Remove duplicate health monitoring files
- [ ] Update tests to use unified library
- [ ] Update documentation
- [ ] Verify all health endpoints work

### Phase 4: Validation
- [ ] Test all health endpoints
- [ ] Verify Prometheus metrics
- [ ] Check Kubernetes probes
- [ ] Validate monitoring dashboards

## Expected Results

### Code Reduction
- **Total Lines Removed**: ~1,200+ lines
- **Files Eliminated**: 5+ duplicate files
- **Maintenance Reduction**: 80% less health monitoring code to maintain

### Improved Features
- **Consistent API**: Same health check format across all services
- **Enhanced Monitoring**: Better metrics, alerting, and diagnostics
- **Kubernetes Ready**: Built-in liveness/readiness probes
- **Performance**: Optimized health checking with async operations

### Developer Experience
- **Single Library**: One place to learn and maintain health monitoring
- **Easy Integration**: Simple factory function for any service
- **Comprehensive**: All monitoring needs in one place
- **Well Tested**: Centralized testing and validation

## Rollback Plan

If issues arise during migration:

1. **Keep Original Files**: Don't delete until migration is verified
2. **Feature Flags**: Use environment variables to switch between old/new
3. **Gradual Migration**: Migrate one service at a time
4. **Monitoring**: Watch health metrics during migration

## Support

For questions or issues with the unified health monitoring library:

- **Documentation**: See `shared/health_monitoring.py` docstrings
- **Examples**: See `shared/health_monitoring_example.py`
- **Testing**: Run the example to verify functionality
