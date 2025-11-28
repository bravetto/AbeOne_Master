"""
A/B Testing Framework for AIGuards

Comprehensive A/B testing implementation with:
- Experiment management
- User segmentation
- Statistical analysis
- Canary deployments
- Real-time tracking
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import json
import uuid
import asyncio
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import redis
import logging

logger = logging.getLogger(__name__)

# Database models
Base = declarative_base()

# Lazy imports for scientific computing libraries to avoid startup issues
def _get_numpy():
    """Lazy import numpy to avoid startup issues."""
    try:
        import numpy as np
        return np
    except ImportError:
        return None

def _get_scipy_stats():
    """Lazy import scipy.stats to avoid startup issues."""
    try:
        from scipy import stats
        return stats
    except ImportError:
        return None

# Lazy availability checks - only check when actually needed
def has_numpy():
    """Check if numpy is available."""
    try:
        import importlib.util
        spec = importlib.util.find_spec('numpy')
        return spec is not None
    except Exception:
        return False

def has_scipy():
    """Check if scipy is available."""
    try:
        import importlib.util
        spec = importlib.util.find_spec('scipy')
        return spec is not None
    except Exception:
        return False

class ExperimentStatus(Enum):
    """Experiment status enumeration"""
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class VariantType(Enum):
    """Variant type enumeration"""
    CONTROL = "control"
    TREATMENT = "treatment"
    CANARY = "canary"

@dataclass
class ExperimentConfig:
    """Configuration for A/B test experiments"""
    experiment_id: str
    name: str
    description: str
    status: ExperimentStatus
    start_date: datetime
    end_date: Optional[datetime]
    traffic_split: Dict[str, float]  # variant_name -> percentage
    success_metrics: List[str]
    minimum_sample_size: int
    confidence_level: float
    power: float
    primary_metric: str
    secondary_metrics: List[str]
    target_audience: Dict[str, Any]
    exclusion_criteria: List[str]
    created_by: str
    created_at: datetime
    updated_at: datetime

@dataclass
class VariantConfig:
    """Configuration for experiment variants"""
    variant_id: str
    experiment_id: str
    name: str
    variant_type: VariantType
    traffic_percentage: float
    configuration: Dict[str, Any]
    is_active: bool
    created_at: datetime

@dataclass
class ExperimentResult:
    """Results from A/B test experiments"""
    experiment_id: str
    variant_name: str
    user_id: str
    session_id: str
    timestamp: datetime
    metrics: Dict[str, float]
    result_metadata: Dict[str, Any]

@dataclass
class StatisticalAnalysis:
    """Statistical analysis results"""
    experiment_id: str
    variant_a: str
    variant_b: str
    sample_size_a: int
    sample_size_b: int
    mean_a: float
    mean_b: float
    std_a: float
    std_b: float
    p_value: float
    confidence_interval: tuple
    effect_size: float
    power: float
    is_significant: bool
    recommendation: str
    analysis_timestamp: datetime

# Database Models
class Experiment(Base):
    """Database model for experiments"""
    __tablename__ = "experiments"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    traffic_split = Column(JSON)
    success_metrics = Column(JSON)
    minimum_sample_size = Column(Integer, default=1000)
    confidence_level = Column(Float, default=0.95)
    power = Column(Float, default=0.8)
    primary_metric = Column(String, nullable=False)
    secondary_metrics = Column(JSON)
    target_audience = Column(JSON)
    exclusion_criteria = Column(JSON)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Variant(Base):
    """Database model for experiment variants"""
    __tablename__ = "variants"
    
    id = Column(String, primary_key=True)
    experiment_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    variant_type = Column(String, nullable=False)
    traffic_percentage = Column(Float, nullable=False)
    configuration = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExperimentResult(Base):
    """Database model for experiment results"""
    __tablename__ = "experiment_results"
    
    id = Column(String, primary_key=True)
    experiment_id = Column(String, nullable=False)
    variant_name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metrics = Column(JSON)
    result_metadata = Column(JSON)

class UserSegment(Base):
    """Database model for user segments"""
    __tablename__ = "user_segments"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    experiment_id = Column(String, nullable=False)
    variant_name = Column(String, nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class StatisticalAnalysis(Base):
    """Database model for statistical analysis results"""
    __tablename__ = "statistical_analysis"
    
    id = Column(String, primary_key=True)
    experiment_id = Column(String, nullable=False)
    variant_a = Column(String, nullable=False)
    variant_b = Column(String, nullable=False)
    sample_size_a = Column(Integer, nullable=False)
    sample_size_b = Column(Integer, nullable=False)
    mean_a = Column(Float, nullable=False)
    mean_b = Column(Float, nullable=False)
    std_a = Column(Float, nullable=False)
    std_b = Column(Float, nullable=False)
    p_value = Column(Float, nullable=False)
    confidence_interval = Column(JSON)
    effect_size = Column(Float, nullable=False)
    power = Column(Float, nullable=False)
    is_significant = Column(Boolean, nullable=False)
    recommendation = Column(Text)
    analysis_timestamp = Column(DateTime, default=datetime.utcnow)

# Helper functions for statistical analysis
def calculate_statistical_significance(data_a: List[float], data_b: List[float], alpha: float = 0.05) -> Dict[str, Any]:
    """
    Calculate statistical significance between two datasets.
    
    Args:
        data_a: First dataset
        data_b: Second dataset
        alpha: Significance level
    
    Returns:
        Dictionary with statistical analysis results
    """
    if not has_numpy() or not has_scipy():
        logger.warning("NumPy or SciPy not available. Statistical analysis limited.")
        return {
            "p_value": None,
            "effect_size": None,
            "is_significant": False,
            "recommendation": "Install NumPy and SciPy for statistical analysis",
            "sample_size_a": len(data_a),
            "sample_size_b": len(data_b),
            "mean_a": sum(data_a) / len(data_a) if data_a else 0,
            "mean_b": sum(data_b) / len(data_b) if data_b else 0,
            "std_a": None,
            "std_b": None,
            "confidence_interval": None,
            "power": None
        }
    
    try:
        # Get libraries lazily
        np = _get_numpy()
        stats = _get_scipy_stats()

        if not np or not stats:
            raise ImportError("NumPy or SciPy not available")

        # Perform t-test
        statistic, p_value = stats.ttest_ind(data_a, data_b)

        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(((len(data_a) - 1) * np.std(data_a, ddof=1)**2 +
                             (len(data_b) - 1) * np.std(data_b, ddof=1)**2) /
                            (len(data_a) + len(data_b) - 2))

        if pooled_std > 0:
            effect_size = (np.mean(data_a) - np.mean(data_b)) / pooled_std
        else:
            effect_size = 0

        # Determine significance
        is_significant = p_value < alpha

        # Generate recommendation
        if is_significant:
            if effect_size > 0.8:
                recommendation = "Strong evidence for difference. Large effect size."
            elif effect_size > 0.5:
                recommendation = "Moderate evidence for difference. Medium effect size."
            else:
                recommendation = "Weak evidence for difference. Small effect size."
        else:
            recommendation = "No significant difference detected."

        # Calculate confidence interval
        se = np.sqrt(np.var(data_a, ddof=1)/len(data_a) + np.var(data_b, ddof=1)/len(data_b))
        t_critical = stats.t.ppf(1 - alpha/2, len(data_a) + len(data_b) - 2)
        margin_error = t_critical * se

        diff_mean = np.mean(data_a) - np.mean(data_b)
        confidence_interval = (diff_mean - margin_error, diff_mean + margin_error)

        return {
            "p_value": float(p_value),
            "effect_size": float(effect_size),
            "is_significant": is_significant,
            "recommendation": recommendation,
            "sample_size_a": len(data_a),
            "sample_size_b": len(data_b),
            "mean_a": float(np.mean(data_a)),
            "mean_b": float(np.mean(data_b)),
            "std_a": float(np.std(data_a, ddof=1)),
            "std_b": float(np.std(data_b, ddof=1)),
            "confidence_interval": (float(confidence_interval[0]), float(confidence_interval[1])),
            "power": None  # Would require power analysis
        }
        
    except Exception as e:
        logger.error(f"Error in statistical analysis: {e}")
        return {
            "p_value": None,
            "effect_size": None,
            "is_significant": False,
            "recommendation": f"Statistical analysis failed: {str(e)}",
            "sample_size_a": len(data_a),
            "sample_size_b": len(data_b),
            "mean_a": sum(data_a) / len(data_a) if data_a else 0,
            "mean_b": sum(data_b) / len(data_b) if data_b else 0,
            "std_a": None,
            "std_b": None,
            "confidence_interval": None,
            "power": None
        }
