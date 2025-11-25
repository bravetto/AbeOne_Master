# Domain Configuration Guide

## Overview

This guide covers domain configuration for the AI Guardians platform, including production deployment, SSL certificates, and DNS setup.

## Prerequisites

- Domain name registered
- DNS management access
- SSL certificate (Let's Encrypt recommended)
- Production server with Docker

## Domain Setup

### 1. DNS Configuration

#### A Records
```
# Main API domain
api.aiguardian.ai    A    <server-ip>

# Web application domain
app.aiguardian.ai    A    <server-ip>

# Documentation domain
docs.aiguardian.ai   A    <server-ip>

# Status page domain
status.aiguardian.ai A    <server-ip>
```

#### CNAME Records
```
# WWW redirects
www.aiguardian.ai    CNAME    aiguardian.ai
www.api.aiguardian.ai CNAME   api.aiguardian.ai
```

#### MX Records (if using email)
```
aiguardian.ai    MX    10    mail.aiguardian.ai
aiguardian.ai    MX    20    mail2.aiguardian.ai
```

### 2. SSL Certificate Setup

#### Let's Encrypt with Certbot
```bash
# Install Certbot
sudo apt update
sudo apt install certbot

# Get certificate for API domain
sudo certbot certonly --standalone -d api.aiguardian.ai

# Get certificate for web domain
sudo certbot certonly --standalone -d app.aiguardian.ai

# Get wildcard certificate
sudo certbot certonly --manual --preferred-challenges dns -d "*.aiguardian.ai"
```

#### Certificate Files Location
```
/etc/letsencrypt/live/api.aiguardian.ai/
 fullchain.pem
 privkey.pem
 chain.pem
 cert.pem
```

### 3. Nginx Configuration

#### Main Configuration
```nginx
# /etc/nginx/sites-available/aiguardian
upstream api_backend {
    server 127.0.0.1:8000;
}

upstream app_backend {
    server 127.0.0.1:3000;
}

# API Server
server {
    listen 80;
    server_name api.aiguardian.ai;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.aiguardian.ai;

    ssl_certificate /etc/letsencrypt/live/api.aiguardian.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.aiguardian.ai/privkey.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # API Routes
    location / {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS Headers
        add_header Access-Control-Allow-Origin "https://app.aiguardian.ai" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-API-Key" always;
        
        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin "https://app.aiguardian.ai";
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-API-Key";
            add_header Access-Control-Max-Age 1728000;
            add_header Content-Type "text/plain; charset=utf-8";
            add_header Content-Length 0;
            return 204;
        }
    }

    # Health Check
    location /health {
        proxy_pass http://api_backend;
        access_log off;
    }

    # Metrics (restricted)
    location /metrics {
        allow 127.0.0.1;
        allow 10.0.0.0/8;
        deny all;
        proxy_pass http://api_backend;
    }
}

# Web Application
server {
    listen 80;
    server_name app.aiguardian.ai;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name app.aiguardian.ai;

    ssl_certificate /etc/letsencrypt/live/app.aiguardian.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.aiguardian.ai/privkey.pem;

    # Same SSL configuration as API server

    location / {
        proxy_pass http://app_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Enable Configuration
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/aiguardian /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### 4. Docker Compose Production

#### Production Configuration
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  gateway:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=REPLACE_MEpostgres:5432/aiguardian_db
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - API_KEYS=${API_KEYS}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=aiguardian_db
      - POSTGRES_USER=aiguardian
      - POSTGRES_REPLACE_ME
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U aiguardian -d aiguardian_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  postgres_data:
  redis_data:
```

### 5. Environment Variables

#### Production Environment
```bash
# .env.prod
ENVIRONMENT=production
DATABASE_URL=REPLACE_MEpostgres:5432/aiguardian_db
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here
API_KEYS=key1,key2,key3
DB_REPLACE_ME

# SSL Configuration
SSL_CERT_PATH=/etc/letsencrypt/live/api.aiguardian.ai/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/api.aiguardian.ai/privkey.pem

# Monitoring
PROMETHEUS_ENABLED=true
JAEGER_ENABLED=true
LOG_LEVEL=INFO
```

### 6. SSL Certificate Renewal

#### Automatic Renewal
```bash
# Create renewal script
sudo nano /etc/cron.d/certbot-renew

# Add cron job
0 12 * * * root certbot renew --quiet --post-hook "systemctl reload nginx"
```

#### Manual Renewal
```bash
# Check certificate status
sudo certbot certificates

# Renew certificates
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

### 7. Monitoring and Logging

#### Nginx Logs
```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log

# Log rotation
sudo nano /etc/logrotate.d/nginx
```

#### Application Logs
```bash
# Docker logs
docker-compose logs -f gateway

# Log files
tail -f /var/log/aiguardian/app.log
```

### 8. Security Configuration

#### Firewall Setup
```bash
# UFW configuration
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Check status
sudo ufw status
```

#### Fail2Ban Configuration
```bash
# Install Fail2Ban
sudo apt install fail2ban

# Configure for Nginx
sudo nano /etc/fail2ban/jail.local

[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
```

### 9. Performance Optimization

#### Nginx Optimization
```nginx
# In nginx.conf
worker_processes auto;
worker_connections 1024;

http {
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Caching
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
}
```

#### Docker Optimization
```yaml
# Resource limits
services:
  gateway:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### 10. Backup and Recovery

#### Database Backup
```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U aiguardian -d aiguardian_db | gzip > "$BACKUP_DIR/db_backup_$DATE.sql.gz"
find "$BACKUP_DIR" -name "db_backup_*.sql.gz" -mtime +7 -delete
```

#### SSL Certificate Backup
```bash
# Backup certificates
sudo cp -r /etc/letsencrypt /backups/ssl/
```

### 11. Troubleshooting

#### Common Issues

**SSL Certificate Errors:**
```bash
# Check certificate
openssl x509 -in /etc/letsencrypt/live/api.aiguardian.ai/fullchain.pem -text -noout

# Test SSL
openssl s_client -connect api.aiguardian.ai:443 -servername api.aiguardian.ai
```

**DNS Resolution Issues:**
```bash
# Check DNS
nslookup api.aiguardian.ai
dig api.aiguardian.ai

# Check from different locations
curl -I https://api.aiguardian.ai/health
```

**Nginx Configuration Issues:**
```bash
# Test configuration
sudo nginx -t

# Check syntax
sudo nginx -T

# Reload configuration
sudo systemctl reload nginx
```

### 12. Maintenance

#### Regular Tasks
```bash
# Update system
sudo apt update && sudo apt upgrade

# Update Docker images
docker-compose pull
docker-compose up -d

# Clean up
docker system prune -a
```

#### Monitoring
```bash
# Check service status
systemctl status nginx
docker-compose ps

# Check resource usage
htop
docker stats

# Check logs
journalctl -u nginx
docker-compose logs
```

## Getting Help

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Discord Community](https://discord.gg/aiguardian)
- [GitHub Issues](https://github.com/bravetto/AI-Guardians/issues)

