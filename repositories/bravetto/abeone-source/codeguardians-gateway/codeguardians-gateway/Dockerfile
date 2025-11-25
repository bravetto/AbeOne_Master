# Production Dockerfile for codeguardians-gateway
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/usr/local/bin:$PATH"

# Install system dependencies, create user, and set working directory in one layer
RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    awscli \
    bash \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && groupadd -r codeguardians-gateway && useradd -r -g codeguardians-gateway codeguardians-gateway

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies globally
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=codeguardians-gateway:codeguardians-gateway . .

# Copy entrypoint script and fix line endings
COPY scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && \
    sed -i 's/\r$//' /app/entrypoint.sh && \
    dos2unix /app/entrypoint.sh 2>/dev/null || sed -i 's/\r//' /app/entrypoint.sh && \
    chown codeguardians-gateway:codeguardians-gateway /app/entrypoint.sh

# Install application package globally
RUN pip install --no-cache-dir .

# Create necessary directories and fix permissions
# Note: Removed /app/uploads and /app/cache as we now use S3 and Redis
RUN mkdir -p /app/logs \
    && chown -R codeguardians-gateway:codeguardians-gateway /app

USER codeguardians-gateway

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/live || exit 1

# Use entrypoint script for runtime secret loading
# This enables AWS Secrets Manager support for production
# Use bash explicitly to ensure it works
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]