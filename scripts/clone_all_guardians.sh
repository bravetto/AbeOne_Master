#!/bin/bash
# Clone All Guardian Services from Bravetto Repos
# Atomic Guardians Preparation - Perfect Intelligence & Guardian Integration

set -e

BASE_DIR="${1:-./AIGuards-Backend/aiguardian-repos}"
mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=========================================="
echo " ATOMIC GUARDIANS CLONING"
echo "Base Directory: $BASE_DIR"
echo "=========================================="
echo ""

# Guardian Services (8)
echo -e "${BLUE} Cloning Guardian Services...${NC}"

GUARDIAN_SERVICES=(
    "guardian-zero-service"
    "guardian-aeyon-service"
    "guardian-abe-service"
    "guardian-john-service"
    "guardian-lux-service"
    "guardian-neuro-service"
    "guardian-yagni-service"
    "guardian-jimmy-service"
    "guardian-aurion-service"
)

for repo in "${GUARDIAN_SERVICES[@]}"; do
    if [ ! -d "$repo" ]; then
        echo "  → Cloning $repo..."
        if git clone "https://github.com/bravetto/${repo}.git" 2>&1; then
            echo -e "${GREEN}   $repo cloned${NC}"
        else
            echo -e "${YELLOW}    Failed to clone $repo (may be private or not exist)${NC}"
        fi
    else
        echo -e "${GREEN}   $repo already exists${NC}"
    fi
done

echo ""
echo -e "${BLUE} Cloning Guard Services...${NC}"

# Guard Services (5)
GUARD_SERVICES=(
    "guard-bias-service"
    "guard-context-service"
    "guard-trust-service"
    "guard-security-service"
    "guard-neuromorphic-service"
)

for repo in "${GUARD_SERVICES[@]}"; do
    if [ ! -d "$repo" ]; then
        echo "  → Cloning $repo..."
        if git clone "https://github.com/bravetto/${repo}.git" 2>&1; then
            echo -e "${GREEN}   $repo cloned${NC}"
        else
            echo -e "${YELLOW}    Failed to clone $repo (may be private or not exist)${NC}"
        fi
    else
        echo -e "${GREEN}   $repo already exists${NC}"
    fi
done

echo ""
echo -e "${BLUE} Cloning Orchestration Services...${NC}"

# Orchestration
ORCHESTRATION_SERVICES=(
    "swarm-orchestrator"
    "REPLACE_ME"
)

for repo in "${ORCHESTRATION_SERVICES[@]}"; do
    if [ ! -d "$repo" ]; then
        echo "  → Cloning $repo..."
        if git clone "https://github.com/bravetto/${repo}.git" 2>&1; then
            echo -e "${GREEN}   $repo cloned${NC}"
        else
            echo -e "${YELLOW}    Failed to clone $repo (may be private or not exist)${NC}"
        fi
    else
        echo -e "${GREEN}   $repo already exists${NC}"
    fi
done

echo ""
echo "=========================================="
echo -e "${GREEN}=== CLONING COMPLETE ===${NC}"
echo "All repositories available in: $BASE_DIR"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Review cloned repositories"
echo "2. Create atomic guardian template (Ben's FastAPI patterns)"
echo "3. Build Terraform infrastructure (Danny's AWS/Linkerd patterns)"
echo "4. Convert guardians to atomic microservices"
echo ""
echo "See: ATOMIC_GUARDIANS_PREPARATION_PLAN.md for detailed plan"

