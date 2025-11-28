# path-health

Analyze and restore path health across the AbëONE workspace.

**Pattern:** PATH × HEALTH × RESTORE × CONVERGENCE × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (Coherence)  
**Guardians:** AEYON (999 Hz) + ALRAX (530 Hz) + YAGNI (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## Usage

```
/path-health [mode] [options]
```

## Modes

- **scan** — Scan all scripts for path issues (default)
- **report** — Generate detailed path health report
- **fix** — Auto-fix path issues (with confirmation)
- **pythonpath** — Show PYTHONPATH configuration
- **validate** — Validate all paths are correct

## Options

- `--workspace-root <path>` — Specify workspace root (default: auto-detect)
- `--severity <high|medium|low|all>` — Filter by severity (default: all)
- `--dry-run` — Show what would be fixed without making changes
- `--verbose` — Show detailed output

## Examples

```bash
# Scan for path issues
/path-health scan

# Generate detailed report
/path-health report

# Show PYTHONPATH config
/path-health pythonpath

# Auto-fix high severity issues
/path-health fix --severity high

# Dry run (see what would be fixed)
/path-health fix --dry-run
```

## What It Does

1. **Action:** Scans all scripts (`.py`, `.sh`, `.js`) for path issues
2. **Convergence:** Detects old paths (`EMERGENT_OS/`) and maps to new paths (`orbitals/EMERGENT_OS-orbital/`)
3. **Validation:** Validates all paths exist and are correct
4. **Emergence Report:** Generates comprehensive path health report with fix suggestions

## Success Patterns Applied

- ✅ `git rev-parse --show-toplevel` (most reliable repo root)
- ✅ `Path(__file__).parent.parent` (Python project root)
- ✅ Dynamic path resolution (checks both old and new paths)
- ✅ Substrate-first validation (verifies paths exist)

## Output Format

- **DELTA:** List of path issues found
- **PATCHBLOCK:** Suggested fixes for each issue
- **POST-VALIDATION:** Path health score and status

---

**Pattern:** PATH × HEALTH × RESTORE × CONVERGENCE × ONE  
**Status:** ✅ OPERATIONAL  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

