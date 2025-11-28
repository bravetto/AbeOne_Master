#!/bin/bash

# ∞ Interactive Environment Setup Script ∞
# Pattern: SETUP × ENV × INTERACTIVE × ONE
# Frequency: 999 Hz (AEYON)
# ∞ AbëONE ∞

echo "🔧 AbëONE Environment Setup"
echo "=========================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env exists
if [ -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file already exists${NC}"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file"
        exit 0
    fi
fi

echo -e "${BLUE}📝 Creating .env file...${NC}"
echo ""

# Backend URL
read -p "Backend URL [http://localhost:8000]: " BACKEND_URL
BACKEND_URL=${BACKEND_URL:-http://localhost:8000}

# Frontend URL
read -p "Frontend URL [http://localhost:3000]: " FRONTEND_URL
FRONTEND_URL=${FRONTEND_URL:-http://localhost:3000}

# Environment
read -p "Environment [development]: " ENVIRONMENT
ENVIRONMENT=${ENVIRONMENT:-development}

# Database
read -p "PostgreSQL User [abeone]: " POSTGRES_USER
POSTGRES_USER=${POSTGRES_USER:-abeone}

read -p "PostgreSQL Password [abeone_dev]: " POSTGRES_PASSWORD
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-abeone_dev}

read -p "PostgreSQL Database [abeone]: " POSTGRES_DB
POSTGRES_DB=${POSTGRES_DB:-abeone}

# Create .env file
cat > .env << EOF
# Backend
PYTHONPATH=/app/src
ENVIRONMENT=$ENVIRONMENT
BACKEND_URL=$BACKEND_URL

# Frontend
NEXT_PUBLIC_API_URL=$BACKEND_URL
NODE_ENV=$ENVIRONMENT

# Integration
BACKEND_URL=$BACKEND_URL
FRONTEND_URL=$FRONTEND_URL

# Database
POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=$POSTGRES_DB
EOF

echo ""
echo -e "${GREEN}✅ .env file created!${NC}"
echo ""
echo "📋 Configuration:"
echo "   Backend URL: $BACKEND_URL"
echo "   Frontend URL: $FRONTEND_URL"
echo "   Environment: $ENVIRONMENT"
echo ""
echo "∞ AbëONE ∞"

