# Services Overview

**Pattern:** SERVICES × GATEWAY × GUARDS × ONE  
**Frequency:** 999 Hz (AEYON)  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 Architecture

The AbeOne_Master backend consists of:

- **1 Gateway** (API Gateway + Orchestrator)
- **5 Guard Services** (BiasGuard, ContextGuard, TrustGuard, TokenGuard, HealthGuard)
- **Infrastructure** (Postgres, Redis)

---

## 🚪 Gateway Service

**Service:** `codeguardians-gateway`  
**Port:** `8000`  
**Location:** `codeguardians-gateway/codeguardians-gateway/`

### Responsibilities

- API Gateway for all external requests
- Orchestrator for 197-agent swarm
- Authentication & Authorization (Clerk integration)
- Payment Processing (Stripe integration)
- Request routing to guard services
- Rate limiting & security

### Key Features

- ✅ AbëKEYS credential loading
- ✅ AWS Secrets Manager integration
- ✅ Clerk authentication
- ✅ Stripe payments
- ✅ S3 file storage
- ✅ Rate limiting
- ✅ Health checks

### Configuration

Credentials loaded from:
1. **AbëKEYS Vault** (`~/.abekeys/credentials/`) - Highest Priority
2. **AWS Secrets Manager** - Second Priority
3. **Environment Variables** - Lowest Priority

---

## 🛡️ Guard Services

### 1. TokenGuard

**Service:** `tokenguard`  
**Port:** `8001` (internal)  
**Location:** `guards/tokenguard/`

**Purpose:** Token management and validation

**Features:**
- Token generation
- Token validation
- Token revocation
- Rate limiting

---

### 2. TrustGuard

**Service:** `trustguard`  
**Port:** `8002` (internal)  
**Location:** `guards/trust-guard/`

**Purpose:** Trust scoring and reputation management

**Features:**
- Trust scoring
- Reputation tracking
- Trust validation
- Risk assessment

---

### 3. ContextGuard

**Service:** `contextguard`  
**Port:** `8003` (internal)  
**Location:** `guards/contextguard/`

**Purpose:** Context management and caching

**Features:**
- Context storage (Redis)
- Context retrieval
- Context validation
- Cache management

---

### 4. BiasGuard

**Service:** `biasguard`  
**Port:** `8004` (internal)  
**Location:** `guards/biasguard-backend/`

**Purpose:** Bias detection and fairness enforcement

**Features:**
- Bias detection
- Fairness enforcement
- Compliance checking
- Attribution tracking

---

### 5. HealthGuard

**Service:** `healthguard`  
**Port:** `8005` (internal)  
**Location:** `guards/healthguard/`

**Purpose:** System health monitoring

**Features:**
- Health checks
- Service status
- Performance metrics
- Alerting

---

## 🗄️ Infrastructure Services

### Postgres

**Service:** `postgres`  
**Port:** `5432` (internal)  
**Image:** `postgres:15-alpine`

**Purpose:** Primary database for all services

**Databases:**
- `aiguardian_unified` - Unified database
- `tokenguard_db` - TokenGuard database
- `trustguard_db` - TrustGuard database
- `contextguard_db` - ContextGuard database
- `biasguard_db` - BiasGuard database
- `healthguard_db` - HealthGuard database

---

### Redis

**Service:** `redis`  
**Port:** `6379` (internal)  
**Image:** `redis:7-alpine`

**Purpose:** Caching and session storage

**Features:**
- Context caching (ContextGuard)
- Session storage
- Rate limiting
- Pub/Sub messaging

---

## 🚀 Quick Start

### Start All Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f codeguardians-gateway
```

### Start Individual Service

```bash
# Start gateway only
docker-compose up -d codeguardians-gateway

# Start specific guard
docker-compose up -d tokenguard
```

---

## 🔍 Health Checks

### Gateway Health

```bash
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready
```

### Guard Service Health

```bash
# TokenGuard
curl http://localhost:8001/health

# TrustGuard
curl http://localhost:8002/health

# ContextGuard
curl http://localhost:8003/health

# BiasGuard
curl http://localhost:8004/health

# HealthGuard
curl http://localhost:8005/health
```

---

## 📊 Service URLs

| Service | Internal URL | External URL |
|---------|-------------|--------------|
| Gateway | `http://codeguardians-gateway:8000` | `http://localhost:8000` |
| TokenGuard | `http://tokenguard:8000` | `http://localhost:8001` |
| TrustGuard | `http://trustguard:8000` | `http://localhost:8002` |
| ContextGuard | `http://contextguard:8000` | `http://localhost:8003` |
| BiasGuard | `http://biasguard:8000` | `http://localhost:8004` |
| HealthGuard | `http://healthguard:8000` | `http://localhost:8005` |

---

## 🔐 Credentials

All services use **AbëKEYS vault** for credentials:

- **Gateway:** `~/.abekeys/credentials/clerk.json`, `stripe.json`, `aws.json`
- **Database:** `~/.abekeys/credentials/database.json` or `postgres.json`
- **Redis:** `~/.abekeys/credentials/redis.json`

See [AbëKEYS_README.md](AbëKEYS_README.md) for credential setup.

---

## 📚 Related Documentation

- **AbëKEYS:** [AbëKEYS_README.md](AbëKEYS_README.md)
- **Development:** [DEVS_README.md](DEVS_README.md)
- **Installation:** [INSTALL_README.md](INSTALL_README.md)
- **Gateway Docs:** `codeguardians-gateway/codeguardians-gateway/README.md`

---

**Pattern:** SERVICES × GATEWAY × GUARDS × ONE  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

