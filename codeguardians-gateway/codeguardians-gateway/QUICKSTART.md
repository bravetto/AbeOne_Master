# AI Guardians Quick Start Guide

## Overview

This guide will help you get up and running with the AI Guardians platform in under 10 minutes.

## Prerequisites

- Docker and Docker Compose
- Git
- API key (get one at [aiguardian.ai](https://aiguardian.ai))

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/bravetto/AI-Guardians-Backend-2.git
cd AI-Guardians-Backend-2
```

### 2. Set Up Environment

```bash
# Copy environment template
cp codeguardians-gateway/codeguardians-gateway/.env.example codeguardians-gateway/codeguardians-gateway/.env

# Edit environment variables
nano codeguardians-gateway/codeguardians-gateway/.env
```

### 3. Start Services

```bash
cd codeguardians-gateway/codeguardians-gateway
docker-compose up --build
```

### 4. Test the API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test guard service
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "service_type": "tokenguard",
    "payload": {
      "text": "This is a test message for token optimization."
    },
    "client_type": "api"
  }'
```

## Next Steps

- [API Documentation](./API_DOCUMENTATION.md)
- [VS Code Extension Integration](./VSCODE_INTEGRATION.md)
- [Chrome Extension Integration](./CHROME_INTEGRATION.md)
- [Docker Deployment Guide](./DOCKER_DEPLOYMENT.md)

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill processes using port 8000
   sudo lsof -ti:8000 | xargs kill -9
   ```

2. **Docker build fails**
   ```bash
   # Clean Docker cache
   docker system prune -a
   ```

3. **Database connection error**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps postgres
   ```

### Getting Help

- [Documentation](https://docs.aiguardian.ai)
- [Discord Community](https://discord.gg/aiguardian)
- [GitHub Issues](https://github.com/bravetto/AI-Guardians/issues)

