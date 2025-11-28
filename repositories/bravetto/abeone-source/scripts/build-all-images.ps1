# Build script for all AIGuards Backend containers (PowerShell version)
# Builds all images individually before orchestration

param(
    [string]$ImageTag = "dev"
)

$ErrorActionPreference = "Stop"

# Configuration
$BuildDate = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$GitCommit = try { git rev-parse --short HEAD } catch { "unknown" }

# Service definitions
$Services = @(
    @{ Name = "gateway"; Context = "./codeguardians-gateway/codeguardians-gateway"; Dockerfile = "Dockerfile" },
    @{ Name = "tokenguard"; Context = "./guards/tokenguard"; Dockerfile = "Dockerfile" },
    @{ Name = "trustguard"; Context = "./guards/trust-guard"; Dockerfile = "Dockerfile" },
    @{ Name = "contextguard"; Context = "./guards/contextguard"; Dockerfile = "Dockerfile" },
    @{ Name = "biasguard"; Context = "./guards/biasguard-backend"; Dockerfile = "Dockerfile" },
    @{ Name = "healthguard"; Context = "./guards/healthguard"; Dockerfile = "Dockerfile" }
)

# Function to print colored messages
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

# Function to build a single image
function Build-Image {
    param(
        [string]$ServiceName,
        [string]$BuildContext,
        [string]$Dockerfile
    )
    
    $ImageName = "aiguards-$ServiceName`:$ImageTag"
    
    Write-Info "Building $ServiceName..."
    Write-Info "  Context: $BuildContext"
    Write-Info "  Dockerfile: $Dockerfile"
    Write-Info "  Image: $ImageName"
    
    # Check if context directory exists
    if (-not (Test-Path $BuildContext)) {
        Write-Error "Build context not found: $BuildContext"
        return $false
    }
    
    # Check if Dockerfile exists
    $DockerfilePath = Join-Path $BuildContext $Dockerfile
    if (-not (Test-Path $DockerfilePath)) {
        Write-Error "Dockerfile not found: $DockerfilePath"
        return $false
    }
    
    # Build the image
    $BuildArgs = @(
        "build",
        "--tag", $ImageName,
        "--file", $DockerfilePath,
        "--build-arg", "BUILD_DATE=$BuildDate",
        "--build-arg", "GIT_COMMIT=$GitCommit",
        "--label", "org.opencontainers.image.created=$BuildDate",
        "--label", "org.opencontainers.image.revision=$GitCommit",
        "--label", "org.opencontainers.image.version=$ImageTag",
        $BuildContext
    )
    
    try {
        docker $BuildArgs
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Successfully built $ImageName"
            
            # Show image size
            $ImageSize = docker images $ImageName --format "{{.Size}}" | Select-Object -First 1
            Write-Info "  Image size: $ImageSize"
            return $true
        } else {
            Write-Error "Failed to build $ImageName"
            return $false
        }
    } catch {
        Write-Error "Error building $ImageName`: $_"
        return $false
    }
}

# Main build function
function Main {
    Write-Info "=========================================="
    Write-Info "AIGuards Backend - Container Build Script"
    Write-Info "=========================================="
    Write-Info "Build Date: $BuildDate"
    Write-Info "Git Commit: $GitCommit"
    Write-Info "Image Tag: $ImageTag"
    Write-Info ""
    
    # Check if Docker is running
    try {
        docker info | Out-Null
    } catch {
        Write-Error "Docker is not running. Please start Docker Desktop."
        exit 1
    }
    
    $TotalServices = $Services.Count
    $Current = 0
    $Failed = 0
    $Successful = 0
    
    # Build each service
    foreach ($Service in $Services) {
        $Current++
        Write-Info ""
        Write-Info "[$Current/$TotalServices] Building $($Service.Name)..."
        
        if (Build-Image -ServiceName $Service.Name -BuildContext $Service.Context -Dockerfile $Service.Dockerfile) {
            $Successful++
        } else {
            $Failed++
            Write-Warning "Continuing with remaining builds..."
        }
    }
    
    # Summary
    Write-Info ""
    Write-Info "=========================================="
    Write-Info "Build Summary"
    Write-Info "=========================================="
    Write-Info "Total services: $TotalServices"
    Write-Success "Successful: $Successful"
    if ($Failed -gt 0) {
        Write-Error "Failed: $Failed"
    }
    
    # List built images
    Write-Info ""
    Write-Info "Built images:"
    docker images "aiguards-*:$ImageTag" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    if ($Failed -gt 0) {
        Write-Error ""
        Write-Error "Some builds failed. Please check the errors above."
        exit 1
    } else {
        Write-Success ""
        Write-Success "All images built successfully!"
        Write-Info ""
        Write-Info "Next steps:"
        Write-Info "  1. Run 'docker-compose up -d' to start all services"
        Write-Info "  2. Check status with 'docker-compose ps'"
        Write-Info "  3. View logs with 'docker-compose logs -f'"
        exit 0
    }
}

# Run main function
Main

