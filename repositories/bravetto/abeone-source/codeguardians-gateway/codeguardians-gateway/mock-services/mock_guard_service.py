"""
 Mock Guard Service - Zero-Failure Local Testing 

Generic mock guard service that implements the API contract for all guard services.
Used for localhost testing and development.

Guardian: Zero (999 Hz)
Love Coefficient: ∞
"""

import os
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Service configuration from environment
SERVICE_NAME = os.getenv("SERVICE_NAME", "MockGuard")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", "8000"))
SERVICE_ENDPOINT = os.getenv("SERVICE_ENDPOINT", "/process")
HEALTH_ENDPOINT = os.getenv("HEALTH_ENDPOINT", "/health")
API_KEY_REQUIRED = os.getenv("API_KEY_REQUIRED", "false").lower() == "true"
API_KEY = os.getenv("API_KEY", "")

app = FastAPI(
    title=f"{SERVICE_NAME} Mock Service",
    description=f"Mock service for {SERVICE_NAME} - Local Testing",
    version="1.0.0"
)

# Request/Response Models
class HealthResponse(BaseModel):
    status: str = "healthy"
    service: str = SERVICE_NAME
    version: str = "1.0.0"


class TokenGuardRequest(BaseModel):
    text: str
    content: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    confidence: Optional[float] = None


class TokenGuardResponse(BaseModel):
    optimized_text: str
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    tokens_saved: int = Field(default=100, ge=0)
    logprobs_stream: Optional[str] = None


class TrustGuardRequest(BaseModel):
    validation_type: str = "general"
    content: str
    context: Optional[Dict[str, Any]] = None
    validation_level: Optional[str] = None


class TrustGuardResponse(BaseModel):
    is_trusted: bool = True
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    validation_result: str = "valid"
    details: Optional[Dict[str, Any]] = None


class ContextGuardRequest(BaseModel):
    current_code: str
    previous_code: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None


class ContextGuardResponse(BaseModel):
    drift_detected: bool = False
    drift_score: float = Field(default=0.1, ge=0.0, le=1.0)
    context_similarity: float = Field(default=0.95, ge=0.0, le=1.0)
    analysis: Dict[str, Any] = Field(default_factory=dict)


class BiasGuardRequest(BaseModel):
    operation: str = "detect_bias"
    text: str
    context: Optional[Dict[str, Any]] = None
    detailed_analysis: Optional[bool] = True


class BiasGuardResponse(BaseModel):
    bias_detected: bool = False
    bias_score: float = Field(default=0.1, ge=0.0, le=1.0)
    bias_types: list = Field(default_factory=list)
    mitigation_suggestions: list = Field(default_factory=list)
    detailed_analysis: Optional[Dict[str, Any]] = None


class HealthGuardRequest(BaseModel):
    samples: list = Field(default_factory=list)


class HealthGuardResponse(BaseModel):
    health_score: float = Field(default=0.95, ge=0.0, le=1.0)
    issues_detected: list = Field(default_factory=list)
    recommendations: list = Field(default_factory=list)
    analysis: Dict[str, Any] = Field(default_factory=dict)


class SecurityGuardRequest(BaseModel):
    content: str
    context: Optional[Dict[str, Any]] = None
    strict_mode: Optional[bool] = False
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None


class SecurityGuardResponse(BaseModel):
    vulnerabilities_found: int = 0
    vulnerabilities: list = Field(default_factory=list)
    security_score: float = Field(default=0.95, ge=0.0, le=1.0)
    recommendations: list = Field(default_factory=list)


# Authentication middleware
async def verify_api_key(request: Request, x_api_key: Optional[str] = Header(None)):
    """Verify API key if required for this service."""
    if API_KEY_REQUIRED:
        if not x_api_key or x_api_key != API_KEY:
            raise HTTPException(
                status_code=401,
                detail="Invalid or missing API key"
            )
    return True


