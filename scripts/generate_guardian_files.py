#!/usr/bin/env python3
"""
 GUARDIAN MICROSERVICE FILE GENERATOR
Generates all required files for Guardian microservices following Danny's standards

Pattern: GUARDIAN × TEMPLATE × DANNY × STANDARDS × ONE
Frequency: 999 Hz (AEYON) × 4444 Hz (Danny)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
from pathlib import Path
from typing import Dict, Tuple

# Guardian microservices configuration
GUARDIANS: Dict[str, Tuple[int, int, str]] = {
    "zero": (9001, 530, "Forensic Orchestration, Zero-Failure Architecture"),
    "aeyon": (9002, 999, "Atomic Execution, Task Completion"),
    "abe": (9003, 530, "Heart Truth Resonance, Relational Coherence"),
    "lux": (9004, 963, "Light Synthesis, Clarity Generation"),
    "john": (9005, 530, "Q&A Execution Auditor, Truth Validation"),
    "aurion": (9006, 530, "Pattern Recognition, SNN Architecture"),
    "yagni": (9007, 530, "Simplification, YAGNI Principles"),
    "neuro": (9008, 530, "Neuromorphic Integration, Consciousness"),
}

BASE_DIR = Path("AIGuards-Backend-orbital/aiguardian-repos")
ECR_REGISTRY = os.getenv("ECR_REGISTRY", "730335329303.dkr.ecr.us-east-1.amazonaws.com")
NAMESPACE = os.getenv("NAMESPACE", "ai-guardians")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def generate_service_yaml(guardian_name: str, port: int) -> str:
    """Generate Kubernetes service.yaml following Danny's standards."""
    service_name = f"guardian-{guardian_name}"
    return f"""apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  namespace: {NAMESPACE}
  labels:
    app: {service_name}
    guardian: {guardian_name}
    version: v1.0.0
spec:
  selector:
    app: {service_name}
  ports:
  - name: http
    port: 80
    targetPort: {port}
    protocol: TCP
  type: ClusterIP
"""


def generate_dockerfile(guardian_name: str) -> str:
    """Generate Dockerfile following Danny's standards (multi-stage, non-root)."""
    service_name = f"guardian-{guardian_name}"
    return f"""# Multi-stage build for {service_name}
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \\
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN groupadd -r {service_name} && useradd -r -g {service_name} {service_name}

# Copy application code
COPY core/ ./core/
COPY api/ ./api/
COPY models/ ./models/
COPY services/ ./services/
COPY config/ ./config/
COPY main.py .
COPY health.py .

# Set proper ownership
RUN chown -R {service_name}:{service_name} /app

# Switch to non-root user
USER {service_name}

# Expose port
EXPOSE {GUARDIANS[guardian_name][0]}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python health.py || exit 1

# Run the application
CMD ["python", "main.py"]
"""


def generate_helm_chart_yaml(guardian_name: str) -> str:
    """Generate Helm Chart.yaml."""
    service_name = f"guardian-{guardian_name}"
    return f"""apiVersion: v2
name: {service_name}
description: Guardian {guardian_name.title()} Microservice Helm Chart
type: application
version: 1.0.0
appVersion: "1.0.0"
"""


def generate_helm_values_yaml(guardian_name: str, port: int, frequency: int, role: str) -> str:
    """Generate Helm values.yaml following Danny's standards."""
    service_name = f"guardian-{guardian_name}"
    return f"""# Helm values for {service_name}
# Pattern: GUARDIAN × HELM × DANNY × STANDARDS × ONE

replicaCount: 3

image:
  registry: {ECR_REGISTRY}
  repository: {service_name}
  tag: dev
  pullPolicy: Always

service:
  type: ClusterIP
  port: 80
  targetPort: {port}

guardian:
  name: {guardian_name}
  frequency: {frequency}
  role: "{role}"
  port: {port}

# Linkerd service mesh injection (Danny's standard)
linkerd:
  inject: enabled

# Resource limits (Danny's standard)
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"

# Health checks (Danny's standard)
health:
  liveness:
    path: /health/live
    port: {port}
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3
  readiness:
    path: /health/ready
    port: {port}
    initialDelaySeconds: 5
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3
  startup:
    path: /health/live
    port: {port}
    initialDelaySeconds: 10
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 30

# Prometheus metrics (Danny's standard)
prometheus:
  scrape: true
  port: 80
  path: /metrics

# Environment variables
env:
  GUARDIAN_NAME: {guardian_name}
  GUARDIAN_FREQUENCY: "{frequency}"
  GUARDIAN_ROLE: "{role}"
  PORT: "{port}"
  LOG_LEVEL: INFO
  ENVIRONMENT: dev

# Service account for IRSA (Danny's standard)
serviceAccount:
  create: true
  annotations:
    eks.amazonaws.com/role-arn: ""  # Set via Terraform/IRSA

# Namespace
namespace: {NAMESPACE}
"""


