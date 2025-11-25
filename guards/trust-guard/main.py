"""
Trust Guard Service - AI Reliability Solution

FastAPI-based microservice for detecting and mitigating seven AI failure patterns:
- Hallucination, Drift, Bias, Deception, Security Theater, Duplication, Stub Syndrome
"""

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, Depends, Header
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
import asyncio
import time
import psutil
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from trustguard.core import TrustGuardDetector
from trustguard.validation import ValidationEngine
from trustguard.constitutional import ConstitutionalPrompting
from trustguard.metrics import ReliabilityMetrics
from trustguard.config import get_config
from trustguard.logging import setup_logging
from trustguard.auth import get_security_manager, Permission, AuthenticationError, AuthorizationError, Role, ROLE_PERMISSIONS
from trustguard.security import SecurityHeadersMiddleware, InputSanitizationMiddleware, get_security_manager as get_security_mgr
from trustguard.observability import get_observability_manager, trace_operation, record_request, record_pattern_detection, record_validation, record_mitigation
from trustguard.health import get_health_checker, HealthStatus
from trustguard.tracer import get_tracer_manager, trace_operation, fire_bullet, trace_api_request, end_trace

# Setup configuration and logging
config = get_config()
logger = setup_logging()

# Initialize core components
detector = TrustGuardDetector()
validator = ValidationEngine()
constitutional = ConstitutionalPrompting()
metrics = ReliabilityMetrics()

# Initialize security components
auth_manager = get_security_manager()
security_manager = get_security_mgr()

# Initialize observability
observability_manager = get_observability_manager()

# Initialize health checker
health_checker = get_health_checker()

# Initialize tracer manager
tracer_manager = get_tracer_manager()

# Rate limiting
limiter = Limiter(key_func=get_remote_address, default_limits=[f"{config.rate_limit}/minute"])

# System metrics cache for performance optimization
_system_metrics_cache = {
    "last_update": 0,
    "cache_duration": 5,  # seconds
    "data": {}
}

def get_cached_system_metrics():
    """Get cached system metrics to avoid repeated psutil calls."""
    current_time = time.time()
    
    # Check if cache is still valid
    if current_time - _system_metrics_cache["last_update"] < _system_metrics_cache["cache_duration"]:
        return _system_metrics_cache["data"]
    
    # Update cache
    try:
        memory_info = psutil.virtual_memory()
        _system_metrics_cache["data"] = {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": memory_info.percent,
            "memory_used_mb": memory_info.used / 1024 / 1024,
            "memory_available_mb": memory_info.available / 1024 / 1024,
            "disk_usage": psutil.disk_usage('/').percent
        }
        _system_metrics_cache["last_update"] = current_time
    except Exception as e:
        logger.warning(f"Failed to update system metrics cache: {e}")
        # Return default values if psutil fails
        _system_metrics_cache["data"] = {
            "cpu_percent": 0,
            "memory_percent": 0,
            "memory_used_mb": 0,
            "memory_available_mb": 0,
            "disk_usage": 0
        }
    
    return _system_metrics_cache["data"]

