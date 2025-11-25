"""
AWS Secrets Manager Integration

This module handles fetching secrets from AWS Secrets Manager
for database, Redis, and other service configurations.
"""

import json
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AWSSecretsManager:
    """AWS Secrets Manager client for fetching configuration secrets."""
    
    def __init__(self, secret_name: str = "codeguardians-gateway/production", region_name: str = "us-east-1"):
        self.secret_name = secret_name
        self.region_name = region_name
        self._secrets_cache = {}
        self._client = None
    
    def _get_client(self):
        """Get or create AWS Secrets Manager client."""
        if self._client is None:
            session = boto3.session.Session()
            self._client = session.client(
                service_name='secretsmanager',
                region_name=self.region_name
            )
        return self._client
    
    def get_secret(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get all secrets from AWS Secrets Manager.
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh secrets
            
        Returns:
            Dictionary containing all secrets
        """
        if not force_refresh and self._secrets_cache:
            return self._secrets_cache
        
        try:
            client = self._get_client()
            response = client.get_secret_value(SecretId=self.secret_name)
            
            # Parse the secret string as JSON
            secret_string = response.get('SecretString', '')
            if not secret_string:
                logger.error(f"Secret {self.secret_name} has no SecretString")
                return {}
                
            secrets = json.loads(secret_string)
            
            # Cache the secrets
            self._secrets_cache = secrets
            
            logger.info(f"Successfully retrieved secrets from AWS Secrets Manager: {self.secret_name}")
            return secrets
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'UnknownError')
            if error_code == 'ResourceNotFoundException':
                logger.error(f"Secret {self.secret_name} not found in AWS Secrets Manager")
            elif error_code == 'InvalidRequestException':
                logger.error(f"Invalid request for secret {self.secret_name}")
            elif error_code == 'InvalidParameterException':
                logger.error(f"Invalid parameter for secret {self.secret_name}")
            elif error_code == 'DecryptionFailureException':
                logger.error(f"Failed to decrypt secret {self.secret_name}")
            elif error_code == 'InternalServiceErrorException':
                logger.error(f"AWS Secrets Manager internal error for {self.secret_name}")
            else:
                logger.error(f"Error retrieving secret {self.secret_name}: {e}")
            
            # Return empty dict on error
            return {}
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse secret JSON for {self.secret_name}: {e}")
            return {}
            
        except Exception as e:
            logger.error(f"Unexpected error retrieving secret {self.secret_name}: {e}")
            return {}
    
    def get_database_url(self) -> Optional[str]:
        """Get database URL from secrets."""
        secrets = self.get_secret()
        return secrets.get('DATABASE_URL')
    
    def get_redis_url(self) -> Optional[str]:
        """Get Redis URL from secrets."""
        secrets = self.get_secret()
        return secrets.get('REDIS_URL')
    
    def get_clerk_secrets(self) -> Dict[str, Optional[str]]:
        """Get Clerk authentication secrets."""
        secrets = self.get_secret()
        return {
            'CLERK_SECRET_KEY': secrets.get('CLERK_SECRET_KEY'),
            'CLERK_PUBLISHABLE_KEY': secrets.get('CLERK_PUBLISHABLE_KEY'),
            'CLERK_WEBHOOK_SECRET': secrets.get('CLERK_WEBHOOK_SECRET')
        }
    
    def get_stripe_secrets(self) -> Dict[str, Optional[str]]:
        """Get Stripe payment secrets."""
        secrets = self.get_secret()
        return {
            'STRIPE_SECRET_KEY': secrets.get('STRIPE_SECRET_KEY'),
            'STRIPE_PUBLISHABLE_KEY': secrets.get('STRIPE_PUBLISHABLE_KEY'),
            'STRIPE_WEBHOOK_SECRET': secrets.get('STRIPE_WEBHOOK_SECRET')
        }
    
    def get_unified_api_key(self) -> Optional[str]:
        """Get unified API key for guard services."""
        secrets = self.get_secret()
        return secrets.get('UNIFIED_API_KEY') or secrets.get('GATEWAY_API_KEY')


# Global instance
aws_secrets = AWSSecretsManager()


def initialize_aws_secrets(region: str = "us-east-1", secret_name: str = "codeguardians-gateway/production") -> AWSSecretsManager:
    """
    Initialize AWS Secrets Manager instance.
    
    Args:
        region: AWS region name
        secret_name: Name of the secret in AWS Secrets Manager
        
    Returns:
        AWSSecretsManager instance
    """
    return AWSSecretsManager(secret_name=secret_name, region_name=region)


def validate_aws_secrets_available() -> bool:
    """
    Validate if AWS Secrets Manager is available and accessible.
    
    Returns:
        True if AWS Secrets Manager is available, False otherwise
    """
    try:
        manager = AWSSecretsManager()
        # Try to get client (will fail if AWS credentials not configured)
        client = manager._get_client()
        # Test connection by checking if we can call describe_secret
        # Don't fail if secret doesn't exist yet - just check if AWS is accessible
        try:
            client.describe_secret(SecretId=manager.secret_name)
        except ClientError as e:
            # If secret doesn't exist, that's okay - AWS is still accessible
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'ResourceNotFoundException':
                logger.debug(f"Secret {manager.secret_name} not found, but AWS is accessible")
                return True
            # For other errors, AWS might not be configured
            logger.debug(f"AWS Secrets Manager error: {e}")
            return False
        return True
    except Exception as e:
        logger.debug(f"AWS Secrets Manager not available: {e}")
        return False


def get_aws_secrets_for_environment(region: str = "us-east-1", secret_name: str = "codeguardians-gateway/production") -> Dict[str, Any]:
    """
    Get all secrets from AWS Secrets Manager for the current environment.
    
    Args:
        region: AWS region name
        secret_name: Name of the secret in AWS Secrets Manager
        
    Returns:
        Dictionary containing all secrets, or empty dict if unavailable
    """
    try:
        manager = initialize_aws_secrets(region=region, secret_name=secret_name)
        return manager.get_secret(force_refresh=True)
    except Exception as e:
        logger.error(f"Failed to get AWS secrets: {e}")
        return {}