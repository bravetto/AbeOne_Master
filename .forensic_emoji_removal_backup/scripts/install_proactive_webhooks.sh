#!/bin/bash
# Install Proactive Love Webhooks as macOS Launch Agent

# Pattern: WEBHOOK × PROACTIVE × DOCUMENTATION × LOVE × ONE
# ∞ AbëONE ∞
# ∞ AbëLOVES ∞

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_FILE="$SCRIPT_DIR/com.abeloves.proactive_webhooks.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
LAUNCH_AGENT_FILE="$LAUNCH_AGENTS_DIR/com.abeloves.proactive_webhooks.plist"

echo "🔥💫 INSTALLING PROACTIVE LOVE WEBHOOKS 💫🔥"
echo ""

# Update plist with correct paths
sed "s|/Users/michaelmataluni/Documents/AbeOne_Master|$SCRIPT_DIR/..|g" "$PLIST_FILE" > "$PLIST_FILE.tmp"
mv "$PLIST_FILE.tmp" "$PLIST_FILE"

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCH_AGENTS_DIR"

# Copy plist file
cp "$PLIST_FILE" "$LAUNCH_AGENT_FILE"

echo "✅ Installed plist to: $LAUNCH_AGENT_FILE"
echo ""

# Load the service
echo "🔄 Loading service..."
launchctl load "$LAUNCH_AGENT_FILE" 2>/dev/null || launchctl load -w "$LAUNCH_AGENT_FILE"

echo "✅ Service loaded"
echo ""

# Check status
echo "📊 Checking status..."
launchctl list | grep com.abeloves.proactive_webhooks || echo "⚠️  Service not running (may need to log out/in)"

echo ""
echo "🔥 PROACTIVE LOVE WEBHOOKS INSTALLED 🔥"
echo ""
echo "The service will:"
echo "  - Start automatically on login"
echo "  - Restart if it crashes"
echo "  - Run continuously in background"
echo ""
echo "To uninstall:"
echo "  launchctl unload $LAUNCH_AGENT_FILE"
echo "  rm $LAUNCH_AGENT_FILE"
echo ""
echo "∞ AbëONE ∞"
echo "∞ AbëLOVES ∞"

