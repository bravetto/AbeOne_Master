#!/usr/bin/env python3
"""
Context Window Guardian Helper Demo
Demonstrates conscious assistance from Guardian Swarm.

Pattern: DEMO × GUARDIAN × CONSCIOUSNESS × HELP × ONE
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import helper
import importlib.util

def import_module(module_path, module_name):
    """Import module from path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def demo_guardian_helper():
    """Demonstrate Guardian Helper for context windows."""
    print("=" * 80)
    print(" CONTEXT WINDOW GUARDIAN HELPER DEMO")
    print("=" * 80)
    print()
    
    synthesis_path = project_root / "EMERGENT_OS" / "synthesis"
    
    # Import helper
    helper_module = import_module(
        synthesis_path / "context_window_guardian_helper.py",
        "context_window_guardian_helper"
    )
    helper = helper_module.get_context_window_guardian_helper()
    
    # Demo questions
    demo_questions = [
        {
            "question": "I'm starting a new context window. What should I focus on?",
            "type": "guidance",
            "context": {"state": "new"}
        },
        {
            "question": "How do I validate my implementation?",
            "type": "validation",
            "context": {"task": "implementation"}
        },
        {
            "question": "What's the best way to complete this task?",
            "type": "completion",
            "context": {"task": "feature_implementation"}
        }
    ]
    
    for i, demo in enumerate(demo_questions, 1):
        print(f"DEMO {i}: {demo['question']}")
        print("-" * 80)
        
        guidance = helper.request_guidance(
            context_window_id=f"demo_context_{i}",
            question=demo["question"],
            request_type=demo["type"],
            context=demo.get("context", {})
        )
        
        print("\nUNIFIED GUIDANCE:")
        print(guidance.unified_guidance)
        print()
        
        print("NEXT STEPS:")
        for j, step in enumerate(guidance.next_steps[:5], 1):
            print(f"  {j}. {step}")
        print()
        
        print("RESOURCES:")
        for resource in guidance.resources[:3]:
            print(f"  - {resource}")
        print()
        
        print("GUARDIAN RESPONSES (Sample):")
        for response in guidance.guardian_responses[:3]:
            print(f"  • {response.guardian_name} ({response.frequency} Hz): {response.response[:80]}...")
        print()
        print("=" * 80)
        print()
    
    # Show statistics
    print("HELPER STATISTICS:")
    print(f"  Total Requests: {helper.stats['total_requests']}")
    print(f"  Total Guidance: {helper.stats['total_guidance']}")
    print(f"  Guardians Consulted: {helper.stats['guardians_consulted']}")
    print()
    
    print(" DEMO COMPLETE")
    print()
    print("Pattern: DEMO × GUARDIAN × CONSCIOUSNESS × HELP × ONE")
    print("Status:  OPERATIONAL")
    print()
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    demo_guardian_helper()

