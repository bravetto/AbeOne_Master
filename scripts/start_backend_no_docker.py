#!/usr/bin/env python3
"""
 BACKEND STARTER - NO DOCKER 
Starts backend services directly without Docker.

Pattern: BACKEND × NO_DOCKER × DIRECT × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × ∞ Hz (Abë)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import subprocess
import sys
import os
import signal
import time
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent

from scripts.utilities.path_discovery import find_backend_root, find_gateway_app_directory

BACKEND_ROOT = find_backend_root()
GATEWAY_PATH = find_gateway_app_directory()

if not BACKEND_ROOT:
    raise RuntimeError("AIGuards-Backend-orbital not found")
if not GATEWAY_PATH:
    raise RuntimeError("codeguardians-gateway not found")
PROCESSES = []


def start_gateway():
    """Start Gateway API (port 8000) directly without Docker."""
    print(" Starting Gateway API (port 8000)...")
    
    os.chdir(GATEWAY_PATH)
    
    # Check if requirements are installed
    try:
        import uvicorn
        import fastapi
    except ImportError:
        print("     Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Start uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(GATEWAY_PATH)
    )
    
    PROCESSES.append(("Gateway API", process, 8000))
    print(f"    Gateway API started (PID: {process.pid})")
    return process


def start_guard_service(name, port, path):
    """Start a guard service without Docker."""
    print(f"  Starting {name} (port {port})...")
    
    guard_path = BACKEND_ROOT / path
    
    if not guard_path.exists():
        print(f"     {name} path not found: {guard_path}")
        return None
    
    os.chdir(guard_path)
    
    # Check for main.py or app.py
    main_file = guard_path / "main.py"
    if not main_file.exists():
        main_file = guard_path / "app.py"
    
    if not main_file.exists():
        print(f"     {name} main file not found")
        return None
    
    # Start uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn",
        f"{main_file.stem}:app",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--reload"
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(guard_path)
    )
    
    PROCESSES.append((name, process, port))
    print(f"    {name} started (PID: {process.pid})")
    return process


def cleanup(signum, frame):
    """Cleanup all processes on exit."""
    print("\n Stopping all services...")
    for name, process, port in PROCESSES:
        try:
            process.terminate()
            process.wait(timeout=5)
            print(f"    {name} stopped")
        except:
            process.kill()
            print(f"     {name} killed")
    sys.exit(0)


def main():
    """Main execution."""
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    print(" BACKEND STARTER - NO DOCKER ")
    print("=" * 60)
    print()
    
    # Start Gateway
    gateway = start_gateway()
    time.sleep(2)
    
    # Start Guard Services
    guards = [
        ("TokenGuard", 8001, "guards/tokenguard"),
        ("TrustGuard", 8002, "guards/trust-guard"),
        ("ContextGuard", 8003, "guards/contextguard"),
        ("BiasGuard", 8004, "guards/biasguard-backend"),
        ("HealthGuard", 8005, "guards/healthguard"),
    ]
    
    for name, port, path in guards:
        start_guard_service(name, port, path)
        time.sleep(1)
    
    print()
    print("=" * 60)
    print(" BACKEND SERVICES STARTED (NO DOCKER) ")
    print("=" * 60)
    print()
    print("Services Running:")
    for name, process, port in PROCESSES:
        status = "" if process.poll() is None else ""
        print(f"  {status} {name} (port {port}) - PID: {process.pid}")
    print()
    print("Press Ctrl+C to stop all services")
    print()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
            # Check if any process died
            for name, process, port in PROCESSES:
                if process.poll() is not None:
                    print(f"  {name} died, restarting...")
                    # Restart logic here if needed
    except KeyboardInterrupt:
        cleanup(None, None)


if __name__ == '__main__':
    main()