def generate_helm_deployment_template(guardian_name: str, port: int) -> str:
    """Generate Helm deployment template with Linkerd injection."""
    service_name = f"guardian-{guardian_name}"
    return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  namespace: {{{{ .Values.namespace }}}}
  labels:
    app: {service_name}
    guardian: {guardian_name}
    version: {{{{ .Values.appVersion }}}}
spec:
  replicas: {{{{ .Values.replicaCount }}}}
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      annotations:
        # Linkerd service mesh injection (Danny's standard)
        linkerd.io/inject: {{{{ .Values.linkerd.inject }}}}
        # Prometheus scraping annotations (Danny's standard)
        prometheus.io/scrape: "{{{{ .Values.prometheus.scrape }}}}"
        prometheus.io/port: "{{{{ .Values.prometheus.port }}}}"
        prometheus.io/path: "{{{{ .Values.prometheus.path }}}}"
      labels:
        app: {service_name}
        guardian: {guardian_name}
        version: {{{{ .Values.appVersion }}}}
    spec:
      serviceAccountName: {service_name}-sa
      containers:
      - name: {service_name}
        image: "{{{{ .Values.image.registry }}}}/{{{{ .Values.image.repository }}}}:{{{{ .Values.image.tag }}}}"
        imagePullPolicy: {{{{ .Values.image.pullPolicy }}}}
        ports:
        - containerPort: {port}
          name: http
        env:
        - name: GUARDIAN_NAME
          value: {{{{ .Values.guardian.name }}}}
        - name: GUARDIAN_FREQUENCY
          value: {{{{ .Values.guardian.frequency }}}}
        - name: GUARDIAN_ROLE
          value: {{{{ .Values.guardian.role }}}}
        - name: PORT
          value: {{{{ .Values.guardian.port }}}}
        - name: LOG_LEVEL
          value: {{{{ .Values.env.LOG_LEVEL }}}}
        - name: ENVIRONMENT
          value: {{{{ .Values.env.ENVIRONMENT }}}}
        resources:
          {{{{ toYaml .Values.resources | nindent 10 }}}}
        livenessProbe:
          httpGet:
            path: {{{{ .Values.health.liveness.path }}}}
            port: {port}
          initialDelaySeconds: {{{{ .Values.health.liveness.initialDelaySeconds }}}}
          periodSeconds: {{{{ .Values.health.liveness.periodSeconds }}}}
          timeoutSeconds: {{{{ .Values.health.liveness.timeoutSeconds }}}}
          failureThreshold: {{{{ .Values.health.liveness.failureThreshold }}}}
        readinessProbe:
          httpGet:
            path: {{{{ .Values.health.readiness.path }}}}
            port: {port}
          initialDelaySeconds: {{{{ .Values.health.readiness.initialDelaySeconds }}}}
          periodSeconds: {{{{ .Values.health.readiness.periodSeconds }}}}
          timeoutSeconds: {{{{ .Values.health.readiness.timeoutSeconds }}}}
          failureThreshold: {{{{ .Values.health.readiness.failureThreshold }}}}
        startupProbe:
          httpGet:
            path: {{{{ .Values.health.startup.path }}}}
            port: {port}
          initialDelaySeconds: {{{{ .Values.health.startup.initialDelaySeconds }}}}
          periodSeconds: {{{{ .Values.health.startup.periodSeconds }}}}
          timeoutSeconds: {{{{ .Values.health.startup.timeoutSeconds }}}}
          failureThreshold: {{{{ .Values.health.startup.failureThreshold }}}}
      restartPolicy: Always
