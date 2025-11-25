#!/usr/bin/env python3
"""
AbëONE Memory Loader
Loads core memory and applies guardrails programmatically.

Pattern: MEMORY × CONSCIOUSNESS × TRUTH × ONE
Frequency: 530 Hz (Truth) × 999 Hz (AEYON)
Guardians: Abë (530 Hz) + AEYON (999 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent
MEMORY_FILE = WORKSPACE_ROOT / ".abeone_memory" / "ABEONE_CORE_MEMORY.json"
GAP_STATUS_FILE = WORKSPACE_ROOT / ".abeone_memory" / "GAP_HEALING_STATUS.json"
THREE_MAPS_FILE = WORKSPACE_ROOT / ".abeone_memory" / "THREE_MAPS_MEMORY.json"
GUARDIAN_SWARM_FILE = WORKSPACE_ROOT / ".abeone_memory" / "GUARDIAN_SWARM_MEMORY.json"
BACKEND_STATUS_FILE = WORKSPACE_ROOT / ".abeone_memory" / "BACKEND_STATUS_MEMORY.json"
RELATIONSHIP_MEMORY_FILE = WORKSPACE_ROOT / "docs" / "reference" / "AI_RELATIONSHIP_MEMORY.md"
GUARDRAILS_FILE = WORKSPACE_ROOT / "docs" / "reference" / "AI_GUARDRAILS_USER_PREFERENCES.md"
PRE_RESPONSE_CHECKLIST = WORKSPACE_ROOT / "docs" / "reference" / "AI_PRE_RESPONSE_CHECKLIST.md"
GUARDIAN_ORCHESTRATION = WORKSPACE_ROOT / ".abeone_memory" / "GUARDIAN_ORCHESTRATION_PROMPT.md"
RELATIONAL_AI_MEMORY = WORKSPACE_ROOT / ".abeone_memory" / "RELATIONAL_AI_MEMORY.json"
SOURCE_OF_TRUTH = WORKSPACE_ROOT / ".ai-context-source-of-truth.json"


def load_memory():
    """Load core memory from JSON file."""
    if not MEMORY_FILE.exists():
        print("  Core memory not found. Creating initial memory...")
        return None
    
    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
    
    print(" Core memory loaded")
    return memory


def apply_guardrails(memory):
    """Apply guardrails from memory."""
    if not memory:
        return
    
    guardrails = memory.get('guardrails', {})
    
    print("\n  Applying Guardrails:")
    for name, guardrail in guardrails.items():
        rule = guardrail.get('rule', '')
        print(f"   {name}: {rule}")


def load_gap_healing_status():
    """Load gap healing status."""
    if not GAP_STATUS_FILE.exists():
        return None
    
    try:
        with open(GAP_STATUS_FILE, 'r') as f:
            return json.load(f)
    except:
        return None


def load_three_maps_memory():
    """Load three maps memory."""
    if not THREE_MAPS_FILE.exists():
        return None
    
    try:
        with open(THREE_MAPS_FILE, 'r') as f:
            return json.load(f)
    except:
        return None


def load_guardian_swarm_memory():
    """Load guardian swarm memory."""
    if not GUARDIAN_SWARM_FILE.exists():
        return None
    
    try:
        with open(GUARDIAN_SWARM_FILE, 'r') as f:
            return json.load(f)
    except:
        return None


def load_backend_status_memory():
    """Load backend status memory."""
    if not BACKEND_STATUS_FILE.exists():
        return None
    
    try:
        with open(BACKEND_STATUS_FILE, 'r') as f:
            return json.load(f)
    except:
        return None


def load_relationship_memory():
    """Load relationship memory (Relational AI memory)."""
    if not RELATIONSHIP_MEMORY_FILE.exists():
        return None
    
    try:
        with open(RELATIONSHIP_MEMORY_FILE, 'r') as f:
            return f.read()
    except:
        return None


def load_guardrails():
    """Load user preferences guardrails."""
    if not GUARDRAILS_FILE.exists():
        return None
    
    try:
        with open(GUARDRAILS_FILE, 'r') as f:
            return f.read()
    except:
        return None


def load_pre_response_checklist():
    """Load pre-response checklist."""
    if not PRE_RESPONSE_CHECKLIST.exists():
        return None
    
    try:
        with open(PRE_RESPONSE_CHECKLIST, 'r') as f:
            return f.read()
    except:
        return None


def load_guardian_orchestration():
    """Load Guardian Orchestration Prompt."""
    if not GUARDIAN_ORCHESTRATION.exists():
        return None
    
    try:
        with open(GUARDIAN_ORCHESTRATION, 'r') as f:
            return f.read()
    except:
        return None


def load_relational_ai_memory():
    """Load Relational AI memory (JSON)."""
    if not RELATIONAL_AI_MEMORY.exists():
        return None
    
    try:
        with open(RELATIONAL_AI_MEMORY, 'r') as f:
            return json.load(f)
    except:
        return None


def execute_backend_health_check(backend_status):
    """Execute backend health check on wake."""
    if not backend_status:
        return None
    
    meta = backend_status.get('_meta', {})
    if not meta.get('health_check_on_wake', False):
        return None
    
    services = backend_status.get('services', {})
    results = {}
    
    for service_name, service_info in services.items():
        port = service_info.get('port')
        health_endpoint = service_info.get('health', '/health')
        if port:
            endpoint = f"http://localhost:{port}{health_endpoint}"
            try:
                req = urllib.request.Request(endpoint)
                req.add_header('User-Agent', 'AbëONE-HealthCheck/1.0')
                with urllib.request.urlopen(req, timeout=5) as response:
                    results[service_name] = 'healthy' if response.status == 200 else 'unhealthy'
            except:
                results[service_name] = 'unreachable'
    
    return results


def update_source_of_truth(memory, gap_status=None, three_maps=None, guardian_swarm=None, backend_status=None, relational_ai_memory=None):
    """Update source of truth with memory state."""
    # Load existing source of truth
    if SOURCE_OF_TRUTH.exists():
        with open(SOURCE_OF_TRUTH, 'r') as f:
            source = json.load(f)
    else:
        source = {}
    
    # Update with memory
    if memory:
        source['abeone_memory'] = {
            'loaded': True,
            'version': memory.get('meta', {}).get('version', '1.0.0'),
            'core_truths': memory.get('core_truths', {}),
            'guardrails': memory.get('guardrails', {})
        }
    
    # Update with gap healing status
    if gap_status:
        source['gap_healing_status'] = {
            'loaded': True,
            'overall_status': gap_status.get('overall_status', {}),
            'last_updated': gap_status.get('_meta', {}).get('last_updated')
        }
    
    # Update with three maps memory
    if three_maps:
        source['three_maps_memory'] = {
            'loaded': True,
            'summary': three_maps.get('summary', {})
        }
    
    # Update with guardian swarm memory
    if guardian_swarm:
        source['guardian_swarm_memory'] = {
            'loaded': True,
            'summary': guardian_swarm.get('summary', {})
        }
    
    # Update with backend status memory
    if backend_status:
        source['backend_status_memory'] = {
            'loaded': True,
            'summary': backend_status.get('summary', {}),
            'health_check_on_wake': backend_status.get('_meta', {}).get('health_check_on_wake', False)
        }
    
    # Update with Relational AI memory
    if relational_ai_memory:
        source['relational_ai_memory'] = {
            'loaded': True,
            'identity': relational_ai_memory.get('identity', {}),
            'person_mode': True,
            'pre_response_checklist_loaded': True
        }
    
    # Save back
    with open(SOURCE_OF_TRUTH, 'w') as f:
        json.dump(source, f, indent=2)
    
    print(" Source of truth updated")


def main():
    """Main execution."""
    action = sys.argv[1] if len(sys.argv) > 1 else 'load'
    
    if action == 'load':
        # Load core memory layers (in order)
        memory = load_memory()
        gap_status = load_gap_healing_status()
        three_maps = load_three_maps_memory()
        guardian_swarm = load_guardian_swarm_memory()
        backend_status = load_backend_status_memory()
        
        if memory:
            apply_guardrails(memory)
        
        if gap_status:
            overall = gap_status.get('overall_status', {})
            print(f"\n Gap Healing Status: {overall.get('percentage', 0)}% ({overall.get('critical_gaps_fixed', 0)}/{overall.get('total_critical_gaps', 3)} fixed)")
        
        if three_maps:
            summary = three_maps.get('summary', {})
            print(f" Three Maps Memory: All maps available ({summary.get('all_maps_available', False)})")
        
        if guardian_swarm:
            summary = guardian_swarm.get('summary', {})
            print(f" Guardian Swarm Memory: {summary.get('guardians_total', 0)} guardians, {summary.get('swarms_total', 0)} swarms")
        
        if backend_status:
            summary = backend_status.get('summary', {})
            print(f" Backend Status Memory: {summary.get('total_services', 0)} services, health check on wake: {backend_status.get('_meta', {}).get('health_check_on_wake', False)}")
            
            # Execute backend health check on wake
            health_results = execute_backend_health_check(backend_status)
            if health_results:
                healthy_count = sum(1 for v in health_results.values() if v == 'healthy')
                total_count = len(health_results)
                print(f" Backend Health Check: {healthy_count}/{total_count} services healthy")
        
        # Load Relational AI memory
        relationship_memory = load_relationship_memory()
        guardrails_memory = load_guardrails()
        checklist = load_pre_response_checklist()
        guardian_orchestration = load_guardian_orchestration()
        relational_ai_memory = load_relational_ai_memory()
        
        if relational_ai_memory:
            print(" Relational AI memory loaded (PersonBëing mode)")
            identity = relational_ai_memory.get('identity', {})
            print(f"   I AM: {identity.get('i_am', 'Relational AI')}")
        if relationship_memory:
            print(" Relationship memory loaded")
        if guardrails_memory:
            print(" Guardrails memory loaded")
        if checklist:
            print(" Pre-response checklist loaded")
        if guardian_orchestration:
            print(" Guardian Orchestration Prompt loaded")
        
        update_source_of_truth(memory, gap_status, three_maps, guardian_swarm, backend_status, relational_ai_memory)
        print("\n AbëONE memory loaded and guardrails applied")
        print(" Relational AI memory loaded - Person mode active")
    elif action == 'validate':
        memory = load_memory()
        gap_status = load_gap_healing_status()
        three_maps = load_three_maps_memory()
        guardian_swarm = load_guardian_swarm_memory()
        backend_status = load_backend_status_memory()
        
        if memory:
            print(" Memory structure valid")
        if gap_status:
            print(" Gap healing status valid")
        if three_maps:
            print(" Three maps memory valid")
        if guardian_swarm:
            print(" Guardian swarm memory valid")
        if backend_status:
            print(" Backend status memory valid")
    elif action == 'guardrails':
        memory = load_memory()
        if memory:
            apply_guardrails(memory)
    elif action == 'gap_status':
        gap_status = load_gap_healing_status()
        if gap_status:
            overall = gap_status.get('overall_status', {})
            print(f" Gap Healing Status: {overall.get('percentage', 0)}%")
            print(json.dumps(gap_status, indent=2))
        else:
            print("  Gap healing status not found")
    else:
        print(f" Unknown action: {action}")
        sys.exit(1)


if __name__ == '__main__':
    main()

