# main.py
"""
TokenGuard Microservice API

FastAPI-based microservice for intelligent response pruning.
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
import time
import psutil
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from tokenguard.pruning import TokenGuardPruner
from tokenguard.config import config
from tokenguard.logging import setup_logging, log_with_context
from tokenguard.models import GenerateRequest, GenerateResponse, ToolCallRequest, ToolCallResponse, ModeConfig, ServiceMode

# Setup logging
logger = setup_logging()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Create a single, reusable pruner instance
try:
    pruner = TokenGuardPruner()
    logger.info("TokenGuardPruner initialized successfully.")
except Exception as e:
    logger.critical(f"Failed to initialize TokenGuardPruner: {e}")
    # The application should not start if the core component fails
    raise

# Security
security = HTTPBearer(auto_error=False) if config.api_key else None

app = FastAPI(
    title="TokenGuard Microservice",
    description="Intelligent response pruning service based on confidence analysis",
    version="1.0.0",
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Global exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> Any:
    """
    Global exception handler to catch any unhandled exceptions.

    This provides a final safety net for any errors that slip through
    individual endpoint error handling.
    """
    logger.error(
        f"Unhandled exception in {request.method} {request.url}: {type(exc).__name__}: {str(exc)}",
        exc_info=True,
    )

    # Enhanced error response with context
    error_response = {
        "detail": "Internal server error",
        "error_id": str(int(time.time() * 1000)),  # Simple error ID for tracking
    }

    # Add additional context for development/debugging
    if config.log_level.upper() == "DEBUG":
        import traceback
        error_response["traceback"] = traceback.format_exc()

    return JSONResponse(
        status_code=500,
        content=error_response,
    )


# CORS configuration
if config.cors_origins != "none":
    origins = config.cors_origins.split(",") if config.cors_origins != "*" else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Metrics instrumentation
if config.enable_metrics:
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)


def verify_api_key(authorization: str = Header(None)):
    """
    Verify API key if authentication is enabled.

    Raises:
        HTTPException: 401 if authentication is enabled and API key is invalid or missing

    Returns:
        bool: True if authentication is successful or disabled
    """
    if config.api_key:
        if not authorization:
            logger.warning("Authentication attempt without authorization header")
            raise HTTPException(
                status_code=401,
                detail="Authorization header required when authentication is enabled",
            )

        if not authorization.startswith("Bearer "):
            logger.warning(f"Invalid authorization header format: {authorization[:20]}...")
            raise HTTPException(
                status_code=401, detail="Authorization header must use Bearer token format"
            )

        try:
            token = authorization.split(" ")[1]
        except IndexError:
            logger.warning("Malformed Bearer token in authorization header")
            raise HTTPException(
                status_code=401, detail="Malformed Bearer token in authorization header"
            )

        if token != config.api_key:
            logger.warning("Authentication failed with invalid API key")
            raise HTTPException(status_code=401, detail="Invalid API key")

        logger.debug("Authentication successful")

    return True


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Any:
    """Log all requests with timing information."""
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    log_with_context(
        logger,
        "info",
        "Request processed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time_ms=round(process_time * 1000, 2),
        client_ip=get_remote_address(request),
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response


class PruneRequest(BaseModel):
    """Request model for pruning operations."""

    text: str = Field(..., alias="content", description="The text to analyze and potentially prune")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    logprobs_stream: Optional[List[Dict[str, Any]]] = Field(
        None, description="Optional log probabilities for advanced analysis"
    )

    class Config:
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "content": ("This is a long response that might need pruning based on "
                         "confidence analysis."),
                "confidence": 0.6,
                "logprobs_stream": None,
            }
        }


class PruneResponse(BaseModel):
    """Response model for pruning operations."""

    action: str = Field(..., description="Action taken: 'prune' or 'keep'")
    confidence: float = Field(..., description="Confidence score used in decision")
    reason: str = Field(..., description="Explanation for the decision")
    original_length: Optional[int] = Field(None, description="Original text length")
    pruned_length: Optional[int] = Field(None, description="Pruned text length")
    pruned_text: Optional[str] = Field(None, description="Pruned text (if action is 'prune')")

    class Config:
        json_schema_extra = {
            "example": {
                "action": "prune",
                "confidence": 0.6,
                "reason": "Low confidence (0.60) or excessive length (1200 chars)",
                "original_length": 1200,
                "pruned_length": 560,
                "pruned_text": ("This is a long response that might need pruning... "
                               "[Response truncated by TokenGuard for efficiency]"),
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")


def process_and_validate_request(prune_request: PruneRequest) -> float:
    """
    Shared logic to validate the request and perform confidence analysis.

    Args:
        prune_request: The request model instance.

    Returns:
        The calculated confidence score.

    Raises:
        HTTPException: If validation fails.
    """
    # Input validation
    if not prune_request.text or not prune_request.text.strip():
        raise HTTPException(
            status_code=400, detail="Text field is required and cannot be empty"
        )

    if len(prune_request.text) > config.max_length * 100:  # Allow some overhead
        raise HTTPException(
            status_code=400,
            detail=f"Text length ({len(prune_request.text)}) exceeds maximum allowed length",
        )

    # Use advanced confidence analysis if logprobs are provided
    confidence = prune_request.confidence
    if prune_request.logprobs_stream:
        try:
            confidence = pruner.analyze_token_stream_confidence(prune_request.logprobs_stream)
            log_with_context(
                logger,
                "debug",
                "Advanced confidence analysis performed",
                original_confidence=prune_request.confidence,
                analyzed_confidence=confidence,
            )
        except Exception as e:
            logger.warning(f"Failed to analyze logprobs stream, using provided confidence: {e}")
            confidence = prune_request.confidence

    return confidence


@app.get("/health", response_model=Dict[str, Any])
@limiter.limit(f"{config.rate_limit_requests}/{config.rate_limit_window} seconds")
async def health_check(request: Request) -> Any:
    """
    Enhanced health check endpoint with system metrics.

    Returns detailed health information including:
    - Service status
    - System resource usage
    - Configuration summary
    """
    try:
        # Basic service health
        health_data = {"status": "healthy", "version": "1.0.0", "timestamp": time.time()}

        # System metrics
        try:
            process = psutil.Process()
            health_data["system"] = {
                "cpu_percent": process.cpu_percent(),
                "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2),
                "uptime_seconds": round(time.time() - process.create_time(), 2),
            }
        except Exception as e:
            logger.warning(f"Could not gather system metrics: {e}")
            health_data["system"] = {"error": "metrics_unavailable"}

        # Configuration summary (excluding sensitive data)
        health_data["config"] = {
            "confidence_threshold": config.confidence_threshold,
            "max_length": config.max_length,
            "rate_limit_enabled": config.rate_limit_requests > 0,
            "metrics_enabled": config.enable_metrics,
            "auth_enabled": config.api_key is not None,
        }

        log_with_context(logger, "debug", "Health check performed", **health_data)
        return health_data

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.post("/v1/prune", response_model=PruneResponse)
@limiter.limit(f"{config.rate_limit_requests}/{config.rate_limit_window} seconds")
async def prune_text(
    request: Request, prune_request: PruneRequest, _: bool = Depends(verify_api_key)
):
    """
    Analyze and potentially prune text based on confidence and length thresholds.

    This endpoint uses TokenGuard's intelligent pruning algorithm to determine
    if a response should be truncated for efficiency while preserving quality.

    Args:
        prune_request: Request containing text, confidence, and optional logprobs

    Returns:
        PruneResponse: Contains action taken, confidence metrics, and pruned text if applicable

    Raises:
        HTTPException: 400 for invalid input, 500 for processing errors
    """
    start_time = time.time()

    try:
        log_with_context(
            logger,
            "info",
            "Prune request received",
            text_length=len(prune_request.text),
            confidence=prune_request.confidence,
            has_logprobs=prune_request.logprobs_stream is not None,
        )

        confidence = process_and_validate_request(prune_request)

        # Get pruning decision
        try:
            decision = pruner.should_prune(prune_request.text, confidence)
        except Exception as e:
            logger.error(f"Failed to analyze pruning decision: {e}")
            raise HTTPException(status_code=500, detail="Failed to analyze pruning requirements")

        # Apply pruning if needed
        if decision["action"] == "prune":
            try:
                pruned_text, was_pruned = pruner.apply_pruning(prune_request.text, decision)
            except Exception as e:
                logger.error(f"Failed to apply pruning: {e}")
                raise HTTPException(status_code=500, detail="Failed to apply text pruning")

            processing_time = (time.time() - start_time) * 1000
            original_length = decision.get("original_length", len(prune_request.text))
            savings_percent = round((1 - len(pruned_text) / max(original_length, 1)) * 100, 1)

            log_with_context(
                logger,
                "info",
                "Text pruned successfully",
                original_length=original_length,
                pruned_length=len(pruned_text),
                processing_time_ms=round(processing_time, 2),
                savings_percent=savings_percent,
            )

            return PruneResponse(
                action=decision["action"],
                confidence=decision["confidence"],
                reason=decision["reason"],
                original_length=original_length,
                pruned_length=len(pruned_text),
                pruned_text=pruned_text,
            )
        else:
            processing_time = (time.time() - start_time) * 1000
            log_with_context(
                logger,
                "info",
                "Text kept without pruning",
                text_length=len(prune_request.text),
                processing_time_ms=round(processing_time, 2),
            )

            return PruneResponse(
                action=decision["action"],
                confidence=decision["confidence"],
                reason=decision["reason"],
            )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, etc.)
        raise
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        log_with_context(
            logger,
            "error",
            "Pruning request failed",
            error=str(e),
            error_type=type(e).__name__,
            processing_time_ms=round(processing_time, 2),
        )
        raise HTTPException(status_code=500, detail="Internal server error during text processing")


@app.post("/scan", response_model=Dict[str, Any])
@limiter.limit(f"{config.rate_limit_requests}/{config.rate_limit_window} seconds")
async def scan_text(
    request: Request, scan_request: PruneRequest, _: bool = Depends(verify_api_key)
):
    """
    Scan text for confidence analysis and pruning recommendations.

    This endpoint performs the same analysis as /v1/analyze but uses the
    standardized /scan endpoint expected by the gateway.

    Args:
        scan_request: Request containing text, confidence, and optional logprobs

    Returns:
        Dict: Contains analysis results, confidence metrics, and recommendations

    Raises:
        HTTPException: 400 for invalid input, 500 for processing errors
    """
    # Reuse the same logic as /v1/analyze
    return await analyze_confidence(request, scan_request, _)


@app.post("/v1/analyze", response_model=Dict[str, Any])
@limiter.limit(f"{config.rate_limit_requests}/{config.rate_limit_window} seconds")
async def analyze_confidence(
    request: Request, analyze_request: PruneRequest, _: bool = Depends(verify_api_key)
):
    """
    Analyze confidence of text without applying pruning.

    Returns detailed confidence analysis and pruning recommendation.

    Args:
        analyze_request: Request containing text, confidence, and optional logprobs

    Returns:
        Dict: Contains analysis results, confidence metrics, and recommendations

    Raises:
        HTTPException: 400 for invalid input, 500 for processing errors
    """
    start_time = time.time()

    try:
        log_with_context(
            logger,
            "info",
            "Analysis request received",
            text_length=len(analyze_request.text),
            confidence=analyze_request.confidence,
        )

        confidence = process_and_validate_request(analyze_request)

        try:
            decision = pruner.should_prune(analyze_request.text, confidence)
        except Exception as e:
            logger.error(f"Failed to analyze pruning decision: {e}")
            raise HTTPException(status_code=500, detail="Failed to analyze text confidence")

        processing_time = (time.time() - start_time) * 1000

        result = {
            "text_length": len(analyze_request.text),
            "confidence_score": confidence,
            "decision": decision,
            "recommendation": "prune" if decision["action"] == "prune" else "keep",
            "processing_time_ms": round(processing_time, 2),
        }

        log_with_context(logger, "info", "Analysis completed", **result)

        return result

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, etc.)
        raise
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        log_with_context(
            logger,
            "error",
            "Analysis request failed",
            error=str(e),
            error_type=type(e).__name__,
            processing_time_ms=round(processing_time, 2),
        )
        raise HTTPException(status_code=500, detail="Internal server error during text analysis")


@app.post("/v1/generate", response_model=GenerateResponse)
@limiter.limit(f"{config.rate_limit_requests}/{config.rate_limit_window} seconds")
async def generate_text(
    request: Request, generate_request: GenerateRequest, _: bool = Depends(verify_api_key)
):
    """
    Generates text from a prompt and applies real-time confidence-based pruning.
    """
    start_time = time.time()
    try:
        log_with_context(
            logger,
            "info",
            "Generate request received",
            model=generate_request.llm_config.model,
            prompt_length=len(generate_request.prompt),
        )

        response = await pruner.generate_and_prune(generate_request)

        processing_time = (time.time() - start_time) * 1000
        log_with_context(
            logger,
            "info",
            "Generation completed",
            stop_reason=response.stop_reason,
            final_confidence=response.confidence,
            generated_length=len(response.text),
            processing_time_ms=round(processing_time, 2),
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        log_with_context(
            logger,
            "error",
            "Generation request failed",
            error=str(e),
            error_type=type(e).__name__,
            processing_time_ms=round(processing_time, 2),
        )
        raise HTTPException(status_code=500, detail="Internal server error during generation")


@app.post("/v1/generate-with-tools", response_model=ToolCallResponse)
@limiter.limit(f"{config.rate_limit_requests}/{config.rate_limit_window} seconds")
async def generate_with_tools(
    request: Request, tool_request: ToolCallRequest, _: bool = Depends(verify_api_key)
):
    """
    Generates text with tool calling capabilities and applies confidence-based pruning.
    """
    start_time = time.time()
    try:
        log_with_context(
            logger,
            "info",
            "Tool call generation request received",
            model=tool_request.llm_config.model,
            prompt_length=len(tool_request.prompt),
            tools_count=len(tool_request.tools),
        )

        # Convert ToolCallRequest to GenerateRequest for processing
        generate_request = GenerateRequest(
            prompt=tool_request.prompt,
            llm_config=tool_request.llm_config,
            tokenguard_config=tool_request.tokenguard_config
        )

        # Generate with tools support
        response_dict = await pruner.generate_with_tools(generate_request, tool_request.tools)

        # Convert to ToolCallResponse
        response = ToolCallResponse(**response_dict)

        processing_time = (time.time() - start_time) * 1000
        log_with_context(
            logger,
            "info",
            "Tool call generation completed",
            stop_reason=response.stop_reason,
            final_confidence=response.confidence,
            generated_length=len(response.text),
            tool_calls_count=len(response.tool_calls),
            processing_time_ms=round(processing_time, 2),
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        log_with_context(
            logger,
            "error",
            "Tool call generation request failed",
            error=str(e),
            error_type=type(e).__name__,
            processing_time_ms=round(processing_time, 2),
        )
        raise HTTPException(status_code=500, detail="Internal server error during tool call generation")


if __name__ == "__main__":
    # Check service mode and configure accordingly
    mode_config = ModeConfig(
        mode=config.service_mode,
        mcp_server_name=config.mcp_server_name,
        mcp_server_version=config.mcp_server_version
    )

    if config.service_mode == "mcp":
        logger.info("Starting TokenGuard in MCP mode")
        from tokenguard.mcp_server import MCPServer
        mcp_server = MCPServer(mode_config)
        mcp_app = mcp_server.get_app()

        # Mount MCP routes under /mcp
        app.mount("/mcp", mcp_app)

        logger.info(f"Starting TokenGuard MCP server on {config.host}:{config.port}")
        uvicorn.run(app, host=config.host, port=config.port)

    elif config.service_mode == "tool_call":
        logger.info("Starting TokenGuard in tool call mode")
        logger.info(f"Starting TokenGuard microservice on {config.host}:{config.port}")
        uvicorn.run(app, host=config.host, port=config.port)

    else:  # standard mode
        logger.info("Starting TokenGuard in standard mode")
        logger.info(f"Starting TokenGuard microservice on {config.host}:{config.port}")
        uvicorn.run(app, host=config.host, port=config.port)
