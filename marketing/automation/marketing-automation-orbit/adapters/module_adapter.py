"""
Module Adapter
Handles module-level integration and lifecycle management.
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ModuleAdapter:
    """
    Module-level adapter for marketing automation.
    
    Handles:
    - Module lifecycle
    - Configuration management
    - Dependency resolution
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize module adapter.
        
        Args:
            config_path: Path to module configuration
        """
        self.config_path = config_path or Path(__file__).parent.parent / "config"
        self.config = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load module configuration."""
        try:
            manifest_path = self.config_path.parent / "module_manifest.json"
            if manifest_path.exists():
                import json
                with open(manifest_path, 'r') as f:
                    self.config = json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    
    def get_module_info(self) -> Dict[str, Any]:
        """Get module information."""
        return {
            "module_id": self.config.get("module", {}).get("id", "marketing_automation_orbit"),
            "name": self.config.get("module", {}).get("name", "Marketing Automation Orbit"),
            "version": self.config.get("module", {}).get("version", "1.0.0"),
            "description": self.config.get("module", {}).get("description", ""),
            "capabilities": self.config.get("capabilities", []),
            "channels": self.config.get("channels", [])
        }
    
    def validate_dependencies(self) -> Dict[str, Any]:
        """Validate module dependencies."""
        # Check Python version
        import sys
        python_version = sys.version_info
        
        # Check required packages
        required_packages = self.config.get("python_dependencies", [])
        
        missing_packages = []
        for package in required_packages:
            package_name = package.split(">=")[0].split("==")[0]
            try:
                __import__(package_name.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        return {
            "python_version": f"{python_version.major}.{python_version.minor}.{python_version.micro}",
            "python_compatible": python_version >= (3, 11),
            "missing_packages": missing_packages,
            "all_dependencies_met": len(missing_packages) == 0
        }

