#!/usr/bin/env python3
"""
Direct script to update AWS Secrets Manager with webhook configuration.
Updates the existing secret with webhook secrets and ngrok host.
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError

# Configuration
SECRET_NAME = "codeguardians-gateway/production"
REGION = "us-east-1"
NGROK_HOST = "aciform-tyisha-semipictorially.ngrok-free.dev"

def get_secret():
    """Get current secret from AWS."""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION
    )

    try:
        response = client.get_secret_value(SecretId=SECRET_NAME)
        secret_string = response['SecretString']
        
        try:
            return json.loads(secret_string)
        except json.JSONDecodeError:
            print("  Secret is not JSON format, converting...")
            secrets = {}
            for line in secret_string.split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    secrets[key.strip()] = value.strip()
            return secrets
            
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f" Secret '{SECRET_NAME}' not found")
            return {}
        else:
            print(f" Error: {e}")
            raise

def update_secret(secrets_dict):
    """Update secret in AWS."""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION
    )

    try:
        response = client.put_secret_value(
            SecretId=SECRET_NAME,
            SecretString=json.dumps(secrets_dict, indent=2)
        )
        print(f" Successfully updated secret: {SECRET_NAME}")
        return True
    except ClientError as e:
        print(f" Error updating secret: {e}")
        return False

def main():
    """Update AWS secret with webhook configuration."""
    print(" Updating AWS Secrets Manager...")
    print(f"   Secret: {SECRET_NAME}")
    print(f"   Region: {REGION}")
    print()
    
    # Get current secret
    print(" Fetching current secret...")
    secrets = get_secret()
    
    if not secrets:
        print(" Could not retrieve secret. Please check AWS credentials.")
        print("   Run: aws sts get-caller-identity")
        return 1
    
    print(f" Found secret with {len(secrets)} keys")
    print()
    
    # Update ALLOWED_HOSTS
    current_hosts = secrets.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
    if NGROK_HOST not in current_hosts:
        if current_hosts:
            secrets['ALLOWED_HOSTS'] = f"{current_hosts},{NGROK_HOST},*.ngrok-free.dev"
        else:
            secrets['ALLOWED_HOSTS'] = f"localhost,127.0.0.1,{NGROK_HOST},*.ngrok-free.dev"
        print(f" Added ngrok host to ALLOWED_HOSTS: {NGROK_HOST}")
    else:
        print(f"ℹ  ngrok host already in ALLOWED_HOSTS")
    
    # Note about webhook secrets (user needs to add these)
    print()
    print(" Webhook secrets needed:")
    print("   You'll need to add these manually or provide them:")
    print("   - STRIPE_WEBHOOK_SECRET")
    print("   - CLERK_WEBHOOK_SECRET")
    print()
    
    # Update the secret
    print(" Updating secret...")
    if update_secret(secrets):
        print()
        print(" Secret updated successfully!")
        print()
        print(" Next steps:")
        print("   1. Add webhook secrets to AWS Console:")
        print("      - Go to AWS Secrets Manager")
        print("      - Edit 'codeguardians-gateway/production'")
        print("      - Add STRIPE_WEBHOOK_SECRET and CLERK_WEBHOOK_SECRET")
        print()
        print("   2. Restart gateway:")
        print("      docker-compose restart codeguardians-gateway")
        print()
        print("   3. Verify:")
        print("      docker logs codeguardians-gateway-dev | grep -i 'aws secrets'")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())