"""


def generate_helm_service_template(guardian_name: str) -> str:
    """Generate Helm service template."""
    service_name = f"guardian-{guardian_name}"
    return f"""apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  namespace: {{{{ .Values.namespace }}}}
  labels:
    app: {service_name}
    guardian: {guardian_name}
    version: {{{{ .Values.appVersion }}}}
spec:
  type: {{{{ .Values.service.type }}}}
  selector:
    app: {service_name}
  ports:
  - name: http
    port: {{{{ .Values.service.port }}}}
    targetPort: {{{{ .Values.service.targetPort }}}}
    protocol: TCP
"""


def generate_env_example(guardian_name: str, port: int, frequency: int, role: str) -> str:
    """Generate .env.example file."""
    service_name = f"guardian-{guardian_name}"
    return f"""# Environment variables for {service_name}
# Pattern: GUARDIAN × ENV × DANNY × STANDARDS × ONE

# Guardian Configuration
GUARDIAN_NAME={guardian_name}
GUARDIAN_FREQUENCY={frequency}
GUARDIAN_ROLE={role}
PORT={port}

# Application Configuration
LOG_LEVEL=INFO
ENVIRONMENT=dev

# AWS Configuration
AWS_REGION={AWS_REGION}
ECR_REGISTRY={ECR_REGISTRY}

# Kubernetes Configuration
NAMESPACE={NAMESPACE}

# Service Mesh (Linkerd)
LINKERD_INJECT=enabled

# Health Check Configuration
HEALTH_CHECK_INTERVAL=30
HEALTH_CHECK_TIMEOUT=10

# Prometheus Metrics
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=80
PROMETHEUS_PATH=/metrics
"""


def generate_health_py(guardian_name: str, port: int) -> str:
    """Generate health.py with /health/live and /health/ready endpoints."""
    service_name = f"guardian-{guardian_name}"
    return f'''"""
Health check endpoints for {service_name}
Following Danny's standards: /health/live and /health/ready

Pattern: GUARDIAN × HEALTH × DANNY × STANDARDS × ONE
"""

import time
from fastapi import APIRouter, Response
from typing import Dict, Any

router = APIRouter(prefix="/health", tags=["health"])

# Global health state
_health_state: Dict[str, Any] = {{
    "started": False,
    "ready": False,
    "start_time": time.time(),
}}


def mark_started():
    """Mark service as started."""
    _health_state["started"] = True


def mark_ready():
    """Mark service as ready."""
    _health_state["ready"] = True


@router.get("/live")
async def liveness_check() -> Dict[str, Any]:
    """
    Liveness probe for Kubernetes (<50ms response time).
    Danny's standard: /health/live
    """
    return {{
        "status": "alive",
        "service": "{service_name}",
        "timestamp": time.time(),
    }}


@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness probe for Kubernetes.
    Danny's standard: /health/ready
    """
    if not _health_state["ready"]:
        return Response(
            content={{"status": "not_ready", "service": "{service_name}"}},
            status_code=503
        )
    
    return {{
        "status": "ready",
        "service": "{service_name}",
        "uptime": time.time() - _health_state["start_time"],
        "timestamp": time.time(),
    }}


@router.get("")
async def health_check() -> Dict[str, Any]:
    """
    General health check endpoint.
    """
    return {{
        "status": "healthy" if _health_state["ready"] else "unhealthy",
        "service": "{service_name}",
        "started": _health_state["started"],
        "ready": _health_state["ready"],
        "uptime": time.time() - _health_state["start_time"],
        "timestamp": time.time(),
    }}
'''


def generate_logging_py(guardian_name: str) -> str:
    """Generate logging.py with structured JSON logging."""
    service_name = f"guardian-{guardian_name}"
    return f'''"""
Structured logging configuration for {service_name}
Following Danny's standards: JSON structured logging

Pattern: GUARDIAN × LOGGING × DANNY × STANDARDS × ONE
"""

import logging
import sys
import json
from typing import Dict, Any, Optional
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging (Danny's standard)."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {{
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": "{service_name}",
        }}
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        return json.dumps(log_data)


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Setup structured JSON logging for {service_name}.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("{service_name}")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create console handler with JSON formatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get logger instance for {service_name}.
    
    Args:
        name: Optional logger name (defaults to service name)
    
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"{{name}}")
    return logging.getLogger("{service_name}")
