"""
Tests for AutomationEngine.
"""

import pytest
from datetime import datetime
from pathlib import Path
from src.engine.automation_engine import (
    AutomationEngine,
    Campaign,
    Strategy,
    CampaignStatus,
    ExecutionMode
)


class TestAutomationEngine:
    """Test suite for AutomationEngine."""
    
    def test_engine_initialization(self, config_path):
        """Test engine initializes correctly."""
        engine = AutomationEngine(config_path=config_path)
        assert engine is not None
        assert engine.execution_mode == ExecutionMode.AUTONOMOUS
        assert isinstance(engine.strategies, dict)
        assert isinstance(engine.campaigns, dict)
    
    def test_create_strategy(self, config_path, sample_strategy_data):
        """Test creating a strategy."""
        engine = AutomationEngine(config_path=config_path)
        
        strategy = Strategy(
            id=sample_strategy_data["id"],
            name=sample_strategy_data["name"],
            timeframe=sample_strategy_data["timeframe"],
            budget=sample_strategy_data["budget"],
            goals=sample_strategy_data["goals"],
            channels=sample_strategy_data["channels"],
            execution_plan=sample_strategy_data["execution_plan"],
            created_at=datetime.now()
        )
        
        engine.strategies[strategy.id] = strategy
        assert strategy.id in engine.strategies
        assert engine.strategies[strategy.id].name == sample_strategy_data["name"]
    
    def test_create_campaign(self, config_path):
        """Test creating a campaign."""
        engine = AutomationEngine(config_path=config_path)
        
        campaign = Campaign(
            id="test_campaign_1",
            name="Test Campaign",
            channel="google_ads",
            status=CampaignStatus.DRAFT,
            budget=1000.0,
            start_date=datetime.now(),
            end_date=None,
            target_audience={"age": "25-45"},
            creatives=[{"headline": "Test Headline"}]
        )
        
        engine.campaigns[campaign.id] = campaign
        assert campaign.id in engine.campaigns
        assert engine.campaigns[campaign.id].status == CampaignStatus.DRAFT
    
    def test_strategy_to_dict(self, sample_strategy_data):
        """Test strategy serialization."""
        strategy = Strategy(
            id=sample_strategy_data["id"],
            name=sample_strategy_data["name"],
            timeframe=sample_strategy_data["timeframe"],
            budget=sample_strategy_data["budget"],
            goals=sample_strategy_data["goals"],
            channels=sample_strategy_data["channels"],
            execution_plan=sample_strategy_data["execution_plan"],
            created_at=datetime.now()
        )
        
        strategy_dict = strategy.to_dict()
        assert isinstance(strategy_dict, dict)
        assert strategy_dict["id"] == sample_strategy_data["id"]
        assert strategy_dict["name"] == sample_strategy_data["name"]
        assert "created_at" in strategy_dict
    
    def test_campaign_to_dict(self):
        """Test campaign serialization."""
        campaign = Campaign(
            id="test_campaign_1",
            name="Test Campaign",
            channel="google_ads",
            status=CampaignStatus.ACTIVE,
            budget=1000.0,
            start_date=datetime.now(),
            end_date=None,
            target_audience={"age": "25-45"},
            creatives=[{"headline": "Test"}]
        )
        
        campaign_dict = campaign.to_dict()
        assert isinstance(campaign_dict, dict)
        assert campaign_dict["id"] == "test_campaign_1"
        assert campaign_dict["status"] == "active"
        assert "start_date" in campaign_dict
    
    def test_budget_allocation(self, config_path, sample_strategy_data):
        """Test budget allocation logic."""
        engine = AutomationEngine(config_path=config_path)
        
        strategy = Strategy(
            id=sample_strategy_data["id"],
            name=sample_strategy_data["name"],
            timeframe=sample_strategy_data["timeframe"],
            budget=sample_strategy_data["budget"],
            goals=sample_strategy_data["goals"],
            channels=sample_strategy_data["channels"],
            execution_plan=sample_strategy_data["execution_plan"],
            created_at=datetime.now()
        )
        
        allocation = engine._allocate_budget(strategy)
        
        assert isinstance(allocation, dict)
        assert len(allocation) > 0
        assert sum(allocation.values()) <= strategy.budget * 1.1  # Allow small rounding
    
    def test_campaign_status_transitions(self, config_path):
        """Test campaign status transitions."""
        engine = AutomationEngine(config_path=config_path)
        
        campaign = Campaign(
            id="test_campaign_1",
            name="Test Campaign",
            channel="google_ads",
            status=CampaignStatus.DRAFT,
            budget=1000.0,
            start_date=datetime.now(),
            end_date=None,
            target_audience={},
            creatives=[]
        )
        
        # Test status change
        campaign.status = CampaignStatus.ACTIVE
        assert campaign.status == CampaignStatus.ACTIVE
        
        campaign.status = CampaignStatus.PAUSED
        assert campaign.status == CampaignStatus.PAUSED

