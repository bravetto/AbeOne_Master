"""
Monitoring and metrics module for PoisonGuard.
Provides comprehensive runtime statistics, health checks, and performance monitoring.
"""

import time
import psutil
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
from contextvars import ContextVar
import uuid

# Context variable for correlation IDs
correlation_id: ContextVar[str] = ContextVar('correlation_id', default='')

# Prometheus metrics - using a registry to avoid conflicts
from prometheus_client import CollectorRegistry, REGISTRY

# Create a custom registry to avoid conflicts
_metrics_registry = CollectorRegistry()

REQUEST_COUNT = Counter(
    'poisonguard_requests_total', 
    'Total number of requests', 
    ['method', 'endpoint', 'status_code'],
    registry=_metrics_registry
)

REQUEST_DURATION = Histogram(
    'poisonguard_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint'],
    registry=_metrics_registry
)

ANALYSIS_COUNT = Counter(
    'poisonguard_analysis_total',
    'Total number of analysis operations',
    ['result_type'],  # 'poisoned', 'clean'
    registry=_metrics_registry
)

MITIGATION_COUNT = Counter(
    'poisonguard_mitigation_total',
    'Total number of mitigation actions',
    ['action_type'],  # 'flag', 'sanitize', 'redact', 'none'
    registry=_metrics_registry
)

SYSTEM_MEMORY_USAGE = Gauge(
    'poisonguard_memory_usage_bytes',
    'Current memory usage in bytes',
    registry=_metrics_registry
)

SYSTEM_CPU_USAGE = Gauge(
    'poisonguard_cpu_usage_percent',
    'Current CPU usage percentage',
    registry=_metrics_registry
)

PLUGIN_EXECUTION_TIME = Histogram(
    'poisonguard_plugin_execution_seconds',
    'Plugin execution time in seconds',
    ['plugin_name'],
    registry=_metrics_registry
)

logger = logging.getLogger(__name__)


class SystemMetrics:
    """System metrics collector for runtime statistics."""
    
    def __init__(self):
        self.start_time = time.time()
        self.process = psutil.Process()
    
    def get_uptime(self) -> float:
        """Get application uptime in seconds."""
        return time.time() - self.start_time
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage statistics."""
        memory_info = self.process.memory_info()
        return {
            'rss': memory_info.rss,  # Resident Set Size
            'vms': memory_info.vms,  # Virtual Memory Size
            'percent': self.process.memory_percent(),
            'available': psutil.virtual_memory().available
        }
    
    def get_cpu_usage(self) -> Dict[str, Any]:
        """Get current CPU usage statistics."""
        return {
            'percent': self.process.cpu_percent(),
            'system_percent': psutil.cpu_percent(),
            'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information."""
        return {
            'uptime': self.get_uptime(),
            'memory': self.get_memory_usage(),
            'cpu': self.get_cpu_usage(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'pid': self.process.pid,
            'threads': self.process.num_threads()
        }


class HealthChecker:
    """Comprehensive health check system."""
    
    def __init__(self):
        self.metrics = SystemMetrics()
        self.health_status = "healthy"
        self.last_check = datetime.now(timezone.utc)
    
    def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        try:
            system_info = self.metrics.get_system_info()
            
            # Check memory usage
            memory_usage = system_info['memory']['percent']
            if memory_usage > 90:
                self.health_status = "degraded"
                logger.warning(f"High memory usage: {memory_usage}%")
            
            # Check CPU usage
            cpu_usage = system_info['cpu']['percent']
            if cpu_usage > 95:
                self.health_status = "degraded"
                logger.warning(f"High CPU usage: {cpu_usage}%")
            
            # Update metrics
            SYSTEM_MEMORY_USAGE.set(system_info['memory']['rss'])
            SYSTEM_CPU_USAGE.set(cpu_usage)
            
            return {
                "status": self.health_status,
                "timestamp": system_info['timestamp'],
                "uptime_seconds": system_info['uptime'],
                "memory_usage_percent": memory_usage,
                "cpu_usage_percent": cpu_usage,
                "threads": system_info['threads'],
                "pid": system_info['pid']
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            self.health_status = "unhealthy"
            return {
                "status": "unhealthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": str(e)
            }


def get_correlation_id() -> str:
    """Get current correlation ID or generate a new one."""
    current_id = correlation_id.get()
    if not current_id:
        current_id = str(uuid.uuid4())
        correlation_id.set(current_id)
    return current_id


def set_correlation_id(cid: str) -> None:
    """Set correlation ID for request tracking."""
    correlation_id.set(cid)


def get_metrics() -> Response:
    """Get Prometheus metrics endpoint."""
    return Response(generate_latest(_metrics_registry), media_type=CONTENT_TYPE_LATEST)


def record_request_metrics(method: str, endpoint: str, status_code: int, duration: float) -> None:
    """Record request metrics for monitoring."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=str(status_code)).inc()
    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)


def record_analysis_metrics(is_poisoned: bool) -> None:
    """Record analysis metrics."""
    result_type = "poisoned" if is_poisoned else "clean"
    ANALYSIS_COUNT.labels(result_type=result_type).inc()


def record_mitigation_metrics(action_type: str) -> None:
    """Record mitigation metrics."""
    MITIGATION_COUNT.labels(action_type=action_type).inc()


def record_plugin_metrics(plugin_name: str, execution_time: float) -> None:
    """Record plugin execution metrics."""
    PLUGIN_EXECUTION_TIME.labels(plugin_name=plugin_name).observe(execution_time)


# Global health checker instance
health_checker = HealthChecker()
