"""
Pytest configuration and fixtures for Marketing Automation Orbit tests.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def project_root_path():
    """Return project root path."""
    return Path(__file__).parent.parent


@pytest.fixture
def config_path(project_root_path):
    """Return config directory path."""
    return project_root_path / "config"


@pytest.fixture
def sample_strategy_data():
    """Sample strategy data for testing."""
    return {
        "id": "test_strategy_1",
        "name": "Test Strategy",
        "timeframe": "3 months",
        "budget": 5000.0,
        "goals": {"leads": 150, "customers": 10},
        "channels": ["google_ads", "linkedin_ads"],
        "execution_plan": {
            "week_1": "Setup and launch",
            "week_2_4": "Monitor and optimize"
        }
    }

