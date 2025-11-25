#!/usr/bin/env python3
"""
Simple AWS Secrets Manager Validation Script

This script validates the AWS Secrets Manager integration without requiring
the full application to be running.
"""

import os
import sys
import json
import time
from typing import Dict, Any

def test_environment_setup():
    """Test environment variable setup."""
    print("🔍 Testing Environment Setup...")
    
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

def REPLACE_ME():
    """Test AWS CLI availability."""
    print("\n🔍 Testing AWS CLI...")
    
    try:
        import subprocess
        result = subprocess.run(['aws', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ AWS CLI available: {result.stdout.strip()}")
            return True
        else:
            print(f"  ❌ AWS CLI error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("  ❌ AWS CLI not found")
        return False
    except Exception as e:
        print(f"  ❌ AWS CLI test failed: {e}")
        return False

def REPLACE_ME():
    """Test AWS credentials."""
    print("\n🔍 Testing AWS Credentials...")
    
    try:
        import subprocess
        result = subprocess.run(['aws', 'sts', 'get-caller-identity'], capture_output=True, text=True)
        if result.returncode == 0:
            identity = json.loads(result.stdout)
            print(f"  ✅ AWS credentials valid")
            print(f"  Account: {identity.get('Account', 'Unknown')}")
            print(f"  User/Role: {identity.get('Arn', 'Unknown')}")
            return True
        else:
            print(f"  ❌ AWS credentials invalid: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ AWS credentials test failed: {e}")
        return False

def test_boto3_import():
    """Test boto3 import."""
    print("\n🔍 Testing boto3 Import...")
    
    try:
        import boto3
        print(f"  ✅ boto3 available: {boto3.__version__}")
        return True
    except ImportError as e:
        print(f"  ❌ boto3 not available: {e}")
        return False

def REPLACE_ME():
    """Test AWS Secrets Manager access."""
    print("\n🔍 Testing AWS Secrets Manager Access...")
    
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        # Get configuration
        aws_secrets_name = os.getenv('AWS_SECRETS_NAME', 'codeguardians-gateway/production')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        # Create client
        client = boto3.client('secretsmanager', region_name=aws_region)
        
        # Test secret access
        start_time = time.time()
        response = client.get_secret_value(SecretId=aws_secrets_name)
        load_time = time.time() - start_time
        
        print(f"  ✅ Secret accessed successfully in {load_time:.3f}s")
        
        # Parse secret content
        secret_string = response.get('SecretString', '')
        if secret_string:
            try:
                secret_data = json.loads(secret_string)
                print(f"  📊 Secret contains {len(secret_data)} keys: {list(secret_data.keys())}")
                
                # Check for required secrets
                required_secrets = ['SECRET_KEY', 'DATABASE_URL', 'REDIS_URL']
                missing_secrets = [secret for secret in required_secrets if secret not in secret_data]
                
                if missing_secrets:
                    print(f"  ⚠️  Missing required secrets: {missing_secrets}")
                else:
                    print(f"  ✅ All required secrets present")
                
                return {
                    "success": True,
                    "load_time": load_time,
                    "secret_count": len(secret_data),
                    "missing_secrets": missing_secrets
                }
            except json.JSONDecodeError:
                print(f"  ⚠️  Secret is not valid JSON")
                return {"success": True, "load_time": load_time, "json_error": True}
        else:
            print(f"  ⚠️  Secret string is empty")
            return {"success": True, "load_time": load_time, "empty_secret": True}
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"  ❌ Secret '{aws_secrets_name}' not found")
        elif error_code == 'AccessDeniedException':
            print(f"  ❌ Access denied to secret '{aws_secrets_name}'")
        else:
            print(f"  ❌ AWS Secrets Manager error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"  ❌ AWS Secrets Manager test failed: {e}")
        return {"success": False, "error": str(e)}

def test_application_config_loading():
    """Test application configuration loading."""
    print("\n🔍 Testing Application Configuration Loading...")
    
    try:
        # Add the app directory to Python path
        sys.path.insert(0, '/app')
        
        from app.core.config import get_settings
        
        start_time = time.time()
        settings = get_settings()
        load_time = time.time() - start_time
        
        print(f"  ✅ Configuration loaded in {load_time:.3f}s")
        
        # Check key settings
        aws_enabled = getattr(settings, 'AWS_SECRETS_ENABLED', False)
        secret_key = getattr(settings, 'SECRET_KEY', '')
        database_url = getattr(settings, 'DATABASE_URL', '')
        redis_url = getattr(settings, 'REDIS_URL', '')
        
        print(f"  📊 AWS Secrets Manager Enabled: {aws_enabled}")
        print(f"  📊 SECRET_KEY present: {bool(secret_key)} (length: {len(secret_key)})")
        print(f"  📊 DATABASE_URL present: {bool(database_url)}")
        print(f"  📊 REDIS_URL present: {bool(redis_url)}")
        
        # Validate secret key length
        if len(secret_key) >= 32:
            print(f"  ✅ SECRET_KEY length valid: {len(secret_key)} characters")
        else:
            print(f"  ⚠️  SECRET_KEY too short: {len(secret_key)} characters (minimum 32)")
        
        return {
            "success": True,
            "load_time": load_time,
            "aws_enabled": aws_enabled,
            "secret_key_length": len(secret_key),
            "database_url_present": bool(database_url),
            "redis_url_present": bool(redis_url)
        }
        
    except ImportError as e:
        print(f"  ❌ Cannot import application modules: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"  ❌ Configuration loading failed: {e}")
        return {"success": False, "error": str(e)}

def test_docker_entrypoint():
    """Test Docker entrypoint script."""
    print("\n🔍 Testing Docker Entrypoint Script...")
    
    entrypoint_script = "/app/entrypoint.sh"
    
    if os.path.exists(entrypoint_script):
        print(f"  ✅ Entrypoint script exists: {entrypoint_script}")
        
        # Check if script is executable
        if os.access(entrypoint_script, os.X_OK):
            print(f"  ✅ Entrypoint script is executable")
        else:
            print(f"  ⚠️  Entrypoint script is not executable")
        
        # Check script content
        try:
            with open(entrypoint_script, 'r') as f:
                content = f.read()
                
            if "AWS_SECRETS_ENABLED" in content:
                print(f"  ✅ Entrypoint script contains AWS secrets logic")
            else:
                print(f"  ⚠️  Entrypoint script missing AWS secrets logic")
                
            if "aws secretsmanager get-secret-value" in content:
                print(f"  ✅ Entrypoint script contains AWS CLI commands")
            else:
                print(f"  ⚠️  Entrypoint script missing AWS CLI commands")
                
        except Exception as e:
            print(f"  ❌ Error reading entrypoint script: {e}")
    else:
        print(f"  ❌ Entrypoint script not found: {entrypoint_script}")
        return {"success": False, "error": "Entrypoint script not found"}

def main():
    """Main validation function."""
    print("🚀 AWS Secrets Manager Integration Validation")
    print("=" * 60)
    
    results = {}
    
    # Test environment setup
    results["environment"] = test_environment_setup()
    
    # Test AWS CLI
    results["aws_cli"] = REPLACE_ME()
    
    # Test AWS credentials
    results["aws_credentials"] = REPLACE_ME()
    
    # Test boto3 import
    results["boto3"] = test_boto3_import()
    
    # Test AWS Secrets Manager access
    results["secrets_manager"] = REPLACE_ME()
    
    # Test application configuration
    results["app_config"] = test_application_config_loading()
    
    # Test Docker entrypoint
    results["entrypoint"] = test_docker_entrypoint()
    
    # Generate summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result.get("success", False))
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    # Save results
    results_file = "/tmp/secrets_validation_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {results_file}")
    
    if passed_tests >= total_tests * 0.8:  # 80% success rate
        print("\n🎉 Validation completed successfully!")
        return 0
    else:
        print("\n❌ Validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

