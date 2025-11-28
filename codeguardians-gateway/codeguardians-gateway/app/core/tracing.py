"""
Distributed Tracing Configuration

PRODUCTION HARDENING:
- OpenTelemetry integration
- Span correlation across services
- Request ID correlation
- Sampling configuration

SAFETY: Traces don't expose sensitive data
ASSUMES: OpenTelemetry collector available
VERIFY: Traces correlated with request IDs
"""

import os
from typing import Optional, Dict, Any
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from app.core.config import get_settings
from app.utils.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Global tracer
_tracer: Optional[trace.Tracer] = None
_tracer_provider: Optional[TracerProvider] = None


def initialize_tracing(
    service_name: str = "codeguardians-gateway",
    otlp_endpoint: Optional[str] = None,
    sampling_rate: float = 1.0
):
    """
    Initialize OpenTelemetry tracing.
    
    Args:
        service_name: Service name for traces
        otlp_endpoint: OTLP endpoint URL (defaults to env var)
        sampling_rate: Sampling rate (0.0 to 1.0)
    """
    global _tracer, _tracer_provider
    
    try:
        # Get OTLP endpoint from env or parameter
        if otlp_endpoint is None:
            otlp_endpoint = os.getenv(
                "OTEL_EXPORTER_OTLP_ENDPOINT",
                "http://localhost:4317"
            )
        
        # Create resource with service name
        resource = Resource.create({
            "service.name": service_name,
            "service.version": settings.APP_VERSION,
            "deployment.environment": settings.ENVIRONMENT
        })
        
        # Create tracer provider
        _tracer_provider = TracerProvider(resource=resource)
        
        # Configure sampling
        from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
        sampler = TraceIdRatioBased(sampling_rate)
        _tracer_provider.sampler = sampler
        
        # Create OTLP exporter
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        
        # Add span processor
        span_processor = BatchSpanProcessor(otlp_exporter)
        _tracer_provider.add_span_processor(span_processor)
        
        # Set global tracer provider
        trace.set_tracer_provider(_tracer_provider)
        
        # Get tracer
        _tracer = trace.get_tracer(__name__)
        
        # Instrument FastAPI
        FastAPIInstrumentor.instrument()
        
        # Instrument HTTP clients
        HTTPXClientInstrumentor().instrument()
        
        # Instrument Redis
        try:
            RedisInstrumentor().instrument()
        except Exception as e:
            logger.warning(f"Redis instrumentation failed: {e}")
        
        # Instrument SQLAlchemy
        try:
            SQLAlchemyInstrumentor().instrument()
        except Exception as e:
            logger.warning(f"SQLAlchemy instrumentation failed: {e}")
        
        logger.info(f"Tracing initialized: service={service_name}, endpoint={otlp_endpoint}")
        
    except Exception as e:
        logger.error(f"Failed to initialize tracing: {e}")
        logger.warning("Tracing disabled, continuing without distributed tracing")


def get_tracer() -> Optional[trace.Tracer]:
    """Get global tracer instance."""
    return _tracer


def get_current_span() -> Optional[trace.Span]:
    """Get current active span."""
    return trace.get_current_span()


def add_span_attribute(key: str, value: Any):
    """Add attribute to current span."""
    span = get_current_span()
    if span:
        span.set_attribute(key, value)


def set_span_request_id(request_id: str):
    """Set request ID as span attribute for correlation."""
    add_span_attribute("request_id", request_id)


def create_span(
    name: str,
    attributes: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> trace.Span:
    """
    Create a new span.
    
    Args:
        name: Span name
        attributes: Span attributes
        request_id: Request ID for correlation
    
    Returns:
        Span context manager
    """
    tracer = get_tracer()
    if not tracer:
        # Return no-op span if tracing not initialized
        from opentelemetry.trace import NoOpSpan
        return NoOpSpan()
    
    span = tracer.start_as_current_span(name)
    
    if attributes:
        for key, value in attributes.items():
            span.set_attribute(key, value)
    
    if request_id:
        span.set_attribute("request_id", request_id)
    
    return span


# Tracing initialization is handled in app lifespan
# This prevents early initialization before FastAPI app is created

