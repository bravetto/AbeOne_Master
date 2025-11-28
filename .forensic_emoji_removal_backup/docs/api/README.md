# AIGuardian - Unified AI Security Platform

**Single API Endpoint • Context Drift Handling • Enterprise Security**

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://python.org)

---

## 📚 Quick Navigation

**👉 Start Here:**

| Your Role | Start With | Description |
|-----------|------------|-------------|
| **🧪 Testing & Using** | **[GETTING_STARTED.md](GETTING_STARTED.md)** | Quick start, testing, API usage examples |
| **💻 Developing** | **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** | Development setup, testing, contributing |

**Additional Documentation:**

| Document | Audience | Purpose |
|----------|----------|---------|
| [docs/api/README.md](docs/api/README.md) | All | **Unified API Documentation** - Complete endpoint reference |
| [OPTIMIZATION_AND_FIXES_STATUS.md](OPTIMIZATION_AND_FIXES_STATUS.md) | All | **System Status** - Complete optimization and fixes overview |
| [INFRASTRUCTURE_AND_DEPLOYMENT_STATUS.md](INFRASTRUCTURE_AND_DEPLOYMENT_STATUS.md) | DevOps | **Infrastructure Status** - Deployment and container status |
| [SECRETS_CONFIGURATION_GUIDE.md](SECRETS_CONFIGURATION_GUIDE.md) | DevOps | **Secrets Management** - Complete secrets configuration |
| [docs/SUBMODULE_CLONING_GUIDE.md](docs/SUBMODULE_CLONING_GUIDE.md) | All | **Git Submodule Cloning** - Access requirements and troubleshooting |
| [USER_GUIDE.md](USER_GUIDE.md) | End Users | Detailed API usage and examples |
| [DEVOPS_GUIDE.md](DEVOPS_GUIDE.md) | DevOps | Production deployment and AWS setup |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | All | Common issues and solutions |

---

## 🛡️ Overview

AIGuardian provides intelligent AI protection through a **single unified API endpoint** with automatic context drift detection and handling. It combines 8 specialized guard services into one seamless security platform.

### Key Features
- **Single Endpoint**: `POST /api/v1/guards/process` for all guard services
- **Context Drift Handling**: Automatic detection and mitigation
- **Enterprise Security**: JWT, rate limiting, input validation
- **Production Ready**: Docker, AWS ECS, monitoring, health checks
- **External Integrations**: AWS Secrets Manager, Neon DB, Stripe payments

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- AWS CLI (for production deployment)
- Git

### 1. Clone & Setup
```bash
git clone <repository-url>
cd AIGuards-Backend-1
```

### 2. Local Development
```bash
# Start all services (development mode)
./scripts/aiguardian.sh dev

# Check health
curl http://localhost:8000/health
```

### 3. Production Deployment
**⚠️ External Services Required**

For production deployment, you must first set up external services:

```bash
# Interactive setup for all external services
./scripts/aiguardian.sh setup-external

# Validate all configurations
./scripts/aiguardian.sh validate

# Deploy to AWS with secrets management
./scripts/aiguardian.sh prod
```

### 🆕 Consolidated Script System

AIGuardian now uses a unified script system for better maintainability and cross-platform support:

| Platform | Script | Purpose |
|----------|--------|---------|
| **Linux/macOS** | `./scripts/aiguardian.sh` | Main management script |
| **Windows** | `.\scripts\aiguardian.ps1` | PowerShell management script |
| **Cross-platform** | `python scripts/aiguardian_deploy.py` | Python deployment script |

**Quick Commands:**
```bash
# Development
./scripts/aiguardian.sh dev

# Testing
./scripts/aiguardian.sh test

# Production
./scripts/aiguardian.sh prod

# Health check
./scripts/aiguardian.sh health
```

📖 **Script Documentation: [scripts/README.md](scripts/README.md)**

📖 **Complete Setup Guide**: See [EXTERNAL_SERVICES_SETUP.md](EXTERNAL_SERVICES_SETUP.md) for detailed instructions.

### External Services Checklist
- [ ] **Stripe Account** - Payment processing & webhooks
- [ ] **Clerk Application** - User authentication & JWT
- [ ] **Neon Database** - PostgreSQL with connection pooling
- [ ] **AWS Secrets Manager** - Secure configuration storage
- [ ] **ElastiCache Redis** - High-performance caching

## 📋 Guard Services

| Service | Internal Port | Purpose | Access Method | Status |
|---------|---------------|---------|---------------|--------|
| **TokenGuard** | 8001 | Token optimization & cost management | Via Gateway | ✅ Active |
| **TrustGuard** | 8002 | Trust validation & reliability | Via Gateway | ✅ Active |
| **ContextGuard** | 8003 | Context drift detection & memory management | Via Gateway | ✅ Active |
| **BiasGuard** | 8004 | Bias detection & content analysis | Via Gateway | ✅ Active |
| **SecurityGuard** | 8005 | Security scanning & threat detection | Via Gateway | ✅ Active |
| **HealthGuard** | 8005 | Health monitoring & validation | Via Gateway | ✅ Active |

