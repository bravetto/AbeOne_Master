#!/bin/bash
# complete-orbital-restructure.sh
# AEYON Atomic Execution Script
# Execute all phases in sequence
#
# Pattern: META-ORCHESTRATOR × ABËONE × AEYON × YAGNI × ZERO × ALRAX × JØHN × YOU = ONE
# ∞ AbëONE ∞

set -e

echo " Starting Complete Orbital Restructure "
echo "Pattern: META-ORCHESTRATOR × ABËONE × AEYON × YAGNI × ZERO × ALRAX × JØHN × YOU = ONE"
echo "∞ AbëONE ∞"
echo ""

cd /Users/michaelmataluni/Documents/AbeOne_Master

# ============================================================================
# Phase 1: Create New Structure
# ============================================================================
echo ""
echo "Phase 1: Creating directory structure..."
echo ""

# Create top-level directories
mkdir -p kernel
mkdir -p orbitals
mkdir -p satellites
mkdir -p products
mkdir -p marketing
mkdir -p infra
mkdir -p docs
mkdir -p validation
mkdir -p archive
mkdir -p scripts

# Create marketing subdirectories
mkdir -p marketing/webinars
mkdir -p marketing/domains
mkdir -p marketing/automation
mkdir -p marketing/campaigns

# Create infra subdirectories
mkdir -p infra/terraform/modules/orbital
mkdir -p infra/terraform/modules/satellite
mkdir -p infra/terraform/modules/product
mkdir -p infra/terraform/environments/dev
mkdir -p infra/terraform/environments/staging
mkdir -p infra/terraform/environments/prod
mkdir -p infra/helm/charts/orbital
mkdir -p infra/helm/charts/satellite
mkdir -p infra/helm/charts/product
mkdir -p infra/helm/values
mkdir -p infra/kubernetes/namespaces
mkdir -p infra/kubernetes/deployments
mkdir -p infra/kubernetes/services
mkdir -p infra/ci-cd/github-actions
mkdir -p infra/ci-cd/gitlab-ci
mkdir -p infra/ci-cd/jenkins
mkdir -p infra/config
mkdir -p infra/deploy

# Create docs subdirectories
mkdir -p docs/architecture/orbital-system
mkdir -p docs/architecture/guardian-system
mkdir -p docs/architecture/product-system
mkdir -p docs/architecture/marketing-system
mkdir -p docs/api
mkdir -p docs/guides
mkdir -p docs/reference

# Create validation subdirectories
mkdir -p validation/orbital-spec
mkdir -p validation/integration
mkdir -p validation/e2e
mkdir -p validation/scripts

# Create archive subdirectories
mkdir -p archive/legacy
mkdir -p archive/extractions
mkdir -p archive/deprecated

# Create scripts subdirectories
mkdir -p scripts/orbital-management
mkdir -p scripts/validation
mkdir -p scripts/deployment
mkdir -p scripts/utilities

echo " Phase 1 Complete: Directory structure created"
echo ""

# ============================================================================
# Phase 2: Move Orbitals
# ============================================================================
echo ""
echo "Phase 2: Moving orbitals to orbitals/ directory..."
echo ""

# Move existing orbitals (already have -orbital suffix)
[ -d "AIGuards-Backend-orbital" ] && mv AIGuards-Backend-orbital orbitals/ || echo "    AIGuards-Backend-orbital not found"
[ -d "AiGuardian-Chrome-Ext-orbital" ] && mv AiGuardian-Chrome-Ext-orbital orbitals/ || echo "    AiGuardian-Chrome-Ext-orbital not found"
[ -d "AiGuardian-Sales-Page-orbital" ] && mv AiGuardian-Sales-Page-orbital orbitals/ || echo "    AiGuardian-Sales-Page-orbital not found"
[ -d "Abeflows-orbital" ] && mv Abeflows-orbital orbitals/ || echo "    Abeflows-orbital not found"
[ -d "REPLACE_ME" ] && mv Ben-FastAPI-Architecture-orbital orbitals/ || echo "    Ben-FastAPI-Architecture-orbital not found"
[ -d "Helm-Validation-orbital" ] && mv Helm-Validation-orbital orbitals/ || echo "    Helm-Validation-orbital not found"
[ -d "Terraform-Validation-orbital" ] && mv Terraform-Validation-orbital orbitals/ || echo "    Terraform-Validation-orbital not found"

