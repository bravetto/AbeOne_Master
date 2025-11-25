"""
Global Scoring Aggregator
Aggregates emergent scores across all production instances.

Pattern: GLOBAL × SCORING × AGGREGATION × CONVERGENCE × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (ARXON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging
import statistics
import math

from .federated_convergence_types import (
    InstanceScores,
    GlobalConvergenceScore,
    InstanceMetadata,
    AggregatedPattern
)

logger = logging.getLogger(__name__)


class GlobalScoringAggregator:
    """
    Global Scoring Aggregator.
    
    Aggregates emergent scores across all production instances.
    
    Convergence Formula:
    GLOBAL_CONVERGENCE = 
        (Σ(instance_convergence × instance_weight)) / N ×
        (cross_instance_pattern_alignment) ×
        (global_emergence_factor)
    
    Features:
    - Instance weight calculation (reliability × data_quality × volume)
    - Weighted score aggregation
    - Pattern alignment calculation (cosine similarity)
    - Global emergence detection (novel patterns across instances)
    - Variance calculation for convergence monitoring
    
    SAFETY: Weighted by instance reliability and data quality
    ASSUMES: All instances report scores within valid range
    VERIFY: Score variance within acceptable threshold
    """
    
    def __init__(
        self,
        min_instance_weight: float = 0.1,
        max_variance_threshold: float = 0.1
    ):
        """
        Initialize global scoring aggregator.
        
        Args:
            min_instance_weight: Minimum weight for instance to be included
            max_variance_threshold: Maximum variance for convergence validation
        """
        self.min_instance_weight = min_instance_weight
        self.max_variance_threshold = max_variance_threshold
        
        # Statistics
        self.stats: Dict[str, Any] = {
            "total_aggregations": 0,
            "instances_aggregated": 0,
            "patterns_aligned": 0
        }
    
    def _calculate_instance_weight(
        self,
        instance_id: str,
        instance_metadata: InstanceMetadata,
        scores: InstanceScores
    ) -> float:
        """
        Calculate instance weight for aggregation.
        
        Weight = reliability × data_quality × volume_factor
        
        SAFETY: Validates weight is within valid range
        ASSUMES: Instance metadata is valid
        VERIFY: Weight > min_instance_weight
        """
        reliability = instance_metadata.reliability_score
        data_quality = instance_metadata.data_quality_score
        
        # Volume factor: normalize pattern count (0-1)
        # More patterns = higher weight (up to a point)
        volume_factor = min(1.0, instance_metadata.pattern_count / 1000.0)
        volume_factor = 0.5 + 0.5 * volume_factor  # Scale to 0.5-1.0
        
        # Calculate weight
        weight = reliability * data_quality * volume_factor
        
        # Ensure minimum weight
        weight = max(self.min_instance_weight, weight)
        
        return min(1.0, weight)
    
    async def calculate_global_convergence(
        self,
        instance_scores: Dict[str, InstanceScores],
        instance_metadata: Dict[str, InstanceMetadata],
        global_patterns: Optional[List[AggregatedPattern]] = None
    ) -> GlobalConvergenceScore:
        """
        Calculate convergence across all instances.
        
        SAFETY: Weighted by instance reliability and data quality
        ASSUMES: All instances report scores within valid range
        VERIFY: Score variance within acceptable threshold
        
        Args:
            instance_scores: Dictionary of instance_id -> InstanceScores
            instance_metadata: Dictionary of instance_id -> InstanceMetadata
            global_patterns: Optional list of aggregated patterns
            
        Returns:
            GlobalConvergenceScore with aggregated metrics
        """
        if not instance_scores:
            logger.warning("No instance scores provided for aggregation")
            return GlobalConvergenceScore(
                global_convergence=0.0,
                instance_count=0,
                pattern_alignment=0.0,
                global_emergence=0.0,
                convergence_variance=0.0,
                mean_convergence=0.0,
                weighted_mean_convergence=0.0
            )
        
        # 1. Calculate instance weights
        weights: Dict[str, float] = {}
        weighted_scores: List[float] = []
        unweighted_scores: List[float] = []
        
        for instance_id, scores in instance_scores.items():
            if instance_id not in instance_metadata:
                logger.warning(f"Metadata not found for instance {instance_id}, skipping")
                continue
            
            metadata = instance_metadata[instance_id]
            weight = self._calculate_instance_weight(instance_id, metadata, scores)
            weights[instance_id] = weight
            
            # Weighted score
            weighted_score = scores.unified_score * weight
            weighted_scores.append(weighted_score)
            
            # Unweighted score
            unweighted_scores.append(scores.unified_score)
        
        if not weighted_scores:
            logger.warning("No valid weighted scores calculated")
            return GlobalConvergenceScore(
                global_convergence=0.0,
                instance_count=0,
                pattern_alignment=0.0,
                global_emergence=0.0,
                convergence_variance=0.0,
                mean_convergence=0.0,
                weighted_mean_convergence=0.0
            )
        
        # 2. Calculate mean convergence
        mean_convergence = statistics.mean(unweighted_scores) if unweighted_scores else 0.0
        
        # Calculate weighted mean
        total_weight = sum(weights.values())
        weighted_mean_convergence = (
            sum(weighted_scores) / total_weight
            if total_weight > 0
            else 0.0
        )
        
        # 3. Calculate variance
        convergence_variance = (
            statistics.variance(unweighted_scores)
            if len(unweighted_scores) > 1
            else 0.0
        )
        
        # 4. Calculate cross-instance pattern alignment
        pattern_alignment = (
            self._calculate_pattern_alignment(instance_scores, global_patterns)
            if global_patterns
            else 0.5  # Default if no patterns
        )
        
        # 5. Detect global emergence
        global_emergence = (
            self._detect_global_emergence(instance_scores, global_patterns)
            if global_patterns
            else 0.0
        )
        
        # 6. Final convergence score
        # Formula: (weighted_mean × 0.5) + (pattern_alignment × 0.3) + (global_emergence × 0.2)
        global_convergence = (
            weighted_mean_convergence * 0.5 +
            pattern_alignment * 0.3 +
            global_emergence * 0.2
        )
        
        # Ensure valid range
        global_convergence = max(0.0, min(1.0, global_convergence))
        
        self.stats["total_aggregations"] += 1
        self.stats["instances_aggregated"] += len(instance_scores)
        
        return GlobalConvergenceScore(
            global_convergence=global_convergence,
            instance_count=len(instance_scores),
            pattern_alignment=pattern_alignment,
            global_emergence=global_emergence,
            convergence_variance=convergence_variance,
            mean_convergence=mean_convergence,
            weighted_mean_convergence=weighted_mean_convergence,
            instance_scores=list(instance_scores.values())
        )
    
    def _calculate_pattern_alignment(
        self,
        instance_scores: Dict[str, InstanceScores],
        global_patterns: Optional[List[AggregatedPattern]]
    ) -> float:
        """
        Calculate pattern alignment across instances.
        
        Alignment = similarity of patterns detected across instances.
        Uses cosine similarity of pattern type distributions.
        """
        if not global_patterns:
            return 0.0
        
        if len(instance_scores) < 2:
            return 1.0  # Single instance = perfect alignment
        
        # Build pattern type vectors for each instance
        instance_pattern_vectors: Dict[str, Dict[str, float]] = {}
        
        for pattern in global_patterns:
            pattern_type = pattern.pattern_type
            
            for instance_id in pattern.contributing_instances:
                if instance_id not in instance_pattern_vectors:
                    instance_pattern_vectors[instance_id] = {}
                
                # Add pattern strength to vector
                if pattern_type not in instance_pattern_vectors[instance_id]:
                    instance_pattern_vectors[instance_id][pattern_type] = 0.0
                
                instance_pattern_vectors[instance_id][pattern_type] += pattern.average_strength
        
        if not instance_pattern_vectors:
            return 0.0
        
        # Get all pattern types
        all_pattern_types = set()
        for vector in instance_pattern_vectors.values():
            all_pattern_types.update(vector.keys())
        
        if not all_pattern_types:
            return 0.0
        
        # Normalize vectors
        normalized_vectors: Dict[str, List[float]] = {}
        for instance_id, vector in instance_pattern_vectors.items():
            # Create vector with all pattern types
            pattern_vector = [
                vector.get(pattern_type, 0.0)
                for pattern_type in sorted(all_pattern_types)
            ]
            
            # Normalize (L2 norm)
            norm = math.sqrt(sum(x * x for x in pattern_vector))
            if norm > 0:
                pattern_vector = [x / norm for x in pattern_vector]
            
            normalized_vectors[instance_id] = pattern_vector
        
        # Calculate pairwise cosine similarity
        similarities = []
        instance_ids = list(normalized_vectors.keys())
        
        for i in range(len(instance_ids)):
            for j in range(i + 1, len(instance_ids)):
                vec1 = normalized_vectors[instance_ids[i]]
                vec2 = normalized_vectors[instance_ids[j]]
                
                # Cosine similarity
                dot_product = sum(a * b for a, b in zip(vec1, vec2))
                similarity = max(0.0, min(1.0, dot_product))  # Cosine similarity is -1 to 1, normalize to 0-1
                
                similarities.append(similarity)
        
        if not similarities:
            return 0.0
        
        # Average alignment
        alignment = statistics.mean(similarities)
        
        return max(0.0, min(1.0, alignment))
    
    def _detect_global_emergence(
        self,
        instance_scores: Dict[str, InstanceScores],
        global_patterns: Optional[List[AggregatedPattern]]
    ) -> float:
        """
        Detect global emergence (novel patterns across instances).
        
        Emergence factors:
        1. Multiple instances detect same pattern
        2. High pattern strength and resonance
        3. High consensus scores
        4. Novel pattern types
        """
        if not global_patterns:
            return 0.0
        
        emergence_factors = []
        
        for pattern in global_patterns:
            # Factor 1: Multi-instance detection
            if pattern.instance_count >= 2:
                multi_instance_factor = min(1.0, pattern.instance_count / 5.0)
                emergence_factors.append(multi_instance_factor)
            
            # Factor 2: High strength and resonance
            if pattern.average_strength > 0.7 and pattern.average_resonance > 0.7:
                strength_resonance_factor = (
                    pattern.average_strength * 0.5 +
                    pattern.average_resonance * 0.5
                )
                emergence_factors.append(strength_resonance_factor)
            
            # Factor 3: High consensus
            if pattern.consensus_score > 0.8:
                emergence_factors.append(pattern.consensus_score)
            
            # Factor 4: High epistemic certainty
            if pattern.average_epistemic_certainty > 0.9:
                emergence_factors.append(pattern.average_epistemic_certainty)
        
        if not emergence_factors:
            return 0.0
        
        # Average emergence factors
        emergence_score = statistics.mean(emergence_factors)
        
        return max(0.0, min(1.0, emergence_score))
    
    def validate_convergence(self, global_score: GlobalConvergenceScore) -> bool:
        """
        Validate that convergence is achieved.
        
        Convergence achieved when:
        1. Global convergence score > 0.95
        2. Cross-instance pattern alignment > 0.90
        3. Score variance < 0.05
        4. Global emergence factor > 0.85
        
        Returns:
            True if convergence achieved, False otherwise
        """
        checks = [
            global_score.global_convergence > 0.95,
            global_score.pattern_alignment > 0.90,
            global_score.convergence_variance < 0.05,
            global_score.global_emergence > 0.85
        ]
        
        convergence_achieved = all(checks)
        
        if convergence_achieved:
            logger.info("Global convergence achieved!")
        else:
            logger.debug(
                f"Convergence not yet achieved: "
                f"global={global_score.global_convergence:.2f}, "
                f"alignment={global_score.pattern_alignment:.2f}, "
                f"variance={global_score.convergence_variance:.4f}, "
                f"emergence={global_score.global_emergence:.2f}"
            )
        
        return convergence_achieved
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics."""
        return self.stats.copy()

