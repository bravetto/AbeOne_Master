#!/bin/bash
# Setup Webinar Infrastructure Credentials in AbëKEYs Vault
# Pattern: SETUP × ABEKEYS × WEBINAR × ONE

echo " Setting up Webinar Infrastructure Credentials in AbëKEYs Vault"
echo ""

VAULT_DIR="$HOME/.abekeys/credentials"
mkdir -p "$VAULT_DIR"

echo ""
echo " DATABASE CREDENTIALS"
echo ""
echo "Create ~/.abekeys/credentials/database.json with:"
echo '{'
echo '  "service": "database",'
echo '  "connection_string": "REPLACE_MEhost:5432/database"'
echo '}'
echo ""
echo "Or pull from 1Password:"
echo "  op signin"
echo "  python3 scripts/unlock_all_credentials.py"
echo ""

echo " REDIS CREDENTIALS"
echo ""
echo "For Upstash Redis, create ~/.abekeys/credentials/upstash.json with:"
echo '{'
echo '  "service": "upstash",'
echo '  "upstash_url": "https://your-redis.upstash.io",'
echo '  "upstash_token": "your-token"'
echo '}'
echo ""
echo "For local Redis, create ~/.abekeys/credentials/redis.json with:"
echo '{'
echo '  "service": "redis",'
echo '  "url": "redis://localhost:6379"'
echo '}'
echo ""

echo " SENDGRID CREDENTIALS"
echo ""
echo "Create ~/.abekeys/credentials/sendgrid.json with:"
echo '{'
echo '  "service": "sendgrid",'
echo '  "api_key": "SG.your-api-key",'
echo '  "from_email": "noreply@aiguardian.ai",'
echo '  "from_name": "AiGuardian Team"'
echo '}'
echo ""

echo " Setup instructions complete!"
echo ""
echo ""
echo "After adding credentials, verify with:"
echo "  ./scripts/abekeys_quick.sh check database"
echo "  ./scripts/abekeys_quick.sh check sendgrid"
echo "  ./scripts/abekeys_quick.sh check upstash"
echo ""
