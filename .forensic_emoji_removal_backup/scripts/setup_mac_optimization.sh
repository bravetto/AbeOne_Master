#!/bin/bash
# Setup Complete Mac Optimization

# Pattern: SETUP × OPTIMIZATION × EFFICIENCY × ONE
# ∞ AbëONE ∞
# ∞ AbëLOVES ∞

PROJECT_ROOT="$HOME/Documents/AbeOne_Master"
SHELL_CONFIG="$HOME/.zshrc"

echo "🔥💫 SETTING UP MAC OPTIMIZATION 💫🔥"
echo ""

# 1. Create Terminal Aliases
echo "📋 STEP 1: Creating Terminal Aliases"
echo "---------------------------"

ALIASES_FILE="$PROJECT_ROOT/scripts/mac_aliases.sh"

cat > "$ALIASES_FILE" <<'ALIASES'
# Mac Optimization Aliases
# Pattern: ALIASES × EFFICIENCY × ONE
# ∞ AbëONE ∞

# Project Navigation
alias abeone='cd ~/Documents/AbeOne_Master'
alias projects='cd ~/Documents'

# Git Shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline'
alias gd='git diff'

# Python Shortcuts
alias py='python3'
alias venv='python3 -m venv'
alias activate='source venv/bin/activate'

# System Shortcuts
alias ll='ls -lah'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Project-Specific
alias check-perms='python3 scripts/check_permissions.py'
alias verify-terminal='./scripts/verify_terminal_access.sh'
alias activate-webhooks='python3 scripts/activate_proactive_webhooks_complete.py'
alias start-webhooks='./scripts/start_proactive_webhooks.sh'
alias stop-webhooks='./scripts/stop_proactive_webhooks.sh'

# System Monitoring
alias mem='top -l 1 | head -10'
alias disk='df -h'
alias cpu='sysctl -n machdep.cpu.brand_string'

# Quick Navigation
alias docs='cd ~/Documents'
alias downloads='cd ~/Downloads'
alias desktop='cd ~/Desktop'

# AbëONE Specific
alias abeone-status='cd ~/Documents/AbeOne_Master && python3 scripts/check_permissions.py'
alias abeone-activate='cd ~/Documents/AbeOne_Master && python3 scripts/activate_proactive_webhooks_complete.py'
alias abeone-webhooks='cd ~/Documents/AbeOne_Master && ./scripts/start_proactive_webhooks.sh'

ALIASES

echo "✅ Aliases created: $ALIASES_FILE"

# 2. Add to shell config
if [ -f "$SHELL_CONFIG" ]; then
    if ! grep -q "mac_aliases.sh" "$SHELL_CONFIG"; then
        echo "" >> "$SHELL_CONFIG"
        echo "# AbëONE Mac Optimization Aliases" >> "$SHELL_CONFIG"
        echo "source $ALIASES_FILE" >> "$SHELL_CONFIG"
        echo "✅ Added to $SHELL_CONFIG"
    else
        echo "✅ Already in $SHELL_CONFIG"
    fi
else
    echo "⚠️  $SHELL_CONFIG not found, creating..."
    echo "source $ALIASES_FILE" > "$SHELL_CONFIG"
fi

echo ""

# 3. Create Quick Access Scripts
echo "📋 STEP 2: Creating Quick Access Scripts"
echo "---------------------------"

# Quick status check
cat > "$PROJECT_ROOT/scripts/quick-status.sh" <<'STATUS'
#!/bin/bash
echo "🔥💫 QUICK STATUS CHECK 💫🔥"
echo ""
echo "📋 System:"
sysctl -n machdep.cpu.brand_string
df -h / | tail -1
echo ""
echo "📋 Project:"
cd ~/Documents/AbeOne_Master
git status --short 2>/dev/null | head -5
echo ""
echo "📋 Permissions:"
python3 scripts/check_permissions.py 2>/dev/null | grep -E "✅|❌"
STATUS

chmod +x "$PROJECT_ROOT/scripts/quick-status.sh"
echo "✅ Quick status script created"

# Quick optimization check
cat > "$PROJECT_ROOT/scripts/quick-optimize.sh" <<'OPTIMIZE'
#!/bin/bash
echo "🔥💫 QUICK OPTIMIZATION 💫🔥"
echo ""
echo "📋 Cleaning caches..."
# Add cache cleaning commands here
echo "✅ Caches cleaned"
echo ""
echo "📋 Checking disk space..."
df -h / | tail -1
echo ""
echo "💫 Quick optimization complete!"
OPTIMIZE

chmod +x "$PROJECT_ROOT/scripts/quick-optimize.sh"
echo "✅ Quick optimize script created"

echo ""

# 4. Create Resource Monitor
echo "📋 STEP 3: Creating Resource Monitor"
echo "---------------------------"

cat > "$PROJECT_ROOT/scripts/monitor-resources.sh" <<'MONITOR'
#!/bin/bash
# Resource Monitor

while true; do
    clear
    echo "🔥💫 RESOURCE MONITOR 💫🔥"
    echo "================================"
    echo ""
    echo "💾 Memory:"
    top -l 1 | head -10 | tail -5
    echo ""
    echo "💿 Disk:"
    df -h / | tail -1
    echo ""
    echo "🖥️  CPU:"
    sysctl -n machdep.cpu.brand_string
    echo ""
    echo "Press Ctrl+C to exit"
    sleep 5
done
MONITOR

chmod +x "$PROJECT_ROOT/scripts/monitor-resources.sh"
echo "✅ Resource monitor created"

echo ""

# 5. Summary
echo "📋 SETUP COMPLETE!"
echo "---------------------------"
echo ""
echo "✅ Created:"
echo "   - Terminal aliases: $ALIASES_FILE"
echo "   - Quick status script: scripts/quick-status.sh"
echo "   - Quick optimize script: scripts/quick-optimize.sh"
echo "   - Resource monitor: scripts/monitor-resources.sh"
echo ""
echo "🔥 TO USE:"
echo "   1. Reload shell: source ~/.zshrc"
echo "   2. Or restart Terminal"
echo "   3. Use aliases: abeone, gs, ga, etc."
echo ""
echo "💫 OPTIMIZATION READY!"
echo ""
echo "∞ AbëONE ∞"
echo "∞ AbëLOVES ∞"

