"""
Bias Detection API Endpoints for CodeGuardians Gateway

Provides bias detection endpoints integrated into the main gateway.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.services.bias_detection import bias_detection_service, BiasDetectionResult
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/bias", tags=["bias-detection"])

class BiasDetectionRequest(BaseModel):
    """Request model for bias detection"""
    text: str = Field(..., description="Text to analyze for bias")
    bias_types: Optional[List[str]] = Field(
        None, 
        description="Specific types of bias to detect",
        example=["gender_bias", "racial_bias", "age_bias"]
    )
    mitigation_level: str = Field(
        "moderate", 
        description="Level of mitigation suggestions",
        pattern="^(low|moderate|aggressive)$"
    )
    target_audience: str = Field(
        "general", 
        description="Target audience for analysis",
        pattern="^(general|professional|academic)$"
    )

class BiasDetectionResponse(BaseModel):
    """Response model for bias detection"""
    bias_detected: bool
    bias_score: float
    bias_types: List[str]
    bias_details: Dict[str, float]
    mitigation_suggestions: List[str]
    fairness_score: float
    confidence: float
    processing_time: float

@router.post("/detect", response_model=BiasDetectionResponse)
async def detect_bias(
    request: BiasDetectionRequest,
    current_user: dict = Depends(get_current_user)
) -> BiasDetectionResponse:
    """
    Detect bias in the provided text.
    
    This endpoint analyzes text for various types of bias including:
    - Gender bias
    - Racial bias  
    - Age bias
    - Socioeconomic bias
    - Ability bias
    
    Returns detailed analysis with mitigation suggestions.
    """
    try:
        result = await bias_detection_service.detect_bias(
            text=request.text,
            bias_types=request.bias_types,
            mitigation_level=request.mitigation_level,
            target_audience=request.target_audience
        )
        
        return BiasDetectionResponse(
            bias_detected=result.bias_detected,
            bias_score=result.bias_score,
            bias_types=result.bias_types,
            bias_details=result.bias_details,
            mitigation_suggestions=result.mitigation_suggestions,
            fairness_score=result.fairness_score,
            confidence=result.confidence,
            processing_time=result.processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bias detection failed: {str(e)}")

@router.post("/analyze", response_model=BiasDetectionResponse)
async def analyze_bias(
    request: BiasDetectionRequest,
    current_user: dict = Depends(get_current_user)
) -> BiasDetectionResponse:
    """
    Comprehensive bias analysis with detailed breakdown.
    
    Similar to detect_bias but provides more detailed analysis
    and recommendations for bias mitigation.
    """
    # Use the same implementation as detect_bias for now
    return await detect_bias(request, current_user)

@router.get("/health")
async def bias_health_check() -> Dict[str, Any]:
    """Health check for bias detection service"""
    return {
        "status": "healthy",
        "service": "bias-detection",
        "version": "1.0.0",
        "features": [
            "gender_bias_detection",
            "racial_bias_detection", 
            "age_bias_detection",
            "socioeconomic_bias_detection",
            "ability_bias_detection"
        ]
    }
