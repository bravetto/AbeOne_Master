"""
Comprehensive Unit Tests for Trust Guard Logging System

Tests logging functionality with various scenarios, trace context, and performance data.
"""

import pytest
import time
import json
import logging
from unittest.mock import Mock, patch
from typing import Dict, Any, List

from trustguard.logging import (
    setup_logging, set_trace_context, get_trace_context, generate_trace_id,
    generate_span_id, log_with_context, log_performance, log_security_event,
    log_business_event, PerformanceLogger
)


class TestLoggingSetup:
    """Test logging setup and configuration."""
    
    def test_setup_logging_json_format(self):
        """Test logging setup with JSON format."""
        logger = setup_logging(level="INFO", format_type="json")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "trustguard"
        assert logger.level <= logging.INFO
    
    def test_setup_logging_text_format(self):
        """Test logging setup with text format."""
        logger = setup_logging(level="DEBUG", format_type="text")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "trustguard"
        assert logger.level <= logging.DEBUG
    
    def test_setup_logging_different_levels(self):
        """Test logging setup with different levels."""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        for level in levels:
            logger = setup_logging(level=level)
            assert isinstance(logger, logging.Logger)
            assert logger.name == "trustguard"
    
    def test_setup_logging_invalid_level(self):
        """Test logging setup with invalid level."""
        logger = setup_logging(level="INVALID")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "trustguard"
        # Should default to INFO level


class TestTraceContext:
    """Test trace context management."""
    
    def setup_method(self):
        """Clear trace context before each test."""
        set_trace_context(trace_id=None, span_id=None, user_id=None, request_id=None)
    
    def test_set_trace_context(self):
        """Test setting trace context."""
        trace_id = "test-trace-123"
        span_id = "test-span-456"
        user_id = "test-user-789"
        request_id = "test-request-101"
        
        set_trace_context(
            trace_id=trace_id,
            span_id=span_id,
            user_id=user_id,
            request_id=request_id
        )
        
        context = get_trace_context()
        
        assert context["trace_id"] == trace_id
        assert context["span_id"] == span_id
        assert context["user_id"] == user_id
        assert context["request_id"] == request_id
    
    def test_set_trace_context_partial(self):
        """Test setting partial trace context."""
        # Clear context first
        set_trace_context(trace_id=None, span_id=None, user_id=None, request_id=None)
        
        trace_id = "test-trace-123"
        
        set_trace_context(trace_id=trace_id)
        
        context = get_trace_context()
        
        assert context["trace_id"] == trace_id
        assert context["span_id"] is None
        assert context["user_id"] is None
        assert context["request_id"] is None
    
    def test_set_trace_context_none_values(self):
        """Test setting trace context with None values."""
        set_trace_context(
            trace_id=None,
            span_id=None,
            user_id=None,
            request_id=None
        )
        
        context = get_trace_context()
        
        assert context["trace_id"] is None
        assert context["span_id"] is None
        assert context["user_id"] is None
        assert context["request_id"] is None
    
    def test_generate_trace_id(self):
        """Test trace ID generation."""
        trace_id = generate_trace_id()
        
        assert isinstance(trace_id, str)
        assert len(trace_id) > 0
        assert "-" in trace_id  # UUID format
    
    def test_generate_span_id(self):
        """Test span ID generation."""
        span_id = generate_span_id()
        
        assert isinstance(span_id, str)
        assert len(span_id) == 8  # Truncated UUID
    
    def test_trace_context_isolation(self):
        """Test that trace context is isolated between calls."""
        # Set initial context
        set_trace_context(trace_id="initial-trace")
        initial_context = get_trace_context()
        
        # Set new context
        set_trace_context(trace_id="new-trace")
        new_context = get_trace_context()
        
        assert initial_context["trace_id"] == "initial-trace"
        assert new_context["trace_id"] == "new-trace"


