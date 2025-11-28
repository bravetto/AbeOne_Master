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

# System Settings Access
alias sys-update='cd ~/Documents/AbeOne_Master && ./scripts/system_settings_access.sh software-update'
alias sys-privacy='cd ~/Documents/AbeOne_Master && ./scripts/system_settings_access.sh privacy'
alias sys-full-disk='cd ~/Documents/AbeOne_Master && ./scripts/system_settings_access.sh full-disk'
alias sys-storage='cd ~/Documents/AbeOne_Master && ./scripts/system_settings_access.sh storage'
alias sys-general='cd ~/Documents/AbeOne_Master && ./scripts/system_settings_access.sh general'