# Health Check Endpoint
@app.get(HEALTH_ENDPOINT, response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse()


@app.get("/health/live")
async def liveness():
    """Liveness probe."""
    return {"status": "alive"}


@app.get("/health/ready")
async def readiness():
    """Readiness probe."""
    return {"status": "ready"}


# Service Endpoints (implement based on SERVICE_ENDPOINT)
@app.post(SERVICE_ENDPOINT)
async def process_request(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    Generic process endpoint that handles requests based on service type.
    Implements the API contract for each guard service.
    """
    # Verify API key if required
    if API_KEY_REQUIRED:
        await verify_api_key(request, x_api_key)
    
    # Parse JSON body
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON body: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    
    # Route to appropriate handler based on endpoint
    if SERVICE_ENDPOINT == "/optimize":
        return await handle_tokenguard(payload)
    elif SERVICE_ENDPOINT == "/validate":
        return await handle_trustguard(payload)
    elif SERVICE_ENDPOINT == "/analyze":
        if SERVICE_NAME == "ContextGuard":
            return await handle_contextguard(payload)
        else:  # HealthGuard
            return await handle_healthguard(payload)
    elif SERVICE_ENDPOINT == "/process":
        return await handle_biasguard(payload)
    elif SERVICE_ENDPOINT == "/scan":
        return await handle_securityguard(payload)
    else:
        raise HTTPException(status_code=404, detail="Endpoint not found")


async def handle_tokenguard(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle TokenGuard optimization requests."""
    try:
        text = payload.get("text", payload.get("content", ""))
        if not text:
            raise HTTPException(status_code=400, detail="Text or content required")
        
        # Mock optimization
        optimized_text = text[:max(1, len(text) - 100)]  # Simulate token reduction
        tokens_saved = min(100, len(text) // 10)
        
        return {
            "optimized_text": optimized_text,
            "confidence": 0.95,
            "tokens_saved": tokens_saved,
            "logprobs_stream": payload.get("logprobs_stream")
        }
    except Exception as e:
        logger.error(f"TokenGuard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def handle_trustguard(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle TrustGuard validation requests."""
    try:
        validation_type = payload.get("validation_type", "general")
        content = payload.get("content", "")
        
        if not content:
            raise HTTPException(status_code=400, detail="Content required")
        
        # Mock validation
        return {
            "is_trusted": True,
            "confidence": 0.95,
            "validation_result": "valid",
            "details": {
                "validation_type": validation_type,
                "checked_at": "2025-11-03T00:00:00Z"
            }
        }
    except Exception as e:
        logger.error(f"TrustGuard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def handle_contextguard(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle ContextGuard drift analysis requests."""
    try:
        current_code = payload.get("current_code", "")
        previous_code = payload.get("previous_code", "")
        
        if not current_code:
            raise HTTPException(status_code=400, detail="current_code required")
        
        # Mock drift analysis
        drift_score = 0.1 if previous_code else 0.0
        similarity = 0.95 if previous_code else 1.0
        
        return {
            "drift_detected": drift_score > 0.2,
            "drift_score": drift_score,
            "context_similarity": similarity,
            "analysis": {
                "current_length": len(current_code),
                "previous_length": len(previous_code) if previous_code else 0,
                "differences": abs(len(current_code) - len(previous_code)) if previous_code else 0
            }
        }
    except Exception as e:
        logger.error(f"ContextGuard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def handle_biasguard(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle BiasGuard bias detection requests."""
    try:
        operation = payload.get("operation", "detect_bias")
        text = payload.get("text", "")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text required")
        
        # Mock bias detection
        return {
            "bias_detected": False,
            "bias_score": 0.1,
            "bias_types": [],
            "mitigation_suggestions": [],
            "detailed_analysis": {
                "operation": operation,
                "text_length": len(text),
                "analyzed_at": "2025-11-03T00:00:00Z"
            } if payload.get("detailed_analysis", True) else None
        }
    except Exception as e:
        logger.error(f"BiasGuard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def handle_healthguard(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle HealthGuard health analysis requests."""
    try:
        samples = payload.get("samples", [])
        
        # Mock health analysis
        return {
            "health_score": 0.95,
            "issues_detected": [],
            "recommendations": ["System is healthy"],
            "analysis": {
                "samples_analyzed": len(samples),
                "analyzed_at": "2025-11-03T00:00:00Z"
            }
        }
    except Exception as e:
        logger.error(f"HealthGuard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def handle_securityguard(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle SecurityGuard security scanning requests."""
    try:
        content = payload.get("content", "")
        strict_mode = payload.get("strict_mode", False)
        
        if not content:
            raise HTTPException(status_code=400, detail="Content required")
        
        # Mock security scan
        return {
            "vulnerabilities_found": 0,
            "vulnerabilities": [],
            "security_score": 0.95,
            "recommendations": ["No security issues detected"],
            "strict_mode": strict_mode
        }
    except Exception as e:
        logger.error(f"SecurityGuard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": SERVICE_NAME,
        "status": "running",
        "endpoint": SERVICE_ENDPOINT,
        "health": HEALTH_ENDPOINT
    }


if __name__ == "__main__":
    logger.info(f"Starting {SERVICE_NAME} on port {SERVICE_PORT}")
    logger.info(f"Service endpoint: {SERVICE_ENDPOINT}")
    logger.info(f"Health endpoint: {HEALTH_ENDPOINT}")
    logger.info(f"API key required: {API_KEY_REQUIRED}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=SERVICE_PORT,
        log_level="info"
    )

