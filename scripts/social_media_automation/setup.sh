#!/bin/bash
#  Social Media Automation Setup Script
# Sets up the better-than-Sintra scheduler

set -e

echo " Setting up Social Media Automation System..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo " Python 3 is required"
    exit 1
fi

# Create virtual environment
echo " Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo " Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env.social from example
if [ ! -f .env.social ]; then
    echo " Creating .env.social from example..."
    cp .env.social.example .env.social
    echo " Created .env.social - Please fill in your API credentials"
else
    echo " .env.social already exists"
fi

echo ""
echo " Setup complete!"
echo ""
echo " Next steps:"
echo "1. Edit .env.social and add your API credentials"
echo "2. Get Facebook/Instagram tokens from: https://developers.facebook.com/"
echo "3. Get LinkedIn token from: https://www.linkedin.com/developers/"
echo "4. Run: python social_scheduler.py"
echo ""
echo " Your better-than-Sintra scheduler is ready!"

