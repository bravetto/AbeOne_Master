# Trust Guard AI Reliability Service

## Overview

Trust Guard is an enterprise-grade AI reliability service that detects and mitigates seven critical AI failure patterns: hallucination, drift, bias, deception, security theater, duplication, and stub syndrome. It provides comprehensive validation, constitutional prompting, and real-time monitoring to ensure AI systems maintain reliability and trustworthiness in production environments.

## Features

- **AI Failure Pattern Detection**: Detects 7 critical AI failure patterns with high accuracy
- **Mathematical Validation**: KL divergence, uncertainty quantification, and statistical analysis
- **Constitutional Prompting**: Automated mitigation strategies and enhancement techniques
- **Enterprise Security**: API key authentication, JWT tokens, RBAC, and audit logging
- **Real-time Monitoring**: Prometheus metrics, health checks, and distributed tracing
- **Production Ready**: Comprehensive error handling, graceful degradation, and observability
- **FastAPI**: Modern async API with automatic documentation and OpenAPI specs

## Quick Start

### Prerequisites

- Python 3.8+
- Docker (optional)
- Kubernetes (optional)

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Access API documentation
open http://localhost:8000/docs

# Run comprehensive tests
python -m pytest tests/unit/ -v

# Run CI/CD test suite
python tests/ci_cd_test_reporter.py --base-url http://localhost:8000 --output-dir test-results --verbose
```

### Docker

```bash
# Build image
docker build -t trust-guard .

# Run container
docker run -p 8000:8000 trust-guard

# Or use docker-compose
docker-compose up
```

### AWS Production Deployment

Trust Guard includes complete AWS infrastructure-as-code for production deployment using ECS Fargate:

#### Prerequisites

1. **AWS Account & CLI**: Configure AWS credentials
   ```bash
   aws configure
   ```

2. **Permissions Required**:
   - EC2 Full Access
   - ECS Full Access
   - ECR Full Access
   - CloudFormation Full Access
   - IAM Full Access (for stack deployment)

#### One-Command Deployment

```bash
# Deploy everything to AWS (default VPC configuration)
cd aws && ./deploy.sh

# Or deploy specific components
./deploy.sh infrastructure  # Only AWS infrastructure
./deploy.sh image          # Only build and push Docker image
```

#### Manual Deployment Steps

1. **Build and push Docker image**:
   ```bash
   docker build -t trust-guard:latest .
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com
   docker tag trust-guard:latest YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/trust-guard:latest
   docker push YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/trust-guard:latest
   ```

2. **Deploy CloudFormation infrastructure**:
   ```bash
   aws cloudformation deploy \
     --template-file aws/infrastructure.yml \
     --stack-name trust-guard-prod \
     --parameter-overrides \
       EnvironmentName=prod \
       VpcId=vpc-xxxxx \
       SubnetIds="subnet-xxxxx,subnet-yyyyy" \
     --capabilities CAPABILITY_IAM
   ```

#### Environment Variables for Production

```bash
TOKENGUARD_LOG_LEVEL=INFO
TOKENGUARD_ENABLE_METRICS=true
TOKENGUARD_API_KEY=your-secure-api-key  # Optional: API authentication
AWS_REGION=us-east-1
```

#### Monitoring & Logging

- **CloudWatch Logs**: `/ecs/prod/trust-guard`
- **Health Checks**: ALB performs health checks every 30 seconds
- **Metrics**: CPU/Memory utilization alarms set at 80%
- **Load Balancing**: Application Load Balancer with auto-scaling

#### Repository Structure for AWS
```
trust-guard/
├── aws/
│   ├── infrastructure.yml    # CloudFormation template
│   └── deploy.sh            # Deployment automation script
├── docker-compose.aws.yml   # Development/testing compose
├── Dockerfile              # Production container
└── .github/
    └── workflows/
        └── deploy.yml      # CI/CD pipeline
```

### Kubernetes

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment
kubectl get pods -l app=tokenguard
kubectl get services -l app=tokenguard
```

## API Endpoints

### AI Pattern Detection

- `POST /v1/detect` - Detect AI failure patterns in text
- `POST /v1/validate` - Comprehensive mathematical validation
- `POST /v1/mitigate` - Apply constitutional prompting and mitigation
- `POST /v1/constitutional` - Generate constitutional prompts

### Security & Authentication

- `POST /v1/auth/keys` - Create API keys
- `GET /v1/auth/keys` - List API keys
- `DELETE /v1/auth/keys/{key_id}` - Revoke API key
- `POST /v1/auth/jwt` - Generate JWT tokens

### Monitoring & Observability

- `GET /health` - Basic health check
- `GET /health/live` - Kubernetes liveness probe
- `GET /health/ready` - Kubernetes readiness probe
- `GET /health/detailed` - Comprehensive health status
- `GET /metrics` - Prometheus metrics
- `GET /v1/observability/summary` - Observability summary