class TestContextualLogging:
    """Test contextual logging functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging(level="INFO", format_type="json")
    
    def test_log_with_context_basic(self):
        """Test basic contextual logging."""
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(self.logger, "info", "Test message")
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert call_args[0][0] == "Test message"
    
    def test_log_with_context_with_extra_data(self):
        """Test contextual logging with extra data."""
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(
                self.logger, 
                "info", 
                "Test message",
                operation="test_operation",
                value=42
            )
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert call_args[0][0] == "Test message"
            assert "extra" in call_args[1]
            assert call_args[1]["extra"]["operation"] == "test_operation"
            assert call_args[1]["extra"]["value"] == 42
    
    def test_log_with_context_with_trace_context(self):
        """Test contextual logging with trace context."""
        set_trace_context(trace_id="test-trace", user_id="test-user")
        
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(self.logger, "info", "Test message")
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["trace_id"] == "test-trace"
            assert extra["user_id"] == "test-user"
    
    def test_log_with_context_different_levels(self):
        """Test contextual logging with different levels."""
        levels = ["debug", "info", "warning", "error", "critical"]
        
        for level in levels:
            with patch.object(self.logger, level) as mock_method:
                log_with_context(self.logger, level, f"Test {level} message")
                
                mock_method.assert_called_once()
    
    def test_log_with_context_invalid_level(self):
        """Test contextual logging with invalid level."""
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(self.logger, "invalid", "Test message")
            
            mock_info.assert_called_once()  # Should default to info
    
    def test_log_with_context_with_duration_calculation(self):
        """Test contextual logging with duration calculation."""
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(
                self.logger, 
                "info", 
                "Test message",
                start_time=time.time() - 0.1
            )
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert "duration" in extra
            assert extra["duration"] > 0.0


class TestPerformanceLogging:
    """Test performance logging functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging(level="INFO", format_type="json")
    
    def test_log_performance_basic(self):
        """Test basic performance logging."""
        with patch.object(self.logger, 'info') as mock_info:
            log_performance(self.logger, "test_operation", 0.5)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "Performance: test_operation" in call_args[0][0]
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["operation"] == "test_operation"
            assert extra["duration_seconds"] == 0.5
            assert extra["duration_ms"] == 500.0
    
    def test_log_performance_with_metrics(self):
        """Test performance logging with additional metrics."""
        with patch.object(self.logger, 'info') as mock_info:
            log_performance(
                self.logger, 
                "test_operation", 
                0.5,
                patterns_detected=3,
                risk_level="medium"
            )
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["patterns_detected"] == 3
            assert extra["risk_level"] == "medium"
    
    def test_log_performance_with_trace_context(self):
        """Test performance logging with trace context."""
        set_trace_context(trace_id="test-trace")
        
        with patch.object(self.logger, 'info') as mock_info:
            log_performance(self.logger, "test_operation", 0.5)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["trace_id"] == "test-trace"


class TestSecurityEventLogging:
    """Test security event logging functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging(level="INFO", format_type="json")
    
    def test_log_security_event_basic(self):
        """Test basic security event logging."""
        with patch.object(self.logger, 'info') as mock_info:
            log_security_event(self.logger, "authentication_failed")
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "Security event: authentication_failed" in call_args[0][0]
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["event_type"] == "authentication_failed"
            assert extra["severity"] == "medium"
    
    def test_log_security_event_different_severities(self):
        """Test security event logging with different severities."""
        severities = ["low", "medium", "high", "critical"]
        
        for severity in severities:
            with patch.object(self.logger, 'info' if severity in ['low', 'medium'] else 'warning') as mock_method:
                log_security_event(self.logger, "test_event", severity)
                
                mock_method.assert_called_once()
                call_args = mock_method.call_args
                assert "extra" in call_args[1]
                extra = call_args[1]["extra"]
                assert extra["severity"] == severity
    
    def test_log_security_event_with_details(self):
        """Test security event logging with additional details."""
        with patch.object(self.logger, 'warning') as mock_warning:
            log_security_event(
                self.logger, 
                "authentication_failed",
                "high",
                user_id="test_user",
                ip_address="192.168.1.1",
                attempt_count=3
            )
            
            mock_warning.assert_called_once()
            call_args = mock_warning.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["user_id"] == "test_user"
            assert extra["ip_address"] == "192.168.1.1"
            assert extra["attempt_count"] == 3


class TestBusinessEventLogging:
    """Test business event logging functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging(level="INFO", format_type="json")
    
    def test_log_business_event_basic(self):
        """Test basic business event logging."""
        with patch.object(self.logger, 'info') as mock_info:
            log_business_event(self.logger, "user_registration")
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "Business event: user_registration" in call_args[0][0]
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["event_type"] == "user_registration"
    
    def test_log_business_event_with_details(self):
        """Test business event logging with additional details."""
        with patch.object(self.logger, 'info') as mock_info:
            log_business_event(
                self.logger, 
                "pattern_detection",
                user_id="test_user",
                patterns_detected=["hallucination", "bias"],
                risk_score=0.8
            )
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["user_id"] == "test_user"
            assert extra["patterns_detected"] == ["hallucination", "bias"]
            assert extra["risk_score"] == 0.8


