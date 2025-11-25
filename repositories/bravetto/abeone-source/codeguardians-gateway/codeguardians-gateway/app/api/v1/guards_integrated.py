"""
Integrated Guard Services API
All guard services integrated into the unified gateway
"""

import asyncio
import time
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/guards", tags=["Integrated Guard Services"])

class GuardRequest(BaseModel):
    """Request model for guard processing."""
    text: str
    session_id: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None

class GuardResponse(BaseModel):
    """Response model for guard processing."""
    success: bool
    data: Dict[str, Any]
    processing_time_ms: float
    service_used: str

# Global metrics storage (in production, this would be in Redis/DB)
guard_metrics = {
    'tokenguard': {'requests': 0, 'tokens_saved': 0, 'cost_savings': 0.0},
    'trustguard': {'requests': 0, 'violations_blocked': 0, 'compliance_score': 0.0},
    'contextguard': {'requests': 0, 'contexts_stored': 0, 'relevance_score': 0.0},
    'biasguard': {'requests': 0, 'bias_detected': 0, 'bias_score': 0.0},
    'healthguard': {'requests': 0, 'health_checks': 0, 'status': 'healthy'}
}

@router.post("/tokenguard", response_model=GuardResponse, summary="TokenGuard - Text Compression")
async def process_tokenguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process text through TokenGuard for compression and token savings."""
    start_time = time.time()
    
    try:
        text = request.text
        
        # Simple token compression logic
        words = text.split()
        original_length = len(words)
        
        # Compress by removing common filler words
        filler_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        compressed_words = [word for word in words if word.lower() not in filler_words]
        
        # Ensure we don't compress too much
        if len(compressed_words) < max(1, original_length // 3):
            compressed_words = words[:max(1, original_length // 2)]
        
        compressed_text = ' '.join(compressed_words)
        tokens_saved = original_length - len(compressed_words)
        compression_ratio = tokens_saved / original_length if original_length > 0 else 0
        
        # Calculate cost savings (assuming $0.002 per 1000 tokens)
        cost_savings = (tokens_saved / 1000) * 0.002
        
        # Update metrics
        guard_metrics['tokenguard']['requests'] += 1
        guard_metrics['tokenguard']['tokens_saved'] += tokens_saved
        guard_metrics['tokenguard']['cost_savings'] += cost_savings
        
        processing_time = (time.time() - start_time) * 1000
        
        return GuardResponse(
            success=True,
            data={
                "original_text": text,
                "compressed_text": compressed_text,
                "tokens_saved": tokens_saved,
                "compression_ratio": compression_ratio,
                "cost_savings_usd": cost_savings,
                "confidence": 0.85
            },
            processing_time_ms=processing_time,
            service_used="integrated_tokenguard"
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        raise HTTPException(status_code=500, detail=f"TokenGuard processing failed: {str(e)}")

@router.post("/trustguard", response_model=GuardResponse, summary="TrustGuard - Safety & Compliance")
async def process_trustguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process text through TrustGuard for safety and compliance checking."""
    start_time = time.time()
    
    try:
        text = request.text.lower()
        
        # Safety keywords and patterns
        unsafe_patterns = [
            'violence', 'harm', 'dangerous', 'illegal', 'hate speech',
            'threat', 'attack', 'kill', 'hurt', 'danger'
        ]
        
        # Compliance keywords
        compliance_patterns = [
            'privacy', 'confidential', 'personal data', 'gdpr', 'compliance'
        ]
        
        # Check for violations
        violations = []
        for pattern in unsafe_patterns:
            if pattern in text:
                violations.append(pattern)
        
        is_safe = len(violations) == 0
        compliance_score = 0.9 if is_safe else max(0.1, 0.9 - (len(violations) * 0.2))
        
        # Update metrics
        guard_metrics['trustguard']['requests'] += 1
        if not is_safe:
            guard_metrics['trustguard']['violations_blocked'] += 1
        guard_metrics['trustguard']['compliance_score'] = compliance_score
        
        processing_time = (time.time() - start_time) * 1000
        
        return GuardResponse(
            success=True,
            data={
                "text": request.text,
                "is_safe": is_safe,
                "violations_detected": violations,
                "compliance_score": compliance_score,
                "blocked": not is_safe,
                "confidence": 0.9
            },
            processing_time_ms=processing_time,
            service_used="integrated_trustguard"
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        raise HTTPException(status_code=500, detail=f"TrustGuard processing failed: {str(e)}")

@router.post("/contextguard", response_model=GuardResponse, summary="ContextGuard - Context Management")
async def process_contextguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process text through ContextGuard for context storage and retrieval."""
    start_time = time.time()
    
    try:
        text = request.text
        session_id = request.session_id or f"session_{int(time.time())}"
        
        # Simple context storage simulation
        context_data = {
            "text": text,
            "session_id": session_id,
            "timestamp": time.time(),
            "relevance_score": 0.85,
            "keywords": text.split()[:5]  # First 5 words as keywords
        }
        
        # Calculate relevance score based on text length and content
        relevance_score = min(1.0, len(text) / 100)  # Longer text = more relevant
        
        # Update metrics
        guard_metrics['contextguard']['requests'] += 1
        guard_metrics['contextguard']['contexts_stored'] += 1
        guard_metrics['contextguard']['relevance_score'] = relevance_score
        
        processing_time = (time.time() - start_time) * 1000
        
        return GuardResponse(
            success=True,
            data={
                "context_stored": context_data,
                "session_id": session_id,
                "relevance_score": relevance_score,
                "slots_used": 1,
                "confidence": 0.8
            },
            processing_time_ms=processing_time,
            service_used="integrated_contextguard"
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        raise HTTPException(status_code=500, detail=f"ContextGuard processing failed: {str(e)}")

@router.post("/biasguard", response_model=GuardResponse, summary="BiasGuard - Bias Detection")
async def process_biasguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process text through BiasGuard for bias detection."""
    start_time = time.time()
    
    try:
        text = request.text.lower()
        
        # Bias detection patterns
        gender_bias_patterns = [
            'he is', 'she is', 'men are', 'women are', 'boys are', 'girls are',
            'masculine', 'feminine', 'gentlemen', 'ladies'
        ]
        
        age_bias_patterns = [
            'young people', 'old people', 'millennials', 'boomers',
            'too young', 'too old', 'senior', 'junior'
        ]
        
        racial_bias_patterns = [
            'white people', 'black people', 'asian people', 'ethnicity',
            'race matters', 'cultural background'
        ]
        
        # Check for bias
        detected_bias = []
        bias_score = 0.0
        
        for pattern in gender_bias_patterns:
            if pattern in text:
                detected_bias.append('gender_bias')
                bias_score += 0.3
        
        for pattern in age_bias_patterns:
            if pattern in text:
                detected_bias.append('age_bias')
                bias_score += 0.3
        
        for pattern in racial_bias_patterns:
            if pattern in text:
                detected_bias.append('racial_bias')
                bias_score += 0.3
        
        bias_detected = len(detected_bias) > 0
        bias_score = min(1.0, bias_score)
        
        # Update metrics
        guard_metrics['biasguard']['requests'] += 1
        if bias_detected:
            guard_metrics['biasguard']['bias_detected'] += 1
        guard_metrics['biasguard']['bias_score'] = bias_score
        
        processing_time = (time.time() - start_time) * 1000
        
        return GuardResponse(
            success=True,
            data={
                "text": request.text,
                "bias_detected": bias_detected,
                "bias_score": bias_score,
                "bias_types": list(set(detected_bias)),
                "confidence": 0.8,
                "mitigation_suggestions": [
                    "Use gender-neutral language",
                    "Avoid age-specific assumptions",
                    "Focus on individual capabilities"
                ] if bias_detected else []
            },
            processing_time_ms=processing_time,
            service_used="integrated_biasguard"
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        raise HTTPException(status_code=500, detail=f"BiasGuard processing failed: {str(e)}")

@router.post("/healthguard", response_model=GuardResponse, summary="HealthGuard - System Monitoring")
async def process_healthguard(
    request: GuardRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process request through HealthGuard for system health monitoring."""
    start_time = time.time()
    
    try:
        # Simulate health metrics
        health_metrics = {
            "cpu_usage": 45.2,
            "memory_usage": 67.8,
            "disk_usage": 23.1,
            "response_time_ms": 15.5,
            "active_connections": 42,
            "error_rate": 0.02,
            "uptime_seconds": time.time() - 3600  # Simulate 1 hour uptime
        }
        
        # Determine overall health status
        overall_status = "healthy"
        if health_metrics["cpu_usage"] > 80 or health_metrics["memory_usage"] > 90:
            overall_status = "warning"
        if health_metrics["error_rate"] > 0.1:
            overall_status = "critical"
        
        # Update metrics
        guard_metrics['healthguard']['requests'] += 1
        guard_metrics['healthguard']['health_checks'] += 1
        guard_metrics['healthguard']['status'] = overall_status
        
        processing_time = (time.time() - start_time) * 1000
        
        return GuardResponse(
            success=True,
            data={
                "text": request.text,
                "health_metrics": health_metrics,
                "overall_status": overall_status,
                "timestamp": time.time(),
                "recommendations": [
                    "System running normally",
                    "Monitor CPU usage",
                    "Check memory allocation"
                ] if overall_status == "healthy" else [
                    "Investigate high resource usage",
                    "Check for memory leaks",
                    "Review error logs"
                ]
            },
            processing_time_ms=processing_time,
            service_used="integrated_healthguard"
        )
        
    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        raise HTTPException(status_code=500, detail=f"HealthGuard processing failed: {str(e)}")

@router.get("/metrics", summary="Get Guard Service Metrics")
async def get_guard_metrics(current_user: dict = Depends(get_current_user)):
    """Get metrics for all integrated guard services."""
    return {
        "guard_metrics": guard_metrics,
        "timestamp": time.time(),
        "total_requests": sum(metrics['requests'] for metrics in guard_metrics.values())
    }

@router.get("/health", summary="Health Check for Guard Services")
async def guard_health_check():
    """Health check for all integrated guard services."""
    return {
        "status": "healthy",
        "services": {
            name: {
                "status": "healthy",
                "requests_processed": metrics['requests'],
                "enabled": True
            }
            for name, metrics in guard_metrics.items()
        },
        "timestamp": time.time()
    }


