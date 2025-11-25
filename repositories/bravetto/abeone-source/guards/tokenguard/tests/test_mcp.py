from typing import Any
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

# Create a client for testing
client = TestClient(app)

# --- Test Cases ---

def test_mcp_initialize() -> Any:
    """Test MCP initialization."""
    request_payload = {
        "method": "initialize",
        "params": {}
    }

    response = client.post("/mcp", json=request_payload)

    # Note: This will only work if MCP mode is enabled
    # In standard mode, this endpoint might not exist
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert "protocolVersion" in data["result"]
        assert "capabilities" in data["result"]
    else:
        # In non-MCP mode, expect 404 or similar
        assert response.status_code in [404, 405]


def test_mcp_tools_list() -> Any:
    """Test MCP tools list."""
    request_payload = {
        "method": "tools/list",
        "params": {}
    }

    response = client.post("/mcp", json=request_payload)

    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert "tools" in data["result"]
        tools = data["result"]["tools"]

        # Should have our TokenGuard tools
        tool_names = [tool["name"] for tool in tools]
        assert "prune_text" in tool_names
        assert "analyze_confidence" in tool_names
        assert "generate_with_pruning" in tool_names
    else:
        assert response.status_code in [404, 405]


def test_mcp_tools_call_prune_text() -> Any:
    """Test MCP tool call for prune_text."""
    request_payload = {
        "method": "tools/call",
        "params": {
            "name": "prune_text",
            "arguments": {
                "text": "This is a very long text that should be pruned because it exceeds normal length limits for testing purposes.",
                "confidence_threshold": 0.8
            }
        }
    }

    response = client.post("/mcp", json=request_payload)

    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        result = data["result"]
        assert "original_text" in result
        assert "decision" in result
        assert "should_prune" in result
    else:
        assert response.status_code in [404, 405]


def test_mcp_tools_call_analyze_confidence() -> Any:
    """Test MCP tool call for analyze_confidence."""
    request_payload = {
        "method": "tools/call",
        "params": {
            "name": "analyze_confidence",
            "arguments": {
                "text": "Sample text for confidence analysis",
                "logprobs_stream": [
                    {"token": "Sample", "logprob": -0.1, "top_logprobs": []},
                    {"token": " text", "logprob": -0.2, "top_logprobs": []}
                ]
            }
        }
    }

    response = client.post("/mcp", json=request_payload)

    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        result = data["result"]
        assert "text" in result
        assert "confidence_score" in result
        assert "interpretation" in result
    else:
        assert response.status_code in [404, 405]


def test_mcp_tools_call_generate_with_pruning() -> Any:
    """Test MCP tool call for generate_with_pruning."""
    request_payload = {
        "method": "tools/call",
        "params": {
            "name": "generate_with_pruning",
            "arguments": {
                "prompt": "Write a short summary",
                "model": "gpt-4",
                "max_tokens": 50,
                "confidence_threshold": 0.7,
                "max_length": 200
            }
        }
    }

    response = client.post("/mcp", json=request_payload)

    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        result = data["result"]
        assert "generated_text" in result
        assert "stop_reason" in result
        assert "final_confidence" in result
        assert "token_usage" in result
    else:
        assert response.status_code in [404, 405]


def test_mcp_unknown_method() -> Any:
    """Test MCP unknown method handling."""
    request_payload = {
        "method": "unknown_method",
        "params": {}
    }

    response = client.post("/mcp", json=request_payload)

    if response.status_code == 400:
        data = response.json()
        assert "detail" in data
        assert "Unknown method" in data["detail"]
    else:
        assert response.status_code in [404, 405]


def test_mcp_unknown_tool() -> Any:
    """Test MCP unknown tool handling."""
    request_payload = {
        "method": "tools/call",
        "params": {
            "name": "unknown_tool",
            "arguments": {}
        }
    }

    response = client.post("/mcp", json=request_payload)

    if response.status_code == 400:
        data = response.json()
        assert "detail" in data
        assert "Unknown tool" in data["detail"]
    else:
        assert response.status_code in [404, 405]