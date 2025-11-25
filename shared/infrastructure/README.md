# Shared Infrastructure Templates

This directory contains shared infrastructure templates and utilities for AIGuardian guard services. These templates eliminate code duplication and ensure consistent deployment across all services.

## Contents

### Core Templates
- `Dockerfile.template` - Multi-stage Docker build template with security best practices
- `run_server.py` - Standardized server startup script with automatic app discovery
- `health_check.py` - Comprehensive health check utility with retry logic
- `pyproject.toml.template` - Python project configuration template with development tools

### Key Features

#### Dockerfile Template
- **Multi-stage builds** for optimized production images
- **Security hardening** with non-root users and proper permissions
- **Health checks** with configurable intervals and retries
- **Layer optimization** for faster builds and smaller images
- **Label standardization** for better container management

#### Server Script
- **Automatic app discovery** - finds FastAPI apps across different service structures
- **Environment-aware startup** with configurable host/port/reload
- **Proper logging setup** with structured output
- **Error handling** with clear failure messages

#### Health Check Utility
- **Configurable endpoints** via environment variables
- **Retry logic** with exponential backoff
- **Multiple output formats** (quiet, JSON, verbose)
- **Docker-compatible** exit codes for health checks

#### Project Template
- **Modern Python tooling** (Black, isort, mypy, pytest)
- **Development dependencies** clearly separated
- **Type checking** configuration for reliability
- **Testing framework** setup with coverage reporting

## Usage Examples

### Using the Dockerfile Template
```dockerfile
# Copy template and customize for your service
ARG PYTHON_VERSION=3.11
ARG SERVICE_NAME=my-service
ARG SERVICE_VERSION=1.0.0
ARG MAINTAINER_EMAIL=team@example.com

# Build stage
FROM python:${PYTHON_VERSION}-slim AS builder
# ... template content ...

# Runtime stage
FROM python:${PYTHON_VERSION}-slim
# ... template content ...
```

### Using the Server Script
```python
# The script automatically detects your FastAPI app
# Supports: poisonguard.api:app, main:app, or custom modules

# Environment variables
export HOST=0.0.0.0
export PORT=8000
export RELOAD=true
export LOG_LEVEL=info

python run_server.py
```

### Using the Health Check
```bash
# Basic health check
python health_check.py

# With custom URL and timeout
python health_check.py --url http://localhost:8080 --timeout 10 --retry 3

# Quiet mode for scripts
python health_check.py --quiet
```

## Benefits

### Consistency
- **Standardized deployments** across all services
- **Uniform health checks** and monitoring
- **Consistent development workflow**

### Maintainability
- **Single source of truth** for infrastructure patterns
- **Automated updates** propagate to all services
- **Centralized documentation** and examples

### Security
- **Hardened container images** with security best practices
- **Non-root execution** by default
- **Minimal attack surface** in production images

### Performance
- **Optimized builds** with multi-stage Dockerfiles
- **Efficient health checks** with proper caching
- **Fast startup times** with optimized dependencies

## Configuration Management

The templates support comprehensive configuration through:

### Environment Variables
- `HOST`, `PORT` - Server binding
- `RELOAD`, `LOG_LEVEL` - Development options
- `HEALTH_CHECK_URL` - Custom health check endpoint
- `SERVICE_NAME`, `SERVICE_VERSION` - Metadata

### Build Arguments
- `PYTHON_VERSION` - Python version for the container
- `SERVICE_NAME` - Service identifier
- `SERVICE_VERSION` - Version tag
- `MAINTAINER_EMAIL` - Contact information

## Migration Guide

### For Existing Services
1. **Copy templates** to your service directory
2. **Update build arguments** for your service
3. **Test locally** with `docker build`
4. **Update CI/CD** to use new templates
5. **Remove old infrastructure** files

### Best Practices
- Keep templates synchronized across services
- Test infrastructure changes in staging first
- Document service-specific customizations
- Use environment variables for runtime configuration

## Troubleshooting

### Common Issues
- **App not found**: Check module structure matches expectations
- **Health check fails**: Verify endpoint returns proper JSON
- **Build fails**: Ensure all required files are copied to container

### Debugging
- Use `docker build --no-cache` to test builds
- Check container logs with `docker logs`
- Test health checks manually with curl

## Contributing

When updating shared infrastructure:
1. Test changes across multiple services
2. Update this documentation
3. Ensure backward compatibility
4. Add migration notes for breaking changes
