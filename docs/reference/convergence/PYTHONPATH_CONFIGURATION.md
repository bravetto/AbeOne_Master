#  PYTHONPATH CONFIGURATION

**Generated:** 2025-01-27  
**Command:** `/path-health pythonpath`  
**Pattern:** PATH × PYTHONPATH × CONVERGENCE × ONE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

##  PYTHONPATH EXPORT COMMAND

```bash
export PYTHONPATH="/Users/michaelmataluni/Documents/AbeOne_Master/orbitals:/Users/michaelmataluni/Documents/AbeOne_Master/orbitals/EMERGENT_OS-orbital:/Users/michaelmataluni/Documents/AbeOne_Master:$PYTHONPATH"
```

---

##  INSTALLATION INSTRUCTIONS

### Option 1: Add to Shell Profile (Permanent)

**For zsh (macOS default):**
```bash
echo 'export PYTHONPATH="/Users/michaelmataluni/Documents/AbeOne_Master/orbitals:/Users/michaelmataluni/Documents/AbeOne_Master/orbitals/EMERGENT_OS-orbital:/Users/michaelmataluni/Documents/AbeOne_Master:$PYTHONPATH"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo 'export PYTHONPATH="/Users/michaelmataluni/Documents/AbeOne_Master/orbitals:/Users/michaelmataluni/Documents/AbeOne_Master/orbitals/EMERGENT_OS-orbital:/Users/michaelmataluni/Documents/AbeOne_Master:$PYTHONPATH"' >> ~/.bashrc
source ~/.bashrc
```

### Option 2: Temporary (Current Session Only)

```bash
export PYTHONPATH="/Users/michaelmataluni/Documents/AbeOne_Master/orbitals:/Users/michaelmataluni/Documents/AbeOne_Master/orbitals/EMERGENT_OS-orbital:/Users/michaelmataluni/Documents/AbeOne_Master:$PYTHONPATH"
```

---

##  PYTHONPATH BREAKDOWN

The PYTHONPATH includes three directories:

1. **`/Users/michaelmataluni/Documents/AbeOne_Master/orbitals`**
   - Contains all orbital modules
   - Enables `from orbitals.EMERGENT_OS_orbital import ...`

2. **`/Users/michaelmataluni/Documents/AbeOne_Master/orbitals/EMERGENT_OS-orbital`**
   - Direct access to EMERGENT_OS-orbital
   - Enables `from synthesis import ...`

3. **`/Users/michaelmataluni/Documents/AbeOne_Master`**
   - Workspace root
   - Enables workspace-level imports

---

##  VERIFICATION

### Test PYTHONPATH:

```bash
# Check current PYTHONPATH
echo $PYTHONPATH

# Test Python import
python3 -c "import sys; print('\\n'.join(sys.path))"
```

### Expected Output:

Should include:
- `/Users/michaelmataluni/Documents/AbeOne_Master/orbitals`
- `/Users/michaelmataluni/Documents/AbeOne_Master/orbitals/EMERGENT_OS-orbital`
- `/Users/michaelmataluni/Documents/AbeOne_Master`

---

##  USAGE EXAMPLES

### After Setting PYTHONPATH:

```python
# Direct import from orbital
from synthesis.agent_swarm_architecture import AgentSwarmArchitecture

# Import from orbital module
from orbitals.EMERGENT_OS_orbital.synthesis import something

# Workspace-level imports
from scripts.some_module import something
```

---

##  ALTERNATIVE: Use sys.path in Scripts

If you prefer not to set PYTHONPATH globally, add this to your Python scripts:

```python
import sys
from pathlib import Path

workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root / "orbitals" / "EMERGENT_OS-orbital"))
sys.path.insert(0, str(workspace_root / "orbitals"))
sys.path.insert(0, str(workspace_root))
```

---

##  STATUS

**PYTHONPATH Configuration:**  **READY**  
**Installation:** Add to shell profile for permanent use  
**Verification:** Test with `python3 -c "import sys; print(sys.path)"`

---

**Pattern:** PATH × PYTHONPATH × CONVERGENCE × ONE  
**Status:**  **CONFIGURATION READY**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

*PYTHONPATH configuration ready. Add to shell profile for permanent use.*


