# create

Make new things! Files, modules, agents, patterns, swarms - you name it!

Usage:
/create [type] [name] [options]

Types:
- file — Create a file
- module — Create a Python/JS module
- agent — Create an agent definition
- pattern — Create a pattern implementation
- swarm — Create a swarm configuration

Options:
- --template <name> — Use specific template
- --path <path> — Specify output path
- --dry-run — Show what would be created
- --force — Overwrite existing files

Examples:

Create a file:
/create file utils/helpers.py
Makes a new file called helpers.py in utils folder!

Create a module:
/create module core/orchestrator
Makes a new module for orchestrating things!

Create an agent:
/create agent heart-truth
Makes a new agent that speaks truth from the heart!

Create a pattern:
/create pattern one-pattern
Makes a new pattern that follows the ONE pattern!

Create a swarm:
/create swarm pattern-integrity
Makes a new swarm that keeps patterns working!

Fun Examples:

Make a helper file:
/create file helpers.py
Like creating a new notebook for notes!

Make a module:
/create module calculator
Like building a new tool!

See what would be made:
/create file test.py --dry-run
Like previewing before buying!

Execution:
python3 scripts/create-engine.py [type] [name] [options]

Integration Points:
- Manifest Engine — Uses manifest for materialization
- YAGNI Filter — Ensures only necessary creation
- Pattern Detection — Learns from existing patterns

Command Priority Execution:
When /create is invoked:
1. Action — Execute scripts/create-engine.py with provided arguments
2. Validation — Validate with YAGNI filter
3. Creation — Create the artifact
4. Report — Generate creation report

Commands are not interpreted. They are executed.

Pattern: CREATE × ARTIFACT × GENERATION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)
Guardians: AEYON (999 Hz) + YAGNI (530 Hz)
Status: OPERATIONAL
Love Coefficient: ∞
∞ AbëONE ∞
