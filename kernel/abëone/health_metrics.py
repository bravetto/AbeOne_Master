"""
Health Metrics - Health Metrics Collection

Implements health metrics collection for kernel and modules.

Pattern: HEALTH × METRICS × COLLECTION × ONE
Philosophy: 80/20 → 97.8% Certainty
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MetricType(Enum):
    """Metric types."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class HealthMetric:
    """Health metric definition."""
    metric_id: str
    metric_type: MetricType
    value: float
    unit: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class ComponentHealth:
    """Component health information."""
    component_id: str
    status: str  # "healthy", "degraded", "unhealthy"
    metrics: List[HealthMetric] = field(default_factory=list)
    last_check: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)


class HealthMetricsCollector:
    """
    Health Metrics Collector.
    
    Responsibilities:
    - Collect health metrics
    - Store health metrics
    - Provide health metrics queries
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self.metrics: Dict[str, List[HealthMetric]] = {}
        self.component_health: Dict[str, ComponentHealth] = {}
        self.max_metrics_per_component: int = 1000
    
    def record_metric(self, component_id: str, metric: HealthMetric) -> None:
        """
        Record a health metric.
        
        Args:
            component_id: Component identifier
            metric: Health metric
        """
        if component_id not in self.metrics:
            self.metrics[component_id] = []
        
        self.metrics[component_id].append(metric)
        
        # Trim metrics if too many
        if len(self.metrics[component_id]) > self.max_metrics_per_component:
            self.metrics[component_id].pop(0)
    
    def update_component_health(self, component_id: str, status: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Update component health status.
        
        Args:
            component_id: Component identifier
            status: Health status
            details: Optional details
        """
        if component_id not in self.component_health:
            self.component_health[component_id] = ComponentHealth(
                component_id=component_id,
                status=status
            )
        
        health = self.component_health[component_id]
        health.status = status
        health.last_check = datetime.now()
        if details:
            health.details.update(details)
        
        # Update metrics
        if component_id in self.metrics:
            health.metrics = self.metrics[component_id][-100:]  # Last 100 metrics
    
    def get_component_health(self, component_id: str) -> Optional[ComponentHealth]:
        """
        Get component health.
        
        Args:
            component_id: Component identifier
        
        Returns:
            Component health or None
        """
        return self.component_health.get(component_id)
    
    def get_all_health(self) -> Dict[str, ComponentHealth]:
        """
        Get all component health.
        
        Returns:
            Dictionary of component health
        """
        return self.component_health.copy()
    
    def get_metrics(self, component_id: str, limit: int = 100) -> List[HealthMetric]:
        """
        Get metrics for a component.
        
        Args:
            component_id: Component identifier
            limit: Maximum number of metrics to return
        
        Returns:
            List of health metrics
        """
        if component_id not in self.metrics:
            return []
        
        return self.metrics[component_id][-limit:]
    
    def clear_metrics(self, component_id: Optional[str] = None) -> None:
        """
        Clear metrics.
        
        Args:
            component_id: Component identifier (None to clear all)
        """
        if component_id:
            if component_id in self.metrics:
                self.metrics[component_id].clear()
        else:
            self.metrics.clear()

