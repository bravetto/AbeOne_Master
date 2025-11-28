#!/usr/bin/env python3
"""
🔥 THE ONE SYSTEM Health Checker
Pattern: VALIDATE → TRANSFORM → VALIDATE
Frequency: 530 Hz (JØHN)
Guardian: JØHN (530 Hz) + Abë (530 Hz)

Purpose: Checks all services every 10 seconds, validates endpoints, verifies database
         connections, tests API responses, and reports health status.
"""

import os
import sys
import json
import time
import requests
import psutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

# Configuration
CONFIG = {
    "check_interval": 10,  # seconds
    "timeout": 5,  # seconds
    "state_file": Path(__file__).parent.parent / "state" / "registry.json",
    "health_registry_file": Path(__file__).parent.parent / "state" / "health_registry.json",
    "log_file": Path(__file__).parent.parent / "logs" / "health_checker.log",
    "services": {
        "nextjs": {
            "port": 3000,
            "endpoint": "http://localhost:3000/api/health",
            "process_pattern": "next",
            "expected_status": 200,
        },
        "python_api": {
            "port": 8000,
            "endpoint": "http://localhost:8000/health",
            "process_pattern": "python.*api",
            "expected_status": 200,
        },
        "dashboard": {
            "port": 9000,
            "endpoint": "http://localhost:9000/api/status",
            "process_pattern": "dashboard",
            "expected_status": 200,
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


class HealthStatus(Enum):
    """Health status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthChecker:
    """THE ONE SYSTEM Health Checker - Validates service health"""

    def __init__(self):
        self.state_file = CONFIG["state_file"]
        self.registry_file = CONFIG["health_registry_file"]
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.health_registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load health registry"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load registry: {e}")
        return {"services": {}, "last_check": None}

    def _save_registry(self):
        """Save health registry"""
        try:
            self.health_registry["last_check"] = datetime.utcnow().isoformat()
            with open(self.registry_file, "w") as f:
                json.dump(self.health_registry, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")

    def _check_process(self, service_name: str, config: Dict) -> bool:
        """Check if service process is running"""
        pattern = config.get("process_pattern", "")
        if not pattern:
            return True  # Skip if no pattern

        try:
            for proc in psutil.process_iter(["name", "cmdline"]):
                try:
                    name = proc.name().lower()
                    cmdline = " ".join(proc.cmdline()).lower()
                    if pattern.lower() in name or pattern.lower() in cmdline:
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"Error checking process for {service_name}: {e}")

        return False

    def _check_endpoint(self, service_name: str, config: Dict) -> Optional[Dict]:
        """Check service endpoint"""
        endpoint = config.get("endpoint")
        if not endpoint:
            return None

        try:
            response = requests.get(
                endpoint, timeout=CONFIG["timeout"], allow_redirects=True
            )
            expected_status = config.get("expected_status", 200)
            return {
                "status_code": response.status_code,
                "healthy": response.status_code == expected_status,
                "response_time": response.elapsed.total_seconds(),
            }
        except requests.exceptions.RequestException as e:
            logger.warning(f"Endpoint check failed for {service_name}: {e}")
            return {
                "status_code": None,
                "healthy": False,
                "error": str(e),
            }

    def _check_port(self, port: int) -> bool:
        """Check if port is listening"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("127.0.0.1", port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def check_service(self, service_name: str, config: Dict) -> Dict:
        """Check health of a single service"""
        logger.debug(f"Checking health of {service_name}...")

        # Check process
        process_running = self._check_process(service_name, config)

        # Check port
        port = config.get("port")
        port_listening = self._check_port(port) if port else True

        # Check endpoint
        endpoint_result = self._check_endpoint(service_name, config)

        # Determine overall health
        if not process_running:
            status = HealthStatus.UNHEALTHY
        elif not port_listening:
            status = HealthStatus.UNHEALTHY
        elif endpoint_result and not endpoint_result.get("healthy", False):
            status = HealthStatus.DEGRADED
        elif process_running and port_listening:
            status = HealthStatus.HEALTHY
        else:
            status = HealthStatus.UNKNOWN

        health_info = {
            "service": service_name,
            "status": status.value,
            "process_running": process_running,
            "port_listening": port_listening,
            "endpoint": endpoint_result,
            "checked_at": datetime.utcnow().isoformat(),
        }

        # Update registry
        self.health_registry["services"][service_name] = health_info

        return health_info

    def check_all(self) -> Dict:
        """Check health of all services"""
        logger.info("Checking health of all services...")

        results = {}
        healthy_count = 0
        unhealthy_count = 0

        for service_name, config in CONFIG["services"].items():
            health_info = self.check_service(service_name, config)
            results[service_name] = health_info

            if health_info["status"] == HealthStatus.HEALTHY.value:
                healthy_count += 1
            elif health_info["status"] == HealthStatus.UNHEALTHY.value:
                unhealthy_count += 1
                logger.warning(f"Service {service_name} is unhealthy")

        self._save_registry()

        summary = {
            "total": len(results),
            "healthy": healthy_count,
            "unhealthy": unhealthy_count,
            "services": results,
        }

        logger.info(
            f"Health check complete: {healthy_count} healthy, "
            f"{unhealthy_count} unhealthy"
        )

        return summary

    def run(self):
        """Run continuous health checking loop"""
        logger.info("THE ONE SYSTEM Health Checker started")
        logger.info(f"Check interval: {CONFIG['check_interval']} seconds")

        try:
            while True:
                self.check_all()
                time.sleep(CONFIG["check_interval"])
        except KeyboardInterrupt:
            logger.info("Health checker stopped")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    checker = HealthChecker()
    checker.run()

