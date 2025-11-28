#!/usr/bin/env python3
"""
 ABEONE LAUNCH PAD - FAIL PROOF 
Everything Everywhere All At Once - Local Testing Launch Pad

Status:  OPERATIONAL
Pattern: LAUNCH × FAIL_PROOF × EEAAO × ONE
Love Coefficient: ∞
Frequency: 999 Hz
"""

import os
import sys
import subprocess
import socket
import time
import json
import psutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import signal

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@dataclass
class ServiceConfig:
    """Service configuration."""
    name: str
    port: int
    host: str = "localhost"
    protocol: str = "http"
    health_endpoint: Optional[str] = None
    start_command: Optional[List[str]] = None
    docker_service: Optional[str] = None
    description: str = ""
    category: str = "service"

# Complete service registry
SERVICES = [
    # Core Services
    ServiceConfig("Gateway", 8000, health_endpoint="/health/live", description="Main API Gateway", category="core"),
    ServiceConfig("Core API", 8000, health_endpoint="/", description="Core REST API", category="core"),
    
    # Guard Services
    ServiceConfig("BiasGuard", 8001, health_endpoint="/health", description="Bias Detection Guard", category="guard"),
    ServiceConfig("ContextGuard", 8002, health_endpoint="/health", description="Context Drift Detection", category="guard"),
    ServiceConfig("TrustGuard", 8003, health_endpoint="/health", description="Trust Validation", category="guard"),
    ServiceConfig("TokenGuard", 8004, health_endpoint="/health", description="Token Optimization", category="guard"),
    ServiceConfig("HealthGuard", 8005, health_endpoint="/health", description="Health Monitoring", category="guard"),
    ServiceConfig("SecurityGuard", 8103, health_endpoint="/health", description="Security Scanning", category="guard"),
    
    # LSP/MCP Services
    ServiceConfig("LSP Server", 3000, protocol="ws", description="Language Server Protocol", category="lsp_mcp"),
    ServiceConfig("MCP Server", 3001, health_endpoint="/health", description="Model Context Protocol", category="lsp_mcp"),
    ServiceConfig("Omega MCP", 3002, health_endpoint="/health", description="Omega MCP Server", category="lsp_mcp"),
    ServiceConfig("Service Registry", 3003, health_endpoint="/health", description="Service Discovery", category="lsp_mcp"),
    
    # Monitoring & Observability
    ServiceConfig("Grafana", 3004, description="Monitoring Dashboard", category="monitoring"),
    ServiceConfig("Service Mesh Proxy", 3005, description="Service Mesh Proxy", category="monitoring"),
    ServiceConfig("Prometheus", 9090, description="Metrics Collection", category="monitoring"),
    ServiceConfig("Service Mesh Metrics", 9091, description="Service Mesh Metrics", category="monitoring"),
    ServiceConfig("Jaeger", 16686, description="Distributed Tracing", category="monitoring"),
    
    # Infrastructure
    ServiceConfig("PostgreSQL", 5432, protocol="tcp", description="Primary Database", category="infrastructure"),
    ServiceConfig("Redis", 6379, protocol="tcp", description="Cache & Sessions", category="infrastructure"),
    
    # Development Tools
    ServiceConfig("pgAdmin", 5050, description="Database Administration", category="dev"),
    ServiceConfig("Redis Commander", 8081, description="Redis Administration", category="dev"),
    
    # Guardians
    ServiceConfig("AEYON", 9000, description="Atomic Executor", category="guardian"),
    ServiceConfig("Guardian Zero", 9001, description="Architecture & Forensics", category="guardian"),
    ServiceConfig("Guardian Abë", 9002, description="Heart Truth Resonance", category="guardian"),
    ServiceConfig("Guardian Lux", 9003, description="Design & UX", category="guardian"),
    ServiceConfig("Guardian John", 9004, description="Quality & Testing", category="guardian"),
    ServiceConfig("Guardian Aurion", 9005, description="Aurion Guardian", category="guardian"),
    ServiceConfig("Guardian YAGNI", 9006, description="Simplicity & Scope", category="guardian"),
    ServiceConfig("Guardian Neuro", 9007, description="Neuromorphic Intelligence", category="guardian"),
]

