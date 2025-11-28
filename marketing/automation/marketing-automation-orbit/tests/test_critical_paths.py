"""
Critical path tests - actual business logic.
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from src.engine.automation_engine import AutomationEngine, Strategy


class TestCriticalPaths:
    """Tests for actual business logic."""
    
    def test_load_strategy_from_json(self, config_path):
        """Test loading strategy from JSON file."""
        engine = AutomationEngine(config_path=config_path)
        
        strategy_data = {
            "id": "test_json_strategy",
            "name": "JSON Test Strategy",
            "timeframe": "3 months",
            "budget": 5000.0,
            "goals": {"leads": 150},
            "channels": ["google_ads", "linkedin_ads"],
            "execution_plan": {"week_1": "Launch"},
            "created_at": datetime.now().isoformat()
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(strategy_data, f)
            temp_path = Path(f.name)
        
        try:
            strategy = engine.load_strategy(temp_path)
            assert strategy.id == strategy_data["id"]
            assert strategy.name == strategy_data["name"]
            assert strategy.budget == strategy_data["budget"]
            assert strategy.id in engine.strategies
        finally:
            temp_path.unlink()
    
    def test_load_strategy_from_markdown(self, config_path):
        """Test loading strategy from markdown file."""
        engine = AutomationEngine(config_path=config_path)
        
        markdown_content = """# Marketing Strategy

**Timeframe:** 3 months
**Budget:** $5,000/month
**Goal:** Leads & Sales

## Channels
- Google Ads
- LinkedIn Ads
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(markdown_content)
            temp_path = Path(f.name)
        
        try:
            strategy = engine.load_strategy(temp_path)
            assert strategy is not None
            assert strategy.id in engine.strategies
            # Markdown parsing may not extract all fields perfectly, but should not crash
        finally:
            temp_path.unlink()
    
    @pytest.mark.asyncio
    async def test_execute_strategy_basic(self, config_path, sample_strategy_data):
        """Test executing a strategy."""
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
        
        result = await engine.execute_strategy(strategy.id)
        
        assert isinstance(result, dict)
        assert result["strategy_id"] == strategy.id
        assert "status" in result
        assert "campaigns_created" in result
        assert "budget_allocated" in result
    
    def test_optimize_campaigns(self, config_path, sample_strategy_data):
        """Test campaign optimization."""
        engine = AutomationEngine(config_path=config_path)
        
        # Create a strategy with campaigns
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
        
        result = engine.optimize_campaigns(strategy_id=strategy.id)
        
        assert isinstance(result, dict)
        assert "strategy_id" in result or "optimizations" in result
    
    def test_get_performance_report(self, config_path):
        """Test getting performance report."""
        engine = AutomationEngine(config_path=config_path)
        
        report = engine.get_performance_report()
        
        assert isinstance(report, dict)
        assert "report_type" in report
        assert "timestamp" in report

