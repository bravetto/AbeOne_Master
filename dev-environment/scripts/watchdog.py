#!/usr/bin/env python3
"""
🔥 THE ONE SYSTEM Process Watchdog
Pattern: OBSERVER × TRUTH × ATOMIC × ONE
Frequency: 530 Hz (JØHN)
Guardian: JØHN (530 Hz) + ALRAX (530 Hz)

Purpose: Tracks all project processes, validates parent-child relationships,
         detects zombie processes, prevents process leaks, and maintains process registry.
"""

import os
import sys
import json
import time
import psutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import defaultdict

# Configuration
CONFIG = {
    "check_interval": 10,  # seconds
    "state_file": Path(__file__).parent.parent / "state" / "registry.json",
    "log_file": Path(__file__).parent.parent / "logs" / "watchdog.log",
    "process_registry_file": Path(__file__).parent.parent / "state" / "process_registry.json",
    "project_paths": [
        "/home/user/AbeOne_Master",
        "/home/user/AbeOne_Master/AIGuards-Backend",
        "/home/user/AbeOne_Master/AIGuards-Backend-orbital",
    ],
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(CONFIG["log_file"]),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


class ProcessWatchdog:
    """THE ONE SYSTEM Process Watchdog - Monitors process tree integrity"""

    def __init__(self):
        self.state_file = CONFIG["state_file"]
        self.registry_file = CONFIG["process_registry_file"]
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.process_registry = self._load_registry()
        self.process_tree = {}

    def _load_registry(self) -> Dict:
        """Load process registry"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load registry: {e}")
        return {"processes": {}, "tree": {}, "last_update": None}

    def _save_registry(self):
        """Save process registry"""
        try:
            self.process_registry["last_update"] = datetime.utcnow().isoformat()
            with open(self.registry_file, "w") as f:
                json.dump(self.process_registry, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")

    def _is_project_process(self, proc: psutil.Process) -> bool:
        """Check if process belongs to project"""
        try:
            cwd = proc.cwd()
            for project_path in CONFIG["project_paths"]:
                if cwd.startswith(project_path):
                    return True
            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def _get_process_info(self, proc: psutil.Process) -> Optional[Dict]:
        """Get process information"""
        try:
            return {
                "pid": proc.pid,
                "ppid": proc.ppid(),
                "name": proc.name(),
                "status": proc.status(),
                "create_time": proc.create_time(),
                "cwd": proc.cwd(),
                "cmdline": proc.cmdline(),
                "memory_mb": proc.memory_info().rss / 1024 / 1024,
                "cpu_percent": proc.cpu_percent(interval=0.1),
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def _detect_zombies(self) -> List[int]:
        """Detect zombie processes"""
        zombies = []
        try:
            for proc in psutil.process_iter(["pid", "status"]):
                try:
                    if proc.status() == psutil.STATUS_ZOMBIE:
                        if self._is_project_process(proc):
                            zombies.append(proc.pid)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"Error detecting zombies: {e}")
        return zombies

    def _validate_tree(self) -> Dict:
        """Validate process tree integrity"""
        tree = defaultdict(list)
        orphans = []
        leaks = []

        try:
            for proc in psutil.process_iter(["pid", "ppid"]):
                try:
                    if not self._is_project_process(proc):
                        continue

                    pid = proc.pid
                    ppid = proc.ppid()

                    # Build tree
                    tree[ppid].append(pid)

                    # Check for orphans (PPID=1 but not init)
                    if ppid == 1 and pid != 1:
                        orphans.append(pid)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Detect leaks (processes with no parent in registry)
            registered_pids = set(self.process_registry.get("processes", {}).keys())
            for ppid, children in tree.items():
                if ppid not in registered_pids and ppid != 1:
                    leaks.extend(children)

        except Exception as e:
            logger.error(f"Error validating tree: {e}")

        return {
            "tree": dict(tree),
            "orphans": orphans,
            "leaks": leaks,
            "zombies": self._detect_zombies(),
        }

    def scan(self) -> Dict:
        """Scan and update process registry"""
        logger.info("Scanning processes...")

        processes = {}
        tree_info = self._validate_tree()

        try:
            for proc in psutil.process_iter():
                try:
                    if not self._is_project_process(proc):
                        continue

                    info = self._get_process_info(proc)
                    if info:
                        processes[str(proc.pid)] = info

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        except Exception as e:
            logger.error(f"Error scanning processes: {e}")

        # Update registry
        self.process_registry["processes"] = processes
        self.process_registry["tree"] = tree_info["tree"]

        # Log issues
        if tree_info["orphans"]:
            logger.warning(f"Found {len(tree_info['orphans'])} orphaned processes")
        if tree_info["leaks"]:
            logger.warning(f"Found {len(tree_info['leaks'])} process leaks")
        if tree_info["zombies"]:
            logger.warning(f"Found {len(tree_info['zombies'])} zombie processes")

        self._save_registry()

        return {
            "total": len(processes),
            "orphans": len(tree_info["orphans"]),
            "leaks": len(tree_info["leaks"]),
            "zombies": len(tree_info["zombies"]),
        }

    def run(self):
        """Run continuous watchdog loop"""
        logger.info("THE ONE SYSTEM Process Watchdog started")
        logger.info(f"Check interval: {CONFIG['check_interval']} seconds")

        try:
            while True:
                result = self.scan()
                logger.info(
                    f"Watchdog scan: {result['total']} processes, "
                    f"{result['orphans']} orphans, {result['leaks']} leaks, "
                    f"{result['zombies']} zombies"
                )
                time.sleep(CONFIG["check_interval"])
        except KeyboardInterrupt:
            logger.info("Watchdog stopped")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    watchdog = ProcessWatchdog()
    watchdog.run()

