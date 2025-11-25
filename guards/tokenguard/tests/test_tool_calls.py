from typing import Any
import pytest
import httpx
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from main import app

# Create a client for testing
client = TestClient(app)

# --- Mock Data and Helpers ---

def create_stream_chunk_with_tools(content: str, logprobs: list, tool_calls=None) -> Any:
    """Creates a mock stream chunk with tool calls."""
    chunk = {
        "choices": [
            {
                "delta": {"content": content},
                "logprobs": {
                    "content": [
                        {
                            "token": content,
                            "logprob": lp["logprob"],
                            "top_logprobs": lp["top_logprobs"],
                        }
                        for lp in logprobs
                    ]
                },
            }
        ]
    }

    if tool_calls:
        chunk["choices"][0]["delta"]["tool_calls"] = tool_calls

    return chunk

async def mock_openai_stream_with_tools(chunks: Any) -> Any:
    """Async generator to yield stream chunks with tool support."""
    for chunk in chunks:
        yield f"data: {json.dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"

# --- Test Cases ---

@pytest.mark.asyncio
@patch("tokenguard.llm_client.LLMClient.__init__", return_value=None)
@patch("tokenguard.llm_client.LLMClient.agenerate_stream_aclosing")
async def test_generate_with_tools_success(mock_agenerate_stream: Any, mock_llm_client_init) -> Any:
    """Test successful generation with tools."""
    # Arrange
    tool_calls = [
        {
            "id": "call_123",
            "type": "function",
            "function": {
                "name": "prune_text",
                "arguments": '{"text": "test text", "confidence_threshold": 0.8}'
            }
        }
    ]

    mock_chunks = [
        create_stream_chunk_with_tools("Hello", [{"logprob": -0.1, "top_logprobs": []}]),
        create_stream_chunk_with_tools(" world", [{"logprob": -0.2, "top_logprobs": []}], tool_calls),
    ]

    mock_agenerate_stream.return_value = mock_openai_stream_with_tools(mock_chunks)

    request_payload = {
        "prompt": "Test prompt",
        "llm_config": {
            "model": "gpt-4",
            "max_tokens": 100
        },
        "tokenguard_config": {
            "confidence_threshold": 0.7,
            "max_length": 1000
        },
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "prune_text",
                    "description": "Prune text based on confidence",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "confidence_threshold": {"type": "number"}
                        }
                    }
                }
            }
        ]
    }

    # Act
    response = client.post("/v1/generate-with-tools", json=request_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "tool_calls" in data
    assert len(data["tool_calls"]) > 0
    assert data["tool_calls"][0]["function"]["name"] == "prune_text"

    mock_agenerate_stream.assert_called_once()


@pytest.mark.asyncio
@patch("tokenguard.llm_client.LLMClient.__init__", return_value=None)
@patch("tokenguard.llm_client.LLMClient.agenerate_stream_aclosing")
async def test_generate_with_tools_no_tools(mock_agenerate_stream: Any, mock_llm_client_init) -> Any:
    """Test generation with empty tools list."""
    # Arrange
    mock_chunks = [
        create_stream_chunk_with_tools("Hello", [{"logprob": -0.1, "top_logprobs": []}]),
        create_stream_chunk_with_tools(" world", [{"logprob": -0.2, "top_logprobs": []}]),
    ]

    mock_agenerate_stream.return_value = mock_openai_stream_with_tools(mock_chunks)

    request_payload = {
        "prompt": "Test prompt",
        "llm_config": {
            "model": "gpt-4",
            "max_tokens": 100
        },
        "tokenguard_config": {
            "confidence_threshold": 0.7,
            "max_length": 1000
        },
        "tools": []
    }

    # Act
    response = client.post("/v1/generate-with-tools", json=request_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "tool_calls" in data
    assert len(data["tool_calls"]) == 0


@pytest.mark.asyncio
@patch("tokenguard.llm_client.LLMClient.agenerate_stream", new_callable=AsyncMock)
async def test_generate_with_tools_api_error(mock_agenerate_stream: Any, mock_llm_client_init) -> Any:
    """Test handling of API errors during tool generation."""
    # Arrange
    mock_agenerate_stream.side_effect = httpx.HTTPStatusError(
        "API Error", request=None, response=None
    )

    request_payload = {
        "prompt": "Test prompt",
        "llm_config": {
            "model": "gpt-4",
            "max_tokens": 100
        },
        "tokenguard_config": {
            "confidence_threshold": 0.7,
            "max_length": 1000
        },
        "tools": []
    }

    # Act
    response = client.post("/v1/generate-with-tools", json=request_payload)

    # Assert
    assert response.status_code == 500
    assert "error" in response.json() or "detail" in response.json()
