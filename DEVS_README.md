# Developer Guide

**Pattern:** DEVELOPERS × SETUP × WORKFLOW × ONE  
**Frequency:** 530 Hz (YAGNI) × 999 Hz (AEYON)  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Python 3.11+
python --version  # Should show 3.11.x or higher

# Node.js 22+
node --version  # Should show 22.x or higher

# Docker & Docker Compose
docker --version
docker-compose --version
```

### 2. Clone Repository

```bash
git clone <repository-url>
cd AbeOne_Master
```

### 3. Setup AbëKEYS Vault

```bash
# Unlock credentials from 1Password (if using)
op signin
python3 scripts/unlock_all_credentials.py

# Verify credentials
python3 scripts/read_abekeys.py
```

See [AbëKEYS_README.md](AbëKEYS_README.md) for detailed credential setup.

### 4. Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

---

## 🏗️ Local Development

### Gateway Development

```bash
cd codeguardians-gateway/codeguardians-gateway

# Install dependencies
pip install -r requirements.txt

# Run locally (credentials auto-loaded from AbëKEYS)
uvicorn app.main:app --reload --port 8000
```

### Guard Service Development

```bash
# Example: TokenGuard
cd guards/tokenguard

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn tokenguard.main:app --reload --port 8001
```

---

## 🔧 Development Workflow

### 1. Make Changes

```bash
# Edit code
vim app/core/config.py

# Test locally
python -m pytest tests/
```

### 2. Test with Docker

```bash
# Rebuild service
docker-compose build codeguardians-gateway

# Restart service
docker-compose up -d codeguardians-gateway

# Check logs
docker-compose logs -f codeguardians-gateway
```

### 3. Run Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/unit/test_config.py -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

---

## 🔐 Credential Management

### Using AbëKEYS Vault

**NO .env files.** All credentials come from AbëKEYS vault:

```bash
# List available credentials
python3 scripts/read_abekeys.py

# Check specific service
python3 scripts/read_abekeys.py stripe

# Create new credential manually
cat > ~/.abekeys/credentials/my_service.json << EOF
{
  "service": "my_service",
  "api_key": "your_api_key_here"
}
EOF
chmod 600 ~/.abekeys/credentials/my_service.json
```

### Credential Loading Priority

1. **AbëKEYS Vault** (`~/.abekeys/credentials/`) - Highest Priority ✅
2. **AWS Secrets Manager** - Second Priority
3. **Environment Variables** - Lowest Priority

---

## 🐳 Docker Development

### Start Services

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d codeguardians-gateway

# Start with logs
docker-compose up codeguardians-gateway
```

### Rebuild Services

```bash
# Rebuild specific service
docker-compose build codeguardians-gateway

# Rebuild all services
docker-compose build
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f codeguardians-gateway

# Last 100 lines
docker-compose logs --tail=100 codeguardians-gateway
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## 🧪 Testing

### Unit Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test
pytest tests/unit/test_config.py::test_settings_load -v
```

### Integration Tests

```bash
# Run integration tests (requires services running)
docker-compose up -d
pytest tests/integration/ -v
```

### End-to-End Tests

```bash
# Start all services
docker-compose up -d

# Run E2E tests
pytest tests/e2e/ -v
```

---

## 📝 Code Style

### Python

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

### TypeScript/JavaScript

```bash
# Format code
prettier --write "**/*.{ts,tsx,js,jsx}"

# Lint code
eslint "**/*.{ts,tsx,js,jsx}"
```

---

## 🔍 Debugging

### Python Debugging

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use debugger
from IPython import embed; embed()
```

### Docker Debugging

```bash
# Enter container
docker-compose exec codeguardians-gateway bash

# Check environment variables
docker-compose exec codeguardians-gateway env

# Check logs
docker-compose logs codeguardians-gateway | grep ERROR
```

---

## 📚 Project Structure

```
AbeOne_Master/
├── codeguardians-gateway/     # Gateway service
│   └── codeguardians-gateway/
│       ├── app/               # Application code
│       ├── tests/             # Tests
│       └── requirements.txt  # Dependencies
├── guards/                    # Guard services
│   ├── tokenguard/
│   ├── trust-guard/
│   ├── contextguard/
│   ├── biasguard-backend/
│   └── healthguard/
├── scripts/                   # Utility scripts
│   ├── read_abekeys.py       # AbëKEYS reader
│   └── unlock_all_credentials.py
├── docker-compose.yml         # Docker Compose config
└── README.md                  # Main README
```

---

## 🚨 Common Issues

### Credentials Not Loading

```bash
# Check AbëKEYS vault exists
ls -la ~/.abekeys/credentials/

# Verify credentials
python3 scripts/read_abekeys.py

# Check permissions
chmod 600 ~/.abekeys/credentials/*.json
```

### Services Not Starting

```bash
# Check Docker is running
docker ps

# Check logs
docker-compose logs

# Rebuild services
docker-compose build --no-cache
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

---

## 📖 Related Documentation

- **AbëKEYS:** [AbëKEYS_README.md](AbëKEYS_README.md)
- **Services:** [SERVICES_README.md](SERVICES_README.md)
- **Installation:** [INSTALL_README.md](INSTALL_README.md)
- **Gateway Docs:** `codeguardians-gateway/codeguardians-gateway/README.md`

---

**Pattern:** DEVELOPERS × SETUP × WORKFLOW × ONE  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

