"""
Federated Learning Convergence Types
Type definitions for federated learning convergence system.

Pattern: FEDERATED × LEARNING × CONVERGENCE × EMERGENCE × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (ARXON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class InstanceStatus(Enum):
    """Instance status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class PatternQuality(Enum):
    """Pattern quality enumeration."""
    HIGH = "high"  # Epistemic certainty > 0.9
    MEDIUM = "medium"  # Epistemic certainty 0.7-0.9
    LOW = "low"  # Epistemic certainty < 0.7
    INVALID = "invalid"  # Failed validation


@dataclass
class InstanceMetadata:
    """Metadata for a production instance."""
    instance_id: str
    instance_name: str
    deployment_region: str
    registered_at: datetime = field(default_factory=datetime.now)
    last_heartbeat: Optional[datetime] = None
    status: InstanceStatus = InstanceStatus.ACTIVE
    reliability_score: float = 1.0  # 0.0-1.0
    data_quality_score: float = 1.0  # 0.0-1.0
    pattern_count: int = 0
    total_requests: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update_heartbeat(self) -> None:
        """Update heartbeat timestamp."""
        self.last_heartbeat = datetime.now()
    
    def calculate_weight(self) -> float:
        """Calculate instance weight for aggregation."""
        # Weight = reliability × data_quality × volume_factor
        volume_factor = min(1.0, self.pattern_count / 1000.0)  # Normalize to 0-1
        return self.reliability_score * self.data_quality_score * (0.5 + 0.5 * volume_factor)


@dataclass
class PatternSignature:
    """Privacy-preserving pattern signature."""
    signature_id: str
    pattern_type: str
    strength: float  # 0.0-1.0
    resonance: float  # 0.0-1.0
    frequency: int
    module_signatures: List[str]  # Anonymized module identifiers
    event_type_signatures: List[str]  # Anonymized event types
    epistemic_certainty: float  # 0.0-1.0
    quality: PatternQuality
    instance_id: str  # Source instance (for tracking, not raw data)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "signature_id": self.signature_id,
            "pattern_type": self.pattern_type,
            "strength": self.strength,
            "resonance": self.resonance,
            "frequency": self.frequency,
            "module_signatures": self.module_signatures,
            "event_type_signatures": self.event_type_signatures,
            "epistemic_certainty": self.epistemic_certainty,
            "quality": self.quality.value,
            "created_at": self.created_at.isoformat(),
            "instance_id": self.instance_id
        }


@dataclass
class InstanceScores:
    """Scores from a single instance."""
    instance_id: str
    convergence_score: float  # 0.0-1.0
    emergence_score: float  # 0.0-1.0
    resonance_score: float  # 0.0-1.0
    unified_score: float  # 0.0-1.0
    pattern_count: int
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "instance_id": self.instance_id,
            "convergence_score": self.convergence_score,
            "emergence_score": self.emergence_score,
            "resonance_score": self.resonance_score,
            "unified_score": self.unified_score,
            "pattern_count": self.pattern_count,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class AggregatedPattern:
    """Pattern aggregated from multiple instances."""
    pattern_id: str
    pattern_type: str
    aggregated_signature: PatternSignature
    contributing_instances: List[str]
    instance_count: int
    total_frequency: int
    average_strength: float
    average_resonance: float
    average_epistemic_certainty: float
    consensus_score: float  # 0.0-1.0 (agreement between instances)
    aggregated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "aggregated_signature": self.aggregated_signature.to_dict(),
            "contributing_instances": self.contributing_instances,
            "instance_count": self.instance_count,
            "total_frequency": self.total_frequency,
            "average_strength": self.average_strength,
            "average_resonance": self.average_resonance,
            "average_epistemic_certainty": self.average_epistemic_certainty,
            "consensus_score": self.consensus_score,
            "aggregated_at": self.aggregated_at.isoformat()
        }


@dataclass
class ConvergenceResult:
    """Result from convergence calculation."""
    convergence_score: float  # 0.0-1.0
    emergence_score: float  # 0.0-1.0
    patterns_aggregated: int
    instances_contributing: int
    pattern_alignment: float  # 0.0-1.0
    global_emergence_factor: float  # 0.0-1.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "convergence_score": self.convergence_score,
            "emergence_score": self.emergence_score,
            "patterns_aggregated": self.patterns_aggregated,
            "instances_contributing": self.instances_contributing,
            "pattern_alignment": self.pattern_alignment,
            "global_emergence_factor": self.global_emergence_factor,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class GlobalConvergenceScore:
    """Global convergence score across all instances."""
    global_convergence: float  # 0.0-1.0
    instance_count: int
    pattern_alignment: float  # 0.0-1.0
    global_emergence: float  # 0.0-1.0
    convergence_variance: float  # Variance of instance scores
    mean_convergence: float  # Mean of instance convergence scores
    weighted_mean_convergence: float  # Weighted mean
    timestamp: datetime = field(default_factory=datetime.now)
    instance_scores: List[InstanceScores] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "global_convergence": self.global_convergence,
            "instance_count": self.instance_count,
            "pattern_alignment": self.pattern_alignment,
            "global_emergence": self.global_emergence,
            "convergence_variance": self.convergence_variance,
            "mean_convergence": self.mean_convergence,
            "weighted_mean_convergence": self.weighted_mean_convergence,
            "timestamp": self.timestamp.isoformat(),
            "instance_scores": [score.to_dict() for score in self.instance_scores]
        }


@dataclass
class SynchronizationResult:
    """Result from synchronization protocol."""
    convergence_score: float  # 0.0-1.0
    instances_synced: int
    patterns_aggregated: int
    convergence_achieved: bool
    next_sync_window: datetime
    sync_duration_ms: float
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "convergence_score": self.convergence_score,
            "instances_synced": self.instances_synced,
            "patterns_aggregated": self.patterns_aggregated,
            "convergence_achieved": self.convergence_achieved,
            "next_sync_window": self.next_sync_window.isoformat(),
            "sync_duration_ms": self.sync_duration_ms,
            "errors": self.errors,
            "warnings": self.warnings,
            "timestamp": self.timestamp.isoformat()
        }

