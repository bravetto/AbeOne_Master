"""
Tests for monitoring and metrics functionality.
"""

import unittest
import time
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.poisonguard.monitoring import (
    SystemMetrics, HealthChecker, get_correlation_id, set_correlation_id,
    record_request_metrics, record_analysis_metrics, record_mitigation_metrics
)
from src.poisonguard.api import app


class TestSystemMetrics(unittest.TestCase):
    """Test system metrics collection."""
    
    def setUp(self):
        self.metrics = SystemMetrics()
    
    def test_get_uptime(self):
        """Test uptime calculation."""
        uptime = self.metrics.get_uptime()
        self.assertGreater(uptime, 0)
        self.assertIsInstance(uptime, float)
    
    def test_get_memory_usage(self):
        """Test memory usage collection."""
        memory = self.metrics.get_memory_usage()
        self.assertIn('rss', memory)
        self.assertIn('vms', memory)
        self.assertIn('percent', memory)
        self.assertIn('available', memory)
        self.assertGreater(memory['rss'], 0)
        self.assertGreaterEqual(memory['percent'], 0)
    
    def test_get_cpu_usage(self):
        """Test CPU usage collection."""
        cpu = self.metrics.get_cpu_usage()
        self.assertIn('percent', cpu)
        self.assertIn('system_percent', cpu)
        self.assertGreaterEqual(cpu['percent'], 0)
        self.assertGreaterEqual(cpu['system_percent'], 0)
    
    def test_get_system_info(self):
        """Test comprehensive system info."""
        info = self.metrics.get_system_info()
        self.assertIn('uptime', info)
        self.assertIn('memory', info)
        self.assertIn('cpu', info)
        self.assertIn('timestamp', info)
        self.assertIn('pid', info)
        self.assertIn('threads', info)


class TestHealthChecker(unittest.TestCase):
    """Test health check functionality."""
    
    def setUp(self):
        self.health_checker = HealthChecker()
    
    def test_health_check_healthy(self):
        """Test health check when system is healthy."""
        with patch.object(self.health_checker.metrics, 'get_system_info') as mock_info:
            mock_info.return_value = {
                'uptime': 100.0,
                'memory': {'percent': 50.0, 'rss': 1000000},
                'cpu': {'percent': 30.0},
                'timestamp': '2023-01-01T00:00:00Z',
                'pid': 1234,
                'threads': 5
            }
            
            result = self.health_checker.check_health()
            
            self.assertEqual(result['status'], 'healthy')
            self.assertIn('timestamp', result)
            self.assertIn('uptime_seconds', result)
            self.assertIn('memory_usage_percent', result)
            self.assertIn('cpu_usage_percent', result)
    
    def test_health_check_degraded_memory(self):
        """Test health check when memory usage is high."""
        with patch.object(self.health_checker.metrics, 'get_system_info') as mock_info:
            mock_info.return_value = {
                'uptime': 100.0,
                'memory': {'percent': 95.0, 'rss': 1000000},
                'cpu': {'percent': 30.0},
                'timestamp': '2023-01-01T00:00:00Z',
                'pid': 1234,
                'threads': 5
            }
            
            result = self.health_checker.check_health()
            self.assertEqual(result['status'], 'degraded')
    
    def test_health_check_degraded_cpu(self):
        """Test health check when CPU usage is high."""
        with patch.object(self.health_checker.metrics, 'get_system_info') as mock_info:
            mock_info.return_value = {
                'uptime': 100.0,
                'memory': {'percent': 50.0, 'rss': 1000000},
                'cpu': {'percent': 98.0},
                'timestamp': '2023-01-01T00:00:00Z',
                'pid': 1234,
                'threads': 5
            }
            
            result = self.health_checker.check_health()
            self.assertEqual(result['status'], 'degraded')
    
    def test_health_check_error(self):
        """Test health check when system info fails."""
        with patch.object(self.health_checker.metrics, 'get_system_info') as mock_info:
            mock_info.side_effect = Exception("System error")
            
            result = self.health_checker.check_health()
            self.assertEqual(result['status'], 'unhealthy')
            self.assertIn('error', result)