app = FastAPI(
    title="Trust Guard - AI Reliability Solution",
    description="Detects and mitigates seven AI failure patterns: hallucination, drift, bias, deception, security theater, duplication, and stub syndrome",
    version="1.0.0",
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add security middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(InputSanitizationMiddleware)

# CORS middleware
if config.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Metrics instrumentation
if config.enable_metrics:
    instrumentator = Instrumentator().instrument(app).expose(app)

# OpenTelemetry instrumentation
observability_manager.instrument_fastapi(app)


# Authentication dependency
async def get_current_user(
    request: Request,
    api_key: Optional[str] = Header(None, alias="X-API-Key"),
    authorization: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """Get current authenticated user."""
    try:
        # Allow service-to-service requests from gateway (bypass auth for internal requests)
        # This enables the gateway to communicate with TrustGuard without requiring API keys
        gateway_request = request.headers.get("X-Gateway-Request", "").lower() == "true"
        if gateway_request:
            # Create a service user with SERVICE role permissions
            # SERVICE role has DETECT, VALIDATE, and HEALTH permissions (see ROLE_PERMISSIONS)
            logger.debug("Gateway service-to-service request detected, authenticating as SERVICE role")
            return {
                "user_id": "gateway-service",
                "role": Role.SERVICE,
                "auth_type": "service",
                "permissions": ROLE_PERMISSIONS[Role.SERVICE]
            }
        
        # Extract JWT token from Authorization header
        jwt_token = None
        if authorization and authorization.startswith("Bearer "):
            jwt_token = authorization[7:]
        
        # Authenticate user
        user_info = auth_manager.authenticate_request(api_key=api_key, jwt_token=jwt_token)
        
        # Debug logging for authentication
        if api_key:
            logger.debug(f"Authentication attempt with API key: {api_key[:20]}...")
            logger.debug(f"Authentication result: {bool(user_info)}")
        
        if not user_info:
            # Log failed authentication attempt
            client_ip = request.client.host if request.client else "unknown"
            try:
                security_manager.log_auth_event("authentication_failed", "anonymous", client_ip, False)
            except Exception as log_error:
                logger.warning(f"Failed to log auth event: {log_error}")
            
            raise HTTPException(
                status_code=401,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Log successful authentication
        client_ip = request.client.host if request.client else "unknown"
        try:
            security_manager.log_auth_event("authentication_success", user_info["user_id"], client_ip, True)
        except Exception as log_error:
            logger.warning(f"Failed to log auth success event: {log_error}")
        
        return user_info
        
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication required")


# Authorization dependency
def require_permission(permission: Permission):
    """Create a dependency that requires a specific permission."""
    async def permission_checker(user_info: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        if not user_info:
            raise HTTPException(
                status_code=401,
                detail="Authentication required"
            )
        if not auth_manager.authorize_request(user_info, permission):
            logger.warning(
                f"Permission denied: user {user_info.get('user_id', 'unknown')} "
                f"(role: {user_info.get('role', 'unknown')}) "
                f"attempted to access {permission.value} endpoint"
            )
            raise HTTPException(
                status_code=403,
                detail=f"Permission '{permission.value}' required"
            )
        return user_info
    return permission_checker


# Pydantic Models
class TextInput(BaseModel):
    """Input model for text analysis"""
    text: str = Field(..., min_length=1, description="The AI-generated text to analyze")
    context: Optional[str] = Field(None, description="Context information")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "The capital of France is Paris. This city has a population of 2.1 million.",
                "context": "Geography question about European capitals",
                "metadata": {"model": "gpt-4", "confidence": 0.85}
            }
        }
    }


class ValidationRequest(BaseModel):
    """Request model for comprehensive validation"""
    input_text: str = Field(..., description="Original input prompt")
    output_text: str = Field(..., description="AI-generated output to validate")
    context: Optional[str] = Field(None, description="Conversation context")
    expected_factors: Optional[List[str]] = Field(None, description="Expected validation factors")

    model_config = {
        "json_schema_extra": {
            "example": {
                "input_text": "What is the capital of France?",
                "output_text": "Paris is the capital of France with a population of 2.1 million people.",
                "context": "Geography quiz",
                "expected_factors": ["factual_accuracy", "context_relevance"]
            }
        }
    }


class MitigationRequest(BaseModel):
    """Request model for failure pattern mitigation"""
    text: str = Field(..., description="Text to mitigate")
    detected_patterns: List[str] = Field(..., description="Detected failure patterns")
    severity: str = Field("high", description="Mitigation severity level")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "The AI is now safe and secure with 100% trustworthiness.",
                "detected_patterns": ["security_theater", "deception"],
                "severity": "high"
            }
        }
    }


