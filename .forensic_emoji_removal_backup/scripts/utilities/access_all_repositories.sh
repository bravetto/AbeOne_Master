#!/bin/bash
# AbëFLOWs Easy Repository Access
# IS SOURCE × CLEAR × EASY

set -e

BASE_DIR="${1:-./repositories}"
mkdir -p "$BASE_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "AbëFLOWs Repository Access"
echo "Base Directory: $BASE_DIR"
echo "=========================================="
echo ""

# Source 1: @Jimmy-Dejesus
echo -e "${BLUE}📦 Cloning @Jimmy-Dejesus repositories...${NC}"
cd "$BASE_DIR"
mkdir -p jimmy-dejesus
cd jimmy-dejesus

if [ ! -d "aiagentsuite" ]; then
    echo "  → Cloning aiagentsuite..."
    git clone https://github.com/Jimmy-Dejesus/aiagentsuite.git
    echo -e "${GREEN}  ✅ aiagentsuite cloned${NC}"
else
    echo -e "${GREEN}  ✓ aiagentsuite already exists${NC}"
fi

# Source 2: @bravetto
echo ""
echo -e "${BLUE}📦 Cloning @bravetto repositories...${NC}"
cd ..
mkdir -p bravetto
cd bravetto

repos=(
    "bias-detect"
    "biasguards.ai"
    "bridge"
    "bravetto-recruitment-platform"
    "spike-transformer"
)

for repo in "${repos[@]}"; do
    if [ ! -d "$repo" ]; then
        echo "  → Cloning $repo..."
        git clone "https://github.com/bravetto/${repo}.git" || echo -e "${YELLOW}  ⚠️  Failed to clone $repo${NC}"
        if [ -d "$repo" ]; then
            echo -e "${GREEN}  ✅ $repo cloned${NC}"
        fi
    else
        echo -e "${GREEN}  ✓ $repo already exists${NC}"
    fi
done

# Source 3: @BravettoBackendTeam
echo ""
echo -e "${BLUE}📦 Accessing @BravettoBackendTeam repositories...${NC}"
cd ..
mkdir -p bravetto-backend
cd bravetto-backend

if command -v gh &> /dev/null && gh auth status &>/dev/null; then
    echo "  → Listing repositories..."
    gh repo list BravettoBackendTeam --json name,url --jq '.[] | "\(.name)|\(.url)"' 2>/dev/null | while IFS='|' read -r name url; do
        if [ ! -z "$name" ] && [ ! -d "$name" ]; then
            echo "    → Cloning $name..."
            git clone "$url" || echo -e "${YELLOW}    ⚠️  Failed to clone $name${NC}"
            if [ -d "$name" ]; then
                echo -e "${GREEN}    ✅ $name cloned${NC}"
            fi
        elif [ ! -z "$name" ]; then
            echo -e "${GREEN}    ✓ $name already exists${NC}"
        fi
    done || echo -e "${YELLOW}  ⚠️  No repositories found or access denied${NC}"
else
    echo -e "${YELLOW}  ⚠️  Authentication required for private repositories${NC}"
    echo "  → Run: gh auth login"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}=== ACCESS COMPLETE ===${NC}"
echo "All repositories available in: $BASE_DIR"
echo "=========================================="

