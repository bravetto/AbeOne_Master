#!/usr/bin/env python3
"""
Simple AWS Secrets Manager Validation Script (Windows Compatible)

This script validates the AWS Secrets Manager integration without emojis
and with Windows-compatible output.
"""

import os
import sys
import json
import time
from typing import Dict, Any

def test_environment_setup():
    """Test environment variable setup."""
    print("Testing Environment Setup...")
    
    # Check AWS configuration
    aws_enabled = os.getenv('AWS_SECRETS_ENABLED', 'true').lower() == 'true'
    aws_secrets_name = os.getenv('AWS_SECRETS_NAME', 'codeguardians-gateway/production')
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    
    print(f"  AWS Secrets Manager Enabled: {aws_enabled}")
    print(f"  Secret Name: {aws_secrets_name}")
    print(f"  AWS Region: {aws_region}")
    
    return {
        "aws_enabled": aws_enabled,
        "secrets_name": aws_secrets_name,
        "region": aws_region
    }

def test_boto3_import():
    """Test boto3 import."""
    print("\nTesting boto3 Import...")
    
    try:
        import boto3
        print(f"  SUCCESS: boto3 available - version {boto3.__version__}")
        return True
    except ImportError as e:
        print(f"  FAILED: boto3 not available - {e}")
        return False

def test_aws_secrets_module():
    """Test AWS secrets module import."""
    print("\nTesting AWS Secrets Module...")
    
    try:
        sys.path.insert(0, '.')
        from app.core.aws_secrets import AWSSecretsManager, validate_aws_secrets_available
        print("  SUCCESS: AWS secrets module imported")
        
        # Test AWS availability
        available = validate_aws_secrets_available()
        print(f"  AWS Secrets Manager Available: {available}")
        
        return True
    except ImportError as e:
        print(f"  FAILED: Cannot import AWS secrets module - {e}")
        return False
    except Exception as e:
        print(f"  WARNING: AWS secrets module imported but error occurred - {e}")
        return True

def test_configuration_loading():
    """Test configuration loading."""
    print("\nTesting Configuration Loading...")
    
    try:
        sys.path.insert(0, '.')
        from app.core.config import get_settings
        
        start_time = time.time()
        settings = get_settings()
        load_time = time.time() - start_time
        
        print(f"  SUCCESS: Configuration loaded in {load_time:.3f}s")
        
        # Check key settings
        aws_enabled = getattr(settings, 'AWS_SECRETS_ENABLED', False)
        secret_key = getattr(settings, 'SECRET_KEY', '')
        database_url = getattr(settings, 'DATABASE_URL', '')
        redis_url = getattr(settings, 'REDIS_URL', '')
        
        print(f"  AWS Secrets Manager Enabled: {aws_enabled}")
        print(f"  SECRET_KEY present: {bool(secret_key)} (length: {len(secret_key)})")
        print(f"  DATABASE_URL present: {bool(database_url)}")
        print(f"  REDIS_URL present: {bool(redis_url)}")
        
        # Validate secret key length
        if len(secret_key) >= 32:
            print(f"  SUCCESS: SECRET_KEY length valid - {len(secret_key)} characters")
        else:
            print(f"  WARNING: SECRET_KEY too short - {len(secret_key)} characters (minimum 32)")
        
        return {
            "success": True,
            "load_time": load_time,
            "aws_enabled": aws_enabled,
            "secret_key_length": len(secret_key),
            "database_url_present": bool(database_url),
            "redis_url_present": bool(redis_url)
        }
        
    except ImportError as e:
        print(f"  FAILED: Cannot import application modules - {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"  FAILED: Configuration loading failed - {e}")
        return {"success": False, "error": str(e)}

def test_docker_files():
    """Test Docker-related files."""
    print("\nTesting Docker Files...")
    
    # Check Dockerfile
    dockerfile_path = "Dockerfile"
    if os.path.exists(dockerfile_path):
        print(f"  SUCCESS: Dockerfile exists")
        
        with open(dockerfile_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "boto3" in content:
            print(f"  SUCCESS: Dockerfile contains boto3")
        else:
            print(f"  WARNING: Dockerfile missing boto3")
            
        if "entrypoint.sh" in content:
            print(f"  SUCCESS: Dockerfile contains entrypoint script")
        else:
            print(f"  WARNING: Dockerfile missing entrypoint script")
    else:
        print(f"  FAILED: Dockerfile not found")
        return False
    
    # Check entrypoint script
    entrypoint_path = "scripts/entrypoint.sh"
    if os.path.exists(entrypoint_path):
        print(f"  SUCCESS: Entrypoint script exists")
        
        with open(entrypoint_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "AWS_SECRETS_ENABLED" in content:
            print(f"  SUCCESS: Entrypoint script contains AWS secrets logic")
        else:
            print(f"  WARNING: Entrypoint script missing AWS secrets logic")
    else:
        print(f"  FAILED: Entrypoint script not found")
        return False
    
    return True

def test_environment_files():
    """Test environment files."""
    print("\nTesting Environment Files...")
    
    # Check env.example
    env_example_path = "env.example"
    if os.path.exists(env_example_path):
        print(f"  SUCCESS: env.example exists")
        
        with open(env_example_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "AWS_SECRETS_ENABLED" in content:
            print(f"  SUCCESS: env.example contains AWS secrets configuration")
        else:
            print(f"  WARNING: env.example missing AWS secrets configuration")
    else:
        print(f"  FAILED: env.example not found")
    
    # Check env.unified
    env_unified_path = "env.unified"
    if os.path.exists(env_unified_path):
        print(f"  SUCCESS: env.unified exists")
        
        with open(env_unified_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "AWS_SECRETS_ENABLED" in content:
            print(f"  SUCCESS: env.unified contains AWS secrets configuration")
        else:
            print(f"  WARNING: env.unified missing AWS secrets configuration")
    else:
        print(f"  FAILED: env.unified not found")
    
    return True

def test_requirements():
    """Test requirements.txt."""
    print("\nTesting Requirements...")
    
    requirements_path = "requirements.txt"
    if os.path.exists(requirements_path):
        print(f"  SUCCESS: requirements.txt exists")
        
        with open(requirements_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "boto3" in content:
            print(f"  SUCCESS: requirements.txt contains boto3")
        else:
            print(f"  WARNING: requirements.txt missing boto3")
            
        if "botocore" in content:
            print(f"  SUCCESS: requirements.txt contains botocore")
        else:
            print(f"  WARNING: requirements.txt missing botocore")
    else:
        print(f"  FAILED: requirements.txt not found")
        return False
    
    return True

def main():
    """Main validation function."""
    print("AWS Secrets Manager Integration Validation")
    print("=" * 50)
    
    results = {}
    
    # Test environment setup
    results["environment"] = test_environment_setup()
    
    # Test boto3 import
    results["boto3"] = test_boto3_import()
    
    # Test AWS secrets module
    results["aws_secrets_module"] = test_aws_secrets_module()
    
    # Test application configuration
    results["app_config"] = test_configuration_loading()
    
    # Test Docker files
    results["docker_files"] = test_docker_files()
    
    # Test environment files
    results["environment_files"] = test_environment_files()
    
    # Test requirements
    results["requirements"] = test_requirements()
    
    # Generate summary
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if (isinstance(result, dict) and result.get("success", False)) or (isinstance(result, bool) and result))
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    # Save results
    results_file = "validation_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {results_file}")
    
    if passed_tests >= total_tests * 0.8:  # 80% success rate
        print("\nSUCCESS: Validation completed successfully!")
        return 0
    else:
        print("\nFAILED: Validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
