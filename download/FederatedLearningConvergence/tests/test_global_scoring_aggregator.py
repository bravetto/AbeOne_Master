"""
Unit tests for GlobalScoringAggregator.
"""

import pytest
import asyncio

from EMERGENT_OS.synthesis.global_scoring_aggregator import GlobalScoringAggregator
from EMERGENT_OS.synthesis.federated_convergence_types import (
    InstanceScores,
    InstanceMetadata,
    AggregatedPattern,
    PatternSignature,
    PatternQuality
)
from tests.synthesis.conftest import (
    create_test_instance,
    create_test_instance_scores
)


class TestGlobalScoringAggregator:
    """Test suite for GlobalScoringAggregator."""
    
    def test_initialization(self):
        """Test initialization."""
        gsa = GlobalScoringAggregator()
        assert gsa.min_instance_weight == 0.1
        assert gsa.max_variance_threshold == 0.1
    
    def test_calculate_instance_weight(self):
        """Test instance weight calculation."""
        gsa = GlobalScoringAggregator()
        
        instance = create_test_instance("test-1", reliability=0.95, data_quality=0.90, pattern_count=100)
        scores = create_test_instance_scores("test-1")
        
        weight = gsa._calculate_instance_weight("test-1", instance, scores)
        
        assert weight >= gsa.min_instance_weight
        assert weight <= 1.0
    
    def test_calculate_instance_weight_minimum(self):
        """Test instance weight respects minimum."""
        gsa = GlobalScoringAggregator(min_instance_weight=0.2)
        
        instance = create_test_instance("test-1", reliability=0.1, data_quality=0.1, pattern_count=1)
        scores = create_test_instance_scores("test-1")
        
        weight = gsa._calculate_instance_weight("test-1", instance, scores)
        
        assert weight >= 0.2  # Minimum weight
    
    @pytest.mark.asyncio
    async def test_calculate_global_convergence_empty(self):
        """Test global convergence calculation with no instances."""
        gsa = GlobalScoringAggregator()
        
        result = await gsa.calculate_global_convergence({}, {})
        
        assert result.global_convergence == 0.0
        assert result.instance_count == 0
    
    @pytest.mark.asyncio
    async def test_calculate_global_convergence_single_instance(self):
        """Test global convergence calculation with single instance."""
        gsa = GlobalScoringAggregator()
        
        instance = create_test_instance("test-1")
        scores = create_test_instance_scores("test-1", convergence_score=0.85, emergence_score=0.80)
        
        result = await gsa.calculate_global_convergence(
            {"test-1": scores},
            {"test-1": instance}
        )
        
        assert result.instance_count == 1
        assert 0.0 <= result.global_convergence <= 1.0
        assert result.mean_convergence > 0.0
    
    @pytest.mark.asyncio
    async def test_calculate_global_convergence_multiple_instances(self):
        """Test global convergence calculation with multiple instances."""
        gsa = GlobalScoringAggregator()
        
        instance_scores = {}
        instance_metadata = {}
        
        for i in range(3):
            instance_id = f"test-{i}"
            instance_scores[instance_id] = create_test_instance_scores(
                instance_id,
                convergence_score=0.80 + (i * 0.05),
                emergence_score=0.75 + (i * 0.05)
            )
            instance_metadata[instance_id] = create_test_instance(
                instance_id,
                reliability=0.90 + (i * 0.02),
                data_quality=0.85 + (i * 0.02)
            )
        
        result = await gsa.calculate_global_convergence(
            instance_scores,
            instance_metadata
        )
        
        assert result.instance_count == 3
        assert 0.0 <= result.global_convergence <= 1.0
        assert result.mean_convergence > 0.0
        assert result.weighted_mean_convergence > 0.0
    
    @pytest.mark.asyncio
    async def test_calculate_global_convergence_with_patterns(self):
        """Test global convergence calculation with patterns."""
        gsa = GlobalScoringAggregator()
        
        instance = create_test_instance("test-1")
        scores = create_test_instance_scores("test-1")
        
        # Create sample patterns
        patterns = [
            AggregatedPattern(
                pattern_id="pattern-1",
                pattern_type="positive",
                aggregated_signature=PatternSignature(
                    signature_id="sig-1",
                    pattern_type="positive",
                    strength=0.85,
                    resonance=0.80,
                    frequency=10,
                    module_signatures=["mod1"],
                    event_type_signatures=["evt1"],
                    epistemic_certainty=0.90,
                    quality=PatternQuality.HIGH,
                    instance_id="test-1"
                ),
                contributing_instances=["test-1"],
                instance_count=1,
                total_frequency=10,
                average_strength=0.85,
                average_resonance=0.80,
                average_epistemic_certainty=0.90,
                consensus_score=1.0
            )
        ]
        
        result = await gsa.calculate_global_convergence(
            {"test-1": scores},
            {"test-1": instance},
            patterns
        )
        
        assert result.instance_count == 1
        assert 0.0 <= result.global_convergence <= 1.0
        assert 0.0 <= result.pattern_alignment <= 1.0
        assert 0.0 <= result.global_emergence <= 1.0
    
    def test_calculate_pattern_alignment_empty(self):
        """Test pattern alignment calculation with no patterns."""
        gsa = GlobalScoringAggregator()
        
        alignment = gsa._calculate_pattern_alignment({}, None)
        assert alignment == 0.0
    
    def test_calculate_pattern_alignment_single_instance(self):
        """Test pattern alignment with single instance."""
        gsa = GlobalScoringAggregator()
        
        instance_scores = {"test-1": create_test_instance_scores("test-1")}
        
        alignment = gsa._calculate_pattern_alignment(instance_scores, None)
        assert alignment == 0.0  # No patterns
    
    def test_detect_global_emergence_empty(self):
        """Test global emergence detection with no patterns."""
        gsa = GlobalScoringAggregator()
        
        emergence = gsa._detect_global_emergence({}, None)
        assert emergence == 0.0
    
    def test_detect_global_emergence_with_patterns(self):
        """Test global emergence detection with patterns."""
        gsa = GlobalScoringAggregator()
        
        instance_scores = {"test-1": create_test_instance_scores("test-1")}
        
        patterns = [
            AggregatedPattern(
                pattern_id="pattern-1",
                pattern_type="positive",
                aggregated_signature=PatternSignature(
                    signature_id="sig-1",
                    pattern_type="positive",
                    strength=0.85,
                    resonance=0.80,
                    frequency=10,
                    module_signatures=["mod1"],
                    event_type_signatures=["evt1"],
                    epistemic_certainty=0.95,
                    quality=PatternQuality.HIGH,
                    instance_id="test-1"
                ),
                contributing_instances=["test-1", "test-2"],
                instance_count=2,
                total_frequency=20,
                average_strength=0.85,
                average_resonance=0.80,
                average_epistemic_certainty=0.95,
                consensus_score=0.90
            )
        ]
        
        emergence = gsa._detect_global_emergence(instance_scores, patterns)
        assert 0.0 <= emergence <= 1.0
    
    def test_validate_convergence_achieved(self):
        """Test convergence validation - achieved."""
        gsa = GlobalScoringAggregator()
        
        from EMERGENT_OS.synthesis.federated_convergence_types import GlobalConvergenceScore
        
        global_score = GlobalConvergenceScore(
            global_convergence=0.96,
            instance_count=5,
            pattern_alignment=0.92,
            global_emergence=0.88,
            convergence_variance=0.03,
            mean_convergence=0.95,
            weighted_mean_convergence=0.96
        )
        
        result = gsa.validate_convergence(global_score)
        assert result is True
    
    def test_validate_convergence_not_achieved(self):
        """Test convergence validation - not achieved."""
        gsa = GlobalScoringAggregator()
        
        from EMERGENT_OS.synthesis.federated_convergence_types import GlobalConvergenceScore
        
        global_score = GlobalConvergenceScore(
            global_convergence=0.80,
            instance_count=2,
            pattern_alignment=0.70,
            global_emergence=0.60,
            convergence_variance=0.15,
            mean_convergence=0.75,
            weighted_mean_convergence=0.80
        )
        
        result = gsa.validate_convergence(global_score)
        assert result is False
    
    def test_get_stats(self):
        """Test getting statistics."""
        gsa = GlobalScoringAggregator()
        
        stats = gsa.get_stats()
        assert isinstance(stats, dict)
        assert "total_aggregations" in stats
        assert "instances_aggregated" in stats

