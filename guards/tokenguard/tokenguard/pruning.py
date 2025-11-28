# tokenguard/pruning.py
"""
TokenGuard Core Pruning Logic

This module contains the core confidence analysis and response pruning algorithms
extracted from the Local Assistant codebase.
"""

import numpy as np
import logging
from typing import Dict, List, Any, Tuple, Optional
from .config import config
import asyncio
from .llm_client import LLMClient
from .models import (
    GenerateRequest, GenerateResponse, ConversationBuffer,
    ContextualTokenMetrics, ContextPattern, CompressionTrend,
    SemanticPattern, CompressionStrategy
)
import httpx
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TokenGuardPruner:
    """
    TokenGuard pruner for intelligent response truncation based on confidence analysis.
    """

    def __init__(
        self: Any,
        uncertainty_threshold: Optional[float] = None,
        check_interval_tokens: Optional[int] = None,
        trailing_tokens_window: Optional[int] = None,
        length_threshold: Optional[int] = None,
        confidence_threshold: Optional[float] = None,
    ):
        """
        Initialize the TokenGuard pruner with validation.

        Args:
            uncertainty_threshold: Threshold for uncertainty scoring (defaults to config)
            check_interval_tokens: How often to check confidence (defaults to config)
            trailing_tokens_window: Number of recent tokens to analyze (defaults to config)
            length_threshold: Maximum response length before truncation (defaults to config)
            confidence_threshold: Minimum confidence required (defaults to config)

        Raises:
            ValueError: If any parameter is out of valid range
        """
        try:
            self.uncertainty_threshold = (
                uncertainty_threshold
                if uncertainty_threshold is not None
                else config.uncertainty_threshold
            )
            self.check_interval_tokens = (
                check_interval_tokens
                if check_interval_tokens is not None
                else config.check_interval_tokens
            )
            self.trailing_tokens_window = (
                trailing_tokens_window
                if trailing_tokens_window is not None
                else config.trailing_tokens_window
            )
            self.length_threshold = (
                length_threshold if length_threshold is not None else config.max_length
            )
            self.confidence_threshold = (
                confidence_threshold
                if confidence_threshold is not None
                else config.confidence_threshold
            )

            # Validate parameters
            if not 0.0 <= self.uncertainty_threshold <= 1.0:
                raise ValueError(
                    f"uncertainty_threshold must be between 0.0 and 1.0, got {self.uncertainty_threshold}"
                )
            if not 0.0 <= self.confidence_threshold <= 1.0:
                raise ValueError(
                    f"confidence_threshold must be between 0.0 and 1.0, got {self.confidence_threshold}"
                )
            if self.check_interval_tokens < 1:
                raise ValueError(
                    f"check_interval_tokens must be positive, got {self.check_interval_tokens}"
                )
            if self.trailing_tokens_window < 1:
                raise ValueError(
                    f"trailing_tokens_window must be positive, got {self.trailing_tokens_window}"
                )
            if self.length_threshold < 1:
                raise ValueError(f"length_threshold must be positive, got {self.length_threshold}")

            logger.debug(
                f"TokenGuardPruner initialized with confidence_threshold={self.confidence_threshold}, "
                f"length_threshold={self.length_threshold}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize TokenGuardPruner: {e}")
            raise

    def analyze_token_stream_confidence(self: Any, logprobs_stream: List[Dict[str, Any]]) -> float:
        """
        Analyzes the uncertainty of a token stream based on confidence analysis.
        Returns a confidence score between 0.0 (low confidence) and 1.0 (high confidence).

        Args:
            logprobs_stream: List of log probability dictionaries from LLM

        Returns:
            Confidence score between 0.0 and 1.0

        Raises:
            ValueError: If logprobs_stream contains invalid data
        """
        try:
            if not logprobs_stream:
                logger.debug("Empty logprobs_stream, returning high confidence")
                return 1.0  # High confidence if no data

            if not isinstance(logprobs_stream, list):
                raise ValueError(f"logprobs_stream must be a list, got {type(logprobs_stream)}")

            # Extract the sum of probabilities of *alternative* tokens for the last few steps
            uncertainty_scores = []
            window_size = min(len(logprobs_stream), self.trailing_tokens_window)

            for logprob_step in logprobs_stream[-window_size:]:
                if not isinstance(logprob_step, dict):
                    logger.warning(f"Invalid logprob_step format: {type(logprob_step)}")
                    continue

                top_logprobs = logprob_step.get("top_logprobs", [])

                if not isinstance(top_logprobs, list):
                    logger.warning(f"Invalid top_logprobs format: {type(top_logprobs)}")
                    continue

                if len(top_logprobs) > 1:
                    try:
                        # Sum the probabilities of all tokens *except* the chosen one
                        alternative_probs = []
                        for lp in top_logprobs[1:]:
                            if isinstance(lp, dict) and "logprob" in lp:
                                prob = np.exp(lp["logprob"])
                                if 0.0 <= prob <= 1.0:  # Validate probability range
                                    alternative_probs.append(prob)
                                else:
                                    logger.warning(f"Invalid probability value: {prob}")

                        uncertainty_scores.append(sum(alternative_probs))
                    except (ValueError, TypeError, OverflowError) as e:
                        logger.warning(f"Error processing logprobs: {e}")
                        uncertainty_scores.append(0.0)
                else:
                    uncertainty_scores.append(0.0)  # No alternatives, very certain

            if not uncertainty_scores:
                logger.warning("No valid uncertainty scores computed, returning default confidence")
                return 0.5  # Return neutral confidence if no valid data

            avg_uncertainty = np.mean(uncertainty_scores)

            # Convert uncertainty to confidence score (higher uncertainty = lower confidence)
            # Scale so that uncertainty_threshold corresponds to 0.5 confidence
            confidence_score = max(0.0, 1.0 - (avg_uncertainty / self.uncertainty_threshold))

            result = min(1.0, max(0.0, confidence_score))  # Clamp to [0, 1]
            logger.debug(
                f"Computed confidence score: {result:.3f} from {len(uncertainty_scores)} tokens"
            )
            return result

        except Exception as e:
            logger.error(f"Error in analyze_token_stream_confidence: {e}")
            return 0.5  # Return neutral confidence on error

    def should_prune(self: Any, text: str, confidence: float, context_metrics: Optional["ContextualTokenMetrics"] = None) -> Dict[str, Any]:
        """
        Determine if a response should be pruned based on confidence, length, and context awareness.

        Args:
            text: The response text to analyze
            confidence: Confidence score (0.0 to 1.0)
            context_metrics: Optional enhanced context metrics for adaptive thresholding

        Returns:
            Dict with 'action' ('prune' or 'keep'), 'confidence', and optional 'reason'

        Raises:
            ValueError: If inputs are invalid
        """
        try:
            if not isinstance(text, str):
                raise ValueError(f"text must be a string, got {type(text)}")

            if not isinstance(confidence, (int, float)):
                raise ValueError(f"confidence must be a number, got {type(confidence)}")

            if not 0.0 <= confidence <= 1.0:
                logger.warning(f"Confidence {confidence} outside valid range [0,1], clamping")
                confidence = max(0.0, min(1.0, confidence))

            text_length = len(text)
            logger.debug(f"Analyzing text: length={text_length}, confidence={confidence:.3f}")

            # Get adaptive threshold from context if available
            effective_threshold = self.confidence_threshold
            if context_metrics:
                effective_threshold = context_metrics.adaptive_threshold
                logger.debug(f"Using adaptive threshold: {effective_threshold:.3f}")

            # Check if pruning conditions are met with adaptive logic
            should_prune_response = (
                confidence < effective_threshold or text_length > self.length_threshold
            )

            # Context-aware pruning: be more lenient for high-semantic-density content
            if context_metrics and context_metrics.semantic_density > 0.7 and confidence >= effective_threshold * 0.8:
                should_prune_response = text_length > self.length_threshold * 1.5  # More lenient threshold
                logger.debug("Applying semantic density adjustment - more lenient pruning")

            if should_prune_response:
                # Calculate if pruning would actually save characters with context awareness
                max_length = max(50, int(self.length_threshold * 0.7))  # Ensure minimum length

                # Adjust target length based on context
                if context_metrics and context_metrics.semantic_density > 0.8:
                    max_length = int(max_length * 1.2)  # Preserve more for dense content

                truncation_message = "\n\n[Response truncated by NeuroForge TokenGuard for efficiency]"

                if text_length > max_length + len(truncation_message):
                    reason_parts = []
                    if confidence < effective_threshold:
                        reason_parts.append(
                            f"low confidence ({confidence:.2f} < {effective_threshold:.2f})"
                        )
                    if text_length > self.length_threshold:
                        reason_parts.append(
                            f"excessive length ({text_length} > {self.length_threshold} chars)"
                        )

                    result = {
                        "action": "prune",
                        "confidence": confidence,
                        "reason": " and ".join(reason_parts),
                        "target_length": max_length,
                        "original_length": text_length,
                        "estimated_savings": text_length - max_length - len(truncation_message),
                        "context_aware": context_metrics is not None,
                        "adaptive_threshold_used": effective_threshold
                    }

                    logger.info(f"Pruning recommended: {result['reason']}")
                    return result
                else:
                    result = {
                        "action": "keep",
                        "confidence": confidence,
                        "reason": "Pruning would not save significant characters",
                        "original_length": text_length,
                    }

                    logger.debug("Pruning not beneficial despite triggers")
                    return result
            else:
                result = {
                    "action": "keep",
                    "confidence": confidence,
                    "reason": f"High confidence ({confidence:.2f}) and acceptable length ({text_length} chars)",
                    "original_length": text_length,
                    "context_aware": context_metrics is not None,
                    "adaptive_threshold_used": effective_threshold
                }

                logger.debug("No pruning needed")
                return result

        except Exception as e:
            logger.error(f"Error in should_prune: {e}")
            # Safe fallback - keep the text
            return {
                "action": "keep",
                "confidence": confidence if isinstance(confidence, (int, float)) else 0.5,
                "reason": f"Error in analysis: {e}",
                "error": True,
            }

    def apply_pruning(self: Any, text: str, prune_decision: Dict[str, Any]) -> Tuple[str, bool]:
        """
        Apply the pruning decision to the text with error handling.

        Args:
            text: Original text
            prune_decision: Decision from should_prune()

        Returns:
            Tuple of (pruned_text, was_pruned)

        Raises:
            ValueError: If inputs are invalid
        """
        try:
            if not isinstance(text, str):
                raise ValueError(f"text must be a string, got {type(text)}")

            if not isinstance(prune_decision, dict):
                raise ValueError(f"prune_decision must be a dict, got {type(prune_decision)}")

            if "action" not in prune_decision:
                raise ValueError("prune_decision must contain 'action' key")

            action = prune_decision["action"]

            if action == "prune":
                target_length = prune_decision.get("target_length")
                if target_length is None:
                    logger.warning("No target_length in prune_decision, using default")
                    target_length = max(50, int(len(text) * 0.7))

                if not isinstance(target_length, int) or target_length < 0:
                    raise ValueError(f"Invalid target_length: {target_length}")

                if target_length >= len(text):
                    logger.warning(
                        f"target_length ({target_length}) >= text length ({len(text)}), not pruning"
                    )
                    return text, False

                truncation_message = "\n\n[Response truncated by TokenGuard for efficiency]"

                # Truncate at sentence boundary if possible
                truncated_text = text[:target_length]

                # Try to find a sentence ending near the truncation point
                sentence_endings = [".", "!", "?", "\n"]
                best_end_pos = -1
                min_acceptable_length = max(10, int(target_length * 0.5))  # Don't cut too short

                for end_char in sentence_endings:
                    last_pos = truncated_text.rfind(end_char)
                    if last_pos >= min_acceptable_length:
                        best_end_pos = max(best_end_pos, last_pos)

                if best_end_pos > -1:
                    truncated_text = truncated_text[: best_end_pos + 1]
                    logger.debug(f"Found sentence boundary at position {best_end_pos}")

                pruned_text = truncated_text + truncation_message

                logger.info(f"Text pruned from {len(text)} to {len(pruned_text)} characters")
                return pruned_text, True

            elif action == "keep":
                logger.debug("Keeping text unchanged")
                return text, False

            else:
                logger.warning(f"Unknown action '{action}', keeping text unchanged")
                return text, False

        except Exception as e:
            logger.error(f"Error in apply_pruning: {e}")
            # Safe fallback - return original text
            return text, False

    async def generate_and_prune(self: Any, request: GenerateRequest) -> GenerateResponse:
        """
        Generates text using an LLM and prunes it in real-time based on confidence.
        """
        # Augment prompt with context from ContextGuard if URL provided
        prompt = request.prompt
        guidelines = ""
        if request.context_guard_url:
            try:
                # Retrieve analysis and guidelines from ContextGuard
                async with httpx.AsyncClient() as client:
                    # Get analysis
                    response = await client.get(f"{request.context_guard_url}/memory/neuromorphic_analysis", timeout=5.0)
                    if response.status_code == 200:
                        data = response.json()
                        analysis = data.get("value", "")
                        # Simple retrieval: check if query words in analysis
                        query_words = prompt.lower().split()
                        relevant_parts = [part for part in analysis.split('\n') if any(word in part.lower() for word in query_words)]
                        context = '\n'.join(relevant_parts[:5])  # Limit to 5 relevant lines
                        if context:
                            prompt = f"Context from codebase: {context}\n\n{prompt}"
                            logger.info("Augmented prompt with ContextGuard data")
                    
                    # Get guidelines
                    response = await client.get(f"{request.context_guard_url}/memory/ai_guidelines", timeout=5.0)
                    if response.status_code == 200:
                        data = response.json()
                        guidelines = data.get("value", "")
                        if guidelines:
                            prompt = f"Follow these AI guidelines: {guidelines[:1000]}\n\n{prompt}"
                            logger.info("Included AI guidelines in prompt")
            except Exception as e:
                logger.warning(f"Failed to retrieve context from ContextGuard: {e}")

        llm_client = LLMClient()
        full_text = ""
        last_confidence = 1.0
        stop_reason = "eos_token"  # End of sequence
        token_count = 0

        try:
            # Use model dump for llm_config
            llm_config_dict = request.llm_config.model_dump()
            stream = llm_client.agenerate_stream(prompt, llm_config_dict)

            async for chunk in stream:
                if chunk.get('choices'):
                    choice = chunk['choices'][0]

                    # Handle content delta
                    if choice.get('delta') and choice['delta'].get('content'):
                        full_text += choice['delta']['content']
                        token_count += 1

                    # Handle logprobs
                    if choice.get('logprobs') and choice['logprobs'].get('content'):
                        logprobs_content = choice['logprobs']['content']
                        if logprobs_content:
                            confidence = self.analyze_token_stream_confidence(logprobs_content)
                            last_confidence = confidence

                            if confidence < request.tokenguard_config.confidence_threshold:
                                stop_reason = "confidence_threshold"
                                logger.info(f"Stopping generation due to low confidence: {confidence}")
                                break

                # Check max length
                if len(full_text) > request.tokenguard_config.max_length:
                    stop_reason = "max_length"
                    logger.info(f"Stopping generation due to exceeding max length: {len(full_text)}")
                    break

        except Exception as e:
            logger.error(f"Error during LLM stream generation: {e}", exc_info=True)
            stop_reason = "error"

        return GenerateResponse(
            text=full_text,
            stop_reason=stop_reason,
            confidence=last_confidence,
            token_usage={"generated_tokens": token_count}
        )

    async def generate_with_tools(self: Any, request: GenerateRequest, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates text with tool calling capabilities and applies real-time confidence-based pruning.

        Args:
            request: Generation request with prompt and configuration
            tools: List of available tools for the LLM to use

        Returns:
            Dict containing generated text, confidence, tool calls, and metadata

        Raises:
            Exception: If generation fails
        """
        from .llm_client import LLMClient
        from .models import ToolCall

        llm_client = LLMClient()
        full_text = ""
        last_confidence = 1.0
        stop_reason = "eos_token"
        token_count = 0
        tool_calls = []

        try:
            # Use model dump for llm_config
            llm_config_dict = request.llm_config.model_dump()
            stream = llm_client.agenerate_stream_aclosing(request.prompt, llm_config_dict, tools=tools)

            async for chunk in stream:
                if chunk.get('choices'):
                    choice = chunk['choices'][0]

                    # Handle content delta
                    if choice.get('delta') and choice['delta'].get('content'):
                        full_text += choice['delta']['content']
                        token_count += 1

                    # Handle tool calls
                    if choice.get('delta') and choice['delta'].get('tool_calls'):
                        tool_call_delta = choice['delta']['tool_calls']
                        # Handle tool call deltas (simplified - in practice you'd accumulate them)
                        for tool_call in tool_call_delta:
                            if tool_call.get('function'):
                                tool_calls.append(ToolCall(
                                    id=tool_call.get('id', ''),
                                    type='function',
                                    function=tool_call['function']
                                ))

                    # Handle logprobs
                    if choice.get('logprobs') and choice['logprobs'].get('content'):
                        logprobs_content = choice['logprobs']['content']
                        if logprobs_content:
                            confidence = self.analyze_token_stream_confidence(logprobs_content)
                            last_confidence = confidence

                            if confidence < request.tokenguard_config.confidence_threshold:
                                stop_reason = "confidence_threshold"
                                logger.info(f"Stopping generation due to low confidence: {confidence}")
                                break

                # Check max length
                if len(full_text) > request.tokenguard_config.max_length:
                    stop_reason = "max_length"
                    logger.info(f"Stopping generation due to exceeding max length: {len(full_text)}")
                    break

        except Exception as e:
            logger.error(f"Error during tool call generation: {e}", exc_info=True)
            stop_reason = "error"




def should_prune(
    text_stream: str, confidence_threshold: float
) -> Dict[str, Any]:
    """
    Convenience function for simple pruning decisions.

    Args:
        text_stream: The text to analyze
        confidence_threshold: Minimum confidence required (0.0-1.0)

    Returns:
        Dict with pruning decision
    """
    pruner = TokenGuardPruner(confidence_threshold=confidence_threshold)
    return pruner.should_prune(text_stream, 1.0)  # Assume high confidence for simple text analysis


class ConversationContextAnalyzer:
    """Analyzes conversation history for compression optimization patterns."""

    def __init__(self: Any, buffer: ConversationBuffer):
        self.buffer = buffer
        self.patterns: Dict[str, ContextPattern] = {}
        self.compression_trends: List[CompressionTrend] = []
        self.semantic_patterns: Dict[str, SemanticPattern] = {}

    def analyze_conversation_context(self: Any) -> ContextualTokenMetrics:
        """
        Analyze current conversation state for compression opportunities.

        Returns:
            Enhanced token metrics with context awareness
        """
        conversation_tokens = self._count_conversation_tokens()
        semantic_density = self._calculate_semantic_density()
        patterns = self._detect_active_patterns()

        # Calculate adaptive threshold based on context
        base_threshold = config.confidence_threshold
        adaptive_threshold = self._calculate_adaptive_threshold(
            base_threshold, patterns, semantic_density
        )

        return ContextualTokenMetrics(
            conversation_tokens=conversation_tokens,
            compressed_tokens=int(conversation_tokens * 0.4),  # Estimated 60% compression
            semantic_density=semantic_density,
            neural_efficiency=0.85,  # Placeholder neural efficiency score
            adaptive_threshold=adaptive_threshold,
            trend_predictions=self._predict_compression_gains(),
            context_patterns=patterns
        )

    def _count_conversation_tokens(self: Any) -> int:
        """Count total tokens in conversation history."""
        total_tokens = 0
        for message in self.buffer.messages[-10:]:  # Last 10 messages
            if "content" in message:
                # Rough token estimation (characters / 4)
                total_tokens += len(message["content"]) // 4
        return total_tokens

    def _calculate_semantic_density(self: Any) -> float:
        """Calculate semantic richness of conversation."""
        if not self.buffer.messages:
            return 0.5

        # Calculate semantic density using basic heuristics
        recent_messages = self.buffer.messages[-5:]  # Last 5 messages

        # Check for code, technical terms, URLs
        technical_indicators = 0
        for msg in recent_messages:
            content = msg.get("content", "").lower()
            if any(keyword in content for keyword in ["code", "function", "class", "import", "api", "http", ".py", ".js"]):
                technical_indicators += 1

        # Calculate density based on technical content ratio
        density = min(1.0, 0.3 + (technical_indicators / len(recent_messages)) * 0.7)
        return density

    def _detect_active_patterns(self: Any) -> List[ContextPattern]:
        """Detect currently active compression patterns."""
        active_patterns = []

        if len(self.buffer.messages) >= 3:
            # Check for repetitive question patterns
            recent_questions = [
                msg for msg in self.buffer.messages[-5:]
                if msg.get("content", "").strip().endswith("?")
            ]
            if len(recent_questions) >= 2:
                pattern_id = f"repetitive_questions_{len(recent_questions)}"
                active_patterns.append(ContextPattern(
                    pattern_id=pattern_id,
                    pattern_type="repetitive_questions",
                    frequency=len(recent_questions),
                    confidence=0.8,
                    tokens_saved=len(recent_questions) * 20  # Estimate
                ))

        return active_patterns

    def _calculate_adaptive_threshold(self: Any, base_threshold: float, patterns: List[ContextPattern],
                                    semantic_density: float) -> float:
        """Calculate adaptive confidence threshold based on context."""
        adjustment = 0.0

        # Increase threshold for technical conversations (allow less certain but relevant responses)
        if semantic_density > 0.7:
            adjustment += 0.1

        # Adjust based on active patterns
        for pattern in patterns:
            if pattern.pattern_type == "repetitive_questions":
                adjustment += 0.05

        # Ensure threshold stays within reasonable bounds
        adaptive = min(0.9, max(0.5, base_threshold + adjustment))
        return adaptive

    def _predict_compression_gains(self: Any) -> Dict[str, float]:
        """Predict expected compression gains based on trends."""
        predictions = {}

        # Analyze recent trends
        if len(self.compression_trends) >= 3:
            recent_ratios = [trend.compression_ratio for trend in self.compression_trends[-3:]]
            avg_ratio = np.mean(recent_ratios)

            predictions["expected_compression_ratio"] = avg_ratio
            predictions["predicted_token_savings"] = (1 - avg_ratio) * 100

        return predictions

    def update_trends(self: Any, new_trend: CompressionTrend) -> None:
        """Update compression trends with new data."""
        self.compression_trends.append(new_trend)

        # Keep only recent trends (last 24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        self.compression_trends = [
            trend for trend in self.compression_trends
            if trend.timestamp > cutoff
        ]


class PredictiveCompressionPredictor:
    """Predictive model for optimal compression strategies."""

    def __init__(self: Any):
        self.historical_data: List[Dict[str, Any]] = []

    def predict_optimal_strategy(self: Any, context: ContextualTokenMetrics) -> CompressionStrategy:
        """
        Predict optimal compression strategy for current context.

        Returns:
            Recommended compression strategy
        """
        # Adjust thresholds based on semantic density
        confidence_threshold = 0.75
        uncertainty_threshold = 0.25

        # For high semantic density contexts, be more aggressive
        if context.semantic_density > 0.7:
            confidence_threshold = 0.8
            uncertainty_threshold = 0.3
        elif context.semantic_density < 0.3:
            confidence_threshold = 0.7
            uncertainty_threshold = 0.2

        # Factor in active patterns
        pattern_weights = {}
        for pattern in context.context_patterns:
            pattern_weights[pattern.pattern_id] = min(2.0, pattern.frequency * 0.2)

        # Calculate expected compression based on neural efficiency
        expected_compression = 0.4 + (context.neural_efficiency * 0.4)

        return CompressionStrategy(
            strategy_id=f"dynamic_{len(self.historical_data)}",
            confidence_threshold=confidence_threshold,
            uncertainty_threshold=uncertainty_threshold,
            pattern_weights=pattern_weights,
            expected_compression=expected_compression,
            neural_activation_cost=context.neural_efficiency * 0.1
        )

    def update_model(self: Any, feedback: Dict[str, Any]) -> None:
        """Update prediction model with feedback."""
        self.historical_data.append({
            "timestamp": datetime.now(),
            "feedback": feedback
        })

        # Limit historical data size
        if len(self.historical_data) > 100:
            self.historical_data = self.historical_data[-100:]


class SemanticExtractor:
    """Extract semantic patterns for compression optimization."""

    def __init__(self: Any):
        self.pattern_cache: Dict[str, SemanticPattern] = {}

    def extract_semantic_patterns(self: Any, text: str) -> List[SemanticPattern]:
        """Extract semantic patterns from text content."""
        patterns = []

        # Calculate semantic density based on content analysis
        words = text.split()
        total_words = len(words)

        # Technical content indicators
        tech_indicators = sum(1 for word in words if any(
            keyword in word.lower() for keyword in
            ["code", "function", "class", "import", "api", "error", "debug"]
        ))

        semantic_density = min(1.0, tech_indicators / max(1, total_words))

        # Calculate compressibility based on semantic density
        compressibility = 0.3 + (semantic_density * 0.4)  # Higher density = more compressible

        # Determine optimal context window
        context_window = 2048 if semantic_density > 0.5 else 4096

        pattern_hash = hash(text[:100])  # Simple hash for pattern identification

        pattern = SemanticPattern(
            pattern_hash=str(pattern_hash),
            semantic_density=semantic_density,
            compressibility_score=compressibility,
            context_window=context_window,
            neural_efficiency=0.8 + (semantic_density * 0.2)
        )

        patterns.append(pattern)
        return patterns
