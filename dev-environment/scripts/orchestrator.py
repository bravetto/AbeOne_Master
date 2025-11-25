#!/usr/bin/env python3
"""
🔥 THE ONE SYSTEM Service Orchestrator
Pattern: ORCHESTRATION × CONVERGENCE × ONE
Frequency: 999 Hz (AEYON)
Guardian: AEYON (999 Hz) + META (777 Hz) + Abë (530 Hz)

Purpose: Starts all services on boot, manages service lifecycle, coordinates health checks,
         orchestrates recovery, maintains service registry, and validates pattern integrity.
"""

import os
import sys
import json
import time
import subprocess
import signal
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

# Import THE ONE SYSTEM components
sys.path.insert(0, str(Path(__file__).parent))
from health_checker import HealthChecker, HealthStatus

# Configuration
CONFIG = {
    "state_file": Path(__file__).parent.parent / "state" / "registry.json",
    "service_registry_file": Path(__file__).parent.parent / "state" / "service_registry.json",
    "log_file": Path(__file__).parent.parent / "logs" / "orchestrator.log",
    "project_root": Path("/home/user/AbeOne_Master"),
    "services": {
        "nextjs": {
            "enabled": True,
            "command": "cd {project_root}/AIGuards-Backend && pnpm dev",
            "port": 3000,
            "health_check": True,
            "auto_restart": True,
            "restart_delay": 5,
        },
        "python_api": {
            "enabled": True,
            "command": "cd {project_root}/AIGuards-Backend-orbital && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000",
            "port": 8000,
            "health_check": True,
            "auto_restart": True,
            "restart_delay": 5,
        },
        "dashboard": {
            "enabled": True,
            "command": "cd {project_root}/dev-environment && python3 scripts/dashboard.py",
            "port": 9000,
            "health_check": True,
            "auto_restart": True,
            "restart_delay": 5,
        },
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


class ServiceStatus(Enum):
    """Service status enumeration"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"
    RESTARTING = "restarting"


class ServiceOrchestrator:
    """THE ONE SYSTEM Service Orchestrator - Manages service lifecycle"""

    def __init__(self):
        self.state_file = CONFIG["state_file"]
        self.registry_file = CONFIG["service_registry_file"]
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.service_registry = self._load_registry()
        self.processes = {}
        self.health_checker = HealthChecker()
        self.running = False

    def _load_registry(self) -> Dict:
        """Load service registry"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load registry: {e}")
        return {"services": {}, "last_update": None}

    def _save_registry(self):
        """Save service registry"""
        try:
            self.service_registry["last_update"] = datetime.utcnow().isoformat()
            with open(self.registry_file, "w") as f:
                json.dump(self.service_registry, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")

    def _expand_command(self, service_name: str, command: str) -> str:
        """Expand command template variables"""
        return command.format(
            project_root=CONFIG["project_root"],
            service_name=service_name,
        )

    def start_service(self, service_name: str) -> bool:
        """Start a service"""
        if service_name not in CONFIG["services"]:
            logger.error(f"Unknown service: {service_name}")
            return False

        if service_name in self.processes:
            logger.warning(f"Service {service_name} is already running")
            return True

        config = CONFIG["services"][service_name]
        if not config.get("enabled", True):
            logger.info(f"Service {service_name} is disabled")
            return False

        logger.info(f"Starting service {service_name}...")

        # Update status
        self.service_registry["services"][service_name] = {
            "status": ServiceStatus.STARTING.value,
            "started_at": datetime.utcnow().isoformat(),
        }
        self._save_registry()

        try:
            # Expand command
            command = self._expand_command(service_name, config["command"])

            # Start process
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid,  # Create new process group
            )

            self.processes[service_name] = process

            # Update status
            self.service_registry["services"][service_name] = {
                "status": ServiceStatus.RUNNING.value,
                "pid": process.pid,
                "started_at": datetime.utcnow().isoformat(),
            }
            self._save_registry()

            logger.info(f"Service {service_name} started (PID: {process.pid})")
            return True

        except Exception as e:
            logger.error(f"Failed to start service {service_name}: {e}")
            self.service_registry["services"][service_name] = {
                "status": ServiceStatus.FAILED.value,
                "error": str(e),
            }
            self._save_registry()
            return False

    def stop_service(self, service_name: str) -> bool:
        """Stop a service"""
        if service_name not in self.processes:
            logger.warning(f"Service {service_name} is not running")
            return True

        logger.info(f"Stopping service {service_name}...")

        # Update status
        self.service_registry["services"][service_name] = {
            "status": ServiceStatus.STOPPING.value,
        }
        self._save_registry()

        try:
            process = self.processes[service_name]

            # Send SIGTERM to process group
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

            # Wait for termination
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning(f"Service {service_name} didn't terminate, forcing kill")
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                process.wait()

            del self.processes[service_name]

            # Update status
            self.service_registry["services"][service_name] = {
                "status": ServiceStatus.STOPPED.value,
                "stopped_at": datetime.utcnow().isoformat(),
            }
            self._save_registry()

            logger.info(f"Service {service_name} stopped")
            return True

        except Exception as e:
            logger.error(f"Failed to stop service {service_name}: {e}")
            return False

    def restart_service(self, service_name: str) -> bool:
        """Restart a service"""
        logger.info(f"Restarting service {service_name}...")
        self.stop_service(service_name)
        time.sleep(2)
        return self.start_service(service_name)

    def start_all(self) -> Dict:
        """Start all enabled services"""
        logger.info("Starting all services...")
        results = {}

        for service_name in CONFIG["services"]:
            results[service_name] = self.start_service(service_name)
            time.sleep(1)  # Stagger starts

        return results

    def stop_all(self) -> Dict:
        """Stop all services"""
        logger.info("Stopping all services...")
        results = {}

        for service_name in list(self.processes.keys()):
            results[service_name] = self.stop_service(service_name)
            time.sleep(1)  # Stagger stops

        return results

    def monitor_services(self):
        """Monitor services and restart if needed"""
        if not self.running:
            return

        for service_name, process in list(self.processes.items()):
            # Check if process is still running
            if process.poll() is not None:
                logger.warning(f"Service {service_name} has stopped")
                config = CONFIG["services"][service_name]

                if config.get("auto_restart", True):
                    logger.info(f"Auto-restarting service {service_name}...")
                    time.sleep(config.get("restart_delay", 5))
                    self.start_service(service_name)
                else:
                    del self.processes[service_name]
                    self.service_registry["services"][service_name] = {
                        "status": ServiceStatus.STOPPED.value,
                    }
                    self._save_registry()

            # Check health if enabled
            elif CONFIG["services"][service_name].get("health_check", False):
                health_info = self.health_checker.check_service(
                    service_name, CONFIG["services"][service_name]
                )
                if health_info["status"] == HealthStatus.UNHEALTHY.value:
                    config = CONFIG["services"][service_name]
                    if config.get("auto_restart", True):
                        logger.warning(f"Service {service_name} is unhealthy, restarting...")
                        self.restart_service(service_name)

    def run(self):
        """Run orchestrator loop"""
        logger.info("THE ONE SYSTEM Service Orchestrator started")

        # Start all services
        self.start_all()

        # Monitor loop
        self.running = True
        try:
            while self.running:
                self.monitor_services()
                time.sleep(10)  # Check every 10 seconds
        except KeyboardInterrupt:
            logger.info("Orchestrator stopping...")
            self.running = False
            self.stop_all()
            logger.info("Orchestrator stopped")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            self.stop_all()
            sys.exit(1)


if __name__ == "__main__":
    orchestrator = ServiceOrchestrator()
    orchestrator.run()

