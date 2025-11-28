"""
SDK Tests

Basic tests for SDK functionality.
"""

import pytest
from SDK.client import HyperVectorClient
from SDK.exceptions import HyperVectorError


def test_client_initialization():
    """Test client initialization."""
    client = HyperVectorClient(api_url="http://localhost:8000")
    assert client.api_url == "http://localhost:8000"
    assert client.timeout == 30


def test_client_custom_timeout():
    """Test client with custom timeout."""
    client = HyperVectorClient(api_url="http://localhost:8000", timeout=60)
    assert client.timeout == 60


# Note: These tests require a running API server
# Run with: pytest tests/test_sdk.py -v

