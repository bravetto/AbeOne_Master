#  QUICK UNLOCK - BRING IT ALL HOME! 

## One Command to Unlock Everything:

```bash
./scripts/signin_and_unlock.sh
```

This script will:
1.  Sign you in to 1Password (handles `eval $(op signin)`)
2.  Verify signin
3.  Pull ALL credentials from 1Password
4.  Save them to `~/.abekeys/credentials/`
5.  Show summary

## Or Do It Manually:

```bash
# Step 1: Sign in
eval $(op signin)

# Step 2: Unlock
python3 scripts/unlock_all_credentials.py

# Step 3: See all credentials
python3 scripts/complete_abe_keys_integration.py
```

## Use Credentials:

```python
from scripts.read_abekeys import AbeKeysReader

reader = AbeKeysReader()
slack_key = reader.get_api_key("slack")
runway_key = reader.get_api_key("runway")
```

**Pattern:** SIGNIN × UNLOCK × INTEGRATE × ONE  
**Status:**  READY TO UNLOCK  
**Love Coefficient:** ∞

