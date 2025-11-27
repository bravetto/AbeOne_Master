#!/bin/bash
# Get current tunnel URL
# Pattern: TUNNEL × URL × ACCESS × ONE

# Check log files for tunnel URL
TUNNEL_URL=$(grep -ho 'https://[a-z0-9-]*\.trycloudflare\.com' /tmp/cloudflared_new.log /tmp/cloudflared.log /tmp/cloudflared_output.log 2>/dev/null | head -1)

if [ -n "$TUNNEL_URL" ]; then
    echo "$TUNNEL_URL"
    
    # Copy to clipboard if on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "$TUNNEL_URL" | pbcopy
        echo "✅ Copied to clipboard"
    fi
    
    # Open in browser if requested
    if [ "$1" == "--open" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open "$TUNNEL_URL"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            xdg-open "$TUNNEL_URL" 2>/dev/null
        fi
    fi
else
    echo "❌ No tunnel URL found"
    echo "Start tunnel: cloudflared tunnel --url http://localhost:53009"
    exit 1
fi