### Tracer Bullets (Debugging)

- `GET /v1/tracer/bullets` - Get tracer bullets
- `GET /v1/tracer/performance` - Performance metrics
- `GET /v1/tracer/health` - Tracer system health
- `DELETE /v1/tracer/bullets` - Clear tracer bullets

### Documentation

- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Architecture Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - Complete system architecture
- [High-Level Architecture](docs/high-level-architecture.md) - Simplified architecture diagrams
- [Component Interactions](docs/component-interactions.md) - Detailed component relationships
- [API Documentation](docs/API.md) - Complete API reference
- [Performance Guide](docs/PERFORMANCE.md) - Performance tuning and benchmarks
- [Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md) - Pre-deployment validation

## Configuration

Environment variables:

- `TRUSTGUARD_HOST` - Service host (default: 0.0.0.0)
- `TRUSTGUARD_PORT` - Service port (default: 8000)
- `TRUSTGUARD_LOG_LEVEL` - Logging level (default: INFO)
- `TRUSTGUARD_RATE_LIMIT` - Rate limit per minute (default: 100)
- `TRUSTGUARD_SECRET_KEY` - Secret key for API authentication
- `TRUSTGUARD_JWT_SECRET` - JWT signing secret
- `TRUSTGUARD_ENCRYPTION_KEY` - Data encryption key
- `TRUSTGUARD_ENV` - Environment (development/production)
- `TRUSTGUARD_DEBUG` - Debug mode (true/false)

## Testing

```bash
# Run all unit tests
python -m pytest tests/unit/ -v

# Run specific test suites
python -m pytest tests/unit/test_comprehensive_core.py -v
python -m pytest tests/unit/test_comprehensive_validation.py -v
python -m pytest tests/unit/test_comprehensive_constitutional.py -v
python -m pytest tests/unit/test_comprehensive_metrics.py -v
python -m pytest tests/unit/test_comprehensive_logging.py -v

# Run integration tests
python -m pytest tests/integration/ -v

# Run comprehensive CI/CD test suite
python tests/ci_cd_test_reporter.py --base-url http://localhost:8000 --output-dir test-results --verbose

# Run with coverage
python -m pytest tests/unit/ --cov=trustguard --cov-report=html
```

## Architecture

Trust Guard uses a modular, enterprise-grade architecture with:

- **FastAPI Application**: Modern async web framework with automatic OpenAPI documentation
- **AI Pattern Detectors**: Seven specialized detectors for different failure patterns
- **Validation Engine**: Mathematical validation using KL divergence and statistical analysis
- **Constitutional Prompting**: Automated mitigation strategies and enhancement techniques
- **Security Manager**: API key authentication, JWT tokens, and role-based access control
- **Observability Manager**: OpenTelemetry integration, distributed tracing, and metrics
- **Health Checker**: Kubernetes-compatible health checks and system monitoring
- **Tracer Manager**: Debugging and performance monitoring with tracer bullets
- **Configuration Manager**: Environment-based settings with secrets management

## Performance

- **Response Time**: < 200ms for pattern detection requests
- **Throughput**: 1000+ requests/minute with rate limiting
- **Memory Usage**: < 512MB under normal load
- **Test Coverage**: 281/281 unit tests passing (100% success rate)
- **Health Checks**: < 5ms response time for Kubernetes probes
- **Pattern Detection**: 7 AI failure patterns detected with high accuracy

## Security

- **API Key Authentication**: Secure API key management with role-based access control
- **JWT Token Support**: Stateless authentication with configurable expiration
- **Input Validation**: Comprehensive input sanitization and validation
- **Rate Limiting**: Built-in protection against abuse and DoS attacks
- **Audit Logging**: Structured logging for security events and access tracking
- **Secrets Management**: Secure secrets rotation and environment-based configuration
- **Non-root Container**: Secure container execution with minimal privileges
- **Resource Limits**: Memory and CPU limits with monitoring

## Monitoring

Trust Guard includes comprehensive enterprise-grade monitoring:

- **Health Checks**: Kubernetes-compatible liveness, readiness, and detailed health probes
- **Prometheus Metrics**: Custom metrics for pattern detection, validation, and system performance
- **Distributed Tracing**: OpenTelemetry integration for request correlation and performance analysis
- **Structured Logging**: JSON-formatted logs with trace context and performance data
- **Tracer Bullets**: Debugging and performance monitoring with configurable bullet tracking
- **Observability Dashboard**: Real-time system health and performance metrics
- **SLI/SLO Tracking**: Service level indicators and objectives monitoring

## License

This project is part of the AIGuardians suite and is proprietary software.

## Support

For issues and questions, please contact the AIGuardians development team.
