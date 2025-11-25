# Quick Activation Reference Card

## One Command to Activate Everything

```bash
python3 scripts/activate_all_abe_systems.py
```

---

## Individual Activations

```bash
# YAGNI Guardian (validates requirements)
python3 scripts/activate_yagni_guardian.py

# AbëVOiCEs (perfect communication sync)
python3 scripts/activate_abevoices_sync.py

# AbëViSiONs + AbëDESiGNs (vision + design)
python3 scripts/activate_abevisions_abedesigns.py
```

---

## In Cursor IDE

### Method 1: Terminal (Easiest)
1. Press `` Ctrl + ` `` or `Cmd + J` to open terminal
2. Run: `python3 scripts/activate_all_abe_systems.py`

### Method 2: Command Palette
1. Press `Cmd + Shift + P` (Mac) or `Ctrl + Shift + P` (Windows)
2. Type: `Terminal: Run Command`
3. Enter: `python3 scripts/activate_all_abe_systems.py`

---

## Check Activation Status

```bash
# View activation state
cat .abeone_memory/ALL_ABE_SYSTEMS_ACTIVATION.json | python3 -m json.tool
```

---

## What Gets Activated

**YAGNI Guardian:**
- Radical simplification
- Requirement validation
- Necessity checking

**AbëVOiCEs:**
- 8 communication channels
- Perfect input/output sync
- Pattern alignment (8 patterns)
- Kernel sync (10 modules)

**AbëViSiONs:**
- 5 vision components
- Real-time tracking
- Consciousness monitoring

**AbëDESiGNs:**
- 18 design components
- 4 design tokens
- 4 utilities

---

## Quick Aliases (Add to ~/.zshrc)

```bash
alias abe-activate="cd /Users/michaelmataluni/Documents/AbeOne_Master && python3 scripts/activate_all_abe_systems.py"
alias abe-yagni="cd /Users/michaelmataluni/Documents/AbeOne_Master && python3 scripts/activate_yagni_guardian.py"
alias abe-voices="cd /Users/michaelmataluni/Documents/AbeOne_Master && python3 scripts/activate_abevoices_sync.py"
alias abe-visions="cd /Users/michaelmataluni/Documents/AbeOne_Master && python3 scripts/activate_abevisions_abedesigns.py"
```

Then use: `abe-activate` anywhere!

---

**Full Guide:** See `HOW_TO_ACTIVATE_AND_USE.md`


