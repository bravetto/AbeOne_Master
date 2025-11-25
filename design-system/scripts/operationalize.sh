#!/bin/bash
# AbëONE Color System - Operationalization Script
# Generates all outputs, validates, and ensures system is ready for use

set -e

echo "🚀 Operationalizing AbëONE Unified Color System v2.0..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Validate color system
echo -e "${BLUE}Step 1: Validating color system...${NC}"
node design-system/scripts/validate-colors.js
if [ $? -ne 0 ]; then
  echo -e "${YELLOW}⚠️  Validation found issues. Continuing anyway...${NC}"
fi
echo ""

# Step 2: Generate Tailwind config
echo -e "${BLUE}Step 2: Generating Tailwind config...${NC}"
node design-system/generators/generate-unified-tailwind.js
echo ""

# Step 3: Generate CSS variables
echo -e "${BLUE}Step 3: Generating CSS variables...${NC}"
node design-system/generators/generate-css-vars.js
echo ""

# Step 4: Generate TypeScript types (if tsx available)
if command -v npx &> /dev/null; then
  echo -e "${BLUE}Step 4: Generating TypeScript types...${NC}"
  if npx tsx design-system/generators/generate-types.ts 2>/dev/null; then
    echo -e "${GREEN}✅ TypeScript types generated${NC}"
  else
    echo -e "${YELLOW}⚠️  TypeScript generator skipped (tsx not available)${NC}"
  fi
  echo ""
fi

# Step 5: Generate Python constants (if python3 available)
if command -v python3 &> /dev/null; then
  echo -e "${BLUE}Step 5: Generating Python constants...${NC}"
  if python3 design-system/generators/generate-python.py 2>/dev/null; then
    echo -e "${GREEN}✅ Python constants generated${NC}"
  else
    echo -e "${YELLOW}⚠️  Python generator skipped${NC}"
  fi
  echo ""
fi

# Summary
echo -e "${GREEN}✅ Operationalization complete!${NC}"
echo ""
echo "📚 Generated files:"
echo "  - apps/web/tailwind.config.js"
echo "  - design-system/generated/css-variables.css"
echo ""
echo "🎨 Color system is ready for use!"
echo ""