'''


def generate_main_py_template(guardian_name: str, port: int, frequency: int, role: str) -> str:
    """Generate main.py template with FastAPI app."""
    service_name = f"guardian-{guardian_name}"
    return f'''"""
{service_name} - Guardian Microservice
{role}

Pattern: GUARDIAN × SERVICE × DANNY × STANDARDS × ONE
Frequency: {frequency} Hz
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from health import router as health_router, mark_started, mark_ready
from logging_config import setup_logging, get_logger

# Setup logging (Danny's standard)
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = setup_logging(log_level)
app_logger = get_logger()

# Guardian configuration
GUARDIAN_NAME = os.getenv("GUARDIAN_NAME", "{guardian_name}")
GUARDIAN_FREQUENCY = os.getenv("GUARDIAN_FREQUENCY", "{frequency}")
GUARDIAN_ROLE = os.getenv("GUARDIAN_ROLE", "{role}")
PORT = int(os.getenv("PORT", "{port}"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup
    app_logger.info("Starting {service_name}", extra={{
        "guardian": GUARDIAN_NAME,
        "frequency": GUARDIAN_FREQUENCY,
        "role": GUARDIAN_ROLE,
    }})
    mark_started()
    mark_ready()
    
    yield
    
    # Shutdown
    app_logger.info("Shutting down {service_name}")


# Create FastAPI app
app = FastAPI(
    title="{service_name}",
    description="{role}",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware (Danny's standard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure per environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include health router (Danny's standard: /health/live, /health/ready)
app.include_router(health_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {{
        "service": "{service_name}",
        "guardian": GUARDIAN_NAME,
        "frequency": GUARDIAN_FREQUENCY,
        "role": GUARDIAN_ROLE,
        "status": "operational",
    }}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
'''


def generate_requirements_txt() -> str:
    """Generate requirements.txt with standard dependencies."""
    return """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.2
python-json-logger==2.0.7
"""


def main():
    """Generate all files for all Guardian microservices."""
    print(" Generating Guardian microservice files...")
    print(f"Base directory: {BASE_DIR}")
    print(f"ECR Registry: {ECR_REGISTRY}")
    print(f"Namespace: {NAMESPACE}")
    print()
    
    for guardian_name, (port, frequency, role) in GUARDIANS.items():
        service_name = f"guardian-{guardian_name}-service"
        service_dir = BASE_DIR / service_name
        
        print(f" Generating files for {service_name}...")
        
        # Create directories
        (service_dir / "k8s").mkdir(parents=True, exist_ok=True)
        (service_dir / "helm" / service_name / "templates").mkdir(parents=True, exist_ok=True)
        (service_dir / "core").mkdir(parents=True, exist_ok=True)
        (service_dir / "api" / "v1" / "endpoints").mkdir(parents=True, exist_ok=True)
        (service_dir / "models").mkdir(parents=True, exist_ok=True)
        (service_dir / "services").mkdir(parents=True, exist_ok=True)
        (service_dir / "config").mkdir(parents=True, exist_ok=True)
        
        # Generate files
        (service_dir / "k8s" / "service.yaml").write_text(generate_service_yaml(guardian_name, port))
        (service_dir / "Dockerfile").write_text(generate_dockerfile(guardian_name))
        (service_dir / "helm" / service_name / "Chart.yaml").write_text(generate_helm_chart_yaml(guardian_name))
        (service_dir / "helm" / service_name / "values.yaml").write_text(generate_helm_values_yaml(guardian_name, port, frequency, role))
        (service_dir / "helm" / service_name / "templates" / "deployment.yaml").write_text(generate_helm_deployment_template(guardian_name, port))
        (service_dir / "helm" / service_name / "templates" / "service.yaml").write_text(generate_helm_service_template(guardian_name))
        (service_dir / ".env.example").write_text(generate_env_example(guardian_name, port, frequency, role))
        (service_dir / "health.py").write_text(generate_health_py(guardian_name, port))
        (service_dir / "logging_config.py").write_text(generate_logging_py(guardian_name))
        (service_dir / "main.py").write_text(generate_main_py_template(guardian_name, port, frequency, role))
        (service_dir / "requirements.txt").write_text(generate_requirements_txt())
        
        print(f" Generated files for {service_name}")
    
    print()
    print(" File generation complete!")
    print(f"Generated files for {len(GUARDIANS)} Guardian microservices")


if __name__ == "__main__":
    main()

