#!/usr/bin/env python3
"""
TokenGuard Copilot Integration

This module provides seamless integration of TokenGuard into your own Copilot/AI assistant.
It handles response optimization, confidence analysis, and tool calling with minimal overhead.
"""

import requests
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

DEFAULT_TOKENGUARD_URL = "http://localhost:8000"

@dataclass
class TokenGuardConfig:
    """Configuration for TokenGuard integration."""
    base_url: str = DEFAULT_TOKENGUARD_URL
    api_key: Optional[str] = None
    timeout: int = 10
    confidence_threshold: float = 0.7
    auto_prune: bool = True

class TokenGuardCopilotClient:
    """
    Client for integrating TokenGuard into your Copilot workflow.

    This client provides:
    - Automatic response pruning based on confidence
    - Tool calling with confidence analysis
    - Real-time performance metrics
    - Graceful fallback when service unavailable
    """

    def __init__(self: Any, config: TokenGuardConfig):
        self.config = config
        self.session = requests.Session()
        self.session.timeout = config.timeout

        # Set up headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "TokenGuard-Copilot-Integration/1.0"
        })

        if config.api_key:
            self.session.headers["Authorization"] = f"Bearer {config.api_key}"

        # Track metrics
        self.metrics = {
            "requests_total": 0,
            "pruned_responses": 0,
            "tokens_saved": 0,
            "avg_response_time": 0.0
        }

    def is_service_available(self: Any) -> bool:
        """Check if TokenGuard service is available."""
        try:
            response = self.session.get(f"{self.config.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False

    def optimize_response(self: Any, text: str, confidence: float,
                         logprobs: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Optimize an AI response using TokenGuard.

        Args:
            text: The AI response text to optimize
            confidence: Confidence score (0.0-1.0)
            logprobs: Optional log probability data for advanced analysis

        Returns:
            Dict containing optimization results and metrics
        """
        if not self.config.auto_prune or confidence >= self.config.confidence_threshold:
            return {
                "action": "keep",
                "original_text": text,
                "confidence": confidence,
                "tokens_saved": 0
            }

        try:
            payload = {
                "text": text,
                "confidence": confidence,
                "logprobs_stream": logprobs
            }

            response = self.session.post(
                f"{self.config.base_url}/v1/prune",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                self._update_metrics(result, response.elapsed.total_seconds())
                return result
            else:
                logger.warning(f"TokenGuard prune failed: {response.status_code}")
                return self._fallback_response(text, confidence)

        except Exception as e:
            logger.warning(f"TokenGuard request failed: {e}")
            return self._fallback_response(text, confidence)

    def analyze_confidence(self: Any, text: str, confidence: float,
                          logprobs: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Analyze confidence without pruning."""
        try:
            payload = {
                "text": text,
                "confidence": confidence,
                "logprobs_stream": logprobs
            }

            response = self.session.post(
                f"{self.config.base_url}/v1/analyze",
                json=payload
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Analysis failed: {response.status_code}"}

        except Exception as e:
            return {"error": f"Analysis request failed: {e}"}

    def generate_with_tools(self: Any, prompt: str, tools: List[Dict],
                           llm_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate text with tool calling support and confidence pruning.

        This enables your Copilot to use TokenGuard as a tool during generation.
        """
        try:
            payload = {
                "prompt": prompt,
                "tools": tools,
                "llm_config": llm_config,
                "tokenguard_config": {
                    "confidence_threshold": self.config.confidence_threshold,
                    "max_length": 1000
                }
            }

            response = self.session.post(
                f"{self.config.base_url}/v1/generate-with-tools",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                self._update_metrics(result, response.elapsed.total_seconds())
                return result
            else:
                return {"error": f"Tool generation failed: {response.status_code}"}

        except Exception as e:
            return {"error": f"Tool generation request failed: {e}"}

    def get_metrics(self: Any) -> Dict[str, Any]:
        """Get integration metrics."""
        return {
            **self.metrics,
            "service_available": self.is_service_available()
        }

    def _update_metrics(self: Any, result: Dict[str, Any], response_time: float) -> Any:
        """Update internal metrics."""
        self.metrics["requests_total"] += 1
        self.metrics["avg_response_time"] = (
            (self.metrics["avg_response_time"] * (self.metrics["requests_total"] - 1)) +
            response_time
        ) / self.metrics["requests_total"]

        if result.get("action") == "prune":
            self.metrics["pruned_responses"] += 1
            original_len = result.get("original_length", 0)
            pruned_len = result.get("pruned_length", 0)
            self.metrics["tokens_saved"] += max(0, original_len - pruned_len)

    def _fallback_response(self: Any, text: str, confidence: float) -> Dict[str, Any]:
        """Fallback response when service is unavailable."""
        return {
            "action": "keep",
            "reason": "TokenGuard service unavailable - keeping original response",
            "confidence": confidence,
            "original_length": len(text)
        }

# Convenience functions for easy integration
def create_tokenguard_client(base_url: str = DEFAULT_TOKENGUARD_URL,
                           api_key: str = None) -> TokenGuardCopilotClient:
    """Create a TokenGuard client for Copilot integration."""
    config = TokenGuardConfig(
        base_url=base_url,
        api_key=api_key,
        auto_prune=True
    )
    return TokenGuardCopilotClient(config)

def optimize_ai_response(text: str, confidence: float,
                        tokenguard_url: str = DEFAULT_TOKENGUARD_URL) -> str:
    """
    Quick utility to optimize a single AI response.

    Returns the optimized text (pruned if confidence is low).
    """
    client = create_tokenguard_client(tokenguard_url)
    result = client.optimize_response(text, confidence)

    if result["action"] == "prune":
        return result.get("pruned_text", text)
    return text