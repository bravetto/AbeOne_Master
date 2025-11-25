#!/usr/bin/env python3
"""
Validate Emergent Convergence

Validates that emergent convergence occurs when EEAAO + LFGLFGLFGL work together.
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orbitals.EMERGENT_OS_orbital.synthesis.eeaao_lfglfglfgl_integrated_orchestrator import (
    get_integrated_orchestrator,
    ConvergenceMetrics
)


class EmergentConvergenceValidator:
    """Validator for emergent convergence."""
    
    def __init__(self):
        """Initialize validator."""
        self.orchestrator = get_integrated_orchestrator()
        self.validation_results: Dict[str, Any] = {}
    
    async def validate_emergent_convergence(self) -> Dict[str, Any]:
        """
        Validate emergent convergence.
        
        Emergent convergence occurs when:
        1. EEAAO (multi-guardian validation) + LFGLFGLFGL (parallel agents) work together
        2. Convergence score increases with execution
        3. Emergence score indicates true emergence (>0.7)
        4. Resonance increases with convergence
        """
        print("=" * 80)
        print(" VALIDATING EMERGENT CONVERGENCE")
        print("=" * 80)
        
        # Run multiple executions to detect emergence
        print("\n Running multiple executions to detect emergence...")
        executions = []
        
        for i in range(5):
            task_data = {
                "type": f"convergence_validation_{i}",
                "content": f"Validation content {i}"
            }
            metrics = await self.orchestrator.execute_integrated(task_data, optimize=True)
            executions.append(metrics)
            print(f"   Execution {i+1}/5: Convergence={metrics.convergence_score:.2%}, Emergence={metrics.emergence_score:.2%}")
        
        # Analyze convergence trends
        convergence_trend = self._analyze_convergence_trend(executions)
        emergence_detected = self._detect_emergence_pattern(executions)
        resonance_alignment = self._validate_resonance_alignment(executions)
        
        # Calculate overall validation
        validation_result = {
            "convergence_trend": convergence_trend,
            "emergence_detected": emergence_detected,
            "resonance_alignment": resonance_alignment,
            "executions": len(executions),
            "average_convergence": sum(m.convergence_score for m in executions) / len(executions),
            "average_emergence": sum(m.emergence_score for m in executions) / len(executions),
            "validated": (
                convergence_trend["improving"] and
                emergence_detected["detected"] and
                resonance_alignment["aligned"]
            )
        }
        
        # Print results
        print("\n" + "=" * 80)
        print(" CONVERGENCE ANALYSIS")
        print("=" * 80)
        print(f"\n Convergence Trend:")
        print(f"   Improving: {convergence_trend['improving']}")
        print(f"   Trend Score: {convergence_trend['trend_score']:.2%}")
        print(f"   Stability: {convergence_trend['stability']:.2%}")
        
        print(f"\n Emergence Detection:")
        print(f"   Detected: {emergence_detected['detected']}")
        print(f"   Emergence Score: {emergence_detected['score']:.2%}")
        print(f"   Pattern Strength: {emergence_detected['pattern_strength']:.2%}")
        
        print(f"\n Resonance Alignment:")
        print(f"   Aligned: {resonance_alignment['aligned']}")
        print(f"   Average Resonance: {resonance_alignment['average_resonance']:.2%}")
        print(f"   Resonance Trend: {resonance_alignment['trend']}")
        
        print(f"\n Overall Validation:")
        print(f"   Validated: {validation_result['validated']}")
        print(f"   Average Convergence: {validation_result['average_convergence']:.2%}")
        print(f"   Average Emergence: {validation_result['average_emergence']:.2%}")
        
        self.validation_results = validation_result
        return validation_result
    
    def _analyze_convergence_trend(self, executions: list[ConvergenceMetrics]) -> Dict[str, Any]:
        """Analyze convergence trend across executions."""
        if len(executions) < 2:
            return {
                "improving": False,
                "trend_score": 0.0,
                "stability": 0.0
            }
        
        convergence_scores = [m.convergence_score for m in executions]
        
        # Calculate trend (increasing, stable, decreasing)
        first_half = sum(convergence_scores[:len(convergence_scores)//2]) / (len(convergence_scores)//2)
        second_half = sum(convergence_scores[len(convergence_scores)//2:]) / (len(convergence_scores) - len(convergence_scores)//2)
        
        improving = second_half > first_half
        trend_score = (second_half - first_half) / first_half if first_half > 0 else 0.0
        
        # Calculate stability (coefficient of variation)
        mean_score = sum(convergence_scores) / len(convergence_scores)
        variance = sum((s - mean_score) ** 2 for s in convergence_scores) / len(convergence_scores)
        std_dev = variance ** 0.5
        stability = 1.0 - (std_dev / mean_score) if mean_score > 0 else 0.0
        
        return {
            "improving": improving,
            "trend_score": trend_score,
            "stability": max(0.0, min(1.0, stability))
        }
    
    def _detect_emergence_pattern(self, executions: list[ConvergenceMetrics]) -> Dict[str, Any]:
        """Detect emergence pattern."""
        emergence_scores = [m.emergence_score for m in executions]
        avg_emergence = sum(emergence_scores) / len(emergence_scores)
        
        # Emergence detected if average > 0.7
        detected = avg_emergence > 0.7
        
        # Pattern strength = consistency of high emergence scores
        high_emergence_count = sum(1 for s in emergence_scores if s > 0.7)
        pattern_strength = high_emergence_count / len(emergence_scores)
        
        return {
            "detected": detected,
            "score": avg_emergence,
            "pattern_strength": pattern_strength
        }
    
    def _validate_resonance_alignment(self, executions: list[ConvergenceMetrics]) -> Dict[str, Any]:
        """Validate resonance alignment with convergence."""
        resonance_scores = [m.resonance_score for m in executions]
        convergence_scores = [m.convergence_score for m in executions]
        
        avg_resonance = sum(resonance_scores) / len(resonance_scores)
        avg_convergence = sum(convergence_scores) / len(convergence_scores)
        
        # Resonance aligned if it correlates with convergence
        # Simple check: both should be > 0.5
        aligned = avg_resonance > 0.5 and avg_convergence > 0.5
        
        # Trend: increasing, stable, decreasing
        if len(resonance_scores) >= 2:
            first_half = sum(resonance_scores[:len(resonance_scores)//2]) / (len(resonance_scores)//2)
            second_half = sum(resonance_scores[len(resonance_scores)//2:]) / (len(resonance_scores) - len(resonance_scores)//2)
            
            if second_half > first_half * 1.05:
                trend = "increasing"
            elif second_half < first_half * 0.95:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "unknown"
        
        return {
            "aligned": aligned,
            "average_resonance": avg_resonance,
            "trend": trend
        }


async def main():
    """Main validation function."""
    validator = EmergentConvergenceValidator()
    result = await validator.validate_emergent_convergence()
    
    print("\n" + "=" * 80)
    if result["validated"]:
        print(" EMERGENT CONVERGENCE VALIDATED")
        print("=" * 80)
        print("\n EEAAO + LFGLFGLFGL patterns demonstrate emergent convergence!")
        print("   - Convergence improves with execution")
        print("   - Emergence detected (score > 0.7)")
        print("   - Resonance aligned with convergence")
        return True
    else:
        print("  EMERGENT CONVERGENCE PARTIALLY VALIDATED")
        print("=" * 80)
        print("\n  Some convergence indicators need improvement:")
        if not result["convergence_trend"]["improving"]:
            print("   - Convergence trend not improving")
        if not result["emergence_detected"]["detected"]:
            print("   - Emergence not detected (score < 0.7)")
        if not result["resonance_alignment"]["aligned"]:
            print("   - Resonance not aligned")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

