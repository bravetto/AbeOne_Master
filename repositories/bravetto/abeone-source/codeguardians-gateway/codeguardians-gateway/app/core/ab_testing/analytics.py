"""
Experiment Tracking and Analytics

Comprehensive tracking and analytics for A/B testing including:
- Real-time metrics collection
- Performance monitoring
- Business impact analysis
- Automated reporting
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import asyncio
import json
import logging
import redis
from collections import defaultdict, Counter

from .models import ExperimentConfig, ExperimentResult, StatisticalAnalysis
from .statistical_analysis import StatisticalAnalyzer

logger = logging.getLogger(__name__)

# Conditional imports for scientific computing libraries
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

@dataclass
class ExperimentMetrics:
    """Real-time experiment metrics"""
    experiment_id: str
    timestamp: datetime
    total_users: int
    variant_counts: Dict[str, int]
    success_counts: Dict[str, int]
    error_counts: Dict[str, int]
    conversion_rates: Dict[str, float]
    average_response_times: Dict[str, float]
    throughput: Dict[str, float]
    business_metrics: Dict[str, float]

@dataclass
class PerformanceSnapshot:
    """Performance snapshot for analysis"""
    timestamp: datetime
    metrics: Dict[str, float]
    variant_performance: Dict[str, Dict[str, float]]
    system_health: Dict[str, float]
    alerts: List[str]

@dataclass
class BusinessImpactAnalysis:
    """Business impact analysis results"""
    experiment_id: str
    analysis_date: datetime
    revenue_impact: float
    cost_savings: float
    user_satisfaction_impact: float
    operational_efficiency: float
    risk_assessment: str
    recommendations: List[str]
    confidence_level: float

class ExperimentTracker:
    """
    Real-time experiment tracking and metrics collection.
    
    Provides comprehensive tracking of experiment performance,
    user behavior, and business impact metrics.
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.metrics_prefix = "ab_test:metrics:"
        self.results_prefix = "ab_test:results:"
        self.analytics_prefix = "ab_test:analytics:"
        self.cache_ttl = 3600  # 1 hour
    
    async def track_experiment_result(
        self,
        experiment_id: str,
        variant_name: str,
        user_id: str,
        session_id: str,
        metrics: Dict[str, float],
        result_metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Track experiment result in real-time.
        
        Args:
            experiment_id: Experiment identifier
            variant_name: Variant name
            user_id: User identifier
            session_id: Session identifier
            metrics: Performance metrics
            result_metadata: Additional metadata
        """
        try:
            # Create result record
            result = ExperimentResult(
                experiment_id=experiment_id,
                variant_name=variant_name,
                user_id=user_id,
                session_id=session_id,
                timestamp=datetime.utcnow(),
                metrics=metrics,
                result_metadata=result_metadata or {}
            )
            
            # Store in Redis for real-time access
            result_key = f"{self.results_prefix}{experiment_id}:{user_id}:{session_id}"
            self.redis_client.setex(
                result_key, 
                self.cache_ttl, 
                json.dumps(asdict(result), default=str)
            )
            
            # Update real-time metrics
            await self._update_real_time_metrics(experiment_id, variant_name, metrics)
            
            # Trigger analytics if needed
            await self._trigger_analytics_if_needed(experiment_id)
            
            logger.debug(f"Tracked result for experiment {experiment_id}, variant {variant_name}")
            
        except Exception as e:
            logger.error(f"Error tracking experiment result: {e}")
    
    async def _update_real_time_metrics(
        self,
        experiment_id: str,
        variant_name: str,
        metrics: Dict[str, float]
    ):
        """Update real-time metrics for experiment."""
        try:
            metrics_key = f"{self.metrics_prefix}{experiment_id}"
            
            # Get current metrics
            current_metrics = self._get_current_metrics(experiment_id)
            
            # Update variant-specific metrics
            if variant_name not in current_metrics.variant_counts:
                current_metrics.variant_counts[variant_name] = 0
                current_metrics.success_counts[variant_name] = 0
                current_metrics.error_counts[variant_name] = 0
                current_metrics.conversion_rates[variant_name] = 0.0
                current_metrics.average_response_times[variant_name] = 0.0
                current_metrics.throughput[variant_name] = 0.0
            
            # Update counts
            current_metrics.variant_counts[variant_name] += 1
            current_metrics.total_users += 1
            
            # Update success/error counts
            if metrics.get("success", 0) > 0:
                current_metrics.success_counts[variant_name] += 1
            
            if metrics.get("error", 0) > 0:
                current_metrics.error_counts[variant_name] += 1
            
            # Update conversion rate
            success_rate = current_metrics.success_counts[variant_name] / current_metrics.variant_counts[variant_name]
            current_metrics.conversion_rates[variant_name] = success_rate
            
            # Update response time (rolling average)
            response_time = metrics.get("response_time", 0)
            if response_time > 0:
                current_avg = current_metrics.average_response_times[variant_name]
                count = current_metrics.variant_counts[variant_name]
                current_metrics.average_response_times[variant_name] = (
                    (current_avg * (count - 1) + response_time) / count
                )
            
            # Update throughput
            current_metrics.throughput[variant_name] = current_metrics.variant_counts[variant_name] / 60.0  # per minute
            
            # Update business metrics
            for metric_name, value in metrics.items():
                if metric_name.startswith("business_"):
                    current_metrics.business_metrics[f"{variant_name}_{metric_name}"] = value
            
            # Store updated metrics
            self.redis_client.setex(
                metrics_key,
                self.cache_ttl,
                json.dumps(asdict(current_metrics), default=str)
            )
            
        except Exception as e:
            logger.error(f"Error updating real-time metrics: {e}")
    
    def _get_current_metrics(self, experiment_id: str) -> ExperimentMetrics:
        """Get current metrics for experiment."""
        try:
            metrics_key = f"{self.metrics_prefix}{experiment_id}"
            cached_metrics = self.redis_client.get(metrics_key)
            
            if cached_metrics:
                metrics_data = json.loads(cached_metrics)
                return ExperimentMetrics(**metrics_data)
            else:
                # Return empty metrics
                return ExperimentMetrics(
                    experiment_id=experiment_id,
                    timestamp=datetime.utcnow(),
                    total_users=0,
                    variant_counts={},
                    success_counts={},
                    error_counts={},
                    conversion_rates={},
                    average_response_times={},
                    throughput={},
                    business_metrics={}
                )
                
        except Exception as e:
            logger.error(f"Error getting current metrics: {e}")
            return ExperimentMetrics(
                experiment_id=experiment_id,
                timestamp=datetime.utcnow(),
                total_users=0,
                variant_counts={},
                success_counts={},
                error_counts={},
                conversion_rates={},
                average_response_times={},
                throughput={},
                business_metrics={}
            )
    
    async def get_experiment_metrics(self, experiment_id: str) -> ExperimentMetrics:
        """Get current experiment metrics."""
        return self._get_current_metrics(experiment_id)
    
    async def get_experiment_performance_snapshot(self, experiment_id: str) -> PerformanceSnapshot:
        """Get performance snapshot for experiment."""
        try:
            metrics = await self.get_experiment_metrics(experiment_id)
            
            # Calculate variant performance
            variant_performance = {}
            for variant in metrics.variant_counts.keys():
                variant_performance[variant] = {
                    "conversion_rate": metrics.conversion_rates.get(variant, 0.0),
                    "average_response_time": metrics.average_response_times.get(variant, 0.0),
                    "throughput": metrics.throughput.get(variant, 0.0),
                    "success_count": metrics.success_counts.get(variant, 0),
                    "error_count": metrics.error_counts.get(variant, 0)
                }
            
            # Calculate system health
            system_health = {
                "overall_success_rate": sum(metrics.success_counts.values()) / max(sum(metrics.variant_counts.values()), 1),
                "total_throughput": sum(metrics.throughput.values()),
                "average_response_time": np.mean(list(metrics.average_response_times.values())) if (HAS_NUMPY and metrics.average_response_times) else (sum(metrics.average_response_times.values()) / len(metrics.average_response_times) if metrics.average_response_times else 0.0)
            }
            
            # Generate alerts
            alerts = self._generate_alerts(metrics, system_health)
            
            return PerformanceSnapshot(
                timestamp=datetime.utcnow(),
                metrics=asdict(metrics),
                variant_performance=variant_performance,
                system_health=system_health,
                alerts=alerts
            )
            
        except Exception as e:
            logger.error(f"Error getting performance snapshot: {e}")
            return PerformanceSnapshot(
                timestamp=datetime.utcnow(),
                metrics={},
                variant_performance={},
                system_health={},
                alerts=[f"Error generating snapshot: {str(e)}"]
            )
    
    def _generate_alerts(self, metrics: ExperimentMetrics, system_health: Dict[str, float]) -> List[str]:
        """Generate alerts based on metrics and system health."""
        alerts = []
        
        try:
            # Check overall success rate
            overall_success_rate = system_health.get("overall_success_rate", 0.0)
            if overall_success_rate < 0.9:
                alerts.append(f"Low overall success rate: {overall_success_rate:.2%}")
            
            # Check individual variant performance
            for variant, conversion_rate in metrics.conversion_rates.items():
                if conversion_rate < 0.8:
                    alerts.append(f"Low conversion rate for {variant}: {conversion_rate:.2%}")
            
            # Check response times
            for variant, response_time in metrics.average_response_times.items():
                if response_time > 1000:  # 1 second
                    alerts.append(f"High response time for {variant}: {response_time:.0f}ms")
            
            # Check throughput
            total_throughput = system_health.get("total_throughput", 0.0)
            if total_throughput < 10:  # Less than 10 requests per minute
                alerts.append(f"Low throughput: {total_throughput:.1f} requests/minute")
            
        except Exception as e:
            logger.error(f"Error generating alerts: {e}")
            alerts.append(f"Error generating alerts: {str(e)}")
        
        return alerts
    
    async def _trigger_analytics_if_needed(self, experiment_id: str):
        """Trigger analytics if experiment has enough data."""
        try:
            metrics = await self.get_experiment_metrics(experiment_id)
            
            # Check if we have enough data for analysis
            total_users = metrics.total_users
            if total_users >= 100:  # Minimum sample size
                # Trigger background analytics
                asyncio.create_task(self._perform_analytics(experiment_id))
                
        except Exception as e:
            logger.error(f"Error triggering analytics: {e}")
    
    async def _perform_analytics(self, experiment_id: str):
        """Perform analytics for experiment."""
        try:
            # TODO: Implement comprehensive analytics
            logger.info(f"Performing analytics for experiment {experiment_id}")
            
            # Store analytics results
            analytics_key = f"{self.analytics_prefix}{experiment_id}"
            analytics_data = {
                "experiment_id": experiment_id,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "status": "completed"
            }
            
            self.redis_client.setex(
                analytics_key,
                self.cache_ttl,
                json.dumps(analytics_data)
            )
            
        except Exception as e:
            logger.error(f"Error performing analytics: {e}")

class BusinessImpactAnalyzer:
    """
    Analyzes business impact of A/B test experiments.
    
    Provides comprehensive analysis of revenue impact, cost savings,
    user satisfaction, and operational efficiency.
    """
    
    def __init__(self, tracker: ExperimentTracker):
        self.tracker = tracker
    
    async def analyze_business_impact(
        self,
        experiment_id: str,
        experiment_config: ExperimentConfig,
        analysis_period_days: int = 7
    ) -> BusinessImpactAnalysis:
        """
        Analyze business impact of experiment.
        
        Args:
            experiment_id: Experiment identifier
            experiment_config: Experiment configuration
            analysis_period_days: Analysis period in days
            
        Returns:
            Business impact analysis results
        """
        try:
            # Get experiment metrics
            metrics = await self.tracker.get_experiment_metrics(experiment_id)
            
            # Calculate revenue impact
            revenue_impact = await self._calculate_revenue_impact(metrics, experiment_config)
            
            # Calculate cost savings
            cost_savings = await self._calculate_cost_savings(metrics, experiment_config)
            
            # Calculate user satisfaction impact
            user_satisfaction_impact = await self._calculate_user_satisfaction_impact(metrics)
            
            # Calculate operational efficiency
            operational_efficiency = await self._calculate_operational_efficiency(metrics)
            
            # Assess risk
            risk_assessment = self._assess_risk(metrics, experiment_config)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                revenue_impact, cost_savings, user_satisfaction_impact, operational_efficiency
            )
            
            # Calculate confidence level
            confidence_level = self._calculate_confidence_level(metrics)
            
            return BusinessImpactAnalysis(
                experiment_id=experiment_id,
                analysis_date=datetime.utcnow(),
                revenue_impact=revenue_impact,
                cost_savings=cost_savings,
                user_satisfaction_impact=user_satisfaction_impact,
                operational_efficiency=operational_efficiency,
                risk_assessment=risk_assessment,
                recommendations=recommendations,
                confidence_level=confidence_level
            )
            
        except Exception as e:
            logger.error(f"Error analyzing business impact: {e}")
            raise
    
    async def _calculate_revenue_impact(
        self,
        metrics: ExperimentMetrics,
        experiment_config: ExperimentConfig
    ) -> float:
        """Calculate revenue impact of experiment."""
        try:
            # Calculate revenue impact based on conversion rates and average order value
            control_conversion_rate = metrics.success_counts.get("control", 0) / max(metrics.variant_counts.get("control", 1), 1)
            treatment_conversion_rate = metrics.success_counts.get("treatment", 0) / max(metrics.variant_counts.get("treatment", 1), 1)
            
            # Get average order value from experiment config or use default
            avg_order_value = getattr(experiment_config, 'avg_order_value', 100.0)
            
            # Calculate conversion rate improvement
            conversion_improvement = treatment_conversion_rate - control_conversion_rate
            
            # Calculate revenue impact per user
            revenue_impact_per_user = conversion_improvement * avg_order_value
            
            # Scale by total users in treatment group
            treatment_users = metrics.variant_counts.get("treatment", 0)
            total_revenue_impact = revenue_impact_per_user * treatment_users
            
            # Apply confidence level (if we have statistical significance data)
            confidence_level = getattr(experiment_config, 'confidence_level', 0.95)
            adjusted_revenue_impact = total_revenue_impact * confidence_level
            
            logger.info(f"Revenue impact calculated: {adjusted_revenue_impact:.2f} (improvement: {conversion_improvement:.3f}, users: {treatment_users})")
            
            return adjusted_revenue_impact
            
        except Exception as e:
            logger.error(f"Error calculating revenue impact: {e}")
            return 0.0
    
    async def _calculate_cost_savings(
        self,
        metrics: ExperimentMetrics,
        experiment_config: ExperimentConfig
    ) -> float:
        """Calculate cost savings from experiment."""
        try:
            # Calculate cost savings based on efficiency improvements
            control_avg_response_time = metrics.average_response_times.get("control", 0.0)
            treatment_avg_response_time = metrics.average_response_times.get("treatment", 0.0)
            
            # Calculate response time improvement
            if control_avg_response_time > 0:
                response_time_improvement = (control_avg_response_time - treatment_avg_response_time) / control_avg_response_time
            else:
                response_time_improvement = 0.0
            
            # Get cost per request from experiment config or use default
            cost_per_request = getattr(experiment_config, 'cost_per_request', 0.01)
            
            # Calculate cost savings per request
            cost_savings_per_request = response_time_improvement * cost_per_request
            
            # Scale by total requests in treatment group
            treatment_requests = metrics.variant_counts.get("treatment", 0)
            total_cost_savings = cost_savings_per_request * treatment_requests
            
            # Additional savings from reduced error rates
            control_error_rate = 1 - (metrics.success_counts.get("control", 0) / max(metrics.variant_counts.get("control", 1), 1))
            treatment_error_rate = 1 - (metrics.success_counts.get("treatment", 0) / max(metrics.variant_counts.get("treatment", 1), 1))
            
            error_reduction = control_error_rate - treatment_error_rate
            error_cost_savings = error_reduction * treatment_requests * cost_per_request * 2  # Error handling costs more
            
            # Total cost savings
            total_savings = total_cost_savings + error_cost_savings
            
            # Apply confidence level
            confidence_level = getattr(experiment_config, 'confidence_level', 0.95)
            adjusted_cost_savings = total_savings * confidence_level
            
            logger.info(f"Cost savings calculated: {adjusted_cost_savings:.2f} (response improvement: {response_time_improvement:.3f}, error reduction: {error_reduction:.3f})")
            
            return adjusted_cost_savings
            
        except Exception as e:
            logger.error(f"Error calculating cost savings: {e}")
            return 0.0
    
    async def _calculate_user_satisfaction_impact(self, metrics: ExperimentMetrics) -> float:
        """Calculate user satisfaction impact."""
        try:
            # Calculate based on success rates and response times
            overall_success_rate = sum(metrics.success_counts.values()) / max(sum(metrics.variant_counts.values()), 1)
            
            if HAS_NUMPY:
                avg_response_time = np.mean(list(metrics.average_response_times.values())) if metrics.average_response_times else 0.0
            else:
                avg_response_time = sum(metrics.average_response_times.values()) / len(metrics.average_response_times) if metrics.average_response_times else 0.0
            
            # Simple satisfaction score (0-1)
            satisfaction_score = overall_success_rate * (1 - min(avg_response_time / 1000, 1))
            
            return satisfaction_score
        except Exception as e:
            logger.error(f"Error calculating user satisfaction impact: {e}")
            return 0.0
    
    async def _calculate_operational_efficiency(self, metrics: ExperimentMetrics) -> float:
        """Calculate operational efficiency improvement."""
        try:
            # Calculate based on throughput and error rates
            total_throughput = sum(metrics.throughput.values())
            total_errors = sum(metrics.error_counts.values())
            total_requests = sum(metrics.variant_counts.values())
            
            if total_requests == 0:
                return 0.0
            
            error_rate = total_errors / total_requests
            efficiency_score = total_throughput * (1 - error_rate)
            
            return efficiency_score
        except Exception as e:
            logger.error(f"Error calculating operational efficiency: {e}")
            return 0.0
    
    def _assess_risk(self, metrics: ExperimentMetrics, experiment_config: ExperimentConfig) -> str:
        """Assess risk level of experiment."""
        try:
            # Calculate risk factors
            total_users = metrics.total_users
            error_rate = sum(metrics.error_counts.values()) / max(sum(metrics.variant_counts.values()), 1)
            
            if total_users < experiment_config.minimum_sample_size:
                return "HIGH - Insufficient sample size"
            elif error_rate > 0.1:
                return "HIGH - High error rate"
            elif error_rate > 0.05:
                return "MEDIUM - Elevated error rate"
            else:
                return "LOW - Normal operation"
                
        except Exception as e:
            logger.error(f"Error assessing risk: {e}")
            return "UNKNOWN - Assessment failed"
    
    def _generate_recommendations(
        self,
        revenue_impact: float,
        cost_savings: float,
        user_satisfaction_impact: float,
        operational_efficiency: float
    ) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        try:
            if revenue_impact > 0:
                recommendations.append(f"Positive revenue impact: {revenue_impact:.2%}")
            
            if cost_savings > 0:
                recommendations.append(f"Cost savings achieved: {cost_savings:.2%}")
            
            if user_satisfaction_impact > 0.8:
                recommendations.append("High user satisfaction - consider promoting")
            elif user_satisfaction_impact < 0.6:
                recommendations.append("Low user satisfaction - consider rollback")
            
            if operational_efficiency > 1000:
                recommendations.append("High operational efficiency - scale implementation")
            elif operational_efficiency < 500:
                recommendations.append("Low operational efficiency - optimize implementation")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append(f"Error generating recommendations: {str(e)}")
        
        return recommendations
    
    def _calculate_confidence_level(self, metrics: ExperimentMetrics) -> float:
        """Calculate confidence level for analysis."""
        try:
            total_users = metrics.total_users
            
            # Simple confidence calculation based on sample size
            if total_users >= 10000:
                return 0.95
            elif total_users >= 5000:
                return 0.90
            elif total_users >= 1000:
                return 0.80
            elif total_users >= 500:
                return 0.70
            else:
                return 0.50
                
        except Exception as e:
            logger.error(f"Error calculating confidence level: {e}")
            return 0.50
