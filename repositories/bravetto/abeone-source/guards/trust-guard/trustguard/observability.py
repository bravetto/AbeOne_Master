"""
Trust Guard Observability System

Implements enterprise-grade observability with:
- OpenTelemetry distributed tracing
- Structured logging with trace context
- Performance monitoring
- Error tracking and alerting
"""

import time
import logging
from typing import Dict, Any, Optional, List
from contextlib import contextmanager
from datetime import datetime, timezone

try:
    from opentelemetry import trace
    from opentelemetry import metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.sdk.resources import Resource
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    logging.warning("OpenTelemetry not available. Tracing will be disabled.")

logger = logging.getLogger(__name__)


class TraceContext:
    """Context manager for tracing operations."""
    
    def __init__(self, tracer_name: str, operation_name: str, attributes: Optional[Dict[str, Any]] = None):
        self.tracer_name = tracer_name
        self.operation_name = operation_name
        self.attributes = attributes or {}
        self.span = None
        self.start_time = None
    
    def __enter__(self):
        if OPENTELEMETRY_AVAILABLE:
            tracer = trace.get_tracer(self.tracer_name)
            self.span = tracer.start_span(self.operation_name)
            
            # Add attributes
            for key, value in self.attributes.items():
                self.span.set_attribute(key, value)
            
            # Add start time
            self.start_time = time.time()
            self.span.set_attribute("start_time", self.start_time)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span:
            # Add end time and duration
            end_time = time.time()
            duration = end_time - self.start_time if self.start_time else 0
            
            self.span.set_attribute("end_time", end_time)
            self.span.set_attribute("duration_ms", duration * 1000)
            
            # Add error information if exception occurred
            if exc_type:
                self.span.set_attribute("error", True)
                self.span.set_attribute("error.type", exc_type.__name__)
                if exc_val:
                    self.span.set_attribute("error.message", str(exc_val))
                self.span.record_exception(exc_val)
            
            self.span.end()


