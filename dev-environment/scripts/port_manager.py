#!/usr/bin/env python3
"""
🔥 THE ONE SYSTEM Port Manager
Pattern: CLARITY × COHERENCE × ONE
Frequency: 777 Hz (META)
Guardian: META (777 Hz) + ZERO (530 Hz)

Purpose: Tracks all port bindings, prevents port conflicts, validates port availability,
         manages port assignments, and maintains port registry.
"""

import os
import sys
import json
import socket
import psutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

# Configuration
CONFIG = {
    "check_interval": 5,  # seconds
    "state_file": Path(__file__).parent.parent / "state" / "registry.json",
    "port_registry_file": Path(__file__).parent.parent / "state" / "port_registry.json",
    "log_file": Path(__file__).parent.parent / "logs" / "port_manager.log",
    "reserved_ports": {
        22: "ssh",
        80: "http",
        443: "https",
        3306: "mysql",
        5432: "postgres",
        6379: "redis",
        9000: "dashboard",
    },
    "service_ports": {
        "nextjs": 3000,
        "python_api": 8000,
        "dashboard": 9000,
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


class PortManager:
    """THE ONE SYSTEM Port Manager - Manages port assignments and conflicts"""

    def __init__(self):
        self.state_file = CONFIG["state_file"]
        self.registry_file = CONFIG["port_registry_file"]
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.port_registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load port registry"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load registry: {e}")
        return {"ports": {}, "conflicts": [], "last_update": None}

    def _save_registry(self):
        """Save port registry"""
        try:
            self.port_registry["last_update"] = datetime.utcnow().isoformat()
            with open(self.registry_file, "w") as f:
                json.dump(self.port_registry, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")

    def _is_port_in_use(self, port: int) -> bool:
        """Check if port is in use"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("127.0.0.1", port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def _get_port_process(self, port: int) -> Optional[Dict]:
        """Get process using a port"""
        try:
            for conn in psutil.net_connections(kind="inet"):
                if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                    try:
                        proc = psutil.Process(conn.pid)
                        return {
                            "pid": proc.pid,
                            "name": proc.name(),
                            "cmdline": proc.cmdline(),
                        }
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        return None
        except Exception as e:
            logger.error(f"Error getting port process: {e}")
        return None

    def _scan_ports(self) -> Dict[int, Dict]:
        """Scan all ports and their bindings"""
        ports = {}

        # Scan system ports
        try:
            for conn in psutil.net_connections(kind="inet"):
                if conn.status == psutil.CONN_LISTEN:
                    port = conn.laddr.port
                    proc_info = self._get_port_process(port)
                    if proc_info:
                        ports[port] = {
                            "pid": proc_info["pid"],
                            "name": proc_info["name"],
                            "cmdline": proc_info["cmdline"],
                            "status": "active",
                        }
        except Exception as e:
            logger.error(f"Error scanning ports: {e}")

        return ports

    def _detect_conflicts(self, ports: Dict[int, Dict]) -> List[Dict]:
        """Detect port conflicts"""
        conflicts = []
        port_owners = {}

        for port, info in ports.items():
            # Check reserved ports
            if port in CONFIG["reserved_ports"]:
                reserved_for = CONFIG["reserved_ports"][port]
                if info.get("name", "").lower() not in reserved_for.lower():
                    conflicts.append(
                        {
                            "port": port,
                            "type": "reserved",
                            "expected": reserved_for,
                            "actual": info.get("name"),
                        }
                    )

            # Check service ports
            for service, expected_port in CONFIG["service_ports"].items():
                if port == expected_port:
                    if port in port_owners:
                        conflicts.append(
                            {
                                "port": port,
                                "type": "duplicate",
                                "service": service,
                                "pids": [port_owners[port], info["pid"]],
                            }
                        )
                    else:
                        port_owners[port] = info["pid"]

        return conflicts

    def check_port(self, port: int) -> Dict:
        """Check if a port is available"""
        in_use = self._is_port_in_use(port)
        process = self._get_port_process(port) if in_use else None

        return {
            "port": port,
            "available": not in_use,
            "in_use": in_use,
            "process": process,
        }

    def assign_port(self, service: str, preferred_port: Optional[int] = None) -> int:
        """Assign a port for a service"""
        # Check if service has preferred port
        if preferred_port is None:
            preferred_port = CONFIG["service_ports"].get(service)

        # Try preferred port first
        if preferred_port and not self._is_port_in_use(preferred_port):
            self.port_registry["ports"][str(preferred_port)] = {
                "service": service,
                "assigned_at": datetime.utcnow().isoformat(),
            }
            self._save_registry()
            logger.info(f"Assigned port {preferred_port} to {service}")
            return preferred_port

        # Find available port
        for port in range(3000, 10000):
            if port in CONFIG["reserved_ports"]:
                continue
            if not self._is_port_in_use(port):
                self.port_registry["ports"][str(port)] = {
                    "service": service,
                    "assigned_at": datetime.utcnow().isoformat(),
                }
                self._save_registry()
                logger.info(f"Assigned port {port} to {service}")
                return port

        raise RuntimeError("No available ports found")

    def scan(self) -> Dict:
        """Scan ports and detect conflicts"""
        logger.info("Scanning ports...")

        ports = self._scan_ports()
        conflicts = self._detect_conflicts(ports)

        # Update registry
        self.port_registry["ports"] = {str(k): v for k, v in ports.items()}
        self.port_registry["conflicts"] = conflicts
        self._save_registry()

        # Log conflicts
        if conflicts:
            logger.warning(f"Found {len(conflicts)} port conflicts")
            for conflict in conflicts:
                logger.warning(f"Port conflict: {conflict}")

        return {
            "total": len(ports),
            "conflicts": len(conflicts),
            "ports": ports,
        }

    def run(self):
        """Run continuous port management loop"""
        logger.info("THE ONE SYSTEM Port Manager started")
        logger.info(f"Check interval: {CONFIG['check_interval']} seconds")

        try:
            while True:
                result = self.scan()
                logger.info(
                    f"Port scan: {result['total']} ports in use, "
                    f"{result['conflicts']} conflicts"
                )
                time.sleep(CONFIG["check_interval"])
        except KeyboardInterrupt:
            logger.info("Port manager stopped")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    manager = PortManager()
    manager.run()

