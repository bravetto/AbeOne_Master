# CodeGuardians Gateway

**Unified Orchestration Gateway for AI Guard Services Ecosystem**

The CodeGuardians Gateway is a comprehensive orchestration service that provides unified access, routing, and management for all AI guard services in the Code Guardians ecosystem. Built using Template Heaven's gold-standard Python service template, it ensures enterprise-grade reliability, security, and scalability.

---

##  Quick Start (New Developers - Start Here!)

**Get running in 60 seconds:**

**Linux/Mac/Git Bash:**
```bash
./setup.sh
```

**Windows PowerShell:**
```powershell
.\setup.ps1
```

**That's it!** The script handles everything automatically:

-  Check if Docker is running
-  Create env.unified from env.example if needed
-  Validate configuration
-  Clean up old volumes (prevents password issues)
-  Start all services
-  Wait for health checks
-  Test the API

### Manual Setup (Alternative)

If you prefer manual setup:

1. **Ensure Docker is running**
2. **Copy environment file:**
   ```bash
   cp env.example env.unified
   ```
3. **Start services:**
   ```bash
   docker-compose up -d
   ```
4. **Wait for health checks:**
   ```bash
   docker-compose ps
   ```
5. **Test the API:**
   ```bash
   curl http://localhost:8000/health
   ```

---

##  Guard Services Orchestration

### **Core Guard Services**
- **TokenGuard** - AI token cost optimization and intelligent pruning
- **TrustGuard** - AI reliability service with 7 failure pattern detection
- **ContextGuard** - Advanced context drift detection and management
- **BiasGuard Backend** - Bias detection and mitigation API service

### **Gateway Features**
- **Unified API Gateway** - Single entry point for all guard services
- **Intelligent Routing** - Smart request routing and load balancing
- **Service Discovery** - Dynamic service registration and health monitoring
- **Circuit Breaker** - Fault tolerance and graceful degradation
- **Rate Limiting** - API protection and resource management
- **Authentication & Authorization** - Unified security across all services
- **Monitoring & Observability** - Comprehensive metrics and tracing
- **Configuration Management** - Centralized configuration for all guards

##  Prerequisites

- Docker Desktop (running)
- Git Bash (Windows) or standard terminal (Linux/Mac)

##  Local Development Setup

### Quick Setup (Automated)
```bash
# Run the setup script - it does everything!
./setup.sh              # Linux/Mac/Git Bash
# OR
.\setup.ps1             # Windows PowerShell
```

### Manual Setup
```bash
# 1. Create environment file
cp env.example env.unified

# 2. Clean start (prevents password issues)
docker-compose down -v

# 3. Start all services
docker-compose up -d

# 4. Verify
curl http://localhost:8000/health/live
```

##  Usage

**Access Points:**
- API Gateway: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- PostgreSQL: localhost:5433
- Redis: localhost:6380

**Common Commands:**
```bash
docker-compose logs -f              # View logs
docker-compose restart              # Restart services
docker-compose down                 # Stop services
docker-compose down -v              # Stop and clean volumes
docker ps                           # Check container status
```

##  Documentation

### Quick Guides
- **[QUICKSTART.md](./QUICKSTART.md)** - Get started in 60 seconds
- **[LOCAL_TESTING_GUIDE.md](./LOCAL_TESTING_GUIDE.md)** - Complete local testing instructions
- **[ENDPOINT_REFERENCE.md](./ENDPOINT_REFERENCE.md)** - API endpoint documentation

### Troubleshooting
- **[TROUBLESHOOTING_DATABASE.md](./TROUBLESHOOTING_DATABASE.md)** - Database connection issues
- **[DEBUG_STARTUP.md](./DEBUG_STARTUP.md)** - Startup problems and diagnostics

### Deployment & Integration
- **[DOMAIN_CONFIGURATION.md](./DOMAIN_CONFIGURATION.md)** - Multi-domain setup (aiguardian.ai)
- **[FRONTEND_BACKEND_INTEGRATION.md](./FRONTEND_BACKEND_INTEGRATION.md)** - Frontend integration guide
- See [docs/](docs/) for additional documentation

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

##  License

This project is licensed under the MIT License.

##  Upstream Source

- **Original Template**: gold-standard-python-service
- **Upstream URL**: https://github.com/template-heaven/templateheaven
- **Template Version**: 2.0.0
