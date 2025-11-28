# Automatically update all guard service submodules
# This script updates all guard service submodules to their latest commits

Write-Host "🔄 Updating guard service submodules..." -ForegroundColor Cyan

try {
    # Update each guard service submodule
    Write-Host "📦 Updating TokenGuard..." -ForegroundColor Yellow
    git submodule update --remote --merge guards/tokenguard

    Write-Host "📦 Updating TrustGuard..." -ForegroundColor Yellow
    git submodule update --remote --merge guards/trust-guard

    Write-Host "📦 Updating ContextGuard..." -ForegroundColor Yellow
    git submodule update --remote --merge guards/contextguard

    Write-Host "📦 Updating BiasGuard Backend..." -ForegroundColor Yellow
    git submodule update --remote --merge guards/biasguard-backend

    Write-Host "📦 Updating HealthGuard..." -ForegroundColor Yellow
    git submodule update --remote --merge guards/healthguard

    Write-Host "✅ All guard service submodules updated successfully!" -ForegroundColor Green

    # Show status
    Write-Host "📊 Submodule status:" -ForegroundColor Cyan
    git submodule status

    Write-Host "🎉 Guard services are now up to date!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error updating submodules: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
