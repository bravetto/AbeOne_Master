from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class DataSample(BaseModel):
    """
    Represents a single data sample to be analyzed.
    """
    id: str
    content: Any
    metadata: Optional[Dict[str, Any]] = None


class AnalysisResult(BaseModel):
    """
    Represents the result of an analysis on a data sample.
    """
    sample_id: str
    is_poisoned: bool
    confidence: float
    details: Dict[str, Any]


class MitigationAction(BaseModel):
    """
    Represents an action taken to mitigate a detected threat.
    """
    sample_id: str
    action_taken: str
    details: Optional[Dict[str, Any]] = None


class Report(BaseModel):
    """
    Represents a summary report of the analysis and mitigation process.
    """
    total_samples: int
    poisoned_samples: int
    mitigated_samples: int
    analysis_results: List[AnalysisResult]
    mitigation_actions: List[MitigationAction]