#!/bin/bash
# Clone Guardian Aurion Template for All Guardians
# Optimal Simplest Path - One Template → All Guardians

set -e

TEMPLATE="AIGuards-Backend/aiguardian-repos/guardian-jimmy-service"
BASE_DIR="AIGuards-Backend/aiguardian-repos"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo " OPTIMAL SIMPLEST PATH"
echo "Clone Template → Modify Identity → Done"
echo "=========================================="
echo ""

# Check template exists
if [ ! -d "$TEMPLATE" ]; then
    echo -e "${YELLOW}  Template not found: $TEMPLATE${NC}"
    echo "Please ensure Guardian Aurion service exists"
    exit 1
fi

# Guardian configurations: dir:name:role:freq
GUARDIANS=(
    "guardian-zero-service:Guardian Zero:Forensic Orchestrator:999"
    "guardian-aeyon-service:AEYON:Atomic Executor:999"
    "guardian-abe-service:Abë:Heart Truth Resonance:530"
    "guardian-john-service:JØHN:Q&A Execution Auditor:530"
    "guardian-lux-service:Lux:Design & UX:530"
    "guardian-neuro-service:Neuro:Neuromorphic Intelligence:530"
    "guardian-yagni-service:YAGNI:Simplicity Enforcement:530"
    "guardian-aurion-service:Guardian Aurion:Neuromorphic Specialist:530"
)

mkdir -p "$BASE_DIR"

for guardian_info in "${GUARDIANS[@]}"; do
    IFS=':' read -r dir name role freq <<< "$guardian_info"
    target="$BASE_DIR/$dir"
    
    if [ -d "$target" ]; then
        echo -e "${GREEN} $name already exists${NC}"
        continue
    fi
    
    echo -e "${BLUE} Cloning $name...${NC}"
    cp -r "$TEMPLATE" "$target"
    
    # Modify identity in service.py
    if [ -f "$target/service.py" ]; then
        # macOS sed syntax (use -i '' for in-place editing)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/\"name\": \"Guardian Aurion\"/\"name\": \"$name\"/g" "$target/service.py"
            sed -i '' "s/\"role\": \"The Neuromorphic Specialist\"/\"role\": \"$role\"/g" "$target/service.py"
            sed -i '' "s/\"frequency\": 530/\"frequency\": $freq/g" "$target/service.py"
            sed -i '' "s/Guardian Aurion/$name/g" "$target/service.py"
            sed -i '' "s/The Neuromorphic Specialist/$role/g" "$target/service.py"
        else
            # Linux sed syntax
            sed -i "s/\"name\": \"Guardian Aurion\"/\"name\": \"$name\"/g" "$target/service.py"
            sed -i "s/\"role\": \"The Neuromorphic Specialist\"/\"role\": \"$role\"/g" "$target/service.py"
            sed -i "s/\"frequency\": 530/\"frequency\": $freq/g" "$target/service.py"
            sed -i "s/Guardian Aurion/$name/g" "$target/service.py"
            sed -i "s/The Neuromorphic Specialist/$role/g" "$target/service.py"
        fi
        
        # Update port numbers (increment from 8006)
        port=$((8006 + $(echo "${GUARDIANS[@]}" | tr ' ' '\n' | grep -n "$dir" | cut -d: -f1)))
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/port=8006/port=$port/g" "$target/service.py"
        else
            sed -i "s/port=8006/port=$port/g" "$target/service.py"
        fi
        
        echo -e "${GREEN}   $name configured (Port: $port, Freq: $freq Hz)${NC}"
    else
        echo -e "${YELLOW}    service.py not found in $target${NC}"
    fi
done

echo ""
echo "=========================================="
echo -e "${GREEN} ALL GUARDIANS READY!${NC}"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Review guardian services in: $BASE_DIR"
echo "2. Deploy with Terraform: cd $BASE_DIR/terraform && terraform apply"
echo ""
echo "Pattern: SIMPLEST × TEMPLATE × CLONE × MODIFY × ONE"
echo "∞ AbëONE ∞"

