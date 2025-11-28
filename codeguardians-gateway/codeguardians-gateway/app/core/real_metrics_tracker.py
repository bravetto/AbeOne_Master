"""
Real Metrics Tracking Service

This service tracks real metrics from guard operations and stores them
for business intelligence reporting.
"""

import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session_factory
from app.core.models import Base
from app.core.centralized_database import GuardOperation, GuardMetrics
from app.core.centralized_redis import CentralizedRedis

import logging

logger = logging.getLogger(__name__)


class RealMetricsTracker:
    """Tracks real metrics from guard operations."""
    
    def __init__(self):
        # Use the existing database session factory
        self._redis = None
    
    async def _get_db_session(self):
        """Get database session."""
        session_factory = get_session_factory()
        if session_factory:
            return session_factory()
        return None
    
    async def _get_redis(self):
        """Get Redis instance."""
        if self._redis is None:
            self._redis = CentralizedRedis(logger=logger)
            await self._redis.initialize()
        return self._redis
    
    async def record_guard_operation(
        self,
        guard_name: str,
        response_data: Dict[str, Any],
        processing_time: float,
        success: bool,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """Record a guard operation and extract metrics."""
        try:
            # Normalize response data (handle wrapped responses)
            metrics_data = response_data
            if isinstance(response_data, dict):
                # Check if response is wrapped (e.g., from HealthGuard list responses)
                if "results" in response_data and isinstance(response_data["results"], list):
                    # Extract from first result if available
                    if response_data["results"]:
                        metrics_data = response_data["results"][0] if isinstance(response_data["results"][0], dict) else response_data
                elif "data" in response_data:
                    metrics_data = response_data["data"]
            
            # Store operation in database
            session = await self._get_db_session()
            if session:
                try:
                    operation = GuardOperation(
                        guard_name=guard_name,
                        operation_type="process",
                        input_data={},
                        output_data=metrics_data,
                        processing_time_ms=processing_time,
                        success=success,
                        user_id=user_id,
                        session_id=session_id
                    )
                    session.add(operation)
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    logger.error(f"Error storing guard operation: {e}", exc_info=True)
                finally:
                    try:
                        await session.close()
                    except Exception as e:
                        logger.error(f"Error closing session: {e}")
            
            # Extract and store metrics based on guard type
            if guard_name == "tokenguard":
                # TokenGuard returns: tokens_saved, cost_savings_usd, compression_ratio
                tokens_saved = metrics_data.get("tokens_saved") or metrics_data.get("total_tokens_saved", 0)
                cost_savings = metrics_data.get("cost_savings_usd") or metrics_data.get("cost_savings", 0.0)
                
                if tokens_saved > 0:
                    session = await self._get_db_session()
                    if session:
                        try:
                            metric = GuardMetrics(
                                guard_name=guard_name,
                                metric_type="tokens_saved",
                                metric_value=float(tokens_saved),
                                metric_data={"cost_savings_usd": cost_savings}
                            )
                            session.add(metric)
                            await session.commit()
                        except Exception as e:
                            await session.rollback()
                            logger.error(f"Error storing metrics: {e}", exc_info=True)
                        finally:
                            try:
                                await session.close()
                            except Exception as e:
                                logger.error(f"Error closing session: {e}")
            
            elif guard_name == "trustguard":
                # TrustGuard returns: trust_score, violations_blocked, compliance_score
                violations_blocked = metrics_data.get("violations_blocked") or (1 if metrics_data.get("trust_score", 0) < 0.5 else 0)
                compliance_score = metrics_data.get("compliance_score") or metrics_data.get("trust_score", 1.0)
                
                if violations_blocked > 0:
                    session = await self._get_db_session()
                    if session:
                        try:
                            metric = GuardMetrics(
                                guard_name=guard_name,
                                metric_type="violations_blocked",
                                metric_value=float(violations_blocked),
                                metric_data={"compliance_score": compliance_score}
                            )
                            session.add(metric)
                            await session.commit()
                        except Exception as e:
                            await session.rollback()
                            logger.error(f"Error storing metrics: {e}", exc_info=True)
                        finally:
                            try:
                                await session.close()
                            except Exception as e:
                                logger.error(f"Error closing session: {e}")
            
            elif guard_name == "biasguard":
                # BiasGuard returns: bias_detected (bool), bias_score, bias_types
                bias_detected = 1 if metrics_data.get("bias_detected", False) else 0
                bias_score = metrics_data.get("bias_score", 0.0)
                
                session = await self._get_db_session()
                if session:
                    try:
                        metric = GuardMetrics(
                            guard_name=guard_name,
                            metric_type="bias_detected",
                            metric_value=float(bias_detected),
                            metric_data={"bias_score": bias_score, "bias_types": metrics_data.get("bias_types", [])}
                        )
                        session.add(metric)
                        await session.commit()
                    except Exception as e:
                        await session.rollback()
                        logger.error(f"Error storing metrics: {e}", exc_info=True)
                    finally:
                        try:
                            await session.close()
                        except Exception as e:
                            logger.error(f"Error closing session: {e}")
            
            elif guard_name == "contextguard":
                # ContextGuard returns: success, context_id, stored_data
                contexts_stored = 1 if metrics_data.get("success", False) else 0
                relevance_score = metrics_data.get("relevance_score", 0.0)
                
                session = await self._get_db_session()
                if session:
                    try:
                        metric = GuardMetrics(
                            guard_name=guard_name,
                            metric_type="contexts_stored",
                            metric_value=float(contexts_stored),
                            metric_data={"relevance_score": relevance_score}
                        )
                        session.add(metric)
                        await session.commit()
                    except Exception as e:
                        await session.rollback()
                        logger.error(f"Error storing metrics: {e}", exc_info=True)
                    finally:
                        try:
                            await session.close()
                        except Exception as e:
                            logger.error(f"Error closing session: {e}")
            
            elif guard_name == "healthguard":
                # HealthGuard returns: is_poisoned, confidence, details
                health_score = metrics_data.get("confidence", 0.0) if not metrics_data.get("is_poisoned", False) else 0.0
                
                session = await self._get_db_session()
                if session:
                    try:
                        metric = GuardMetrics(
                            guard_name=guard_name,
                            metric_type="health_score",
                            metric_value=health_score,
                            metric_data={"is_poisoned": metrics_data.get("is_poisoned", False)}
                        )
                        session.add(metric)
                        await session.commit()
                    except Exception as e:
                        await session.rollback()
                        logger.error(f"Error storing metrics: {e}", exc_info=True)
                    finally:
                        try:
                            await session.close()
                        except Exception as e:
                            logger.error(f"Error closing session: {e}")
            
            # Cache metrics in Redis for fast access
            redis = await self._get_redis()
            if redis:
                await redis.set_guard_metrics(guard_name, metrics_data)
            
        except Exception as e:
            logger.error(f"Error recording guard operation metrics: {e}")
    
    async def _update_redis_metrics(self, guard_name: str, response_data: Dict[str, Any]):
        """Update Redis metrics cache."""
        try:
            redis = await self._get_redis()
            if not redis:
                return
            
            current_metrics = await redis.get_guard_metrics(guard_name)
            if not current_metrics:
                current_metrics = {
                    "requests": 0,
                    "tokens_saved": 0,
                    "cost_savings_usd": 0.0,
                    "violations_blocked": 0,
                    "bias_detected": 0,
                    "contexts_stored": 0
                }
            
            # Increment counters
            current_metrics["requests"] = current_metrics.get("requests", 0) + 1
            
            # Add metrics based on guard type
            if guard_name == "tokenguard":
                current_metrics["tokens_saved"] = current_metrics.get("tokens_saved", 0) + response_data.get("tokens_saved", 0)
                current_metrics["cost_savings_usd"] = current_metrics.get("cost_savings_usd", 0.0) + response_data.get("cost_savings_usd", 0.0)
            elif guard_name == "trustguard":
                current_metrics["violations_blocked"] = current_metrics.get("violations_blocked", 0) + response_data.get("violations_blocked", 0)
            elif guard_name == "biasguard":
                current_metrics["bias_detected"] = current_metrics.get("bias_detected", 0) + (1 if response_data.get("bias_detected", False) else 0)
            elif guard_name == "contextguard":
                current_metrics["contexts_stored"] = current_metrics.get("contexts_stored", 0) + response_data.get("contexts_stored", 0)
            
            await redis.set_guard_metrics(guard_name, current_metrics)
            
        except Exception as e:
            logger.error(f"Error updating Redis metrics: {e}")
    
    async def get_real_metrics(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get real aggregated metrics from database."""
        try:
            session = await self._get_db_session()
            if not session:
                # Return empty metrics if database not available
                return self._get_empty_metrics()
            
            try:
                # Get operations count
                cutoff_time = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=time_window_hours)
                
                # Count total requests
                total_requests_query = select(func.count(GuardOperation.id)).where(
                    GuardOperation.created_at >= cutoff_time
                )
                total_requests_result = await session.execute(total_requests_query)
                total_requests = total_requests_result.scalar() or 0
                
                # Aggregate metrics by guard
                guard_metrics = {}
                for guard_name in ["tokenguard", "trustguard", "contextguard", "biasguard", "healthguard"]:
                    # Get operations for this guard
                    guard_ops_query = select(func.count(GuardOperation.id)).where(
                        and_(
                            GuardOperation.guard_name == guard_name,
                            GuardOperation.created_at >= cutoff_time,
                            GuardOperation.success == True
                        )
                    )
                    guard_ops_result = await session.execute(guard_ops_query)
                    requests_processed = guard_ops_result.scalar() or 0
                    
                    # Get metrics for this guard
                    tokens_saved = 0
                    cost_savings = 0.0
                    violations_blocked = 0
                    bias_detected = 0
                    
                    if guard_name == "tokenguard":
                        tokens_query = select(func.sum(GuardMetrics.metric_value)).where(
                            and_(
                                GuardMetrics.guard_name == guard_name,
                                GuardMetrics.metric_type == "tokens_saved",
                                GuardMetrics.timestamp >= cutoff_time
                            )
                        )
                        tokens_result = await session.execute(tokens_query)
                        tokens_saved = int(tokens_result.scalar() or 0)
                        
                        # Get cost savings from metric_data
                        cost_query = select(func.sum(GuardMetrics.metric_data['cost_savings_usd'])).where(
                            and_(
                                GuardMetrics.guard_name == guard_name,
                                GuardMetrics.metric_type == "tokens_saved",
                                GuardMetrics.timestamp >= cutoff_time
                            )
                        )
                        # Note: JSON extraction may need adjustment based on DB type
                    
                    elif guard_name == "trustguard":
                        violations_query = select(func.sum(GuardMetrics.metric_value)).where(
                            and_(
                                GuardMetrics.guard_name == guard_name,
                                GuardMetrics.metric_type == "violations_blocked",
                                GuardMetrics.timestamp >= cutoff_time
                            )
                        )
                        violations_result = await session.execute(violations_query)
                        violations_blocked = int(violations_result.scalar() or 0)
                    
                    elif guard_name == "biasguard":
                        bias_query = select(func.sum(GuardMetrics.metric_value)).where(
                            and_(
                                GuardMetrics.guard_name == guard_name,
                                GuardMetrics.metric_type == "bias_detected",
                                GuardMetrics.timestamp >= cutoff_time
                            )
                        )
                        bias_result = await session.execute(bias_query)
                        bias_detected = int(bias_result.scalar() or 0)
                    
                    guard_metrics[guard_name] = {
                        "requests_processed": requests_processed,
                        "tokens_saved": tokens_saved,
                        "cost_savings_usd": cost_savings,
                        "violations_blocked": violations_blocked,
                        "bias_detected": bias_detected
                    }
                
                # Calculate totals
                total_tokens_saved = sum(m.get("tokens_saved", 0) for m in guard_metrics.values())
                total_cost_savings = sum(m.get("cost_savings_usd", 0.0) for m in guard_metrics.values())
                total_violations_blocked = sum(m.get("violations_blocked", 0) for m in guard_metrics.values())
                total_bias_detected = sum(m.get("bias_detected", 0) for m in guard_metrics.values())
                
                # Calculate productivity and risk reduction (estimates based on data)
                productivity_increase = min(15.0, (total_tokens_saved / 1000) * 0.5) if total_tokens_saved > 0 else 0.0
                risk_reduction = min(95.0, (total_violations_blocked + total_bias_detected) * 5.0) if (total_violations_blocked + total_bias_detected) > 0 else 0.0
                
                return {
                    "total_requests": total_requests,
                    "total_tokens_saved": total_tokens_saved,
                    "total_cost_savings_usd": round(total_cost_savings, 2),
                    "total_violations_blocked": total_violations_blocked,
                    "total_bias_detected": total_bias_detected,
                    "productivity_increase_percent": round(productivity_increase, 1),
                    "risk_reduction_percent": round(risk_reduction, 1),
                    "guard_breakdown": guard_metrics,
                    "time_window_hours": time_window_hours,
                    "last_updated": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error querying database: {e}")
                return self._get_empty_metrics()
            finally:
                await session.close()
                
        except Exception as e:
            logger.error(f"Error getting real metrics: {e}")
            return self._get_empty_metrics()
    
    def _get_empty_metrics(self) -> Dict[str, Any]:
        """Return empty metrics structure."""
        return {
            "total_requests": 0,
            "total_tokens_saved": 0,
            "total_cost_savings_usd": 0.0,
            "total_violations_blocked": 0,
            "total_bias_detected": 0,
            "productivity_increase_percent": 0.0,
            "risk_reduction_percent": 0.0,
            "guard_breakdown": {},
            "time_window_hours": 24,
            "last_updated": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
            "error": "Database not available"
        }


# Global metrics tracker instance
real_metrics_tracker = RealMetricsTracker()
