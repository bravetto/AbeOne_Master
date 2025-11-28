"""
Marketing Automation Orbit API
FastAPI REST API for marketing automation system.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

from ..main import MarketingAutomationOrbit
from ..engine.automation_engine import Strategy, Campaign

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Marketing Automation Orbit API",
    description="Programmatic marketing automation system API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orbit system
orbit = MarketingAutomationOrbit()


@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    orbit.initialize()
    orbit.start_scheduler()
    logger.info("Marketing Automation Orbit API started")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    orbit.stop_scheduler()
    logger.info("Marketing Automation Orbit API stopped")


# Request/Response Models
class StrategyRequest(BaseModel):
    """Strategy execution request."""
    strategy_path: str
    execute: bool = True


class CampaignRequest(BaseModel):
    """Campaign creation request."""
    name: str
    channel: str
    budget: float
    start_date: str
    target_audience: Dict[str, Any]
    creatives: List[Dict[str, Any]]


class OptimizationRequest(BaseModel):
    """Optimization request."""
    strategy_id: Optional[str] = None


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Marketing Automation Orbit API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/api/status")
async def get_status():
    """Get system status."""
    return orbit.get_status()


@app.post("/api/strategies/execute")
async def execute_strategy(request: StrategyRequest, background_tasks: BackgroundTasks):
    """Execute a marketing strategy."""
    try:
        strategy_path = Path(request.strategy_path)
        
        if not strategy_path.exists():
            raise HTTPException(status_code=404, detail="Strategy file not found")
        
        if request.execute:
            result = await orbit.execute_strategy_from_file(strategy_path)
            return {
                "success": True,
                "result": result
            }
        else:
            # Just load strategy
            strategy = orbit.engine.load_strategy(strategy_path)
            return {
                "success": True,
                "strategy": strategy.to_dict()
            }
            
    except Exception as e:
        logger.error(f"Error executing strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/strategies")
async def list_strategies():
    """List all loaded strategies."""
    strategies = [
        strategy.to_dict()
        for strategy in orbit.engine.strategies.values()
    ]
    return {
        "strategies": strategies,
        "count": len(strategies)
    }


@app.get("/api/campaigns")
async def list_campaigns():
    """List all campaigns."""
    campaigns = [
        campaign.to_dict()
        for campaign in orbit.engine.campaigns.values()
    ]
    return {
        "campaigns": campaigns,
        "count": len(campaigns)
    }


@app.post("/api/campaigns")
async def create_campaign(request: CampaignRequest):
    """Create a new campaign."""
    try:
        from datetime import datetime
        from ..engine.automation_engine import CampaignStatus
        
        campaign = Campaign(
            id=f"campaign_{datetime.now().timestamp()}",
            name=request.name,
            channel=request.channel,
            status=CampaignStatus.DRAFT,
            budget=request.budget,
            start_date=datetime.fromisoformat(request.start_date),
            end_date=None,
            target_audience=request.target_audience,
            creatives=request.creatives
        )
        
        orbit.engine.campaigns[campaign.id] = campaign
        
        # Publish event
        orbit.bus_adapter.publish(
            "marketing.campaign.created",
            {"campaign": campaign.to_dict()}
        )
        
        return {
            "success": True,
            "campaign": campaign.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Error creating campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/optimize")
async def optimize_campaigns(request: OptimizationRequest):
    """Optimize campaigns."""
    try:
        results = orbit.engine.optimize_campaigns(request.strategy_id)
        
        # Publish event
        orbit.bus_adapter.publish(
            "marketing.optimization.triggered",
            {"results": results}
        )
        
        return {
            "success": True,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error optimizing campaigns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reports/performance")
async def get_performance_report(strategy_id: Optional[str] = None):
    """Get performance report."""
    try:
        report = orbit.engine.get_performance_report(strategy_id)
        return {
            "success": True,
            "report": report
        }
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/guardians/status")
async def get_guardian_status():
    """Get guardian system status."""
    return orbit.guardian_adapter.get_guardian_status()


@app.post("/api/guardians/validate")
async def validate_with_guardians(data: Dict[str, Any], frequency: Optional[int] = None):
    """Validate data with guardian system."""
    result = orbit.guardian_adapter.validate_with_guardians(data, frequency)
    return {
        "success": True,
        "validation": result
    }

