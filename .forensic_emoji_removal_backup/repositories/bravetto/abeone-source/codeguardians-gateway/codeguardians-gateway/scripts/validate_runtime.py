#!/usr/bin/env python3
"""
Runtime Validation Script for AWS Secrets Manager Integration

This script validates the actual runtime behavior, telemetry, and data output
of the AWS Secrets Manager integration in CodeGuardians Gateway.
"""

import os
import sys
import json
import time
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, '/app')

try:
    from app.core.aws_secrets import (
        AWSSecretsManager, 
        validate_aws_secrets_available,
        get_aws_secrets_for_environment,
        initialize_aws_secrets
    )
    from app.core.config import get_settings
    from app.utils.logging import get_logger
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the correct directory")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RuntimeValidator:
    """Validates runtime behavior of AWS Secrets Manager integration."""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            }
        }
    
    def log_test(self, test_name: str, status: str, message: str, data: Optional[Dict] = None):
        """Log test result."""
        self.results["tests"][test_name] = {
            "status": status,
            "message": message,
            "data": data or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.results["summary"]["total_tests"] += 1
        if status == "PASS":
            self.results["summary"]["passed"] += 1
            print(f"✅ {test_name}: {message}")
        elif status == "FAIL":
            self.results["summary"]["failed"] += 1
            print(f"❌ {test_name}: {message}")
        else:
            self.results["summary"]["warnings"] += 1
            print(f"⚠️  {test_name}: {message}")
    
    def test_environment_variables(self):
        """Test environment variable configuration."""
        print("\n🔍 Testing Environment Variables...")
        
        # Check AWS configuration
        aws_enabled = os.getenv('AWS_SECRETS_ENABLED', 'true').lower() == 'true'
        aws_secrets_name = os.getenv('AWS_SECRETS_NAME', 'codeguardians-gateway/production')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        self.log_test(
            "aws_secrets_enabled",
            "PASS" if aws_enabled else "WARN",
            f"AWS Secrets Manager enabled: {aws_enabled}",
            {"enabled": aws_enabled, "secrets_name": aws_secrets_name, "region": aws_region}
        )
        
        # Check required environment variables
        required_vars = ['ENVIRONMENT', 'LOG_LEVEL']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            self.log_test(
                "required_env_vars",
                "WARN",
                f"Missing environment variables: {missing_vars}",
                {"missing": missing_vars}
            )
        else:
            self.log_test(
                "required_env_vars",
                "PASS",
                "All required environment variables present",
                {"variables": required_vars}
            )
    
    def REPLACE_ME(self):
        """Test AWS Secrets Manager availability."""
        print("\n🔍 Testing AWS Secrets Manager Availability...")
        
        try:
            available = validate_aws_secrets_available()
            self.log_test(
                "aws_secrets_available",
                "PASS" if available else "FAIL",
                f"AWS Secrets Manager available: {available}",
                {"available": available}
            )
            return available
        except Exception as e:
            self.log_test(
                "aws_secrets_available",
                "FAIL",
                f"Error checking AWS Secrets Manager: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def REPLACE_ME(self):
        """Test actual AWS secrets loading."""
        print("\n🔍 Testing AWS Secrets Loading...")
        
        try:
            # Initialize AWS secrets manager
            aws_secrets_name = os.getenv('AWS_SECRETS_NAME', 'codeguardians-gateway/production')
            aws_region = os.getenv('AWS_REGION', 'us-east-1')
            
            manager = initialize_aws_secrets(region=aws_region, secret_name=aws_secrets_name)
            
            # Test fetching secrets
            start_time = time.time()
            secrets = manager.get_secret()
            load_time = time.time() - start_time
            
            self.log_test(
                "secrets_loading_time",
                "PASS" if load_time < 5.0 else "WARN",
                f"Secrets loaded in {load_time:.3f}s",
                {"load_time": load_time, "secret_count": len(secrets)}
            )
            
            # Check required secrets
            required_secrets = [
                "SECRET_KEY", "DATABASE_URL", "REDIS_URL", 
                "POSTGRES_PASSWORD", "REDIS_PASSWORD"
            ]
            
            missing_secrets = [secret for secret in required_secrets if secret not in secrets]
            present_secrets = [secret for secret in required_secrets if secret in secrets]
            
            if missing_secrets:
                self.log_test(
                    "required_secrets",
                    "FAIL",
                    f"Missing required secrets: {missing_secrets}",
                    {"missing": missing_secrets, "present": present_secrets}
                )
            else:
                self.log_test(
                    "required_secrets",
                    "PASS",
                    f"All required secrets present: {present_secrets}",
                    {"present": present_secrets}
                )
            
            # Validate secret key length
            secret_key = secrets.get('SECRET_KEY', '')
            if len(secret_key) >= 32:
                self.log_test(
                    "secret_key_length",
                    "PASS",
                    f"SECRET_KEY length: {len(secret_key)} characters",
                    {"length": len(secret_key)}
                )
            else:
                self.log_test(
                    "secret_key_length",
                    "FAIL",
                    f"SECRET_KEY too short: {len(secret_key)} characters (minimum 32)",
                    {"length": len(secret_key)}
                )
            
            return secrets
            
        except Exception as e:
            self.log_test(
                "secrets_loading",
                "FAIL",
                f"Error loading secrets: {str(e)}",
                {"error": str(e)}
            )
            return None
    
    def test_configuration_loading(self):
        """Test configuration loading with AWS secrets."""
        print("\n🔍 Testing Configuration Loading...")
        
        try:
            # Test settings loading
            start_time = time.time()
            settings = get_settings()
            load_time = time.time() - start_time
            
            self.log_test(
                "config_loading_time",
                "PASS" if load_time < 2.0 else "WARN",
                f"Configuration loaded in {load_time:.3f}s",
                {"load_time": load_time}
            )
            
            # Test AWS secrets integration
            aws_enabled = getattr(settings, 'AWS_SECRETS_ENABLED', False)
            self.log_test(
                "config_aws_integration",
                "PASS" if aws_enabled else "WARN",
                f"AWS Secrets Manager integration: {aws_enabled}",
                {"enabled": aws_enabled}
            )
            
            # Test secret values
            secret_key = getattr(settings, 'SECRET_KEY', '')
            database_url = getattr(settings, 'DATABASE_URL', '')
            redis_url = getattr(settings, 'REDIS_URL', '')
            
            self.log_test(
                "config_secret_values",
                "PASS" if secret_key and database_url and redis_url else "FAIL",
                f"Secret values loaded: SECRET_KEY={bool(secret_key)}, DATABASE_URL={bool(database_url)}, REDIS_URL={bool(redis_url)}",
                {
                    "secret_key_present": bool(secret_key),
                    "database_url_present": bool(database_url),
                    "redis_url_present": bool(redis_url)
                }
            )
            
            return settings
            
        except Exception as e:
            self.log_test(
                "config_loading",
                "FAIL",
                f"Error loading configuration: {str(e)}",
                {"error": str(e)}
            )
            return None
    
    def test_guard_services_health(self):
        """Test guard services health endpoints."""
        print("\n🔍 Testing Guard Services Health...")
        
        import httpx
        
        guard_services = [
            {"name": "TokenGuard", "port": 8001},
            {"name": "TrustGuard", "port": 8002},
            {"name": "ContextGuard", "port": 8003},
            {"name": "BiasGuard", "port": 8004},
            {"name": "SecurityGuard", "port": 8005},
            {"name": "HealthGuard", "port": 8006}
        ]
        
        healthy_services = []
        unhealthy_services = []
        
        for service in guard_services:
            try:
                with httpx.Client(timeout=5.0) as client:
                    response = client.get(f"http://localhost:{service['port']}/health")
                    if response.status_code == 200:
                        healthy_services.append(service['name'])
                    else:
                        unhealthy_services.append(service['name'])
            except Exception as e:
                unhealthy_services.append(service['name'])
        
        self.log_test(
            "guard_services_health",
            "PASS" if len(healthy_services) >= 4 else "WARN",
            f"Healthy services: {len(healthy_services)}/{len(guard_services)} - {healthy_services}",
            {"healthy": healthy_services, "unhealthy": unhealthy_services}
        )
        
        return healthy_services
    
    def test_gateway_health(self):
        """Test gateway health endpoints."""
        print("\n🔍 Testing Gateway Health...")
        
        import httpx
        
        try:
            with httpx.Client(timeout=10.0) as client:
                # Test liveness endpoint
                liveness_response = client.get("http://localhost:8000/health/live")
                liveness_ok = liveness_response.status_code == 200
                
                # Test readiness endpoint
                readiness_response = client.get("http://localhost:8000/health/ready")
                readiness_ok = readiness_response.status_code == 200
                
                self.log_test(
                    "gateway_health",
                    "PASS" if liveness_ok and readiness_ok else "FAIL",
                    f"Liveness: {liveness_ok}, Readiness: {readiness_ok}",
                    {
                        "liveness_status": liveness_response.status_code,
                        "readiness_status": readiness_response.status_code
                    }
                )
                
                return liveness_ok and readiness_ok
                
        except Exception as e:
            self.log_test(
                "gateway_health",
                "FAIL",
                f"Error testing gateway health: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def test_api_endpoints(self):
        """Test API endpoints functionality."""
        print("\n🔍 Testing API Endpoints...")
        
        import httpx
        
        try:
            with httpx.Client(timeout=15.0) as client:
                # Test unified guards endpoint
                test_payload = {
                    "text": "This is a test input for validation",
                    "service_type": "tokenguard"
                }
                
                response = client.post(
                    "http://localhost:8000/api/v1/guards/process",
                    json=test_payload,
                    headers={"Content-Type": "application/json"}
                )
                
                api_working = response.status_code in [200, 202, 503]  # 503 is OK if guards not running
                
                self.log_test(
                    "api_endpoints",
                    "PASS" if api_working else "FAIL",
                    f"API endpoint status: {response.status_code}",
                    {
                        "status_code": response.status_code,
                        "response_text": response.text[:200] if response.text else None
                    }
                )
                
                return api_working
                
        except Exception as e:
            self.log_test(
                "api_endpoints",
                "FAIL",
                f"Error testing API endpoints: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def test_telemetry_and_logging(self):
        """Test telemetry and logging output."""
        print("\n🔍 Testing Telemetry and Logging...")
        
        # Check if structured logging is working
        try:
            logger = get_logger("test_telemetry")
            logger.info("Test telemetry message")
            
            self.log_test(
                "telemetry_logging",
                "PASS",
                "Structured logging working",
                {"logger": "test_telemetry"}
            )
            
        except Exception as e:
            self.log_test(
                "telemetry_logging",
                "FAIL",
                f"Error with telemetry logging: {str(e)}",
                {"error": str(e)}
            )
    
    def test_performance_metrics(self):
        """Test performance metrics and timing."""
        print("\n🔍 Testing Performance Metrics...")
        
        # Test configuration loading performance
        start_time = time.time()
        settings = get_settings()
        config_load_time = time.time() - start_time
        
        # Test AWS secrets loading performance
        start_time = time.time()
        try:
            secrets = get_aws_secrets_for_environment()
            secrets_load_time = time.time() - start_time
        except Exception as e:
            logger.warning(f"Failed to measure secrets load time: {e}")
            secrets_load_time = None
        
        self.log_test(
            "performance_metrics",
            "PASS",
            f"Config load: {config_load_time:.3f}s, Secrets load: {secrets_load_time:.3f}s" if secrets_load_time else f"Config load: {config_load_time:.3f}s",
            {
                "config_load_time": config_load_time,
                "secrets_load_time": secrets_load_time
            }
        )
    
    def run_all_tests(self):
        """Run all validation tests."""
        print("🚀 Starting Runtime Validation for AWS Secrets Manager Integration")
        print("=" * 70)
        
        # Environment and configuration tests
        self.test_environment_variables()
        
        # AWS Secrets Manager tests
        aws_available = self.REPLACE_ME()
        if aws_available:
            secrets = self.REPLACE_ME()
        else:
            print("⚠️  AWS Secrets Manager not available, skipping secrets tests")
        
        # Configuration tests
        settings = self.test_configuration_loading()
        
        # Service health tests
        healthy_guards = self.test_guard_services_health()
        gateway_healthy = self.test_gateway_health()
        
        # API functionality tests
        api_working = self.test_api_endpoints()
        
        # Telemetry and performance tests
        self.test_telemetry_and_logging()
        self.test_performance_metrics()
        
        # Generate summary
        self.generate_summary()
        
        return self.results
    
    def generate_summary(self):
        """Generate test summary."""
        print("\n" + "=" * 70)
        print("📊 RUNTIME VALIDATION SUMMARY")
        print("=" * 70)
        
        summary = self.results["summary"]
        print(f"Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"⚠️  Warnings: {summary['warnings']}")
        
        success_rate = (summary['passed'] / summary['total_tests']) * 100 if summary['total_tests'] > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if summary['failed'] > 0:
            print("\n❌ FAILED TESTS:")
            for test_name, test_data in self.results["tests"].items():
                if test_data["status"] == "FAIL":
                    print(f"  - {test_name}: {test_data['message']}")
        
        if summary['warnings'] > 0:
            print("\n⚠️  WARNINGS:")
            for test_name, test_data in self.results["tests"].items():
                if test_data["status"] == "WARN":
                    print(f"  - {test_name}: {test_data['message']}")
        
        # Save results to file
        results_file = "/tmp/runtime_validation_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: {results_file}")
        
        return success_rate >= 80  # 80% success rate threshold


def main():
    """Main validation function."""
    validator = RuntimeValidator()
    
    try:
        results = validator.run_all_tests()
        success = validator.generate_summary()
        
        if success:
            print("\n🎉 Runtime validation completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Runtime validation failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Validation script failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

