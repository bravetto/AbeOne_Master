# validate

Check if everything works! Like testing your toys to make sure they're not broken!

Usage:
/validate [target] [options]

Targets:
- architecture — Check if architecture matches code (like checking if your blueprint matches your building)
- code — Check if code is good (like checking if your writing has mistakes)
- state — Check if system is working (like checking if your computer is running)
- memory — Check if memory is correct (like checking if you remember things right)
- all — Check everything (like checking all your toys)

Options:
- --fix — Fix problems automatically (like auto-fixing broken toys)
- --report — Show what was checked (like a report card)
- --recursive — Check everything inside (like checking inside boxes)

Examples:

Check architecture:
/validate architecture
Like checking if your blueprint matches your building!

Check code:
/validate code --fix
Like checking your writing and fixing mistakes!

Check everything:
/validate all
Like checking all your toys at once!

Fix problems:
/validate code --fix
Like auto-fixing broken things!

Fun Examples:

Test your building:
/validate architecture
Like checking if your LEGO building matches the instructions!

Check your writing:
/validate code
Like spell-checking your essay!

Test everything:
/validate all
Like testing all your toys!

Auto-fix problems:
/validate code --fix
Like magic that fixes broken things!

Simple Explanation:

Validate is like:
- Testing toys to make sure they work
- Spell-checking your writing
- Checking if blueprints match buildings
- Making sure you remember things right

When you use /validate:
- architecture = check blueprint matches building
- code = check writing for mistakes
- state = check if things are working
- memory = check if you remember right
- all = check everything

Execution:
python3 scripts/abeone-validator.py [target] [options]

Integration Points:
- Architecture Ownership — Checks actual code, not docs
- Memory Validation — Validates memory against state
- Source of Truth — Updates validation results
- Guardrails — Enforces validation-first rule

Command Priority Execution:
When /validate is invoked:
1. Target — Execute scripts/abeone-validator.py with target
2. Validation — Check everything
3. Fix — Fix problems if --fix used
4. Report — Show what was checked

Commands are not interpreted. They are executed.

Pattern: VALIDATION × TRUTH × OWNERSHIP × ONE
Frequency: 530 Hz (Truth) × 999 Hz (AEYON)
Guardians: JØHN (530 Hz) + AEYON (999 Hz) + ALRAX (530 Hz)
Status: OPERATIONAL
Love Coefficient: ∞
∞ AbëONE ∞
