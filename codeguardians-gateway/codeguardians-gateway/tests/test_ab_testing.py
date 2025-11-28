"""
A/B Testing Framework Test Suite

Comprehensive test suite for A/B testing functionality including:
- Experiment management tests
- User segmentation tests
- Statistical analysis tests
- Canary deployment tests
- Analytics and tracking tests
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
import json
import redis

from app.core.ab_testing import ABTestingFramework
from app.core.ab_testing.models import ExperimentConfig, ExperimentStatus, VariantType
from app.core.ab_testing.segmentation import UserSegmentationEngine, TrafficSplitter
from app.core.ab_testing.statistical_analysis import StatisticalAnalyzer
from app.core.ab_testing.canary_deployment import CanaryDeploymentManager, CanaryStage
from app.core.ab_testing.analytics import ExperimentTracker, BusinessImpactAnalyzer

# Test fixtures
@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    mock_redis = Mock(spec=redis.Redis)
    mock_redis.ping.return_value = True
    mock_redis.get.return_value = None
    mock_redis.setex.return_value = True
    mock_redis.delete.return_value = 1
    mock_redis.keys.return_value = []
    return mock_redis

@pytest.fixture
def ab_testing_framework(mock_redis):
    """A/B testing framework instance for testing."""
    return ABTestingFramework(mock_redis)

@pytest.fixture
def sample_experiment_config():
    """Sample experiment configuration for testing."""
    return ExperimentConfig(
        experiment_id="test_exp_001",
        name="Test Experiment",
        description="A test experiment for validation",
        status=ExperimentStatus.DRAFT,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=7),
        traffic_split={"control": 50.0, "treatment": 50.0},
        success_metrics=["conversion_rate", "response_time"],
        minimum_sample_size=1000,
        confidence_level=0.95,
        power=0.8,
        primary_metric="conversion_rate",
        secondary_metrics=["response_time"],
        target_audience={},
        exclusion_criteria=[],
        created_by="test_user",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

class TestABTestingFramework:
    """Test A/B testing framework integration."""
    
    def test_framework_initialization(self, mock_redis):
        """Test framework initialization."""
        framework = ABTestingFramework(mock_redis)
        
        assert framework.redis_client == mock_redis
        assert framework.segmentation_engine is not None
        assert framework.statistical_analyzer is not None
        assert framework.canary_manager is not None
        assert framework.tracker is not None
        assert framework.business_analyzer is not None
    
    @pytest.mark.asyncio
    async def test_create_experiment(self, ab_testing_framework):
        """Test experiment creation."""
        experiment_id = await ab_testing_framework.create_experiment(
            name="Test Experiment",
            description="A test experiment",
            traffic_split={"control": 50.0, "treatment": 50.0},
            success_metrics=["conversion_rate"],
            primary_metric="conversion_rate",
            created_by="test_user"
        )
        
        assert experiment_id is not None
        assert experiment_id.startswith("exp_")
    
    def test_validate_traffic_split(self, ab_testing_framework):
        """Test traffic split validation."""
        # Valid traffic split
        valid_split = {"control": 50.0, "treatment": 50.0}
        assert ab_testing_framework.validate_traffic_split(valid_split) is True
        
        # Invalid traffic split
        invalid_split = {"control": 30.0, "treatment": 50.0}
        assert ab_testing_framework.validate_traffic_split(invalid_split) is False
    
    def test_normalize_traffic_split(self, ab_testing_framework):
        """Test traffic split normalization."""
        # Test normalization
        unnormalized_split = {"control": 30.0, "treatment": 50.0}
        normalized_split = ab_testing_framework.normalize_traffic_split(unnormalized_split)
        
        assert abs(sum(normalized_split.values()) - 100.0) < 0.01
    
    def test_create_canary_split(self, ab_testing_framework):
        """Test canary split creation."""
        base_split = {"control": 50.0, "treatment": 50.0}
        canary_split = ab_testing_framework.create_canary_split(base_split, 10.0)
        
        assert "canary" in canary_split
        assert canary_split["canary"] == 10.0
        assert abs(sum(canary_split.values()) - 100.0) < 0.01
    
    @pytest.mark.asyncio
    async def test_get_framework_status(self, ab_testing_framework):
        """Test framework status."""
        status = await ab_testing_framework.get_framework_status()
        
        assert status["status"] == "healthy"
        assert "components" in status
        assert "active_deployments" in status
        assert "redis_connected" in status

class TestUserSegmentation:
    """Test user segmentation functionality."""
    
    @pytest.fixture
    def segmentation_engine(self, mock_redis):
        """User segmentation engine for testing."""
        return UserSegmentationEngine(mock_redis)
    
    @pytest.mark.asyncio
    async def test_assign_user_to_variant(self, segmentation_engine):
        """Test user assignment to variants."""
        # Mock experiment config
        with patch.object(segmentation_engine, '_get_experiment_config') as mock_get_config:
            mock_config = Mock()
            mock_config.status = ExperimentStatus.RUNNING
            mock_config.traffic_split = {"control": 50.0, "treatment": 50.0}
            mock_config.exclusion_criteria = []
            mock_config.target_audience = {}
            mock_get_config.return_value = mock_config
            
            variant = await segmentation_engine.assign_user_to_variant(
                user_id="test_user",
                experiment_id="test_exp",
                user_attributes={"age": 25}
            )
            
            assert variant in ["control", "treatment"]
    
    def test_consistent_hashing(self, segmentation_engine):
        """Test consistent hashing for user assignment."""
        # Test that same user gets same variant
        user_id = "test_user"
        experiment_id = "test_exp"
        traffic_split = {"control": 50.0, "treatment": 50.0}
        
        variant1 = segmentation_engine._assign_variant_consistent_hashing(
            user_id, experiment_id, traffic_split
        )
        variant2 = segmentation_engine._assign_variant_consistent_hashing(
            user_id, experiment_id, traffic_split
        )
        
        assert variant1 == variant2
    
    def test_traffic_splitter_validation(self):
        """Test traffic splitter validation."""
        # Valid split
        valid_split = {"control": 50.0, "treatment": 50.0}
        assert TrafficSplitter.validate_traffic_split(valid_split) is True
        
        # Invalid split
        invalid_split = {"control": 30.0, "treatment": 50.0}
        assert TrafficSplitter.validate_traffic_split(invalid_split) is False
    
    def test_traffic_splitter_normalization(self):
        """Test traffic splitter normalization."""
        unnormalized = {"control": 30.0, "treatment": 50.0}
        normalized = TrafficSplitter.normalize_traffic_split(unnormalized)
        
        assert abs(sum(normalized.values()) - 100.0) < 0.01

class TestStatisticalAnalysis:
    """Test statistical analysis functionality."""
    
    @pytest.fixture
    def statistical_analyzer(self):
        """Statistical analyzer for testing."""
        return StatisticalAnalyzer()
    
    def test_t_test_analysis(self, statistical_analyzer):
        """Test t-test statistical analysis."""
        # Generate sample data using fallback if numpy is not available
        try:
            import numpy as np
            np.random.seed(42)
            control_data = np.random.normal(100, 10, 100)
            treatment_data = np.random.normal(105, 10, 100)
            control_data_list = control_data.tolist()
            treatment_data_list = treatment_data.tolist()
        except ImportError:
            # Fallback data generation without numpy
            import random
            import math
            random.seed(42)
            control_data_list = [random.gauss(100, 10) for _ in range(100)]
            treatment_data_list = [random.gauss(105, 10) for _ in range(100)]
        
        analysis = statistical_analyzer.analyze_experiment(
            experiment_id="test_exp",
            variant_a_data=control_data_list,
            variant_b_data=treatment_data_list,
            variant_a_name="control",
            variant_b_name="treatment",
            metric_type="continuous"
        )
        
        assert analysis.experiment_id == "test_exp"
        assert analysis.variant_a == "control"
        assert analysis.variant_b == "treatment"
        assert analysis.sample_size_a == 100
        assert analysis.sample_size_b == 100
        assert analysis.primary_test.test_name in ["Independent Samples t-test", "t-test (approximate)"]
        # p_value may be None if scipy is not available
        if analysis.primary_test.p_value is not None:
            assert 0 <= analysis.primary_test.p_value <= 1
    
    def test_chi_square_analysis(self, statistical_analyzer):
        """Test chi-square statistical analysis."""
        # Generate binary data
        control_data = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0] * 10
        treatment_data = [1, 1, 1, 0, 1, 1, 1, 0, 1, 1] * 10
        
        analysis = statistical_analyzer.analyze_experiment(
            experiment_id="test_exp",
            variant_a_data=control_data,
            variant_b_data=treatment_data,
            variant_a_name="control",
            variant_b_name="treatment",
            metric_type="binary"
        )
        
        assert analysis.primary_test.test_name in ["Chi-square test", "Chi-square test (approximate)"]
        # p_value may be None if scipy is not available
        if analysis.primary_test.p_value is not None:
            assert 0 <= analysis.primary_test.p_value <= 1
    
    def test_mann_whitney_analysis(self, statistical_analyzer):
        """Test Mann-Whitney statistical analysis."""
        # Generate count data
        control_data = [5, 3, 7, 2, 8, 4, 6, 1, 9, 3] * 10
        treatment_data = [8, 6, 9, 5, 10, 7, 8, 4, 11, 6] * 10
        
        analysis = statistical_analyzer.analyze_experiment(
            experiment_id="test_exp",
            variant_a_data=control_data,
            variant_b_data=treatment_data,
            variant_a_name="control",
            variant_b_name="treatment",
            metric_type="count"
        )
        
        assert analysis.primary_test.test_name in ["Mann-Whitney U test", "Mann-Whitney U test (approximate)"]
        # p_value may be None if scipy is not available
        if analysis.primary_test.p_value is not None:
            assert 0 <= analysis.primary_test.p_value <= 1

class TestCanaryDeployment:
    """Test canary deployment functionality."""
    
    @pytest.fixture
    def canary_manager(self, mock_redis):
        """Canary deployment manager for testing."""
        segmentation_engine = UserSegmentationEngine(mock_redis)
        statistical_analyzer = StatisticalAnalyzer()
        return CanaryDeploymentManager(segmentation_engine, statistical_analyzer)
    
    @pytest.mark.asyncio
    async def test_canary_deployment_creation(self, canary_manager):
        """Test canary deployment creation."""
        from app.core.ab_testing.canary_deployment import CanaryConfigBuilder
        
        config = (CanaryConfigBuilder()
                 .for_experiment("test_exp", "canary_variant")
                 .with_stages([CanaryStage.INITIAL, CanaryStage.SMALL])
                 .with_duration(5)  # 5 minutes for testing
                 .with_thresholds(0.95, 0.05)
                 .with_automation(True, True)
                 .build())
        
        deployment = await canary_manager.start_canary_deployment(
            experiment_id="test_exp",
            canary_variant="canary_variant",
            config=config
        )
        
        assert deployment.deployment_id is not None
        assert deployment.experiment_id == "test_exp"
        assert deployment.canary_config.canary_variant == "canary_variant"
    
    def test_canary_config_builder(self):
        """Test canary configuration builder."""
        from app.core.ab_testing.canary_deployment import CanaryConfigBuilder, CanaryStage
        
        config = (CanaryConfigBuilder()
                 .for_experiment("test_exp", "canary_variant")
                 .with_stages([CanaryStage.INITIAL, CanaryStage.SMALL])
                 .with_duration(30)
                 .with_thresholds(0.95, 0.05)
                 .with_automation(True, True)
                 .build())
        
        assert config.experiment_id == "test_exp"
        assert config.canary_variant == "canary_variant"
        assert len(config.stages) == 2
        assert config.stage_duration_minutes == 30
        assert config.success_threshold == 0.95
        assert config.failure_threshold == 0.05
        assert config.auto_promote is True
        assert config.auto_rollback is True

class TestExperimentTracking:
    """Test experiment tracking and analytics."""
    
    @pytest.fixture
    def experiment_tracker(self, mock_redis):
        """Experiment tracker for testing."""
        return ExperimentTracker(mock_redis)
    
    @pytest.mark.asyncio
    async def test_track_experiment_result(self, experiment_tracker):
        """Test experiment result tracking."""
        await experiment_tracker.track_experiment_result(
            experiment_id="test_exp",
            variant_name="control",
            user_id="test_user",
            session_id="test_session",
            metrics={"success": 1, "response_time": 100.0},
            result_metadata={"source": "test"}
        )
        
        # Verify metrics were updated
        metrics = await experiment_tracker.get_experiment_metrics("test_exp")
        assert metrics["experiment_id"] == "test_exp"
        assert metrics["total_users"] >= 1
    
    @pytest.mark.asyncio
    async def test_performance_snapshot(self, experiment_tracker):
        """Test performance snapshot generation."""
        # Track some results first
        await experiment_tracker.track_experiment_result(
            experiment_id="test_exp",
            variant_name="control",
            user_id="test_user",
            session_id="test_session",
            metrics={"success": 1, "response_time": 100.0}
        )
        
        snapshot = await experiment_tracker.get_experiment_performance_snapshot("test_exp")
        
        assert "timestamp" in snapshot
        assert "metrics" in snapshot
        assert "variant_performance" in snapshot
        assert "system_health" in snapshot
        assert "alerts" in snapshot

class TestBusinessImpactAnalysis:
    """Test business impact analysis."""
    
    @pytest.fixture
    def business_analyzer(self, mock_redis):
        """Business impact analyzer for testing."""
        tracker = ExperimentTracker(mock_redis)
        return BusinessImpactAnalyzer(tracker)
    
    @pytest.mark.asyncio
    async def test_business_impact_analysis(self, business_analyzer, sample_experiment_config):
        """Test business impact analysis."""
        analysis = await business_analyzer.analyze_business_impact(
            experiment_id="test_exp",
            experiment_config=sample_experiment_config
        )
        
        assert analysis.experiment_id == "test_exp"
        assert "analysis_date" in analysis.__dict__
        assert "revenue_impact" in analysis.__dict__
        assert "cost_savings" in analysis.__dict__
        assert "user_satisfaction_impact" in analysis.__dict__
        assert "operational_efficiency" in analysis.__dict__
        assert "risk_assessment" in analysis.__dict__
        assert "recommendations" in analysis.__dict__
        assert "confidence_level" in analysis.__dict__

# Integration tests
class TestABTestingIntegration:
    """Integration tests for A/B testing framework."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_experiment_flow(self, ab_testing_framework):
        """Test complete experiment flow from creation to analysis."""
        # Create experiment
        experiment_id = await ab_testing_framework.create_experiment(
            name="Integration Test Experiment",
            description="End-to-end test",
            traffic_split={"control": 50.0, "treatment": 50.0},
            success_metrics=["conversion_rate"],
            primary_metric="conversion_rate",
            created_by="test_user"
        )
        
        assert experiment_id is not None
        
        # Start experiment
        success = await ab_testing_framework.start_experiment(experiment_id)
        assert success is True
        
        # Assign users to variants
        variant1 = await ab_testing_framework.assign_user_to_variant(
            user_id="user1",
            experiment_id=experiment_id
        )
        variant2 = await ab_testing_framework.assign_user_to_variant(
            user_id="user2",
            experiment_id=experiment_id
        )
        
        assert variant1 in ["control", "treatment"]
        assert variant2 in ["control", "treatment"]
        
        # Track results
        await ab_testing_framework.track_experiment_result(
            experiment_id=experiment_id,
            variant_name=variant1,
            user_id="user1",
            session_id="session1",
            metrics={"conversion_rate": 0.8, "response_time": 150.0}
        )
        
        await ab_testing_framework.track_experiment_result(
            experiment_id=experiment_id,
            variant_name=variant2,
            user_id="user2",
            session_id="session2",
            metrics={"conversion_rate": 0.9, "response_time": 120.0}
        )
        
        # Get metrics
        metrics = await ab_testing_framework.get_experiment_metrics(experiment_id)
        assert metrics["total_users"] >= 2
        
        # Stop experiment
        success = await ab_testing_framework.stop_experiment(experiment_id)
        assert success is True