class PerformanceMetrics:
    """Performance metrics collection."""
    
    def __init__(self):
        self.metrics_data = {
            "request_count": 0,
            "request_duration": [],
            "error_count": 0,
            "pattern_detection_count": 0,
            "validation_count": 0,
            "mitigation_count": 0
        }
        self.start_time = time.time()
    
    def record_request(self, duration: float, success: bool = True):
        """Record a request metric."""
        self.metrics_data["request_count"] += 1
        self.metrics_data["request_duration"].append(duration)
        
        if not success:
            self.metrics_data["error_count"] += 1
    
    def record_pattern_detection(self, duration: float, patterns_detected: int):
        """Record pattern detection metrics."""
        self.metrics_data["pattern_detection_count"] += 1
    
    def record_validation(self, duration: float, risk_level: str):
        """Record validation metrics."""
        self.metrics_data["validation_count"] += 1
    
    def record_mitigation(self, duration: float, techniques_applied: int):
        """Record mitigation metrics."""
        self.metrics_data["mitigation_count"] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary."""
        durations = self.metrics_data["request_duration"]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "uptime_seconds": time.time() - self.start_time,
            "total_requests": self.metrics_data["request_count"],
            "error_count": self.metrics_data["error_count"],
            "error_rate": self.metrics_data["error_count"] / max(1, self.metrics_data["request_count"]),
            "avg_request_duration_ms": avg_duration * 1000,
            "pattern_detections": self.metrics_data["pattern_detection_count"],
            "validations": self.metrics_data["validation_count"],
            "mitigations": self.metrics_data["mitigation_count"]
        }


class ObservabilityManager:
    """Main observability manager."""
    
    def __init__(self, service_name: str = "trust-guard", service_version: str = "1.0.0"):
        self.service_name = service_name
        self.service_version = service_version
        self.performance_metrics = PerformanceMetrics()
        self.tracer = None
        self.meter = None
        
        if OPENTELEMETRY_AVAILABLE:
            self._setup_opentelemetry()
        else:
            logger.warning("OpenTelemetry not available. Using basic observability.")
    
    def _setup_opentelemetry(self):
        """Setup OpenTelemetry tracing and metrics."""
        try:
            # Create resource
            resource = Resource.create({
                "service.name": self.service_name,
                "service.version": self.service_version,
                "service.instance.id": f"{self.service_name}-{int(time.time())}"
            })
            
            # Setup tracing
            trace.set_tracer_provider(TracerProvider(resource=resource))
            self.tracer = trace.get_tracer(self.service_name, self.service_version)
            
            # Setup metrics
            metrics.set_meter_provider(MeterProvider(resource=resource))
            self.meter = metrics.get_meter(self.service_name, self.service_version)
            
            # Create custom metrics
            self.request_counter = self.meter.create_counter(
                name="trust_guard_requests_total",
                description="Total number of requests"
            )
            
            self.request_duration = self.meter.create_histogram(
                name="REPLACE_ME",
                description="Request duration in seconds"
            )
            
            self.error_counter = self.meter.create_counter(
                name="trust_guard_errors_total",
                description="Total number of errors"
            )
            
            self.pattern_detection_counter = self.meter.create_counter(
                name="REPLACE_ME",
                description="Total number of pattern detections"
            )
            
            logger.info("OpenTelemetry observability initialized")
            
        except Exception as e:
            logger.error(f"Failed to setup OpenTelemetry: {e}")
            OPENTELEMETRY_AVAILABLE = False
    
    def trace_operation(self, operation_name: str, attributes: Optional[Dict[str, Any]] = None):
        """Create a trace context for an operation."""
        return TraceContext(self.service_name, operation_name, attributes)
    
    def record_request(self, method: str, endpoint: str, duration: float, 
                      status_code: int, user_id: Optional[str] = None):
        """Record a request metric."""
        self.performance_metrics.record_request(duration, 200 <= status_code < 400)
        
        if self.meter:
            # Record OpenTelemetry metrics
            self.request_counter.add(1, {
                "method": method,
                "endpoint": endpoint,
                "status_code": str(status_code),
                "user_id": user_id or "anonymous"
            })
            
            self.request_duration.record(duration, {
                "method": method,
                "endpoint": endpoint
            })
            
            if status_code >= 400:
                self.error_counter.add(1, {
                    "method": method,
                    "endpoint": endpoint,
                    "status_code": str(status_code)
                })
    
    def record_pattern_detection(self, patterns_detected: int, duration: float, 
                               text_length: int, user_id: Optional[str] = None):
        """Record pattern detection metrics."""
        self.performance_metrics.record_pattern_detection(duration, patterns_detected)
        
        if self.meter:
            self.pattern_detection_counter.add(1, {
                "patterns_detected": str(patterns_detected),
                "text_length_range": self._get_text_length_range(text_length),
                "user_id": user_id or "anonymous"
            })
    
    def record_validation(self, risk_level: str, duration: float, 
                         overall_score: float, user_id: Optional[str] = None):
        """Record validation metrics."""
        self.performance_metrics.record_validation(duration, risk_level)
    
    def record_mitigation(self, techniques_applied: int, duration: float, 
                         patterns_mitigated: List[str], user_id: Optional[str] = None):
        """Record mitigation metrics."""
        self.performance_metrics.record_mitigation(duration, techniques_applied)
    
    def _get_text_length_range(self, text_length: int) -> str:
        """Get text length range for metrics."""
        if text_length < 100:
            return "short"
        elif text_length < 500:
            return "medium"
        elif text_length < 1000:
            return "long"
        else:
            return "very_long"
    
    def get_observability_summary(self) -> Dict[str, Any]:
        """Get comprehensive observability summary."""
        summary = {
            "service_info": {
                "name": self.service_name,
                "version": self.service_version,
                "tracing_enabled": OPENTELEMETRY_AVAILABLE,
                "metrics_enabled": self.meter is not None
            },
            "performance": self.performance_metrics.get_summary(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return summary
    
    def instrument_fastapi(self, app):
        """Instrument FastAPI application with OpenTelemetry."""
        if OPENTELEMETRY_AVAILABLE:
            try:
                FastAPIInstrumentor.instrument_app(app)
                RequestsInstrumentor().instrument()
                logger.info("FastAPI instrumented with OpenTelemetry")
            except Exception as e:
                logger.error(f"Failed to instrument FastAPI: {e}")


# Global observability manager instance
_observability_manager = None


def get_observability_manager() -> ObservabilityManager:
    """Get the global observability manager instance."""
    global _observability_manager
    if _observability_manager is None:
        _observability_manager = ObservabilityManager()
    return _observability_manager


def trace_operation(operation_name: str, attributes: Optional[Dict[str, Any]] = None):
    """Convenience function to create a trace context."""
    manager = get_observability_manager()
    return manager.trace_operation(operation_name, attributes)


def record_request(method: str, endpoint: str, duration: float, 
                  status_code: int, user_id: Optional[str] = None):
    """Convenience function to record request metrics."""
    manager = get_observability_manager()
    manager.record_request(method, endpoint, duration, status_code, user_id)


def record_pattern_detection(patterns_detected: int, duration: float, 
                           text_length: int, user_id: Optional[str] = None):
    """Convenience function to record pattern detection metrics."""
    manager = get_observability_manager()
    manager.record_pattern_detection(patterns_detected, duration, text_length, user_id)


def record_validation(risk_level: str, duration: float, 
                     overall_score: float, user_id: Optional[str] = None):
    """Convenience function to record validation metrics."""
    manager = get_observability_manager()
    manager.record_validation(risk_level, duration, overall_score, user_id)


def record_mitigation(techniques_applied: int, duration: float, 
                     patterns_mitigated: List[str], user_id: Optional[str] = None):
    """Convenience function to record mitigation metrics."""
    manager = get_observability_manager()
    manager.record_mitigation(techniques_applied, duration, patterns_mitigated, user_id)
