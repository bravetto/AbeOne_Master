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

def create_stream_chunk(content: str, logprobs: list) -> Any:
    """Creates a mock stream chunk in the OpenAI API format."""
    return {
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

def mock_openai_stream_response(chunks: Any) -> Any:
    """Generator to yield stream chunks."""
    for chunk in chunks:
        yield f"data: {json.dumps(chunk)}\n\n"
    yield "data: [DONE]\n\n"

# --- Test Cases ---

@pytest.mark.asyncio
@patch("tokenguard.llm_client.LLMClient.__init__", return_value=None)
@patch("tokenguard.llm_client.LLMClient.agenerate_stream")
async def test_generate_endpoint_success(mock_agenerate_stream: Any, mock_llm_client_init) -> Any:
    """Test successful generation without interruption."""
    # Arrange
    mock_chunks = [
        create_stream_chunk("Hello", [{"logprob": -0.1, "top_logprobs": []}]),
        create_stream_chunk(" world", [{"logprob": -0.2, "top_logprobs": []}]),
    ]

    async def stream_generator() -> Any:
        for chunk in mock_chunks:
            yield chunk

    mock_agenerate_stream.return_value = stream_generator()

    request_payload = {
        "prompt": "Say hello",
        "llm_config": {"model": "gpt-4", "max_tokens": 50},
        "tokenguard_config": {"confidence_threshold": 0.1, "max_length": 100},
    }

    # Act
    response = client.post("/v1/generate", json=request_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Hello world"
    assert data["stop_reason"] == "eos_token"
    assert data["confidence"] > 0.1  # Should be high
    mock_agenerate_stream.assert_called_once()


@pytest.mark.asyncio
@patch("tokenguard.llm_client.LLMClient.__init__", return_value=None)
@patch("tokenguard.llm_client.LLMClient.agenerate_stream")
async def test_generate_stops_on_low_confidence(mock_agenerate_stream: Any, mock_llm_client_init) -> Any:
    """Test that generation stops when confidence drops below the threshold."""
    # Arrange
    mock_chunks = [
        create_stream_chunk("This is good.", [{"logprob": -0.1, "top_logprobs": []}]),
        # This chunk has low probability alternatives, causing low confidence
        create_stream_chunk(
            "This is bad.",
            [
                {"logprob": -2.5, "top_logprobs": [
                    {"token": "bad", "logprob": -2.5},
                    {"token": "terrible", "logprob": -2.6},
                ]}
            ],
        ),
    ]

    async def stream_generator() -> Any:
        for chunk in mock_chunks:
            yield chunk

    mock_agenerate_stream.return_value = stream_generator()

    request_payload = {
        "prompt": "Give a mixed review.",
        "llm_config": {"model": "gpt-4", "max_tokens": 50},
        "tokenguard_config": {"confidence_threshold": 0.8, "max_length": 100},
    }

    # Act
    response = client.post("/v1/generate", json=request_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "This is good.This is bad."
    assert data["stop_reason"] == "confidence_threshold"
    assert data["confidence"] < 0.8


@pytest.mark.asyncio
@patch("tokenguard.llm_client.LLMClient.__init__", return_value=None)
@patch("tokenguard.llm_client.LLMClient.agenerate_stream")
async def test_generate_stops_on_max_length(mock_agenerate_stream: Any, mock_llm_client_init) -> Any:
    """Test that generation stops when the max_length is exceeded."""
    # Arrange
    mock_chunks = [
        create_stream_chunk("This is a long sentence.", [{"logprob": -0.1, "top_logprobs": []}]),
        create_stream_chunk(" This is another long one.", [{"logprob": -0.2, "top_logprobs": []}]),
    ]

    async def stream_generator() -> Any:
        for chunk in mock_chunks:
            yield chunk

    mock_agenerate_stream.return_value = stream_generator()

    request_payload = {
        "prompt": "Write a long text.",
        "llm_config": {"model": "gpt-4", "max_tokens": 100},
        "tokenguard_config": {"confidence_threshold": 0.1, "max_length": 30},
    }

    # Act
    response = client.post("/v1/generate", json=request_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["stop_reason"] == "max_length"


@pytest.mark.asyncio
@patch("tokenguard.llm_client.LLMClient.__init__", return_value=None)
@patch("tokenguard.llm_client.LLMClient.agenerate_stream", new_callable=AsyncMock)
async def test_generate_handles_llm_api_error(mock_agenerate_stream: Any, mock_llm_client_init) -> Any:
    """Test that the endpoint handles errors from the LLM API gracefully."""
    # Arrange
    mock_agenerate_stream.side_effect = httpx.HTTPStatusError(
        "Service Unavailable", request=AsyncMock(), response=AsyncMock(status_code=503)
    )

    request_payload = {
        "prompt": "This will fail.",
        "llm_config": {"model": "gpt-4", "max_tokens": 50},
        "tokenguard_config": {"confidence_threshold": 0.5, "max_length": 100},
    }

    # Act
    response = client.post("/v1/generate", json=request_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["stop_reason"] == "error"