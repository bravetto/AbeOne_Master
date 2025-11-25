"""
Health Monitor - Comprehensive Health Monitoring System

Implements comprehensive health monitoring system for kernel and modules.

Pattern: HEALTH × MONITOR × CHECK × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import threading
import time
from .health_metrics import HealthMetricsCollector, ComponentHealth, HealthMetric, MetricType


class HealthStatus(Enum):
    """Health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Health check definition."""
    check_id: str
    component_id: str
    check_func: Callable[[], bool]
    interval: float = 60.0  # seconds
    timeout: float = 5.0  # seconds
    enabled: bool = True
    last_run: Optional[datetime] = None
    last_result: Optional[bool] = None


class HealthMonitor:
    """
    Health Monitor.
    
    Responsibilities:
    - Register health checks
    - Execute health checks
    - Aggregate health status
    - Provide health alerts
    """
    
    def __init__(self, metrics_collector: Optional[HealthMetricsCollector] = None):
        """Initialize health monitor."""
        self.metrics_collector = metrics_collector or HealthMetricsCollector()
        self.health_checks: Dict[str, HealthCheck] = {}
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active: bool = False
        self._lock = threading.Lock()
    
    def register_health_check(self, check: HealthCheck) -> bool:
        """
        Register a health check.
        
        Args:
            check: Health check definition
        
        Returns:
            True if registration successful
        """
        with self._lock:
            if check.check_id in self.health_checks:
                return False  # Already registered
            
            self.health_checks[check.check_id] = check
            return True
    
    def unregister_health_check(self, check_id: str) -> bool:
        """
        Unregister a health check.
        
        Args:
            check_id: Health check identifier
        
        Returns:
            True if unregistration successful
        """
        with self._lock:
            if check_id not in self.health_checks:
                return False
            
            del self.health_checks[check_id]
            return True
    
    def run_health_check(self, check_id: str) -> bool:
        """
        Run a specific health check.
        
        Args:
            check_id: Health check identifier
        
        Returns:
            True if health check passed
        """
        with self._lock:
            if check_id not in self.health_checks:
                return False
            
            check = self.health_checks[check_id]
        
        if not check.enabled:
            return True
        
        try:
            # Run check with timeout
            start_time = datetime.now()
            result = check.check_func()
            duration = (datetime.now() - start_time).total_seconds()
            
            check.last_run = datetime.now()
            check.last_result = result
            
            # Record metric
            metric = HealthMetric(
                metric_id=f"{check_id}_health_check",
                metric_type=MetricType.GAUGE,
                value=1.0 if result else 0.0,
                unit="status",
                tags={"check_id": check_id, "component_id": check.component_id}
            )
            self.metrics_collector.record_metric(check.component_id, metric)
            
            # Update component health
            status = HealthStatus.HEALTHY if result else HealthStatus.UNHEALTHY
            self.metrics_collector.update_component_health(
                check.component_id,
                status.value,
                {
                    "check_id": check_id,
                    "last_check": check.last_run.isoformat(),
                    "duration": duration
                }
            )
            
            return result
            
        except Exception as e:
            check.last_run = datetime.now()
            check.last_result = False
            
            # Record error metric
            metric = HealthMetric(
                metric_id=f"{check_id}_health_check_error",
                metric_type=MetricType.COUNTER,
                value=1.0,
                unit="errors",
                tags={"check_id": check_id, "component_id": check.component_id, "error": str(e)}
            )
            self.metrics_collector.record_metric(check.component_id, metric)
            
            # Update component health
            self.metrics_collector.update_component_health(
                check.component_id,
                HealthStatus.UNHEALTHY.value,
                {
                    "check_id": check_id,
                    "error": str(e),
                    "last_check": check.last_run.isoformat()
                }
            )
            
            return False
    
    def run_all_health_checks(self) -> Dict[str, bool]:
        """
        Run all health checks.
        
        Returns:
            Dictionary of check results
        """
        results: Dict[str, bool] = {}
        
        with self._lock:
            check_ids = list(self.health_checks.keys())
        
        for check_id in check_ids:
            results[check_id] = self.run_health_check(check_id)
        
        return results
    
    def start_monitoring(self, interval: float = 60.0) -> None:
        """
        Start health monitoring loop.
        
        Args:
            interval: Monitoring interval in seconds
        """
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        
        def monitoring_loop():
            while self.monitoring_active:
                self.run_all_health_checks()
                time.sleep(interval)
        
        self.monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self) -> None:
        """Stop health monitoring loop."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
    
    def get_component_health(self, component_id: str) -> Optional[ComponentHealth]:
        """
        Get component health.
        
        Args:
            component_id: Component identifier
        
        Returns:
            Component health or None
        """
        return self.metrics_collector.get_component_health(component_id)
    
    def get_all_health(self) -> Dict[str, ComponentHealth]:
        """
        Get all component health.
        
        Returns:
            Dictionary of component health
        """
        return self.metrics_collector.get_all_health()
    
    def get_health_summary(self) -> Dict[str, Any]:
        """
        Get health summary.
        
        Returns:
            Health summary dictionary
        """
        all_health = self.get_all_health()
        
        healthy_count = sum(1 for h in all_health.values() if h.status == "healthy")
        degraded_count = sum(1 for h in all_health.values() if h.status == "degraded")
        unhealthy_count = sum(1 for h in all_health.values() if h.status == "unhealthy")
        
        return {
            "total_components": len(all_health),
            "healthy": healthy_count,
            "degraded": degraded_count,
            "unhealthy": unhealthy_count,
            "components": all_health
        }

