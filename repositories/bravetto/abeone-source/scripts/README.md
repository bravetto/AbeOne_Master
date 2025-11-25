# AIGuards Backend - Scripts Directory

This directory contains consolidated deployment, testing, and utility scripts for the AIGuards Backend project.

##  Table of Contents

- [Deployment Scripts](#deployment-scripts)
- [Testing Scripts](#testing-scripts)
- [Utility Scripts](#utility-scripts)
- [Quick Start](#quick-start)

##  Deployment Scripts

**Note:** Deployment is handled by DevOps. Use `docker-compose` commands for local development.

### push-to-ecr.ps1

Push Docker images to AWS ECR (Elastic Container Registry).

**Usage:**

```powershell
# Push latest tag
.\scripts\push-to-ecr.ps1

# Push specific tag
.\scripts\push-to-ecr.ps1 -Tag v1.0.0

# Push to specific region
.\scripts\push-to-ecr.ps1 -Tag v1.0.0 -Region us-west-2

# Specify account ID
.\scripts\push-to-ecr.ps1 -AccountId 123456789012 -Tag latest
```

**Features:**

- Automatically builds image if not found locally
- Creates ECR repository if it doesn't exist
- Authenticates with AWS ECR
- Verifies successful push
- Lists all available tags in ECR

##  Utility Scripts

### Database & Data Management

#### check_db.py
Database connectivity and health check utility.

```bash
# Check database connection
python scripts/check_db.py

# Validate database schema
python scripts/check_db.py --schema
```

#### create_posts_table.py
Database table creation and migration script for posts functionality.

```bash
# Create posts table
python scripts/create_posts_table.py

# Run with verbose output
python scripts/create_posts_table.py --verbose
```

#### deduplicate.py
Data deduplication utility for cleaning up duplicate records.

```bash
# Analyze duplicates
python scripts/deduplicate.py --analyze

# Remove duplicates (dry run)
python scripts/deduplicate.py --dry-run

# Remove duplicates (production)
python scripts/deduplicate.py --confirm
```

##  Testing Scripts

### test-suite.py

Consolidated test suite for all system components.

**Usage:**

```bash
# Run all tests
python scripts/test-suite.py

# Run quick smoke tests
python scripts/test-suite.py --quick

# Test guard services only
python scripts/test-suite.py --guards

# Test infrastructure only
python scripts/test-suite.py --infra

# Run end-to-end tests
python scripts/test-suite.py --e2e

# Test against different URL
python scripts/test-suite.py --url http://staging.example.com
```

**Test Categories:**

1. **Gateway Health Tests**
   - Live check
   - Ready check

2. **Service Discovery Tests**
   - Available services
   - Service status

3. **Guard Services Tests**
   - TokenGuard processing
   - TrustGuard processing
   - ContextGuard processing
   - BiasGuard processing
   - HealthGuard processing

4. **Infrastructure Tests**
   - Database connectivity
   - Redis connectivity
   - Service dependencies

**Output:**

The test suite provides colored output with:
-  PASS - Test passed
-  FAIL - Test failed
- Summary statistics
- Failed test details

##  Utility Scripts

### update-guards.sh / update-guards.ps1

Update all guard service submodules to their latest versions.

**Usage:**

```bash
# Bash
./scripts/update-guards.sh

# PowerShell
.\scripts\update-guards.ps1
```

**What it does:**

- Updates TokenGuard submodule
- Updates TrustGuard submodule
- Updates ContextGuard submodule
- Updates BiasGuard submodule
- Updates HealthGuard submodule
- Shows final submodule status

##  Quick Start

### Local Development

```bash
# 1. Start development environment
docker-compose up -d

# 2. Run quick tests
python scripts/test-suite.py --quick

# 3. View logs
docker-compose logs -f

# 4. Stop when done
docker-compose down
```

### Production Deployment

**Note:** Production deployment is handled by DevOps. For local testing:

```bash
# 1. Configure environment
cp codeguardians-gateway/codeguardians-gateway/env.unified.template \
   codeguardians-gateway/codeguardians-gateway/env.unified

# Edit env.unified with production values

# 2. Start services
docker-compose up -d

# 3. Run full test suite
python scripts/test-suite.py --e2e

# 4. Monitor logs
docker-compose logs -f
```

### AWS ECS Deployment

**Note:** AWS deployment is handled by DevOps. For local ECR push:

```bash
# 1. Configure AWS credentials
aws configure

# 2. Build and push to ECR (Windows)
.\scripts\push-to-ecr.ps1 -Tag dev

# 3. Verify deployment (after DevOps deployment)
python scripts/test-suite.py --url https://your-alb-endpoint.com
```

##  Additional Resources

- [Main README](../README.md)
- [Quickstart Guide](../codeguardians-gateway/codeguardians-gateway/QUICKSTART.md)
- [DevOps Guide](../DEVOPS_GUIDE.md)
- [Developer Guide](../DEVELOPER_GUIDE.md)
- [Troubleshooting](../TROUBLESHOOTING.md)

##  Tips

1. **Use docker-compose for local development** - `docker-compose up -d` starts all services
2. **Check logs if deployment fails** - Use `docker-compose logs -f`
3. **Run quick tests first** - Saves time during development
4. **Keep submodules updated** - Run `./scripts/update-guards.sh` regularly
5. **Use environment variables** - Don't hard-code configuration
6. **For production deployment** - Contact DevOps team

##  Contributing

When adding new scripts:

1. Add them to this directory
2. Follow the naming convention: `verb-noun.sh` or `verb-noun.ps1`
3. Include comprehensive help messages
4. Update this README
5. Add error handling and logging
6. Support both Bash and PowerShell when applicable

##  License

See [LICENSE](../LICENSE) file in the root directory.
