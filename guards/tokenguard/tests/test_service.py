from typing import Any
#!/usr/bin/env python3
"""
Test script for TokenGuard microservice
"""

import requests
import time


def test_health() -> Any:
    """Test health endpoint."""
    try:
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print(" Health check passed")
    except Exception as e:
        print(f" Health check failed: {e}")
        raise


def test_prune_high_confidence() -> Any:
    """Test pruning with high confidence (should keep)."""
    payload = {"content": "This is a short response that should be kept.", "confidence": 0.9}

    try:
        response = requests.post("http://localhost:8000/v1/prune", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["action"] == "keep"
        print(" High confidence test passed")
    except Exception as e:
        print(f" High confidence test failed: {e}")
        raise


def test_prune_low_confidence() -> Any:
    """Test pruning with low confidence (should prune)."""
    long_text = (
        "This is a very long response that contains multiple sentences and should be pruned because of low confidence. "
        * 20
    )
    payload = {"content": long_text, "confidence": 0.5}

    try:
        response = requests.post("http://localhost:8000/v1/prune", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["action"] == "prune"
        assert "pruned_text" in data
        assert data["pruned_length"] < data["original_length"]
        print(" Low confidence test passed")
    except Exception as e:
        print(f" Low confidence test failed: {e}")
        raise


def test_analyze_endpoint() -> Any:
    """Test analyze endpoint."""
    payload = {"content": "Sample text for analysis.", "confidence": 0.7}

    try:
        response = requests.post("http://localhost:8000/v1/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "text_length" in data
        assert "confidence_score" in data
        assert "decision" in data
        print(" Analyze endpoint test passed")
    except Exception as e:
        print(f" Analyze endpoint test failed: {e}")
        raise


def test_invalid_request() -> Any:
    """Test invalid request handling."""
    payload = {"content": "Valid text", "confidence": 1.5}  # Invalid confidence > 1.0

    try:
        response = requests.post("http://localhost:8000/v1/prune", json=payload)
        assert response.status_code == 422  # Validation error
        print(" Invalid request test passed")
    except Exception as e:
        print(f" Invalid request test failed: {e}")
        raise


def run_all_tests() -> Any:
    """Run all tests."""
    print("Running TokenGuard microservice tests...\n")

    tests = [
        test_health,
        test_prune_high_confidence,
        test_prune_low_confidence,
        test_analyze_endpoint,
        test_invalid_request,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        time.sleep(0.1)  # Small delay between tests

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print(" All tests passed!")
        return True
    else:
        print("  Some tests failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
