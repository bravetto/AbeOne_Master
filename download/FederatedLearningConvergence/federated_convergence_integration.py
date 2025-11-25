"""
Federated Convergence Integration
Integration layer for federated learning convergence with orchestrators.

Pattern: INTEGRATION × FEDERATED × CONVERGENCE × ORCHESTRATION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (ARXON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import asyncio

from .federated_learning_convergence import FederatedLearningConvergence
from .global_scoring_aggregator import GlobalScoringAggregator
from .learning_synchronization_protocol import LearningSynchronizationProtocol
from .federated_convergence_types import (
    InstanceScores,
    GlobalConvergenceScore,
    ConvergenceResult
)

logger = logging.getLogger(__name__)

# Import orchestrators with graceful error handling
try:
    from .unified_orchestrator import UnifiedOrchestrator, get_unified_orchestrator
    UNIFIED_ORCHESTRATOR_AVAILABLE = True
except ImportError:
    logger.debug("UnifiedOrchestrator not available")
    UNIFIED_ORCHESTRATOR_AVAILABLE = False
    UnifiedOrchestrator = None
    def get_unified_orchestrator():
        raise RuntimeError("UnifiedOrchestrator not available")

try:
    from .complete_convergence_orchestrator import (
        CompleteConvergenceOrchestrator,
        get_complete_convergence_orchestrator
    )
    COMPLETE_CONVERGENCE_ORCHESTRATOR_AVAILABLE = True
except ImportError:
    logger.debug("CompleteConvergenceOrchestrator not available")
    COMPLETE_CONVERGENCE_ORCHESTRATOR_AVAILABLE = False
    CompleteConvergenceOrchestrator = None
    def get_complete_convergence_orchestrator():
        raise RuntimeError("CompleteConvergenceOrchestrator not available")

try:
    from .eeaao_lfglfglfgl_integrated_orchestrator import (
        EEAaOLFGLFGLFGLIntegratedOrchestrator,
        get_integrated_orchestrator,
        ConvergenceMetrics
    )
    EEAaO_ORCHESTRATOR_AVAILABLE = True
except ImportError:
    logger.debug("EEAaOLFGLFGLFGLIntegratedOrchestrator not available")
    EEAaO_ORCHESTRATOR_AVAILABLE = False
    EEAaOLFGLFGLFGLIntegratedOrchestrator = None
    ConvergenceMetrics = None
    def get_integrated_orchestrator():
        raise RuntimeError("EEAaOLFGLFGLFGLIntegratedOrchestrator not available")


class FederatedConvergenceIntegration:
    """
    Federated Convergence Integration.
    
    Integrates federated learning convergence with existing orchestrators.
    
    Features:
    - Integration with UnifiedOrchestrator
    - Integration with CompleteConvergenceOrchestrator
    - Integration with EEAaOLFGLFGLFGLIntegratedOrchestrator
    - Singleton pattern for global coordinator
    - Automatic synchronization
    - Cross-instance convergence tracking
    """
    
    def __init__(
        self,
        sync_window: timedelta = timedelta(hours=1),
        auto_sync: bool = True
    ):
        """
        Initialize federated convergence integration.
        
        Args:
            sync_window: Synchronization window
            auto_sync: Enable automatic synchronization
        """
        # Core federated learning components
        self.federated_learning = FederatedLearningConvergence()
        self.global_scoring = GlobalScoringAggregator()
        self.sync_protocol = LearningSynchronizationProtocol(
            self.federated_learning,
            self.global_scoring,
            sync_window=sync_window
        )
        
        # Orchestrator references
        self.unified_orchestrator: Optional[UnifiedOrchestrator] = None
        self.complete_convergence_orchestrator: Optional[CompleteConvergenceOrchestrator] = None
        self.eeaao_orchestrator: Optional[EEAaOLFGLFGLFGLIntegratedOrchestrator] = None
        
        # Initialize orchestrator connections
        self._initialize_orchestrators()
        
        # Auto-sync task
        self.auto_sync = auto_sync
        self._sync_task: Optional[asyncio.Task] = None
        
        # Statistics
        self.stats: Dict[str, Any] = {
            "orchestrator_integrations": 0,
            "convergence_updates": 0,
            "sync_triggers": 0
        }
    
    def _initialize_orchestrators(self) -> None:
        """Initialize orchestrator connections."""
        if UNIFIED_ORCHESTRATOR_AVAILABLE:
            try:
                self.unified_orchestrator = get_unified_orchestrator()
                self.stats["orchestrator_integrations"] += 1
                logger.info("Connected to UnifiedOrchestrator")
            except Exception as e:
                logger.warning(f"Failed to connect to UnifiedOrchestrator: {e}")
        
        if COMPLETE_CONVERGENCE_ORCHESTRATOR_AVAILABLE:
            try:
                self.complete_convergence_orchestrator = get_complete_convergence_orchestrator()
                self.stats["orchestrator_integrations"] += 1
                logger.info("Connected to CompleteConvergenceOrchestrator")
            except Exception as e:
                logger.warning(f"Failed to connect to CompleteConvergenceOrchestrator: {e}")
        
        if EEAaO_ORCHESTRATOR_AVAILABLE:
            try:
                self.eeaao_orchestrator = get_integrated_orchestrator()
                self.stats["orchestrator_integrations"] += 1
                logger.info("Connected to EEAaOLFGLFGLFGLIntegratedOrchestrator")
            except Exception as e:
                logger.warning(f"Failed to connect to EEAaOLFGLFGLFGLIntegratedOrchestrator: {e}")
    
    async def register_instance(
        self,
        instance_id: str,
        instance_name: str,
        deployment_region: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a production instance.
        
        Args:
            instance_id: Instance identifier
            instance_name: Instance name
            deployment_region: Deployment region
            metadata: Optional metadata
        """
        self.federated_learning.register_instance(
            instance_id,
            instance_name,
            deployment_region,
            metadata
        )
        logger.info(f"Registered instance: {instance_id}")
    
    async def update_instance_convergence(
        self,
        instance_id: str,
        local_patterns: List[Dict[str, Any]]
    ) -> ConvergenceResult:
        """
        Update convergence from an instance.
        
        Args:
            instance_id: Instance identifier
            local_patterns: Local patterns from instance
            
        Returns:
            ConvergenceResult with convergence metrics
        """
        # Aggregate learning
        convergence_result = await self.federated_learning.aggregate_learning(
            instance_id,
            local_patterns
        )
        
        # Update orchestrators if available
        await self._update_orchestrators(instance_id, convergence_result)
        
        self.stats["convergence_updates"] += 1
        
        return convergence_result
    
    async def _update_orchestrators(
        self,
        instance_id: str,
        convergence_result: ConvergenceResult
    ) -> None:
        """Update orchestrators with convergence results."""
        # Update UnifiedOrchestrator if available
        if self.unified_orchestrator:
            try:
                # Unified orchestrator doesn't have direct instance update method
                # So we just track the convergence result
                logger.debug(f"Convergence result for {instance_id}: {convergence_result.convergence_score:.2%}")
            except Exception as e:
                logger.warning(f"Failed to update UnifiedOrchestrator: {e}")
        
        # Update CompleteConvergenceOrchestrator if available
        if self.complete_convergence_orchestrator:
            try:
                # Complete convergence orchestrator tracks convergence state
                # We can update it with federated convergence score
                current_state = self.complete_convergence_orchestrator.convergence_state
                current_state["federated_convergence"] = convergence_result.convergence_score
                current_state["federated_emergence"] = convergence_result.emergence_score
                current_state["last_federated_update"] = datetime.now().isoformat()
                logger.debug(f"Updated CompleteConvergenceOrchestrator with federated convergence")
            except Exception as e:
                logger.warning(f"Failed to update CompleteConvergenceOrchestrator: {e}")
        
        # Update EEAaO orchestrator if available
        if self.eeaao_orchestrator:
            try:
                # EEAaO orchestrator tracks convergence metrics
                # We can add federated convergence to metrics
                logger.debug(f"Federated convergence available for EEAaO orchestrator")
            except Exception as e:
                logger.warning(f"Failed to update EEAaO orchestrator: {e}")
    
    async def synchronize_all_instances(
        self,
        sync_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """
        Synchronize learning across all instances.
        
        Args:
            sync_window: Optional override for sync window
            
        Returns:
            Synchronization result
        """
        self.stats["sync_triggers"] += 1
        
        result = await self.sync_protocol.synchronize_learning(sync_window)
        
        # Update orchestrators with global convergence
        if result.convergence_achieved:
            await self._update_orchestrators_with_global_convergence(result)
        
        return result.to_dict()
    
    async def _update_orchestrators_with_global_convergence(
        self,
        sync_result: Any
    ) -> None:
        """Update orchestrators with global convergence results."""
        # Get global convergence score
        global_patterns = list(self.federated_learning.get_global_pattern_library().values())
        instance_scores: Dict[str, InstanceScores] = {}
        instance_metadata: Dict[str, Any] = {}
        
        for instance_id, instance in self.federated_learning.instance_registry.items():
            if instance.pattern_count > 0:
                convergence_score = self.federated_learning._calculate_convergence_score()
                emergence_score = self.federated_learning._detect_cross_instance_emergence()
                
                instance_scores[instance_id] = InstanceScores(
                    instance_id=instance_id,
                    convergence_score=convergence_score,
                    emergence_score=emergence_score,
                    resonance_score=0.8,
                    unified_score=(convergence_score + emergence_score) / 2.0,
                    pattern_count=instance.pattern_count
                )
                instance_metadata[instance_id] = instance
        
        if instance_scores:
            global_score = await self.global_scoring.calculate_global_convergence(
                instance_scores,
                instance_metadata,
                global_patterns
            )
            
            # Update orchestrators
            if self.complete_convergence_orchestrator:
                try:
                    state = self.complete_convergence_orchestrator.convergence_state
                    state["global_convergence"] = global_score.global_convergence
                    state["global_pattern_alignment"] = global_score.pattern_alignment
                    state["global_emergence"] = global_score.global_emergence
                    logger.info(f"Updated orchestrators with global convergence: {global_score.global_convergence:.2%}")
                except Exception as e:
                    logger.warning(f"Failed to update orchestrators: {e}")
    
    async def get_global_convergence_score(self) -> Optional[GlobalConvergenceScore]:
        """
        Get current global convergence score.
        
        Returns:
            GlobalConvergenceScore if available, None otherwise
        """
        instance_scores: Dict[str, InstanceScores] = {}
        instance_metadata: Dict[str, Any] = {}
        
        for instance_id, instance in self.federated_learning.instance_registry.items():
            if instance.pattern_count > 0:
                convergence_score = self.federated_learning._calculate_convergence_score()
                emergence_score = self.federated_learning._detect_cross_instance_emergence()
                
                instance_scores[instance_id] = InstanceScores(
                    instance_id=instance_id,
                    convergence_score=convergence_score,
                    emergence_score=emergence_score,
                    resonance_score=0.8,
                    unified_score=(convergence_score + emergence_score) / 2.0,
                    pattern_count=instance.pattern_count
                )
                instance_metadata[instance_id] = instance
        
        if not instance_scores:
            return None
        
        global_patterns = list(self.federated_learning.get_global_pattern_library().values())
        
        return await self.global_scoring.calculate_global_convergence(
            instance_scores,
            instance_metadata,
            global_patterns
        )
    
    def start_auto_sync(self) -> None:
        """Start automatic synchronization."""
        if self.auto_sync and self._sync_task is None:
            self._sync_task = asyncio.create_task(self._auto_sync_loop())
            logger.info("Started automatic synchronization")
    
    def stop_auto_sync(self) -> None:
        """Stop automatic synchronization."""
        if self._sync_task:
            self._sync_task.cancel()
            self._sync_task = None
            logger.info("Stopped automatic synchronization")
    
    async def _auto_sync_loop(self) -> None:
        """Automatic synchronization loop."""
        while True:
            try:
                await asyncio.sleep(self.sync_protocol.sync_window.total_seconds())
                await self.synchronize_all_instances()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Auto-sync error: {e}", exc_info=True)
                await asyncio.sleep(60)  # Wait before retry
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics."""
        stats = self.stats.copy()
        stats.update({
            "federated_learning_stats": self.federated_learning.get_stats(),
            "global_scoring_stats": self.global_scoring.get_stats(),
            "sync_protocol_stats": self.sync_protocol.get_stats()
        })
        return stats


# Global singleton
_federated_convergence_integration: Optional[FederatedConvergenceIntegration] = None


def get_federated_convergence_integration() -> FederatedConvergenceIntegration:
    """Get FederatedConvergenceIntegration singleton instance."""
    global _federated_convergence_integration
    
    if _federated_convergence_integration is None:
        _federated_convergence_integration = FederatedConvergenceIntegration()
    
    return _federated_convergence_integration

