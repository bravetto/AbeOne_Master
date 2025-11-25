#!/bin/bash
# Enable File Sharing on macOS for Bryan to access
# Run this on Michael's Mac

echo " Enabling File Sharing for Bryan..."
echo ""

# Enable File Sharing
sudo systemsetup -setremotelogin on 2>/dev/null || echo "  Could not enable remote login via systemsetup"

# Alternative method using launchctl
echo " Enabling File Sharing service..."
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.smbd.plist 2>/dev/null || echo "  SMB service may already be running"

# Get current IP
CURRENT_IP=$(ifconfig | grep -A 5 "en0\|en1\|en2" | grep "inet " | head -1 | awk '{print $2}')

echo ""
echo " File Sharing Configuration:"
echo "   IP Address: $CURRENT_IP"
echo "   Share Path: /Users/michaelmataluni/Documents/AbeOne_Master"
echo ""
echo " Manual Steps:"
echo "   1. System Settings → General → Sharing"
echo "   2. Turn ON 'File Sharing'"
echo "   3. Click 'Options' → Enable 'Share files and folders using SMB'"
echo "   4. Add your user account with Read & Write access"
echo ""
echo " Bryan can connect via:"
echo "   smb://$CURRENT_IP"
echo "   or"
echo "   smb://192.168.6.252"
echo ""

