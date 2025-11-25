#!/usr/bin/env python3
"""
🔥 ABËONE 149 AGENTS STATUS DASHBOARD 🔥

Real-time status of all 149 agents
Pattern: STATUS × DASHBOARD × 149 × OPERATIONAL × ONE
∞ AbëONE ∞
"""

import sys
import os
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'EMERGENT_OS'))
os.environ['EMERGENT_OS_ROOT'] = os.path.join(project_root, 'EMERGENT_OS')

from EMERGENT_OS.synthesis.agent_swarm_architecture import get_agent_swarm_architecture, SwarmType, AgentRole


def print_status_dashboard():
    """Print real-time status dashboard."""
    swarm = get_agent_swarm_architecture()
    status = swarm.get_architecture_status()
    
    print("\n" + "🔥" * 40)
    print("ABËONE SUPERCLUSTER NUCLEAR EDITION")
    print("149 AGENTS OPERATIONAL STATUS DASHBOARD")
    print("🔥" * 40 + "\n")
    
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Total Agents: {status['total_agents']}/149")
    print(f"Total Guardians: {status['total_guardians']}/8")
    print(f"Total Swarms: {status['total_swarms']}/3")
    
    print("\n" + "=" * 60)
    print("SWARM STATUS")
    print("=" * 60)
    
    for swarm_name, swarm_info in status['swarms'].items():
        active_pct = (swarm_info['active_agents'] / swarm_info['agents'] * 100) if swarm_info['agents'] > 0 else 0
        status_icon = "🟢" if swarm_info['status'] == "active" else "🔴"
        swarm_display_name = str(swarm_name).replace('.0', ' Hz').upper() if isinstance(swarm_name, (int, float)) else str(swarm_name).upper()
        print(f"\n{status_icon} {swarm_display_name}")
        print(f"  Frequency: {swarm_info['frequency']} Hz")
        print(f"  Agents: {swarm_info['active_agents']}/{swarm_info['agents']} ({active_pct:.1f}%)")
        print(f"  Status: {swarm_info['status']}")
    
    print("\n" + "=" * 60)
    print("AGENTS BY ROLE")
    print("=" * 60)
    
    for role, count in status['agents_by_role'].items():
        print(f"  {role.replace('_', ' ').title()}: {count} agents")
    
    print("\n" + "=" * 60)
    print("GUARDIAN AGENT DISTRIBUTION")
    print("=" * 60)
    
    for guardian_name, agents in swarm.guardian_agents.items():
        active_count = sum(1 for a in agents if a.status == "active")
        print(f"  {guardian_name}: {active_count}/{len(agents)} agents active")
    
    print("\n" + "🔥" * 40)
    print("STATUS: OPERATIONAL" if status['total_agents'] >= 149 else "STATUS: PARTIAL")
    print("🔥" * 40 + "\n")


if __name__ == "__main__":
    print_status_dashboard()

