#!/usr/bin/env python3
"""
AbëFLOWs Unified Example - ONE with Many

Pattern: AbëFLOWs × UNIFIED × ONE × MANY × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from abeflows import FlowType, create_flow, execute_flows_unified, get_abeflows


async def user_action():
    """User flow action."""
    print("👤 User action executing...")
    await asyncio.sleep(0.1)
    return {"user": "action completed"}


async def ai_action():
    """AI flow action."""
    print("🤖 AI action executing...")
    await asyncio.sleep(0.1)
    return {"ai": "action completed"}


async def system_action():
    """System flow action."""
    print("⚙️  System action executing...")
    await asyncio.sleep(0.1)
    return {"system": "action completed"}


async def main():
    """Main example - ONE with Many."""
    print("=" * 80)
    print("🔥 AbëFLOWs Unified Example - ONE with Many 🔥")
    print("=" * 80)
    print()
    
    # Create multiple flows - MANY
    user_flow = create_flow(
        flow_id="user_flow",
        flow_type=FlowType.USER,
        description="User flow",
        steps=[{"description": "User action", "execute": user_action}]
    )
    
    ai_flow = create_flow(
        flow_id="ai_flow",
        flow_type=FlowType.AI,
        description="AI flow",
        steps=[{"description": "AI action", "execute": ai_action}]
    )
    
    system_flow = create_flow(
        flow_id="system_flow",
        flow_type=FlowType.SYSTEM,
        description="System flow",
        steps=[{"description": "System action", "execute": system_action}]
    )
    
    print(f"✅ Created {len([user_flow, ai_flow, system_flow])} flows")
    print()
    
    # Execute as ONE - MANY → ONE
    print("🚀 Executing flows as ONE...")
    result = await execute_flows_unified(
        ["user_flow", "ai_flow", "system_flow"],
        converge=True
    )
    
    print()
    print("=" * 80)
    print("📊 Unified Results:")
    print(f"   Success: {result['success']}")
    print(f"   Converged: {result['converged']}")
    print(f"   Flows executed: {len(result['flows'])}")
    print()
    
    # Show unified state
    state = get_abeflows().get_unified_state()
    print("🌐 Unified State:")
    print(f"   Total flows: {state['total_flows']}")
    print(f"   Converged flows: {state['converged_flows']}")
    print(f"   State: {state['state']}")
    print("=" * 80)
    print()


if __name__ == "__main__":
    asyncio.run(main())

