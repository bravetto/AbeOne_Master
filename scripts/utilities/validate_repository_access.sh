#!/bin/bash
# AbëFLOWs Repository Access Validation
# Epistemically Proven Validation Patterns
# IS SOURCE × CLEAR × EASY

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validation function
validate_repo() {
    local repo_url=$1
    local repo_name=$2
    
    echo -e "${BLUE}Validating: ${repo_name}${NC}"
    
    # Epistemic Proof 1: Repository exists
    if git ls-remote "$repo_url" &>/dev/null; then
        echo -e "${GREEN} EXISTS: ${repo_name}${NC}"
    else
        echo -e "${RED} NOT FOUND: ${repo_name}${NC}"
        return 1
    fi
    
    # Epistemic Proof 2: Repository is accessible
    local clone_test=$(git ls-remote "$repo_url" HEAD 2>&1)
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN} ACCESSIBLE: ${repo_name}${NC}"
    else
        echo -e "${RED} NOT ACCESSIBLE: ${repo_name}${NC}"
        return 1
    fi
    
    # Epistemic Proof 3: Repository has content
    local branch_count=$(git ls-remote --heads "$repo_url" | wc -l | tr -d ' ')
    if [[ $branch_count -gt 0 ]]; then
        echo -e "${GREEN} HAS CONTENT: ${repo_name} (${branch_count} branches)${NC}"
    else
        echo -e "${YELLOW}  NO BRANCHES: ${repo_name}${NC}"
    fi
    
    return 0
}

echo "=========================================="
echo "AbëFLOWs Repository Access Validation"
echo "Epistemically Proven Validation Patterns"
echo "=========================================="
echo ""

# Source 1: @Jimmy-Dejesus
echo "=== SOURCE 1: @Jimmy-Dejesus ==="
validate_repo "https://github.com/Jimmy-Dejesus/aiagentsuite.git" "aiagentsuite"

# Source 2: @bravetto
echo ""
echo "=== SOURCE 2: @bravetto ==="
validate_repo "https://github.com/bravetto/bias-detect.git" "bias-detect"
validate_repo "https://github.com/bravetto/biasguards.ai.git" "biasguards.ai"
validate_repo "https://github.com/bravetto/bridge.git" "bridge"
validate_repo "https://github.com/bravetto/bravetto-recruitment-platform.git" "bravetto-recruitment-platform"
validate_repo "https://github.com/bravetto/spike-transformer.git" "spike-transformer"

# Source 3: @BravettoBackendTeam (requires authentication)
echo ""
echo "=== SOURCE 3: @BravettoBackendTeam ==="
if command -v gh &> /dev/null; then
    if gh auth status &>/dev/null; then
        echo -e "${GREEN} AUTHENTICATED: GitHub CLI${NC}"
        echo "  → Listing repositories..."
        gh repo list BravettoBackendTeam 2>/dev/null || echo -e "${YELLOW}  No access or no repositories${NC}"
    else
        echo -e "${YELLOW}  NOT AUTHENTICATED: Run 'gh auth login'${NC}"
    fi
else
    echo -e "${YELLOW}  GitHub CLI not installed: Install with 'brew install gh'${NC}"
fi

echo ""
echo "=========================================="
echo "=== VALIDATION COMPLETE ==="
echo "=========================================="

