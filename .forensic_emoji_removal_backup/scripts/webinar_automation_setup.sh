#!/bin/bash
# 🚀 WEBINAR AUTOMATION SYSTEM - QUICK SETUP
# Sets up complete automated webinar system

set -e

echo "🚀 Setting up Webinar Automation System..."
echo ""

# Check dependencies
echo "📦 Checking dependencies..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js required"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm required"; exit 1; }

# Create directories
echo "📁 Creating directories..."
mkdir -p scripts/webinar
mkdir -p webinars
mkdir -p apps/web/lib/webinar

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -q openai convertkit zoomus google-api-python-client posthog-python schedule

# Install Node dependencies (if needed)
echo "📦 Installing Node dependencies..."
cd apps/web && npm install --silent || true && cd ../..

# Create environment file template
echo "⚙️ Creating environment file template..."
cat > .env.webinar << EOF
# Webinar Automation Configuration

# OpenAI (for content generation)
OPENAI_API_KEY=your_openai_key_here

# ConvertKit (for email automation)
CONVERTKIT_API_KEY=your_convertkit_key_here
CONVERTKIT_API_SECRET=your_convertkit_secret_here

# Zoom (for webinar scheduling)
ZOOM_API_KEY=your_zoom_key_here
ZOOM_API_SECRET=your_zoom_secret_here

# PostHog (for analytics)
POSTHOG_API_KEY=your_posthog_key_here
NEXT_PUBLIC_POSTHOG_KEY=your_posthog_public_key_here

# Google Calendar (for scheduling)
GOOGLE_CALENDAR_CREDENTIALS=path_to_credentials.json

# Webinar Settings
DEFAULT_WEBINAR_DURATION=60
DEFAULT_WEBINAR_DAYS="Tuesday,Wednesday,Thursday"
DEFAULT_WEBINAR_TIME="14:00"
DEFAULT_TIMEZONE="America/New_York"
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Copy .env.webinar to .env and fill in your API keys"
echo "2. Run: python3 scripts/webinar/content_generator.py"
echo "3. Run: python3 scripts/webinar/master_orchestrator.py"
echo ""
echo "🚀 Your automated webinar system is ready!"