# Performance tests
class TestABTestingPerformance:
    """Performance tests for A/B testing framework."""
    
    @pytest.mark.asyncio
    async def test_concurrent_user_assignment(self, ab_testing_framework):
        """Test concurrent user assignment performance."""
        experiment_id = await ab_testing_framework.create_experiment(
            name="Performance Test",
            description="Concurrent assignment test",
            traffic_split={"control": 50.0, "treatment": 50.0},
            success_metrics=["conversion_rate"],
            primary_metric="conversion_rate",
            created_by="test_user"
        )
        
        # Test concurrent assignments
        tasks = []
        for i in range(100):
            task = ab_testing_framework.assign_user_to_variant(
                user_id=f"user_{i}",
                experiment_id=experiment_id
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Verify all assignments succeeded
        assert len(results) == 100
        assert all(result in ["control", "treatment"] for result in results)
    
    @pytest.mark.asyncio
    async def test_concurrent_result_tracking(self, ab_testing_framework):
        """Test concurrent result tracking performance."""
        experiment_id = await ab_testing_framework.create_experiment(
            name="Performance Test",
            description="Concurrent tracking test",
            traffic_split={"control": 50.0, "treatment": 50.0},
            success_metrics=["conversion_rate"],
            primary_metric="conversion_rate",
            created_by="test_user"
        )
        
        # Test concurrent result tracking
        tasks = []
        for i in range(100):
            task = ab_testing_framework.track_experiment_result(
                experiment_id=experiment_id,
                variant_name="control" if i % 2 == 0 else "treatment",
                user_id=f"user_{i}",
                session_id=f"session_{i}",
                metrics={"conversion_rate": 0.8, "response_time": 150.0}
            )
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        
        # Verify metrics were updated
        metrics = await ab_testing_framework.get_experiment_metrics(experiment_id)
        assert metrics["total_users"] >= 100

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
