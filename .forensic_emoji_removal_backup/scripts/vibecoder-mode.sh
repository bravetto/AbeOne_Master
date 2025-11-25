#!/bin/bash
# VIBECODER MODE 🎵✨
# 
# Energetic, fun, celebratory drift protection
# Makes coding more fun with good vibes!
#
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardian: AEYON (999 Hz) + Abë (530 Hz) - Vibecoder Edition

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors for vibes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${NC}  ${CYAN}🎵✨ VIBECODER MODE ACTIVATED ✨🎵${NC}  ${PURPLE}║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Get status
cd "$WORKSPACE_ROOT"
STATUS_OUTPUT=$(node scripts/always-on-guardian.js 2>/dev/null)
PROJECT=$(echo "$STATUS_OUTPUT" | grep -o '"project":"[^"]*"' | cut -d'"' -f4)
STATUS=$(echo "$STATUS_OUTPUT" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
EMOJI=$(echo "$STATUS_OUTPUT" | grep -o '"emoji":"[^"]*"' | cut -d'"' -f4)

# Vibecoder messages
if [ "$STATUS" = "ACTIVE" ]; then
    echo -e "${GREEN}✨ ${CYAN}YOU'RE IN THE ZONE!${NC} ${GREEN}✨${NC}"
    echo -e "${GREEN}📦 Project: ${YELLOW}$PROJECT${NC}"
    echo -e "${GREEN}🎯 Status: ${YELLOW}ACTIVE${NC} - Perfect vibes for coding!${NC}"
    echo ""
    echo -e "${CYAN}💡 VIBECODER TIPS:${NC}"
    echo -e "   ${PURPLE}🎵${NC} You're in the right place - keep those vibes flowing!"
    echo -e "   ${PURPLE}✨${NC} Run validation anytime - it's all good!"
    echo -e "   ${PURPLE}🚀${NC} Code with confidence - boundaries are protected!"
    echo ""
elif [ "$STATUS" = "LEGACY" ]; then
    echo -e "${YELLOW}💡 ${CYAN}GOOD VIBES DETECTED${NC} ${YELLOW}💡${NC}"
    echo -e "${YELLOW}📦 Project: ${YELLOW}$PROJECT${NC}"
    echo -e "${YELLOW}🎯 Status: ${YELLOW}LEGACY${NC} - Consider switching to active!${NC}"
    echo ""
    echo -e "${CYAN}💡 VIBECODER TIPS:${NC}"
    echo -e "   ${PURPLE}🎵${NC} Switch to active directory for best vibes!"
    echo -e "   ${PURPLE}✨${NC} Check PROJECT_STATUS.md for active directory"
    echo -e "   ${PURPLE}🚀${NC} Keep coding - just switch when ready!"
    echo ""
else
    echo -e "${BLUE}🌊 ${CYAN}VIBECODER MODE${NC} ${BLUE}🌊${NC}"
    echo -e "${BLUE}📦 Status: ${YELLOW}Checking...${NC}"
    echo ""
    echo -e "${CYAN}💡 VIBECODER TIPS:${NC}"
    echo -e "   ${PURPLE}🎵${NC} Navigate to a project directory for best vibes!"
    echo -e "   ${PURPLE}✨${NC} All projects are protected - code with confidence!"
    echo ""
fi

echo -e "${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${NC}  ${CYAN}🎉 KEEP THOSE GOOD VIBES FLOWING! 🎉${NC}  ${PURPLE}║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

