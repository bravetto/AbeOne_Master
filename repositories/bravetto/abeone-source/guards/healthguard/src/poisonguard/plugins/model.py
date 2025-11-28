from typing import Dict, Any
from .base import BasePlugin
from ..core import DataSample, AnalysisResult

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


class ModelPlugin(BasePlugin):
    """
    A plugin that uses a pre-trained model for analysis.
    Requires optional ML dependencies: torch and transformers
    Install with: pip install ".[ml]"
    """
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "ModelPlugin requires transformers and torch. "
                "Install with: pip install '.[ml]'"
            )
        model_name = self.config.get("model_name", "REPLACE_ME")
        self.classifier = pipeline(
            "text-classification",
            model=model_name,
            tokenizer=model_name
        )

    def analyze(self, sample: DataSample) -> AnalysisResult:
        is_poisoned = False
        confidence = 0.0
        details = {"reasons": []}

        if isinstance(sample.content, str):
            try:
                model_results = self.classifier(sample.content)
                if model_results and len(model_results) > 0:
                    label = model_results[0].get('label')
                    score = model_results[0].get('score')
                    if label == 'NEGATIVE' and score > self.config.get("toxicity_threshold", 0.9):
                        is_poisoned = True
                        confidence = score
                        details["reasons"].append(f"Detected potential toxicity with confidence {score:.2f}.")
                        details["model_prediction"] = {"label": label, "score": score}
                else:
                    details["reasons"].append("Model did not return any predictions.")
            except Exception as e:
                details["reasons"].append(f"Model analysis failed: {e}")

        return AnalysisResult(
            sample_id=sample.id,
            is_poisoned=is_poisoned,
            confidence=confidence,
            details=details
        )
