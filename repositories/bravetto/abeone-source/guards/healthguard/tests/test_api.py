import unittest
import json
import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.poisonguard.api import app, load_config

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_analyze_endpoint_success(self):
        response = self.client.post(
            "/analyze",
            json={"samples": [{"id": "1", "content": "This is a test."}]}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertIn("sample_id", data[0])
        self.assertIn("is_poisoned", data[0])
        self.assertIn("confidence", data[0])

    def test_mitigate_endpoint_success(self):
        response = self.client.post(
            "/mitigate",
            json={"samples": [{"id": "1", "content": "This is a test."}]}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertIn("sample_id", data[0])
        self.assertIn("action_taken", data[0])

    def test_report_endpoint_success(self):
        response = self.client.post(
            "/report",
            json={"samples": [{"id": "1", "content": "This is a test."}]}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_samples", data)
        self.assertIn("poisoned_samples", data)
        self.assertIn("mitigated_samples", data)

    def test_empty_input(self):
        response = self.client.post("/analyze", json={"samples": []})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Input samples cannot be empty", response.json()["detail"])

        response = self.client.post("/mitigate", json={"samples": []})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Input samples cannot be empty", response.json()["detail"])

        response = self.client.post("/report", json={"samples": []})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Input samples cannot be empty", response.json()["detail"])

    def test_invalid_input(self):
        response = self.client.post("/analyze", json={"samples": [{"id": "1"}]})
        self.assertEqual(response.status_code, 422)
        self.assertIn("Field required", response.json()["detail"][0]["msg"])

    def test_config_not_found(self):
        # Temporarily rename the config file to simulate it being missing
        if os.path.exists("config.yaml"):
            os.rename("config.yaml", "config.yaml.bak")

        with self.assertRaises(Exception) as context:
            load_config()

        self.assertTrue("Configuration file not found" in str(context.exception))

        # Restore the config file
        if os.path.exists("config.yaml.bak"):
            os.rename("config.yaml.bak", "config.yaml")

    @patch('os.path.exists')
    def test_config_not_found_error(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(Exception) as context:
            load_config()
        self.assertIn("Configuration file not found", str(context.exception))

    @patch('uvicorn.run')
    def test_main(self, mock_run):
        from src.poisonguard import api
        with patch.object(api, "__name__", "__main__"):
            api.uvicorn.run("poisonguard.api:app", host="0.0.0.0", port=8000, reload=True)
            mock_run.assert_called_with("poisonguard.api:app", host="0.0.0.0", port=8000, reload=True)

    def test_health_check_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("timestamp", data)
        self.assertIn("uptime_seconds", data)
        self.assertIn("memory_usage_percent", data)
        self.assertIn("cpu_usage_percent", data)

if __name__ == '__main__':
    # Add src to python path to run tests
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    unittest.main()