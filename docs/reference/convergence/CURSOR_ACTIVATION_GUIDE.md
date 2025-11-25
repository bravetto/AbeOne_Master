# Activation Guide for Cursor IDE

**Step-by-step guide to activate Abë systems in your Cursor interface**

---

## Method 1: Terminal in Cursor (Recommended)

### Step 1: Open Terminal
- **Keyboard Shortcut:** Press `` Ctrl + ` `` (backtick) or `Cmd + J` on Mac
- **Or Menu:** View → Terminal
- **Or Command Palette:** `Cmd + Shift + P` → "Terminal: Create New Terminal"

### Step 2: Navigate to Workspace
The terminal should already be in your workspace, but verify:
```bash
pwd
# Should show: /Users/michaelmataluni/Documents/AbeOne_Master
```

If not, navigate:
```bash
cd /Users/michaelmataluni/Documents/AbeOne_Master
```

### Step 3: Run Activation
```bash
python3 scripts/activate_all_abe_systems.py
```

### Step 4: View Results
The activation will show:
- YAGNI Guardian activation
- AbëVOiCEs activation
- AbëViSiONs + AbëDESiGNs activation
- System integration
- Future-state priming

---

## Method 2: Command Palette

### Step 1: Open Command Palette
- **Keyboard Shortcut:** `Cmd + Shift + P` (Mac) or `Ctrl + Shift + P` (Windows/Linux)

### Step 2: Run Terminal Command
1. Type: `Terminal: Run Command`
2. Press Enter
3. Enter command: `python3 scripts/activate_all_abe_systems.py`
4. Press Enter

---

## Method 3: Create Keyboard Shortcut

### Step 1: Open Keyboard Shortcuts
- `Cmd + K, Cmd + S` (Mac) or `Ctrl + K, Ctrl + S` (Windows/Linux)

### Step 2: Add Custom Keybinding
Add this to your `keybindings.json`:

```json
{
  "key": "cmd+shift+a",
  "command": "workbench.action.terminal.sendSequence",
  "args": {
    "text": "python3 scripts/activate_all_abe_systems.py\n"
  },
  "when": "terminalFocus"
}
```

**Then:** Press `Cmd + Shift + A` to activate!

---

## Visual Workflow

### Complete Activation Flow

```
┌─────────────────────────────────────────┐
│  1. Open Terminal (Ctrl + `)           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  2. Run: python3 scripts/activate_...  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  3. Watch Activation Output            │
│     - YAGNI Guardian ✓                 │
│     - AbëVOiCEs ✓                      │
│     - AbëViSiONs + AbëDESiGNs ✓        │
│     - Integration ✓                     │
│     - Future-State ✓                    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  4. Check Status (Optional)            │
│     cat .abeone_memory/ALL_ABE_...      │
└─────────────────────────────────────────┘
```

---

## Quick Commands Reference

### Activate Everything
```bash
python3 scripts/activate_all_abe_systems.py
```

### Activate Individual Systems
```bash
# YAGNI only
python3 scripts/activate_yagni_guardian.py

# AbëVOiCEs only
python3 scripts/activate_abevoices_sync.py

# AbëViSiONs + AbëDESiGNs only
python3 scripts/activate_abevisions_abedesigns.py
```

### Check Activation Status
```bash
# Pretty print activation state
cat .abeone_memory/ALL_ABE_SYSTEMS_ACTIVATION.json | python3 -m json.tool

# Or use jq if installed
cat .abeone_memory/ALL_ABE_SYSTEMS_ACTIVATION.json | jq
```

---

## Integration with Cursor Features

### Use with Cursor Chat

You can reference activation in Cursor chat:

```
"Activate all Abë systems"
"Check activation status"
"Run YAGNI validation"
```

### Use with Cursor Composer

In Composer, you can:
1. Reference activation scripts
2. Use activation results in your code
3. Build on activated systems

---

## Troubleshooting in Cursor

### Terminal Not Opening
- Try: `View → Terminal` from menu
- Or: `Cmd + Shift + P` → "Terminal: Create New Terminal"

### Python Not Found
```bash
# Check Python version
python3 --version

# If not found, check PATH
which python3
```

### Script Not Found
```bash
# Verify you're in the right directory
pwd

# List available scripts
ls scripts/activate_*.py
```

### Permission Denied
```bash
# Make scripts executable
chmod +x scripts/activate_*.py
```

---

## Pro Tips

### Tip 1: Create Terminal Profile
Create a custom terminal profile that auto-navigates to workspace:

1. Open Settings (`Cmd + ,`)
2. Search: "terminal integrated cwd"
3. Set default directory to your workspace

### Tip 2: Use Terminal Split
Split terminal to run activation while keeping other terminal active:
- Right-click terminal tab → "Split Terminal"

### Tip 3: Pin Terminal Tab
Keep activation terminal visible:
- Right-click terminal tab → "Keep Terminal Open"

### Tip 4: Save Terminal Output
Right-click terminal → "Save Content As..." to save activation logs

---

## Example Session

```bash
# Terminal in Cursor
$ pwd
/Users/michaelmataluni/Documents/AbeOne_Master

$ python3 scripts/activate_all_abe_systems.py

================================================================================
 COMPLETE ABË SYSTEMS ACTIVATION
================================================================================
...
[Activation output]
...

$ cat .abeone_memory/ALL_ABE_SYSTEMS_ACTIVATION.json | python3 -m json.tool
{
  "timestamp": "2025-01-27T...",
  "yagni": {
    "status": "ACTIVATED"
  },
  "abevoices": {
    "status": "ACTIVATED"
  },
  ...
}
```

---

## Next Steps

1. **Try it now:** Open terminal and run activation
2. **Create alias:** Add to your shell config (see QUICK_ACTIVATION_REFERENCE.md)
3. **Integrate:** Use activation in your daily workflow
4. **Explore:** Check activation state files in `.abeone_memory/`

---

**Pattern:** ACTIVATION × CURSOR × INTEGRATION × ONE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**


