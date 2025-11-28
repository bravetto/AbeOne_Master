# AIGuardian - Unified AI Security Platform

**Single API Endpoint • Context Drift Handling • Enterprise Security**

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://python.org)

---

## 📚 Quick Navigation

**Start Here:**

| Your Role | Start With | Description |
|-----------|------------|-------------|
| **Testing & Using** | **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)** | Quick start, testing, API usage examples |
| **Developing** | **[docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** | Development setup, testing, contributing |
| **DevOps** | **[docs/deployment/DEVOPS_GUIDE.md](docs/deployment/DEVOPS_GUIDE.md)** | Production deployment and AWS setup |
| **End Users** | **[docs/USER_GUIDE.md](docs/USER_GUIDE.md)** | Simple API usage and examples |

**Complete Documentation:** [docs/INDEX.md](docs/INDEX.md)

---

## Overview

AIGuardian provides intelligent AI protection through a **single unified API endpoint** with automatic context drift detection and handling. It combines 6 specialized guard services into one seamless security platform.

### Key Features
- **Single Endpoint**: `POST /api/v1/guards/process` for all guard services
- **Context Drift Handling**: Automatic detection and mitigation
- **Enterprise Security**: JWT, rate limiting, input validation
- **Production Ready**: Docker, AWS ECS, monitoring, health checks
- **External Integrations**: AWS Secrets Manager, Neon DB, Stripe payments

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- AWS CLI (for production deployment)
- Git

### 1. Clone & Setup
```bash
git clone <repository-url>
cd AIGuards-Backend-2
```

### 2. Local Development
```bash
# Start all services (development mode)
cd codeguardians-gateway/codeguardians-gateway
docker-compose up -d

# Wait for services to initialize (~30 seconds)
sleep 30

# Check health
curl http://localhost:8000/health/live
```

### 3. Production Deployment
**[WARNING] External Services Required**

For production deployment, you must first set up external services:

```bash
# Use unified deployment scripts
./scripts/deploy.sh prod

# Or follow the complete guide
# See docs/DEVOPS_GUIDE.md for detailed instructions
```

**Complete Setup Guide**: See [docs/EXTERNAL_SERVICES_SETUP.md](docs/EXTERNAL_SERVICES_SETUP.md) for detailed instructions.

### External Services Checklist
- [ ] **Stripe Account** - Payment processing & webhooks
- [ ] **Clerk Application** - User authentication & JWT
- [ ] **Neon Database** - PostgreSQL with connection pooling
- [ ] **AWS Secrets Manager** - Secure configuration storage
- [ ] **ElastiCache Redis** - High-performance caching

---

## Guard Services

| Service | Port | Purpose | Status |
|---------|------|---------|--------|
| **TokenGuard** | 8001 | Token optimization & cost management | [OK] Active |
| **TrustGuard** | 8002 | Trust validation & reliability | [OK] Active |
| **ContextGuard** | 8003 | Context drift detection & memory management | [OK] Active |
| **BiasGuard** | 8004 | Bias detection & content analysis | [OK] Active |
| **HealthGuard** | 8006 | Health monitoring & validation | [OK] Active |

---

## API Usage

### Single Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "your content here"},
    "user_id": "user123",
    "session_id": "session456"
  }'
```

### Response Format
```json
{
  "status": "success",
  "service": "tokenguard",
  "result": {
    "optimized_tokens": 150,
    "cost_savings": 0.3,
    "confidence_score": 0.95
  },
  "processing_time": 0.123
}
```

### Complete API Reference
For comprehensive endpoint documentation, see [api/README.md](api/README.md)

---

## Architecture

### Core Components
```
┌─────────────────────────────────────────────────────────────┐
│                    AIGUARDIAN ECOSYSTEM                     │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ TOKEN GUARD │  │ TRUST GUARD │  │ CONTEXT     │         │
│  │ (Port 8001) │  │ (Port 8002) │  │ GUARD       │         │
│  │             │  │             │  │ (Port 8003) │         │
│  │ • Cost Opt. │  │ • Validation│  │ • Drift Det.│         │
│  │ • Chunking  │  │ • Reliability│  │ • Memory   │         │
│  └─────────────┘  └─────────────┘  └─────────────────┘     │
│           │                │                │              │
│           └────────────────┼────────────────┘              │
│                            │                               │
│  ┌─────────────┐                    ┌─────────────┐         │
│  │ BIAS GUARD  │                    │ HEALTH GUARD│         │
│  │ (Port 8004) │                    │ (Port 8006) │         │
│  │             │                    │             │         │
│  │ • Detection │                    │ • Monitoring│         │
│  │ • Mitigation│                    │ • Validation│         │
│  └─────────────┘                    └─────────────┘         │
│                            │                               │
│                            ▼                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 API GATEWAY                         │   │
│  │                 (Port 8000)                         │   │
│  │                                                     │   │
│  │ • Single Endpoint: /api/v1/guards/process          │   │
│  │ • Load Balancing • Rate Limiting • Auth            │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              EXTERNAL DEPENDENCIES                  │   │
│  │                                                     │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │   │
│  │  │  AWS    │  │  NEON   │  │ STRIPE  │  │ CLERK   │  │   │
│  │  │ Secrets │  │   DB    │  │ PAYMENT │  │  AUTH   │  │   │
│  │  │ Manager │  │         │  │         │  │         │  │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### External Dependencies
| Service | Purpose | Configuration |
|---------|---------|---------------|
| **AWS Secrets Manager** | Secure secrets storage | `codeguardians-gateway/production` |
| **Neon Database** | PostgreSQL database | Connection via secrets |
| **Stripe** | Payment processing | Webhook integration |
| **Clerk** | Authentication | JWT tokens, user management |
| **AWS ECS** | Container orchestration | Production deployment |
| **ElastiCache Redis** | Caching & sessions | High-performance cache |

