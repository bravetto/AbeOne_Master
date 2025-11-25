#!/bin/bash
# Setup Email Credentials for Convergence Analysis
# This script helps set up email credentials securely

echo "=========================================="
echo "EMAIL CONVERGENCE ANALYSIS - CREDENTIALS SETUP"
echo "=========================================="
echo ""

echo "Choose your email provider:"
echo "1) Gmail (recommended - use App Password)"
echo "2) Outlook/Office 365"
echo "3) Other IMAP provider"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📧 Gmail Setup Instructions:"
        echo "1. Enable 2-Step Verification: https://myaccount.google.com/security"
        echo "2. Generate App Password="REPLACE_ME"
        echo "   - Select 'Mail' and 'Other (Custom name)'"
        echo "   - Enter 'Email Analysis Script'"
        echo "   - Copy the 16-character password"
        echo ""
        read -p "Enter your Gmail address: " email
        read -sp "Enter your Gmail App Password (16 chars): " password
        echo ""
        ;;
    2)
        echo ""
        echo "📧 Outlook Setup:"
        read -p "Enter your Outlook email: " email
        read -sp "Enter your password: " password
        echo ""
        ;;
    3)
        echo ""
        echo "📧 IMAP Setup:"
        read -p "Enter your email address: " email
        read -sp "Enter your password: " password
        echo ""
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

if [ -z "$email" ] || [ -z "$password" ]; then
    echo "❌ Email and password are required"
    exit 1
fi

# Export for current session
export EMAIL_ADDRESS="$email"
export EMAIL_PASSWORD="REPLACE_ME"

echo ""
echo "✅ Credentials set for current session"
echo ""
echo "To make permanent, add to your ~/.zshrc or ~/.bashrc:"
echo "export EMAIL_ADDRESS='$email'"
echo "export EMAIL_PASSWORD='REPLACE_ME'"
echo ""
echo "Or run the analysis now with:"
echo "EMAIL_ADDRESS='$email' EMAIL_PASSWORD='REPLACE_ME' python3 scripts/analyze_email_convergence.py"
echo ""