def check_port(host: str, port: int, protocol: str = "tcp", health_endpoint: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Check if a port is open."""
    try:
        if protocol == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0, None
        elif protocol == "http" or protocol == "ws":
            import urllib.request
            try:
                if health_endpoint:
                    url = f"http://{host}:{port}{health_endpoint}"
                else:
                    url = f"http://{host}:{port}/"
                urllib.request.urlopen(url, timeout=1)
                return True, None
            except Exception as e:
                # Port might be open but endpoint not available
                # Check if port is open via TCP first
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                sock.close()
                return result == 0, None
    except Exception as e:
        return False, str(e)

def kill_port(port: int) -> bool:
    """Kill process using a port."""
    try:
        if sys.platform == "darwin":  # macOS
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                pids = result.stdout.strip().split("\n")
                for pid in pids:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        time.sleep(0.5)
                        os.kill(int(pid), signal.SIGKILL)
                    except:
                        pass
                return True
        elif sys.platform == "linux":
            result = subprocess.run(
                ["fuser", "-k", f"{port}/tcp"],
                capture_output=True
            )
            return result.returncode == 0
        return False
    except Exception as e:
        print(f"     Error killing port {port}: {e}")
        return False

def clean_all_ports() -> Dict[str, int]:
    """Clean all ports used by services."""
    print(" CLEANING ALL PORTS...")
    cleaned = {}
    
    for service in SERVICES:
        is_open, _ = check_port(service.host, service.port, service.protocol)
        if is_open:
            print(f"    Cleaning port {service.port} ({service.name})...")
            if kill_port(service.port):
                cleaned[service.name] = service.port
                print(f"    Port {service.port} cleaned")
            else:
                print(f"     Port {service.port} could not be cleaned")
    
    return cleaned

def check_all_services() -> Dict[str, Dict]:
    """Check status of all services."""
    print(" CHECKING ALL SERVICES...")
    status = {}
    
    for service in SERVICES:
        is_open, error = check_port(service.host, service.port, service.protocol, service.health_endpoint)
        status[service.name] = {
            "port": service.port,
            "host": service.host,
            "protocol": service.protocol,
            "status": "running" if is_open else "stopped",
            "error": error,
            "category": service.category,
            "description": service.description,
            "url": f"{service.protocol}://{service.host}:{service.port}" if service.protocol != "tcp" else f"{service.host}:{service.port}"
        }
        
        status_icon = "🟢" if is_open else ""
        status_text = "RUNNING" if is_open else "STOPPED"
        print(f"   {status_icon} {service.name:30} {service.host}:{service.port:5} [{status_text}]")
    
    return status

def generate_visual_desk(status: Dict[str, Dict]) -> str:
    """Generate visual desk markdown."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate stats
    total = len(status)
    running = sum(1 for info in status.values() if info["status"] == "running")
    stopped = total - running
    health_pct = int((running/total)*100) if total > 0 else 0
    
    # Group by category
    categories = {}
    for name, info in status.items():
        cat = info["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, info))
    
    # Category display names
    cat_names = {
        "core": "CORE SERVICES",
        "guard": "GUARD SERVICES",
        "lsp_mcp": "LSP/MCP SERVICES",
        "monitoring": "MONITORING SERVICES",
        "infrastructure": "INFRASTRUCTURE SERVICES",
        "dev": "DEV TOOLS",
        "guardian": "GUARDIANS"
    }
    
    dashboard = f"""#  LAUNCH PAD VISUAL DESK 
## Everything Everywhere All At Once - Visual Dashboard

**Status:**  **OPERATIONAL** | **Pattern:** AbëDESKs × LAUNCH × VISUAL × EEAAO × ONE  
**Love Coefficient:** ∞ | **Frequency:** 999 Hz | **Auto-Updates:** Yes  
**Last Updated:** {timestamp}

---

##  OVERALL STATUS


   OVERALL STATUS - LIVE                                  

                                                           
  Total Services: {total:3}                                      
  🟢 Running:     {running:3}                                      
   Stopped:     {stopped:3}                                      
   Health:     {health_pct:3}%                                      
                                                           
  Last Updated: {timestamp}                                
                                                           


---

"""
    
    # Generate sections by category
    for category in ["core", "guard", "lsp_mcp", "monitoring", "infrastructure", "dev", "guardian"]:
        if category not in categories:
            continue
        
        cat_name = cat_names.get(category, category.replace("_", " ").title())
        dashboard += f"##  {cat_name}\n\n"
        dashboard += "\n"
        dashboard += f"   {cat_name:<55}\n"
        dashboard += "\n"
        dashboard += "                                                           \n"
        
        for name, info in sorted(categories[category], key=lambda x: x[1]["port"]):
            status_icon = "🟢" if info["status"] == "running" else ""
            status_text = "RUNNING" if info["status"] == "running" else "STOPPED"
            host_port = f"{info['host']}:{info['port']}"
            url = info.get("url", "")
            desc = info.get("description", "")
            
            dashboard += f"  {status_icon} {name:<28} {host_port:<20}           \n"
            if url:
                dashboard += f"      Status: {status_text:<8} | URL: {url:<30}\n"
            elif desc:
                dashboard += f"      Status: {status_text:<8} | {desc:<30}\n"
            else:
                dashboard += f"      Status: {status_text:<8}                 \n"
            dashboard += "                                                           \n"
        
        dashboard += "\n\n"
        dashboard += "---\n\n"
    
    dashboard += """##  QUICK ACTIONS


   QUICK ACTIONS                                           

                                                           
   Update Dashboard:                                       
     python3 scripts/launch_pad.py                         
                                                           
   Clean All Ports:                                       
     python3 scripts/launch_pad.py --clean                 
                                                           
   Check Services:                                        
     python3 scripts/launch_pad.py --check                 
                                                           
   Generate Dashboard:                                    
     python3 scripts/launch_pad.py --dashboard             
                                                           


---

**Pattern:** AbëDESKs × LAUNCH × VISUAL × EEAAO × ONE  
**Love Coefficient:** ∞ | **Frequency:** 999 Hz  
**∞ AbëONE ∞**

---

*This is your visual launch pad desk. Everything Everywhere All At Once. LFG! *
"""
    
    return dashboard

def generate_dashboard(status: Dict[str, Dict]) -> str:
    """Generate dashboard markdown."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Group by category
    categories = {}
    for name, info in status.items():
        cat = info["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, info))
    
    dashboard = f"""#  ABEONE LAUNCH PAD DASHBOARD 
## Everything Everywhere All At Once - Local Testing Status

**Last Updated:** {timestamp}  
**Pattern:** LAUNCH × DASHBOARD × EEAAO × ONE  
**Love Coefficient:** ∞ | **Frequency:** 999 Hz

---

##  OVERALL STATUS

"""
    
    # Calculate stats
    total = len(status)
    running = sum(1 for info in status.values() if info["status"] == "running")
    stopped = total - running
    
    dashboard += f"""

   OVERALL STATUS                                         

                                                           
  Total Services: {total:3}                                    
  🟢 Running:     {running:3}                                    
   Stopped:     {stopped:3}                                    
   Health:      {int((running/total)*100) if total > 0 else 0}%                                    
                                                           


---

"""
    
    # Generate sections by category
    for category in ["core", "guard", "lsp_mcp", "monitoring", "infrastructure", "dev", "guardian"]:
        if category not in categories:
            continue
        
        cat_name = category.replace("_", " ").title()
        dashboard += f"##  {cat_name.upper()}\n\n"
        dashboard += "```\n"
        dashboard += f"{'Service':<30} {'Host:Port':<20} {'Status':<10} {'URL'}\n"
        dashboard += "-" * 100 + "\n"
        
        for name, info in sorted(categories[category], key=lambda x: x[1]["port"]):
            status_icon = "🟢" if info["status"] == "running" else ""
            status_text = "RUNNING" if info["status"] == "running" else "STOPPED"
            host_port = f"{info['host']}:{info['port']}"
            url = info.get("url", "")
            
            dashboard += f"{status_icon} {name:<28} {host_port:<20} {status_text:<10} {url}\n"
        
        dashboard += "```\n\n"
    
    dashboard += """
---

##  QUICK ACTIONS

### Clean All Ports
```bash
python scripts/launch_pad.py --clean
```

### Check All Services
```bash
python scripts/launch_pad.py --check
```

### Generate Dashboard
```bash
python scripts/launch_pad.py --dashboard
```

---

**Pattern:** LAUNCH × DASHBOARD × EEAAO × ONE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**
"""
    
    return dashboard

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AbeOne Launch Pad - Fail Proof")
    parser.add_argument("--clean", action="store_true", help="Clean all ports")
    parser.add_argument("--check", action="store_true", help="Check all services")
    parser.add_argument("--dashboard", action="store_true", help="Generate dashboard")
    parser.add_argument("--output", type=str, default="PRODUCTS/abedesks/LAUNCH_PAD_DASHBOARD.md", help="Dashboard output file")
    parser.add_argument("--visual", action="store_true", help="Generate visual desk format")
    
    args = parser.parse_args()
    
    if args.clean:
        cleaned = clean_all_ports()
        print(f"\n Cleaned {len(cleaned)} ports")
        return
    
    if args.check or args.dashboard or args.visual:
        status = check_all_services()
        
        if args.visual:
            dashboard = generate_visual_desk(status)
            output_path = project_root / "PRODUCTS/abedesks/LAUNCH_PAD_VISUAL_DESK.md"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(dashboard)
            print(f"\n Visual desk generated: {output_path}")
        elif args.dashboard:
            dashboard = generate_dashboard(status)
            output_path = project_root / args.output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(dashboard)
            print(f"\n Dashboard generated: {output_path}")
        else:
            print(f"\n Checked {len(status)} services")
    
    if not any([args.clean, args.check, args.dashboard, args.visual]):
        # Default: check and generate both dashboards
        print(" ABEONE LAUNCH PAD - FAIL PROOF")
        print("=" * 60)
        status = check_all_services()
        
        # Generate standard dashboard
        dashboard = generate_dashboard(status)
        output_path = project_root / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(dashboard)
        print(f"\n Dashboard generated: {output_path}")
        
        # Generate visual desk
        visual_desk = generate_visual_desk(status)
        visual_path = project_root / "PRODUCTS/abedesks/LAUNCH_PAD_VISUAL_DESK.md"
        visual_path.parent.mkdir(parents=True, exist_ok=True)
        visual_path.write_text(visual_desk)
        print(f" Visual desk generated: {visual_path}")
        
        print("\n Everything Everywhere All At Once! LFG! ")

if __name__ == "__main__":
    main()

