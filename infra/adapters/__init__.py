"""
AbëONE Master Workspace Adapters

Orbit-Spec v1.0 compliant adapters for workspace orchestration.

Pattern: ADAPTERS × WORKSPACE × ORCHESTRATOR × ONE
"""

# Note: Adapters use dots in their names (adapter.kernel.py) which requires
# importlib or direct imports. Users should import directly:
# import importlib
# kernel_module = importlib.import_module('adapters.adapter.kernel')
# Or use sys.path manipulation

__all__ = [
    "adapter.kernel",
    "adapter.guardians",
    "adapter.module",
    "adapter.bus"
]
