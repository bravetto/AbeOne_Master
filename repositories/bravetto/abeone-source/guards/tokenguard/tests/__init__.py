"""
TokenGuard Microservice Test Suite

This directory contains comprehensive tests for the TokenGuard microservice:

- test_tokenguard.py: Core unit tests for TokenGuard functionality
- test_service.py: Integration tests for the FastAPI service
- test_error_scenarios.py: Comprehensive error handling and edge case tests
- benchmark.py: Performance benchmarking and load testing
- load_test.py: Locust-based load testing scenarios
- validation_final.py: Final validation suite for production readiness
- verify_claims.py: Verification script for code review claims

To run tests:
    python -m pytest tests/

To run specific test files:
    python tests/test_tokenguard.py
    python tests/test_service.py

To run performance tests:
    python tests/benchmark.py
    python tests/validation_final.py
"""
