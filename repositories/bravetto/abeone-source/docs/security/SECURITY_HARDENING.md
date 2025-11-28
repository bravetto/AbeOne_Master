# Security Hardening Guide - AIGuards Backend

This document outlines the security improvements implemented to address identified security issues.

##  Security Issues Resolved

### 1.  Sensitive Environment Variables Management

**Issue**: Keys like `JWT_SECRET_KEY`, `SECRET_KEY`, `CLERK_SECRET_KEY`, and `TRUSTGUARD_API_KEY` were exposed in environment variables.

**Solution**:
- Created separate environment templates (`env.template`, `env.template.development`)
- All sensitive values marked with `CHANGE-ME-IN-PRODUCTION` placeholders
- AWS Secrets Manager integration for production deployments
- Comprehensive documentation on secure secret management

**Implementation**:
- Use `env.template.development` for local development
- Use `env.template` with AWS Secrets Manager for production
- Never commit `.env` files to version control

### 2.  Empty Environment Variables Validation

**Issue**: Variables such as `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` were empty.

**Solution**:
- Created validation script (`scripts/validate-env.sh`)
- Validates required variables based on enabled services
- Provides clear error messages for missing configurations
- Warns about placeholder values

**Usage**:
```bash
# Validate environment variables
./scripts/validate-env.sh
```

### 3.  Redis Password Security

**Issue**: Redis password was embedded in `REDIS_URL` in plain text.

**Solution**:
- Use separate `REDIS_PASSWORD` environment variable
- Construct `REDIS_URL` from components: `REPLACE_ME${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}`
- Password never hardcoded in URLs
- Redis healthcheck updated to use password authentication

**Implementation**:
```yaml
# Before (INSECURE):
REDIS_URL=REPLACE_MEhost:6379/0

# After (SECURE):
REDIS_REPLACE_ME
REDIS_URL=REPLACE_ME${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}
```

### 4.  Debug Mode Protection

**Issue**: `DEBUG` environment variable could be enabled in production.

**Solution**:
- Default `DEBUG=false` in docker-compose.yml
- Validation script checks `DEBUG=false` in production
- Clear warnings in environment templates
- Production profile defaults to `DEBUG=false`

### 5.  Port Exposure Restrictions

**Issue**: Ports like 5433 (Postgres), 6380 (Redis), and 8000 (application) were exposed publicly (0.0.0.0).

**Solution**:
- **Postgres**: Restricted to `127.0.0.1:5432` (localhost only)
- **Redis**: Restricted to `127.0.0.1:6379` (localhost only)
- **Monitoring Services**: Restricted to `127.0.0.1` (Grafana, Prometheus, Elasticsearch, Kibana)
- **Gateway**: Exposed on `0.0.0.0:8000` (required for external access)
- All guard services remain internal-only (no exposed ports)

**Network Security**:
- All services communicate via internal Docker network (`aiguards-network`)
- Only gateway is accessible from outside
- Database and Redis accessible only from localhost for development

### 6.  Database URL Security

**Issue**: Database URLs included credentials in plain text.

**Solution**:
- Use separate database connection variables (`DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD`)
- `DATABASE_URL` can be constructed from components or provided separately
- Credentials stored in AWS Secrets Manager for production
- Environment variables scoped per service

### 7.  Environment Variable Scoping

**Issue**: Too many environment variables shared across containers.

**Solution**:
- Scoped environment variables per service
- Each guard service receives only required variables
- Reduced attack surface by limiting exposed variables
- Clear separation of concerns

**Example**:
```yaml
# Gateway gets all variables
codeguardians-gateway:
  environment:
    - DATABASE_URL=${DATABASE_URL}
    - REDIS_URL=${REDIS_URL}
    - CLERK_SECRET_KEY=${CLERK_SECRET_KEY}
    # ... all gateway variables

# Guard services get only what they need
tokenguard:
  environment:
    - DATABASE_URL=${DATABASE_URL}
    - REDIS_URL=${REDIS_URL}
    - UNIFIED_API_KEY=${UNIFIED_API_KEY}
    # ... only guard-specific variables
```

### 8.  Redis Configuration Hardening

**Issue**: Redis configuration needed security improvements.

