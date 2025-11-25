#!/usr/bin/env python3
"""
ContextGuard - Context Memory and Workflow Management Service
"""

import os
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from urllib.parse import urlparse, urlunparse

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field
import redis.asyncio as redis
import json
import logging
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SAFETY: Rate limiting (100 requests per minute per IP)
limiter = Limiter(key_func=get_remote_address)

# Data Models
class MemoryItem(BaseModel):
    key: str = Field(..., description="Memory key")
    value: Any = Field(..., description="Memory value")
    ttl: Optional[int] = Field(None, description="Time to live in seconds")

class ContextDriftRequest(BaseModel):
    current_code: str = Field(..., description="Current code snippet")
    previous_code: str = Field(..., description="Previous code snippet")
    context: Dict[str, Any] = Field(default_factory=dict, description="Context information")

class RAGRequest(BaseModel):
    query: str = Field(..., description="Query for RAG analysis")
    llm_config: Dict[str, Any] = Field(default_factory=dict, description="LLM configuration")
    tokenguard_config: Dict[str, Any] = Field(default_factory=dict, description="TokenGuard configuration")

class AIGuidelinesRequest(BaseModel):
    guidelines: str = Field(..., description="AI guidelines to store")

class NeuromorphicAnalysisRequest(BaseModel):
    analysis: str = Field(..., description="Neuromorphic analysis to store")

# Global variables
redis_client = None

# Prometheus metrics registry
_metrics_registry = CollectorRegistry()

# SAFETY: Prometheus metrics for production monitoring
REQUEST_COUNT = Counter(
    'contextguard_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status_code'],
    registry=_metrics_registry
)

REQUEST_DURATION = Histogram(
    'contextguard_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint'],
    registry=_metrics_registry
)

REDIS_CONNECTION_STATUS = Gauge(
    'contextguard_redis_connection_status',
    'Redis connection status (1=connected, 0=disconnected)',
    registry=_metrics_registry
)

