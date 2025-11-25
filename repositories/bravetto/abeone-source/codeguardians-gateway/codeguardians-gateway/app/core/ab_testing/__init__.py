"""
A/B Testing Integration Module

Main integration module that ties together all A/B testing components:
- Experiment management
- User segmentation
- Statistical analysis
- Canary deployments
- Analytics and tracking
"""

from typing import Dict, List, Any, Optional
import logging
import redis
from datetime import datetime

from .models import ExperimentConfig, ExperimentStatus, VariantType
from .segmentation import UserSegmentationEngine, TrafficSplitter
from .statistical_analysis import StatisticalAnalyzer
from .canary_deployment import CanaryDeploymentManager, CanaryConfigBuilder, CanaryStage
from .analytics import ExperimentTracker, BusinessImpactAnalyzer

logger = logging.getLogger(__name__)

class ABTestingFramework:
    """
    Complete A/B testing framework integration.
    
    Provides a unified interface for all A/B testing capabilities including
    experiment management, user segmentation, statistical analysis,
    canary deployments, and comprehensive analytics.
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        
        # Initialize components
        self.segmentation_engine = UserSegmentationEngine(redis_client)
        self.statistical_analyzer = StatisticalAnalyzer()
        self.canary_manager = CanaryDeploymentManager(
            self.segmentation_engine, 
            self.statistical_analyzer
        )
        self.tracker = ExperimentTracker(redis_client)
        self.business_analyzer = BusinessImpactAnalyzer(self.tracker)
        
        logger.info("A/B Testing Framework initialized")
    
    # Experiment Management
    
    async def create_experiment(
        self,
        name: str,
        description: str,
        traffic_split: Dict[str, float],
        success_metrics: List[str],
        primary_metric: str,
        created_by: str,
        **kwargs
    ) -> str:
        """
        Create a new A/B test experiment.
        
        Args:
            name: Experiment name
            description: Experiment description
            traffic_split: Traffic distribution across variants
            success_metrics: Metrics to track for success
            primary_metric: Primary metric for analysis
            created_by: User who created the experiment
            **kwargs: Additional experiment parameters
            
        Returns:
            Experiment ID
        """
        try:
            # Validate traffic split
            if not TrafficSplitter.validate_traffic_split(traffic_split):
                raise ValueError("Traffic split must sum to 100%")
            
            # Create experiment configuration
            experiment_config = ExperimentConfig(
                experiment_id=f"exp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                name=name,
                description=description,
                status=ExperimentStatus.DRAFT,
                start_date=datetime.utcnow(),
                end_date=kwargs.get('end_date'),
                traffic_split=traffic_split,
                success_metrics=success_metrics,
                minimum_sample_size=kwargs.get('minimum_sample_size', 1000),
                confidence_level=kwargs.get('confidence_level', 0.95),
                power=kwargs.get('power', 0.8),
                primary_metric=primary_metric,
                secondary_metrics=kwargs.get('secondary_metrics', []),
                target_audience=kwargs.get('target_audience', {}),
                exclusion_criteria=kwargs.get('exclusion_criteria', []),
                created_by=created_by,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # TODO: Store in database
            logger.info(f"Created experiment {experiment_config.experiment_id}")
            
            return experiment_config.experiment_id
            
        except Exception as e:
            logger.error(f"Error creating experiment: {e}")
            raise
    
    async def start_experiment(self, experiment_id: str) -> bool:
        """Start an A/B test experiment."""
        try:
            # TODO: Update experiment status in database
            logger.info(f"Started experiment {experiment_id}")
            return True
        except Exception as e:
            logger.error(f"Error starting experiment {experiment_id}: {e}")
            return False
    
    async def stop_experiment(self, experiment_id: str) -> bool:
        """Stop an A/B test experiment."""
        try:
            # TODO: Update experiment status in database
            logger.info(f"Stopped experiment {experiment_id}")
            return True
        except Exception as e:
            logger.error(f"Error stopping experiment {experiment_id}: {e}")
            return False
    
    # User Assignment
    
    async def assign_user_to_variant(
        self,
        user_id: str,
        experiment_id: str,
        user_attributes: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Assign user to experiment variant.
        
        Args:
            user_id: User identifier
            experiment_id: Experiment identifier
            user_attributes: Optional user attributes for targeting
            
        Returns:
            Variant name or None if user is excluded
        """
        try:
            variant = self.segmentation_engine.assign_user_to_variant(
                user_id=user_id,
                experiment_id=experiment_id,
                user_attributes=user_attributes
            )
            
            logger.debug(f"User {user_id} assigned to variant {variant} for experiment {experiment_id}")
            return variant
            
        except Exception as e:
            logger.error(f"Error assigning user to variant: {e}")
            return None
    
    async def get_user_variants(self, user_id: str) -> Dict[str, str]:
        """Get all active variant assignments for a user."""
        try:
            return self.segmentation_engine.get_user_variants(user_id)
        except Exception as e:
            logger.error(f"Error getting user variants: {e}")
            return {}
    
    # Result Tracking
    
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
        Track experiment result.
        
        Args:
            experiment_id: Experiment identifier
            variant_name: Variant name
            user_id: User identifier
            session_id: Session identifier
            metrics: Performance metrics
            result_metadata: Additional metadata
        """
        try:
            await self.tracker.track_experiment_result(
                experiment_id=experiment_id,
                variant_name=variant_name,
                user_id=user_id,
                session_id=session_id,
                metrics=metrics,
                result_metadata=result_metadata
            )
            
            logger.debug(f"Tracked result for experiment {experiment_id}, variant {variant_name}")
            
        except Exception as e:
            logger.error(f"Error tracking experiment result: {e}")
    
    # Analytics and Monitoring
    
    async def get_experiment_metrics(self, experiment_id: str) -> Dict[str, Any]:
        """Get current experiment metrics."""
        try:
            metrics = await self.tracker.get_experiment_metrics(experiment_id)
            return {
                "experiment_id": metrics.experiment_id,
                "timestamp": metrics.timestamp.isoformat(),
                "total_users": metrics.total_users,
                "variant_counts": metrics.variant_counts,
                "success_counts": metrics.success_counts,
                "error_counts": metrics.error_counts,
                "conversion_rates": metrics.conversion_rates,
                "average_response_times": metrics.average_response_times,
                "throughput": metrics.throughput,
                "business_metrics": metrics.business_metrics
            }
        except Exception as e:
            logger.error(f"Error getting experiment metrics: {e}")
            return {}
    
    async def get_experiment_performance_snapshot(self, experiment_id: str) -> Dict[str, Any]:
        """Get performance snapshot for experiment."""
        try:
            snapshot = await self.tracker.get_experiment_performance_snapshot(experiment_id)
            return {
                "timestamp": snapshot.timestamp.isoformat(),
                "metrics": snapshot.metrics,
                "variant_performance": snapshot.variant_performance,
                "system_health": snapshot.system_health,
                "alerts": snapshot.alerts
            }
        except Exception as e:
            logger.error(f"Error getting performance snapshot: {e}")
            return {}
    
    async def analyze_experiment(
        self,
        experiment_id: str,
        variant_a_data: List[float],
        variant_b_data: List[float],
        variant_a_name: str = "control",
        variant_b_name: str = "treatment",
        metric_type: str = "continuous"
    ) -> Dict[str, Any]:
        """
        Perform statistical analysis of experiment.
        
        Args:
            experiment_id: Experiment identifier
            variant_a_data: Data for variant A
            variant_b_data: Data for variant B
            variant_a_name: Name of variant A
            variant_b_name: Name of variant B
            metric_type: Type of metric (continuous, binary, count)
            
        Returns:
            Statistical analysis results
        """
        try:
            analysis = self.statistical_analyzer.analyze_experiment(
                experiment_id=experiment_id,
                variant_a_data=variant_a_data,
                variant_b_data=variant_b_data,
                variant_a_name=variant_a_name,
                variant_b_name=variant_b_name,
                metric_type=metric_type
            )
            
            return {
                "experiment_id": analysis.experiment_id,
                "variant_a": analysis.variant_a,
                "variant_b": analysis.variant_b,
                "sample_size_a": analysis.sample_size_a,
                "sample_size_b": analysis.sample_size_b,
                "mean_a": analysis.mean_a,
                "mean_b": analysis.mean_b,
                "std_a": analysis.std_a,
                "std_b": analysis.std_b,
                "primary_test": {
                    "test_name": analysis.primary_test.test_name,
                    "statistic": analysis.primary_test.statistic,
                    "p_value": analysis.primary_test.p_value,
                    "degrees_of_freedom": analysis.primary_test.degrees_of_freedom,
                    "confidence_interval": analysis.primary_test.confidence_interval,
                    "effect_size": analysis.primary_test.effect_size,
                    "power": analysis.primary_test.power,
                    "is_significant": analysis.primary_test.is_significant,
                    "interpretation": analysis.primary_test.interpretation
                },
                "secondary_tests": [
                    {
                        "test_name": test.test_name,
                        "statistic": test.statistic,
                        "p_value": test.p_value,
                        "is_significant": test.is_significant,
                        "interpretation": test.interpretation
                    }
                    for test in analysis.secondary_tests
                ],
                "confidence_interval": analysis.confidence_interval,
                "effect_size": analysis.effect_size,
                "power": analysis.power,
                "is_significant": analysis.is_significant,
                "recommendation": analysis.recommendation,
                "analysis_timestamp": analysis.analysis_timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing experiment: {e}")
            raise
    
    async def analyze_business_impact(
        self,
        experiment_id: str,
        experiment_config: ExperimentConfig
    ) -> Dict[str, Any]:
        """Analyze business impact of experiment."""
        try:
            analysis = await self.business_analyzer.analyze_business_impact(
                experiment_id=experiment_id,
                experiment_config=experiment_config
            )
            
            return {
                "experiment_id": analysis.experiment_id,
                "analysis_date": analysis.analysis_date.isoformat(),
                "revenue_impact": analysis.revenue_impact,
                "cost_savings": analysis.cost_savings,
                "user_satisfaction_impact": analysis.user_satisfaction_impact,
                "operational_efficiency": analysis.operational_efficiency,
                "risk_assessment": analysis.risk_assessment,
                "recommendations": analysis.recommendations,
                "confidence_level": analysis.confidence_level
            }
            
        except Exception as e:
            logger.error(f"Error analyzing business impact: {e}")
            raise
    
    # Canary Deployment
    
    async def start_canary_deployment(
        self,
        experiment_id: str,
        canary_variant: str,
        stages: List[CanaryStage] = None,
        stage_duration_minutes: int = 30,
        success_threshold: float = 0.95,
        failure_threshold: float = 0.05,
        auto_promote: bool = True,
        auto_rollback: bool = True
    ) -> str:
        """
        Start a canary deployment.
        
        Args:
            experiment_id: Experiment identifier
            canary_variant: Canary variant name
            stages: Canary deployment stages
            stage_duration_minutes: Duration of each stage
            success_threshold: Success rate threshold
            failure_threshold: Failure rate threshold
            auto_promote: Whether to auto-promote on success
            auto_rollback: Whether to auto-rollback on failure
            
        Returns:
            Deployment ID
        """
        try:
            if stages is None:
                stages = [CanaryStage.INITIAL, CanaryStage.SMALL, CanaryStage.MEDIUM, CanaryStage.LARGE]
            
            # Build canary configuration
            config = (CanaryConfigBuilder()
                     .for_experiment(experiment_id, canary_variant)
                     .with_stages(stages)
                     .with_duration(stage_duration_minutes)
                     .with_thresholds(success_threshold, failure_threshold)
                     .with_automation(auto_promote, auto_rollback)
                     .build())
            
            # Start deployment
            deployment = await self.canary_manager.start_canary_deployment(
                experiment_id=experiment_id,
                canary_variant=canary_variant,
                config=config
            )
            
            logger.info(f"Started canary deployment {deployment.deployment_id}")
            return deployment.deployment_id
            
        except Exception as e:
            logger.error(f"Error starting canary deployment: {e}")
            raise
    
    async def get_canary_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get canary deployment status."""
        try:
            deployment = self.canary_manager.get_deployment_status(deployment_id)
            if not deployment:
                return {"error": "Deployment not found"}
            
            return {
                "deployment_id": deployment.deployment_id,
                "experiment_id": deployment.experiment_id,
                "status": deployment.status.value,
                "current_stage": deployment.current_stage.value if deployment.current_stage else None,
                "stage_results": [
                    {
                        "stage": result.stage.value,
                        "traffic_percentage": result.traffic_percentage,
                        "start_time": result.start_time.isoformat(),
                        "end_time": result.end_time.isoformat() if result.end_time else None,
                        "duration_minutes": result.duration_minutes,
                        "success_rate": result.success_rate,
                        "error_rate": result.error_rate,
                        "is_successful": result.is_successful,
                        "issues_detected": result.issues_detected,
                        "recommendation": result.recommendation
                    }
                    for result in deployment.stage_results
                ],
                "overall_success_rate": deployment.overall_success_rate,
                "overall_error_rate": deployment.overall_error_rate,
                "deployment_start": deployment.deployment_start.isoformat(),
                "deployment_end": deployment.deployment_end.isoformat() if deployment.deployment_end else None,
                "total_duration_minutes": deployment.total_duration_minutes,
                "final_recommendation": deployment.final_recommendation
            }
            
        except Exception as e:
            logger.error(f"Error getting canary deployment status: {e}")
            return {"error": str(e)}
    
    async def cancel_canary_deployment(self, deployment_id: str) -> bool:
        """Cancel an active canary deployment."""
        try:
            return await self.canary_manager.cancel_deployment(deployment_id)
        except Exception as e:
            logger.error(f"Error cancelling canary deployment: {e}")
            return False
    
    # Utility Methods
    
    def validate_traffic_split(self, traffic_split: Dict[str, float]) -> bool:
        """Validate traffic split configuration."""
        return TrafficSplitter.validate_traffic_split(traffic_split)
    
    def normalize_traffic_split(self, traffic_split: Dict[str, float]) -> Dict[str, float]:
        """Normalize traffic split to ensure percentages sum to 100."""
        return TrafficSplitter.normalize_traffic_split(traffic_split)
    
    def create_canary_split(
        self, 
        base_split: Dict[str, float], 
        canary_percentage: float
    ) -> Dict[str, float]:
        """Create traffic split with canary deployment."""
        return TrafficSplitter.create_canary_split(base_split, canary_percentage)
    
    async def get_framework_status(self) -> Dict[str, Any]:
        """Get overall framework status."""
        try:
            return {
                "status": "healthy",
                "components": {
                    "segmentation_engine": "active",
                    "statistical_analyzer": "active",
                    "canary_manager": "active",
                    "tracker": "active",
                    "business_analyzer": "active"
                },
                "active_deployments": len(self.canary_manager.active_deployments),
                "redis_connected": self.redis_client.ping(),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting framework status: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
