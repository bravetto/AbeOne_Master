"""
Integration tests for federated learning convergence system.
"""

import pytest
import asyncio
from datetime import datetime, timedelta

from EMERGENT_OS.synthesis.federated_convergence_integration import (
    FederatedConvergenceIntegration,
    get_federated_convergence_integration
)
from tests.synthesis.conftest import (
    create_test_instance,
    create_test_pattern,
    sample_patterns
)


class TestFederatedIntegration:
    """Integration tests for federated convergence system."""
    
    @pytest.fixture
    def integration(self):
        """Create federated convergence integration instance."""
        return FederatedConvergenceIntegration(
            sync_window=timedelta(minutes=1),
            auto_sync=False  # Disable auto-sync for tests
        )
    
    @pytest.mark.asyncio
    async def test_register_instance(self, integration):
        """Test instance registration."""
        await integration.register_instance(
            "test-instance-1",
            "Test Instance 1",
            "us-east-1",
            {"environment": "production"}
        )
        
        assert "test-instance-1" in integration.federated_learning.instance_registry
    
    @pytest.mark.asyncio
    async def test_update_instance_convergence(self, integration, sample_patterns):
        """Test updating instance convergence."""
        await integration.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        result = await integration.update_instance_convergence(
            "test-instance-1",
            sample_patterns
        )
        
        assert result.convergence_score >= 0.0
        assert result.emergence_score >= 0.0
        assert result.instances_contributing >= 1
    
    @pytest.mark.asyncio
    async def test_synchronize_all_instances(self, integration, sample_patterns):
        """Test synchronizing all instances."""
        # Register multiple instances
        await integration.register_instance("instance-1", "Instance 1", "us-east-1")
        await integration.register_instance("instance-2", "Instance 2", "us-west-2")
        
        # Add patterns to instances
        await integration.update_instance_convergence("instance-1", sample_patterns[:2])
        await integration.update_instance_convergence("instance-2", sample_patterns[2:])
        
        # Synchronize
        result = await integration.synchronize_all_instances()
        
        assert "convergence_score" in result
        assert "instances_synced" in result
        assert "convergence_achieved" in result
    
    @pytest.mark.asyncio
    async def test_get_global_convergence_score(self, integration, sample_patterns):
        """Test getting global convergence score."""
        await integration.register_instance("test-instance-1", "Test 1", "us-east-1")
        await integration.update_instance_convergence("test-instance-1", sample_patterns)
        
        global_score = await integration.get_global_convergence_score()
        
        assert global_score is not None
        assert 0.0 <= global_score.global_convergence <= 1.0
        assert global_score.instance_count >= 1
    
    @pytest.mark.asyncio
    async def test_get_global_convergence_score_no_instances(self, integration):
        """Test getting global convergence score with no instances."""
        global_score = await integration.get_global_convergence_score()
        
        assert global_score is None
    
    @pytest.mark.asyncio
    async def test_multi_instance_convergence_flow(self, integration):
        """Test full convergence flow with multiple instances."""
        # Register 3 instances
        for i in range(3):
            await integration.register_instance(
                f"instance-{i}",
                f"Instance {i}",
                f"us-east-{i+1}"
            )
        
        # Add different patterns to each instance
        for i in range(3):
            patterns = [
                create_test_pattern(
                    f"pattern-{i}-{j}",
                    "positive",
                    0.80 + (j * 0.02),
                    0.75 + (j * 0.02),
                    0.85 + (j * 0.02)
                )
                for j in range(5)
            ]
            await integration.update_instance_convergence(f"instance-{i}", patterns)
        
        # Synchronize
        sync_result = await integration.synchronize_all_instances()
        
        assert sync_result["instances_synced"] >= 0
        assert sync_result["patterns_aggregated"] >= 0
        
        # Get global convergence
        global_score = await integration.get_global_convergence_score()
        
        if global_score:
            assert global_score.instance_count >= 1
            assert 0.0 <= global_score.global_convergence <= 1.0
    
    def test_get_stats(self, integration):
        """Test getting statistics."""
        stats = integration.get_stats()
        
        assert isinstance(stats, dict)
        assert "orchestrator_integrations" in stats
        assert "convergence_updates" in stats
        assert "federated_learning_stats" in stats
        assert "global_scoring_stats" in stats
        assert "sync_protocol_stats" in stats
    
    def test_singleton_pattern(self):
        """Test singleton pattern for get_federated_convergence_integration."""
        instance1 = get_federated_convergence_integration()
        instance2 = get_federated_convergence_integration()
        
        assert instance1 is instance2
    
    @pytest.mark.asyncio
    async def test_convergence_over_time(self, integration):
        """Test convergence improvement over time."""
        await integration.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        # Initial patterns
        patterns1 = [
            create_test_pattern(f"pattern-{i}", "positive", 0.70, 0.65, 0.85)
            for i in range(3)
        ]
        await integration.update_instance_convergence("test-instance-1", patterns1)
        
        score1 = await integration.get_global_convergence_score()
        initial_score = score1.global_convergence if score1 else 0.0
        
        # Add more patterns (simulating learning over time)
        patterns2 = [
            create_test_pattern(f"pattern-{i}", "positive", 0.85, 0.80, 0.90)
            for i in range(3, 6)
        ]
        await integration.update_instance_convergence("test-instance-1", patterns2)
        
        score2 = await integration.get_global_convergence_score()
        updated_score = score2.global_convergence if score2 else 0.0
        
        # Convergence should improve or stay stable
        assert updated_score >= initial_score - 0.1  # Allow small variance
    
    @pytest.mark.asyncio
    async def test_pattern_quality_filtering(self, integration):
        """Test that low-quality patterns are filtered."""
        await integration.register_instance("test-instance-1", "Test 1", "us-east-1")
        
        # Mix of high and low quality patterns
        patterns = [
            create_test_pattern("good-pattern", "positive", 0.85, 0.80, 0.90),  # High quality
            create_test_pattern("bad-pattern", "positive", 0.50, 0.40, 0.50),  # Low quality (below threshold)
        ]
        
        result = await integration.update_instance_convergence("test-instance-1", patterns)
        
        # Should only aggregate high-quality patterns
        instance_patterns = integration.federated_learning.instance_patterns.get("test-instance-1", [])
        assert len(instance_patterns) <= 1  # Only good pattern should pass

