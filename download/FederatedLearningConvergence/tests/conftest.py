"""
Test fixtures and utilities for federated learning convergence tests.
"""

import pytest
import asyncio
from typing import Dict, List, Any
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock

from EMERGENT_OS.synthesis.federated_convergence_types import (
    InstanceMetadata,
    InstanceScores,
    PatternSignature,
    AggregatedPattern,
    InstanceStatus,
    PatternQuality
)
from EMERGENT_OS.synthesis.federated_learning_convergence import FederatedLearningConvergence
from EMERGENT_OS.synthesis.global_scoring_aggregator import GlobalScoringAggregator
from EMERGENT_OS.synthesis.learning_synchronization_protocol import LearningSynchronizationProtocol


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_instance_metadata() -> InstanceMetadata:
    """Create sample instance metadata."""
    return InstanceMetadata(
        instance_id="test-instance-1",
        instance_name="Test Instance 1",
        deployment_region="us-east-1",
        reliability_score=0.95,
        data_quality_score=0.90,
        pattern_count=100,
        total_requests=1000
    )


@pytest.fixture
def sample_pattern() -> Dict[str, Any]:
    """Create sample pattern dictionary."""
    return {
        "pattern_id": "test-pattern-1",
        "pattern_type": "positive",
        "strength": 0.85,
        "resonance": 0.80,
        "frequency": 10,
        "modules": ["module1", "module2"],
        "event_types": ["event1", "event2"],
        "epistemic_certainty": 0.90
    }


@pytest.fixture
def sample_patterns() -> List[Dict[str, Any]]:
    """Create list of sample patterns."""
    return [
        {
            "pattern_id": f"test-pattern-{i}",
            "pattern_type": "positive",
            "strength": 0.80 + (i * 0.01),
            "resonance": 0.75 + (i * 0.01),
            "frequency": 5 + i,
            "modules": [f"module{i}"],
            "event_types": [f"event{i}"],
            "epistemic_certainty": 0.85 + (i * 0.01)
        }
        for i in range(5)
    ]


@pytest.fixture
def sample_instance_scores() -> InstanceScores:
    """Create sample instance scores."""
    return InstanceScores(
        instance_id="test-instance-1",
        convergence_score=0.85,
        emergence_score=0.80,
        resonance_score=0.75,
        unified_score=0.80,
        pattern_count=100
    )


@pytest.fixture
def federated_learning() -> FederatedLearningConvergence:
    """Create FederatedLearningConvergence instance."""
    return FederatedLearningConvergence(
        min_epistemic_certainty=0.85,
        pattern_quality_threshold=0.7
    )


@pytest.fixture
def global_scoring() -> GlobalScoringAggregator:
    """Create GlobalScoringAggregator instance."""
    return GlobalScoringAggregator(
        min_instance_weight=0.1,
        max_variance_threshold=0.1
    )


@pytest.fixture
def sync_protocol(federated_learning, global_scoring) -> LearningSynchronizationProtocol:
    """Create LearningSynchronizationProtocol instance."""
    return LearningSynchronizationProtocol(
        federated_learning=federated_learning,
        global_scoring=global_scoring,
        sync_window=timedelta(minutes=1),  # Short window for tests
        min_instances_for_sync=1  # Lower threshold for tests
    )


@pytest.fixture
def mock_instance_update_callback():
    """Create mock instance update callback."""
    async def callback(instance_id: str, sync_window: timedelta) -> Dict[str, Any]:
        return {
            "instance_id": instance_id,
            "patterns": [],
            "timestamp": datetime.now().isoformat()
        }
    return callback


@pytest.fixture
def mock_instance_distribution_callback():
    """Create mock instance distribution callback."""
    async def callback(instance_id: str, global_patterns: List[AggregatedPattern]) -> None:
        pass
    return callback


def create_test_instance(
    instance_id: str,
    reliability: float = 0.95,
    data_quality: float = 0.90,
    pattern_count: int = 100
) -> InstanceMetadata:
    """Create test instance metadata."""
    return InstanceMetadata(
        instance_id=instance_id,
        instance_name=f"Test Instance {instance_id}",
        deployment_region="us-east-1",
        reliability_score=reliability,
        data_quality_score=data_quality,
        pattern_count=pattern_count,
        total_requests=pattern_count * 10
    )


def create_test_pattern(
    pattern_id: str,
    pattern_type: str = "positive",
    strength: float = 0.85,
    resonance: float = 0.80,
    epistemic_certainty: float = 0.90
) -> Dict[str, Any]:
    """Create test pattern dictionary."""
    return {
        "pattern_id": pattern_id,
        "pattern_type": pattern_type,
        "strength": strength,
        "resonance": resonance,
        "frequency": 10,
        "modules": [f"module-{pattern_id}"],
        "event_types": [f"event-{pattern_id}"],
        "epistemic_certainty": epistemic_certainty
    }


def create_test_instance_scores(
    instance_id: str,
    convergence_score: float = 0.85,
    emergence_score: float = 0.80
) -> InstanceScores:
    """Create test instance scores."""
    return InstanceScores(
        instance_id=instance_id,
        convergence_score=convergence_score,
        emergence_score=emergence_score,
        resonance_score=0.75,
        unified_score=(convergence_score + emergence_score) / 2.0,
        pattern_count=100
    )

