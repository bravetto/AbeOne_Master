@echo off
REM CodeGuardians Gateway - Configuration Test Script (Windows)
REM Validates the streamlined configuration

setlocal enabledelayedexpansion

echo [%date% %time%] Testing CodeGuardians Gateway configuration...

REM Test Docker configuration
echo Testing Docker configuration...
if not exist "docker-compose.yml" (
    echo [ERROR] docker-compose.yml not found
    exit /b 1
)

REM Test environment configuration
echo Testing environment configuration...
if not exist "env.unified" (
    echo [ERROR] env.unified not found
    exit /b 1
)

REM Test deployment script
echo Testing deployment script...
if not exist "..\..\deployment\deploy.sh" (
    echo [ERROR] deployment/deploy.sh not found
    exit /b 1
)

REM Test Dockerfile
echo Testing Dockerfile...
if not exist "Dockerfile" (
    echo [ERROR] Dockerfile not found
    exit /b 1
)

REM Test requirements
echo Testing requirements...
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found
    exit /b 1
)

REM Test main application
echo Testing main application...
if not exist "app\main.py" (
    echo [ERROR] app\main.py not found
    exit /b 1
)

if not exist "app" (
    echo [ERROR] app directory not found
    exit /b 1
)

echo [SUCCESS] All configuration tests passed!
echo.
echo Configuration Summary:
echo - Docker Compose: docker-compose.yml
echo - Environment: env.unified
echo - Startup Script: start.sh
echo - Dockerfile: Dockerfile
echo - Requirements: requirements.txt
echo - Main App: app\main.py
echo.
echo Ready for deployment!
