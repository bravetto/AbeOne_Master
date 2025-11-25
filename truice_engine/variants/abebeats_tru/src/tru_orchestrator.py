"""
TRUICE Pipeline Orchestrator

Orchestrator with proper failure propagation.

Pattern: ORCHESTRATION × FAILURE_PROPAGATION × TRUTH × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import logging

from .tru_activity_types import Activity, ActivityResult
from .tru_visual_test_framework import TruVisualTestFramework, VisualTestResult

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Result of pipeline execution."""
    success: bool
    error: Optional[str] = None
    core_failures: Optional[List[Dict[str, Any]]] = None
    results: Optional[List[ActivityResult]] = None
    visual_validation: Optional[VisualTestResult] = None


class TruiceOrchestrator:
    """
    TRUICE pipeline orchestrator with proper failure propagation.
    
    Pattern: ORCHESTRATION × FAILURE_PROPAGATION × TRUTH × ONE
    """
    
    def __init__(self, visual_test_framework: Optional[TruVisualTestFramework] = None):
        """
        Initialize orchestrator.
        
        SAFETY: Validates visual test framework if provided
        ASSUMES: Visual test framework is optional
        VERIFY: Framework is valid if provided
        """
        self.visual_test_framework = visual_test_framework
        logger.info("TruiceOrchestrator initialized")
    
    def execute_pipeline(
        self,
        activities: List[Activity]
    ) -> PipelineResult:
        """
        Execute pipeline with core function failure propagation.
        
        SAFETY: Core function failure = pipeline failure
        ASSUMES: Activities are properly classified
        VERIFY: Pipeline fails if core function fails
        """
        logger.info(f"Executing pipeline with {len(activities)} activities")
        results = []
        core_failures = []
        
        # Execute all activities
        for activity in activities:
            logger.debug(f"Executing activity: {activity.name} (type: {activity.activity_type.value})")
            result = activity.execute()
            results.append(result)
            
            # Check if this is a core function
            if activity.is_core_function():
                if not result.success:
                    logger.error(f"Core function failed: {activity.name} - {result.error}")
                    core_failures.append({
                        'activity': activity.name,
                        'error': result.error
                    })
                else:
                    logger.info(f"Core function succeeded: {activity.name}")
            
            # Handler activities don't mask core failures
            # (They can fail independently, but don't override core failure)
        
        # Core function failure = pipeline failure
        if core_failures:
            logger.error(f"Pipeline failed: {len(core_failures)} core function(s) failed")
            return PipelineResult(
                success=False,
                error=f"Core function(s) failed: {core_failures}",
                core_failures=core_failures,
                results=results
            )
        
        # Visual validation gate (if enabled)
        if self.visual_test_framework:
            output = self._get_pipeline_output(results, activities)
            if output:
                logger.info(f"Running visual validation on: {output}")
                visual_result = self.visual_test_framework.validate_output(output)
                
                if not visual_result.passed:
                    logger.error(f"Visual validation failed: {visual_result.error}")
                    return PipelineResult(
                        success=False,
                        error=f"Visual validation failed: {visual_result.error}",
                        visual_validation=visual_result,
                        results=results
                    )
                else:
                    logger.info(f"Visual validation passed: {visual_result.similarity:.2f} similarity")
        
        # Only succeed if all core functions succeeded
        logger.info("Pipeline execution completed successfully")
        return PipelineResult(
            success=True,
            results=results
        )
    
    def _get_pipeline_output(
        self,
        results: List[ActivityResult],
        activities: List[Activity]
    ) -> Optional[Path]:
        """
        Extract output path from results.
        
        VERIFY: Returns Path if output found, None otherwise
        """
        # Find output from last core function
        for result, activity in zip(reversed(results), reversed(activities)):
            if activity.is_core_function() and result.output:
                if isinstance(result.output, Path):
                    return result.output
                elif isinstance(result.output, dict) and 'output_path' in result.output:
                    return Path(result.output['output_path'])
                elif isinstance(result.output, dict) and 'output' in result.output:
                    output_val = result.output['output']
                    if isinstance(output_val, (str, Path)):
                        return Path(output_val)
        
        return None

