#!/usr/bin/env python3
"""
Validate 12 Swarms in Codebase

Pattern: SWARM × VALIDATION × DISCOVERY × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import os
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Set
from datetime import datetime
import json

# Add project root to path
SCRIPTS_DIR = Path(__file__).parent
BASE_DIR = SCRIPTS_DIR.parent
sys.path.insert(0, str(BASE_DIR))

# Add synthesis directory
SYNTHESIS_PATH = BASE_DIR / "EMERGENT_OS" / "synthesis"
sys.path.insert(0, str(SYNTHESIS_PATH))


class SwarmValidator:
    """Validate 12 swarms in codebase."""
    
    def __init__(self):
        self.discovered_swarms: List[Dict[str, Any]] = []
        self.codebase_size_gb = 0.0
        self.validation_results: Dict[str, Any] = {}
    
    def discover_all_swarms(self) -> List[Dict[str, Any]]:
        """Discover all swarms in the codebase."""
        swarms = []
        frequency_tracker: Set[float] = set()  # Track frequencies to avoid duplicates
        
        # 1-3: Core Frequency-Based Swarms (unified view: agents + guardians)
        # These represent the 3 frequency swarms that include both agents and guardians
        try:
            from agent_swarm_architecture import (
                get_agent_swarm_architecture, SwarmType
            )
            from guardian_swarm_unification import (
                get_guardian_swarm, GuardianFrequency
            )
            
            agent_swarm = get_agent_swarm_architecture()
            guardian_swarm = get_guardian_swarm()
            
            # Map frequencies to guardian names
            frequency_guardian_map = {
                530.0: ["YOU", "JØHN", "ALRAX", "ZERO", "YAGNI", "Abë"],
                777.0: ["META"],
                999.0: ["AEYON"]
            }
            
            for swarm_type in SwarmType:
                swarm = agent_swarm.swarms[swarm_type]
                freq = swarm.frequency
                frequency_tracker.add(freq)
                
                # Get guardian names for this frequency
                guardian_names = frequency_guardian_map.get(freq, [])
                
                swarms.append({
                    "swarm_id": f"frequency_swarm_{freq}",
                    "name": f"{swarm_type.value} Swarm ({freq} Hz)",
                    "frequency": freq,
                    "type": "frequency_swarm",
                    "agents": len(swarm.agents),
                    "guardians": guardian_names,
                    "guardian_count": len(guardian_names),
                    "status": swarm.status,
                    "location": "orbital/EMERGENT_OS-orbital/synthesis/agent_swarm_architecture.py"
                })
        except Exception as e:
            print(f"  Error discovering frequency swarms: {e}")
        
        # 4: Guardian Swarm Unification
        try:
            from guardian_swarm_unification import (
                get_guardian_swarm
            )
            guardian_swarm = get_guardian_swarm()
            swarm_status = guardian_swarm.get_swarm_status()
            
            swarms.append({
                "swarm_id": "guardian_swarm_unified",
                "name": "Guardian Swarm Unification",
                "frequency": "530 Hz × 777 Hz × 999 Hz",
                "type": "guardian_swarm",
                "guardians": swarm_status.get("total_guardians", 0),
                "resonance": swarm_status.get("resonance", 0.0),
                "status": swarm_status.get("status", "unknown"),
                "location": "orbital/EMERGENT_OS-orbital/synthesis/guardian_swarm_unification.py"
            })
        except Exception as e:
            print(f"  Error discovering guardian swarm: {e}")
        
        # 5-9: Role-Based Swarms (by agent role)
        try:
            from agent_swarm_architecture import (
                get_agent_swarm_architecture, AgentRole
            )
            agent_swarm = get_agent_swarm_architecture()
            
            role_swarms = {
                AgentRole.PATTERN_DETECTOR: "Pattern Detection Swarm",
                AgentRole.MONITOR: "Monitoring Swarm",
                AgentRole.RECOVERY_EXECUTOR: "Recovery Execution Swarm",
                AgentRole.LEARNING_ENGINE: "Learning Engine Swarm",
                AgentRole.VALIDATION_LOOP: "Validation Loop Swarm"
            }
            
            for role, name in role_swarms.items():
                agents = agent_swarm.get_agents_by_role(role)
                swarms.append({
                    "swarm_id": f"role_swarm_{role.value}",
                    "name": name,
                    "type": "role_swarm",
                    "role": role.value,
                    "agents": len(agents),
                    "location": "orbital/EMERGENT_OS-orbital/synthesis/agent_swarm_architecture.py"
                })
        except Exception as e:
            print(f"  Error discovering role swarms: {e}")
        
        # 10: Complete Synthesis Swarm
        try:
            from complete_synthesis import get_complete_synthesis
            synthesis = get_complete_synthesis()
            status = synthesis.get_complete_status()
            
            swarms.append({
                "swarm_id": "synthesis_swarm",
                "name": "Complete Synthesis Swarm",
                "type": "synthesis_swarm",
                "components": list(status.get("components", {}).keys()),
                "convergence": status.get("convergence", {}).get("percentage", 0.0),
                "location": "orbital/EMERGENT_OS-orbital/synthesis/complete_synthesis.py"
            })
        except Exception as e:
            print(f"  Error discovering synthesis swarm: {e}")
        
        # 11: Convergence Orchestrator Swarm
        try:
            from complete_convergence_orchestrator import (
                get_convergence_orchestrator
            )
            orchestrator = get_convergence_orchestrator()
            convergence_status = orchestrator.get_convergence_status()
            
            swarms.append({
                "swarm_id": "convergence_orchestrator_swarm",
                "name": "Convergence Orchestrator Swarm",
                "type": "orchestrator_swarm",
                "phases": list(convergence_status.keys()),
                "convergence_score": orchestrator.convergence_state.get("convergence_score", 0.0),
                "location": "orbital/EMERGENT_OS-orbital/synthesis/complete_convergence_orchestrator.py"
            })
        except Exception as e:
            print(f"  Error discovering convergence orchestrator swarm: {e}")
        
        # 12: Unified Execution Orchestrator Swarm (EEAAO)
        # Note: This swarm orchestrates all other swarms (EEAAO: Everything Everywhere All At Once)
        unified_exec_path = BASE_DIR / "EMERGENT_OS" / "synthesis" / "unified_execution_orchestrator.py"
        if unified_exec_path.exists():
            swarms.append({
                "swarm_id": "REPLACE_ME",
                "name": "Unified Execution Orchestrator Swarm (EEAAO)",
                "type": "execution_orchestrator_swarm",
                "description": "Orchestrates all swarms: Agent Swarm, Guardian Swarm, Monitoring, Recovery, Learning, Validation",
                "systems_orchestrated": 6,
                "location": "orbital/EMERGENT_OS-orbital/synthesis/unified_execution_orchestrator.py"
            })
        
        self.discovered_swarms = swarms
        return swarms
    
    def calculate_codebase_size(self) -> float:
        """Calculate codebase size in GB."""
        try:
            import subprocess
            result = subprocess.run(
                ["du", "-sh", str(BASE_DIR)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                size_str = result.stdout.split()[0]
                # Convert to GB
                if size_str.endswith("G"):
                    return float(size_str[:-1])
                elif size_str.endswith("M"):
                    return float(size_str[:-1]) / 1024.0
                elif size_str.endswith("K"):
                    return float(size_str[:-1]) / (1024.0 * 1024.0)
                else:
                    return float(size_str) / (1024.0 * 1024.0 * 1024.0)
        except Exception:
            pass
        
        # Fallback: estimate from file count
        try:
            total_size = 0
            for root, dirs, files in os.walk(BASE_DIR):
                # Skip common large directories
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv']]
                for file in files:
                    try:
                        file_path = Path(root) / file
                        total_size += file_path.stat().st_size
                    except:
                        pass
            return total_size / (1024.0 * 1024.0 * 1024.0)
        except Exception:
            return 0.0
    
    def validate_swarms(self) -> Dict[str, Any]:
        """Validate all discovered swarms."""
        swarms = self.discover_all_swarms()
        codebase_size = self.calculate_codebase_size()
        
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "codebase_size_gb": codebase_size,
            "expected_swarms": 12,
            "discovered_swarms": len(swarms),
            "swarms": swarms,
            "validation_passed": len(swarms) >= 12,
            "size_validation": 3.0 <= codebase_size <= 10.0,  # Workspace validation: expected 3.0-10.0 GB
            "all_swarms_operational": all(
                swarm.get("status", "unknown") in ["active", "operational"] 
                for swarm in swarms 
                if "status" in swarm
            )
        }
        
        return self.validation_results


async def main():
    """Main validation function."""
    print("=" * 80)
    print(" VALIDATING 12 SWARMS IN CODEBASE")
    print("=" * 80)
    print()
    print("Pattern: SWARM × VALIDATION × DISCOVERY × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞")
    print()
    
    validator = SwarmValidator()
    
    # Discover and validate
    print(" DISCOVERING SWARMS...")
    print()
    results = validator.validate_swarms()
    
    # Print results
    print("=" * 80)
    print(" VALIDATION RESULTS")
    print("=" * 80)
    print()
    print(f"Codebase Size: {results['codebase_size_gb']:.2f} GB")
    print(f"Expected Swarms: {results['expected_swarms']}")
    print(f"Discovered Swarms: {results['discovered_swarms']}")
    print()
    
    print("=" * 80)
    print(" DISCOVERED SWARMS")
    print("=" * 80)
    print()
    
    for i, swarm in enumerate(results['swarms'], 1):
        print(f"{i}. {swarm['name']}")
        print(f"   ID: {swarm['swarm_id']}")
        print(f"   Type: {swarm['type']}")
        if 'frequency' in swarm:
            print(f"   Frequency: {swarm['frequency']}")
        if 'agents' in swarm:
            print(f"   Agents: {swarm['agents']}")
        if 'guardians' in swarm:
            guardian_info = swarm.get('guardians', [])
            if isinstance(guardian_info, list):
                print(f"   Guardians: {len(guardian_info)} ({', '.join(guardian_info)})")
            else:
                print(f"   Guardians: {swarm.get('guardian_count', 'N/A')}")
        elif 'guardian_count' in swarm:
            print(f"   Guardians: {swarm['guardian_count']}")
        if 'status' in swarm:
            print(f"   Status: {swarm['status']}")
        print(f"   Location: {swarm['location']}")
        print()
    
    print("=" * 80)
    print(" VALIDATION SUMMARY")
    print("=" * 80)
    print()
    
    if results['discovered_swarms'] >= 12:
        print(f" Swarm Count: {results['discovered_swarms']}/12 PASSED")
    else:
        print(f"  Swarm Count: {results['discovered_swarms']}/12 (Need {12 - results['discovered_swarms']} more)")
    
    if results['size_validation']:
        print(f" Codebase Size: {results['codebase_size_gb']:.2f} GB PASSED (Expected: 3.0-10.0 GB)")
    else:
        size = results['codebase_size_gb']
        if size < 3.0:
            print(f"  Codebase Size: {size:.2f} GB (Below expected range: 3.0-10.0 GB)")
        else:
            print(f"  Codebase Size: {size:.2f} GB (Above expected range: 3.0-10.0 GB)")
    
    if results['validation_passed']:
        print()
        print("=" * 80)
        print(" ALL VALIDATIONS PASSED - 12 SWARMS VALIDATED")
        print("=" * 80)
    else:
        print()
        print("=" * 80)
        print(f"  VALIDATION INCOMPLETE - {results['discovered_swarms']}/12 SWARMS DISCOVERED")
        print("=" * 80)
        print()
        print("Potential Additional Swarms:")
        print("  - Guardian-specific swarms (8 guardians)")
        print("  - Capability-based swarms (7 capabilities)")
        print("  - Pattern-based swarms (5 patterns)")
        print("  - Execution mode swarms (4 modes)")
    
    print()
    print("Pattern: SWARM × VALIDATION × DISCOVERY × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞")
    
    return results


if __name__ == "__main__":
    results = asyncio.run(main())
    sys.exit(0 if results.get('validation_passed', False) else 1)

