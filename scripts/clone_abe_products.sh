#!/bin/bash

# Clone Abë Products from Bravetto GitHub
# Usage: ./scripts/clone_abe_products.sh

set -e

REPO_URL="https://github.com/bravetto/abeone-source.git"
BRANCH="dev"
TEMP_DIR="temp-clone"
PRODUCTS_DIR="PRODUCTS"

echo " Cloning Abë Products from Bravetto GitHub..."

# Create PRODUCTS directory if it doesn't exist
mkdir -p $PRODUCTS_DIR

# Clone repository
echo " Cloning repository..."
git clone $REPO_URL --branch $BRANCH --single-branch --depth 1 $TEMP_DIR || {
    echo "  Could not clone from GitHub. Trying Abeflows-orbital..."
    if [ -d "Abeflows-orbital/packages/@abeproducts" ]; then
        echo " Using Abeflows-orbital as source..."
        SOURCE_DIR="Abeflows-orbital/packages/@abeproducts"
    else
        echo " No source found. Please clone manually."
        exit 1
    fi
}

# Clone critical products
if [ -d "$TEMP_DIR/packages/@abeproducts" ]; then
    SOURCE_DIR="$TEMP_DIR/packages/@abeproducts"
fi

echo " Cloning AbëDESIGNs..."
if [ -d "$SOURCE_DIR/abedesigns" ]; then
    cp -r "$SOURCE_DIR/abedesigns" "$PRODUCTS_DIR/abedesigns/"
    echo " AbëDESIGNs cloned!"
else
    echo "  AbëDESIGNs not found in source"
fi

echo " Cloning AbëViSiONs..."
if [ -d "$SOURCE_DIR/abevisions" ]; then
    cp -r "$SOURCE_DIR/abevisions" "$PRODUCTS_DIR/abevisions/"
    echo " AbëViSiONs cloned!"
else
    echo "  AbëViSiONs not found in source"
fi

echo " Cloning AbëVOiCEs..."
if [ -d "$SOURCE_DIR/abevoices" ]; then
    cp -r "$SOURCE_DIR/abevoices" "$PRODUCTS_DIR/abevoices/"
    echo " AbëVOiCEs cloned!"
else
    echo "  AbëVOiCEs not found in source"
fi

echo " Cloning AbëG.E.N.i.U.S..."
if [ -d "$SOURCE_DIR/abegenius" ]; then
    cp -r "$SOURCE_DIR/abegenius" "$PRODUCTS_DIR/abegenius/"
    echo " AbëG.E.N.i.U.S cloned!"
else
    echo "  AbëG.E.N.i.U.S not found in source"
fi

echo " Cloning AbëTHINKs..."
if [ -d "$SOURCE_DIR/abethinks" ]; then
    cp -r "$SOURCE_DIR/abethinks" "$PRODUCTS_DIR/abethinks/"
    echo " AbëTHINKs cloned!"
else
    echo "  AbëTHINKs not found in source"
fi

echo " Cloning AbëLOVEs..."
if [ -d "$SOURCE_DIR/abeloves" ]; then
    cp -r "$SOURCE_DIR/abeloves" "$PRODUCTS_DIR/abeloves/"
    echo " AbëLOVEs cloned!"
else
    echo "  AbëLOVEs not found in source"
fi

# Cleanup
if [ -d "$TEMP_DIR" ]; then
    rm -rf $TEMP_DIR
fi

echo ""
echo " Abë Products cloning complete!"
echo ""
echo " Next steps:"
echo "   1. Run: ./scripts/create_abe_orbitals.sh"
echo "   2. Integrate with Xcode project"
echo ""