class TestPerformanceLogger:
    """Test PerformanceLogger context manager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging(level="INFO", format_type="json")
    
    def test_performance_logger_success(self):
        """Test PerformanceLogger with successful operation."""
        with patch.object(self.logger, 'info') as mock_info:
            with PerformanceLogger(self.logger, "test_operation", input_size=100):
                time.sleep(0.01)  # Simulate work
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "Performance: test_operation" in call_args[0][0]
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["operation"] == "test_operation"
            assert extra["success"] is True
            assert extra["input_size"] == 100
            assert extra["duration_seconds"] > 0.0
    
    def test_performance_logger_with_exception(self):
        """Test PerformanceLogger with exception."""
        with patch.object(self.logger, 'info') as mock_info:
            try:
                with PerformanceLogger(self.logger, "test_operation"):
                    raise ValueError("Test error")
            except ValueError:
                pass
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["success"] is False
            assert extra["error_type"] == "ValueError"
            assert extra["error_message"] == "Test error"
    
    def test_performance_logger_with_metrics(self):
        """Test PerformanceLogger with additional metrics."""
        with patch.object(self.logger, 'info') as mock_info:
            with PerformanceLogger(
                self.logger, 
                "test_operation",
                patterns_detected=3,
                risk_level="medium"
            ):
                time.sleep(0.01)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["patterns_detected"] == 3
            assert extra["risk_level"] == "medium"


class TestLoggingIntegration:
    """Test logging integration with other components."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging(level="INFO", format_type="json")
    
    def test_logging_with_trace_context_propagation(self):
        """Test that trace context propagates through logging calls."""
        # Set trace context
        set_trace_context(
            trace_id="integration-test-trace",
            user_id="integration-test-user",
            request_id="integration-test-request"
        )
        
        with patch.object(self.logger, 'info') as mock_info:
            # Log different types of events
            log_with_context(self.logger, "info", "Regular log message")
            log_performance(self.logger, "test_operation", 0.1)
            log_security_event(self.logger, "test_security_event")
            log_business_event(self.logger, "test_business_event")
            
            # All calls should include trace context
            assert mock_info.call_count == 4
            
            for call in mock_info.call_args_list:
                call_args = call[1]
                assert "extra" in call_args
                extra = call_args["extra"]
                assert extra["trace_id"] == "integration-test-trace"
                assert extra["user_id"] == "integration-test-user"
                assert extra["request_id"] == "integration-test-request"
    
    def test_logging_with_performance_logger_integration(self):
        """Test PerformanceLogger integration with other logging functions."""
        set_trace_context(trace_id="perf-test-trace")
        
        with patch.object(self.logger, 'info') as mock_info:
            with PerformanceLogger(self.logger, "integration_test"):
                log_with_context(self.logger, "info", "Message inside performance logger")
                log_business_event(self.logger, "event_inside_perf_logger")
            
            # Should have 3 calls: 2 from inside the context manager, 1 from the context manager itself
            assert mock_info.call_count == 3
            
            # The performance logger call should include trace context
            perf_call = mock_info.call_args_list[-1]  # Last call is from PerformanceLogger
            call_args = perf_call[1]
            assert "extra" in call_args
            extra = call_args["extra"]
            assert extra["trace_id"] == "perf-test-trace"
            assert extra["operation"] == "integration_test"
    
    def test_logging_json_format_validation(self):
        """Test that JSON format logging produces valid JSON."""
        # Capture log output
        import io
        import sys
        
        # Create a string buffer to capture output
        log_capture = io.StringIO()
        
        # Set up logging to write to our buffer
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.INFO)
        
        # Create formatter
        from pythonjsonlogger import jsonlogger
        formatter = jsonlogger.JsonFormatter()
        handler.setFormatter(formatter)
        
        # Add handler to logger
        test_logger = logging.getLogger('test_json_logger')
        test_logger.setLevel(logging.INFO)
        test_logger.addHandler(handler)
        test_logger.propagate = False
        
        # Set trace context
        set_trace_context(trace_id="json-test-trace", user_id="json-test-user")
        
        # Log a message
        log_with_context(test_logger, "info", "JSON format test", test_value=42)
        
        # Get the log output
        log_output = log_capture.getvalue().strip()
        
        # Should be valid JSON
        try:
            log_data = json.loads(log_output)
            assert isinstance(log_data, dict)
            assert log_data["message"] == "JSON format test"
            assert log_data["trace_id"] == "json-test-trace"
            assert log_data["user_id"] == "json-test-user"
            assert log_data["test_value"] == 42
        except json.JSONDecodeError:
            pytest.fail("Log output is not valid JSON")


