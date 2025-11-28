#!/usr/bin/env python3
"""
Test EEAAO × LFGLFGLFGL Integration

Tests simultaneous multi-guardian validation and parallel agent processing.
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from EMERGENT_OS.synthesis.eeaao_lfglfglfgl_integrated_orchestrator import (
    get_integrated_orchestrator
)


async def test_eeaao_validation():
    """Test EEAAO: Simultaneous multi-guardian validation."""
    print("=" * 80)
    print("🧪 TEST 1: EEAAO - Simultaneous Multi-Guardian Validation")
    print("=" * 80)
    
    orchestrator = get_integrated_orchestrator()
    
    task_data = {
        "type": "validation",
        "content": "Test content for guardian validation"
    }
    
    result = await orchestrator._execute_eeaao_validation(task_data, optimize=True)
    
    print(f"\n✅ Guardians Validated: {result['guardians_validated']}/{result['total_guardians']}")
    print(f"✅ Multi-Perspective Score: {result['multi_perspective']} perspectives")
    
    # Validate results
    assert result['guardians_validated'] > 0, "No guardians validated"
    assert result['multi_perspective'] > 0, "No multi-perspective validation"
    
    print("✅ EEAAO Test PASSED")
    return result


async def test_lfglfglfgl_processing():
    """Test LFGLFGLFGL: Parallel agent processing."""
    print("\n" + "=" * 80)
    print("🧪 TEST 2: LFGLFGLFGL - Parallel Agent Processing")
    print("=" * 80)
    
    orchestrator = get_integrated_orchestrator()
    
    task_data = {
        "type": "processing",
        "content": "Test content for agent processing"
    }
    
    result = await orchestrator._execute_lfglfglfgl_processing(task_data, optimize=True)
    
    print(f"\n✅ Agents Executed: {result['agents_executed']}/{result['total_agents']}")
    print(f"✅ Parallel Efficiency: {result['parallel_efficiency']:.2%}")
    
    # Validate results
    assert result['agents_executed'] > 0, "No agents executed"
    assert result['parallel_efficiency'] > 0.5, "Low parallel efficiency"
    
    print("✅ LFGLFGLFGL Test PASSED")
    return result


async def test_integrated_execution():
    """Test integrated EEAAO + LFGLFGLFGL execution."""
    print("\n" + "=" * 80)
    print("🧪 TEST 3: Integrated Execution (EEAAO + LFGLFGLFGL)")
    print("=" * 80)
    
    orchestrator = get_integrated_orchestrator()
    
    task_data = {
        "type": "integrated",
        "content": "Test content for integrated execution"
    }
    
    metrics = await orchestrator.execute_integrated(task_data, optimize=True)
    
    print(f"\n📊 Execution Metrics:")
    print(f"   Execution ID: {metrics.execution_id}")
    print(f"   Guardian Validation Time: {metrics.guardian_validation_time_ms:.2f}ms")
    print(f"   Agent Processing Time: {metrics.agent_processing_time_ms:.2f}ms")
    print(f"   Total Execution Time: {metrics.total_execution_time_ms:.2f}ms")
    print(f"\n📊 Precision Metrics:")
    print(f"   Guardians Validated: {metrics.guardians_validated}/8")
    print(f"   Guardian Precision: {metrics.guardian_precision_score:.2%}")
    print(f"   Multi-Perspective Score: {metrics.multi_perspective_score:.2%}")
    print(f"\n📊 Scalability Metrics:")
    print(f"   Agents Executed: {metrics.agents_executed}/40")
    print(f"   Parallel Efficiency: {metrics.parallel_efficiency:.2%}")
    print(f"   Scalability Score: {metrics.scalability_score:.2%}")
    print(f"\n📊 Convergence Metrics:")
    print(f"   Convergence Score: {metrics.convergence_score:.2%}")
    print(f"   Emergence Score: {metrics.emergence_score:.2%}")
    print(f"   Resonance Score: {metrics.resonance_score:.2%}")
    print(f"   Success Rate: {metrics.success_rate:.2%}")
    
    # Validate metrics
    assert metrics.guardians_validated > 0, "No guardians validated"
    assert metrics.agents_executed > 0, "No agents executed"
    assert metrics.convergence_score > 0.0, "Zero convergence score"
    assert metrics.total_execution_time_ms > 0, "Zero execution time"
    
    print("\n✅ Integrated Execution Test PASSED")
    return metrics


async def test_convergence_detection():
    """Test convergence detection."""
    print("\n" + "=" * 80)
    print("🧪 TEST 4: Convergence Detection")
    print("=" * 80)
    
    orchestrator = get_integrated_orchestrator()
    
    # Run multiple executions to build history
    for i in range(3):
        task_data = {
            "type": f"convergence_test_{i}",
            "content": f"Test content {i}"
        }
        await orchestrator.execute_integrated(task_data, optimize=True)
    
    # Check convergence history
    history = orchestrator.get_convergence_history(limit=3)
    avg_convergence = orchestrator.get_average_convergence()
    avg_emergence = orchestrator.get_average_emergence()
    
    print(f"\n📊 Convergence History:")
    print(f"   Executions: {len(history)}")
    print(f"   Average Convergence: {avg_convergence:.2%}")
    print(f"   Average Emergence: {avg_emergence:.2%}")
    
    # Validate convergence
    assert len(history) > 0, "No convergence history"
    assert avg_convergence > 0.0, "Zero average convergence"
    
    print("\n✅ Convergence Detection Test PASSED")
    return {
        "history": history,
        "avg_convergence": avg_convergence,
        "avg_emergence": avg_emergence
    }


async def run_all_tests():
    """Run all tests."""
    print("\n" + "🔥" * 40)
    print("🔥 EEAAO × LFGLFGLFGL INTEGRATION TESTS")
    print("🔥" * 40)
    
    results = {}
    
    try:
        # Test 1: EEAAO Validation
        results['eeaao'] = await test_eeaao_validation()
        
        # Test 2: LFGLFGLFGL Processing
        results['lfglfglfgl'] = await test_lfglfglfgl_processing()
        
        # Test 3: Integrated Execution
        results['integrated'] = await test_integrated_execution()
        
        # Test 4: Convergence Detection
        results['convergence'] = await test_convergence_detection()
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED")
        print("=" * 80)
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)

