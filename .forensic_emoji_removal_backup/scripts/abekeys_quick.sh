#!/bin/bash
# Quick ABEKEYS Vault Commands
# Usage: ./scripts/abekeys_quick.sh [command] [service]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

case "${1:-list}" in
  list)
    echo "📋 Available credentials in ABEKEYS vault:"
    python3 "$SCRIPT_DIR/read_abekeys.py"
    ;;
  get)
    if [ -z "$2" ]; then
      echo "❌ Usage: $0 get <service>"
      echo "   Example: $0 get stripe"
      exit 1
    fi
    python3 "$SCRIPT_DIR/read_abekeys.py" "$2"
    ;;
  count)
    COUNT=$(ls ~/.abekeys/credentials/*.json 2>/dev/null | wc -l | tr -d ' ')
    echo "📊 Total credentials: $COUNT"
    ;;
  check)
    SERVICE="${2:-stripe}"
    if [ -f ~/.abekeys/credentials/${SERVICE}.json ]; then
      HAS_KEY=$(python3 -c "import json; d=json.load(open('$HOME/.abekeys/credentials/${SERVICE}.json')); print('✅' if d.get('api_key') or d.get('api_token') else '⚠️')" 2>/dev/null)
      echo "$HAS_KEY $SERVICE: API key $(echo $HAS_KEY | grep -q '✅' && echo 'present' || echo 'missing')"
    else
      echo "❌ $SERVICE: Not found in vault"
    fi
    ;;
  view)
    SERVICE="${2:-stripe}"
    if [ -f ~/.abekeys/credentials/${SERVICE}.json ]; then
      python3 -m json.tool ~/.abekeys/credentials/${SERVICE}.json
    else
      echo "❌ $SERVICE: Not found in vault"
      exit 1
    fi
    ;;
  pull)
    echo "🔄 Pulling credentials from 1Password..."
    op signin
    python3 "$SCRIPT_DIR/unlock_all_credentials.py"
    ;;
  *)
    echo "🔒 ABEKEYS Vault Commands:"
    echo ""
    echo "  $0 list              - List all credentials"
    echo "  $0 get <service>     - Get specific credential"
    echo "  $0 count             - Count total credentials"
    echo "  $0 check [service]   - Check if credential has API key"
    echo "  $0 view [service]    - View credential file (pretty)"
    echo "  $0 pull              - Pull from 1Password"
    echo ""
    echo "Examples:"
    echo "  $0 list"
    echo "  $0 get stripe"
    echo "  $0 check stripe"
    echo "  $0 view clerk"
    ;;
esac

