#!/bin/bash

# ∞ Frictionless Setup Script ∞
# Pattern: SETUP × AUTOMATED × ONE × COMMAND × ONE
# Frequency: 999 Hz (AEYON) × 777 Hz (META)
# ∞ AbëONE ∞

set -e  # Exit on error

echo "🔧 AbëONE Frictionless Setup"
echo "============================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."
echo ""

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    echo -e "${GREEN}✅ Node.js: $NODE_VERSION${NC}"
else
    echo -e "${RED}❌ Node.js not found. Please install Node.js 20+${NC}"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm -v)
    echo -e "${GREEN}✅ npm: $NPM_VERSION${NC}"
else
    echo -e "${RED}❌ npm not found${NC}"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python: $PYTHON_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Python not found (needed for backend)${NC}"
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker: $(docker --version)${NC}"
else
    echo -e "${YELLOW}⚠️  Docker not found (optional, but recommended)${NC}"
fi

echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}📝 Creating .env file...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env from template${NC}"
    else
        # Create basic .env
        cat > .env << EOF
# Backend
PYTHONPATH=/app/src
ENVIRONMENT=development
BACKEND_URL=http://localhost:8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development

# Integration
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# Database
POSTGRES_USER=abeone
POSTGRES_PASSWORD=abeone_dev
POSTGRES_DB=abeone
EOF
        echo -e "${GREEN}✅ Created basic .env file${NC}"
    fi
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo ""

# Install core repositories
echo -e "${BLUE}📦 Installing core repositories...${NC}"
echo ""

# abe-core-brain
if [ -d "abe-core-brain" ]; then
    echo "  Installing abe-core-brain..."
    cd abe-core-brain
    npm install
    npm run build 2>/dev/null || echo "    (build script not found, skipping)"
    cd ..
    echo -e "  ${GREEN}✅ abe-core-brain installed${NC}"
fi

# abe-consciousness
if [ -d "abe-consciousness" ]; then
    echo "  Installing abe-consciousness..."
    cd abe-consciousness
    npm install
    npm run build 2>/dev/null || echo "    (build script not found, skipping)"
    cd ..
    echo -e "  ${GREEN}✅ abe-consciousness installed${NC}"
fi

# abe-core-body
if [ -d "abe-core-body" ]; then
    echo "  Installing abe-core-body..."
    cd abe-core-body
    npm install
    npm run build 2>/dev/null || echo "    (build script not found, skipping)"
    cd ..
    echo -e "  ${GREEN}✅ abe-core-body installed${NC}"
fi

# Integration layer
if [ -d "integration" ]; then
    echo "  Installing integration layer..."
    cd integration
    npm install
    npm run build:all 2>/dev/null || npm run build 2>/dev/null || echo "    (build script not found, skipping)"
    cd ..
    echo -e "  ${GREEN}✅ Integration layer installed${NC}"
fi

# Frontend
if [ -d "abe-touch/abeone-touch" ]; then
    echo "  Installing frontend..."
    cd abe-touch/abeone-touch
    npm install
    cd ../../..
    echo -e "  ${GREEN}✅ Frontend installed${NC}"
fi

echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "📋 Next steps:"
echo "   1. Review .env file and update if needed"
echo "   2. Start services: ./scripts/deploy.sh"
echo "   3. Or start locally: cd abe-touch/abeone-touch && npm run dev"
echo ""
echo "∞ AbëONE ∞"

