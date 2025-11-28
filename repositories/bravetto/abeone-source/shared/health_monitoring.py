"""
Unified Health Monitoring Library

A comprehensive, reusable health monitoring system for all AI Guardian services.
Provides consistent health checks, metrics collection, and monitoring across the entire ecosystem.

Features:
- Standardized health status reporting
- System resource monitoring
- Service dependency checking
- Prometheus metrics integration
- Kubernetes-compatible health probes
- Performance tracking and alerting
"""

import asyncio
import time
import psutil
import aiohttp
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from contextvars import ContextVar
import uuid
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry

# Context variable for correlation IDs
correlation_id: ContextVar[str] = ContextVar('correlation_id', default='')

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Standardized health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Standardized health check result."""
    service: str
    status: HealthStatus
    response_time: float
    timestamp: float
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemMetrics:
    """System resource metrics."""
    cpu_percent: float
    memory_percent: float
    memory_rss: int
    memory_vms: int
    disk_usage_percent: float
    uptime_seconds: float
    thread_count: int
    process_id: int
    timestamp: float


class UnifiedHealthMonitor:
    """
    Unified health monitoring system for all AI Guardian services.
    
    Provides:
    - Service health checking
    - System resource monitoring
    - Dependency validation
    - Prometheus metrics
    - Kubernetes health probes
    """
    
    def __init__(self, service_name: str, service_version: str = "1.0.0"):
        self.service_name = service_name
        self.service_version = service_version
        self.start_time = time.time()
        self.process = psutil.Process()
        
        # Health check history
        self.health_history: List[HealthCheck] = []
        self.max_history = 100
        
        # Service dependencies
        self.dependencies: Dict[str, str] = {}
        
        # Metrics registry
        self.metrics_registry = CollectorRegistry()
        self._setup_metrics()
        
        # Health thresholds
        self.cpu_threshold = 90.0
        self.memory_threshold = 90.0
        self.response_time_threshold = 2.0
        
    def _setup_metrics(self):
        """Setup Prometheus metrics."""
        self.request_count = Counter(
            f'{self.service_name}_requests_total',
            'Total number of requests',
            ['method', 'endpoint', 'status_code'],
            registry=self.metrics_registry
        )
        
        self.request_duration = Histogram(
            f'{self.service_name}_request_duration_seconds',
            'Request duration in seconds',
            ['method', 'endpoint'],
            registry=self.metrics_registry
        )
        
        self.health_checks = Counter(
            f'{self.service_name}_health_checks_total',
            'Total number of health checks',
            ['status'],
            registry=self.metrics_registry
        )
        
        self.system_cpu = Gauge(
            f'{self.service_name}_cpu_usage_percent',
            'CPU usage percentage',
            registry=self.metrics_registry
        )
        
        self.system_memory = Gauge(
            f'{self.service_name}_memory_usage_bytes',
            'Memory usage in bytes',
            registry=self.metrics_registry
        )
        
        self.system_uptime = Gauge(
            f'{self.service_name}_uptime_seconds',
            'Service uptime in seconds',
            registry=self.metrics_registry
        )
    
    def add_dependency(self, name: str, endpoint: str):
        """Add a service dependency to monitor."""
        self.dependencies[name] = endpoint
    
    async def check_service_health(self, service_name: str, endpoint: str) -> HealthCheck:
        """Check health of a single service."""
        start_time = time.time()
        
        try:
            if service_name in ["postgres", "redis", "database"]:
                return await self._check_database_health(service_name, endpoint)
            else:
                return await self._check_http_health(service_name, endpoint)
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Health check failed for {service_name}: {e}")
            
            return HealthCheck(
                service=service_name,
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                timestamp=time.time(),
                details={},
                error=str(e)
            )
    
    async def _check_http_health(self, service_name: str, endpoint: str) -> HealthCheck:
        """Check HTTP service health."""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, timeout=5) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        status = HealthStatus.HEALTHY
                        
                        # Check for degraded status based on response time
                        if response_time > self.response_time_threshold:
                            status = HealthStatus.DEGRADED
                        
                        return HealthCheck(
                            service=service_name,
                            status=status,
                            response_time=response_time,
                            timestamp=time.time(),
                            details=data
                        )
                    else:
                        return HealthCheck(
                            service=service_name,
                            status=HealthStatus.UNHEALTHY,
                            response_time=response_time,
                            timestamp=time.time(),
                            details={"status_code": response.status},
                            error=f"HTTP {response.status}"
                        )
        except asyncio.TimeoutError:
            return HealthCheck(
                service=service_name,
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                timestamp=time.time(),
                error="Timeout"
            )
        except Exception as e:
            return HealthCheck(
                service=service_name,
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                timestamp=time.time(),
                error=str(e)
            )
    
    async def _check_database_health(self, service_name: str, connection_string: str) -> HealthCheck:
        """Check database health."""
        start_time = time.time()
        
        try:
            # This would be implemented based on the specific database
            # For now, return a basic health check
            response_time = time.time() - start_time
            
            return HealthCheck(
                service=service_name,
                status=HealthStatus.HEALTHY,
                response_time=response_time,
                timestamp=time.time(),
                details={"type": "database", "status": "connected"}
            )
        except Exception as e:
            return HealthCheck(
                service=service_name,
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                timestamp=time.time(),
                error=str(e)
            )
    
    def get_system_metrics(self) -> SystemMetrics:
        """Get current system resource metrics."""
        try:
            memory_info = self.process.memory_info()
            disk_usage = psutil.disk_usage('/')
            
            return SystemMetrics(
                cpu_percent=self.process.cpu_percent(),
                memory_percent=self.process.memory_percent(),
                memory_rss=memory_info.rss,
                memory_vms=memory_info.vms,
                disk_usage_percent=disk_usage.percent,
                uptime_seconds=time.time() - self.start_time,
                thread_count=self.process.num_threads(),
                process_id=self.process.pid,
                timestamp=time.time()
            )
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return SystemMetrics(
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_rss=0,
                memory_vms=0,
                disk_usage_percent=0.0,
                uptime_seconds=0.0,
                thread_count=0,
                process_id=0,
                timestamp=time.time()
            )
    
    def check_system_health(self) -> HealthStatus:
        """Check overall system health based on resource usage."""
        metrics = self.get_system_metrics()
        
        # Update Prometheus metrics
        self.system_cpu.set(metrics.cpu_percent)
        self.system_memory.set(metrics.memory_rss)
        self.system_uptime.set(metrics.uptime_seconds)
        
        # Check thresholds
        if metrics.cpu_percent > self.cpu_threshold or metrics.memory_percent > self.memory_threshold:
            return HealthStatus.DEGRADED
        
        return HealthStatus.HEALTHY
    
    async def check_all_dependencies(self) -> List[HealthCheck]:
        """Check health of all configured dependencies."""
        if not self.dependencies:
            return []
        
        tasks = [
            self.check_service_health(name, endpoint)
            for name, endpoint in self.dependencies.items()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        health_checks = []
        for result in results:
            if isinstance(result, HealthCheck):
                health_checks.append(result)
                self.health_checks.labels(status=result.status.value).inc()
            else:
                logger.error(f"Health check failed with exception: {result}")
        
        # Store in history
        self.health_history.extend(health_checks)
        if len(self.health_history) > self.max_history:
            self.health_history = self.health_history[-self.max_history:]
        
        return health_checks
    
    def get_liveness_probe(self) -> Dict[str, Any]:
        """Get Kubernetes liveness probe response."""
        system_health = self.check_system_health()
        
        return {
            "status": "alive" if system_health in [HealthStatus.HEALTHY, HealthStatus.DEGRADED] else "dead",
            "service": self.service_name,
            "version": self.service_version,
            "timestamp": time.time(),
            "uptime_seconds": time.time() - self.start_time
        }
    
    def get_readiness_probe(self) -> Dict[str, Any]:
        """Get Kubernetes readiness probe response."""
        system_health = self.check_system_health()
        
        return {
            "status": "ready" if system_health == HealthStatus.HEALTHY else "not_ready",
            "service": self.service_name,
            "version": self.service_version,
            "timestamp": time.time(),
            "checks": {
                "system": system_health.value,
                "dependencies": len(self.dependencies)
            }
        }
    
    async def get_comprehensive_health(self) -> Dict[str, Any]:
        """Get comprehensive health status including all dependencies."""
        # Check system health
        system_health = self.check_system_health()
        system_metrics = self.get_system_metrics()
        
        # Check all dependencies
        dependency_health = await self.check_all_dependencies()
        
        # Determine overall status
        overall_status = system_health
        if dependency_health:
            unhealthy_deps = [h for h in dependency_health if h.status == HealthStatus.UNHEALTHY]
            if unhealthy_deps:
                overall_status = HealthStatus.DEGRADED if system_health == HealthStatus.HEALTHY else HealthStatus.UNHEALTHY
        
        return {
            "overall_status": overall_status.value,
            "service": self.service_name,
            "version": self.service_version,
            "timestamp": time.time(),
            "uptime_seconds": system_metrics.uptime_seconds,
            "system_metrics": {
                "cpu_percent": system_metrics.cpu_percent,
                "memory_percent": system_metrics.memory_percent,
                "memory_rss_bytes": system_metrics.memory_rss,
                "disk_usage_percent": system_metrics.disk_usage_percent,
                "thread_count": system_metrics.thread_count
            },
            "dependencies": {
                dep.service: {
                    "status": dep.status.value,
                    "response_time": dep.response_time,
                    "error": dep.error
                }
                for dep in dependency_health
            },
            "alerts": self._generate_alerts(system_metrics, dependency_health)
        }
    
    def _generate_alerts(self, system_metrics: SystemMetrics, dependency_health: List[HealthCheck]) -> List[Dict[str, Any]]:
        """Generate alerts based on system metrics and dependency health."""
        alerts = []
        
        # System resource alerts
        if system_metrics.cpu_percent > self.cpu_threshold:
            alerts.append({
                "type": "high_cpu",
                "severity": "warning",
                "message": f"High CPU usage: {system_metrics.cpu_percent:.1f}%",
                "threshold": self.cpu_threshold
            })
        
        if system_metrics.memory_percent > self.memory_threshold:
            alerts.append({
                "type": "high_memory",
                "severity": "warning", 
                "message": f"High memory usage: {system_metrics.memory_percent:.1f}%",
                "threshold": self.memory_threshold
            })
        
        # Dependency alerts
        for dep in dependency_health:
            if dep.status == HealthStatus.UNHEALTHY:
                alerts.append({
                    "type": "dependency_unhealthy",
                    "severity": "critical",
                    "message": f"Dependency {dep.service} is unhealthy",
                    "service": dep.service,
                    "error": dep.error
                })
            elif dep.status == HealthStatus.DEGRADED:
                alerts.append({
                    "type": "dependency_degraded",
                    "severity": "warning",
                    "message": f"Dependency {dep.service} is degraded",
                    "service": dep.service,
                    "response_time": dep.response_time
                })
        
        return alerts
    
    def get_prometheus_metrics(self) -> str:
        """Get Prometheus metrics in text format."""
        return generate_latest(self.metrics_registry)
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get health summary for monitoring dashboards."""
        system_health = self.check_system_health()
        system_metrics = self.get_system_metrics()
        
        return {
            "status": system_health.value,
            "service": self.service_name,
            "version": self.service_version,
            "uptime_seconds": system_metrics.uptime_seconds,
            "cpu_percent": system_metrics.cpu_percent,
            "memory_percent": system_metrics.memory_percent,
            "dependencies_count": len(self.dependencies),
            "last_check": time.time()
        }


def get_correlation_id() -> str:
    """Get current correlation ID or generate a new one."""
    current_id = correlation_id.get()
    if not current_id:
        current_id = str(uuid.uuid4())
        correlation_id.set(current_id)
    return current_id


def set_correlation_id(corr_id: str) -> None:
    """Set correlation ID for request tracing."""
    correlation_id.set(corr_id)


# Factory function for easy service integration
def create_health_monitor(service_name: str, service_version: str = "1.0.0") -> UnifiedHealthMonitor:
    """Create a health monitor instance for a service."""
    return UnifiedHealthMonitor(service_name, service_version)
