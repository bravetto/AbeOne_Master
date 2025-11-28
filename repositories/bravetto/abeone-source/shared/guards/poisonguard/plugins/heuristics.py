from .base import BasePlugin
from ..core import DataSample, AnalysisResult


class KeywordPlugin(BasePlugin):
    """
    A plugin that checks for the presence of suspicious keywords.
    """
    def analyze(self, sample: DataSample) -> AnalysisResult:
        is_poisoned = False
        confidence = 0.0
        details = {"reasons": []}
        keyword_list = self.config.get("keyword_list", [])

        if isinstance(sample.content, str):
            if any(keyword in sample.content.lower() for keyword in keyword_list):
                is_poisoned = True
                confidence = 0.9
                details["reasons"].append("Found suspicious keywords.")

        return AnalysisResult(
            sample_id=sample.id,
            is_poisoned=is_poisoned,
            confidence=confidence,
            details=details
        )


class LengthPlugin(BasePlugin):
    """
    A plugin that checks if the content length is within an acceptable range.
    """
    def analyze(self, sample: DataSample) -> AnalysisResult:
        is_poisoned = False
        confidence = 0.0
        details = {"reasons": []}
        min_length = self.config.get("min_length", 10)
        max_length = self.config.get("max_length", 1000)

        if isinstance(sample.content, str):
            content_len = len(sample.content)
            if not (min_length <= content_len <= max_length):
                is_poisoned = True
                confidence = 0.8
                details["reasons"].append(
                    f"Content length {content_len} is outside the acceptable range "
                    f"[{min_length}, {max_length}]."
                )

        return AnalysisResult(
            sample_id=sample.id,
            is_poisoned=is_poisoned,
            confidence=confidence,
            details=details
        )
