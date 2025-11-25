"""
Tests for database functionality and audit trails.
"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from src.poisonguard.database import (
    DatabaseManager, AnalysisAudit, MitigationAudit, SystemMetrics
)
from src.poisonguard.core import DataSample, AnalysisResult, MitigationAction


class TestDatabaseManager(unittest.TestCase):
    """Test database manager functionality."""
    
    def setUp(self):
        """Set up test database."""
        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_url = f"sqlite:///{self.temp_db.name}"
        self.db_manager = DatabaseManager(self.db_url)
    
    def tearDown(self):
        """Clean up test database."""
        try:
            os.unlink(self.temp_db.name)
        except (PermissionError, FileNotFoundError):
            # File might be locked or already deleted, ignore
            pass
    
    def test_store_analysis_result(self):
        """Test storing analysis results."""
        result_id = self.db_manager.store_analysis_result(
            sample_id="test-123",
            is_poisoned=True,
            confidence=0.95,
            details={"reasons": ["suspicious_keyword"]},
            correlation_id="corr-123",
            processing_time_ms=150
        )
        
        self.assertIsNotNone(result_id)
        
        # Verify the record was stored
        history = self.db_manager.get_analysis_history(sample_id="test-123")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["sample_id"], "test-123")
        self.assertEqual(history[0]["is_poisoned"], True)
        self.assertEqual(history[0]["confidence"], 0.95)
        self.assertEqual(history[0]["correlation_id"], "corr-123")
        self.assertEqual(history[0]["processing_time_ms"], 150)
    
    def test_store_mitigation_result(self):
        """Test storing mitigation results."""
        result_id = self.db_manager.store_mitigation_result(
            sample_id="test-123",
            action_taken="sanitize",
            details={"sanitized_content": "cleaned text"},
            correlation_id="corr-123",
            processing_time_ms=200
        )
        
        self.assertIsNotNone(result_id)
        
        # Verify the record was stored
        history = self.db_manager.get_mitigation_history(sample_id="test-123")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["sample_id"], "test-123")
        self.assertEqual(history[0]["action_taken"], "sanitize")
        self.assertEqual(history[0]["correlation_id"], "corr-123")
        self.assertEqual(history[0]["processing_time_ms"], 200)
    
    def test_store_system_metrics(self):
        """Test storing system metrics."""
        result_id = self.db_manager.store_system_metrics(
            memory_usage_bytes=1024000,
            cpu_usage_percent=45.5,
            active_requests=5,
            health_status="healthy"
        )
        
        self.assertIsNotNone(result_id)
        
        # Verify the record was stored
        history = self.db_manager.get_system_metrics_history(limit=1)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["memory_usage_bytes"], 1024000)
        self.assertEqual(history[0]["cpu_usage_percent"], 45.5)
        self.assertEqual(history[0]["active_requests"], 5)
        self.assertEqual(history[0]["health_status"], "healthy")
    
    def test_get_analysis_history_with_filters(self):
        """Test getting analysis history with filters."""
        # Store multiple records
        self.db_manager.store_analysis_result("sample-1", True, 0.9, {}, "corr-1")
        self.db_manager.store_analysis_result("sample-2", False, 0.1, {}, "corr-1")
        self.db_manager.store_analysis_result("sample-1", True, 0.8, {}, "corr-2")
        
        # Test filter by sample_id
        history = self.db_manager.get_analysis_history(sample_id="sample-1")
        self.assertEqual(len(history), 2)
        
        # Test filter by correlation_id
        history = self.db_manager.get_analysis_history(correlation_id="corr-1")
        self.assertEqual(len(history), 2)
        
        # Test limit
        history = self.db_manager.get_analysis_history(limit=1)
        self.assertEqual(len(history), 1)
    
    def test_get_mitigation_history_with_filters(self):
        """Test getting mitigation history with filters."""
        # Store multiple records
        self.db_manager.store_mitigation_result("sample-1", "flag", {}, "corr-1")
        self.db_manager.store_mitigation_result("sample-2", "sanitize", {}, "corr-1")
        self.db_manager.store_mitigation_result("sample-1", "redact", {}, "corr-2")
        
        # Test filter by sample_id
        history = self.db_manager.get_mitigation_history(sample_id="sample-1")
        self.assertEqual(len(history), 2)
        
        # Test filter by correlation_id
        history = self.db_manager.get_mitigation_history(correlation_id="corr-1")
        self.assertEqual(len(history), 2)
        
        # Test limit
        history = self.db_manager.get_mitigation_history(limit=1)
        self.assertEqual(len(history), 1)
    
    def test_cleanup_old_records(self):
        """Test cleanup of old records."""
        # Store some records
        self.db_manager.store_analysis_result("sample-1", True, 0.9, {})
        self.db_manager.store_mitigation_result("sample-1", "flag", {})
        self.db_manager.store_system_metrics(1000, 50.0, 1, "healthy")
        
        # Clean up (should not remove recent records)
        deleted_count = self.db_manager.cleanup_old_records(days_to_keep=0)
        self.assertEqual(deleted_count, 0)  # No old records to delete


class TestDatabaseModels(unittest.TestCase):
    """Test database model functionality."""
    
    def test_analysis_audit_model(self):
        """Test AnalysisAudit model."""
        audit = AnalysisAudit(
            sample_id="test-123",
            is_poisoned=True,
            confidence=0.95,
            details={"test": "data"},
            correlation_id="corr-123",
            processing_time_ms=150
        )
        
        self.assertEqual(audit.sample_id, "test-123")
        self.assertEqual(audit.is_poisoned, True)
        self.assertEqual(audit.confidence, 0.95)
        self.assertEqual(audit.details, {"test": "data"})
        self.assertEqual(audit.correlation_id, "corr-123")
        self.assertEqual(audit.processing_time_ms, 150)
        # ID is auto-generated, so we just check it exists
        self.assertTrue(hasattr(audit, 'id'))
        self.assertIsNotNone(audit.timestamp)
    
    def test_mitigation_audit_model(self):
        """Test MitigationAudit model."""
        audit = MitigationAudit(
            sample_id="test-123",
            action_taken="sanitize",
            details={"sanitized": "content"},
            correlation_id="corr-123",
            processing_time_ms=200
        )
        
        self.assertEqual(audit.sample_id, "test-123")
        self.assertEqual(audit.action_taken, "sanitize")
        self.assertEqual(audit.details, {"sanitized": "content"})
        self.assertEqual(audit.correlation_id, "corr-123")
        self.assertEqual(audit.processing_time_ms, 200)
        # ID is auto-generated, so we just check it exists
        self.assertTrue(hasattr(audit, 'id'))
        self.assertIsNotNone(audit.timestamp)
    
    def test_system_metrics_model(self):
        """Test SystemMetrics model."""
        metrics = SystemMetrics(
            memory_usage_bytes=1024000,
            cpu_usage_percent=45.5,
            active_requests=5,
            health_status="healthy"
        )
        
        self.assertEqual(metrics.memory_usage_bytes, 1024000)
        self.assertEqual(metrics.cpu_usage_percent, 45.5)
        self.assertEqual(metrics.active_requests, 5)
        self.assertEqual(metrics.health_status, "healthy")
        # ID is auto-generated, so we just check it exists
        self.assertTrue(hasattr(metrics, 'id'))
        self.assertIsNotNone(metrics.timestamp)


class TestDatabaseIntegration(unittest.TestCase):
    """Test database integration with API."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_url = f"sqlite:///{self.temp_db.name}"
        
        # Patch the global db_manager
        self.patcher = patch('src.poisonguard.database.db_manager')
        self.mock_db_manager = self.patcher.start()
        self.mock_db_manager.store_analysis_result.return_value = "test-id-123"
        self.mock_db_manager.store_mitigation_result.return_value = "test-id-456"
        self.mock_db_manager.get_analysis_history.return_value = []
        self.mock_db_manager.get_mitigation_history.return_value = []
        self.mock_db_manager.get_system_metrics_history.return_value = []
    
    def tearDown(self):
        """Clean up."""
        self.patcher.stop()
        os.unlink(self.temp_db.name)
    
    def test_analyze_endpoint_database_integration(self):
        """Test that analyze endpoint stores results in database."""
        from fastapi.testclient import TestClient
        from src.poisonguard.api import app
        
        client = TestClient(app)
        
        response = client.post(
            "/analyze",
            json={"samples": [{"id": "test-1", "content": "Test content."}]}
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify database methods were called
        self.mock_db_manager.store_analysis_result.assert_called_once()
        call_args = self.mock_db_manager.store_analysis_result.call_args
        self.assertEqual(call_args[1]["sample_id"], "test-1")
        self.assertIn("is_poisoned", call_args[1])
        self.assertIn("confidence", call_args[1])
        self.assertIn("details", call_args[1])
        self.assertIn("correlation_id", call_args[1])
        self.assertIn("processing_time_ms", call_args[1])
    
    def test_mitigate_endpoint_database_integration(self):
        """Test that mitigate endpoint stores results in database."""
        from fastapi.testclient import TestClient
        from src.poisonguard.api import app
        
        client = TestClient(app)
        
        response = client.post(
            "/mitigate",
            json={"samples": [{"id": "test-1", "content": "Test content."}]}
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify both analysis and mitigation results were stored
        self.mock_db_manager.store_analysis_result.assert_called_once()
        self.mock_db_manager.store_mitigation_result.assert_called_once()
    
    def test_audit_endpoints_database_integration(self):
        """Test that audit endpoints use database."""
        from fastapi.testclient import TestClient
        from src.poisonguard.api import app
        
        client = TestClient(app)
        
        # Test analysis audit endpoint
        response = client.get("/audit/analysis")
        self.assertEqual(response.status_code, 200)
        self.mock_db_manager.get_analysis_history.assert_called_once()
        
        # Test mitigation audit endpoint
        response = client.get("/audit/mitigation")
        self.assertEqual(response.status_code, 200)
        self.mock_db_manager.get_mitigation_history.assert_called_once()
        
        # Test system audit endpoint
        response = client.get("/audit/system")
        self.assertEqual(response.status_code, 200)
        self.mock_db_manager.get_system_metrics_history.assert_called_once()


if __name__ == '__main__':
    unittest.main()
