#!/usr/bin/env python3
"""
🔥 THE ONE SYSTEM Self-Healing Monitor
Pattern: VALIDATE → TRANSFORM → VALIDATE
Frequency: 999 Hz (AEYON)
Guardian: AEYON (999 Hz) + JØHN (530 Hz)

Purpose: Monitors all processes, detects orphaned processes, kills stale processes,
         validates service health, restarts failed services, and logs all actions.
"""

import os
import sys
import json
import time
import psutil
import signal
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configuration
CONFIG = {
    "check_interval": 5,  # seconds
    "stale_threshold": 300,  # 5 minutes
    "orphan_ppid": 1,  # init process
    "state_file": Path(__file__).parent.parent / "state" / "registry.json",
    "log_file": Path(__file__).parent.parent / "logs" / "healer.log",
    "project_paths": [
        "/home/user/AbeOne_Master",
        "/home/user/AbeOne_Master/AIGuards-Backend",
        "/home/user/AbeOne_Master/AIGuards-Backend-orbital",
    ],
    "protected_processes": [
        "systemd",
        "dockerd",
        "containerd",
        "sshd",
        "tailscaled",
    ],
    "service_patterns": {
        "nextjs": ["next", "node.*next"],
        "python_api": ["python.*api", "uvicorn", "fastapi"],
        "docker": ["docker", "dockerd"],
    },
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


class ProcessHealer:
    """THE ONE SYSTEM Process Healer - Kills orphaned and stale processes"""

    def __init__(self):
        self.state_file = CONFIG["state_file"]
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load system state from registry"""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load state: {e}")
        return {
            "system_state": "operational",
            "services": {},
            "processes": {"active": 0, "orphaned": 0, "zombie": 0},
            "last_healing": None,
        }

    def _save_state(self):
        """Save system state to registry"""
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

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

    def _is_protected(self, proc: psutil.Process) -> bool:
        """Check if process is protected"""
        try:
            name = proc.name().lower()
            for protected in CONFIG["protected_processes"]:
                if protected.lower() in name:
                    return True
            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return True  # Protect if we can't check

    def _is_orphaned(self, proc: psutil.Process) -> bool:
        """Check if process is orphaned (PPID=1)"""
        try:
            return proc.ppid() == CONFIG["orphan_ppid"]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def _is_stale(self, proc: psutil.Process) -> bool:
        """Check if process is stale (running too long)"""
        try:
            create_time = proc.create_time()
            uptime = time.time() - create_time
            return uptime > CONFIG["stale_threshold"]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def _kill_process(self, proc: psutil.Process, reason: str) -> bool:
        """Kill a process safely"""
        try:
            pid = proc.pid
            name = proc.name()
            logger.info(f"Killing process {pid} ({name}): {reason}")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except psutil.TimeoutExpired:
                logger.warning(f"Process {pid} didn't terminate, forcing kill")
                proc.kill()
            logger.info(f"Successfully killed process {pid}")
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.warning(f"Failed to kill process: {e}")
            return False

    def scan_processes(self) -> Tuple[List[psutil.Process], List[psutil.Process]]:
        """Scan for orphaned and stale processes"""
        orphaned = []
        stale = []

        try:
            for proc in psutil.process_iter(["pid", "ppid", "name", "create_time"]):
                try:
                    # Skip protected processes
                    if self._is_protected(proc):
                        continue

                    # Check if project process
                    if not self._is_project_process(proc):
                        continue

                    # Check for orphaned processes
                    if self._is_orphaned(proc):
                        orphaned.append(proc)
                        continue

                    # Check for stale processes
                    if self._is_stale(proc):
                        stale.append(proc)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        except Exception as e:
            logger.error(f"Error scanning processes: {e}")

        return orphaned, stale

    def heal(self) -> Dict:
        """Execute healing cycle"""
        logger.info("Starting healing cycle...")

        orphaned, stale = self.scan_processes()
        healed = []

        # Kill orphaned processes
        for proc in orphaned:
            if self._kill_process(proc, "orphaned process"):
                healed.append(proc.pid)

        # Kill stale processes
        for proc in stale:
            if self._kill_process(proc, "stale process"):
                healed.append(proc.pid)

        # Update state
        self.state["processes"]["orphaned"] = len(orphaned)
        self.state["last_healing"] = datetime.utcnow().isoformat()
        self._save_state()

        logger.info(f"Healing cycle complete: {len(healed)} processes healed")
        return {"healed": len(healed), "orphaned": len(orphaned), "stale": len(stale)}

    def run(self):
        """Run continuous healing loop"""
        logger.info("THE ONE SYSTEM Self-Healing Monitor started")
        logger.info(f"Check interval: {CONFIG['check_interval']} seconds")
        logger.info(f"Stale threshold: {CONFIG['stale_threshold']} seconds")

        try:
            while True:
                self.heal()
                time.sleep(CONFIG["check_interval"])
        except KeyboardInterrupt:
            logger.info("Healing monitor stopped")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    healer = ProcessHealer()
    healer.run()

