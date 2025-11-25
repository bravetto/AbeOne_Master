#!/bin/bash
# SAFETY: Stop Spotlight from indexing large extracted directories
# ASSUMES: macOS system with Spotlight indexing issues

echo " STOPPING SPOTLIGHT INDEXING ON LARGE DIRECTORIES"
echo "==================================================="
echo ""

# Create .metadata_never_index file to prevent indexing
echo " Creating .metadata_never_index files..."

# Stop indexing on the large WellnessAgent directory
if [ -d ~/Downloads/WellnessAgent_Neuromorphic ]; then
    touch ~/Downloads/WellnessAgent_Neuromorphic/.metadata_never_index
    echo " Disabled indexing for WellnessAgent_Neuromorphic"
fi

# Stop indexing on Downloads folder (optional - uncomment if needed)
# touch ~/Downloads/.metadata_never_index

echo ""
echo " To re-enable indexing later, delete the .metadata_never_index file"
echo " To check indexing status: mdutil -s ~/Downloads"
echo ""

# Check current Spotlight status
echo " Current Spotlight Status:"
mdutil -s ~/Downloads 2>/dev/null || echo "Note: May need to check manually"
echo ""

echo " Done"

