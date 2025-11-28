"""
MCP (Model Context Protocol) Server implementation for TokenGuard.
"""
import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from .models import MCPRequest, MCPResponse, MCPTool, ModeConfig
from .pruning import TokenGuardPruner
from .config import config

logger = logging.getLogger(__name__)


class MCPServer:
    """MCP Server for TokenGuard functionality."""

    def __init__(self: Any, mode_config: ModeConfig):
        self.mode_config = mode_config
        self.pruner = TokenGuardPruner()
        self.app = FastAPI(title=self.mode_config.mcp_server_name, version=self.mode_config.mcp_server_version)
        self._setup_routes()

    def _setup_routes(self: Any) -> Any:
        """Set up MCP routes."""

        @self.app.post("/mcp")
        async def handle_mcp_request(request: Request, mcp_request: MCPRequest) -> Any:
            """Handle MCP requests."""
            try:
                if mcp_request.method == "initialize":
                    return self._handle_initialize()
                elif mcp_request.method == "tools/list":
                    return self._handle_tools_list()
                elif mcp_request.method == "tools/call":
                    return await self._handle_tools_call(mcp_request)
                else:
                    raise HTTPException(status_code=400, detail=f"Unknown method: {mcp_request.method}")
            except Exception as e:
                logger.error(f"MCP request failed: {e}", exc_info=True)
                return MCPResponse(error={"code": -32000, "message": str(e)})

        @self.app.get("/status")
        async def get_status() -> Any:
            """Get server status and configuration."""
            return {
                "server": self.mode_config.mcp_server_name,
                "version": self.mode_config.mcp_server_version,
                "status": "running",
                "mode": self.mode_config.mode.value,
                "tools_available": len(self._handle_tools_list().result["tools"]),
                "confidence_threshold": self.pruner.confidence_threshold,
                "max_length": self.pruner.length_threshold
            }

        @self.app.get("/")
        async def root() -> Any:
            """Root endpoint with basic info."""
            return {
                "service": self.mode_config.mcp_server_name,
                "status": "running",
                "endpoints": {
                    "mcp": "/mcp",
                    "status": "/status"
                }
            }

    def _handle_initialize(self: Any) -> MCPResponse:
        """Handle MCP initialization."""
        return MCPResponse(
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": self.mode_config.mcp_server_name,
                    "version": self.mode_config.mcp_server_version
                }
            }
        )

    def _handle_tools_list(self: Any) -> MCPResponse:
        """Handle tools list request."""
        tools = [
            MCPTool(
                name="prune_text",
                description="Analyze and prune text based on confidence analysis. Reduces token usage while preserving response quality.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to analyze and potentially prune"
                        },
                        "confidence_threshold": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "default": 0.75,
                            "description": "Minimum confidence required (0.0-1.0)"
                        },
                        "max_length": {
                            "type": "integer",
                            "minimum": 1,
                            "default": 3000,
                            "description": "Maximum length of text in characters"
                        }
                    },
                    "required": ["text"]
                }
            ),
            MCPTool(
                name="analyze_confidence",
                description="Analyze the confidence of generated text using log probability streams.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to analyze"
                        },
                        "logprobs_stream": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "token": {"type": "string"},
                                    "logprob": {"type": "number"},
                                    "top_logprobs": {"type": "array"}
                                }
                            },
                            "description": "Log probability stream from LLM"
                        }
                    },
                    "required": ["text"]
                }
            ),
            MCPTool(
                name="generate_with_pruning",
                description="Generate text using an LLM with real-time confidence-based pruning.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The prompt for text generation"
                        },
                        "model": {
                            "type": "string",
                            "default": "gpt-4",
                            "description": "LLM model to use"
                        },
                        "max_tokens": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 4096,
                            "default": 4096,
                            "description": "Maximum tokens to generate"
                        },
                        "confidence_threshold": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "default": 0.75,
                            "description": "Confidence threshold for pruning"
                        },
                        "max_length": {
                            "type": "integer",
                            "minimum": 1,
                            "default": 3000,
                            "description": "Maximum text length in characters"
                        }
                    },
                    "required": ["prompt"]
                }
            )
        ]

        return MCPResponse(result={"tools": [tool.model_dump() for tool in tools]})

    async def _handle_tools_call(self: Any, request: MCPRequest) -> MCPResponse:
        """Handle tool call requests."""
        tool_name = request.params.get("name")
        tool_args = request.params.get("arguments", {})

        if tool_name == "prune_text":
            return self._call_prune_text(tool_args)
        elif tool_name == "analyze_confidence":
            return self._call_analyze_confidence(tool_args)
        elif tool_name == "generate_with_pruning":
            return await self._call_generate_with_pruning(tool_args)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")

    def _call_prune_text(self: Any, args: Dict[str, Any]) -> MCPResponse:
        """Call the prune_text tool."""
        text = args.get("text", "")
        confidence_threshold = args.get("confidence_threshold", 0.75)
        max_length = args.get("max_length", 3000)

        # Create a temporary pruner with custom settings
        temp_pruner = TokenGuardPruner(
            confidence_threshold=confidence_threshold,
            length_threshold=max_length
        )

        decision = temp_pruner.should_prune(text, 1.0)  # Assume high confidence for analysis

        result = {
            "original_text": text,
            "decision": decision,
            "should_prune": decision["action"] == "prune"
        }

        if decision["action"] == "prune":
            pruned_text, was_pruned = temp_pruner.apply_pruning(text, decision)
            result["pruned_text"] = pruned_text
            result["was_pruned"] = was_pruned

        return MCPResponse(result=result)

    def _call_analyze_confidence(self: Any, args: Dict[str, Any]) -> MCPResponse:
        """Call the analyze_confidence tool."""
        text = args.get("text", "")
        logprobs_stream = args.get("logprobs_stream", [])

        confidence = self.pruner.analyze_token_stream_confidence(logprobs_stream)

        if confidence >= 0.8:
            interpretation = "high_confidence"
        elif confidence >= 0.6:
            interpretation = "medium_confidence"
        else:
            interpretation = "low_confidence"

        return MCPResponse(result={
            "text": text,
            "confidence_score": confidence,
            "interpretation": interpretation
        })

    async def _call_generate_with_pruning(self: Any, args: Dict[str, Any]) -> MCPResponse:
        """Call the generate_with_pruning tool."""
        from .models import GenerateRequest, LLMConfig, TokenGuardConfig

        prompt = args.get("prompt", "")
        model = args.get("model", "gpt-4")
        max_tokens = args.get("max_tokens", 4096)
        confidence_threshold = args.get("confidence_threshold", 0.75)
        max_length = args.get("max_length", 3000)

        generate_request = GenerateRequest(
            prompt=prompt,
            llm_config=LLMConfig(model=model, max_tokens=max_tokens),
            tokenguard_config=TokenGuardConfig(
                confidence_threshold=confidence_threshold,
                max_length=max_length
            )
        )

        response = await self.pruner.generate_and_prune(generate_request)

        return MCPResponse(result={
            "generated_text": response.text,
            "stop_reason": response.stop_reason,
            "final_confidence": response.confidence,
            "token_usage": response.token_usage
        })

    def get_app(self: Any) -> FastAPI:
        """Get the FastAPI application."""
        return self.app
