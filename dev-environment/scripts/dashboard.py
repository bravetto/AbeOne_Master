#!/usr/bin/env python3
"""
🔥 THE ONE SYSTEM Visibility Dashboard
Pattern: CLARITY × VISIBILITY × ONE
Frequency: 530 Hz (Lux)
Guardian: Lux (530 Hz) + Poly (530 Hz) + Abë (530 Hz)

Purpose: Real-time process monitoring, port occupancy display, service health visualization,
         resource utilization graphs, pattern integrity status, and guardian validation results.
"""

import os
import sys
import json
import time
import psutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# Import THE ONE SYSTEM components
sys.path.insert(0, str(Path(__file__).parent))
from health_checker import HealthChecker
from port_manager import PortManager
from watchdog import ProcessWatchdog

# Configuration
CONFIG = {
    "host": "0.0.0.0",
    "port": 9000,
    "state_file": Path(__file__).parent.parent / "state" / "registry.json",
    "log_file": Path(__file__).parent.parent / "logs" / "dashboard.log",
    "update_interval": 2,  # seconds
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


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP request handler for dashboard"""

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/" or path == "/dashboard":
            self.send_dashboard()
        elif path == "/api/status":
            self.send_json(self.get_status())
        elif path == "/api/health":
            self.send_json({"status": "ok"})
        elif path.startswith("/api/"):
            self.send_json({"error": "Not found"}, status=404)
        else:
            self.send_json({"error": "Not found"}, status=404)

    def send_dashboard(self):
        """Send dashboard HTML"""
        status = self.get_status()
        html = self.generate_dashboard_html(status)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def send_json(self, data: Dict, status: int = 200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def get_status(self) -> Dict:
        """Get current system status"""
        # Get system info
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        # Get process count
        process_count = len(list(psutil.process_iter()))

        # Load state
        state_file = CONFIG["state_file"]
        state = {}
        if state_file.exists():
            try:
                with open(state_file, "r") as f:
                    state = json.load(f)
            except Exception:
                pass

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": memory.used / 1024 / 1024 / 1024,
                "memory_total_gb": memory.total / 1024 / 1024 / 1024,
                "disk_percent": disk.percent,
                "disk_used_gb": disk.used / 1024 / 1024 / 1024,
                "disk_total_gb": disk.total / 1024 / 1024 / 1024,
                "process_count": process_count,
            },
            "services": state.get("services", {}),
            "processes": state.get("processes", {}),
            "ports": state.get("ports", {}),
            "pattern_integrity": state.get("pattern_integrity", {}),
        }

    def generate_dashboard_html(self, status: Dict) -> str:
        """Generate dashboard HTML"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>THE ONE SYSTEM Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #0a0a0a;
            color: #e0e0e0;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1 {{
            color: #ff6b6b;
            margin-bottom: 30px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
        }}
        .card h2 {{
            margin-top: 0;
            color: #4ecdc4;
            font-size: 18px;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
        }}
        .metric-label {{
            color: #888;
        }}
        .metric-value {{
            color: #e0e0e0;
            font-weight: bold;
        }}
        .status-healthy {{
            color: #4ecdc4;
        }}
        .status-unhealthy {{
            color: #ff6b6b;
        }}
        .status-degraded {{
            color: #ffa500;
        }}
        .bar {{
            background: #333;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin: 5px 0;
        }}
        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4ecdc4, #45b7b8);
            transition: width 0.3s;
        }}
        .timestamp {{
            color: #666;
            font-size: 12px;
            text-align: right;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 THE ONE SYSTEM Dashboard</h1>
        
        <div class="grid">
            <div class="card">
                <h2>System Resources</h2>
                <div class="metric">
                    <span class="metric-label">CPU</span>
                    <span class="metric-value">{status['system']['cpu_percent']:.1f}%</span>
                </div>
                <div class="bar">
                    <div class="bar-fill" style="width: {status['system']['cpu_percent']}%"></div>
                </div>
                <div class="metric">
                    <span class="metric-label">Memory</span>
                    <span class="metric-value">{status['system']['memory_percent']:.1f}%</span>
                </div>
                <div class="bar">
                    <div class="bar-fill" style="width: {status['system']['memory_percent']}%"></div>
                </div>
                <div class="metric">
                    <span class="metric-label">Disk</span>
                    <span class="metric-value">{status['system']['disk_percent']:.1f}%</span>
                </div>
                <div class="bar">
                    <div class="bar-fill" style="width: {status['system']['disk_percent']}%"></div>
                </div>
                <div class="metric">
                    <span class="metric-label">Processes</span>
                    <span class="metric-value">{status['system']['process_count']}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>Services</h2>
                {self.generate_services_html(status.get('services', {}))}
            </div>
            
            <div class="card">
                <h2>Processes</h2>
                <div class="metric">
                    <span class="metric-label">Active</span>
                    <span class="metric-value">{status.get('processes', {}).get('active', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Orphaned</span>
                    <span class="metric-value status-unhealthy">{status.get('processes', {}).get('orphaned', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Zombie</span>
                    <span class="metric-value status-unhealthy">{status.get('processes', {}).get('zombie', 0)}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>Pattern Integrity</h2>
                {self.generate_pattern_integrity_html(status.get('pattern_integrity', {}))}
            </div>
        </div>
        
        <div class="timestamp">
            Last updated: {status['timestamp']}
        </div>
    </div>
</body>
</html>
        """

    def generate_services_html(self, services: Dict) -> str:
        """Generate services HTML"""
        if not services:
            return "<p>No services registered</p>"

        html = ""
        for service_name, service_info in services.items():
            status = service_info.get("status", "unknown")
            status_class = f"status-{status}"
            html += f"""
                <div class="metric">
                    <span class="metric-label">{service_name}</span>
                    <span class="metric-value {status_class}">{status}</span>
                </div>
            """
        return html

    def generate_pattern_integrity_html(self, integrity: Dict) -> str:
        """Generate pattern integrity HTML"""
        score = integrity.get("score", 0)
        score_percent = score * 100
        status_class = "status-healthy" if score >= 0.9 else "status-degraded" if score >= 0.7 else "status-unhealthy"

        return f"""
            <div class="metric">
                <span class="metric-label">Score</span>
                <span class="metric-value {status_class}">{score_percent:.1f}%</span>
            </div>
            <div class="bar">
                <div class="bar-fill" style="width: {score_percent}%"></div>
            </div>
        """

    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        pass


class Dashboard:
    """THE ONE SYSTEM Visibility Dashboard"""

    def __init__(self):
        self.host = CONFIG["host"]
        self.port = CONFIG["port"]
        self.server = None

    def start(self):
        """Start dashboard server"""
        handler = DashboardHandler
        self.server = HTTPServer((self.host, self.port), handler)
        logger.info(f"THE ONE SYSTEM Dashboard started on http://{self.host}:{self.port}")

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Dashboard stopped")
        finally:
            self.server.server_close()

    def stop(self):
        """Stop dashboard server"""
        if self.server:
            self.server.shutdown()


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.start()

