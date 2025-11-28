"""
Prometheus metrics for Guard Services Orchestrator.

Provides comprehensive observability for orchestrator operations including
request rates, durations, circuit breaker states, and service health.
"""

from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, Optional
import time

# Orchestrator request metrics
ORCHESTRATOR_REQUESTS_TOTAL = Counter(
    'orchestrator_requests_total',
    'Total number of orchestrator requests',
    ['service_type', 'status']  # status: success, error, timeout
)

ORCHESTRATOR_REQUEST_DURATION_SECONDS = Histogram(
    'REPLACE_ME',
    'Orchestrator request duration in seconds',
    ['service_type'],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0)
)

# Circuit breaker metrics
CIRCUIT_BREAKER_STATE = Gauge(
    'circuit_breaker_state',
    'Circuit breaker state (0=CLOSED, 1=HALF_OPEN, 2=OPEN)',
    ['service_name']
)

CIRCUIT_BREAKER_FAILURE_COUNT = Gauge(
    'circuit_breaker_failure_count',
    'Current failure count for circuit breaker',
    ['service_name']
)

# Service health metrics
SERVICE_HEALTH_STATUS = Gauge(
    'service_health_status',
    'Service health status (0=unknown, 1=healthy, 2=degraded, 3=unhealthy)',
    ['service_name']
)

SERVICE_RESPONSE_TIME_SECONDS = Histogram(
    'service_response_time_seconds',
    'Service response time in seconds',
    ['service_name'],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

# Service availability metrics
SERVICE_AVAILABILITY = Gauge(
    'service_availability',
    'Service availability (1=available, 0=unavailable)',
    ['service_name']
)

# Payload size metrics
PAYLOAD_SIZE_BYTES = Histogram(
    'payload_size_bytes',
    'Request payload size in bytes',
    ['endpoint'],
    buckets=(1024, 10240, 102400, 1048576, 10485760)  # 1KB to 10MB
)

# Rate limiting metrics
RATE_LIMIT_HITS = Counter(
    'rate_limit_hits_total',
    'Total number of rate limit hits',
    ['endpoint', 'limit_type']  # limit_type: global, endpoint, user, ip
)

# Guardian Zero forensic analysis metrics
GUARDIAN_ZERO_REQUESTS_TOTAL = Counter(
    'guardian_zero_requests_total',
    'Total Guardian Zero forensic analysis requests',
    ['trigger_reason', 'status']  # status: success, error, unavailable
)

GUARDIAN_ZERO_ANALYSIS_DURATION_SECONDS = Histogram(
    'REPLACE_ME',
    'Guardian Zero analysis duration in seconds',
    buckets=(1.0, 5.0, 10.0, 30.0, 60.0)
)


def record_orchestrator_request(service_type: str, status: str, duration: float):
    """Record an orchestrator request."""
    ORCHESTRATOR_REQUESTS_TOTAL.labels(service_type=service_type, status=status).inc()
    ORCHESTRATOR_REQUEST_DURATION_SECONDS.labels(service_type=service_type).observe(duration)


def update_circuit_breaker_state(service_name: str, state: str, failure_count: int):
    """Update circuit breaker metrics."""
    state_value = {"CLOSED": 0, "HALF_OPEN": 1, "OPEN": 2}.get(state, 0)
    CIRCUIT_BREAKER_STATE.labels(service_name=service_name).set(state_value)
    CIRCUIT_BREAKER_FAILURE_COUNT.labels(service_name=service_name).set(failure_count)


def update_service_health(service_name: str, status: str, response_time: Optional[float]):
    """Update service health metrics."""
    status_value = {"unknown": 0, "healthy": 1, "degraded": 2, "unhealthy": 3}.get(status.lower(), 0)
    SERVICE_HEALTH_STATUS.labels(service_name=service_name).set(status_value)
    
    if response_time is not None:
        SERVICE_RESPONSE_TIME_SECONDS.labels(service_name=service_name).observe(response_time)


def update_service_availability(service_name: str, available: bool):
    """Update service availability metric."""
    SERVICE_AVAILABILITY.labels(service_name=service_name).set(1 if available else 0)


def record_payload_size(endpoint: str, size_bytes: int):
    """Record payload size."""
    PAYLOAD_SIZE_BYTES.labels(endpoint=endpoint).observe(size_bytes)


def record_rate_limit_hit(endpoint: str, limit_type: str):
    """Record a rate limit hit."""
    RATE_LIMIT_HITS.labels(endpoint=endpoint, limit_type=limit_type).inc()


def record_guardian_zero_request(trigger_reason: str, status: str, duration: Optional[float] = None):
    """Record Guardian Zero forensic analysis request."""
    GUARDIAN_ZERO_REQUESTS_TOTAL.labels(trigger_reason=trigger_reason, status=status).inc()
    if duration is not None:
        GUARDIAN_ZERO_ANALYSIS_DURATION_SECONDS.observe(duration)