MEMORY_OPERATIONS = Counter(
    'contextguard_memory_operations_total',
    'Total memory operations',
    ['operation'],  # 'store', 'retrieve', 'list'
    registry=_metrics_registry
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    global redis_client

    # Startup
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        redis_password = os.getenv("REDIS_PASSWORD")

        # Safely construct Redis URL with password if provided
        if redis_password:
            try:
                parsed = urlparse(redis_url)
                # Only add password if there's no existing username/password and hostname is valid
                if (not parsed.username and not parsed.password and
                    parsed.hostname and parsed.scheme):
                    # Reconstruct URL with password
                    netloc = f":{redis_password}@{parsed.hostname}"
                    if parsed.port:
                        netloc += f":{parsed.port}"
                    redis_url = urlunparse((
                        parsed.scheme,
                        netloc,
                        parsed.path,
                        parsed.params,
                        parsed.query,
                        parsed.fragment
                    ))
            except Exception as url_error:
                logger.warning(f"Failed to parse Redis URL for password insertion: {url_error}. Using original URL.")

        redis_client = redis.from_url(redis_url, decode_responses=True)
        await redis_client.ping()
        logger.info("Connected to Redis")
        REDIS_CONNECTION_STATUS.set(1)
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        logger.error(f"Redis URL: {redis_url}")
        redis_client = None
        REDIS_CONNECTION_STATUS.set(0)

    yield

    # Shutdown
    if redis_client:
        await redis_client.close()

# Create FastAPI app
app = FastAPI(
    title="ContextGuard",
    description="Context Memory and Workflow Management Service",
    version="1.0.0",
    lifespan=lifespan
)

# SAFETY: Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "message": "ContextGuard server is running",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_endpoint(request: Request):
    """Detailed health check"""
    start_time = time.time()
    health_status = {
        "service": "ContextGuard",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

    # Check Redis connection
    if redis_client:
        try:
            await redis_client.ping()
            health_status["redis"] = "connected"
            REDIS_CONNECTION_STATUS.set(1)
        except Exception as e:
            health_status["redis"] = f"error: {str(e)}"
            health_status["status"] = "unhealthy"
            REDIS_CONNECTION_STATUS.set(0)
    else:
        health_status["redis"] = "not connected"
        health_status["status"] = "unhealthy"
        REDIS_CONNECTION_STATUS.set(0)

    REQUEST_COUNT.labels(method="GET", endpoint="/health", status_code="200").inc()
    REQUEST_DURATION.labels(method="GET", endpoint="/health").observe(time.time() - start_time)
    return health_status

@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint.
    
    Returns Prometheus-formatted metrics including:
    - Request counts and durations
    - Redis connection status
    - Memory operation counts
    """
    try:
        return Response(
            content=generate_latest(_metrics_registry),
            media_type=CONTENT_TYPE_LATEST
        )
    except Exception as e:
        logger.error(f"Error generating metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Metrics generation failed: {str(e)}")

@app.post("/memory")
@limiter.limit("100/minute")
async def store_memory(item: MemoryItem, request: Request):
    """Store item in memory"""
    start_time = time.time()
    if not redis_client:
        REQUEST_COUNT.labels(method="POST", endpoint="/memory", status_code="503").inc()
        raise HTTPException(status_code=503, detail="Redis not available")

    try:
        # SAFETY: Validate key format
        if not item.key or len(item.key) > 255:
            REQUEST_COUNT.labels(method="POST", endpoint="/memory", status_code="400").inc()
            REQUEST_DURATION.labels(method="POST", endpoint="/memory").observe(time.time() - start_time)
            raise HTTPException(status_code=400, detail="Invalid key format")
        
        # SAFETY: Validate TTL range
        if item.ttl and (item.ttl < 0 or item.ttl > 31536000):  # Max 1 year
            REQUEST_COUNT.labels(method="POST", endpoint="/memory", status_code="400").inc()
            REQUEST_DURATION.labels(method="POST", endpoint="/memory").observe(time.time() - start_time)
            raise HTTPException(status_code=400, detail="TTL must be between 0 and 31536000 seconds")

        key = f"contextguard:memory:{item.key}"
        value = json.dumps({"value": item.value, "timestamp": datetime.utcnow().isoformat()})

        if item.ttl:
            await redis_client.setex(key, item.ttl, value)
        else:
            await redis_client.set(key, value)

        MEMORY_OPERATIONS.labels(operation="store").inc()
        REQUEST_COUNT.labels(method="POST", endpoint="/memory", status_code="200").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/memory").observe(time.time() - start_time)
        return {"message": "Stored successfully", "key": item.key}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error storing memory: {e}")
        REQUEST_COUNT.labels(method="POST", endpoint="/memory", status_code="500").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/memory").observe(time.time() - start_time)
        raise HTTPException(status_code=500, detail=f"Storage failed: {str(e)}")

@app.get("/memory/{key}")
@limiter.limit("100/minute")
async def get_memory(key: str, request: Request):
    """Retrieve item from memory"""
    start_time = time.time()
    if not redis_client:
        REQUEST_COUNT.labels(method="GET", endpoint="/memory/{key}", status_code="503").inc()
        raise HTTPException(status_code=503, detail="Redis not available")

    try:
        # SAFETY: Validate key format
        if not key or len(key) > 255:
            REQUEST_COUNT.labels(method="GET", endpoint="/memory/{key}", status_code="400").inc()
            REQUEST_DURATION.labels(method="GET", endpoint="/memory/{key}").observe(time.time() - start_time)
            raise HTTPException(status_code=400, detail="Invalid key format")
        
        redis_key = f"contextguard:memory:{key}"
        data = await redis_client.get(redis_key)

        if data:
            parsed = json.loads(data)
            MEMORY_OPERATIONS.labels(operation="retrieve").inc()
            REQUEST_COUNT.labels(method="GET", endpoint="/memory/{key}", status_code="200").inc()
            REQUEST_DURATION.labels(method="GET", endpoint="/memory/{key}").observe(time.time() - start_time)
            return {"key": key, "value": parsed["value"], "timestamp": parsed["timestamp"]}
        else:
            REQUEST_COUNT.labels(method="GET", endpoint="/memory/{key}", status_code="404").inc()
            REQUEST_DURATION.labels(method="GET", endpoint="/memory/{key}").observe(time.time() - start_time)
            raise HTTPException(status_code=404, detail="Key not found")

    except HTTPException:
        raise
    except json.JSONDecodeError:
        REQUEST_COUNT.labels(method="GET", endpoint="/memory/{key}", status_code="500").inc()
        REQUEST_DURATION.labels(method="GET", endpoint="/memory/{key}").observe(time.time() - start_time)
        raise HTTPException(status_code=500, detail="Invalid data format")
    except Exception as e:
        logger.error(f"Error retrieving memory: {e}")
        REQUEST_COUNT.labels(method="GET", endpoint="/memory/{key}", status_code="500").inc()
        REQUEST_DURATION.labels(method="GET", endpoint="/memory/{key}").observe(time.time() - start_time)
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@app.get("/memory")
@limiter.limit("100/minute")
async def get_memory_snapshot(request: Request):
    """Get all memory items"""
    start_time = time.time()
    if not redis_client:
        REQUEST_COUNT.labels(method="GET", endpoint="/memory", status_code="503").inc()
        raise HTTPException(status_code=503, detail="Redis not available")

    try:
        pattern = "contextguard:memory:*"
        keys = await redis_client.keys(pattern)

        memory = {}
        for key in keys:
            data = await redis_client.get(key)
            if data:
                try:
                    parsed = json.loads(data)
                    clean_key = key.replace("contextguard:memory:", "")
                    memory[clean_key] = parsed["value"]
                except json.JSONDecodeError:
                    continue

        MEMORY_OPERATIONS.labels(operation="list").inc()
        REQUEST_COUNT.labels(method="GET", endpoint="/memory", status_code="200").inc()
        REQUEST_DURATION.labels(method="GET", endpoint="/memory").observe(time.time() - start_time)
        return {"memory": memory, "count": len(memory)}

    except Exception as e:
        logger.error(f"Error getting memory snapshot: {e}")
        REQUEST_COUNT.labels(method="GET", endpoint="/memory", status_code="500").inc()
        REQUEST_DURATION.labels(method="GET", endpoint="/memory").observe(time.time() - start_time)
        raise HTTPException(status_code=500, detail=f"Snapshot failed: {str(e)}")

@app.post("/analyze")
@limiter.limit("100/minute")
async def analyze_context_drift(http_request: Request, request: ContextDriftRequest):
    """Analyze context drift between code snippets"""
    start_time = time.time()
    try:
        # SAFETY: Validate input
        if not request.current_code or not request.previous_code:
            REQUEST_COUNT.labels(method="POST", endpoint="/analyze", status_code="400").inc()
            REQUEST_DURATION.labels(method="POST", endpoint="/analyze").observe(time.time() - start_time)
            raise HTTPException(status_code=400, detail="current_code and previous_code are required")
        
        # SAFETY: Size limits
        max_code_length = 10 * 1024 * 1024  # 10MB
        if len(request.current_code) > max_code_length or len(request.previous_code) > max_code_length:
            REQUEST_COUNT.labels(method="POST", endpoint="/analyze", status_code="413").inc()
            REQUEST_DURATION.labels(method="POST", endpoint="/analyze").observe(time.time() - start_time)
            raise HTTPException(status_code=413, detail=f"Code length exceeds maximum of {max_code_length} bytes")
        # Simple drift detection based on code differences
        current_lines = set(request.current_code.split('\n'))
        previous_lines = set(request.previous_code.split('\n'))

        added_lines = current_lines - previous_lines
        removed_lines = previous_lines - current_lines
        common_lines = current_lines & previous_lines

        # Calculate drift metrics
        total_changes = len(added_lines) + len(removed_lines)
        total_lines = len(current_lines) + len(previous_lines)

        if total_lines == 0:
            drift_ratio = 0.0
        else:
            drift_ratio = total_changes / total_lines

        # Determine if drift is significant
        confidence = min(drift_ratio * 2, 1.0)  # Scale to 0-1 range

        drift_detected = confidence > 0.3  # Threshold for drift detection

        severity = "low"
        if confidence > 0.7:
            severity = "high"
        elif confidence > 0.5:
            severity = "medium"

        result = {
            "drift_detected": drift_detected,
            "confidence": confidence,
            "severity": severity,
            "metrics": {
                "added_lines": len(added_lines),
                "removed_lines": len(removed_lines),
                "common_lines": len(common_lines),
                "drift_ratio": drift_ratio
            },
            "recommendations": [
                "Review code changes for consistency",
                "Update context tracking if needed"
            ] if drift_detected else []
        }
        
        REQUEST_COUNT.labels(method="POST", endpoint="/analyze", status_code="200").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/analyze").observe(time.time() - start_time)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing context drift: {e}")
        REQUEST_COUNT.labels(method="POST", endpoint="/analyze", status_code="500").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/analyze").observe(time.time() - start_time)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/rag")
@limiter.limit("100/minute")
async def perform_rag_analysis(http_request: Request, request: RAGRequest):
    """Perform Retrieval-Augmented Generation analysis"""
    start_time = time.time()
    try:
        # SAFETY: Validate input
        if not request.query or len(request.query) > 10000:  # Max 10KB query
            REQUEST_COUNT.labels(method="POST", endpoint="/rag", status_code="400").inc()
            REQUEST_DURATION.labels(method="POST", endpoint="/rag").observe(time.time() - start_time)
            raise HTTPException(status_code=400, detail="Query is required and must be less than 10000 characters")
        
        if not redis_client:
            REQUEST_COUNT.labels(method="POST", endpoint="/rag", status_code="503").inc()
            REQUEST_DURATION.labels(method="POST", endpoint="/rag").observe(time.time() - start_time)
            raise HTTPException(status_code=503, detail="Redis not available")
        
        # Get stored neuromorphic analysis
        neuromorphic_key = "contextguard:neuromorphic:latest"
        neuromorphic_data = await redis_client.get(neuromorphic_key) if redis_client else None

        # Get stored AI guidelines
        guidelines_key = "contextguard:guidelines:latest"
        guidelines_data = await redis_client.get(guidelines_key) if redis_client else None

        context = ""
        if neuromorphic_data:
            context += f"Neuromorphic Analysis: {neuromorphic_data}\n"
        if guidelines_data:
            context += f"AI Guidelines: {guidelines_data}\n"

        # Simple RAG response (in a real implementation, this would call an LLM)
        response_text = f"Based on the context and query '{request.query}', here's the analysis."

        metacognitive_note = "Response generated using available context and guidelines."

        result = {
            "text": response_text,
            "metacognitive_note": metacognitive_note,
            "context_used": bool(context),
            "confidence": 0.85
        }
        
        REQUEST_COUNT.labels(method="POST", endpoint="/rag", status_code="200").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/rag").observe(time.time() - start_time)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error performing RAG analysis: {e}")
        REQUEST_COUNT.labels(method="POST", endpoint="/rag", status_code="500").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/rag").observe(time.time() - start_time)
        raise HTTPException(status_code=500, detail=f"RAG analysis failed: {str(e)}")

@app.post("/ai-guidelines")
@limiter.limit("100/minute")
async def store_ai_guidelines(http_request: Request, request: AIGuidelinesRequest):
    """Store AI guidelines"""
    start_time = time.time()
    if not redis_client:
        REQUEST_COUNT.labels(method="POST", endpoint="/ai-guidelines", status_code="503").inc()
        raise HTTPException(status_code=503, detail="Redis not available")

    try:
        key = "contextguard:guidelines:latest"
        value = json.dumps({
            "guidelines": request.guidelines,
            "timestamp": datetime.utcnow().isoformat()
        })

        await redis_client.set(key, value)

        REQUEST_COUNT.labels(method="POST", endpoint="/ai-guidelines", status_code="200").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/ai-guidelines").observe(time.time() - start_time)
        return {"message": "AI guidelines stored successfully"}

    except Exception as e:
        logger.error(f"Error storing AI guidelines: {e}")
        REQUEST_COUNT.labels(method="POST", endpoint="/ai-guidelines", status_code="500").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/ai-guidelines").observe(time.time() - start_time)
        raise HTTPException(status_code=500, detail=f"Storage failed: {str(e)}")

@app.post("/neuromorphic-analysis")
@limiter.limit("100/minute")
async def store_neuromorphic_analysis(http_request: Request, request: NeuromorphicAnalysisRequest):
    """Store neuromorphic analysis"""
    start_time = time.time()
    if not redis_client:
        REQUEST_COUNT.labels(method="POST", endpoint="/neuromorphic-analysis", status_code="503").inc()
        raise HTTPException(status_code=503, detail="Redis not available")

    try:
        key = "contextguard:neuromorphic:latest"
        value = json.dumps({
            "analysis": request.analysis,
            "timestamp": datetime.utcnow().isoformat()
        })

        await redis_client.set(key, value)

        REQUEST_COUNT.labels(method="POST", endpoint="/neuromorphic-analysis", status_code="200").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/neuromorphic-analysis").observe(time.time() - start_time)
        return {"message": "Neuromorphic analysis stored successfully"}

    except Exception as e:
        logger.error(f"Error storing neuromorphic analysis: {e}")
        REQUEST_COUNT.labels(method="POST", endpoint="/neuromorphic-analysis", status_code="500").inc()
        REQUEST_DURATION.labels(method="POST", endpoint="/neuromorphic-analysis").observe(time.time() - start_time)
        raise HTTPException(status_code=500, detail=f"Storage failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
