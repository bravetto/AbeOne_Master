"""
Bias Detection Metrics for CodeGuardians Gateway

Integrated metrics collection for bias detection functionality.
"""

import time
from typing import Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class BiasDetectionMetrics:
    """Metrics for bias detection service"""
    total_requests: int = 0
    bias_detected_count: int = 0
    average_bias_score: float = 0.0
    average_fairness_score: float = 0.0
    average_processing_time: float = 0.0
    bias_type_counts: Dict[str, int] = field(default_factory=dict)
    mitigation_suggestions_given: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def record_detection(
        self,
        bias_detected: bool,
        bias_score: float,
        fairness_score: float,
        processing_time: float,
        bias_types: list,
        suggestions_count: int
    ) -> None:
        """Record a bias detection result"""
        self.total_requests += 1
        
        if bias_detected:
            self.bias_detected_count += 1
        
        # Update running averages
        self.average_bias_score = (
            (self.average_bias_score * (self.total_requests - 1) + bias_score) / self.total_requests
        )
        self.average_fairness_score = (
            (self.average_fairness_score * (self.total_requests - 1) + fairness_score) / self.total_requests
        )
        self.average_processing_time = (
            (self.average_processing_time * (self.total_requests - 1) + processing_time) / self.total_requests
        )
        
        # Count bias types
        for bias_type in bias_types:
            self.bias_type_counts[bias_type] = self.bias_type_counts.get(bias_type, 0) + 1
        
        self.mitigation_suggestions_given += suggestions_count
        self.last_updated = datetime.now()
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        bias_detection_rate = (
            self.bias_detected_count / self.total_requests if self.total_requests > 0 else 0
        )
        
        return {
            "total_requests": self.total_requests,
            "bias_detection_rate": bias_detection_rate,
            "average_bias_score": round(self.average_bias_score, 3),
            "average_fairness_score": round(self.average_fairness_score, 3),
            "average_processing_time": round(self.average_processing_time, 3),
            "bias_type_breakdown": self.bias_type_counts,
            "mitigation_suggestions_given": self.mitigation_suggestions_given,
            "last_updated": self.last_updated.isoformat()
        }

# Global metrics instance
bias_metrics = BiasDetectionMetrics()