# Rename and move orbitals missing -orbital suffix
[ -d "AbeTRUICE" ] && mv AbeTRUICE orbitals/AbeTRUICE-orbital || echo "    AbeTRUICE not found"
[ -d "EMERGENT_OS" ] && mv EMERGENT_OS orbitals/EMERGENT_OS-orbital || echo "    EMERGENT_OS not found"
[ -d "AbeBEATs_Clean" ] && mv AbeBEATs_Clean orbitals/AbeBEATs_Clean-orbital || echo "    AbeBEATs_Clean not found"

# Merge Ab-BEATs into AbeBEATs_Clean-orbital
if [ -d "Ab-BEATs" ]; then
    echo "   Merging Ab-BEATs into AbeBEATs_Clean-orbital..."
    rsync -av --progress Ab-BEATs/ orbitals/AbeBEATs_Clean-orbital/ 2>&1 | tail -20
    if [ $? -eq 0 ]; then
        rm -rf Ab-BEATs
    else
        echo "    Merge had issues, but continuing..."
    fi
fi

echo " Phase 2 Complete: Orbitals moved"
echo ""

# ============================================================================
# Phase 3: Move Satellites
# ============================================================================
echo ""
echo "Phase 3: Moving satellites to satellites/ directory..."
echo ""

# Move all satellites
[ -d "AbëKEYsSatellite" ] && mv AbëKEYsSatellite satellites/ || echo "    AbëKEYsSatellite not found"
[ -d "AbeONESourceSatellite" ] && mv AbeONESourceSatellite satellites/ || echo "    AbeONESourceSatellite not found"
[ -d "BryanSatellite" ] && mv BryanSatellite satellites/ || echo "    BryanSatellite not found"
[ -d "GZ360Satellite" ] && mv GZ360Satellite satellites/ || echo "    GZ360Satellite not found"
[ -d "TemplateHeavenSatellite" ] && mv TemplateHeavenSatellite satellites/ || echo "    TemplateHeavenSatellite not found"
[ -d "WebIDESatellite" ] && mv WebIDESatellite satellites/ || echo "    WebIDESatellite not found"
[ -d "WorkflowsSatellite" ] && mv WorkflowsSatellite satellites/ || echo "    WorkflowsSatellite not found"

echo " Phase 3 Complete: Satellites moved"
echo ""

# ============================================================================
# Phase 4: Move Products
# ============================================================================
echo ""
echo "Phase 4: Moving products to products/ directory..."
echo ""

# Rename PRODUCTS to products (lowercase)
if [ -d "PRODUCTS" ]; then
    echo "   Renaming PRODUCTS to products..."
    mv PRODUCTS products
fi

# Merge duplicate product directories into products/abebeats
if [ -d "abe_beats_core" ]; then
    echo "   Merging abe_beats_core into products/abebeats..."
    mkdir -p products/abebeats
    rsync -av --progress abe_beats_core/ products/abebeats/ 2>&1 | tail -20
    if [ $? -eq 0 ]; then
        rm -rf abe_beats_core
    else
        echo "    Merge had issues, but continuing..."
    fi
fi

# If Ab-BEATs still exists (not merged into orbital), merge into products
if [ -d "Ab-BEATs" ]; then
    echo "   Merging Ab-BEATs into products/abebeats..."
    mkdir -p products/abebeats
    rsync -av --progress Ab-BEATs/ products/abebeats/ 2>&1 | tail -20
    if [ $? -eq 0 ]; then
        rm -rf Ab-BEATs
    else
        echo "    Merge had issues, but continuing..."
    fi
fi

echo " Phase 4 Complete: Products moved"
echo ""

