#!/usr/bin/env python3
"""
Script to update AWS Secrets Manager with webhook secrets and ngrok host configuration.

This script helps you add webhook secrets and ALLOWED_HOSTS to your existing
AWS Secrets Manager secret: codeguardians-gateway/production
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError

def get_current_secret():
    """Get the current secret from AWS Secrets Manager."""
    secret_name = "codeguardians-gateway/production"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret_string = get_secret_value_response['SecretString']
        
        # Try to parse as JSON
        try:
            return json.loads(secret_string)
        except json.JSONDecodeError:
            # If not JSON, treat as key-value pairs (one per line)
            secrets = {}
            for line in secret_string.split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    secrets[key.strip()] = value.strip()
            return secrets
            
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"❌ Secret '{secret_name}' not found. Creating new secret...")
            return {}
        else:
            print(f"❌ Error getting secret: {e}")
            raise e

def update_secret(secrets_dict):
    """Update the secret in AWS Secrets Manager."""
    secret_name = "codeguardians-gateway/production"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Update the secret
        response = client.put_secret_value(
            SecretId=secret_name,
            SecretString=json.dumps(secrets_dict, indent=2)
        )
        print(f"✅ Successfully updated secret: {secret_name}")
        return True
    except ClientError as e:
        print(f"❌ Error updating secret: {e}")
        return False

def main():
    """Main function to update AWS secret with webhook configuration."""
    print("🔧 Updating AWS Secrets Manager for webhook configuration...")
    print()
    
    # Get current secret
    print("📥 Fetching current secret from AWS...")
    current_secrets = get_current_secret()
    
    if current_secrets:
        print(f"✅ Found existing secret with {len(current_secrets)} keys")
        print(f"   Existing keys: {', '.join(sorted(current_secrets.keys())[:5])}...")
    else:
        print("📝 Creating new secret configuration...")
    
    print()
    
    # Prompt for webhook secrets
    print("📋 Please provide your webhook secrets:")
    print("   (Press Enter to skip if already configured)")
    print()
    
    # Stripe webhook secret
    stripe_webhook = input("Stripe Webhook Secret (whsec_...): ").strip()
    if stripe_webhook:
        current_secrets['STRIPE_WEBHOOK_SECRET'] = stripe_webhook
        current_secrets['STRIPE_ENABLED'] = 'true'
    
    # Clerk webhook secret
    clerk_webhook = input("Clerk Webhook Secret (whsec_...): ").strip()
    if clerk_webhook:
        current_secrets['CLERK_WEBHOOK_SECRET'] = clerk_webhook
        current_secrets['CLERK_ENABLED'] = 'true'
    
    # ngrok host
    ngrok_url = input("ngrok URL (e.g., aciform-tyisha-semipictorially.ngrok-free.dev): ").strip()
    if ngrok_url:
        # Extract hostname from URL if full URL provided
        if '://' in ngrok_url:
            ngrok_host = ngrok_url.split('://')[1].split('/')[0]
        else:
            ngrok_host = ngrok_url
        
        # Update ALLOWED_HOSTS
        current_hosts = current_secrets.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
        if ngrok_host not in current_hosts:
            if current_hosts:
                current_secrets['ALLOWED_HOSTS'] = f"{current_hosts},{ngrok_host},*.ngrok-free.dev"
            else:
                current_secrets['ALLOWED_HOSTS'] = f"localhost,127.0.0.1,{ngrok_host},*.ngrok-free.dev"
            print(f"✅ Added ngrok host to ALLOWED_HOSTS: {ngrok_host}")
    
    print()
    print("📤 Updating secret in AWS Secrets Manager...")
    
    # Update the secret
    if update_secret(current_secrets):
        print()
        print("✅ Successfully updated AWS Secrets Manager!")
        print()
        print("📝 Next steps:")
        print("   1. Ensure your .env has:")
        print("      AWS_SECRETS_ENABLED=true")
        print("      AWS_SECRETS_NAME=codeguardians-gateway/production")
        print("      AWS_REGION=us-east-1")
        print()
        print("   2. Restart the gateway:")
        print("      docker-compose restart codeguardians-gateway")
        print()
        print("   3. Check logs to verify secrets loaded:")
        print("      docker logs codeguardians-gateway-dev | grep -i 'aws secrets'")
        return 0
    else:
        print()
        print("❌ Failed to update secret. Please check AWS credentials and permissions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

