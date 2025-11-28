import logging
import re
from typing import List, Dict, Any
from .core import DataSample, AnalysisResult, MitigationAction

logger = logging.getLogger(__name__)


class Mitigator:
    """
    Takes actions to mitigate threats found in data samples.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('mitigator', {})
        self.default_action = self.config.get('default_action', 'flag')

    def mitigate(self, samples: List[DataSample], analysis_results: List[AnalysisResult]) -> List[MitigationAction]:
        """
        Mitigates threats based on analysis results and the configured strategy.
        """
        actions = []
        for sample, result in zip(samples, analysis_results):
            action_taken = "none"
            details = {}

            if result.is_poisoned:
                action_taken = self.default_action
                logger.warning(f"Mitigating sample {sample.id} with action: {action_taken}")
                if action_taken == "sanitize":
                    keywords = self.config.get('sanitize_keywords', [])
                    original_content = sample.content
                    sanitized_content = original_content

                    if isinstance(original_content, str) and keywords:
                        # Create a regex pattern to find whole words, case-insensitively
                        pattern = r'\b(' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b'
                        sanitized_content = re.sub(pattern, '[SANITIZED]', original_content, flags=re.IGNORECASE)

                    details['sanitized_content'] = sanitized_content
                    logger.info(
                        f"Sanitized sample {sample.id}. Original: '{original_content}', "
                        f"Sanitized: '{sanitized_content}'"
                    )
                elif action_taken == "redact":
                    details['redacted_content_preview'] = "[REDACTED]"
                    logger.info(f"Redacted sample {sample.id}.")

                details['reason'] = "; ".join(result.details.get('reasons', ['No specific reason provided.']))

            actions.append(
                MitigationAction(
                    sample_id=result.sample_id,
                    action_taken=action_taken,
                    details=details,
                )
            )
        return actions
