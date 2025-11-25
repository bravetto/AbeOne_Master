#!/usr/bin/env python3
"""
ARDM Integration Example

Shows how to integrate ARDM into existing workflows.

Pattern: AEYON × ARDM × INTEGRATION × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

# Import ARDM detector
# Note: Import from module name (hyphens converted to underscores in Python)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "detect_actionable_requests",
    Path(__file__).parent / "detect-actionable-requests.py"
)
detect_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(detect_module)
ActionableRequestDetector = detect_module.ActionableRequestDetector
ARDMResult = detect_module.ARDMResult


def integrate_with_meta_orchestrator(conversation_text: str) -> ARDMResult:
    """
    Example: Integrate ARDM with Meta Orchestrator
    
    This function can be called before operationalization
    to detect all actionable items.
    """
    detector = ActionableRequestDetector()
    result = detector.scan(conversation_text)
    
    # If items detected, operationalize them
    if result.total_items > 0:
        print(f" ARDM detected {result.total_items} actionable items")
        print("\n" + detector.to_markdown(result))
        
        # Here you would pass result to Meta Orchestrator
        # for operationalization
    
    return result


def integrate_with_pre_commit(conversation_text: str) -> bool:
    """
    Example: Integrate ARDM with pre-commit hooks
    
    Returns True if all actionable items are delivered.
    """
    detector = ActionableRequestDetector()
    result = detector.scan(conversation_text)
    
    # Check if there are undelivered items
    if result.total_items > 0:
        print("  Warning: Undelivered actionable items detected")
        print("\n" + detector.to_markdown(result))
        return False
    
    return True


def integrate_with_validation(conversation_text: str) -> Dict:
    """
    Example: Integrate ARDM with validation workflows
    
    Returns validation report with actionable items.
    """
    detector = ActionableRequestDetector()
    result = detector.scan(conversation_text)
    
    validation_report = {
        "has_actionable_items": result.total_items > 0,
        "total_items": result.total_items,
        "by_category": {
            cat.value: len(result.delta[cat])
            for cat in result.delta.keys()
        },
        "report": detector.to_markdown(result),
    }
    
    return validation_report


if __name__ == "__main__":
    # Example usage
    example_conversation = """
    I need to implement a new feature for user authentication.
    Create a file called auth.py with login and logout functions.
    Also, we should set up a validator for the authentication module.
    I'll generate the test cases next.
    """
    
    print(" ARDM Integration Example")
    print("=" * 60)
    
    # Example 1: Meta Orchestrator integration
    print("\n1. Meta Orchestrator Integration:")
    result = integrate_with_meta_orchestrator(example_conversation)
    
    # Example 2: Pre-commit integration
    print("\n2. Pre-commit Integration:")
    all_delivered = integrate_with_pre_commit(example_conversation)
    print(f"   All items delivered: {all_delivered}")
    
    # Example 3: Validation integration
    print("\n3. Validation Integration:")
    validation = integrate_with_validation(example_conversation)
    print(f"   Has actionable items: {validation['has_actionable_items']}")
    print(f"   Total items: {validation['total_items']}")
    print(f"   By category: {validation['by_category']}")

