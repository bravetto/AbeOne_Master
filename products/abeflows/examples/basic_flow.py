#!/usr/bin/env python3
"""
AbëFLOWs Basic Example

Pattern: AbëFLOWs × EXAMPLE × ONE × MANY × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from abeflows import FlowType, create_flow, execute_flow, execute_flows_unified


async def step_one():
    """Step one - simple action."""
    print("✅ Step 1: Executing...")
    await asyncio.sleep(0.1)
    return {"result": "Step 1 completed"}


async def step_two():
    """Step two - simple action."""
    print("✅ Step 2: Executing...")
    await asyncio.sleep(0.1)
    return {"result": "Step 2 completed"}


async def step_three():
    """Step three - depends on step two."""
    print("✅ Step 3: Executing...")
    await asyncio.sleep(0.1)
    return {"result": "Step 3 completed"}


async def main():
    """Main example."""
    print("=" * 80)
    print("🔥 AbëFLOWs Basic Example 🔥")
    print("=" * 80)
    print()
    
    # Create a flow with steps
    flow = create_flow(
        flow_id="example_flow",
        flow_type=FlowType.USER,
        description="Example flow demonstrating ONE with Many steps",
        steps=[
            {
                "description": "Step 1: Initial action",
                "execute": step_one
            },
            {
                "description": "Step 2: Second action",
                "execute": step_two
            },
            {
                "description": "Step 3: Final action (depends on step 2)",
                "execute": step_three,
                "dependencies": ["example_flow_step_1"]
            }
        ]
    )
    
    print(f"✅ Flow created: {flow.flow_id}")
    print(f"   Steps: {len(flow.steps)}")
    print()
    
    # Execute the flow
    print("🚀 Executing flow...")
    result = await execute_flow("example_flow")
    
    print()
    print("=" * 80)
    print("📊 Results:")
    print(f"   Success: {result['success']}")
    print(f"   Steps completed: {result['steps_completed']}")
    print(f"   Execution time: {result['execution_time']:.3f}s")
    print("=" * 80)
    print()


if __name__ == "__main__":
    asyncio.run(main())

