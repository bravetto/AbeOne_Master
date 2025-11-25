# Unified Makefile for CodeGuardians Gateway
# Single Docker Compose file with environment-based configuration

.PHONY: help dev prod test clean logs shell health metrics config

# Default target
help:
	@echo "CodeGuardians Gateway - Unified Commands:"
	@echo ""
	@echo "Environment Management:"
	@echo "  dev              Start development environment"
	@echo "  prod             Start production environment"
	@echo "  test             Start test environment"
	@echo ""
	@echo "Service Management:"
	@echo "  up               Start services (uses ENVIRONMENT variable)"
	@echo "  down             Stop all services"
	@echo "  restart          Restart services"
	@echo "  logs             View logs"
	@echo "  shell            Open shell in main container"
	@echo ""
	@echo "Profiles:"
	@echo "  worker           Start with Celery worker and beat"
	@echo "  nginx            Start with Nginx reverse proxy"
	@echo "  aws-test         Start with AWS testing tools"
	@echo "  email-test       Start with Mailhog for email testing"
	@echo "  monitoring      Start with monitoring stack"
	@echo ""
	@echo "Configuration:"
	@echo "  config-reload    Reload dynamic configuration"
	@echo "  config-status    Check configuration status"
	@echo "  rate-limits      Get current rate limits"
	@echo ""
	@echo "Utilities:"
	@echo "  clean            Clean up containers and volumes"
	@echo "  health           Check service health"
	@echo "  metrics          View metrics"

# Environment Management
dev:
	@echo "Starting development environment..."
	@ENVIRONMENT=development DOCKER_TARGET=development SOURCE_MOUNT=. MOUNT_MODE=rw DEBUG=true RELOAD=true docker-compose up -d
	@echo "Development environment started!"
	@echo "Gateway: http://localhost:8000"
	@echo "Debug port: 5678"

prod:
	@echo "Starting production environment..."
	@ENVIRONMENT=production DOCKER_TARGET=production READ_ONLY=true DEBUG=false RELOAD=false docker-compose up -d
	@echo "Production environment started!"
	@echo "Gateway: http://localhost:8000"

test:
	@echo "Starting test environment..."
	@ENVIRONMENT=test DOCKER_TARGET=development docker-compose --profile testing up -d
	@echo "Test environment started!"

# Service Management
up:
	@echo "Starting services with current environment..."
	@docker-compose up -d
	@echo "Services started!"

down:
	@echo "Stopping all services..."
	@docker-compose down
	@echo "Services stopped!"

restart: down up

logs:
	@echo "Viewing logs..."
	@docker-compose logs -f

shell:
	@echo "Opening shell in main container..."
	@docker-compose exec codeguardians-gateway-${ENVIRONMENT:-production} bash

# Profiles
worker:
	@echo "Starting with Celery worker and beat..."
	@docker-compose --profile worker up -d
	@echo "Worker services started!"

nginx:
	@echo "Starting with Nginx reverse proxy..."
	@docker-compose --profile nginx up -d
	@echo "Nginx started!"

aws-test:
	@echo "Starting with AWS testing tools..."
	@docker-compose --profile aws-testing up -d
	@echo "AWS testing tools started!"

email-test:
	@echo "Starting with Mailhog for email testing..."
	@docker-compose --profile email-testing up -d
	@echo "Email testing tools started!"

monitoring:
	@echo "Starting monitoring stack..."
	@docker-compose --profile worker --profile nginx up -d
	@echo "Monitoring stack started!"

# Configuration Management
config-reload:
	@echo "Reloading dynamic configuration..."
	@curl -X POST http://localhost:8000/api/v1/config/reload \
		-H "Authorization: Bearer $(shell cat .env 2>/dev/null | grep ADMIN_TOKEN | cut -d'=' -f2 || echo 'your-token')"

config-status:
	@echo "Checking configuration status..."
	@curl -X GET http://localhost:8000/api/v1/config/status \
		-H "Authorization: Bearer $(shell cat .env 2>/dev/null | grep ADMIN_TOKEN | cut -d'=' -f2 || echo 'your-token')"

rate-limits:
	@echo "Getting current rate limits..."
	@curl -X GET http://localhost:8000/api/v1/config/rate-limits \
		-H "Authorization: Bearer $(shell cat .env 2>/dev/null | grep ADMIN_TOKEN | cut -d'=' -f2 || echo 'your-token')"

# Utilities
clean:
	@echo "Cleaning up containers and volumes..."
	@docker-compose down -v --remove-orphans
	@docker system prune -f
	@echo "Cleanup complete!"

health:
	@echo "Checking service health..."
	@echo "Gateway Health:"
	@curl -f http://localhost:8000/health/live || echo "Gateway not responding"
	@echo ""
	@echo "Database Health:"
	@docker-compose exec postgres pg_isready -U codeguardians-gateway || echo "Database not responding"
	@echo ""
	@echo "Redis Health:"
	@docker-compose exec redis redis-cli ping || echo "Redis not responding"

metrics:
	@echo "Viewing metrics..."
	@curl http://localhost:8000/metrics

# Quick Commands
status: health
ps:
	@docker-compose ps