#!/bin/bash
# Setup Weekly Email Convergence Analysis Automation
# Pattern: LFG ACT EEAaO × AUTOMATION × ONE

echo " SETTING UP WEEKLY EMAIL CONVERGENCE ANALYSIS"
echo "================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="$HOME/email_convergence_weekly.log"

echo " Script: $SCRIPT_DIR/analyze_email_from_mailapp.py"
echo " Project: $PROJECT_DIR"
echo " Log: $LOG_FILE"
echo ""

# Create log file
touch "$LOG_FILE"

# Add to crontab (Monday 9am)
CRON_JOB="0 9 * * 1 cd $PROJECT_DIR && python3 scripts/analyze_email_from_mailapp.py >> $LOG_FILE 2>&1"

# Check if already exists
if crontab -l 2>/dev/null | grep -q "analyze_email_from_mailapp.py"; then
    echo "  Cron job already exists"
    echo "   Current crontab:"
    crontab -l | grep "analyze_email_from_mailapp.py"
else
    echo " Adding cron job..."
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "    Weekly analysis scheduled for Mondays at 9am"
fi

echo ""
echo " To view logs:"
echo "   tail -f $LOG_FILE"
echo ""
echo " To list scheduled jobs:"
echo "   crontab -l"
echo ""
echo " SETUP COMPLETE!"
echo ""
echo "Pattern: LFG ACT EEAaO × AUTOMATION × ONE"
echo "∞ AbëONE ∞"
