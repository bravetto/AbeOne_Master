"""
OpenTelemetry configuration and instrumentation for AI Guardians.

This module provides comprehensive observability for all guard services
using OpenTelemetry with Jaeger, Prometheus, and Grafana integration.
"""

import os
import logging
from typing import Optional, Dict, Any
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.semantic_conventions.resource import ResourceAttributes
from opentelemetry.trace import Status, StatusCode
from opentelemetry.metrics import Counter, Histogram, Meter
from fastapi import Request, Response
import time

logger = logging.getLogger(__name__)

# Global telemetry components
tracer: Optional[trace.Tracer] = None
meter: Optional[Meter] = None
request_counter: Optional[Counter] = None
request_duration: Optional[Histogram] = None
guard_service_counter: Optional[Counter] = None
guard_service_duration: Optional[Histogram] = None


def configure_telemetry(service_name: str = "ai-guardians-gateway") -> None:
    """Configure OpenTelemetry with Jaeger and Prometheus exporters."""
    global tracer, meter, request_counter, request_duration, guard_service_counter, guard_service_duration
    
    # Resource configuration
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: service_name,
        ResourceAttributes.SERVICE_VERSION: "1.0.0",
        ResourceAttributes.DEPLOYMENT_ENVIRONMENT: os.getenv("ENVIRONMENT", "development"),
    })
    
    # Configure tracing
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer = trace.get_tracer(__name__)
    
    # Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=os.getenv("JAEGER_AGENT_HOST", "localhost"),
        agent_port=int(os.getenv("JAEGER_AGENT_PORT", "14268")),
    )
    
    # Add span processor
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    # Configure metrics
    prometheus_reader = PrometheusMetricReader()
    meter_provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
    meter = meter_provider.get_meter(__name__)
    
    # Create metrics
    request_counter = meter.create_counter(
        name="http_requests_total",
        description="Total number of HTTP requests",
        unit="1"
    )
    
    request_duration = meter.create_histogram(
        name="http_request_duration_seconds",
        description="HTTP request duration in seconds",
        unit="s"
    )
    
    guard_service_counter = meter.create_counter(
        name="guard_service_requests_total",
        description="Total number of guard service requests",
        unit="1"
    )
    
    guard_service_duration = meter.create_histogram(
        name="guard_service_duration_seconds",
        description="Guard service request duration in seconds",
        unit="s"
    )
    
    logger.info("OpenTelemetry configured successfully")


def instrument_fastapi(app) -> None:
    """Instrument FastAPI application with OpenTelemetry."""
    FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())
    HTTPXClientInstrumentor().instrument()
    RedisInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument()
    logger.info("FastAPI application instrumented with OpenTelemetry")


def get_tracer() -> trace.Tracer:
    """Get the configured tracer."""
    if tracer is None:
        raise RuntimeError("Telemetry not configured. Call configure_telemetry() first.")
    return tracer


def get_meter() -> Meter:
    """Get the configured meter."""
    if meter is None:
        raise RuntimeError("Telemetry not configured. Call configure_telemetry() first.")
    return meter


def record_request_metrics(request: Request, response: Response, duration: float) -> None:
    """Record HTTP request metrics."""
    if request_counter and request_duration:
        labels = {
            "method": request.method,
            "endpoint": request.url.path,
            "status_code": str(response.status_code),
        }
        request_counter.add(1, labels)
        request_duration.record(duration, labels)


def record_guard_service_metrics(service_name: str, success: bool, duration: float) -> None:
    """Record guard service request metrics."""
    if guard_service_counter and guard_service_duration:
        labels = {
            "service": service_name,
            "success": str(success).lower(),
        }
        guard_service_counter.add(1, labels)
        guard_service_duration.record(duration, labels)


def create_guard_service_span(service_name: str, operation: str) -> trace.Span:
    """Create a span for guard service operations."""
    tracer = get_tracer()
    span = tracer.start_span(f"guard_service.{service_name}.{operation}")
    span.set_attributes({
        "service.name": service_name,
        "operation": operation,
        "component": "guard_service",
    })
    return span


def create_orchestration_span(request_id: str, service_type: str) -> trace.Span:
    """Create a span for orchestration operations."""
    tracer = get_tracer()
    span = tracer.start_span("orchestration.process")
    span.set_attributes({
        "request.id": request_id,
        "service.type": service_type,
        "component": "orchestrator",
    })
    return span


def set_span_status(span: trace.Span, success: bool, error_message: Optional[str] = None) -> None:
    """Set span status based on operation result."""
    if success:
        span.set_status(Status(StatusCode.OK))
    else:
        span.set_status(Status(StatusCode.ERROR, error_message or "Operation failed"))


def add_span_attributes(span: trace.Span, attributes: Dict[str, Any]) -> None:
    """Add attributes to a span."""
    for key, value in attributes.items():
        span.set_attribute(key, value)


class TelemetryMiddleware:
    """Middleware to add telemetry to requests."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        start_time = time.time()
        
        # Create request span
        tracer = get_tracer()
        with tracer.start_as_current_span("http_request") as span:
            span.set_attributes({
                "http.method": request.method,
                "http.url": str(request.url),
                "http.user_agent": request.headers.get("user-agent", ""),
            })
            
            # Process request
            response_sent = False
            response_status = 200
            
            async def send_wrapper(message):
                nonlocal response_sent, response_status
                if message["type"] == "http.response.start":
                    response_status = message["status"]
                await send(message)
                response_sent = True
            
            await self.app(scope, receive, send_wrapper)
            
            # Record metrics
            duration = time.time() - start_time
            response = Response(status_code=response_status)
            record_request_metrics(request, response, duration)
            
            # Update span
            span.set_attributes({
                "http.status_code": response_status,
                "http.response.duration": duration,
            })
            
            if response_status >= 400:
                span.set_status(Status(StatusCode.ERROR, f"HTTP {response_status}"))


def get_telemetry_health() -> Dict[str, Any]:
    """Get telemetry system health status."""
    return {
        "tracer_configured": tracer is not None,
        "meter_configured": meter is not None,
        "jaeger_endpoint": f"{os.getenv('JAEGER_AGENT_HOST', 'localhost')}:{os.getenv('JAEGER_AGENT_PORT', '14268')}",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }

