"""
Pydantic models for TokenGuard API requests and responses.
Enhanced with neuromorphic compression and dynamic optimization capabilities.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class LLMConfig(BaseModel):
    """Configuration for the Language Model."""
    model: str = Field(..., description="The model to use for generation, e.g., 'gpt-4'.")
    max_tokens: int = Field(4096, description="The maximum number of tokens to generate.")


class TokenGuardConfig(BaseModel):
    """Configuration for TokenGuard's behavior."""
    confidence_threshold: float = Field(
        0.75, ge=0.0, le=1.0, description="The confidence threshold to stop generation."
    )
    max_length: int = Field(
        3000, gt=0, description="The maximum length of the generated text in characters."
    )


class GenerateRequest(BaseModel):
    """Request body for the /v1/generate endpoint."""
    prompt: str = Field(..., description="The user's initial prompt for the LLM.")
    llm_config: LLMConfig = Field(..., description="Configuration for the LLM.")
    tokenguard_config: TokenGuardConfig = Field(..., description="Configuration for TokenGuard.")
    context_guard_url: Optional[str] = Field(None, description="URL of ContextGuard service for RAG retrieval.")


class GenerateResponse(BaseModel):
    """Response body for the /v1/generate endpoint."""
    text: str = Field(..., description="The generated text from the LLM.")
    stop_reason: str = Field(
        ...,
        description="The reason why the generation was stopped (e.g., 'confidence_threshold', 'max_length', 'eos_token').",
    )
    confidence: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="The final confidence score when generation stopped."
    )
    token_usage: Dict[str, Any] = Field({}, description="Token usage statistics.")


# Enhanced TokenGuard Types for NeuroForge Integration
class ContextPattern(BaseModel):
    """Identified pattern in conversation context."""
    pattern_id: str = Field(..., description="Unique identifier for the pattern")
    pattern_type: str = Field(..., description="Type of pattern (repetitive_questions, command_sequences, error_patterns)")
    frequency: int = Field(..., description="How many times this pattern has been observed")
    confidence: float = Field(..., description="Confidence in pattern recognition")
    tokens_saved: int = Field(default=0, description="Tokens saved by this pattern recognition")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional pattern metadata")


class SemanticPattern(BaseModel):
    """Semantic density pattern for compression optimization."""
    pattern_hash: str = Field(..., description="Hash identifier for semantic pattern")
    semantic_density: float = Field(..., description="Depth of semantic content (0.0-1.0)")
    compressibility_score: float = Field(..., description="How compressible this semantic type is")
    context_window: int = Field(..., description="Optimal context window for this pattern")
    neural_efficiency: float = Field(..., description="Neural processing efficiency score")


class CompressionTrend(BaseModel):
    """Historical compression trend analysis."""
    timestamp: datetime = Field(..., description="When this trend was observed")
    conversation_tokens: int = Field(..., description="Original conversation token count")
    compressed_tokens: int = Field(..., description="Compressed token count")
    compression_ratio: float = Field(..., description="Ratio of compressed/original tokens")
    context_patterns: List[str] = Field(default_factory=list, description="Active context patterns")
    prediction_accuracy: float = Field(..., description="Accuracy of compression prediction")


class ConversationBuffer(BaseModel):
    """Rolling buffer of conversation history for context analysis."""
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Recent conversation messages")
    max_size: int = Field(100, description="Maximum number of messages to retain")
    token_budget: int = Field(8000, description="Maximum tokens to maintain in buffer")
    current_tokens: int = Field(0, description="Current token usage")
    patterns_detected: List[ContextPattern] = Field(default_factory=list, description="Detected context patterns")


class ContextualTokenMetrics(BaseModel):
    """Enhanced TokenGuard metrics with neuromorphic awareness."""
    conversation_tokens: int = Field(..., description="Total tokens in current conversation")
    compressed_tokens: int = Field(..., description="Tokens after compression")
    semantic_density: float = Field(..., description="Average semantic density of content")
    neural_efficiency: float = Field(..., description="Neural processing efficiency score")
    adaptive_threshold: float = Field(..., description="Current adaptive confidence threshold")
    trend_predictions: Dict[str, float] = Field(default_factory=dict, description="Predicted compression outcomes")
    context_patterns: List[ContextPattern] = Field(default_factory=list, description="Active patterns in context")


class ModelProfile(BaseModel):
    """LLM model capabilities and optimization profile."""
    model_name: str = Field(..., description="Name of the LLM model")
    token_limit: int = Field(..., description="Maximum tokens supported")
    compression_baseline: float = Field(0.31, description="Current compression ratio baseline")
    context_window: int = Field(4096, description="Maximum context window")
    optimal_patterns: List[str] = Field(default_factory=list, description="Best performing compression patterns")


class CompressionStrategy(BaseModel):
    """Optimized compression strategy for current context."""
    strategy_id: str = Field(..., description="Unique strategy identifier")
    confidence_threshold: float = Field(..., description="Adaptive confidence threshold")
    uncertainty_threshold: float = Field(..., description="Adaptive uncertainty threshold")
    semantic_filters: List[str] = Field(default_factory=list, description="Semantic content filters")
    pattern_weights: Dict[str, float] = Field(default_factory=dict, description="Pattern-specific weights")
    expected_compression: float = Field(..., description="Predicted compression ratio")
    neural_activation_cost: float = Field(..., description="Estimated neural processing cost")


# Tool Call Models
class ToolDefinition(BaseModel):
    """Definition of a tool that can be called by the LLM."""
    type: str = Field("function", description="The type of tool (currently only 'function' is supported)")
    function: Dict[str, Any] = Field(..., description="Function definition with name, description, and parameters")


class ToolCall(BaseModel):
    """A tool call made by the LLM."""
    id: str = Field(..., description="Unique identifier for the tool call")
    type: str = Field("function", description="The type of tool call")
    function: Dict[str, Any] = Field(..., description="Function call details with name and arguments")


class ToolCallRequest(BaseModel):
    """Request body for tool call generation."""
    prompt: str = Field(..., description="The user's initial prompt for the LLM.")
    llm_config: LLMConfig = Field(..., description="Configuration for the LLM.")
    tokenguard_config: TokenGuardConfig = Field(..., description="Configuration for TokenGuard.")
    tools: List[ToolDefinition] = Field(default_factory=list, description="Available tools for the LLM to use")


class ToolCallResponse(BaseModel):
    """Response body for tool call generation."""
    text: str = Field(..., description="The generated text from the LLM.")
    stop_reason: str = Field(
        ...,
        description="The reason why the generation was stopped (e.g., 'confidence_threshold', 'max_length', 'eos_token', 'tool_calls').",
    )
    confidence: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="The final confidence score when generation stopped."
    )
    token_usage: Dict[str, Any] = Field({}, description="Token usage statistics.")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="Tool calls made during generation")


# MCP Models
class MCPTool(BaseModel):
    """MCP tool definition."""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    inputSchema: Dict[str, Any] = Field(..., description="JSON schema for tool input")


class MCPRequest(BaseModel):
    """MCP request model."""
    method: str = Field(..., description="MCP method to call")
    params: Dict[str, Any] = Field(default_factory=dict, description="Method parameters")


class MCPResponse(BaseModel):
    """MCP response model."""
    result: Dict[str, Any] = Field(default_factory=dict, description="Method result")
    error: Optional[Dict[str, Any]] = Field(None, description="Error information if any")


# Mode Configuration
class ServiceMode(str, Enum):
    """Service operating modes."""
    STANDARD = "standard"  # Original TokenGuard functionality
    TOOL_CALL = "tool_call"  # LLM tool calling mode
    MCP = "mcp"  # Model Context Protocol mode


class ModeConfig(BaseModel):
    """Configuration for service operating mode."""
    mode: ServiceMode = Field(ServiceMode.STANDARD, description="Operating mode for the service")
    mcp_server_name: str = Field("TokenGuard", description="Name for MCP server")
    mcp_server_version: str = Field("1.0.0", description="Version for MCP server")


# Enhanced TokenGuard Classes
class DynamicCompressionEngine:
    """Advanced compression with contextual awareness for neuromorphic optimization."""

    def __init__(self: Any, model_profile: "ModelProfile", conversation_history: "ConversationBuffer", semantic_extractor: "SemanticExtractor", prediction_engine: "CompressionPredictor", fallback_strategies: List["CompressionStrategy"]):
        self.model_profile = model_profile
        self.conversation_history = conversation_history
        self.semantic_extractor = semantic_extractor
        self.prediction_engine = prediction_engine
        self.fallback_strategies = fallback_strategies
        self.active_strategy = fallback_strategies[0] if fallback_strategies else None

    async def analyze_context(self: Any, current_prompt: str) -> ContextualTokenMetrics:
        """Analyze current context for compression opportunities."""
        # Placeholder for implementation
        return ContextualTokenMetrics(
            conversation_tokens=100,
            compressed_tokens=69,
            semantic_density=0.8,
            neural_efficiency=0.85,
            adaptive_threshold=0.75
        )

    def get_optimal_strategy(self: Any, context_analysis: ContextualTokenMetrics) -> CompressionStrategy:
        """Return optimal compression strategy based on context analysis."""
        # Placeholder for implementation
        return self.active_strategy or CompressionStrategy(
            strategy_id="baseline",
            confidence_threshold=0.75,
            uncertainty_threshold=0.25
        )


class ContextualOptimization:
    """Runtime optimization based on conversation context for enhanced compression."""

    def __init__(self: Any, semantic_patterns: List[SemanticPattern], token_efficiency: float, compression_trends: List[CompressionTrend], prediction_accuracy: float, adaptive_parameters: Dict[str, float]):
        self.semantic_patterns = semantic_patterns
        self.token_efficiency = token_efficiency
        self.compression_trends = compression_trends
        self.prediction_accuracy = prediction_accuracy
        self.adaptive_parameters = adaptive_parameters

    def predict_compression_gain(self: Any, context: "QueryContext") -> float:
        """Predict compression gain for given context."""
        # Placeholder for implementation
        return 0.5

    def update_parameters(self: Any, feedback: Dict[str, Any]) -> None:
        """Update optimization parameters based on feedback."""
        # Placeholder for implementation
        pass
