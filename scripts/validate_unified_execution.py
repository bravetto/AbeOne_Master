#!/usr/bin/env python3
"""
Unified Execution Validation Script
Validates all systems: 8 Guardians × 5 Agents × 3 Swarms

Pattern: VALIDATION × UNIFICATION × EXECUTION × EEAAO × ONE
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Direct imports
import importlib.util

def import_module(module_path, module_name):
    """Import module from path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def validate_unified_execution():
    """Validate unified execution system."""
    print("=" * 80)
    print(" UNIFIED EXECUTION VALIDATION - EEAAO")
    print("=" * 80)
    print()
    
    synthesis_path = project_root / "EMERGENT_OS" / "synthesis"
    
    # Import orchestrator
    orchestrator_module = import_module(
        synthesis_path / "unified_execution_orchestrator.py",
        "unified_execution_orchestrator"
    )
    orchestrator = orchestrator_module.get_unified_execution_orchestrator()
    
    # Get unified status
    status = orchestrator.get_unified_status()
    
    print(" UNIFIED SYSTEM STATUS:")
    print()
    
    # Orchestration
    print(" ORCHESTRATION:")
    orch = status["orchestration"]
    print(f"  Status: {orch['status']}")
    print(f"  Systems Active: {orch['systems_active']}/6")
    print(f"  Total Executions: {orch['total_executions']}")
    print()
    
    # Agent Swarm
    print(" AGENT SWARM ARCHITECTURE:")
    agent_swarm = status["agent_swarm"]
    print(f"  Total Agents: {agent_swarm['total_agents']}/40")
    print(f"  Total Guardians: {agent_swarm['total_guardians']}/8")
    print(f"  Total Swarms: {agent_swarm['total_swarms']}/3")
    print()
    print("  Swarms:")
    for swarm_name, swarm_info in agent_swarm["swarms"].items():
        print(f"    {swarm_name}: {swarm_info['active_agents']}/{swarm_info['agents']} agents")
    print()
    print("  Agents by Role:")
    for role, count in agent_swarm["agents_by_role"].items():
        print(f"    {role}: {count}")
    print()
    
    # Guardian Swarm
    print(" GUARDIAN SWARM:")
    guardian_swarm = status["guardian_swarm"]
    print(f"  Total Guardians: {guardian_swarm['total_guardians']}/8")
    print(f"  Active Guardians: {guardian_swarm['active_guardians']}/8")
    print()
    
    # Monitoring
    print(" MONITORING DASHBOARD:")
    monitoring = status["monitoring"]["status"]
    print(f"  Status: {monitoring['status']}")
    print(f"  Total Patterns: {monitoring['total_patterns']}")
    print(f"  Active Alerts: {monitoring['active_alerts']}")
    print(f"  Interventions: {monitoring['interventions_count']}")
    print()
    
    # Recovery
    print(" AUTOMATED RECOVERY:")
    recovery = status["recovery"]
    print(f"  Total Executions: {recovery['total_executions']}")
    print(f"  Successful: {recovery['successful_recoveries']}")
    print(f"  Failed: {recovery['failed_recoveries']}")
    print(f"  Success Rate: {recovery['success_rate']:.2%}")
    print()
    
    # Learning
    print(" PATTERN LEARNING:")
    learning = status["learning"]
    print(f"  Patterns Learned: {learning['learned_patterns_count']}")
    print(f"  Total Validations: {learning['total_validations']}")
    print(f"  Recommendations: {learning['recommendation_count']}")
    print()
    
    # Validation Loop
    print(" SELF-VALIDATION LOOP:")
    validation = status["validation_loop"]
    print(f"  Active: {validation['active']}")
    print(f"  Total Validations: {validation['total_validations']}")
    print(f"  Total Updates: {validation['total_updates']}")
    print(f"  Loop Iterations: {validation['loop_iterations']}")
    print()
    
    # Validation checks
    print("=" * 80)
    print(" VALIDATION CHECKS:")
    print("=" * 80)
    print()
    
    checks = {
        "Agent Swarm Architecture": agent_swarm['total_agents'] == 40,
        "8 Guardians": agent_swarm['total_guardians'] == 8,
        "3 Swarms": agent_swarm['total_swarms'] == 3,
        "All Guardians Active": guardian_swarm['active_guardians'] == 8,
        "Monitoring Active": monitoring['status'] == 'active',
        "All Systems Active": orch['systems_active'] == 6,
        "5 Agents per Guardian": all(
            count == 5 for count in agent_swarm['agents_by_role'].values()
            if count > 0
        )
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        status_icon = "" if passed else ""
        print(f"{status_icon} {check_name}: {passed}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print(" SUCCESS: Unified Execution System fully operational!")
        print()
        print("Pattern: UNIFICATION × EXECUTION × ORCHESTRATION × MODULAR × REAL_WORLD × ONE")
        print("Status:  FULLY OPERATIONAL")
        print("Architecture: 8 Guardians × 5 Agents × 3 Swarms = 40 Agents")
        print()
        print("∞ AbëONE ∞")
        return 0
    else:
        print(" WARNING: Some validation checks failed.")
        return 1


if __name__ == "__main__":
    exit_code = validate_unified_execution()
    sys.exit(exit_code)