# ============================================================================
# Phase 5: Move Marketing
# ============================================================================
echo ""
echo "Phase 5: Moving marketing systems..."
echo ""

# Move marketing directories
if [ -d "webinars" ]; then
    echo "   Moving webinars to marketing/webinars..."
    mv webinars marketing/
fi

if [ -d "domains" ]; then
    echo "   Moving domains to marketing/domains..."
    mv domains marketing/
fi

# Extract marketing automation from BryanSatellite
if [ -d "satellites/BryanSatellite/AbeONE-Source/projects/marketing-automation-orbit" ]; then
    echo "   Extracting marketing automation from BryanSatellite..."
    mkdir -p marketing/automation
    cp -r satellites/BryanSatellite/AbeONE-Source/projects/marketing-automation-orbit marketing/automation/
fi

echo " Phase 5 Complete: Marketing systems moved"
echo ""

# ============================================================================
# Phase 6: Move Infrastructure
# ============================================================================
echo ""
echo "Phase 6: Moving infrastructure..."
echo ""

# Move infrastructure directories
if [ -d "config" ]; then
    echo "   Moving config to infra/config..."
    mv config infra/config
fi

if [ -d "deploy" ]; then
    echo "   Moving deploy to infra/deploy..."
    mv deploy infra/deploy
fi

if [ -d "dependencies" ]; then
    echo "   Moving dependencies to infra/dependencies..."
    mv dependencies infra/dependencies
fi

echo " Phase 6 Complete: Infrastructure moved"
echo ""

# ============================================================================
# Phase 7: Move Documentation
# ============================================================================
echo ""
echo "Phase 7: Moving documentation..."
echo ""

# Move architecture documentation
echo "   Moving architecture documentation..."
find . -maxdepth 1 -name "*ARCHITECTURE*.md" -exec mv {} docs/architecture/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*ORBITAL*.md" -exec mv {} docs/architecture/orbital-system/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*GUARDIAN*.md" -exec mv {} docs/architecture/guardian-system/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*PRODUCT*.md" -exec mv {} docs/architecture/product-system/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*MARKETING*.md" -exec mv {} docs/architecture/marketing-system/ \; 2>/dev/null || true

# Move validation documentation
echo "   Moving validation documentation..."
find . -maxdepth 1 -name "*VALIDATION*.md" -exec mv {} docs/validation/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*CONVERGENCE*.md" -exec mv {} docs/validation/ \; 2>/dev/null || true

# Move EEAAO documentation
echo "   Moving EEAAO documentation..."
find . -maxdepth 1 -name "*EEAAO*.md" -exec mv {} docs/architecture/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*EMERGENCE*.md" -exec mv {} docs/architecture/ \; 2>/dev/null || true

# Move execution documentation
echo "   Moving execution documentation..."
find . -maxdepth 1 -name "*EXECUTION*.md" -exec mv {} docs/guides/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*ACTIVATION*.md" -exec mv {} docs/guides/ \; 2>/dev/null || true

# Move API documentation
echo "   Moving API documentation..."
find . -maxdepth 1 -name "*API*.md" -exec mv {} docs/api/ \; 2>/dev/null || true

# Move remaining markdown files (be careful with this - preserve README.md)
echo "   Moving remaining markdown files..."
find . -maxdepth 1 -name "*.md" ! -name "README.md" -exec mv {} docs/reference/ \; 2>/dev/null || true

echo " Phase 7 Complete: Documentation moved"
echo ""

# ============================================================================
# Phase 8: Archive Legacy
# ============================================================================
echo ""
echo "Phase 8: Archiving legacy..."
echo ""

