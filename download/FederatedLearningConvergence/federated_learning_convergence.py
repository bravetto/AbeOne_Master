"""
Federated Learning Convergence
Ensures learning converges across all customer instances.

Pattern: FEDERATED × LEARNING × CONVERGENCE × EMERGENCE × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (ARXON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import logging
import hashlib
import json

from .federated_convergence_types import (
    InstanceMetadata,
    InstanceStatus,
    PatternSignature,
    PatternQuality,
    AggregatedPattern,
    ConvergenceResult
)

logger = logging.getLogger(__name__)


class FederatedLearningConvergence:
    """
    Federated Learning Convergence System.
    
    Ensures learning converges across all production deployment instances.
    
    Features:
    - Instance registration and health monitoring
    - Pattern quality validation (epistemic certainty > 0.85)
    - Privacy-preserving pattern signature extraction
    - Pattern merging with conflict resolution
    - Convergence score calculation
    - Cross-instance emergence detection
    
    SAFETY: Privacy-preserving aggregation (no raw data, only patterns)
    ASSUMES: Patterns are validated before aggregation
    VERIFY: Pattern quality threshold met before aggregation
    """
    
    def __init__(
        self,
        min_epistemic_certainty: float = 0.85,
        pattern_quality_threshold: float = 0.7,
        heartbeat_timeout: timedelta = timedelta(minutes=5)
    ):
        """
        Initialize federated learning convergence system.
        
        Args:
            min_epistemic_certainty: Minimum epistemic certainty for pattern validation
            pattern_quality_threshold: Minimum quality threshold for aggregation
            heartbeat_timeout: Timeout for instance heartbeat
        """
        # Instance registry
        self.instance_registry: Dict[str, InstanceMetadata] = {}
        
        # Global pattern library (aggregated from all instances)
        self.global_pattern_library: Dict[str, AggregatedPattern] = {}
        
        # Pattern signatures by instance
        self.instance_patterns: Dict[str, List[PatternSignature]] = {}
        
        # Configuration
        self.min_epistemic_certainty = min_epistemic_certainty
        self.pattern_quality_threshold = pattern_quality_threshold
        self.heartbeat_timeout = heartbeat_timeout
        
        # Statistics
        self.stats: Dict[str, Any] = {
            "total_patterns_received": 0,
            "total_patterns_aggregated": 0,
            "total_instances_registered": 0,
            "convergence_calculations": 0
        }
    
    def register_instance(
        self,
        instance_id: str,
        instance_name: str,
        deployment_region: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> InstanceMetadata:
        """
        Register a new production instance.
        
        SAFETY: Validates instance ID uniqueness
        ASSUMES: Instance ID is unique and valid
        VERIFY: Instance successfully registered
        """
        if instance_id in self.instance_registry:
            logger.warning(f"Instance {instance_id} already registered, updating metadata")
            instance = self.instance_registry[instance_id]
            instance.instance_name = instance_name
            instance.deployment_region = deployment_region
            if metadata:
                instance.metadata.update(metadata)
            instance.update_heartbeat()
            return instance
        
        instance = InstanceMetadata(
            instance_id=instance_id,
            instance_name=instance_name,
            deployment_region=deployment_region,
            metadata=metadata or {}
        )
        
        self.instance_registry[instance_id] = instance
        self.instance_patterns[instance_id] = []
        self.stats["total_instances_registered"] += 1
        
        logger.info(f"Registered instance: {instance_id} ({instance_name}) in {deployment_region}")
        
        return instance
    
    def update_instance_heartbeat(self, instance_id: str) -> bool:
        """
        Update instance heartbeat.
        
        Returns:
            True if instance exists and heartbeat updated, False otherwise
        """
        if instance_id not in self.instance_registry:
            logger.warning(f"Instance {instance_id} not found for heartbeat update")
            return False
        
        instance = self.instance_registry[instance_id]
        instance.update_heartbeat()
        instance.status = InstanceStatus.ACTIVE
        
        return True
    
    def check_instance_health(self, instance_id: str) -> bool:
        """
        Check if instance is healthy (heartbeat within timeout).
        
        Returns:
            True if healthy, False otherwise
        """
        if instance_id not in self.instance_registry:
            return False
        
        instance = self.instance_registry[instance_id]
        
        if instance.last_heartbeat is None:
            instance.status = InstanceStatus.UNKNOWN
            return False
        
        time_since_heartbeat = datetime.now() - instance.last_heartbeat
        
        if time_since_heartbeat > self.heartbeat_timeout:
            instance.status = InstanceStatus.INACTIVE
            return False
        
        instance.status = InstanceStatus.ACTIVE
        return True
    
    def _validate_pattern_quality(self, pattern: Dict[str, Any]) -> PatternQuality:
        """
        Validate pattern quality based on epistemic certainty.
        
        SAFETY: Validates epistemic certainty threshold
        ASSUMES: Pattern has epistemic_certainty field
        VERIFY: Pattern quality meets threshold
        """
        epistemic_certainty = pattern.get("epistemic_certainty", 0.0)
        strength = pattern.get("strength", 0.0)
        
        if epistemic_certainty < self.min_epistemic_certainty:
            return PatternQuality.INVALID
        
        if epistemic_certainty >= 0.9 and strength >= 0.7:
            return PatternQuality.HIGH
        
        if epistemic_certainty >= 0.7 and strength >= 0.5:
            return PatternQuality.MEDIUM
        
        if epistemic_certainty >= self.min_epistemic_certainty:
            return PatternQuality.LOW
        
        return PatternQuality.INVALID
    
    def _extract_pattern_signature(
        self,
        pattern: Dict[str, Any],
        instance_id: str
    ) -> Optional[PatternSignature]:
        """
        Extract privacy-preserving pattern signature.
        
        SAFETY: Only extracts signatures, no raw data
        ASSUMES: Pattern is validated before extraction
        VERIFY: Signature successfully extracted
        """
        pattern_id = pattern.get("pattern_id", "unknown")
        pattern_type = pattern.get("pattern_type", "unknown")
        
        # Extract and anonymize module identifiers
        modules = pattern.get("modules", [])
        module_signatures = [
            hashlib.sha256(f"{m}_{instance_id}".encode()).hexdigest()[:16]
            for m in modules
        ]
        
        # Extract and anonymize event types
        event_types = pattern.get("event_types", [])
        event_type_signatures = [
            hashlib.sha256(f"{e}_{instance_id}".encode()).hexdigest()[:16]
            for e in event_types
        ]
        
        # Extract metrics
        strength = pattern.get("strength", 0.0)
        resonance = pattern.get("resonance", 0.0)
        frequency = pattern.get("frequency", 1)
        epistemic_certainty = pattern.get("epistemic_certainty", 0.0)
        
        # Validate quality
        quality = self._validate_pattern_quality(pattern)
        
        if quality == PatternQuality.INVALID:
            logger.warning(f"Pattern {pattern_id} failed quality validation")
            return None
        
        signature = PatternSignature(
            signature_id=f"{pattern_id}_{instance_id}_{datetime.now().timestamp()}",
            pattern_type=pattern_type,
            strength=strength,
            resonance=resonance,
            frequency=frequency,
            module_signatures=module_signatures,
            event_type_signatures=event_type_signatures,
            epistemic_certainty=epistemic_certainty,
            quality=quality,
            instance_id=instance_id
        )
        
        return signature
    
    async def aggregate_learning(
        self,
        instance_id: str,
        local_patterns: List[Dict[str, Any]]
    ) -> ConvergenceResult:
        """
        Aggregate learning from single instance into global knowledge.
        
        SAFETY: Privacy-preserving aggregation (no raw data, only patterns)
        ASSUMES: Patterns are anonymized and validated
        VERIFY: Pattern quality threshold met before aggregation
        
        Args:
            instance_id: Instance identifier
            local_patterns: List of patterns from instance
            
        Returns:
            ConvergenceResult with aggregation metrics
        """
        # Verify instance is registered
        if instance_id not in self.instance_registry:
            raise ValueError(f"Instance {instance_id} not registered")
        
        instance = self.instance_registry[instance_id]
        
        # Validate patterns and extract signatures
        validated_signatures: List[PatternSignature] = []
        
        for pattern in local_patterns:
            signature = self._extract_pattern_signature(pattern, instance_id)
            if signature:
                validated_signatures.append(signature)
                self.stats["total_patterns_received"] += 1
        
        # Store patterns for this instance
        self.instance_patterns[instance_id] = validated_signatures
        
        # Update instance metadata
        instance.pattern_count = len(validated_signatures)
        instance.total_requests += len(local_patterns)
        instance.update_heartbeat()
        
        # Merge patterns with global library
        aggregated_count = await self._merge_patterns(instance_id, validated_signatures)
        
        # Calculate convergence score
        convergence_score = self._calculate_convergence_score()
        
        # Detect cross-instance emergence
        emergence_score = self._detect_cross_instance_emergence()
        
        self.stats["convergence_calculations"] += 1
        
        return ConvergenceResult(
            convergence_score=convergence_score,
            emergence_score=emergence_score,
            patterns_aggregated=aggregated_count,
            instances_contributing=len([i for i in self.instance_registry.values() if i.pattern_count > 0]),
            pattern_alignment=self._calculate_pattern_alignment(),
            global_emergence_factor=emergence_score,
            metadata={
                "instance_id": instance_id,
                "patterns_received": len(local_patterns),
                "patterns_validated": len(validated_signatures)
            }
        )
    
    async def _merge_patterns(
        self,
        instance_id: str,
        signatures: List[PatternSignature]
    ) -> int:
        """
        Merge patterns with global library using consensus.
        
        SAFETY: Conflict resolution using weighted consensus
        ASSUMES: Signatures are validated and anonymized
        VERIFY: Patterns successfully merged
        """
        aggregated_count = 0
        
        for signature in signatures:
            # Create pattern key from signature characteristics
            pattern_key = self._create_pattern_key(signature)
            
            if pattern_key in self.global_pattern_library:
                # Update existing aggregated pattern
                aggregated = self.global_pattern_library[pattern_key]
                
                # Add instance to contributors if not already present
                if instance_id not in aggregated.contributing_instances:
                    aggregated.contributing_instances.append(instance_id)
                    aggregated.instance_count += 1
                
                # Update aggregated metrics (weighted by instance weight)
                instance_weight = self.instance_registry[instance_id].calculate_weight()
                total_weight = sum(
                    self.instance_registry[i].calculate_weight()
                    for i in aggregated.contributing_instances
                )
                
                # Weighted average update
                weight_ratio = instance_weight / (total_weight + instance_weight)
                
                aggregated.total_frequency += signature.frequency
                aggregated.average_strength = (
                    aggregated.average_strength * (1 - weight_ratio) +
                    signature.strength * weight_ratio
                )
                aggregated.average_resonance = (
                    aggregated.average_resonance * (1 - weight_ratio) +
                    signature.resonance * weight_ratio
                )
                aggregated.average_epistemic_certainty = (
                    aggregated.average_epistemic_certainty * (1 - weight_ratio) +
                    signature.epistemic_certainty * weight_ratio
                )
                
                # Update consensus score (agreement between instances)
                aggregated.consensus_score = self._calculate_consensus_score(aggregated)
                
            else:
                # Create new aggregated pattern
                aggregated = AggregatedPattern(
                    pattern_id=pattern_key,
                    pattern_type=signature.pattern_type,
                    aggregated_signature=signature,
                    contributing_instances=[instance_id],
                    instance_count=1,
                    total_frequency=signature.frequency,
                    average_strength=signature.strength,
                    average_resonance=signature.resonance,
                    average_epistemic_certainty=signature.epistemic_certainty,
                    consensus_score=1.0  # Single instance = perfect consensus
                )
                
                self.global_pattern_library[pattern_key] = aggregated
                aggregated_count += 1
                self.stats["total_patterns_aggregated"] += 1
        
        return aggregated_count
    
    def _create_pattern_key(self, signature: PatternSignature) -> str:
        """Create unique pattern key from signature."""
        # Use pattern type and module/event signatures for key
        key_parts = [
            signature.pattern_type,
            ",".join(sorted(signature.module_signatures)),
            ",".join(sorted(signature.event_type_signatures))
        ]
        key_string = "|".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def _calculate_consensus_score(self, aggregated: AggregatedPattern) -> float:
        """
        Calculate consensus score (agreement between instances).
        
        Higher score = more instances agree on pattern characteristics.
        """
        if aggregated.instance_count <= 1:
            return 1.0
        
        # Calculate variance in pattern characteristics
        instances = aggregated.contributing_instances
        strengths = []
        resonances = []
        
        for instance_id in instances:
            instance_patterns = self.instance_patterns.get(instance_id, [])
            for sig in instance_patterns:
                if self._create_pattern_key(sig) == aggregated.pattern_id:
                    strengths.append(sig.strength)
                    resonances.append(sig.resonance)
                    break
        
        if not strengths:
            return 0.5  # Default if no matching signatures found
        
        # Calculate coefficient of variation (lower = more consensus)
        import statistics
        strength_cv = statistics.stdev(strengths) / (statistics.mean(strengths) + 0.001)
        resonance_cv = statistics.stdev(resonances) / (statistics.mean(resonances) + 0.001)
        
        # Consensus score = 1 - normalized variance
        consensus = 1.0 - min(1.0, (strength_cv + resonance_cv) / 2.0)
        
        return max(0.0, min(1.0, consensus))
    
    def _calculate_convergence_score(self) -> float:
        """
        Calculate convergence score based on global patterns.
        
        Convergence = (pattern_coverage × pattern_quality × instance_participation) / 3
        """
        if not self.global_pattern_library:
            return 0.0
        
        # Pattern coverage: how many unique patterns detected
        unique_patterns = len(self.global_pattern_library)
        
        # Pattern quality: average epistemic certainty
        total_quality = sum(
            p.average_epistemic_certainty
            for p in self.global_pattern_library.values()
        )
        avg_quality = total_quality / unique_patterns if unique_patterns > 0 else 0.0
        
        # Instance participation: how many instances contribute
        active_instances = len([
            i for i in self.instance_registry.values()
            if i.pattern_count > 0 and i.status == InstanceStatus.ACTIVE
        ])
        total_instances = len(self.instance_registry)
        participation = active_instances / total_instances if total_instances > 0 else 0.0
        
        # Normalize pattern coverage (assume 100+ patterns = full coverage)
        coverage = min(1.0, unique_patterns / 100.0)
        
        # Convergence score
        convergence = (coverage + avg_quality + participation) / 3.0
        
        return max(0.0, min(1.0, convergence))
    
    def _detect_cross_instance_emergence(self) -> float:
        """
        Detect emergence across instances.
        
        Emergence occurs when:
        1. Multiple instances detect similar patterns
        2. High consensus scores
        3. High pattern strength and resonance
        """
        if not self.global_pattern_library:
            return 0.0
        
        emergence_factors = []
        
        for pattern in self.global_pattern_library.values():
            # Factor 1: Multi-instance detection
            if pattern.instance_count >= 3:
                multi_instance_factor = min(1.0, pattern.instance_count / 10.0)
                emergence_factors.append(multi_instance_factor)
            
            # Factor 2: High consensus
            if pattern.consensus_score > 0.8:
                emergence_factors.append(pattern.consensus_score)
            
            # Factor 3: High strength and resonance
            if pattern.average_strength > 0.7 and pattern.average_resonance > 0.7:
                strength_resonance_factor = (
                    pattern.average_strength * 0.5 +
                    pattern.average_resonance * 0.5
                )
                emergence_factors.append(strength_resonance_factor)
        
        if not emergence_factors:
            return 0.0
        
        # Average emergence factors
        emergence_score = sum(emergence_factors) / len(emergence_factors)
        
        return max(0.0, min(1.0, emergence_score))
    
    def _calculate_pattern_alignment(self) -> float:
        """
        Calculate pattern alignment across instances.
        
        Alignment = similarity of patterns detected across different instances.
        """
        if len(self.instance_registry) < 2:
            return 1.0  # Single instance = perfect alignment
        
        # Calculate pattern overlap between instances
        instance_pattern_sets = {}
        for instance_id, patterns in self.instance_patterns.items():
            pattern_types = set(p.pattern_type for p in patterns)
            instance_pattern_sets[instance_id] = pattern_types
        
        if not instance_pattern_sets:
            return 0.0
        
        # Calculate pairwise Jaccard similarity
        similarities = []
        instance_ids = list(instance_pattern_sets.keys())
        
        for i in range(len(instance_ids)):
            for j in range(i + 1, len(instance_ids)):
                set1 = instance_pattern_sets[instance_ids[i]]
                set2 = instance_pattern_sets[instance_ids[j]]
                
                if not set1 and not set2:
                    similarity = 1.0
                elif not set1 or not set2:
                    similarity = 0.0
                else:
                    intersection = len(set1 & set2)
                    union = len(set1 | set2)
                    similarity = intersection / union if union > 0 else 0.0
                
                similarities.append(similarity)
        
        if not similarities:
            return 0.0
        
        # Average alignment
        alignment = sum(similarities) / len(similarities)
        
        return max(0.0, min(1.0, alignment))
    
    def get_global_pattern_library(self) -> Dict[str, AggregatedPattern]:
        """Get global pattern library."""
        return self.global_pattern_library.copy()
    
    def get_instance_registry(self) -> Dict[str, InstanceMetadata]:
        """Get instance registry."""
        return self.instance_registry.copy()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics."""
        return self.stats.copy()

