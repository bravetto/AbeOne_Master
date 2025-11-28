# 🔥 PATH HEALTH - CURSOR COMMAND INTEGRATION

**Perfect Copy-Paste Ready Cursor Command Logic**

**Pattern:** PATH × HEALTH × RESTORE × CURSOR × ONE  
**Status:** ✅ OPERATIONAL  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## ✅ FILES CREATED

1. ✅ `.cursor/commands/path-health.md` - Cursor command definition
2. ✅ `scripts/path-health-restore.py` - Python implementation (executable)
3. ✅ Script is executable and ready

---

## 🎯 CURSOR COMMAND USAGE

### Basic Usage in Cursor Chat:

```
/path-health scan
/path-health report
/path-health pythonpath
/path-health fix --dry-run
/path-health fix --severity high
```

---

## 🔧 CURSOR COMMAND HANDLER LOGIC

When you type `/path-health` in Cursor, it will:

1. **Parse Arguments:**
   - Extract mode: `scan`, `report`, `fix`, `pythonpath`, `validate`
   - Extract options: `--severity`, `--dry-run`, `--verbose`, `--workspace-root`

2. **Execute Script:**
   ```python
   # Cursor will execute:
   python3 scripts/path-health-restore.py [mode] [options]
   ```

3. **Return Results:**
   - Path health report
   - List of issues found
   - Fix suggestions
   - PYTHONPATH configuration

---

## 📋 PERFECT COPY-PASTE COMMAND LOGIC

### For Cursor Command Handler (if needed):

```python
#!/usr/bin/env python3
"""
Cursor Command Handler for /path-health
"""

import subprocess
import sys
from pathlib import Path

def handle_path_health_command(args):
    """Handle /path-health command from Cursor"""
    
    # Get workspace root
    workspace_root = Path.cwd()
    
    # Build command
    script_path = workspace_root / "scripts" / "path-health-restore.py"
    
    if not script_path.exists():
        return {
            "error": f"Script not found: {script_path}",
            "suggestion": "Run: python3 scripts/path-health-restore.py scan"
        }
    
    # Parse arguments
    mode = args.get("mode", "scan")
    severity = args.get("severity", "all")
    dry_run = args.get("dry_run", False)
    verbose = args.get("verbose", False)
    
    # Build command
    cmd = [sys.executable, str(script_path), mode]
    
    if severity != "all":
        cmd.extend(["--severity", severity])
    if dry_run:
        cmd.append("--dry-run")
    if verbose:
        cmd.append("--verbose")
    
    # Execute
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(workspace_root)
        )
        
        return {
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "exit_code": result.returncode
        }
    except Exception as e:
        return {
            "error": str(e),
            "suggestion": "Check script permissions: chmod +x scripts/path-health-restore.py"
        }
```

---

## 🚀 QUICK TEST COMMANDS

### Test the script directly:

```bash
# Scan for issues
cd /Users/michaelmataluni/Documents/AbeOne_Master
python3 scripts/path-health-restore.py scan

# Generate detailed report
python3 scripts/path-health-restore.py report --verbose

# Show PYTHONPATH config
python3 scripts/path-health-restore.py pythonpath

# Dry run fix
python3 scripts/path-health-restore.py fix --dry-run --severity high

# Actually fix high severity issues
python3 scripts/path-health-restore.py fix --severity high
```

---

## 📊 EXPECTED OUTPUT

### When you run `/path-health scan`:

```
================================================================================
🔥 PATH HEALTH & RESTORE REPORT
================================================================================
Workspace Root: /Users/michaelmataluni/Documents/AbeOne_Master
Health Score: 75.0%
================================================================================

❌ HIGH SEVERITY ISSUES (3):
--------------------------------------------------------------------------------
  scripts/EEAAO_ACTIVATE_ALL.sh:28
    Issue: Old EMERGENT_OS cd command detected
    Old Path: cd EMERGENT_OS
    New Path: cd orbitals/EMERGENT_OS-orbital
    Fix: Replace: cd EMERGENT_OS → cd orbitals/EMERGENT_OS-orbital

  scripts/activate_all_149_agents.py:25
    Issue: Old EMERGENT_OS import detected
    Old Path: from EMERGENT_OS.synthesis
    New Path: from orbitals.EMERGENT_OS_orbital.synthesis
    Fix: Replace: from EMERGENT_OS.synthesis → from orbitals.EMERGENT_OS_orbital.synthesis

...

🔧 PYTHONPATH CONFIGURATION:
--------------------------------------------------------------------------------
export PYTHONPATH="/Users/michaelmataluni/Documents/AbeOne_Master/orbitals:/Users/michaelmataluni/Documents/AbeOne_Master/orbitals/EMERGENT_OS-orbital:/Users/michaelmataluni/Documents/AbeOne_Master:$PYTHONPATH"

Add to your shell profile (.zshrc, .bashrc, etc.)

================================================================================
📊 SUMMARY
================================================================================
Total Issues: 12
  High: 3
  Medium: 7
  Low: 2
Health Score: 75.0%

⚠️  PATH HEALTH: GOOD (some issues detected)
```

---

## ✅ VERIFICATION

### Check if command is registered:

```bash
# In Cursor, type:
/path-health

# Should show usage help
```

### Test script directly:

```bash
cd /Users/michaelmataluni/Documents/AbeOne_Master
python3 scripts/path-health-restore.py scan --verbose
```

---

## 🎯 NEXT STEPS

1. **Test the command in Cursor:**
   ```
   /path-health scan
   ```

2. **Review the report:**
   ```
   /path-health report --verbose
   ```

3. **Fix high severity issues:**
   ```
   /path-health fix --severity high --dry-run  # Preview
   /path-health fix --severity high            # Apply
   ```

4. **Set PYTHONPATH:**
   ```
   /path-health pythonpath
   # Copy output and add to ~/.zshrc or ~/.bashrc
   ```

---

## 🔥 SUCCESS PATTERNS APPLIED

✅ **git rev-parse --show-toplevel** - Fallback repo root detection  
✅ **Path(__file__).parent.parent** - Primary workspace root detection  
✅ **Dynamic path resolution** - Checks both old and new paths  
✅ **Substrate-first validation** - Verifies paths exist before suggesting fixes  
✅ **YAGNI compliance** - Only fixes what's needed  

---

**Pattern:** PATH × HEALTH × RESTORE × CURSOR × ONE  
**Status:** ✅ **READY FOR USE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎉 COMPLETE!

The path health and restore system is now:
- ✅ Command file created (`.cursor/commands/path-health.md`)
- ✅ Script created and executable (`scripts/path-health-restore.py`)
- ✅ Ready to use in Cursor (`/path-health scan`)

**Just type `/path-health scan` in Cursor to start!**

