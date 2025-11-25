from abc import ABC, abstractmethod
from typing import Dict, Any
from ..core import DataSample, AnalysisResult


class BasePlugin(ABC):
    """
    Abstract base class for all analysis plugins.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def analyze(self, sample: DataSample) -> AnalysisResult:
        """
        Analyzes a single data sample and returns an analysis result.
        """
        pass
