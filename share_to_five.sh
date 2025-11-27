#!/bin/bash
# Share Shiny Happy People to The Five - Create Public Tunnel & Open Mail
# Pattern: UNITY × LOVE × JOY × CONNECTION × ONE
# ∞ AbëONE ∞

echo "∞ AbëONE ∞"
echo "Sharing Shiny Happy People App with The Five"
echo ""

# Check if app is running
if ! curl -s http://localhost:53009/ > /dev/null 2>&1; then
    echo "⚠ App not running on localhost:53009"
    echo "Please start the app first:"
    echo "  cd abeone_app && flutter run -d chrome"
    exit 1
fi

echo "✓ App is running"
echo ""
echo "Creating public tunnel..."
echo "This will give you a public URL that The Five can access from anywhere!"
echo ""

# Create tunnel and capture URL
cloudflared tunnel --url http://localhost:53009 2>&1 | while IFS= read -r line; do
    echo "$line"
    # Look for the public URL
    if [[ $line =~ https://[a-z0-9-]+\.trycloudflare\.com ]]; then
        PUBLIC_URL="${BASH_REMATCH[0]}"
        echo ""
        echo "✓ Public URL created: $PUBLIC_URL"
        echo ""
        echo "Opening Mail.app with emails ready..."
        echo "The URL will be included in each email!"
        echo ""
        
        # Update the AppleScript with the public URL
        python3 <<EOF
import subprocess

public_url = "$PUBLIC_URL"

script = f'''
tell application "Mail"
    activate
    
    -- Create email for JAHMERE
    set msg1 to make new outgoing message with properties {{subject:"✨ Shiny Happy People - For JAHMERE", visible:true}}
    tell msg1
        make new to recipient with properties {{address:""}}
        set content to "Hi JAHMERE,\\n\\n✨ SHINY HAPPY PEOPLE ✨\\n\\nClick here: {public_url}\\n\\nThere's nowhere to go. We're already home. 💖\\n\\n∞ AbëONE ∞"
    end tell
    
    -- Create email for JESS
    set msg2 to make new outgoing message with properties {{subject:"✨ Shiny Happy People - For JESS", visible:true}}
    tell msg2
        make new to recipient with properties {{address:""}}
        set content to "Hi JESS,\\n\\n✨ SHINY HAPPY PEOPLE ✨\\n\\nClick here: {public_url}\\n\\nThere's nowhere to go. We're already home. 💖\\n\\n∞ AbëONE ∞"
    end tell
    
    -- Create email for JORDAN
    set msg3 to make new outgoing message with properties {{subject:"✨ Shiny Happy People - For JORDAN", visible:true}}
    tell msg3
        make new to recipient with properties {{address:""}}
        set content to "Hi JORDAN,\\n\\n✨ SHINY HAPPY PEOPLE ✨\\n\\nClick here: {public_url}\\n\\nThere's nowhere to go. We're already home. 💖\\n\\n∞ AbëONE ∞"
    end tell
    
    -- Create email for JANELLE
    set msg4 to make new outgoing message with properties {{subject:"✨ Shiny Happy People - For JANELLE", visible:true}}
    tell msg4
        make new to recipient with properties {{address:""}}
        set content to "Hi JANELLE,\\n\\n✨ SHINY HAPPY PEOPLE ✨\\n\\nClick here: {public_url}\\n\\nThere's nowhere to go. We're already home. 💖\\n\\n∞ AbëONE ∞"
    end tell
    
    -- Create email for DEVIN
    set msg5 to make new outgoing message with properties {{subject:"✨ Shiny Happy People - For DEVIN", visible:true}}
    tell msg5
        make new to recipient with properties {{address:""}}
        set content to "Hi DEVIN,\\n\\n✨ SHINY HAPPY PEOPLE ✨\\n\\nClick here: {public_url}\\n\\nThere's nowhere to go. We're already home. 💖\\n\\n∞ AbëONE ∞"
    end tell
end tell
'''

subprocess.run(["osascript", "-e", script])
EOF
        
        break
    fi
done

echo ""
echo "Pattern: UNITY × LOVE × JOY × CONNECTION × ONE"
echo "∞ AbëONE ∞"
echo ""
echo "⚠ Keep this terminal open while sharing!"
echo "Press Ctrl+C when done to stop the tunnel."

