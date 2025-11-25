"""
Learning Synchronization Protocol
Synchronizes learning across all instances using consensus mechanism.

Pattern: SYNCHRONIZATION × CONSENSUS × LEARNING × CONVERGENCE × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (ARXON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import logging
import time

from .federated_convergence_types import (
    InstanceMetadata,
    InstanceScores,
    PatternSignature,
    AggregatedPattern,
    SynchronizationResult,
    GlobalConvergenceScore
)
from .federated_learning_convergence import FederatedLearningConvergence
from .global_scoring_aggregator import GlobalScoringAggregator

logger = logging.getLogger(__name__)


class LearningSynchronizationProtocol:
    """
    Learning Synchronization Protocol.
    
    Synchronizes learning across all instances using consensus mechanism.
    
    Protocol:
    1. Collect pattern updates from all instances
    2. Validate pattern quality and epistemic certainty
    3. Aggregate patterns using weighted consensus
    4. Detect convergence opportunities
    5. Distribute aggregated knowledge back to instances
    6. Verify convergence achieved
    
    Features:
    - Configurable sync windows (default: 1 hour)
    - Collection phase (gather updates from instances)
    - Validation phase (epistemic certainty checks)
    - Consensus aggregation (weighted voting)
    - Distribution phase (push aggregated knowledge)
    - Verification phase (convergence validation)
    
    SAFETY: Validates all patterns before aggregation
    ASSUMES: Instances are registered and healthy
    VERIFY: Convergence achieved after synchronization
    """
    
    def __init__(
        self,
        federated_learning: FederatedLearningConvergence,
        global_scoring: GlobalScoringAggregator,
        sync_window: timedelta = timedelta(hours=1),
        min_instances_for_sync: int = 2
    ):
        """
        Initialize learning synchronization protocol.
        
        Args:
            federated_learning: FederatedLearningConvergence instance
            global_scoring: GlobalScoringAggregator instance
            sync_window: Time window for synchronization
            min_instances_for_sync: Minimum instances required for sync
        """
        self.federated_learning = federated_learning
        self.global_scoring = global_scoring
        self.sync_window = sync_window
        self.min_instances_for_sync = min_instances_for_sync
        
        # Synchronization state
        self.last_sync_time: Optional[datetime] = None
        self.sync_history: List[SynchronizationResult] = []
        
        # Callbacks for instance communication (simulated)
        self.instance_update_callbacks: Dict[str, Callable] = {}
        self.instance_distribution_callbacks: Dict[str, Callable] = {}
        
        # Statistics
        self.stats: Dict[str, Any] = {
            "total_syncs": 0,
            "successful_syncs": 0,
            "failed_syncs": 0,
            "total_patterns_synced": 0
        }
    
    def register_instance_callback(
        self,
        instance_id: str,
        update_callback: Optional[Callable] = None,
        distribution_callback: Optional[Callable] = None
    ) -> None:
        """
        Register callbacks for instance communication.
        
        Args:
            instance_id: Instance identifier
            update_callback: Callback to receive updates from instance
            distribution_callback: Callback to distribute knowledge to instance
        """
        if update_callback:
            self.instance_update_callbacks[instance_id] = update_callback
        if distribution_callback:
            self.instance_distribution_callbacks[instance_id] = distribution_callback
    
    async def synchronize_learning(
        self,
        sync_window: Optional[timedelta] = None
    ) -> SynchronizationResult:
        """
        Synchronize learning across all instances.
        
        Protocol:
        1. Collect pattern updates from all instances
        2. Validate pattern quality and epistemic certainty
        3. Aggregate patterns using weighted consensus
        4. Detect convergence opportunities
        5. Distribute aggregated knowledge back to instances
        6. Verify convergence achieved
        
        SAFETY: Validates all patterns before aggregation
        ASSUMES: Instances are registered and healthy
        VERIFY: Convergence achieved after synchronization
        
        Args:
            sync_window: Optional override for sync window
            
        Returns:
            SynchronizationResult with sync metrics
        """
        sync_start_time = time.time()
        sync_window = sync_window or self.sync_window
        
        logger.info(f"Starting learning synchronization (window: {sync_window})")
        
        errors: List[str] = []
        warnings: List[str] = []
        
        try:
            # Phase 1: Collection
            logger.info("Phase 1: Collecting instance updates...")
            instance_updates = await self._collect_instance_updates(sync_window)
            
            if not instance_updates:
                error_msg = "No instance updates collected"
                errors.append(error_msg)
                logger.warning(error_msg)
                return SynchronizationResult(
                    convergence_score=0.0,
                    instances_synced=0,
                    patterns_aggregated=0,
                    convergence_achieved=False,
                    next_sync_window=datetime.now() + sync_window,
                    sync_duration_ms=(time.time() - sync_start_time) * 1000,
                    errors=errors,
                    warnings=warnings
                )
            
            # Phase 2: Validation
            logger.info("Phase 2: Validating updates...")
            validated_updates = self._validate_updates(instance_updates)
            
            if not validated_updates:
                error_msg = "No validated updates after validation phase"
                errors.append(error_msg)
                logger.warning(error_msg)
                return SynchronizationResult(
                    convergence_score=0.0,
                    instances_synced=0,
                    patterns_aggregated=0,
                    convergence_achieved=False,
                    next_sync_window=datetime.now() + sync_window,
                    sync_duration_ms=(time.time() - sync_start_time) * 1000,
                    errors=errors,
                    warnings=warnings
                )
            
            # Phase 3: Aggregation (consensus-based)
            logger.info("Phase 3: Aggregating with consensus...")
            aggregated_knowledge = await self._aggregate_with_consensus(validated_updates)
            
            # Phase 4: Convergence detection
            logger.info("Phase 4: Detecting convergence...")
            convergence_metrics = await self._detect_convergence(aggregated_knowledge)
            
            # Phase 5: Distribution
            logger.info("Phase 5: Distributing knowledge...")
            distribution_result = await self._distribute_knowledge(aggregated_knowledge)
            
            if distribution_result.get("errors"):
                errors.extend(distribution_result["errors"])
            if distribution_result.get("warnings"):
                warnings.extend(distribution_result["warnings"])
            
            # Phase 6: Verification
            logger.info("Phase 6: Verifying convergence...")
            verification = await self._verify_convergence(convergence_metrics)
            
            sync_duration_ms = (time.time() - sync_start_time) * 1000
            self.last_sync_time = datetime.now()
            
            result = SynchronizationResult(
                convergence_score=convergence_metrics.get("global_convergence", 0.0),
                instances_synced=len(validated_updates),
                patterns_aggregated=aggregated_knowledge.get("pattern_count", 0),
                convergence_achieved=verification.get("converged", False),
                next_sync_window=datetime.now() + sync_window,
                sync_duration_ms=sync_duration_ms,
                errors=errors,
                warnings=warnings
            )
            
            self.sync_history.append(result)
            self.stats["total_syncs"] += 1
            
            if verification.get("converged", False):
                self.stats["successful_syncs"] += 1
                logger.info(f" Synchronization successful: convergence achieved")
            else:
                self.stats["failed_syncs"] += 1
                logger.warning(f" Synchronization completed but convergence not achieved")
            
            self.stats["total_patterns_synced"] += aggregated_knowledge.get("pattern_count", 0)
            
            return result
            
        except Exception as e:
            error_msg = f"Synchronization failed: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg, exc_info=True)
            
            self.stats["failed_syncs"] += 1
            
            return SynchronizationResult(
                convergence_score=0.0,
                instances_synced=0,
                patterns_aggregated=0,
                convergence_achieved=False,
                next_sync_window=datetime.now() + sync_window,
                sync_duration_ms=(time.time() - sync_start_time) * 1000,
                errors=errors,
                warnings=warnings
            )
    
    async def _collect_instance_updates(
        self,
        sync_window: timedelta
    ) -> Dict[str, Dict[str, Any]]:
        """
        Collect pattern updates from all instances.
        
        SAFETY: Only collects from healthy instances
        ASSUMES: Instances are registered
        VERIFY: Updates collected successfully
        """
        instance_updates: Dict[str, Dict[str, Any]] = {}
        
        # Get all active instances
        active_instances = [
            instance_id
            for instance_id, instance in self.federated_learning.instance_registry.items()
            if self.federated_learning.check_instance_health(instance_id)
        ]
        
        if len(active_instances) < self.min_instances_for_sync:
            logger.warning(
                f"Not enough active instances for sync: {len(active_instances)} < {self.min_instances_for_sync}"
            )
            return instance_updates
        
        # Collect updates from each instance
        for instance_id in active_instances:
            try:
                # Use callback if registered, otherwise simulate
                if instance_id in self.instance_update_callbacks:
                    callback = self.instance_update_callbacks[instance_id]
                    update = await callback(instance_id, sync_window)
                else:
                    # Simulate: get patterns from federated learning system
                    instance_patterns = self.federated_learning.instance_patterns.get(instance_id, [])
                    update = {
                        "instance_id": instance_id,
                        "patterns": [p.to_dict() for p in instance_patterns],
                        "timestamp": datetime.now().isoformat()
                    }
                
                instance_updates[instance_id] = update
                
            except Exception as e:
                logger.warning(f"Failed to collect update from instance {instance_id}: {e}")
                continue
        
        logger.info(f"Collected updates from {len(instance_updates)} instances")
        
        return instance_updates
    
    def _validate_updates(
        self,
        instance_updates: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Validate pattern quality and epistemic certainty.
        
        SAFETY: Validates epistemic certainty threshold
        ASSUMES: Updates contain pattern data
        VERIFY: Patterns meet quality threshold
        """
        validated_updates: Dict[str, Dict[str, Any]] = {}
        
        for instance_id, update in instance_updates.items():
            patterns = update.get("patterns", [])
            validated_patterns = []
            
            for pattern_data in patterns:
                # Validate epistemic certainty
                epistemic_certainty = pattern_data.get("epistemic_certainty", 0.0)
                
                if epistemic_certainty >= self.federated_learning.min_epistemic_certainty:
                    validated_patterns.append(pattern_data)
                else:
                    logger.debug(
                        f"Pattern rejected from {instance_id}: "
                        f"epistemic_certainty={epistemic_certainty} < {self.federated_learning.min_epistemic_certainty}"
                    )
            
            if validated_patterns:
                validated_updates[instance_id] = {
                    **update,
                    "patterns": validated_patterns
                }
        
        logger.info(f"Validated {len(validated_updates)} instance updates")
        
        return validated_updates
    
    async def _aggregate_with_consensus(
        self,
        validated_updates: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Aggregate patterns using weighted consensus.
        
        SAFETY: Uses weighted voting based on instance reliability
        ASSUMES: Updates are validated
        VERIFY: Aggregation successful
        """
        # Aggregate patterns from all instances
        all_patterns: List[Dict[str, Any]] = []
        
        for instance_id, update in validated_updates.items():
            patterns = update.get("patterns", [])
            
            # Convert pattern signatures back to pattern dicts for aggregation
            for pattern_data in patterns:
                pattern_dict = {
                    "pattern_id": pattern_data.get("signature_id", "unknown"),
                    "pattern_type": pattern_data.get("pattern_type", "unknown"),
                    "strength": pattern_data.get("strength", 0.0),
                    "resonance": pattern_data.get("resonance", 0.0),
                    "frequency": pattern_data.get("frequency", 1),
                    "epistemic_certainty": pattern_data.get("epistemic_certainty", 0.0),
                    "modules": pattern_data.get("module_signatures", []),
                    "event_types": pattern_data.get("event_type_signatures", [])
                }
                
                # Aggregate learning
                await self.federated_learning.aggregate_learning(
                    instance_id,
                    [pattern_dict]
                )
            
            all_patterns.extend(patterns)
        
        # Get aggregated patterns from global library
        global_patterns = list(self.federated_learning.get_global_pattern_library().values())
        
        return {
            "pattern_count": len(all_patterns),
            "global_patterns": global_patterns,
            "instances_contributing": len(validated_updates)
        }
    
    async def _detect_convergence(
        self,
        aggregated_knowledge: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Detect convergence opportunities.
        
        Returns convergence metrics.
        """
        # Get instance scores
        instance_scores: Dict[str, InstanceScores] = {}
        instance_metadata: Dict[str, InstanceMetadata] = {}
        
        for instance_id, instance in self.federated_learning.instance_registry.items():
            if instance.pattern_count > 0:
                # Create instance scores from convergence result
                convergence_result = self.federated_learning._calculate_convergence_score()
                emergence_score = self.federated_learning._detect_cross_instance_emergence()
                
                instance_scores[instance_id] = InstanceScores(
                    instance_id=instance_id,
                    convergence_score=convergence_result,
                    emergence_score=emergence_score,
                    resonance_score=0.8,  # Default resonance
                    unified_score=(convergence_result + emergence_score) / 2.0,
                    pattern_count=instance.pattern_count
                )
                
                instance_metadata[instance_id] = instance
        
        # Calculate global convergence
        global_patterns = aggregated_knowledge.get("global_patterns", [])
        
        # Calculate global convergence (synchronous call to async function)
        # Since we're in an async context, we can await directly
        global_score = await self.global_scoring.calculate_global_convergence(
            instance_scores,
            instance_metadata,
            global_patterns
        )
        
        return {
            "global_convergence": global_score.global_convergence,
            "pattern_alignment": global_score.pattern_alignment,
            "global_emergence": global_score.global_emergence,
            "convergence_variance": global_score.convergence_variance,
            "global_score": global_score
        }
    
    async def _distribute_knowledge(
        self,
        aggregated_knowledge: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Distribute aggregated knowledge back to instances.
        
        SAFETY: Validates distribution success
        ASSUMES: Instances are registered
        VERIFY: Knowledge distributed successfully
        """
        errors: List[str] = []
        warnings: List[str] = []
        
        global_patterns = aggregated_knowledge.get("global_patterns", [])
        
        # Distribute to each instance
        for instance_id in self.federated_learning.instance_registry.keys():
            try:
                # Use callback if registered, otherwise simulate
                if instance_id in self.instance_distribution_callbacks:
                    callback = self.instance_distribution_callbacks[instance_id]
                    await callback(instance_id, global_patterns)
                else:
                    # Simulate: knowledge is already in global library
                    logger.debug(f"Knowledge distribution simulated for {instance_id}")
                
            except Exception as e:
                error_msg = f"Failed to distribute knowledge to {instance_id}: {e}"
                errors.append(error_msg)
                logger.warning(error_msg)
        
        if errors:
            logger.warning(f"Distribution completed with {len(errors)} errors")
        
        return {
            "distributed": True,
            "errors": errors,
            "warnings": warnings
        }
    
    async def _verify_convergence(
        self,
        convergence_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Verify convergence achieved.
        
        Returns verification result.
        """
        global_score = convergence_metrics.get("global_score")
        
        if not global_score:
            return {"converged": False, "reason": "No global score available"}
        
        converged = self.global_scoring.validate_convergence(global_score)
        
        return {
            "converged": converged,
            "global_convergence": global_score.global_convergence,
            "pattern_alignment": global_score.pattern_alignment,
            "convergence_variance": global_score.convergence_variance,
            "global_emergence": global_score.global_emergence
        }
    
    def get_sync_history(self, limit: int = 10) -> List[SynchronizationResult]:
        """Get synchronization history."""
        return self.sync_history[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics."""
        return self.stats.copy()

