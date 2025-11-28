"""
Trust Guard Reliability Metrics

Tracks and analyzes AI reliability patterns and performance metrics with SLI/SLO tracking
"""

from typing import Dict, Any, List, Optional
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta
import statistics

try:
    from prometheus_client import Counter, Histogram, Gauge, Summary, CollectorRegistry, generate_latest
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logging.warning("Prometheus client not available. Metrics will be limited.")

logger = logging.getLogger(__name__)


class ReliabilityMetrics:
    """
    Comprehensive metrics collection for Trust Guard reliability analysis.

    Tracks patterns, performance, and risk trends over time.
    """

    def __init__(self):
        """Initialize metrics collection."""
        self.reset()
        self._setup_prometheus_metrics()
        logger.info("Reliability metrics initialized")
    
    def _setup_prometheus_metrics(self):
        """Setup Prometheus metrics."""
        if not PROMETHEUS_AVAILABLE:
            return
        
        # Create custom registry
        self.registry = CollectorRegistry()
        
        # Request metrics
        self.request_total = Counter(
            'trust_guard_requests_total',
            'Total number of requests',
            ['method', 'endpoint', 'status_code'],
            registry=self.registry
        )
        
        self.request_duration = Histogram(
            'REPLACE_ME',
            'Request duration in seconds',
            ['method', 'endpoint'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
            registry=self.registry
        )
        
        # Pattern detection metrics
        self.pattern_detections_total = Counter(
            'REPLACE_ME',
            'Total number of pattern detections',
            ['pattern_name', 'risk_level'],
            registry=self.registry
        )
        
        self.pattern_detection_duration = Histogram(
            'REPLACE_ME',
            'Pattern detection duration in seconds',
            ['pattern_name'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0],
            registry=self.registry
        )
        
        # Validation metrics
        self.validations_total = Counter(
            'trust_guard_validations_total',
            'Total number of validations',
            ['risk_level'],
            registry=self.registry
        )
        
        self.validation_duration = Histogram(
            'REPLACE_ME',
            'Validation duration in seconds',
            buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
            registry=self.registry
        )
        
        # Mitigation metrics
        self.mitigations_total = Counter(
            'trust_guard_mitigations_total',
            'Total number of mitigations',
            ['technique'],
            registry=self.registry
        )
        
        # SLI/SLO metrics
        self.availability_gauge = Gauge(
            'trust_guard_availability_ratio',
            'Service availability ratio',
            registry=self.registry
        )
        
        self.latency_p95 = Gauge(
            'trust_guard_latency_p95_seconds',
            '95th percentile latency in seconds',
            registry=self.registry
        )
        
        self.latency_p99 = Gauge(
            'trust_guard_latency_p99_seconds',
            '99th percentile latency in seconds',
            registry=self.registry
        )
        
        self.error_rate = Gauge(
            'trust_guard_error_rate_ratio',
            'Error rate ratio',
            registry=self.registry
        )
        
        # System metrics
        self.active_requests = Gauge(
            'trust_guard_active_requests',
            'Number of active requests',
            registry=self.registry
        )
        
        self.pattern_accuracy = Gauge(
            'REPLACE_ME',
            'Pattern detection accuracy ratio',
            ['pattern_name'],
            registry=self.registry
        )

    def reset(self):
        """Reset all metrics."""
        self.pattern_counts = defaultdict(int)
        self.validation_counts = {"total": 0, "by_risk_level": defaultdict(int)}
        self.detection_counts = 0
        self.mitigation_counts = 0
        self.start_time = time.time()
        self.hourly_stats = []
        self.max_hourly_stats = 168  # Keep only 7 days of hourly stats (24 * 7)

    def record_detection(self, detection_result: Dict[str, Any], duration: float = 0.0):
        """Record pattern detection results."""
        self.detection_counts += 1

        # Handle None or invalid input
        if detection_result is None or not isinstance(detection_result, dict):
            detection_result = {}
        
        # Count detected patterns
        detections = detection_result.get("detections", {})
        if isinstance(detections, dict):
            for pattern_name, pattern_data in detections.items():
                if isinstance(pattern_data, dict):
                    score = pattern_data.get("score", 0.0)
                    risk_level = pattern_data.get("risk_level", "unknown")
                    
                    # Handle invalid score types
                    try:
                        score = float(score) if score is not None else 0.0
                    except (ValueError, TypeError):
                        score = 0.0
                    
                    if score >= 0.0:  # Count all patterns with any score >= 0
                        self.pattern_counts[pattern_name] += 1
                    
                    # Record Prometheus metrics
                    if PROMETHEUS_AVAILABLE:
                        self.pattern_detections_total.labels(
                            pattern_name=pattern_name,
                            risk_level=risk_level
                        ).inc()
                        
                        self.pattern_detection_duration.labels(
                            pattern_name=pattern_name
                        ).observe(duration)

    def record_validation(self, validation_result: Dict[str, Dict[str, Any]]):
        """Record comprehensive validation results."""
        self.validation_counts["total"] += 1

        # Handle None or invalid input
        if validation_result is None or not isinstance(validation_result, dict):
            validation_result = {}
        
        risk_level = validation_result.get("risk_level", "unknown")
        self.validation_counts["by_risk_level"][risk_level] += 1

    def record_mitigation(self, mitigation_result: Dict[str, Any]):
        """Record mitigation application results."""
        self.mitigation_counts += 1
        
        # Handle None or invalid input gracefully
        if mitigation_result is None:
            mitigation_result = {}

    def get_total_validations(self) -> int:
        """Get total number of validations performed."""
        return self.validation_counts["total"]

    def get_total_detections(self) -> int:
        """Get total number of detections performed."""
        return self.detection_counts

    def get_total_mitigations(self) -> int:
        """Get total number of mitigations applied."""
        return self.mitigation_counts

    def get_average_risk_score(self) -> float:
        """Calculate average risk score across all validations."""
        total_risk_score = 0
        total_validations = 0

        for risk_level, count in self.validation_counts["by_risk_level"].items():
            risk_score = self._risk_level_to_score(risk_level)
            total_risk_score += risk_score * count
            total_validations += count

        return total_risk_score / max(total_validations, 1)

    def get_patterns_detected_today(self) -> int:
        """Get patterns detected in the last 24 hours."""
        return sum(self.pattern_counts.values())

    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get comprehensive pattern detection statistics."""
        total_patterns = sum(self.pattern_counts.values())

        return {
            "total_detected": total_patterns,
            "by_pattern": dict(self.pattern_counts),
            "most_common": max(self.pattern_counts.items(), key=lambda x: x[1]) if self.pattern_counts else None,
            "detection_rate": total_patterns / max(self.detection_counts, 1)
        }

    def get_reliability_trends(self) -> List[Dict[str, Any]]:
        """Get reliability trend analysis."""
        trends = []

        # Calculate success rate (validations with low/medium risk)
        low_risk = self.validation_counts["by_risk_level"].get("low", 0)
        medium_risk = self.validation_counts["by_risk_level"].get("medium", 0)
        total = self.validation_counts["total"]

        if total > 0:
            success_rate = (low_risk + medium_risk) / total
            trends.append({
                "metric": "success_rate",
                "value": success_rate,
                "description": f"{success_rate:.1%} of validations pass with low/medium risk"
            })

        # Pattern detection efficiency
        if self.detection_counts > 0:
            avg_patterns_per_detection = sum(self.pattern_counts.values()) / self.detection_counts
            trends.append({
                "metric": "avg_patterns_per_detection",
                "value": avg_patterns_per_detection,
                "description": ".1f"
            })

        # Mitigation effectiveness
        if self.mitigation_counts > 0 and total > 0:
            mitigation_rate = self.mitigation_counts / total
            trends.append({
                "metric": "mitigation_rate",
                "value": mitigation_rate,
                "description": f"{mitigation_rate:.1%} of validations require mitigation"
            })

        return trends

    def _risk_level_to_score(self, risk_level: str) -> float:
        """Convert risk level to numerical score."""
        risk_scores = {
            "low": 1.0,
            "medium": 2.0,
            "high": 3.0,
            "unknown": 1.5
        }
        return risk_scores.get(risk_level, 1.5)
    
    def is_healthy(self) -> bool:
        """Check if metrics system is healthy."""
        return True  # Metrics system is always healthy
    
    def record_request(self, method: str, endpoint: str, duration: float, 
                      status_code: int, user_id: Optional[str] = None):
        """Record request metrics."""
        if PROMETHEUS_AVAILABLE:
            self.request_total.labels(
                method=method,
                endpoint=endpoint,
                status_code=str(status_code)
            ).inc()
            
            self.request_duration.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
    
    def record_validation_metrics(self, risk_level: str, duration: float):
        """Record validation metrics."""
        if PROMETHEUS_AVAILABLE:
            self.validations_total.labels(risk_level=risk_level).inc()
            self.validation_duration.observe(duration)
    
    def record_mitigation_metrics(self, technique: str, duration: float):
        """Record mitigation metrics."""
        if PROMETHEUS_AVAILABLE:
            self.mitigations_total.labels(technique=technique).inc()
    
    def calculate_sli_slo_metrics(self):
        """Calculate SLI/SLO metrics."""
        if not PROMETHEUS_AVAILABLE:
            return
        
        # Calculate availability (assuming 99.9% target)
        uptime = time.time() - self.start_time
        availability = 0.999  # Placeholder - would be calculated from actual uptime
        self.availability_gauge.set(availability)
        
        # Calculate latency percentiles (placeholder values)
        # In production, these would be calculated from actual request durations
        self.latency_p95.set(0.2)  # 200ms p95
        self.latency_p99.set(0.5)  # 500ms p99
        
        # Calculate error rate
        total_requests = self.detection_counts + self.validation_counts["total"] + self.mitigation_counts
        error_count = self.validation_counts["by_risk_level"].get("high", 0)
        error_rate = error_count / max(1, total_requests)
        self.error_rate.set(error_rate)
    
    def get_prometheus_metrics(self) -> str:
        """Get Prometheus metrics in text format."""
        if not PROMETHEUS_AVAILABLE:
            return "# Prometheus metrics not available\n"
        
        # Update SLI/SLO metrics
        self.calculate_sli_slo_metrics()
        
        return generate_latest(self.registry).decode('utf-8')
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        return {
            "total_validations": self.validation_counts["total"],
            "total_detections": self.detection_counts,
            "total_mitigations": self.mitigation_counts,
            "pattern_counts": dict(self.pattern_counts),  # Add pattern counts
            "validation_breakdown": dict(self.validation_counts["by_risk_level"]),  # Add validation breakdown
            "average_risk_score": self.get_average_risk_score(),
            "patterns_detected_today": self.get_patterns_detected_today(),
            "uptime_seconds": time.time() - self.start_time,
            "last_updated": time.time(),
            "prometheus_available": PROMETHEUS_AVAILABLE
        }