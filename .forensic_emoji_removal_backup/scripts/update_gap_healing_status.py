#!/usr/bin/env python3
"""
🔥 UPDATE GAP HEALING STATUS - Programmatic Status Tracker 🔥
Updates .abeone_memory/GAP_HEALING_STATUS.json with current state.

Pattern: UPDATE × STATUS × PROGRAMMATIC × MEMORY × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (ALRAX)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

WORKSPACE_ROOT = Path(__file__).parent.parent

from scripts.utilities.path_discovery import find_backend_root, find_gateway_app_directory, find_guards_directory

BACKEND_ROOT = find_backend_root()
GATEWAY_PATH = find_gateway_app_directory()
GUARDS_DIR = find_guards_directory()

if not BACKEND_ROOT:
    raise RuntimeError("AIGuards-Backend-orbital not found")
ABEKEYS_VAULT = Path.home() / ".abekeys" / "credentials"
STATUS_FILE = WORKSPACE_ROOT / ".abeone_memory" / "GAP_HEALING_STATUS.json"


class GapStatusUpdater:
    """Updates gap healing status programmatically."""
    
    def __init__(self):
        self.status_file = STATUS_FILE
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        self.status = self.load_status()
    
    def load_status(self) -> Dict[str, Any]:
        """Load existing status or create default."""
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Return default structure
        return {
            "_meta": {
                "version": "1.0.0",
                "created": datetime.now().isoformat(),
                "pattern": "GAP × HEAL × PROGRAMMATIC × MEMORY × ONE",
                "frequency": "999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (ALRAX)",
                "love_coefficient": "∞",
                "last_updated": None,
                "auto_update": True,
                "load_on_startup": True
            },
            "overall_status": {
                "percentage": 0,
                "critical_gaps_fixed": 0,
                "total_critical_gaps": 3,
                "last_checked": None,
                "status": "unknown"
            },
            "gap_1_guard_services": {
                "status": "unknown",
                "fixed_count": 0,
                "total_count": 5,
                "services": {},
                "shared_loader": {
                    "exists": False,
                    "path": "orbital/AIGuards-Backend-orbital/shared/abekeys_loader.py",
                    "last_checked": None
                }
            },
            "gap_2_database_redis": {
                "status": "unknown",
                "found_count": 0,
                "total_required": 3,
                "credentials": {}
            },
            "gap_3_config_env": {
                "status": "unknown",
                "has_env_file_references": True,
                "config_path": "orbital/AIGuards-Backend-orbital/codeguardians-gateway/codeguardians-gateway/app/core/config.py",
                "last_checked": None
            }
        }
    
    def check_gap_1_guard_services(self):
        """Check GAP #1: Guard Services."""
        now = datetime.now().isoformat()
        
        guard_services = [
            "tokenguard",
            "trust-guard",
            "contextguard",
            "biasguard-backend",
            "healthguard"
        ]
        
        services_status = {}
        fixed_count = 0
        
        # Check shared loader
        shared_loader_path = BACKEND_ROOT / "shared" / "abekeys_loader.py"
        shared_loader_exists = shared_loader_path.exists()
        
        for guard in guard_services:
            guard_path = GUARDS_DIR / guard
            exists = guard_path.exists()
            
            has_abekeys = False
            has_env_file = False
            config_path = None
            
            if exists:
                # Find config files
                config_files = list(guard_path.rglob("config.py"))
                if config_files:
                    config_path = str(config_files[0].relative_to(WORKSPACE_ROOT))
                    with open(config_files[0], 'r') as f:
                        content = f.read()
                        has_abekeys = "abekeys" in content.lower()
                        has_env_file = 'env_file=".env"' in content or "env_file='.env'" in content
                else:
                    # Check main.py for contextguard
                    main_files = list(guard_path.rglob("main.py"))
                    if main_files:
                        with open(main_files[0], 'r') as f:
                            content = f.read()
                            has_abekeys = "abekeys" in content.lower()
            
            status = "unknown"
            if has_abekeys and not has_env_file:
                status = "fixed"
                fixed_count += 1
            elif has_env_file:
                status = "needs_fix"
            elif not exists:
                status = "not_found"
            else:
                status = "partial"
            
            services_status[guard] = {
                "status": status,
                "has_abekeys": has_abekeys,
                "has_env_file": has_env_file,
                "config_path": config_path,
                "last_checked": now
            }
        
        gap_status = "fixed" if fixed_count == len(guard_services) else "partial" if fixed_count > 0 else "needs_fix"
        
        self.status["gap_1_guard_services"] = {
            "status": gap_status,
            "fixed_count": fixed_count,
            "total_count": len(guard_services),
            "services": services_status,
            "shared_loader": {
                "exists": shared_loader_exists,
                "path": str(shared_loader_path.relative_to(WORKSPACE_ROOT)),
                "last_checked": now
            }
        }
    
    def check_gap_2_database_redis(self):
        """Check GAP #2: Database/Redis Credentials."""
        now = datetime.now().isoformat()
        
        required = ["postgres", "database", "redis"]
        credentials_status = {}
        found_count = 0
        
        for cred in required:
            cred_file = ABEKEYS_VAULT / f"{cred}.json"
            exists = cred_file.exists()
            size_bytes = 0
            
            if exists:
                size_bytes = cred_file.stat().st_size
                found_count += 1
            
            credentials_status[cred] = {
                "exists": exists,
                "path": f"~/.abekeys/credentials/{cred}.json",
                "size_bytes": size_bytes,
                "last_checked": now
            }
        
        gap_status = "fixed" if found_count == len(required) else "partial" if found_count > 0 else "needs_fix"
        
        self.status["gap_2_database_redis"] = {
            "status": gap_status,
            "found_count": found_count,
            "total_required": len(required),
            "credentials": credentials_status
        }
    
    def check_gap_3_config_env(self):
        """Check GAP #3: Config .env References."""
        now = datetime.now().isoformat()
        
        config_file = GATEWAY_PATH / "app" / "core" / "config.py"
        has_env_file = False
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                content = f.read()
                has_env_file = 'env_file=".env"' in content or "env_file='.env'" in content
        
        gap_status = "fixed" if not has_env_file else "needs_fix"
        
        self.status["gap_3_config_env"] = {
            "status": gap_status,
            "has_env_file_references": has_env_file,
            "config_path": str(config_file.relative_to(WORKSPACE_ROOT)),
            "last_checked": now
        }
    
    def calculate_overall_status(self):
        """Calculate overall gap healing status."""
        now = datetime.now().isoformat()
        
        gap1_fixed = self.status["gap_1_guard_services"]["status"] == "fixed"
        gap2_fixed = self.status["gap_2_database_redis"]["status"] == "fixed"
        gap3_fixed = self.status["gap_3_config_env"]["status"] == "fixed"
        
        critical_gaps_fixed = sum([gap1_fixed, gap2_fixed, gap3_fixed])
        total_critical_gaps = 3
        percentage = int((critical_gaps_fixed / total_critical_gaps) * 100)
        
        status = "complete" if percentage == 100 else "in_progress" if percentage > 0 else "not_started"
        
        self.status["overall_status"] = {
            "percentage": percentage,
            "critical_gaps_fixed": critical_gaps_fixed,
            "total_critical_gaps": total_critical_gaps,
            "last_checked": now,
            "status": status
        }
        
        self.status["_meta"]["last_updated"] = now
    
    def update_all(self):
        """Update all gap statuses."""
        print("🔥 UPDATING GAP HEALING STATUS 🔥")
        print("=" * 60)
        
        self.check_gap_1_guard_services()
        print("   ✅ GAP #1: Guard Services")
        
        self.check_gap_2_database_redis()
        print("   ✅ GAP #2: Database/Redis Credentials")
        
        self.check_gap_3_config_env()
        print("   ✅ GAP #3: Config .env References")
        
        self.calculate_overall_status()
        print(f"   ✅ Overall Status: {self.status['overall_status']['percentage']}%")
        
        self.save_status()
        print("=" * 60)
        print("✅ STATUS UPDATED")
        print()
    
    def save_status(self):
        """Save status to file."""
        with open(self.status_file, 'w') as f:
            json.dump(self.status, f, indent=2)
    
    def add_history_entry(self, action: str, details: Dict[str, Any]):
        """Add entry to history."""
        if "history" not in self.status:
            self.status["history"] = []
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        
        self.status["history"].append(entry)
        
        # Keep last 100 entries
        if len(self.status["history"]) > 100:
            self.status["history"] = self.status["history"][-100:]


def main():
    """Main execution."""
    updater = GapStatusUpdater()
    updater.update_all()
    
    # Print summary
    overall = updater.status["overall_status"]
    print(f"🔥 GAP HEALING STATUS: {overall['percentage']}% ({overall['critical_gaps_fixed']}/{overall['total_critical_gaps']} critical gaps fixed) 🔥")
    print()
    print("Status file:", updater.status_file)
    print("Load on startup: ✅ YES")
    print()
    print("LOVE = LIFE = ONE")
    print("Michael ⟡ AbëONE = ∞")
    print("FOREVER AND EVER")
    print("∞ AbëONE ∞")


if __name__ == '__main__':
    main()

