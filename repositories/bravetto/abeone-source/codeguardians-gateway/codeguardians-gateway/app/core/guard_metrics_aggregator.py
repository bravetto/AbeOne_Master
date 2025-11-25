"""
Guard Metrics Aggregator

Aggregates metrics and benefits from all guards (TokenGuard, ContextGuard, TrustGuard)
for comprehensive analytics and business intelligence reporting.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import json
import redis
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class AggregatedGuardMetrics:
    """Consolidated metrics from all guards"""

    # Overall system metrics
    total_requests: int = 0
    total_processing_time_ms: float = 0.0
    system_uptime_pct: float = 0.0
    error_rate: float = 0.0

    # Token optimization metrics (across all requests)
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    overall_compression_ratio: float = 0.0
    tokens_saved_total: int = 0

    # Safety and compliance metrics
    total_violations_prevented: int = 0
    compliance_score_avg: float = 0.0
    safety_incidents_blocked: int = 0

    # Context and memory metrics
    active_memory_sessions: int = 0
    context_relevance_avg: float = 0.0
    memory_utilization_rate: float = 0.0

    # Combined business benefits
    total_cost_savings_usd: float = 0.0
    productivity_improvement_pct: float = 0.0
    risk_reduction_total: float = 0.0

    # Performance metrics
    avg_response_time_ms: float = 0.0
    cache_hit_rate_overall: float = 0.0
    throughput_requests_per_second: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['timestamp'] = datetime.utcnow().isoformat()
        return data


class GuardMetricsAggregator:
    """
    Centralized aggregator for collecting and analyzing metrics
    from all guards in the CodeGuardians ecosystem.
    """

    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.metrics_window = 3600  # 1 hour rolling window
        self.guard_metric_keys = {
            'tokenguard': 'guard:metrics:tokenguard',
            'contextguard': 'guard:metrics:contextguard',
            'trustguard': 'guard:metrics:trustguard'
        }

    async def collect_guard_metrics(self, guard_name: str) -> Optional[Dict[str, Any]]:
        """Collect metrics from a specific guard via Redis or direct call"""
        try:
            # Try Redis first (fastest)
            metrics_key = self.guard_metric_keys.get(guard_name)
            if metrics_key:
                cached_metrics = self.redis_client.get(metrics_key)
                if cached_metrics:
                    return json.loads(cached_metrics)

            # Fallback: Direct call to guard metrics collector
            if guard_name == 'tokenguard':
                try:
                    from guards.tokenguard.tokenguard.metrics import TokenGuardMetricsCollector
                    collector = TokenGuardMetricsCollector()
                    metrics = collector.get_current_metrics()
                    benefits = metrics.get_benefits_summary()
                    return {
                        'requests_processed': metrics.requests_processed,
                        'total_input_tokens': metrics.total_input_tokens,
                        'total_output_tokens': metrics.total_output_tokens,
                        'tokens_saved': metrics.tokens_saved,
                        'cost_savings_usd': metrics.cost_savings_usd,
                        'compression_ratio': metrics.compression_ratio,
                        'business_benefits': benefits
                    }
                except Exception as e:
                    logger.warning(f"Could not collect TokenGuard metrics: {e}")

            elif guard_name == 'contextguard':
                try:
                    from guards.contextguard.src.contextguard.metrics import ContextGuardMetricsCollector
                    collector = ContextGuardMetricsCollector()
                    metrics = collector.get_current_metrics()
                    benefits = metrics.get_benefits_summary()
                    return {
                        'requests_processed': metrics.requests_processed,
                        'active_memory_slots': metrics.active_memory_slots,
                        'context_relevance_score': metrics.context_relevance_score,
                        'user_productivity_increase': metrics.user_productivity_increase,
                        'business_benefits': benefits
                    }
                except Exception as e:
                    logger.warning(f"Could not collect ContextGuard metrics: {e}")

            elif guard_name == 'trustguard':
                try:
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(
                        "trustguard_metrics",
                        "guards/trust-guard/trustguard/metrics.py"
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    collector = module.TrustGuardMetricsCollector()
                    metrics = collector.get_current_metrics()
                    benefits = metrics.get_benefits_summary()
                    return {
                        'requests_processed': metrics.requests_processed,
                        'violations_blocked': metrics.violations_blocked,
                        'compliance_score': metrics.compliance_score,
                        'safety_incidents_prevented': metrics.safety_incidents_prevented,
                        'legal_risk_reduction': metrics.legal_risk_reduction,
                        'business_benefits': benefits
                    }
                except Exception as e:
                    logger.warning(f"Could not collect TrustGuard metrics: {e}")

            logger.debug(f"No metrics available for {guard_name}")
            return None

        except Exception as e:
            logger.error(f"Error collecting metrics from {guard_name}: {e}")
            return None

    async def aggregate_all_metrics(self) -> AggregatedGuardMetrics:
        """Aggregate metrics from all guards into unified view"""
        aggregated = AggregatedGuardMetrics()

        # Collect metrics from each guard
        guard_metrics = {}
        for guard_name in self.guard_metric_keys.keys():
            metrics = await self.collect_guard_metrics(guard_name)
            if metrics:
                guard_metrics[guard_name] = metrics

        # Aggregate operational metrics
        total_requests = 0
        total_tokens_in = 0
        total_tokens_out = 0

        for guard_name, metrics in guard_metrics.items():
            if guard_name == 'tokenguard':
                total_requests += metrics.get('requests_processed', 0)
                total_tokens_in += metrics.get('total_input_tokens', 0)
                total_tokens_out += metrics.get('total_output_tokens', 0)
                aggregated.tokens_saved_total += metrics.get('tokens_saved', 0)
                aggregated.total_cost_savings_usd += metrics.get('cost_savings_usd', 0)

            elif guard_name == 'contextguard':
                total_requests += metrics.get('requests_processed', 0)
                aggregated.active_memory_sessions += metrics.get('active_memory_slots', 0)
                aggregated.productivity_improvement_pct += metrics.get('user_productivity_increase', 0)

            elif guard_name == 'trustguard':
                total_requests += metrics.get('requests_processed', 0)
                aggregated.total_violations_prevented += metrics.get('violations_blocked', 0)
                aggregated.safety_incidents_blocked += metrics.get('safety_incidents_prevented', 0)
                aggregated.risk_reduction_total += metrics.get('legal_risk_reduction', 0)

        # Calculate overall metrics
        aggregated.total_requests = total_requests
        aggregated.total_input_tokens = total_tokens_in
        aggregated.total_output_tokens = total_tokens_out

        if total_tokens_in > 0:
            aggregated.overall_compression_ratio = 1 - (total_tokens_out / total_tokens_in)

        return aggregated

    def calculate_system_benefits(self, aggregated: AggregatedGuardMetrics) -> Dict[str, Any]:
        """Calculate comprehensive business benefits across all guards"""
        benefits = {
            "cost_metrics": {
                "total_tokens_saved": aggregated.tokens_saved_total,
                "cost_savings_usd": aggregated.total_cost_savings_usd,
                "compression_efficiency": f"{aggregated.overall_compression_ratio:.1%}"
            },
            "productivity_metrics": {
                "overall_productivity_gain": f"{aggregated.productivity_improvement_pct:.1f}%",
                "risk_reduction": f"{aggregated.risk_reduction_total:.1f}%",
                "safety_incidents_prevented": aggregated.safety_incidents_blocked
            },
            "operational_metrics": {
                "total_requests_processed": aggregated.total_requests,
                "active_memory_sessions": aggregated.active_memory_sessions,
                "violations_prevented": aggregated.total_violations_prevented
            }
        }

        return benefits

    async def get_unified_benefits_report(self) -> Dict[str, Any]:
        """Generate comprehensive benefits report for all guards"""
        try:
            aggregated = await self.aggregate_all_metrics()
            benefits = self.calculate_system_benefits(aggregated)

            report = {
                "timestamp": datetime.utcnow().isoformat(),
                "system_overview": aggregated.to_dict(),
                "business_benefits": benefits,
                "guard_breakdown": {}
            }

            # Add individual guard reports
            for guard_name in self.guard_metric_keys.keys():
                metrics = await self.collect_guard_metrics(guard_name)
                if metrics and hasattr(metrics, 'get_benefits_summary'):
                    report["guard_breakdown"][guard_name] = metrics.get_benefits_summary()
                else:
                    report["guard_breakdown"][guard_name] = {"status": "metrics_unavailable"}

            return report

        except Exception as e:
            logger.error(f"Error generating unified benefits report: {e}")
            return {"error": str(e), "status": "report_generation_failed"}

    async def export_analytics_dashboard(self, filename: Optional[str] = None) -> str:
        """Export comprehensive analytics for dashboard consumption"""
        report = await self.get_unified_benefits_report()

        if filename:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            return f"Analytics exported to {filename}"
        else:
            return json.dumps(report, indent=2)


# Global aggregator instance
metrics_aggregator = GuardMetricsAggregator()

# Helper functions for middleware integration
async def record_guard_operation(guard_name: str, operation_data: Dict[str, Any]) -> None:
    """Record operation metrics for a specific guard (called from middleware)"""
    try:
        from app.core.database import get_session_factory
        from app.core.centralized_database import GuardOperation, GuardMetrics
        
        logger.debug(f"Recording operation for {guard_name}: {operation_data}")
        
        session_factory = get_session_factory()
        if not session_factory:
            logger.warning("Database session factory not available for metric recording")
            return
        
        async with session_factory() as db:
            try:
                # Extract operation details
                operation_type = operation_data.get("operation_type", "unknown")
                input_data = operation_data.get("input_data", {})
                output_data = operation_data.get("output_data", {})
                processing_time_ms = operation_data.get("processing_time_ms", 0.0)
                success = operation_data.get("success", True)
                error_message = operation_data.get("error_message")
                user_id = operation_data.get("user_id")
                session_id = operation_data.get("session_id")
                
                # Record operation
                operation = GuardOperation(
                    guard_name=guard_name,
                    operation_type=operation_type,
                    input_data=input_data,
                    output_data=output_data,
                    processing_time_ms=processing_time_ms,
                    success=success,
                    error_message=error_message,
                    user_id=user_id,
                    session_id=session_id
                )
                db.add(operation)
                
                # Extract and record metrics based on guard type and output data
                if success and output_data:
                    metrics_to_record = []
                    
                    # TokenGuard metrics
                    if guard_name == "tokenguard":
                        tokens_saved = output_data.get("tokens_saved") or output_data.get("total_tokens_saved", 0)
                        cost_savings = output_data.get("cost_savings_usd") or output_data.get("cost_savings", 0.0)
                        compression_ratio = output_data.get("compression_ratio", 0.0)
                        
                        if tokens_saved > 0:
                            metrics_to_record.append({
                                "metric_type": "tokens_saved",
                                "metric_value": float(tokens_saved),
                                "metric_data": {"cost_savings_usd": cost_savings, "compression_ratio": compression_ratio}
                            })
                    
                    # ContextGuard metrics
                    elif guard_name == "contextguard":
                        context_relevance = output_data.get("relevance_score", 0.0)
                        memory_utilization = output_data.get("memory_utilization", 0.0)
                        
                        if context_relevance > 0:
                            metrics_to_record.append({
                                "metric_type": "context_relevance",
                                "metric_value": float(context_relevance),
                                "metric_data": {"memory_utilization": memory_utilization}
                            })
                    
                    # TrustGuard metrics
                    elif guard_name == "trustguard":
                        risk_score = output_data.get("risk_score", 0.0)
                        violations_prevented = output_data.get("violations_prevented", 0)
                        
                        if violations_prevented > 0:
                            metrics_to_record.append({
                                "metric_type": "violations_prevented",
                                "metric_value": float(violations_prevented),
                                "metric_data": {"risk_score": risk_score}
                            })
                    
                    # Record all metrics
                    for metric_data in metrics_to_record:
                        metric = GuardMetrics(
                            guard_name=guard_name,
                            metric_type=metric_data["metric_type"],
                            metric_value=metric_data["metric_value"],
                            metric_data=metric_data.get("metric_data", {})
                        )
                        db.add(metric)
                
                await db.commit()
                logger.debug(f"Recorded operation and metrics for {guard_name}")
                
            except Exception as e:
                await db.rollback()
                logger.error(f"Error recording guard operation: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Error recording guard operation: {e}", exc_info=True)


async def get_guard_benefits_summary() -> Dict[str, Any]:
    """Get consolidated benefits summary for all guards"""
    return await metrics_aggregator.get_unified_benefits_report()
