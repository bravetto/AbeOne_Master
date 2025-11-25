"""
Unit tests for FederatedLearningConvergence.
"""

import pytest
import asyncio
from datetime import datetime, timedelta

from EMERGENT_OS.synthesis.federated_learning_convergence import FederatedLearningConvergence
from EMERGENT_OS.synthesis.federated_convergence_types import InstanceStatus, PatternQuality
from tests.synthesis.conftest import (
    create_test_instance,
    create_test_pattern,
    sample_pattern,
    sample_patterns
)


class TestFederatedLearningConvergence:
    """Test suite for FederatedLearningConvergence."""
    
    def test_initialization(self):
        """Test initialization."""
        flc = FederatedLearningConvergence()
        assert flc.min_epistemic_certainty == 0.85
        assert flc.pattern_quality_threshold == 0.7
        assert len(flc.instance_registry) == 0
        assert len(flc.global_pattern_library) == 0
    
    def test_register_instance(self):
        """Test instance registration."""
        flc = FederatedLearningConvergence()
        
        instance = flc.register_instance(
            "test-instance-1",
            "Test Instance 1",
            "us-east-1"
        )
        
        assert instance.instance_id == "test-instance-1"
        assert instance.instance_name == "Test Instance 1"
        assert instance.deployment_region == "us-east-1"
        assert instance.status == InstanceStatus.ACTIVE
        assert "test-instance-1" in flc.instance_registry
    
    def test_register_duplicate_instance(self):
        """Test registering duplicate instance updates metadata."""
        flc = FederatedLearningConvergence()
        
        instance1 = flc.register_instance("test-instance-1", "Test 1", "us-east-1")
        instance2 = flc.register_instance("test-instance-1", "Test 1 Updated", "us-west-2")
        
        assert instance1.instance_id == instance2.instance_id
        assert instance2.instance_name == "Test 1 Updated"
        assert instance2.deployment_region == "us-west-2"
    
    def test_update_instance_heartbeat(self):
        """Test heartbeat update."""
        flc = FederatedLearningConvergence()
        flc.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        result = flc.update_instance_heartbeat("test-instance-1")
        assert result is True
        
        instance = flc.instance_registry["test-instance-1"]
        assert instance.last_heartbeat is not None
        assert instance.status == InstanceStatus.ACTIVE
    
    def test_update_nonexistent_instance_heartbeat(self):
        """Test heartbeat update for nonexistent instance."""
        flc = FederatedLearningConvergence()
        
        result = flc.update_instance_heartbeat("nonexistent")
        assert result is False
    
    def test_check_instance_health(self):
        """Test instance health check."""
        flc = FederatedLearningConvergence()
        flc.register_instance("test-instance-1", "Test 1", "us-east-1")
        flc.update_instance_heartbeat("test-instance-1")
        
        health = flc.check_instance_health("test-instance-1")
        assert health is True
    
    def test_check_instance_health_timeout(self):
        """Test instance health check with timeout."""
        flc = FederatedLearningConvergence(
            heartbeat_timeout=timedelta(seconds=1)
        )
        flc.register_instance("test-instance-1", "Test 1", "us-east-1")
        flc.update_instance_heartbeat("test-instance-1")
        
        # Wait for timeout
        import time
        time.sleep(1.1)
        
        health = flc.check_instance_health("test-instance-1")
        assert health is False
        assert flc.instance_registry["test-instance-1"].status == InstanceStatus.INACTIVE
    
    def test_validate_pattern_quality_high(self):
        """Test pattern quality validation - high quality."""
        flc = FederatedLearningConvergence()
        
        pattern = {
            "epistemic_certainty": 0.95,
            "strength": 0.85
        }
        
        quality = flc._validate_pattern_quality(pattern)
        assert quality == PatternQuality.HIGH
    
    def test_validate_pattern_quality_medium(self):
        """Test pattern quality validation - medium quality."""
        flc = FederatedLearningConvergence()
        
        pattern = {
            "epistemic_certainty": 0.80,
            "strength": 0.60
        }
        
        quality = flc._validate_pattern_quality(pattern)
        assert quality == PatternQuality.MEDIUM
    
    def test_validate_pattern_quality_invalid(self):
        """Test pattern quality validation - invalid."""
        flc = FederatedLearningConvergence()
        
        pattern = {
            "epistemic_certainty": 0.50,  # Below threshold
            "strength": 0.30
        }
        
        quality = flc._validate_pattern_quality(pattern)
        assert quality == PatternQuality.INVALID
    
    @pytest.mark.asyncio
    async def test_aggregate_learning(self, federated_learning, sample_pattern):
        """Test learning aggregation."""
        federated_learning.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        result = await federated_learning.aggregate_learning(
            "test-instance-1",
            [sample_pattern]
        )
        
        assert result.convergence_score >= 0.0
        assert result.emergence_score >= 0.0
        assert result.patterns_aggregated >= 0
        assert result.instances_contributing >= 1
    
    @pytest.mark.asyncio
    async def test_aggregate_learning_unregistered_instance(self, federated_learning, sample_pattern):
        """Test aggregation with unregistered instance raises error."""
        with pytest.raises(ValueError, match="not registered"):
            await federated_learning.aggregate_learning(
                "unregistered-instance",
                [sample_pattern]
            )
    
    @pytest.mark.asyncio
    async def test_aggregate_learning_multiple_patterns(self, federated_learning, sample_patterns):
        """Test aggregation with multiple patterns."""
        federated_learning.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        result = await federated_learning.aggregate_learning(
            "test-instance-1",
            sample_patterns
        )
        
        assert result.patterns_aggregated >= 0
        assert len(federated_learning.instance_patterns["test-instance-1"]) > 0
    
    @pytest.mark.asyncio
    async def test_aggregate_learning_invalid_patterns(self, federated_learning):
        """Test aggregation filters invalid patterns."""
        federated_learning.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        invalid_pattern = {
            "pattern_id": "invalid",
            "pattern_type": "test",
            "epistemic_certainty": 0.50,  # Below threshold
            "strength": 0.30
        }
        
        result = await federated_learning.aggregate_learning(
            "test-instance-1",
            [invalid_pattern]
        )
        
        # Invalid pattern should be filtered out
        assert len(federated_learning.instance_patterns["test-instance-1"]) == 0
    
    def test_calculate_convergence_score_empty(self):
        """Test convergence score calculation with no patterns."""
        flc = FederatedLearningConvergence()
        
        score = flc._calculate_convergence_score()
        assert score == 0.0
    
    @pytest.mark.asyncio
    async def test_calculate_convergence_score_with_patterns(self, federated_learning, sample_patterns):
        """Test convergence score calculation with patterns."""
        federated_learning.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        await federated_learning.aggregate_learning(
            "test-instance-1",
            sample_patterns
        )
        
        score = federated_learning._calculate_convergence_score()
        assert 0.0 <= score <= 1.0
    
    def test_detect_cross_instance_emergence_empty(self):
        """Test emergence detection with no patterns."""
        flc = FederatedLearningConvergence()
        
        emergence = flc._detect_cross_instance_emergence()
        assert emergence == 0.0
    
    @pytest.mark.asyncio
    async def test_detect_cross_instance_emergence_with_patterns(self, federated_learning, sample_patterns):
        """Test emergence detection with patterns."""
        federated_learning.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        await federated_learning.aggregate_learning(
            "test-instance-1",
            sample_patterns
        )
        
        emergence = federated_learning._detect_cross_instance_emergence()
        assert 0.0 <= emergence <= 1.0
    
    def test_calculate_pattern_alignment_single_instance(self):
        """Test pattern alignment with single instance."""
        flc = FederatedLearningConvergence()
        flc.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        alignment = flc._calculate_pattern_alignment()
        assert alignment == 1.0  # Single instance = perfect alignment
    
    @pytest.mark.asyncio
    async def test_calculate_pattern_alignment_multiple_instances(self, federated_learning):
        """Test pattern alignment with multiple instances."""
        # Register multiple instances
        federated_learning.register_instance("instance-1", "Instance 1", "us-east-1")
        federated_learning.register_instance("instance-2", "Instance 2", "us-west-2")
        
        # Add patterns to each instance
        pattern1 = create_test_pattern("pattern-1", "positive", 0.85, 0.80, 0.90)
        pattern2 = create_test_pattern("pattern-2", "positive", 0.85, 0.80, 0.90)
        
        await federated_learning.aggregate_learning("instance-1", [pattern1])
        await federated_learning.aggregate_learning("instance-2", [pattern2])
        
        alignment = federated_learning._calculate_pattern_alignment()
        assert 0.0 <= alignment <= 1.0
    
    def test_get_global_pattern_library(self):
        """Test getting global pattern library."""
        flc = FederatedLearningConvergence()
        
        library = flc.get_global_pattern_library()
        assert isinstance(library, dict)
        assert len(library) == 0
    
    def test_get_instance_registry(self):
        """Test getting instance registry."""
        flc = FederatedLearningConvergence()
        flc.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        registry = flc.get_instance_registry()
        assert isinstance(registry, dict)
        assert "test-instance-1" in registry
    
    def test_get_stats(self):
        """Test getting statistics."""
        flc = FederatedLearningConvergence()
        
        stats = flc.get_stats()
        assert isinstance(stats, dict)
        assert "total_patterns_received" in stats
        assert "total_patterns_aggregated" in stats
        assert "total_instances_registered" in stats