---

## Development & Testing

### Local Development
```bash
# Start development environment
cd codeguardians-gateway/codeguardians-gateway
docker-compose up -d

# Run tests
python scripts/test-suite.py --quick

# View API documentation
open http://localhost:8000/docs
```

### Code Structure
```
AIGuards-Backend-2/
├── codeguardians-gateway/    # Main API gateway
├── guards/                   # All guard services
│   ├── tokenguard/          # Token optimization & cost management
│   ├── trust-guard/         # Trust validation & reliability
│   ├── contextguard/        # Context drift detection & memory management
│   ├── biasguard-backend/   # Bias detection & content analysis
│   └── healthguard/         # Health monitoring & validation
├── tests/                   # Comprehensive test suite
│   ├── integration/         # System integration tests
│   ├── docker/              # Container & infrastructure tests
│   ├── services/            # Individual guard service tests
│   ├── gateways/            # API gateway & routing tests
│   └── helpers/             # Test utilities & helpers
├── scripts/                 # Build, deployment & utility scripts
│   ├── check_db.py          # Database connectivity checks
│   ├── create_posts_table.py # Database table creation
│   ├── deduplicate.py       # Data deduplication utilities
│   └── [deployment scripts] # Build and deployment automation
├── shared/                  # Shared utilities and common code
├── docs/                    # Organized documentation
└── monitoring/              # Monitoring and observability configs
```

### Testing
```bash
# Run all tests (organized by category)
pytest tests/ -v

# Run specific test categories
pytest tests/integration/ -v    # System integration tests
pytest tests/services/ -v       # Individual guard service tests
pytest tests/docker/ -v         # Container & infrastructure tests
pytest tests/gateways/ -v       # API gateway tests

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Legacy test runner (still available)
python scripts/test-suite.py --quick
```

---

## Documentation

### Quick References
- **API Documentation**: `http://localhost:8000/docs`
- **Health Checks**: `http://localhost:8000/health`
- **Service Discovery**: `http://localhost:8000/api/v1/guards/services`

### Setup & Deployment
- **[Getting Started](docs/GETTING_STARTED.md)** - Quick start and testing guide
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Development setup and contributing
- **[DevOps Guide](docs/deployment/DEVOPS_GUIDE.md)** - Production deployment and AWS setup
- **[External Services Setup](docs/deployment/EXTERNAL_SERVICES_SETUP.md)** - Complete external service configuration

### Additional Documentation
- **[Complete Documentation Index](docs/INDEX.md)** - Full documentation navigation
- **[API Reference](api/README.md)** - Complete API endpoint reference
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

---

## Troubleshooting

### Common Issues
```bash
# Services not starting
docker-compose logs -f
docker-compose restart

# Database connection issues
docker-compose ps postgres
docker-compose logs postgres

# Health check failures
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
docker-compose up -d

# Check service connectivity
curl http://localhost:8000/api/v1/guards/services
```

For detailed troubleshooting, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## Support & Resources

### Health Checks
- Gateway: `http://localhost:8000/health`
- Individual Services: `http://localhost:8001-8004/health` and `http://localhost:8006/health`

### Logs
```bash
# View all logs
docker-compose logs -f

# Follow logs in real-time
docker-compose logs -f --tail 50 --timestamps

# Service-specific logs
docker-compose logs -f codeguardians-gateway
docker-compose logs -f tokenguard
```

---

## What's Different

This consolidated version provides:
- **Single Script**: `./scripts/deploy.sh` handles all deployment scenarios
- **Unified Documentation**: Fewer files, clearer navigation
- **External Dependencies**: Clear mapping of all external services
- **AWS Secrets Manager**: Comprehensive setup guide
- **Streamlined Architecture**: Focus on essential components

---

## Migration from Previous Versions

If migrating from AIGuards-Backend or AIGuards-Backend-1:
1. Use `./scripts/deploy.sh` instead of multiple deployment scripts
2. Configure AWS Secrets Manager for production secrets
3. Update external service configurations
4. Test with `python scripts/test-suite.py` before deployment

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and changes.

---

## Contributing

We welcome contributions! Please see:
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - How to contribute
- **[CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md)** - Community guidelines
- **[DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** - Development setup

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Links

- **Documentation**: [docs/INDEX.md](docs/INDEX.md)
- **API Reference**: [api/README.md](api/README.md)
- **Scripts**: [scripts/README.md](scripts/README.md)
- **Issues**: Create GitHub issues for bugs and feature requests

---

**Ready to deploy?** Run `./scripts/deploy.sh dev` for development or `./scripts/deploy.sh prod` for production with AWS Secrets Manager.