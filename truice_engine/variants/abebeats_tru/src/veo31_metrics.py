"""
Veo 3.1 Performance Metrics System
Track Prompt Effectiveness and Generation Quality

Uses EmergenceMetricsCollector pattern.

Pattern: METRICS × EFFECTIVENESS × TRACKING × ONE
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class PromptEffectivenessMetrics:
    """Metrics for prompt effectiveness"""
    total_generations: int = 0
    successful_generations: int = 0
    failed_generations: int = 0
    avg_quality_score: float = 0.0
    avg_user_satisfaction: float = 0.0
    avg_generation_time: float = 0.0
    credits_used: int = 0
    patterns_by_type: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    last_generation_time: Optional[datetime] = None
    
    def get_success_rate(self) -> float:
        """Calculate success rate"""
        if self.total_generations == 0:
            return 0.0
        return self.successful_generations / self.total_generations
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "total_generations": self.total_generations,
            "successful_generations": self.successful_generations,
            "failed_generations": self.failed_generations,
            "success_rate": self.get_success_rate(),
            "avg_quality_score": self.avg_quality_score,
            "avg_user_satisfaction": self.avg_user_satisfaction,
            "avg_generation_time": self.avg_generation_time,
            "credits_used": self.credits_used,
            "patterns_by_type": dict(self.patterns_by_type),
            "last_generation_time": self.last_generation_time.isoformat() if self.last_generation_time else None
        }


@dataclass
class GenerationLog:
    """Log entry for a generation"""
    generation_id: str
    timestamp: datetime
    prompt_type: str  # "layered_prompt", "character_bible", "workflow"
    model: str
    success: bool
    quality_score: Optional[float] = None
    user_satisfaction: Optional[float] = None
    generation_time: Optional[float] = None
    credits_used: Optional[int] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class Veo31MetricsCollector:
    """
    Performance Metrics Collector for Veo 3.1
    
    Tracks:
    - Prompt effectiveness
    - Generation quality
    - User satisfaction
    - Resource usage
    - Pattern performance
    """
    
    def __init__(self, log_retention_hours: int = 168):  # 7 days default
        """
        Initialize Metrics Collector.
        
        Args:
            log_retention_hours: Hours to retain logs
        """
        self.logger = logging.getLogger(f"{__name__}.Veo31MetricsCollector")
        self.log_retention_hours = log_retention_hours
        
        self.metrics = PromptEffectivenessMetrics()
        self.generation_logs: deque = deque(maxlen=10000)  # Keep last 10k logs
        
        # Pattern-specific metrics
        self.pattern_metrics: Dict[str, PromptEffectivenessMetrics] = defaultdict(
            lambda: PromptEffectivenessMetrics()
        )
    
    def record_generation(
        self,
        generation_id: str,
        prompt_type: str,
        model: str,
        success: bool,
        quality_score: Optional[float] = None,
        user_satisfaction: Optional[float] = None,
        generation_time: Optional[float] = None,
        credits_used: Optional[int] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record a generation result.
        
        Args:
            generation_id: Unique generation ID
            prompt_type: Type of prompt used
            model: Model used
            success: Whether generation succeeded
            quality_score: Optional quality score (0.0-1.0)
            user_satisfaction: Optional user satisfaction (0.0-1.0)
            generation_time: Optional generation time in seconds
            credits_used: Optional credits used
            error: Optional error message
            metadata: Optional metadata
        """
        timestamp = datetime.now()
        
        # Create log entry
        log_entry = GenerationLog(
            generation_id=generation_id,
            timestamp=timestamp,
            prompt_type=prompt_type,
            model=model,
            success=success,
            quality_score=quality_score,
            user_satisfaction=user_satisfaction,
            generation_time=generation_time,
            credits_used=credits_used,
            error=error,
            metadata=metadata or {}
        )
        
        self.generation_logs.append(log_entry)
        
        # Update overall metrics
        self.metrics.total_generations += 1
        if success:
            self.metrics.successful_generations += 1
        else:
            self.metrics.failed_generations += 1
        
        self.metrics.patterns_by_type[prompt_type] += 1
        self.metrics.last_generation_time = timestamp
        
        if credits_used:
            self.metrics.credits_used += credits_used
        
        # Update quality scores (exponential moving average)
        if quality_score is not None:
            alpha = 0.1
            self.metrics.avg_quality_score = (
                alpha * quality_score +
                (1 - alpha) * self.metrics.avg_quality_score
            )
        
        if user_satisfaction is not None:
            alpha = 0.1
            self.metrics.avg_user_satisfaction = (
                alpha * user_satisfaction +
                (1 - alpha) * self.metrics.avg_user_satisfaction
            )
        
        if generation_time is not None:
            alpha = 0.1
            self.metrics.avg_generation_time = (
                alpha * generation_time +
                (1 - alpha) * self.metrics.avg_generation_time
            )
        
        # Update pattern-specific metrics
        pattern_key = f"{prompt_type}_{model}"
        pattern_metrics = self.pattern_metrics[pattern_key]
        pattern_metrics.total_generations += 1
        if success:
            pattern_metrics.successful_generations += 1
        else:
            pattern_metrics.failed_generations += 1
        
        if quality_score is not None:
            alpha = 0.1
            pattern_metrics.avg_quality_score = (
                alpha * quality_score +
                (1 - alpha) * pattern_metrics.avg_quality_score
            )
    
    def get_effectiveness_report(self) -> Dict[str, Any]:
        """
        Generate effectiveness report.
        
        Returns:
            Dictionary with effectiveness metrics
        """
        return {
            "overall_metrics": self.metrics.to_dict(),
            "pattern_metrics": {
                key: metrics.to_dict()
                for key, metrics in self.pattern_metrics.items()
            },
            "recent_activity": self._get_recent_activity(),
            "top_performing_patterns": self._get_top_patterns(),
            "recommendations": self._generate_recommendations()
        }
    
    def get_pattern_effectiveness(
        self,
        prompt_type: str,
        model: Optional[str] = None
    ) -> Optional[PromptEffectivenessMetrics]:
        """Get effectiveness metrics for a specific pattern"""
        if model:
            pattern_key = f"{prompt_type}_{model}"
            return self.pattern_metrics.get(pattern_key)
        else:
            # Aggregate across all models for this prompt type
            aggregated = PromptEffectivenessMetrics()
            for key, metrics in self.pattern_metrics.items():
                if key.startswith(prompt_type):
                    aggregated.total_generations += metrics.total_generations
                    aggregated.successful_generations += metrics.successful_generations
                    aggregated.failed_generations += metrics.failed_generations
            return aggregated
    
    def _get_recent_activity(self, hours: int = 24) -> Dict[str, Any]:
        """Get recent activity statistics"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_logs = [
            log for log in self.generation_logs
            if log.timestamp >= cutoff
        ]
        
        return {
            "total_generations": len(recent_logs),
            "successful": sum(1 for log in recent_logs if log.success),
            "failed": sum(1 for log in recent_logs if not log.success),
            "avg_quality": (
                sum(log.quality_score for log in recent_logs if log.quality_score) /
                len([l for l in recent_logs if l.quality_score])
                if recent_logs else 0.0
            )
        }
    
    def _get_top_patterns(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing patterns"""
        patterns = []
        for key, metrics in self.pattern_metrics.items():
            if metrics.total_generations >= 3:  # Minimum usage
                patterns.append({
                    "pattern": key,
                    "success_rate": metrics.get_success_rate(),
                    "avg_quality": metrics.avg_quality_score,
                    "usage_count": metrics.total_generations
                })
        
        # Sort by success rate and quality
        patterns.sort(key=lambda x: (x["success_rate"], x["avg_quality"]), reverse=True)
        return patterns[:limit]
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        # Check overall success rate
        if self.metrics.get_success_rate() < 0.7:
            recommendations.append(
                f" Overall success rate is {self.metrics.get_success_rate():.1%} - "
                "consider reviewing prompt patterns"
            )
        
        # Check quality scores
        if self.metrics.avg_quality_score < 0.6:
            recommendations.append(
                f" Average quality score is {self.metrics.avg_quality_score:.2f} - "
                "consider improving prompt specificity"
            )
        
        # Check for underperforming patterns
        for key, metrics in self.pattern_metrics.items():
            if metrics.total_generations >= 5 and metrics.get_success_rate() < 0.5:
                recommendations.append(
                    f" Pattern '{key}' has low success rate ({metrics.get_success_rate():.1%}) - "
                    "consider alternative approaches"
                )
        
        # Check credits usage
        if self.metrics.credits_used > 1000:
            recommendations.append(
                f" Total credits used: {self.metrics.credits_used} - "
                "consider optimizing prompt length or using faster models"
            )
        
        return recommendations