class TestLoggingEdgeCases:
    """Test logging edge cases and error scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = setup_logging(level="INFO", format_type="json")
    
    def test_logging_with_very_long_messages(self):
        """Test logging with very long messages."""
        long_message = "A" * 10000  # 10KB message
        
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(self.logger, "info", long_message)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert call_args[0][0] == long_message
    
    def test_logging_with_special_characters(self):
        """Test logging with special characters."""
        special_message = "Test message with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(self.logger, "info", special_message)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert call_args[0][0] == special_message
    
    def test_logging_with_unicode_characters(self):
        """Test logging with unicode characters."""
        unicode_message = "Test message with unicode: Hello !  émojis and àccénts"
        
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(self.logger, "info", unicode_message)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert call_args[0][0] == unicode_message
    
    def test_logging_with_none_values(self):
        """Test logging with None values in context."""
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(
                self.logger, 
                "info", 
                "Test message",
                none_value=None,
                empty_string="",
                zero_value=0
            )
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["none_value"] is None
            assert extra["empty_string"] == ""
            assert extra["zero_value"] == 0
    
    def test_logging_with_complex_objects(self):
        """Test logging with complex objects in context."""
        complex_data = {
            "nested": {"key": "value"},
            "list": [1, 2, 3],
            "tuple": (4, 5, 6)
        }
        
        with patch.object(self.logger, 'info') as mock_info:
            log_with_context(self.logger, "info", "Test message", data=complex_data)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            assert "extra" in call_args[1]
            extra = call_args[1]["extra"]
            assert extra["data"] == complex_data
    
    def test_logging_concurrent_access(self):
        """Test logging with concurrent access."""
        import threading
        import queue
        
        results = queue.Queue()
        errors = queue.Queue()
        
        def logging_worker(worker_id):
            try:
                set_trace_context(trace_id=f"worker-{worker_id}")
                
                with patch.object(self.logger, 'info') as mock_info:
                    log_with_context(self.logger, "info", f"Message from worker {worker_id}")
                    results.put((worker_id, mock_info.call_count))
            except Exception as e:
                errors.put((worker_id, e))
        
        # Start multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=logging_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        assert errors.empty(), f"Errors occurred: {list(errors.queue)}"
        assert results.qsize() == 10, f"Expected 10 results, got {results.qsize()}"
        
        # Verify all results are valid
        while not results.empty():
            worker_id, call_count = results.get()
            assert call_count == 1, f"Worker {worker_id} should have made 1 call"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
