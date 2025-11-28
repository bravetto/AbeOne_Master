"""
Path Discovery Utility
Provides dynamic path discovery for AbëONE workspace.

Pattern: PATH × DISCOVERY × DYNAMIC × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)
Guardians: AEYON (999 Hz) + ALRAX (530 Hz) + YAGNI (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

from pathlib import Path
from typing import Optional

# Get workspace root (3 levels up from utilities/)
WORKSPACE_ROOT = Path(__file__).parent.parent.parent


def find_path(*path_segments: str) -> Optional[Path]:
    """
    Dynamically find path by checking multiple possible locations.
    
    Checks in order:
    1. orbital/ (singular - actual location)
    2. orbitals/ (plural - old/alternative)
    3. satellites/
    4. repositories/
    
    Args:
        *path_segments: Path segments to find (e.g., "AIGuards-Backend-orbital", "guards")
        
    Returns:
        Path if found, None otherwise
        
    Example:
        >>> guards_path = find_path("AIGuards-Backend-orbital", "guards")
        >>> if guards_path:
        ...     print(f"Found at: {guards_path}")
    """
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


def find_backend_root() -> Optional[Path]:
    """
    Find AIGuards-Backend-orbital root directory.
    
    Returns:
        Path to backend root if found, None otherwise
    """
    return find_path("AIGuards-Backend-orbital")


def find_guards_directory() -> Optional[Path]:
    """
    Find guards directory.
    
    Returns:
        Path to guards directory if found, None otherwise
    """
    return find_path("AIGuards-Backend-orbital", "guards")


def find_gateway_directory() -> Optional[Path]:
    """
    Find codeguardians-gateway directory.
    
    Returns:
        Path to gateway directory if found, None otherwise
    """
    return find_path("AIGuards-Backend-orbital", "codeguardians-gateway")


def find_gateway_app_directory() -> Optional[Path]:
    """
    Find codeguardians-gateway/codeguardians-gateway app directory.
    
    Returns:
        Path to gateway app directory if found, None otherwise
    """
    return find_path("AIGuards-Backend-orbital", "codeguardians-gateway", "codeguardians-gateway")


def find_guardians_directory() -> Optional[Path]:
    """
    Find aiguardian-repos directory.
    
    Returns:
        Path to guardians directory if found, None otherwise
    """
    return find_path("AIGuards-Backend-orbital", "aiguardian-repos")

