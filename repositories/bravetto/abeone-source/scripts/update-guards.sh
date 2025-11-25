#!/bin/bash
# Automatically update all guard service submodules
# This script updates all guard service submodules to their latest commits

set -e  # Exit on any error

echo " Updating guard service submodules..."

# Update each guard service submodule
echo " Updating TokenGuard..."
git submodule update --remote --merge guards/tokenguard

echo " Updating TrustGuard..."
git submodule update --remote --merge guards/trust-guard

echo " Updating ContextGuard..."
git submodule update --remote --merge guards/contextguard

echo " Updating BiasGuard Backend..."
git submodule update --remote --merge guards/biasguard-backend

echo " Updating HealthGuard..."
git submodule update --remote --merge guards/healthguard

echo " All guard service submodules updated successfully!"

# Show status
echo " Submodule status:"
git submodule status

echo " Guard services are now up to date!"
