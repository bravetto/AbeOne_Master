"""
A/B Testing API Endpoints

RESTful API for managing A/B test experiments including:
- Experiment CRUD operations
- User assignment and tracking
- Statistical analysis
- Real-time monitoring
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid
import logging
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import User
from app.api.dependencies import get_current_user, require_permissions
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Main router with prefix for new API structure
router = APIRouter(prefix="/api/v1/ab-testing", tags=["A/B Testing"])

# Backward compatibility router without prefix for tests
legacy_router = APIRouter(tags=["A/B Testing (Legacy)"])

# Lazy initialization to avoid numpy import issues
_segmentation_engine = None
_statistical_analyzer = None
_redis_client = None

def _get_segmentation_engine():
    """Lazy initialization of segmentation engine."""
    global _segmentation_engine
    if _segmentation_engine is None:
        try:
            import redis
            from app.core.ab_testing.segmentation import UserSegmentationEngine
            
            _redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                REPLACE_ME
                decode_responses=True
            )
            _segmentation_engine = UserSegmentationEngine(_redis_client)
        except Exception as e:
            logger.warning(f"Could not initialize segmentation engine: {e}")
            _segmentation_engine = None
    return _segmentation_engine

def _get_statistical_analyzer():
    """Lazy initialization of statistical analyzer."""
    global _statistical_analyzer
    if _statistical_analyzer is None:
        try:
            from app.core.ab_testing.statistical_analysis import StatisticalAnalyzer
            _statistical_analyzer = StatisticalAnalyzer()
        except Exception as e:
            logger.warning(f"Could not initialize statistical analyzer: {e}")
            _statistical_analyzer = None
    return _statistical_analyzer

# Request/Response Models
from pydantic import BaseModel, Field

class ExperimentCreateRequest(BaseModel):
    name: str = Field(..., description="Experiment name")
    description: str = Field(..., description="Experiment description")
    traffic_split: Dict[str, float] = Field(..., description="Traffic distribution")
    success_metrics: List[str] = Field(..., description="Success metrics to track")
    minimum_sample_size: int = Field(1000, description="Minimum sample size")
    confidence_level: float = Field(0.95, description="Confidence level")
    power: float = Field(0.8, description="Statistical power")
    primary_metric: str = Field(..., description="Primary metric")
    secondary_metrics: List[str] = Field(default_factory=list, description="Secondary metrics")
    target_audience: Dict[str, Any] = Field(default_factory=dict, description="Target audience criteria")
    exclusion_criteria: List[str] = Field(default_factory=list, description="Exclusion criteria")
    duration_days: int = Field(7, description="Experiment duration in days")

class VariantCreateRequest(BaseModel):
    name: str = Field(..., description="Variant name")
    variant_type: str = Field(..., description="Variant type")
    traffic_percentage: float = Field(..., description="Traffic percentage")
    configuration: Dict[str, Any] = Field(..., description="Variant configuration")

class ExperimentUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    traffic_split: Optional[Dict[str, float]] = None
    target_audience: Optional[Dict[str, Any]] = None
    exclusion_criteria: Optional[List[str]] = None

class ExperimentResultRequest(BaseModel):
    experiment_id: str = Field(..., description="Experiment ID")
    variant_name: str = Field(..., description="Variant name")
    session_id: str = Field(..., description="Session ID")
    metrics: Dict[str, float] = Field(..., description="Metrics to record")
    result_metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class UserAssignmentRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    experiment_id: str = Field(..., description="Experiment ID")
    user_attributes: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User attributes")

# Helper function for lazy imports
def _get_ab_testing_models():
    """Lazy import ab_testing models to avoid startup issues."""
    from app.core.ab_testing.models import (
        ExperimentConfig, VariantConfig, ExperimentResult, 
        ExperimentStatus, VariantType, StatisticalAnalysis
    )
    return {
        'ExperimentConfig': ExperimentConfig,
        'VariantConfig': VariantConfig,
        'ExperimentResult': ExperimentResult,
        'ExperimentStatus': ExperimentStatus,
        'VariantType': VariantType,
        'StatisticalAnalysis': StatisticalAnalysis
    }

def _get_traffic_splitter():
    """Lazy import TrafficSplitter."""
    from app.core.ab_testing.segmentation import TrafficSplitter
    return TrafficSplitter

# Experiment Management Endpoints

@router.post("/experiments")
@legacy_router.post("/experiments")
async def create_experiment(
    request: ExperimentCreateRequest,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:create"])),
    db: Session = Depends(get_db)
):
    """Create a new A/B test experiment."""
    try:
        models = _get_ab_testing_models()
        TrafficSplitter = _get_traffic_splitter()
        
        # Validate traffic split
        if not TrafficSplitter.validate_traffic_split(request.traffic_split):
            raise HTTPException(
                status_code=400, 
                detail="Traffic split must sum to 100%"
            )
        
        # Generate experiment ID
        experiment_id = str(uuid.uuid4())
        
        # Create experiment configuration
        experiment_config = models['ExperimentConfig'](
            experiment_id=experiment_id,
            name=request.name,
            description=request.description,
            status=models['ExperimentStatus'].DRAFT,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=request.duration_days),
            traffic_split=request.traffic_split,
            success_metrics=request.success_metrics,
            minimum_sample_size=request.minimum_sample_size,
            confidence_level=request.confidence_level,
            power=request.power,
            primary_metric=request.primary_metric,
            secondary_metrics=request.secondary_metrics,
            target_audience=request.target_audience,
            exclusion_criteria=request.exclusion_criteria,
            created_by=current_user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # TODO: Store in database
        # For now, just return success
        
        logger.info(f"Created experiment {experiment_id} by user {current_user.id}")
        
        return {
            "experiment_id": experiment_id,
            "status": "created",
            "message": "Experiment created successfully",
            "experiment": experiment_config.__dict__
        }
        
    except Exception as e:
        logger.error(f"Error creating experiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/experiments")
@legacy_router.get("/experiments")
async def list_experiments(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:read"])),
    db: Session = Depends(get_db)
):
    """List A/B test experiments."""
    try:
        # TODO: Implement database query
        # For now, return empty list
        
        experiments = []
        
        return {
            "experiments": experiments,
            "total": len(experiments)
        }
        
    except Exception as e:
        logger.error(f"Error listing experiments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/experiments/{experiment_id}")
@legacy_router.get("/experiments/{experiment_id}")
async def get_experiment(
    experiment_id: str,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:read"])),
    db: Session = Depends(get_db)
):
    """Get experiment details."""
    try:
        # TODO: Implement database query
        # For now, return not found
        
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting experiment {experiment_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/experiments/{experiment_id}")
@legacy_router.put("/experiments/{experiment_id}")
async def update_experiment(
    experiment_id: str,
    request: ExperimentUpdateRequest,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:update"])),
    db: Session = Depends(get_db)
):
    """Update experiment configuration."""
    try:
        # TODO: Implement database update
        # For now, return not found
        
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating experiment {experiment_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/experiments/{experiment_id}/start")
@legacy_router.post("/experiments/{experiment_id}/start")
async def start_experiment(
    experiment_id: str,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:update"])),
    db: Session = Depends(get_db)
):
    """Start an A/B test experiment."""
    try:
        # TODO: Implement experiment start logic
        # For now, return not found
        
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting experiment {experiment_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/experiments/{experiment_id}/stop")
@legacy_router.post("/experiments/{experiment_id}/stop")
async def stop_experiment(
    experiment_id: str,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:update"])),
    db: Session = Depends(get_db)
):
    """Stop an A/B test experiment."""
    try:
        # TODO: Implement experiment stop logic
        # For now, return not found
        
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error stopping experiment {experiment_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# User Assignment Endpoints

@router.post("/assign-user")
async def assign_user_to_experiment(
    request: UserAssignmentRequest,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["user", "experiment:participate"])),
    db: Session = Depends(get_db)
):
    """Assign user to experiment variant."""
    try:
        segmentation_engine = _get_segmentation_engine()
        if not segmentation_engine:
            raise HTTPException(status_code=503, detail="Segmentation engine not available")
        
        # Assign user to variant
        variant = segmentation_engine.assign_user_to_variant(
            user_id=request.user_id,
            experiment_id=request.experiment_id,
            user_attributes=request.user_attributes
        )
        
        if variant:
            return {
                "user_id": request.user_id,
                "experiment_id": request.experiment_id,
                "variant": variant,
                "assigned_at": datetime.utcnow().isoformat()
            }
        else:
            return {
                "user_id": request.user_id,
                "experiment_id": request.experiment_id,
                "variant": None,
                "reason": "User excluded or experiment not active"
            }
        
    except Exception as e:
        logger.error(f"Error assigning user to experiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}/variants")
async def get_user_variants(
    user_id: str,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["user", "experiment:read"])),
    db: Session = Depends(get_db)
):
    """Get all active variant assignments for a user."""
    try:
        segmentation_engine = _get_segmentation_engine()
        if not segmentation_engine:
            raise HTTPException(status_code=503, detail="Segmentation engine not available")
        
        variants = segmentation_engine.get_user_variants(user_id)
        
        return {
            "user_id": user_id,
            "variants": variants,
            "total": len(variants)
        }
        
    except Exception as e:
        logger.error(f"Error getting user variants: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Result Tracking Endpoints

@router.post("/results")
async def record_experiment_result(
    request: ExperimentResultRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["user", "experiment:participate"])),
    db: Session = Depends(get_db)
):
    """Record experiment result."""
    try:
        models = _get_ab_testing_models()
        
        # Create result record
        result = models['ExperimentResult'](
            experiment_id=request.experiment_id,
            variant_name=request.variant_name,
            user_id=current_user.id,
            session_id=request.session_id,
            timestamp=datetime.utcnow(),
            metrics=request.metrics,
            result_metadata=request.result_metadata
        )
        
        # TODO: Store in database
        # For now, just log
        
        logger.info(f"Recorded result for experiment {request.experiment_id}, variant {request.variant_name}")
        
        # Trigger background analysis if needed
        background_tasks.add_task(
            _trigger_analysis_if_needed,
            request.experiment_id
        )
        
        return {
            "status": "recorded",
            "message": "Result recorded successfully",
            "result_id": str(uuid.uuid4())
        }
        
    except Exception as e:
        logger.error(f"Error recording experiment result: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Analysis Endpoints

@router.get("/experiments/{experiment_id}/analysis")
@legacy_router.get("/experiments/{experiment_id}/analysis")
async def get_experiment_analysis(
    experiment_id: str,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:read"])),
    db: Session = Depends(get_db)
):
    """Get statistical analysis for experiment."""
    try:
        # TODO: Implement analysis retrieval
        # For now, return not found
        
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting experiment analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/experiments/{experiment_id}/analyze")
@legacy_router.post("/experiments/{experiment_id}/analyze")
async def analyze_experiment(
    experiment_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:analyze"])),
    db: Session = Depends(get_db)
):
    """Trigger statistical analysis for experiment."""
    try:
        # Add background task for analysis
        background_tasks.add_task(
            _perform_experiment_analysis,
            experiment_id,
            current_user.id
        )
        
        return {
            "status": "analysis_started",
            "message": "Statistical analysis started",
            "experiment_id": experiment_id
        }
        
    except Exception as e:
        logger.error(f"Error starting experiment analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Monitoring Endpoints

@router.get("/experiments/{experiment_id}/metrics")
@legacy_router.get("/experiments/{experiment_id}/metrics")
async def get_experiment_metrics(
    experiment_id: str,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:read"])),
    db: Session = Depends(get_db)
):
    """Get real-time experiment metrics."""
    try:
        # TODO: Implement metrics retrieval
        # For now, return not found
        
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting experiment metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/experiments/{experiment_id}/status")
@legacy_router.get("/experiments/{experiment_id}/status")
async def get_experiment_status(
    experiment_id: str,
    current_user: User = Depends(get_current_user),
    _: None = Depends(require_permissions(["admin", "experiment:read"])),
    db: Session = Depends(get_db)
):
    """Get experiment status and health."""
    try:
        # TODO: Implement status retrieval
        # For now, return not found
        
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting experiment status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background Tasks

async def _trigger_analysis_if_needed(experiment_id: str):
    """Trigger analysis if experiment has enough data."""
    try:
        # TODO: Implement analysis triggering logic
        logger.info(f"Checking if analysis needed for experiment {experiment_id}")
    except Exception as e:
        logger.error(f"Error triggering analysis: {e}")

async def _perform_experiment_analysis(experiment_id: str, user_id: str):
    """Perform statistical analysis for experiment."""
    try:
        # TODO: Implement analysis logic
        logger.info(f"Performing analysis for experiment {experiment_id} by user {user_id}")
    except Exception as e:
        logger.error(f"Error performing experiment analysis: {e}")
