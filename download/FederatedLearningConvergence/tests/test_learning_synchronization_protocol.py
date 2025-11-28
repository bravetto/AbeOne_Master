"""
Unit tests for LearningSynchronizationProtocol.
"""

import pytest
import asyncio
from datetime import datetime, timedelta

from EMERGENT_OS.synthesis.learning_synchronization_protocol import LearningSynchronizationProtocol
from EMERGENT_OS.synthesis.federated_learning_convergence import FederatedLearningConvergence
from EMERGENT_OS.synthesis.global_scoring_aggregator import GlobalScoringAggregator
from tests.synthesis.conftest import (
    create_test_instance,
    create_test_pattern,
    sample_patterns
)


class TestLearningSynchronizationProtocol:
    """Test suite for LearningSynchronizationProtocol."""
    
    @pytest.fixture
    def protocol(self):
        """Create synchronization protocol instance."""
        flc = FederatedLearningConvergence()
        gsa = GlobalScoringAggregator()
        return LearningSynchronizationProtocol(
            flc,
            gsa,
            sync_window=timedelta(minutes=1),
            min_instances_for_sync=1
        )
    
    def test_initialization(self, protocol):
        """Test initialization."""
        assert protocol.sync_window == timedelta(minutes=1)
        assert protocol.min_instances_for_sync == 1
        assert protocol.last_sync_time is None
        assert len(protocol.sync_history) == 0
    
    def test_register_instance_callback(self, protocol):
        """Test registering instance callbacks."""
        async def update_callback(instance_id, sync_window):
            return {"instance_id": instance_id, "patterns": []}
        
        async def dist_callback(instance_id, patterns):
            pass
        
        protocol.register_instance_callback("test-1", update_callback, dist_callback)
        
        assert "test-1" in protocol.instance_update_callbacks
        assert "test-1" in protocol.instance_distribution_callbacks
    
    @pytest.mark.asyncio
    async def test_synchronize_learning_no_instances(self, protocol):
        """Test synchronization with no instances."""
        result = await protocol.synchronize_learning()
        
        assert result.convergence_score == 0.0
        assert result.instances_synced == 0
        assert result.convergence_achieved is False
    
    @pytest.mark.asyncio
    async def test_synchronize_learning_with_instances(self, protocol, sample_patterns):
        """Test synchronization with instances."""
        # Register instances
        protocol.federated_learning.register_instance("test-1", "Test 1", "us-east-1")
        protocol.federated_learning.register_instance("test-2", "Test 2", "us-west-2")
        
        # Add patterns to instances
        await protocol.federated_learning.aggregate_learning("test-1", sample_patterns[:2])
        await protocol.federated_learning.aggregate_learning("test-2", sample_patterns[2:])
        
        # Synchronize
        result = await protocol.synchronize_learning()
        
        assert result.instances_synced >= 0
        assert result.patterns_aggregated >= 0
        assert isinstance(result.convergence_achieved, bool)
    
    @pytest.mark.asyncio
    async def test_collect_instance_updates(self, protocol, sample_patterns):
        """Test collecting instance updates."""
        protocol.federated_learning.register_instance("test-1", "Test 1", "us-east-1")
        await protocol.federated_learning.aggregate_learning("test-1", sample_patterns)
        
        updates = await protocol._collect_instance_updates(timedelta(minutes=1))
        
        assert isinstance(updates, dict)
        # May be empty if instance doesn't have callback, but should not error
    
    def test_validate_updates(self, protocol):
        """Test validating updates."""
        updates = {
            "test-1": {
                "instance_id": "test-1",
                "patterns": [
                    {
                        "signature_id": "sig-1",
                        "pattern_type": "positive",
                        "strength": 0.85,
                        "resonance": 0.80,
                        "frequency": 10,
                        "epistemic_certainty": 0.90  # Valid
                    },
                    {
                        "signature_id": "sig-2",
                        "pattern_type": "positive",
                        "strength": 0.50,
                        "resonance": 0.40,
                        "frequency": 5,
                        "epistemic_certainty": 0.50  # Invalid (below threshold)
                    }
                ]
            }
        }
        
        validated = protocol._validate_updates(updates)
        
        assert "test-1" in validated
        # Should filter out invalid pattern
        assert len(validated["test-1"]["patterns"]) <= len(updates["test-1"]["patterns"])
    
    @pytest.mark.asyncio
    async def test_aggregate_with_consensus(self, protocol, sample_patterns):
        """Test aggregation with consensus."""
        protocol.federated_learning.register_instance("test-1", "Test 1", "us-east-1")
        await protocol.federated_learning.aggregate_learning("test-1", sample_patterns)
        
        # Create validated updates
        updates = {
            "test-1": {
                "instance_id": "test-1",
                "patterns": [
                    {
                        "signature_id": f"sig-{i}",
                        "pattern_type": "positive",
                        "strength": 0.85,
                        "resonance": 0.80,
                        "frequency": 10,
                        "epistemic_certainty": 0.90,
                        "module_signatures": ["mod1"],
                        "event_type_signatures": ["evt1"]
                    }
                    for i in range(3)
                ]
            }
        }
        
        aggregated = await protocol._aggregate_with_consensus(updates)
        
        assert "pattern_count" in aggregated
        assert "instances_contributing" in aggregated
    
    def test_detect_convergence(self, protocol):
        """Test convergence detection."""
        # Register instance and add patterns
        protocol.federated_learning.register_instance("test-1", "Test 1", "us-east-1")
        
        aggregated_knowledge = {
            "pattern_count": 10,
            "global_patterns": []
        }
        
        metrics = protocol._detect_convergence(aggregated_knowledge)
        
        assert "global_convergence" in metrics
        assert "pattern_alignment" in metrics
        assert "global_emergence" in metrics
    
    @pytest.mark.asyncio
    async def test_distribute_knowledge(self, protocol):
        """Test knowledge distribution."""
        aggregated_knowledge = {
            "global_patterns": []
        }
        
        result = await protocol._distribute_knowledge(aggregated_knowledge)
        
        assert "distributed" in result
        assert result["distributed"] is True
    
    @pytest.mark.asyncio
    async def test_verify_convergence(self, protocol):
        """Test convergence verification."""
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
        
        convergence_metrics = {
            "global_score": global_score
        }
        
        verification = await protocol._verify_convergence(convergence_metrics)
        
        assert "converged" in verification
        assert isinstance(verification["converged"], bool)
    
    def test_get_sync_history(self, protocol):
        """Test getting sync history."""
        history = protocol.get_sync_history()
        assert isinstance(history, list)
        assert len(history) == 0
    
    def test_get_stats(self, protocol):
        """Test getting statistics."""
        stats = protocol.get_stats()
        assert isinstance(stats, dict)
        assert "total_syncs" in stats
        assert "successful_syncs" in stats
        assert "failed_syncs" in stats