**⚠️ Important**: All guard services run on internal Docker network ports only. Access all services via the unified gateway endpoint: `POST /api/v1/guards/process`.

## 🔧 API Usage

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
For comprehensive endpoint documentation, see [docs/api/README.md](docs/api/README.md)

## 🔀 Service Access Pattern

### Gateway-Only Architecture
The CodeGuardians system uses a **gateway-only access pattern** where all external requests must go through the unified API gateway. Guard services run on internal Docker network ports and are not directly accessible from outside the container network.

### Why This Architecture?
- **Security**: Direct service exposure increases attack surface
- **Load Balancing**: Gateway handles request distribution and failover
- **Monitoring**: Centralized logging and metrics collection
- **Rate Limiting**: Unified rate limiting across all services
- **Authentication**: Single point of authentication and authorization

### Access Methods

#### 1. Service Processing
```bash
POST /api/v1/guards/process
Content-Type: application/json

{
  "service_type": "tokenguard|trustguard|contextguard|biasguard|securityguard|healthguard",
  "payload": { /* service-specific parameters */ },
  "user_id": "string",
  "session_id": "string"
}
```

#### 2. Service Health Checks
```bash
# Individual service health
GET /api/v1/guards/health/{service_name}

# Overall system health
GET /api/v1/guards/health

# Service discovery
GET /api/v1/guards/services
```

#### 3. Authentication (when required)
```bash
POST /api/v1/auth/login
POST /api/v1/auth/register
```

## 🏗️ Architecture

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
│  │ (Port 8004) │                    │ (Port 8005) │         │
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



## � Development & Testing

### Local Development
```bash
# Start development environment
./run.sh dev

# Run tests
./run.sh test

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
├── deployment/              # Deployment configurations
├── shared/                  # Shared utilities and common code
├── scripts/                 # Build and deployment scripts
└── docs/                    # Documentation
```

### Testing
```bash
# Run all tests
./run.sh test

# Run specific service tests
./run.sh test tokenguard

# Integration tests
./run.sh test integration
```

## 📚 Documentation

### Quick References
- **API Documentation**: `http://localhost:8000/docs`
- **Health Checks**: `http://localhost:8000/health`
- **Service Discovery**: `http://localhost:8000/api/v1/guards/services`



### Setup & Deployment
- **[Getting Started](GETTING_STARTED.md)** - Quick start and testing guide
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Development setup and contributing
- **[Infrastructure & Deployment Status](INFRASTRUCTURE_AND_DEPLOYMENT_STATUS.md)** - Complete infrastructure and deployment overview
- **[DevOps Guide](DEVOPS_GUIDE.md)** - Production deployment and AWS setup
- **[Secrets Configuration Guide](SECRETS_CONFIGURATION_GUIDE.md)** - Complete secrets management
- **[External Services Setup](EXTERNAL_SERVICES_SETUP.md)** - Complete external service configuration

## � Troubleshooting

### Common Issues
```bash
# Services not starting
./run.sh logs
./run.sh restart

# Database connection issues
./run.sh db-check

# AWS deployment issues
./run.sh aws-status
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
./run.sh dev

# Check service connectivity
./run.sh network-test
```

## 📞 Support & Resources

### Health Checks
- Gateway: `http://localhost:8000/health`
- Individual Services: `http://localhost:8001-8004/health` and `http://localhost:8005/health`

### Logs
```bash
# View all logs
./run.sh logs

# Follow logs in real-time
./run.sh logs -f

# Service-specific logs
./run.sh logs tokenguard
```

### Backups
```bash
# Database backup
./run.sh backup

# Configuration backup
./run.sh config-backup
```

## 🎯 What's Different

This consolidated version provides:
- **Single Script**: `./run.sh` handles all deployment scenarios
- **Unified Documentation**: Fewer files, clearer navigation
- **External Dependencies**: Clear mapping of all external services
- **AWS Secrets Manager**: Comprehensive setup guide
- **Streamlined Architecture**: Focus on essential components

## 📋 Migration from Previous Versions

If migrating from AIGuards-Backend or AIGuards-Backend-1:
1. Use `./run.sh` instead of multiple deployment scripts
2. Configure AWS Secrets Manager for production secrets
3. Update external service configurations
4. Test with `./run.sh test` before deployment

---

**Ready to deploy?** Run `./run.sh dev` for development or `./run.sh prod` for production with AWS Secrets Manager.
