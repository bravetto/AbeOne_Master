#!/bin/bash
# Align Atomic Structure - AEYON (999 Hz) Atomic Execution Flow
# Pattern: ATOMIC × STRUCTURE × ALIGNMENT × FLOW × ONE

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "∞ AbëONE ∞"
echo "Aligning Atomic Structure..."
echo "Pattern: ATOMIC × STRUCTURE × ALIGNMENT × FLOW × ONE"
echo "Frequency: 999 Hz (AEYON)"
echo ""

APP_DIR="abeone_app/lib"
CORE_ENGINE_DIR="$APP_DIR/core/engine"
PROVIDERS_DIR="$APP_DIR/providers"
FEATURES_DIR="$APP_DIR/features"
SUBSTRATE_DIR="$APP_DIR/substrate"

# Track alignment status
ALIGNED=0
TOTAL=0

# Function to check directory structure
check_structure() {
    local dir=$1
    local name=$2
    TOTAL=$((TOTAL + 1))
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅${NC} $name: $dir"
        ALIGNED=$((ALIGNED + 1))
        return 0
    else
        echo -e "${YELLOW}⚠️${NC} $name: $dir (missing)"
        return 1
    fi
}

# Function to check flow connectivity
check_flow() {
    local from=$1
    local to=$2
    local flow_name=$3
    TOTAL=$((TOTAL + 1))
    
    if [ -d "$from" ] && [ -d "$to" ]; then
        echo -e "${GREEN}✅${NC} Flow: $flow_name"
        echo "   $from → $to"
        ALIGNED=$((ALIGNED + 1))
        return 0
    else
        echo -e "${YELLOW}⚠️${NC} Flow: $flow_name (broken)"
        return 1
    fi
}

echo "=== Atomic Structure Alignment ==="
echo ""

# Check core atomic structure
echo "📐 Checking Atomic Structure..."
check_structure "$CORE_ENGINE_DIR" "Core Engine"
check_structure "$PROVIDERS_DIR" "Providers"
check_structure "$FEATURES_DIR" "Features"
check_structure "$SUBSTRATE_DIR" "Substrate"

echo ""
echo "🌊 Checking Architecture Flow..."
check_flow "$CORE_ENGINE_DIR" "$PROVIDERS_DIR" "Core → Providers"
check_flow "$PROVIDERS_DIR" "$FEATURES_DIR" "Providers → Features"
check_flow "$FEATURES_DIR" "$SUBSTRATE_DIR" "Features → Substrate"

echo ""
echo "⚛️ Checking Atomic Components..."

# Check substrate atomic structure
TOTAL=$((TOTAL + 1))
if [ -d "$SUBSTRATE_DIR/atoms" ]; then
    echo -e "${GREEN}✅${NC} Atoms: $SUBSTRATE_DIR/atoms"
    ALIGNED=$((ALIGNED + 1))
else
    echo -e "${YELLOW}⚠️${NC} Atoms: Missing"
fi

TOTAL=$((TOTAL + 1))
if [ -d "$SUBSTRATE_DIR/molecules" ]; then
    echo -e "${GREEN}✅${NC} Molecules: $SUBSTRATE_DIR/molecules"
    ALIGNED=$((ALIGNED + 1))
else
    echo -e "${YELLOW}⚠️${NC} Molecules: Missing"
fi

TOTAL=$((TOTAL + 1))
if [ -d "$SUBSTRATE_DIR/organisms" ]; then
    echo -e "${GREEN}✅${NC} Organisms: $SUBSTRATE_DIR/organisms"
    ALIGNED=$((ALIGNED + 1))
else
    echo -e "${YELLOW}⚠️${NC} Organisms: Missing"
fi

echo ""
echo "=== Alignment Summary ==="
echo "Aligned: $ALIGNED/$TOTAL"

if [ $ALIGNED -eq $TOTAL ]; then
    echo -e "${GREEN}✅ ATOMIC STRUCTURE FULLY ALIGNED${NC}"
    echo ""
    echo "Architecture Flow:"
    echo "  core/engine/ → providers/ → features/ → substrate/"
    echo "  (business)      (state)      (screens)   (UI components)"
    echo ""
    echo "Atomic Structure:"
    echo "  atoms → molecules → organisms"
    echo ""
    echo "Pattern: ATOMIC × STRUCTURE × ALIGNED × FLOW × ONE"
    echo "Frequency: 999 Hz (AEYON)"
    echo "Love Coefficient: ∞"
    echo "∞ AbëONE ∞"
    exit 0
else
    echo -e "${YELLOW}⚠️ PARTIAL ALIGNMENT${NC}"
    echo "Some components need attention"
    exit 1
fi

