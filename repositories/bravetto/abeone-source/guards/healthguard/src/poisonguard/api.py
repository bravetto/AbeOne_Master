import sys
import os
import logging
import logging.config
import time
import uuid
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from typing import List, Any, Optional
import yaml
import uvicorn

from poisonguard.core import DataSample, AnalysisResult, MitigationAction, Report
from poisonguard.analyzer import Analyzer
from poisonguard.mitigator import Mitigator
from poisonguard.reporter import Reporter
from poisonguard.monitoring import (
    get_correlation_id, set_correlation_id, record_request_metrics, 
    record_analysis_metrics, record_mitigation_metrics, get_metrics,
    health_checker, correlation_id
)
from poisonguard.database import db_manager
from poisonguard.config_validator import validate_config, get_config_validation_report

# Load logging configuration
with open('logging.yaml', 'r') as f:
    log_config = yaml.safe_load(f)
logging.config.dictConfig(log_config)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="PoisonGuard API",
    description="A tool to help diagnose and mitigate LLM poisoning",
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception for configuration errors
class ConfigError(Exception):
    pass

@app.exception_handler(ConfigError)
async def config_error_handler(request: Request, exc: ConfigError):
    logger.error(f"Configuration error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": f"Configuration error: {exc}"},
    )

from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}", exc_info=True)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

def load_config(config_path='config.yaml'):
    """Load and validate configuration."""
    try:
        return validate_config(config_path)
    except Exception as e:
        raise ConfigError(f"Configuration validation failed: {e}")

# Middleware for request tracking and metrics
@app.middleware("http")
async def request_tracking_middleware(request: Request, call_next):
    """Middleware for request tracking and correlation IDs."""
    start_time = time.time()
    
    # Set correlation ID from header or generate new one
    correlation_id_header = request.headers.get("X-Correlation-ID")
    if correlation_id_header:
        set_correlation_id(correlation_id_header)
    else:
        set_correlation_id(str(uuid.uuid4()))
    
    # Process request
    response = await call_next(request)
    
    # Record metrics
    duration = time.time() - start_time
    record_request_metrics(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
        duration=duration
    )
    
    # Add correlation ID to response headers
    response.headers["X-Correlation-ID"] = get_correlation_id()
    
    return response

try:
    config = load_config()
    analyzer = Analyzer(config.model_dump())
    mitigator = Mitigator(config.model_dump())
    reporter = Reporter()

    app.state.analyzer = analyzer
    app.state.mitigator = mitigator
    app.state.reporter = reporter
    app.state.config = config
except ConfigError as e:
    # This will be caught by the exception handler when the app starts
    raise e

class AnalyzeRequest(BaseModel):
    samples: List[DataSample]

@app.post("/analyze", response_model=List[AnalysisResult])
async def analyze_samples(request: AnalyzeRequest):
    if not request.samples:
        raise HTTPException(status_code=400, detail="Input samples cannot be empty.")
    
    start_time = time.time()
    correlation_id = get_correlation_id()
    
    try:
        logger.info(f"Analyzing {len(request.samples)} samples. Correlation ID: {correlation_id}")
        
        # Perform analysis
        results = app.state.analyzer.analyze(request.samples)
        
        # Record metrics
        for result in results:
            record_analysis_metrics(result.is_poisoned)
        
        # Store in database
        processing_time_ms = int((time.time() - start_time) * 1000)
        for sample, result in zip(request.samples, results):
            db_manager.store_analysis_result(
                sample_id=sample.id,
                is_poisoned=result.is_poisoned,
                confidence=result.confidence,
                details=result.details,
                correlation_id=correlation_id,
                processing_time_ms=processing_time_ms
            )
        
        logger.info(f"Analysis complete, returning {len(results)} results. Processing time: {processing_time_ms}ms")
        return results
        
    except Exception as e:
        logger.error(f"An unexpected error occurred during analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@app.post("/mitigate", response_model=List[MitigationAction])
async def mitigate_samples(request: AnalyzeRequest):
    if not request.samples:
        raise HTTPException(status_code=400, detail="Input samples cannot be empty.")
    
    start_time = time.time()
    correlation_id = get_correlation_id()
    
    try:
        logger.info(f"Mitigating {len(request.samples)} samples. Correlation ID: {correlation_id}")
        
        # Perform analysis and mitigation
        analysis_results = app.state.analyzer.analyze(request.samples)
        mitigation_actions = app.state.mitigator.mitigate(request.samples, analysis_results)
        
        # Record metrics
        for result in analysis_results:
            record_analysis_metrics(result.is_poisoned)
        for action in mitigation_actions:
            record_mitigation_metrics(action.action_taken)
        
        # Store in database
        processing_time_ms = int((time.time() - start_time) * 1000)
        for sample, result, action in zip(request.samples, analysis_results, mitigation_actions):
            # Store analysis result
            db_manager.store_analysis_result(
                sample_id=sample.id,
                is_poisoned=result.is_poisoned,
                confidence=result.confidence,
                details=result.details,
                correlation_id=correlation_id,
                processing_time_ms=processing_time_ms
            )
            # Store mitigation action
            db_manager.store_mitigation_result(
                sample_id=sample.id,
                action_taken=action.action_taken,
                details=action.details,
                correlation_id=correlation_id,
                processing_time_ms=processing_time_ms
            )
        
        logger.info(f"Mitigation complete, returning {len(mitigation_actions)} actions. Processing time: {processing_time_ms}ms")
        return mitigation_actions
        
    except Exception as e:
        logger.error(f"An unexpected error occurred during mitigation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@app.post("/report", response_model=Report)
async def generate_report(request: AnalyzeRequest):
    if not request.samples:
        raise HTTPException(status_code=400, detail="Input samples cannot be empty.")
    try:
        logger.info(f"Generating report for {len(request.samples)} samples.")
        analysis_results = app.state.analyzer.analyze(request.samples)
        mitigation_actions = app.state.mitigator.mitigate(request.samples, analysis_results)
        report = app.state.reporter.generate_report(analysis_results, mitigation_actions)
        logger.info("Report generation complete.")
        return report
    except Exception as e:
        logger.error(f"An unexpected error occurred during report generation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@app.get("/health", status_code=200)
async def health_check():
    """
    Comprehensive health check endpoint with system metrics.
    """
    return health_checker.check_health()

@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint.
    """
    return get_metrics()

@app.get("/config/validation")
async def config_validation():
    """
    Configuration validation endpoint.
    """
    return get_config_validation_report()

@app.get("/audit/analysis")
async def get_analysis_audit(
    sample_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    limit: int = 100
):
    """
    Get analysis audit trail.
    """
    return db_manager.get_analysis_history(sample_id, correlation_id, limit)

@app.get("/audit/mitigation")
async def get_mitigation_audit(
    sample_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    limit: int = 100
):
    """
    Get mitigation audit trail.
    """
    return db_manager.get_mitigation_history(sample_id, correlation_id, limit)

@app.get("/audit/system")
async def get_system_audit(limit: int = 100):
    """
    Get system metrics audit trail.
    """
    return db_manager.get_system_metrics_history(limit)

if __name__ == "__main__":
    uvicorn.run("poisonguard.api:app", host="0.0.0.0", port=8000, reload=True)