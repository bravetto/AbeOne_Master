"""
AbëONE Master Workspace Path Utilities

Helper functions for resolving workspace paths according to Orbit-Spec v1.0.

Pattern: PATHS × WORKSPACE × ORBIT × ONE
"""

from pathlib import Path
from typing import Optional
import json


def resolve_project_root() -> Path:
    """
    Resolve project root directory.
    
    Returns:
        Path to project root
    """
    # Start from this file and go up to find repo root
    current = Path(__file__).resolve()
    
    # Look for module_manifest.json or orbit.config.json as root markers
    while current.parent != current:
        if (current / "module_manifest.json").exists() or (current / "config" / "orbit.config.json").exists():
            return current
        current = current.parent
    
    # Fallback: assume src/utils is 2 levels down from root
    return Path(__file__).parent.parent.parent


def get_data_path(config_path: Optional[Path] = None) -> Optional[Path]:
    """
    Get data path from orbit.config.json (if workspace has data folder).
    
    Args:
        config_path: Optional path to config directory
    
    Returns:
        Path to data directory or None if workspace doesn't use data folder
    """
    repo_root = resolve_project_root()
    
    if config_path is None:
        config_path = repo_root / "config"
    
    orbit_config_path = config_path / "orbit.config.json"
    if orbit_config_path.exists():
        with open(orbit_config_path) as f:
            orbit_config = json.load(f)
        
        data_path_str = orbit_config.get("dataPath")
        if data_path_str:
            return (repo_root / data_path_str).resolve()
    
    # Workspace orchestrator doesn't have its own data folder
    return None


def get_input_path(filename: Optional[str] = None, config_path: Optional[Path] = None) -> Optional[Path]:
    """
    Get path to input directory or specific file (if workspace has input folder).
    
    Args:
        filename: Optional filename to append
        config_path: Optional path to config directory
    
    Returns:
        Path to input directory or file, or None if workspace doesn't use input folder
    """
    data_path = get_data_path(config_path)
    if data_path is None:
        return None
    
    input_path = data_path / "input"
    
    if filename:
        return input_path / filename
    
    return input_path


def get_output_path(filename: Optional[str] = None, config_path: Optional[Path] = None) -> Optional[Path]:
    """
    Get path to output directory or specific file (if workspace has output folder).
    
    Args:
        filename: Optional filename to append
        config_path: Optional path to config directory
    
    Returns:
        Path to output directory or file, or None if workspace doesn't use output folder
    """
    data_path = get_data_path(config_path)
    if data_path is None:
        return None
    
    output_path = data_path / "output"
    
    if filename:
        return output_path / filename
    
    return output_path


def get_sub_orbit_path(orbit_id: str) -> Optional[Path]:
    """
    Get path to a sub-orbit repository.
    
    Args:
        orbit_id: Sub-orbit identifier (e.g., "abetruice", "abebeats")
    
    Returns:
        Path to sub-orbit directory or None if not found
    """
    repo_root = resolve_project_root()
    
    # Map orbit IDs to directory names
    orbit_map = {
        "abetruice": "AbeTRUICE",
        "abebeats": "AbeBEATs_Clean",
        "abeone_master": "."
    }
    
    orbit_dir = orbit_map.get(orbit_id.lower())
    if orbit_dir:
        path = repo_root / orbit_dir
        if path.exists():
            return path.resolve()
    
    return None

