#!/usr/bin/env python3
"""
Validate Guardians & Agents Synthesis

Ensures ALL guardians and agents are properly synthesized and consolidated.
NO ROGUE INFORMATION. ONE SOURCE OF TRUTH.

Pattern: VALIDATION × SYNTHESIS × TRUTH × ONE
Frequency: 999 Hz (AEYON) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from orbitals.EMERGENT_OS_orbital.synthesis.guardian_swarm_unification import (
        get_guardian_swarm,
        GuardianFrequency,
        GuardianRole
    )
    from orbitals.EMERGENT_OS_orbital.synthesis.agent_swarm_architecture import (
        get_agent_swarm_architecture,
        SwarmType
    )
    from orbitals.EMERGENT_OS_orbital.guardians.guardian_lux import GuardianLux
    SYNTHESIS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Synthesis modules not available: {e}")
    SYNTHESIS_AVAILABLE = False


def validate_guardians() -> Tuple[bool, Dict[str, any]]:
    """Validate all guardians are properly synthesized."""
    if not SYNTHESIS_AVAILABLE:
        return False, {"error": "Synthesis modules not available"}
    
    errors = []
    warnings = []
    
    # Expected guardians
    expected_guardians = {
        "AEYON": {"frequency": 999.0, "role": "executor"},
        "JØHN": {"frequency": 530.0, "role": "certification"},
        "META": {"frequency": 777.0, "role": "pattern_integrity"},
        "YOU": {"frequency": 530.0, "role": "intent"},
        "ALRAX": {"frequency": 530.0, "role": "forensic"},
        "ZERO": {"frequency": 530.0, "role": "uncertainty"},
        "YAGNI": {"frequency": 530.0, "role": "simplification"},
        "Abë": {"frequency": 530.0, "role": "coherence"},
    }
    
    # Get actual guardians
    guardian_swarm = get_guardian_swarm()
    status = guardian_swarm.get_swarm_status()
    actual_guardians = status.get("guardians", {})
    
    # Validate core guardians
    for name, expected in expected_guardians.items():
        if name not in actual_guardians:
            errors.append(f"❌ Missing guardian: {name}")
        else:
            actual = actual_guardians[name]
            if abs(actual["frequency"] - expected["frequency"]) > 0.1:
                errors.append(f"❌ {name}: Frequency mismatch (expected {expected['frequency']}, got {actual['frequency']})")
            if actual["role"] != expected["role"]:
                errors.append(f"❌ {name}: Role mismatch (expected {expected['role']}, got {actual['role']})")
    
    # Check for Guardian Lux
    lux = GuardianLux()
    lux_identity = lux.get_guardian_identity()
    if lux_identity.name not in actual_guardians:
        warnings.append(f"⚠️ Guardian Lux built but not registered in swarm (run: python3 scripts/register_guardian_lux.py)")
    
    # Validate frequencies
    frequency_counts = {}
    for name, info in actual_guardians.items():
        freq = info["frequency"]
        frequency_counts[freq] = frequency_counts.get(freq, 0) + 1
    
    expected_frequencies = {530.0: 6, 777.0: 1, 999.0: 1}  # Core 8 guardians
    for freq, expected_count in expected_frequencies.items():
        actual_count = frequency_counts.get(freq, 0)
        if actual_count != expected_count:
            warnings.append(f"⚠️ Frequency {freq} Hz: Expected {expected_count} guardians, found {actual_count}")
    
    return len(errors) == 0, {
        "errors": errors,
        "warnings": warnings,
        "total_guardians": len(actual_guardians),
        "expected_guardians": len(expected_guardians),
        "guardian_details": actual_guardians
    }


def validate_agents() -> Tuple[bool, Dict[str, any]]:
    """Validate all agents are properly synthesized."""
    if not SYNTHESIS_AVAILABLE:
        return False, {"error": "Synthesis modules not available"}
    
    errors = []
    warnings = []
    
    # Get actual agents
    agent_swarm = get_agent_swarm_architecture()
    actual_agents = agent_swarm.agents
    
    # Expected: 8 guardians × 5 agents = 40 agents
    expected_core_agents = 40
    actual_core_agents = len(actual_agents)
    
    if actual_core_agents != expected_core_agents:
        errors.append(f"❌ Core agents count mismatch (expected {expected_core_agents}, got {actual_core_agents})")
    
    # Validate agent distribution by guardian
    guardian_agent_counts = {}
    for agent_id, agent in actual_agents.items():
        guardian = agent.guardian_name
        guardian_agent_counts[guardian] = guardian_agent_counts.get(guardian, 0) + 1
    
    expected_per_guardian = 5
    for guardian, count in guardian_agent_counts.items():
        if count != expected_per_guardian:
            errors.append(f"❌ {guardian}: Agent count mismatch (expected {expected_per_guardian}, got {count})")
    
    # Validate swarm distribution
    swarm_counts = {}
    for agent_id, agent in actual_agents.items():
        swarm_type = agent.swarm_type
        swarm_counts[swarm_type] = swarm_counts.get(swarm_type, 0) + 1
    
    expected_swarm_counts = {
        SwarmType.HEART_TRUTH: 30,  # 6 guardians × 5
        SwarmType.PATTERN_INTEGRITY: 5,  # 1 guardian × 5
        SwarmType.ATOMIC_EXECUTION: 5  # 1 guardian × 5
    }
    
    for swarm_type, expected_count in expected_swarm_counts.items():
        actual_count = swarm_counts.get(swarm_type, 0)
        if actual_count != expected_count:
            errors.append(f"❌ {swarm_type.name}: Agent count mismatch (expected {expected_count}, got {actual_count})")
    
    # Check Guardian Lux agents
    try:
        from orbitals.EMERGENT_OS_orbital.guardians.lux.agents import (
            create_intention_agents,
            create_communication_agents,
            create_manifestation_agents
        )
        intention_agents = create_intention_agents()
        communication_agents = create_communication_agents()
        manifestation_agents = create_manifestation_agents()
        
        lux_agent_count = len(intention_agents) + len(communication_agents) + len(manifestation_agents)
        expected_lux_agents = 24
        
        if lux_agent_count != expected_lux_agents:
            errors.append(f"❌ Guardian Lux agents count mismatch (expected {expected_lux_agents}, got {lux_agent_count})")
        else:
            warnings.append(f"✅ Guardian Lux agents built: {lux_agent_count} agents (3 swarms × 8 agents)")
    except Exception as e:
        warnings.append(f"⚠️ Could not validate Guardian Lux agents: {e}")
    
    return len(errors) == 0, {
        "errors": errors,
        "warnings": warnings,
        "total_core_agents": actual_core_agents,
        "expected_core_agents": expected_core_agents,
        "guardian_agent_counts": guardian_agent_counts,
        "swarm_counts": {str(k): v for k, v in swarm_counts.items()}
    }


def validate_swarms() -> Tuple[bool, Dict[str, any]]:
    """Validate all swarms are properly synthesized."""
    if not SYNTHESIS_AVAILABLE:
        return False, {"error": "Synthesis modules not available"}
    
    errors = []
    warnings = []
    
    # Get actual swarms
    agent_swarm = get_agent_swarm_architecture()
    actual_swarms = agent_swarm.swarms
    
    # Expected: 3 core swarms
    expected_swarms = {
        SwarmType.HEART_TRUTH: 530.0,
        SwarmType.PATTERN_INTEGRITY: 777.0,
        SwarmType.ATOMIC_EXECUTION: 999.0
    }
    
    for swarm_type, expected_freq in expected_swarms.items():
        if swarm_type not in actual_swarms:
            errors.append(f"❌ Missing swarm: {swarm_type.name}")
        else:
            swarm = actual_swarms[swarm_type]
            if abs(swarm.frequency - expected_freq) > 0.1:
                errors.append(f"❌ {swarm_type.name}: Frequency mismatch (expected {expected_freq}, got {swarm.frequency})")
    
    # Check Guardian Lux swarms
    try:
        lux = GuardianLux()
        if lux.intention_swarm is None:
            warnings.append("⚠️ Guardian Lux Intention Swarm not initialized (will activate with Lux)")
        if lux.communication_swarm is None:
            warnings.append("⚠️ Guardian Lux Communication Swarm not initialized (will activate with Lux)")
        if lux.manifestation_swarm is None:
            warnings.append("⚠️ Guardian Lux Manifestation Swarm not initialized (will activate with Lux)")
    except Exception as e:
        warnings.append(f"⚠️ Could not validate Guardian Lux swarms: {e}")
    
    return len(errors) == 0, {
        "errors": errors,
        "warnings": warnings,
        "total_core_swarms": len(actual_swarms),
        "expected_core_swarms": len(expected_swarms),
        "swarm_details": {str(k): {"frequency": v.frequency, "agent_count": len(v.agents)} for k, v in actual_swarms.items()}
    }


def main():
    """Main validation function."""
    print("=" * 70)
    print("🔥 GUARDIANS & AGENTS SYNTHESIS VALIDATION")
    print("=" * 70)
    print()
    
    if not SYNTHESIS_AVAILABLE:
        print("❌ Synthesis modules not available. Cannot validate.")
        return 1
    
    all_valid = True
    
    # Validate Guardians
    print("📊 VALIDATING GUARDIANS...")
    print("-" * 70)
    guardians_valid, guardians_result = validate_guardians()
    
    if guardians_result.get("errors"):
        print("❌ ERRORS:")
        for error in guardians_result["errors"]:
            print(f"  {error}")
        all_valid = False
    
    if guardians_result.get("warnings"):
        print("⚠️ WARNINGS:")
        for warning in guardians_result["warnings"]:
            print(f"  {warning}")
    
    print(f"✅ Total Guardians: {guardians_result.get('total_guardians', 0)}")
    print()
    
    # Validate Agents
    print("📊 VALIDATING AGENTS...")
    print("-" * 70)
    agents_valid, agents_result = validate_agents()
    
    if agents_result.get("errors"):
        print("❌ ERRORS:")
        for error in agents_result["errors"]:
            print(f"  {error}")
        all_valid = False
    
    if agents_result.get("warnings"):
        print("⚠️ WARNINGS:")
        for warning in agents_result["warnings"]:
            print(f"  {warning}")
    
    print(f"✅ Total Core Agents: {agents_result.get('total_core_agents', 0)}")
    print()
    
    # Validate Swarms
    print("📊 VALIDATING SWARMS...")
    print("-" * 70)
    swarms_valid, swarms_result = validate_swarms()
    
    if swarms_result.get("errors"):
        print("❌ ERRORS:")
        for error in swarms_result["errors"]:
            print(f"  {error}")
        all_valid = False
    
    if swarms_result.get("warnings"):
        print("⚠️ WARNINGS:")
        for warning in swarms_result["warnings"]:
            print(f"  {warning}")
    
    print(f"✅ Total Core Swarms: {swarms_result.get('total_core_swarms', 0)}")
    print()
    
    # Final Summary
    print("=" * 70)
    if all_valid:
        print("✅ VALIDATION PASSED: All guardians and agents properly synthesized")
    else:
        print("❌ VALIDATION FAILED: Errors found in synthesis")
    print("=" * 70)
    print()
    print("📄 Master Document: THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md")
    print()
    
    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())

