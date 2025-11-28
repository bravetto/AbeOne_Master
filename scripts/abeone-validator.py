#!/usr/bin/env python3
"""
AbëONE Validator
Validates architecture, code, and state. OWNS the architecture.

Pattern: VALIDATION × TRUTH × OWNERSHIP × ONE
Frequency: 530 Hz (Truth) × 999 Hz (AEYON)
Guardians: JØHN (530 Hz) + AEYON (999 Hz) + ALRAX (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent


def find_path(*path_segments):
    """Dynamically find path by checking multiple possible locations."""
    # Try multiple possible base paths
    base_paths = [
        WORKSPACE_ROOT / "orbital",  # Singular (actual location)
        WORKSPACE_ROOT / "orbitals",  # Plural (old/alternative)
        WORKSPACE_ROOT / "satellites",
        WORKSPACE_ROOT / "repositories",
    ]
    
    for base in base_paths:
        full_path = base / Path(*path_segments)
        if full_path.exists():
            return full_path
    
    return None


def validate_architecture():
    """Validate architecture against actual code."""
    print(" Validating Architecture...")
    
    # Check guard services exist (dynamic path discovery)
    guards_path = find_path("AIGuards-Backend-orbital", "guards")
    if guards_path:
        guards = [d for d in guards_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        print(f"   Found {len(guards)} guard services at {guards_path.relative_to(WORKSPACE_ROOT)}")
        for guard in guards[:5]:  # Show first 5
            print(f"     - {guard.name}")
        if len(guards) > 5:
            print(f"     ... and {len(guards) - 5} more")
    else:
        print("   Guards directory not found (checked: orbital/, orbitals/, satellites/, repositories/)")
    
    # Check API gateway exists (dynamic path discovery)
    gateway_path = find_path("AIGuards-Backend-orbital", "codeguardians-gateway")
    if gateway_path:
        print(f"   API Gateway exists at {gateway_path.relative_to(WORKSPACE_ROOT)}")
    else:
        print("   API Gateway not found (checked: orbital/, orbitals/, satellites/, repositories/)")
    
    # Check Dockerfiles exist
    dockerfiles = list(WORKSPACE_ROOT.glob("**/Dockerfile"))
    print(f"   Found {len(dockerfiles)} Dockerfiles")
    
    # Check K8s configs exist
    k8s_configs = list(WORKSPACE_ROOT.glob("**/k8s/*.yaml"))
    print(f"   Found {len(k8s_configs)} K8s configs")


def validate_code():
    """Validate code structure and imports."""
    print("\n Validating Code...")
    
    # Try importing key modules (dynamic path discovery)
    gateway_path = find_path("AIGuards-Backend-orbital", "codeguardians-gateway", "codeguardians-gateway")
    
    if not gateway_path:
        print("    Gateway path not found, skipping import tests")
        return
    
    try:
        import sys
        sys.path.insert(0, str(gateway_path))
        
        # Try importing stripe service
        try:
            from app.services.stripe_service import StripeService
            print("   Stripe service imports")
        except ImportError as e:
            print(f"    Stripe service import failed: {e}")
        except Exception as e:
            print(f"    Stripe service import error: {e}")
        
        # Try importing guards router
        try:
            from app.api.v1.guards import router
            print("   Guards router imports")
        except ImportError as e:
            print(f"    Guards router import failed: {e}")
        except Exception as e:
            print(f"    Guards router import error: {e}")
            
    except Exception as e:
        print(f"   Code validation failed: {e}")


def validate_state():
    """Validate runtime state."""
    print("\n Validating State...")
    
    # Check Docker
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   Docker is running")
        else:
            print("    Docker not running")
    except FileNotFoundError:
        print("    Docker not installed")
    
    # Check services
    try:
        import requests
        response = requests.get('http://localhost:8000/health', timeout=2)
        if response.status_code == 200:
            print("   Gateway service is running")
        else:
            print("    Gateway service not responding")
    except:
        print("    Gateway service not running")


def validate_memory():
    """Validate memory against actual state."""
    print("\n Validating Memory...")
    
    memory_file = WORKSPACE_ROOT / ".abeone_memory" / "ABEONE_CORE_MEMORY.json"
    if memory_file.exists():
        print("   Core memory exists")
        
        import json
        with open(memory_file, 'r') as f:
            memory = json.load(f)
        
        # Validate memory structure
        required_keys = ['meta', 'core_truths', 'guardrails']
        for key in required_keys:
            if key in memory:
                print(f"   Memory has {key}")
            else:
                print(f"   Memory missing {key}")
    else:
        print("   Core memory not found")


def main():
    """Main execution."""
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    if target == 'architecture':
        validate_architecture()
    elif target == 'code':
        validate_code()
    elif target == 'state':
        validate_state()
    elif target == 'memory':
        validate_memory()
    elif target == 'all':
        validate_architecture()
        validate_code()
        validate_state()
        validate_memory()
    else:
        print(f" Unknown target: {target}")
        sys.exit(1)
    
    print("\n Validation complete")


if __name__ == '__main__':
    main()