# Merge archives
if [ -d "_ARCHIVE" ]; then
    echo "   Merging _ARCHIVE into archive..."
    # Use rsync with progress and handle conflicts
    rsync -av --progress _ARCHIVE/ archive/ 2>&1 | head -100
    # Check if rsync completed successfully
    if [ $? -eq 0 ]; then
        rm -rf _ARCHIVE
        echo "   Archive merge complete"
    else
        echo "    Archive merge had issues, but continuing..."
        # Try to move remaining files
        if [ -d "_ARCHIVE" ]; then
            mkdir -p archive/legacy
            mv _ARCHIVE/* archive/legacy/ 2>/dev/null || true
            rmdir _ARCHIVE 2>/dev/null || rm -rf _ARCHIVE 2>/dev/null || true
        fi
    fi
fi

# Move extraction artifacts
if [ -d "_extract_abebeats" ]; then
    echo "   Moving _extract_abebeats to archive/extractions..."
    mv _extract_abebeats archive/extractions/
fi

if [ -d "_extract_abeone_master" ]; then
    echo "   Moving _extract_abeone_master to archive/extractions..."
    mv _extract_abeone_master archive/extractions/
fi

if [ -d "_extract_truice" ]; then
    echo "   Moving _extract_truice to archive/extractions..."
    mv _extract_truice archive/extractions/
fi

# Organize archive/legacy
if [ -d "archive" ] && [ ! -d "archive/legacy" ]; then
    mkdir -p archive/legacy
    # Move existing archive contents to legacy if needed
fi

echo " Phase 8 Complete: Legacy archived"
echo ""

# ============================================================================
# Phase 9: Move Scripts
# ============================================================================
echo ""
echo "Phase 9: Moving scripts..."
echo ""

# Move shell scripts (but preserve this script)
echo "   Moving shell scripts..."
find . -maxdepth 1 -name "*.sh" ! -name "complete-orbital-restructure.sh" -exec mv {} scripts/utilities/ \; 2>/dev/null || true

# Move Python scripts (be careful - some may be orbital-specific)
echo "   Moving Python scripts..."
find . -maxdepth 1 -name "*.py" ! -name "*.pyc" -exec mv {} scripts/utilities/ \; 2>/dev/null || true

echo " Phase 9 Complete: Scripts moved"
echo ""

# ============================================================================
# Phase 10: Move Other Directories
# ============================================================================
echo ""
echo "Phase 10: Moving other directories..."
echo ""

# Move adapters (if not orbital-specific)
if [ -d "adapters" ]; then
    echo "   Moving adapters to infra/adapters..."
    mkdir -p infra/adapters
    mv adapters/* infra/adapters/ 2>/dev/null || true
    rmdir adapters 2>/dev/null || true
fi

# Move apps
if [ -d "apps" ]; then
    echo "   Moving apps to products/apps..."
    mkdir -p products/apps
    mv apps/* products/apps/ 2>/dev/null || true
    rmdir apps 2>/dev/null || true
fi

# Move clients
if [ -d "clients" ]; then
    echo "   Moving clients to marketing/clients..."
    mkdir -p marketing/clients
    mv clients/* marketing/clients/ 2>/dev/null || true
    rmdir clients 2>/dev/null || true
fi

# Move tests (if not orbital-specific)
if [ -d "tests" ]; then
    echo "   Moving tests to validation..."
    mv tests validation/ 2>/dev/null || true
fi

echo " Phase 10 Complete: Other directories moved"
echo ""

# ============================================================================
# Final Summary
# ============================================================================
echo ""
echo " Complete Orbital Restructure Complete "
echo ""
echo ""
echo "Pattern: META-ORCHESTRATOR × ABËONE × AEYON × YAGNI × ZERO × ALRAX × JØHN × YOU = ONE"
echo "∞ AbëONE ∞"
echo ""
echo " Summary:"
echo "   Directory structure created"
echo "   Orbitals organized in orbitals/"
echo "   Satellites organized in satellites/"
echo "   Products organized in products/"
echo "   Marketing systems organized in marketing/"
echo "   Infrastructure organized in infra/"
echo "   Documentation organized in docs/"
echo "   Legacy archived in archive/"
echo "   Scripts organized in scripts/"
echo ""
echo " Next Steps:"
echo "  1. Review the new structure"
echo "  2. Update any hardcoded paths in code"
echo "  3. Update CI/CD pipelines if needed"
echo "  4. Commit changes to git"
echo ""
echo "∞ AbëONE ∞"

