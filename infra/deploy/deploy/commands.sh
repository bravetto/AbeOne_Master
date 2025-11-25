#!/bin/bash
# AbëONE Master Workspace Deployment Commands
# Orbit-Spec compliant deployment script

set -e

echo " AbëONE Master Workspace Deployment Script"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if kernel exists
if [ ! -d "abëone" ]; then
    echo -e "${YELLOW}  Kernel directory not found at abëone${NC}"
    echo "This workspace orchestrator expects the kernel at abëone/"
    echo "If using git submodule, run: git submodule update --init --recursive"
fi

# Verify adapters
echo "Verifying adapters..."
REQUIRED_ADAPTERS=("adapter.kernel.py" "adapter.guardians.py" "adapter.module.py" "adapter.bus.py")
for adapter in "${REQUIRED_ADAPTERS[@]}"; do
    if [ ! -f "adapters/$adapter" ]; then
        echo -e "${RED} Missing adapter: $adapter${NC}"
        exit 1
    fi
done
echo -e "${GREEN} All adapters present${NC}"

# Verify config files
echo "Verifying config files..."
if [ ! -f "config/orbit.config.json" ]; then
    echo -e "${RED} Missing config/orbit.config.json${NC}"
    exit 1
fi

if [ ! -f "module_manifest.json" ]; then
    echo -e "${RED} Missing module_manifest.json${NC}"
    exit 1
fi
echo -e "${GREEN} Config files present${NC}"

# Check sub-orbits
echo "Checking sub-orbits..."
if [ -d "AbeTRUICE" ]; then
    echo -e "${GREEN} AbeTRUICE orbit found${NC}"
else
    echo -e "${YELLOW}  AbeTRUICE orbit not found${NC}"
fi

if [ -d "AbeBEATs_Clean" ]; then
    echo -e "${GREEN} AbeBEATs_Clean orbit found${NC}"
else
    echo -e "${YELLOW}  AbeBEATs_Clean orbit not found${NC}"
fi

# Test adapters
echo "Testing adapters..."
python3 -c "
import sys
import importlib.util
from pathlib import Path

sys.path.insert(0, str(Path('.').absolute()))

try:
    # Import adapters using importlib.util (handles dots in module names)
    adapters = [
        ('adapters/adapter.kernel.py', 'adapter.kernel'),
        ('adapters/adapter.guardians.py', 'adapter.guardians'),
        ('adapters/adapter.module.py', 'adapter.module'),
        ('adapters/adapter.bus.py', 'adapter.bus')
    ]
    
    for file_path, module_name in adapters:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    
    print(' All adapters import successfully')
except Exception as e:
    print(f' Adapter import failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

echo -e "${GREEN} Adapters tested${NC}"

echo ""
echo "=============================================="
echo -e "${GREEN} Deployment verification complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Initialize kernel (if using submodule): git submodule update --init --recursive"
echo "2. Register workspace module with AbëONE kernel"
echo "3. Start workspace orchestrator"
echo ""
echo "Pattern: OBSERVER × TRUTH × ATOMIC × ONE"
echo "∞ AbëONE ∞"

