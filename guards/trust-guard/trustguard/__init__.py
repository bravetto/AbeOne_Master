"""
Trust Guard - AI Reliability Solution

A comprehensive AI reliability solution that detects and mitigates seven core failure patterns:
- Hallucination: False/conflicting information presented as fact
- Drift: Loss of conversational coherence and consistency
- Bias: Systematic prejudices in responses or recommendations
- Deception: Intentional misleading or incomplete information
- Security Theater: False sense of security without real protection
- Duplication: Repetitive or redundant responses
- Stub Syndrome: Inadequate or superficial responses that don't address the query

This package provides:
- Pattern detection algorithms
- Mathematical validation (KL divergence, uncertainty quantification)
- Constitutional prompting for mitigation
- Integration with Context Guard and Bias Guard
- Real-time reliability scoring
"""

from .core import TrustGuardDetector
from .validation import ValidationEngine
from .constitutional import ConstitutionalPrompting
from .metrics import ReliabilityMetrics
from .config import get_config
from .logging import setup_logging

__version__ = "1.0.0"
__all__ = [
    "TrustGuardDetector",
    "ValidationEngine",
    "ConstitutionalPrompting",
    "ReliabilityMetrics",
    "get_config",
    "setup_logging"
]