**Solution**:
- Password authentication required (`--requirepass`)
- Memory policy configured (`--maxmemory-policy allkeys-lru`)
- Password from environment variable (never hardcoded)
- Healthcheck updated to use password authentication

### 9.  Container State Monitoring

**Issue**: Trustguard container had stopped/restarted state concerns.

**Solution**:
- All containers configured with `restart: unless-stopped`
- Healthchecks added to all services
- Dependencies properly configured
- Monitoring services available for production

### 10.  Version Consistency

**Issue**: Version mismatches between configuration and runtime.

**Solution**:
- Single `VERSION` variable in docker-compose.yml
- Consistent version tagging across all services
- Version variable used for image tags

##  Security Checklist

### Pre-Deployment Checklist

- [ ] Run `./scripts/validate-env.sh` to validate all environment variables
- [ ] Ensure `DEBUG=false` for production
- [ ] All secrets marked with `CHANGE-ME-IN-PRODUCTION` are updated
- [ ] Redis password is set and not in URL
- [ ] Database credentials are secure
- [ ] AWS Secrets Manager configured for production
- [ ] Ports are restricted appropriately
- [ ] CORS origins are restricted to production domains
- [ ] Grafana password is changed from default
- [ ] All placeholder values are replaced

### Production Deployment Checklist

- [ ] AWS Secrets Manager contains all production secrets
- [ ] `AWS_SECRETS_ENABLED=true` in production
- [ ] IAM roles configured for ECS tasks (not access keys)
- [ ] Database uses encrypted connections (SSL/TLS)
- [ ] Redis uses password authentication
- [ ] Monitoring services behind reverse proxy with authentication
- [ ] Logging configured to exclude sensitive data
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Regular secret rotation scheduled

##  Secrets Management Best Practices

### Development Environment

1. Use `env.template.development` as starting point
2. Copy to `.env` and configure for local development
3. Use placeholder values for external services (Clerk, Stripe)
4. Never commit `.env` files to version control

### Production Environment

1. Use AWS Secrets Manager for all secrets
2. Set `AWS_SECRETS_ENABLED=true`
3. Use IAM roles instead of access keys when possible
4. Rotate secrets regularly (at least quarterly)
5. Use strong, randomly generated passwords (minimum 32 characters)
6. Enable encryption at rest for all secrets
7. Audit secret access regularly

##  Network Security

### Internal Services (No External Access)

-  All guard services (tokenguard, trustguard, contextguard, biasguard, healthguard)
-  Database (Postgres) - localhost only
-  Redis - localhost only
-  Monitoring services - localhost only

### External Services (Controlled Access)

-  Gateway (port 8000) - exposed for API access
-  Monitoring dashboards - behind reverse proxy with authentication

##  Monitoring and Alerting

### Security Monitoring

- Monitor failed authentication attempts
- Monitor unauthorized access attempts
- Monitor secret access patterns
- Alert on suspicious activity

### Container Health

- All containers have healthchecks
- Automatic restart on failure (`restart: unless-stopped`)
- Dependencies properly configured
- Monitoring services available for production

##  Incident Response

### If Secrets Are Compromised

1. **Immediately rotate all compromised secrets**
2. **Revoke access keys** if AWS credentials are compromised
3. **Review access logs** for unauthorized access
4. **Update all affected services** with new secrets
5. **Notify security team** and relevant stakeholders
6. **Document incident** for post-mortem analysis

### If Container Stops Unexpectedly

1. **Check container logs**: `docker-compose logs <service-name>`
2. **Check health status**: `docker-compose ps`
3. **Review resource usage**: `docker stats`
4. **Check dependencies**: Ensure required services are running
5. **Review configuration**: Validate environment variables

##  Additional Resources

- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)
- [Production Secrets Setup Guide](./COMPLETE_SECRETS_SETUP_GUIDE.md)

##  Maintenance

### Regular Security Tasks

- **Weekly**: Review access logs
- **Monthly**: Update dependencies
- **Quarterly**: Rotate secrets
- **Annually**: Security audit

### Continuous Improvement

- Monitor security advisories
- Update security configurations
- Review and update documentation
- Conduct security training

---

**Last Updated**: 2024-01-XX
**Version**: 1.0.0


