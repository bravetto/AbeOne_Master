"""
Tests for MarketingAutomationOrbit main module.
"""

import pytest
from pathlib import Path
from src.main import MarketingAutomationOrbit


class TestMarketingAutomationOrbit:
    """Test suite for MarketingAutomationOrbit."""
    
    def test_orbit_initialization(self, config_path):
        """Test orbit initializes correctly."""
        orbit = MarketingAutomationOrbit(config_path=config_path)
        
        assert orbit is not None
        assert orbit.engine is not None
        assert orbit.scheduler is not None
        assert orbit.kernel_adapter is not None
        assert orbit.guardian_adapter is not None
        assert orbit.module_adapter is not None
        assert orbit.bus_adapter is not None
        assert orbit.initialized is False
        assert orbit.running is False
    
    def test_orbit_initialize(self, config_path):
        """Test orbit initialization process."""
        orbit = MarketingAutomationOrbit(config_path=config_path)
        
        # Initialize should succeed (may have warnings but should not fail)
        result = orbit.initialize()
        
        # Should complete initialization (may have warnings)
        assert orbit.initialized is True
    
    def test_orbit_get_status(self, config_path):
        """Test getting system status."""
        orbit = MarketingAutomationOrbit(config_path=config_path)
        orbit.initialize()
        
        status = orbit.get_status()
        
        assert isinstance(status, dict)
        assert "initialized" in status
        assert "running" in status
        assert "module_info" in status
        assert "guardian_status" in status
        assert "strategies_loaded" in status
        assert "campaigns_active" in status
        assert status["initialized"] is True
    
    def test_orbit_scheduler_lifecycle(self, config_path):
        """Test scheduler start/stop."""
        orbit = MarketingAutomationOrbit(config_path=config_path)
        orbit.initialize()
        
        # Start scheduler
        orbit.start_scheduler()
        assert orbit.running is True
        
        # Stop scheduler
        orbit.stop_scheduler()
        assert orbit.running is False
    
    def test_double_initialization(self, config_path):
        """Test that double initialization doesn't break."""
        orbit = MarketingAutomationOrbit(config_path=config_path)
        
        result1 = orbit.initialize()
        result2 = orbit.initialize()
        
        assert result1 is True
        assert result2 is True
        assert orbit.initialized is True

