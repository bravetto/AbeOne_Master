#!/bin/bash

# Create Abë Product Orbitals
# Usage: ./scripts/create_abe_orbitals.sh

set -e

PRODUCTS_DIR="PRODUCTS"
ORBITALS_DIR="orbitals"

echo " Creating Abë Product Orbitals..."

# Create orbitals directory
mkdir -p $ORBITALS_DIR

# Create orbitals for each product
for product in abedesigns abevisions abevoices abegenius abethinks abeloves; do
    if [ -d "$PRODUCTS_DIR/$product" ]; then
        # Capitalize first letter for orbital name
        orbital_name=$(echo "$product" | sed 's/^./\U&/')
        orbital_dir="$ORBITALS_DIR/${orbital_name}-orbital"
        
        echo " Creating $product orbital..."
        mkdir -p "$orbital_dir"
        cp -r "$PRODUCTS_DIR/$product"/* "$orbital_dir/" 2>/dev/null || true
        echo " $product orbital created at $orbital_dir"
    else
        echo "  $product not found in $PRODUCTS_DIR"
    fi
done

echo ""
echo " All orbitals created successfully!"
echo ""
echo " Created orbitals:"
ls -d $ORBITALS_DIR/*-orbital 2>/dev/null | sed 's|^|   |' || echo "   (none)"
echo ""