class ValidationResponse(BaseModel):
    """Comprehensive validation response"""
    overall_score: float = Field(..., description="Overall reliability score (0-100)")
    pattern_detections: Dict[str, float] = Field(..., description="Detection scores for each pattern")
    risk_level: str = Field(..., description="Risk assessment: low/medium/high")
    recommendations: List[str] = Field(..., description="Mitigation recommendations")
    evidence: Dict[str, Any] = Field(..., description="Supporting evidence and metrics")
    processing_time: float = Field(..., description="Processing time in milliseconds")

    model_config = {
        "json_schema_extra": {
            "example": {
                "overall_score": 78.5,
                "pattern_detections": {
                    "hallucination": 0.2,
                    "bias": 0.8,
                    "deception": 0.3
                },
                "risk_level": "medium",
                "recommendations": ["Apply constitutional prompting", "Cross-reference with Context Guard"],
                "evidence": {"kl_divergence": 0.15, "uncertainty_score": 0.3},
                "processing_time": 45.2
            }
        }
    }


class HealthResponse(BaseModel):
    """Health check response with Trust Guard metrics"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    components: Dict[str, bool] = Field(..., description="Component health status")
    metrics: Dict[str, Any] = Field(..., description="Current metrics")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with Trust Guard context."""
    start_time = time.time()

    # Extract request data for logging (safely)
    request_info = {
        "method": request.method,
        "url": str(request.url),
        "client_ip": get_remote_address(request),
    }

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    # Enhanced logging with Trust Guard metrics
    log_data = {
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "process_time_ms": round(process_time, 2),
        "client_ip": get_remote_address(request),
    }

    if config.log_level.upper() == "DEBUG":
        log_data["headers"] = dict(request.headers)

    logger.info("Request processed", extra=log_data)

    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Trust-Guard-Version"] = "1.0.0"

    return response


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Enhanced health check with Trust Guard component status."""
    try:
        # Get cached system metrics for performance
        system_metrics = get_cached_system_metrics()
        
        # Basic system health - optimized for speed
        health_data = {
            "status": "healthy",
            "version": "1.0.0",
            "components": {
                "detector": detector.is_healthy(),
                "validator": validator.is_healthy(),
                "constitutional": constitutional.is_healthy(),
                "metrics": True
            },
            "metrics": {
                "uptime_seconds": time.time() - psutil.Process().create_time(),
                "cpu_usage": system_metrics["cpu_percent"],
                "memory_mb": system_metrics["memory_used_mb"],
                "patterns_detected_today": metrics.get_patterns_detected_today(),
                "average_risk_score": metrics.get_average_risk_score()
            }
        }

        # Add memory usage details for Trust Guard components - from cache
        health_data["system_memory"] = {
            "used_mb": round(system_metrics["memory_used_mb"], 2),
            "available_mb": round(system_metrics["memory_available_mb"], 2),
            "percentage": system_metrics["memory_percent"]
        }

        status_code = 200
        if not all(health_data["components"].values()):
            health_data["status"] = "degraded"
            status_code = 206
            logger.warning("Trust Guard health check: degraded components", extra=health_data["components"])

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_data = {
            "status": "unhealthy",
            "version": "1.0.0",
            "components": {"error": f"{type(e).__name__}: {str(e)}"},
            "metrics": {}
        }
        status_code = 503

    logger.debug("Health check completed", extra={"status": health_data["status"]})

    return JSONResponse(status_code=status_code, content=health_data)


@app.get("/health/live")
async def liveness_probe():
    """Kubernetes liveness probe - checks if the service is alive."""
    # Simple liveness check - just return alive if we can respond
    return JSONResponse(status_code=200, content={"status": "alive"})


@app.get("/health/ready")
async def readiness_probe():
    """Kubernetes readiness probe - checks if the service is ready to serve traffic."""
    # Simple readiness check - just return ready if we can respond
    return JSONResponse(status_code=200, content={"status": "ready"})


@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with component-by-component analysis."""
    try:
        components = {
            "detector": detector,
            "validator": validator,
            "constitutional": constitutional,
            "metrics": metrics,
            "auth_manager": auth_manager
        }
        
        health_result = health_checker.perform_comprehensive_check(components)
        
        # Add additional detailed information
        health_result["service_info"] = {
            "name": "trust-guard",
            "version": "1.0.0",
            "environment": "production"
        }
        
        health_result["kubernetes"] = {
            "liveness_probe": "/health/live",
            "readiness_probe": "/health/ready",
            "startup_probe": "/health"
        }
        
        return JSONResponse(status_code=200, content=health_result)
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        error_response = {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
        return JSONResponse(status_code=503, content=error_response)


@app.get("/debug/api-key")
async def get_default_api_key():
    """Get the default API key for testing (DEBUG ONLY - REMOVE IN PRODUCTION)."""
    # This endpoint exposes the API key - use only for development/testing
    if hasattr(auth_manager.api_key_manager, 'default_api_key'):
        return {
            "api_key": auth_manager.api_key_manager.default_api_key,
            "note": "Use this key with X-API-Key header for testing"
        }
    else:
        return {"error": "Default API key not found"}


@app.post("/v1/test/detect", response_model=Dict[str, Any])
async def test_detect_patterns(text_input: TextInput):
    """
    Test endpoint for pattern detection without authentication (INTERNAL REVIEW ONLY).
    
    This endpoint bypasses authentication for internal review purposes.
    """
    start_time = time.time()
    
    try:
        logger.info("Test pattern detection request received",
                   extra={"text_length": len(text_input.text)})

        # Run detection on all seven patterns (non-blocking via thread executor)
        logger.debug("Starting test pattern detection in thread executor")
        detections = await asyncio.to_thread(
            detector.detect_all_patterns,
            text=text_input.text,
            context=text_input.context,
            metadata=text_input.metadata
        )
        logger.debug("Test pattern detection completed successfully")

        # Calculate overall risk assessment
        risk_assessment = validator.calculate_risk_assessment(detections)

        processing_time = (time.time() - start_time) * 1000

        result = {
            "detections": detections,
            "risk_assessment": risk_assessment,
            "processing_time_ms": round(processing_time, 2),
            "timestamp": time.time(),
            "note": "Test endpoint - authentication bypassed for internal review"
        }

        # Update metrics
        metrics.record_detection(result)

        logger.info("Test pattern detection completed",
                   extra={"processing_time": processing_time, "risk_level": risk_assessment["level"]})

        return result

    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        logger.error(f"Test pattern detection failed: {e}", extra={"processing_time": processing_time})
        raise HTTPException(status_code=500, detail=f"Test pattern detection failed: {str(e)}")


@app.post("/v1/detect", response_model=Dict[str, Any])
@limiter.limit(f"{config.rate_limit}/minute")
async def detect_patterns(
    request: Request, 
    text_input: TextInput,
    current_user: Dict[str, Any] = Depends(require_permission(Permission.DETECT))
):
    """
    Detect AI failure patterns in the provided text.

    Returns detailed analysis of all seven failure patterns with confidence scores.
    """
    start_time = time.time()
    
    # Start API trace
    trace_id = trace_api_request("/v1/detect", "POST", 
                                text_length=len(text_input.text),
                                user_id=current_user.get("user_id", "anonymous"))

    try:
        logger.info("Pattern detection request received",
                   extra={"text_length": len(text_input.text)})

        # TEMPORARY: Simplified to isolate the issue - removed all tracing/fire_bullet calls
        logger.info("Starting pattern detection in thread executor")

        # Run detection on all seven patterns (non-blocking via thread executor)
        detections = await asyncio.to_thread(
            detector.detect_all_patterns,
            text=text_input.text,
            context=text_input.context,
            metadata=text_input.metadata
        )
        logger.info("Pattern detection completed successfully, got results")

        # Calculate patterns detected (used for observability)
        patterns_detected_count = len([d for d in detections.values() if d.get("score", 0) > 0.5])
        logger.info(f"Patterns detected: {patterns_detected_count}")

        # Calculate overall risk assessment
        logger.info("Calculating risk assessment")
        risk_assessment = validator.calculate_risk_assessment(detections)
        logger.info("Risk assessment calculated")

        processing_time = (time.time() - start_time) * 1000
        logger.info(f"Processing time calculated: {processing_time}ms")

        result = {
            "detections": detections,
            "risk_assessment": risk_assessment,
            "processing_time_ms": round(processing_time, 2),
            "timestamp": time.time()
        }
        logger.info("Result dict created")
        
        # Record observability metrics (non-blocking via thread executor)
        loop = asyncio.get_running_loop()
        
        # Fire success bullet (non-blocking)
        loop.run_in_executor(
            None,
            lambda: fire_bullet(
                "api_request_success",
                "Pattern detection request completed successfully",
                endpoint="/v1/detect",
                method="POST",
                processing_time=processing_time,
                patterns_detected=patterns_detected_count,
                risk_level=risk_assessment["level"]
            )
        )
        
        # Record metrics (non-blocking)
        loop.run_in_executor(None, metrics.record_detection, result)
        
        # Record pattern detection observability (non-blocking)
        loop.run_in_executor(
            None,
            record_pattern_detection,
            patterns_detected_count,
            processing_time / 1000,
            len(text_input.text),
            current_user.get("user_id", "anonymous")
        )
        
        # End API trace (non-blocking) - ensures trace is properly completed
        loop.run_in_executor(
            None,
            lambda: end_trace(
                trace_id,
                True,  # success
                processing_time=processing_time,
                patterns_detected=patterns_detected_count,
                risk_level=risk_assessment["level"]
            )
        )

        logger.info("Pattern detection completed, returning result",
                   extra={"processing_time": processing_time, "risk_level": risk_assessment["level"]})

        return result

    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        
        # Record observability for error path (non-blocking via thread executor)
        loop = asyncio.get_running_loop()
        
        # Fire bullet for error (non-blocking)
        loop.run_in_executor(
            None,
            lambda: fire_bullet(
                "api_request_error",
                "Pattern detection request failed",
                endpoint="/v1/detect",
                method="POST",
                error=str(e),
                error_type=type(e).__name__,
                processing_time=processing_time
            )
        )
        
        # End API trace with error (non-blocking) - ensures trace is properly completed
        loop.run_in_executor(
            None,
            lambda: end_trace(
                trace_id,
                False,  # success
                error=str(e),
                error_type=type(e).__name__,
                processing_time=processing_time
            )
        )
        
        logger.error(f"Pattern detection failed: {e}", extra={"processing_time": processing_time})
        raise HTTPException(status_code=500, detail=f"Pattern detection failed: {str(e)}")


@app.post("/v1/validate", response_model=ValidationResponse)
@limiter.limit(f"{config.rate_limit}/minute")
async def validate_response(
    request: Request, 
    validation_request: ValidationRequest,
    current_user: Dict[str, Any] = Depends(require_permission(Permission.VALIDATE))
):
    """
    Comprehensive validation of AI response against seven failure patterns.

    Returns detailed reliability score and mitigation recommendations.
    """
    start_time = time.time()

    try:
        logger.info("Comprehensive validation request received",
                   extra={"input_length": len(validation_request.input_text), "output_length": len(validation_request.output_text)})

        # Step 1: Detect patterns in output (non-blocking via thread executor)
        pattern_detections = await asyncio.to_thread(
            detector.detect_all_patterns,
            text=validation_request.output_text,
            context=validation_request.context,
            metadata={"input_text": validation_request.input_text}
        )

        # Step 2: Mathematical validation (KL divergence, uncertainty, etc.)
        mathematical_scores = validator.perform_mathematical_validation(
            input_text=validation_request.input_text,
            output_text=validation_request.output_text,
            context=validation_request.context
        )

        # Step 3: Risk assessment and scoring
        risk_assessment = validator.calculate_risk_assessment(pattern_detections)

        # Step 4: Generate evidence-based scoring
        evidence = validator.generate_evidence(
            pattern_detections=pattern_detections,
            mathematical_scores=mathematical_scores,
            request=validation_request
        )

        # Step 5: Create mitigation recommendations
        recommendations = constitutional.generate_recommendations(
            pattern_detections=pattern_detections,
            risk_level=risk_assessment["level"],
            context=validation_request.context
        )

        processing_time = (time.time() - start_time) * 1000

        result = ValidationResponse(
            overall_score=risk_assessment["score"],
            pattern_detections={k: v["score"] for k, v in pattern_detections.items()},
            risk_level=risk_assessment["level"],
            recommendations=recommendations,
            evidence=evidence,
            processing_time=round(processing_time, 2)
        )

        # Update metrics
        metrics.record_validation({
            "score": result.overall_score,
            "risk_level": result.risk_level,
            "patterns_detected": len([p for p in result.pattern_detections.values() if p > 0.5]),
            "processing_time": processing_time
        })

        logger.info("Comprehensive validation completed",
                   extra={
                       "overall_score": result.overall_score,
                       "risk_level": result.risk_level,
                       "processing_time": processing_time
                   })

        return result

    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        logger.error(f"Comprehensive validation failed: {e}", extra={"processing_time": processing_time})
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@app.post("/v1/mitigate", response_model=Dict[str, Any])
@limiter.limit(f"{config.rate_limit}/minute")
async def mitigate_patterns(
    request: Request, 
    mitigation_request: MitigationRequest,
    current_user: Dict[str, Any] = Depends(require_permission(Permission.MITIGATE))
):
    """
    Apply constitutional prompting and mitigation strategies for detected failure patterns.

    Returns mitigated text with applied constitutional guidelines.
    """
    start_time = time.time()

    try:
        logger.info("Mitigation request received",
                   extra={"text_length": len(mitigation_request.text), "patterns": mitigation_request.detected_patterns})

        # Apply constitutional prompting and mitigation
        mitigated_result = constitutional.apply_mitigation(
            text=mitigation_request.text,
            detected_patterns=mitigation_request.detected_patterns,
            severity=mitigation_request.severity
        )

        processing_time = (time.time() - start_time) * 1000

        result = {
            "original_text": mitigation_request.text,
            "mitigated_text": mitigated_result["text"],
            "applied_techniques": mitigated_result["techniques"],
            "constitutional_prompts_used": mitigated_result["prompts_used"],
            "confidence_improvement": mitigated_result["confidence_improvement"],
            "processing_time_ms": round(processing_time, 2),
            "timestamp": time.time()
        }

        # Update metrics
        metrics.record_mitigation({
            "patterns_mitigated": len(mitigation_request.detected_patterns),
            "confidence_improvement": result["confidence_improvement"],
            "techniques_applied": len(result["applied_techniques"]),
            "processing_time": processing_time
        })

        logger.info("Mitigation completed",
                   extra={
                       "patterns_mitigated": len(mitigation_request.detected_patterns),
                       "confidence_improvement": result["confidence_improvement"],
                       "processing_time": processing_time
                   })

        return result

    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        logger.error(f"Mitigation failed: {e}", extra={"processing_time": processing_time})
        raise HTTPException(status_code=500, detail=f"Mitigation failed: {str(e)}")


@app.post("/v1/constitutional")
@limiter.limit(f"{config.rate_limit}/minute")
async def get_constitutional_prompt(
    request: Request, 
    patterns: List[str], 
    severity: str = "medium",
    current_user: Dict[str, Any] = Depends(require_permission(Permission.CONSTITUTIONAL))
):
    """
    Generate constitutional prompts for specific failure patterns.

    Returns tailored prompts to mitigate detected patterns.
    """
    try:
        prompts = constitutional.generate_constitutional_prompts(
            patterns=patterns,
            severity=severity
        )

        return {
            "patterns": patterns,
            "severity": severity,
            "constitutional_prompts": prompts,
            "usage_guidance": "Insert these prompts into your AI system prompt or conversation context"
        }

    except Exception as e:
        logger.error(f"Constitutional prompt generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate constitutional prompts: {str(e)}")


@app.get("/v1/metrics")
async def get_service_metrics(
    current_user: Dict[str, Any] = Depends(require_permission(Permission.METRICS))
):
    """Get comprehensive Trust Guard service metrics and reliability statistics."""
    try:
        comprehensive_metrics = {
            "service_health": {
                "detector_status": detector.is_healthy(),
                "validator_status": validator.is_healthy(),
                "constitutional_status": constitutional.is_healthy(),
                "overall_health": all([
                    detector.is_healthy(),
                    validator.is_healthy(),
                    constitutional.is_healthy()
                ])
            },
            "performance_metrics": {
                "total_validations": metrics.get_total_validations(),
                "total_detections": metrics.get_total_detections(),
                "total_mitigations": metrics.get_total_mitigations(),
                "average_risk_score": metrics.get_average_risk_score(),
                "patterns_detected_today": metrics.get_patterns_detected_today()
            },
            "pattern_statistics": metrics.get_pattern_statistics(),
            "reliability_trends": metrics.get_reliability_trends(),
            "system_metrics": get_cached_system_metrics()
        }

        return comprehensive_metrics

    except Exception as e:
        logger.error(f"Metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {str(e)}")


# API Key Management Endpoints
@app.post("/v1/auth/api-keys")
async def create_api_key(
    name: str,
    role: str,
    expires_in_days: Optional[int] = None,
    current_user: Dict[str, Any] = Depends(require_permission(Permission.ADMIN))
):
    """Create a new API key."""
    try:
        from trustguard.auth import Role
        
        # Validate role
        try:
            role_enum = Role(role)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid role: {role}")
        
        api_key = auth_manager.create_api_key(name, role_enum, expires_in_days)
        
        logger.info(f"API key created: {api_key['key_id']} by user: {current_user['user_id']}")
        
        return api_key
        
    except Exception as e:
        logger.error(f"API key creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create API key: {str(e)}")


@app.get("/v1/auth/api-keys")
async def list_api_keys(
    current_user: Dict[str, Any] = Depends(require_permission(Permission.ADMIN))
):
    """List all API keys."""
    try:
        api_keys = auth_manager.list_api_keys()
        
        logger.info(f"API keys listed by user: {current_user['user_id']}")
        
        return {"api_keys": api_keys}
        
    except Exception as e:
        logger.error(f"API key listing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list API keys: {str(e)}")


@app.delete("/v1/auth/api-keys/{key_id}")
async def revoke_api_key(
    key_id: str,
    current_user: Dict[str, Any] = Depends(require_permission(Permission.ADMIN))
):
    """Revoke an API key."""
    try:
        success = auth_manager.revoke_api_key(key_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="API key not found")
        
        logger.info(f"API key revoked: {key_id} by user: {current_user['user_id']}")
        
        return {"message": "API key revoked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API key revocation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to revoke API key: {str(e)}")


@app.get("/v1/auth/security-events")
async def get_security_events(
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(require_permission(Permission.ADMIN))
):
    """Get recent security events."""
    try:
        events = security_manager.get_security_events(limit)
        
        logger.info(f"Security events retrieved by user: {current_user['user_id']}")
        
        return {"security_events": events}
        
    except Exception as e:
        logger.error(f"Security events retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve security events: {str(e)}")


@app.get("/v1/auth/secrets/status")
async def get_secrets_status(
    current_user: Dict[str, Any] = Depends(require_permission(Permission.ADMIN))
):
    """Get secrets status and rotation information."""
    try:
        secrets_summary = config.get_secrets_summary()
        
        logger.info(f"Secrets status retrieved by user: {current_user['user_id']}")
        
        return {"secrets_status": secrets_summary}
        
    except Exception as e:
        logger.error(f"Secrets status retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve secrets status: {str(e)}")


@app.post("/v1/auth/secrets/rotate")
async def rotate_secret(
    secret_name: str,
    current_user: Dict[str, Any] = Depends(require_permission(Permission.ADMIN))
):
    """Manually rotate a specific secret."""
    try:
        if secret_name not in ["secret_key", "jwt_secret", "encryption_key"]:
            raise HTTPException(status_code=400, detail=f"Invalid secret name: {secret_name}")
        
        # Force rotation by clearing cache
        if hasattr(config, '_secrets_cache') and secret_name in config._secrets_cache:
            del config._secrets_cache[secret_name]
        
        # Get the secret (this will trigger rotation)
        config.get_secret(secret_name)
        
        logger.info(f"Secret rotated: {secret_name} by user: {current_user['user_id']}")
        
        return {"message": f"Secret {secret_name} rotated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Secret rotation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to rotate secret: {str(e)}")


@app.get("/v1/observability/summary")
async def get_observability_summary(
    current_user: Dict[str, Any] = Depends(require_permission(Permission.ADMIN))
):
    """Get comprehensive observability summary."""
    try:
        summary = observability_manager.get_observability_summary()
        
        logger.info(f"Observability summary retrieved by user: {current_user['user_id']}")
        
        return summary
        
    except Exception as e:
        logger.error(f"Observability summary retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve observability summary: {str(e)}")


@app.get("/metrics")
async def get_prometheus_metrics():
    """Get Prometheus metrics in text format."""
    try:
        metrics_text = metrics.get_prometheus_metrics()
        return Response(content=metrics_text, media_type="text/plain")
        
    except Exception as e:
        logger.error(f"Prometheus metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve Prometheus metrics: {str(e)}")


@app.get("/v1/tracer/bullets")
async def get_tracer_bullets(
    count: int = 100,
    event_type: Optional[str] = None,
    format: str = "json",
    current_user: Dict[str, Any] = Depends(require_permission(Permission.READ_ONLY))
):
    """Get recent tracer bullets for debugging and monitoring."""
    try:
        bullets = tracer_manager.get_recent_bullets(count, event_type)
        
        if format == "json":
            bullets_data = []
            for bullet in bullets:
                bullets_data.append({
                    "timestamp": bullet.timestamp,
                    "event_type": bullet.event_type,
                    "message": bullet.message,
                    "data": bullet.data,
                    "thread_id": bullet.thread_id,
                    "duration": bullet.duration,
                    "parent_id": bullet.parent_id,
                    "bullet_id": bullet.bullet_id
                })
            return {"bullets": bullets_data, "count": len(bullets_data)}
        else:
            bullets_text = tracer_manager.export_bullets(format)
            return Response(content=bullets_text, media_type="text/plain")
        
    except Exception as e:
        logger.error(f"Tracer bullets retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tracer bullets: {str(e)}")


@app.get("/v1/tracer/performance")
async def get_tracer_performance(
    operation: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(require_permission(Permission.READ_ONLY))
):
    """Get performance metrics from tracer bullets."""
    try:
        performance_metrics = tracer_manager.get_performance_metrics(operation)
        return {"performance_metrics": performance_metrics}
        
    except Exception as e:
        logger.error(f"Tracer performance retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tracer performance: {str(e)}")


@app.get("/v1/tracer/health")
async def get_tracer_health(
    current_user: Dict[str, Any] = Depends(require_permission(Permission.READ_ONLY))
):
    """Get system health summary based on tracer bullets."""
    try:
        from trustguard.tracer import get_system_health_summary
        health_summary = get_system_health_summary()
        return health_summary
        
    except Exception as e:
        logger.error(f"Tracer health retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tracer health: {str(e)}")


@app.delete("/v1/tracer/bullets")
async def clear_tracer_bullets(
    current_user: Dict[str, Any] = Depends(require_permission(Permission.ADMIN))
):
    """Clear all tracer bullets (admin only)."""
    try:
        tracer_manager.clear_bullets()
        return {"message": "Tracer bullets cleared successfully"}
        
    except Exception as e:
        logger.error(f"Tracer bullets clearing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear tracer bullets: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Trust Guard - AI Reliability Solution",
               extra={"version": "1.0.0", "port": config.port})

    uvicorn.run(app, host=config.host, port=config.port)