class TestCorrelationID(unittest.TestCase):
    """Test correlation ID functionality."""
    
    def test_get_correlation_id(self):
        """Test correlation ID generation and retrieval."""
        # Clear any existing correlation ID
        set_correlation_id("")
        
        # Get new correlation ID
        cid = get_correlation_id()
        self.assertIsInstance(cid, str)
        self.assertGreater(len(cid), 0)
    
    def test_set_correlation_id(self):
        """Test setting correlation ID."""
        test_id = "test-correlation-id-123"
        set_correlation_id(test_id)
        self.assertEqual(get_correlation_id(), test_id)


class TestMetricsRecording(unittest.TestCase):
    """Test metrics recording functionality."""
    
    def test_record_request_metrics(self):
        """Test request metrics recording."""
        # This test verifies the function doesn't raise exceptions
        record_request_metrics("GET", "/health", 200, 0.1)
        record_request_metrics("POST", "/analyze", 200, 0.5)
        record_request_metrics("POST", "/analyze", 400, 0.2)
    
    def test_record_analysis_metrics(self):
        """Test analysis metrics recording."""
        record_analysis_metrics(True)  # Poisoned
        record_analysis_metrics(False)  # Clean
    
    def test_record_mitigation_metrics(self):
        """Test mitigation metrics recording."""
        record_mitigation_metrics("flag")
        record_mitigation_metrics("sanitize")
        record_mitigation_metrics("redact")
        record_mitigation_metrics("none")


class TestMonitoringEndpoints(unittest.TestCase):
    """Test monitoring API endpoints."""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("timestamp", data)
        self.assertIn("uptime_seconds", data)
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "text/plain; version=1.0.0; charset=utf-8")
    
    def test_config_validation_endpoint(self):
        """Test configuration validation endpoint."""
        response = self.client.get("/config/validation")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("valid", data)
        self.assertIn("errors", data)
        self.assertIn("warnings", data)
    
    def test_audit_endpoints(self):
        """Test audit trail endpoints."""
        # Test analysis audit
        response = self.client.get("/audit/analysis")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        
        # Test mitigation audit
        response = self.client.get("/audit/mitigation")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        
        # Test system audit
        response = self.client.get("/audit/system")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
    
    def test_audit_endpoints_with_filters(self):
        """Test audit endpoints with query parameters."""
        # Test with sample_id filter
        response = self.client.get("/audit/analysis?sample_id=test-123")
        self.assertEqual(response.status_code, 200)
        
        # Test with correlation_id filter
        response = self.client.get("/audit/analysis?correlation_id=test-correlation")
        self.assertEqual(response.status_code, 200)
        
        # Test with limit
        response = self.client.get("/audit/analysis?limit=50")
        self.assertEqual(response.status_code, 200)


class TestMonitoringIntegration(unittest.TestCase):
    """Test monitoring integration with main API."""
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_analyze_with_monitoring(self):
        """Test analyze endpoint with monitoring."""
        response = self.client.post(
            "/analyze",
            json={"samples": [{"id": "test-1", "content": "This is a test sample."}]}
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Check for correlation ID in response headers
        self.assertIn("X-Correlation-ID", response.headers)
        
        # Verify response structure
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn("sample_id", data[0])
        self.assertIn("is_poisoned", data[0])
        self.assertIn("confidence", data[0])
        self.assertIn("details", data[0])
    
    def test_mitigate_with_monitoring(self):
        """Test mitigate endpoint with monitoring."""
        response = self.client.post(
            "/mitigate",
            json={"samples": [{"id": "test-1", "content": "This is a test sample."}]}
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Check for correlation ID in response headers
        self.assertIn("X-Correlation-ID", response.headers)
        
        # Verify response structure
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn("sample_id", data[0])
        self.assertIn("action_taken", data[0])
        self.assertIn("details", data[0])
    
    def test_correlation_id_persistence(self):
        """Test that correlation ID is maintained across requests."""
        # First request
        response1 = self.client.post(
            "/analyze",
            json={"samples": [{"id": "test-1", "content": "Test content."}]}
        )
        correlation_id1 = response1.headers.get("X-Correlation-ID")
        
        # Second request
        response2 = self.client.post(
            "/analyze",
            json={"samples": [{"id": "test-2", "content": "Another test."}]}
        )
        correlation_id2 = response2.headers.get("X-Correlation-ID")
        
        # Correlation IDs should be different (new for each request)
        self.assertNotEqual(correlation_id1, correlation_id2)
        self.assertIsNotNone(correlation_id1)
        self.assertIsNotNone(correlation_id2)


if __name__ == '__main__':
    unittest.main()
