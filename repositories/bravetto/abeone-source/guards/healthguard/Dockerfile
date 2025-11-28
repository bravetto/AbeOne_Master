# Stage 1: Build the application
FROM python:3.9-slim AS builder

WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml setup.py ./
COPY src/ /usr/src/app/src/

RUN pip install --upgrade pip
RUN pip install .

# Stage 2: Create the production image
FROM python:3.9-slim

WORKDIR /usr/src/app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy source files and configuration
COPY src/ /usr/src/app/src/
COPY config.yaml logging.yaml ./
COPY run_server.py ./

# Create directories for logs and data and set ownership
RUN mkdir -p /usr/src/app/logs /usr/src/app/data && \
    useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /usr/src/app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Add labels for better container management
LABEL maintainer="Vibe Coders <contact@vibecoders.com>"
LABEL version="0.3.0"
LABEL description="PoisonGuard - LLM Poisoning Detection and Mitigation Tool"

CMD ["python", "run_server.py"]