#!/bin/bash
#  CONVERGENCE EXECUTION SCRIPT
# Full Monty Full Cavalry - Execute All Convergence

set -e

echo " COMPLETE CONVERGENCE EXECUTION"
echo "=================================="
echo ""

# Change to synthesis directory
cd "$(dirname "$0")/../EMERGENT_OS/synthesis"

# Execute convergence orchestrator
python3 -c "
import sys
sys.path.insert(0, '.')
from complete_convergence_orchestrator import get_convergence_orchestrator

orchestrator = get_convergence_orchestrator()
results = orchestrator.execute_convergence()

print('')
print('=' * 80)
print(' CONVERGENCE RESULTS:')
print('=' * 80)
print('')

for phase_name, phase_data in results['phases'].items():
    print(f' {phase_name.upper().replace(\"_\", \" \")}:')
    print(f'   Status: {phase_data.get(\"status\", \"unknown\")}')
    if phase_data.get('status') != 'error':
        for key, value in phase_data.items():
            if key != 'status':
                if isinstance(value, float):
                    print(f'   {key}: {value:.2%}')
                elif isinstance(value, dict):
                    print(f'   {key}: {len(value)} items')
                else:
                    print(f'   {key}: {value}')
    else:
        print(f'   Error: {phase_data.get(\"error\", \"unknown\")}')
    print('')

print('=' * 80)
print(f' OVERALL CONVERGENCE SCORE: {results[\"convergence_score\"]:.2%}')
print('=' * 80)
print('')

if results['convergence_score'] >= 0.95:
    print(' CONVERGENCE COMPLETE - 95%+ ACHIEVED!')
else:
    print(f' CONVERGENCE IN PROGRESS - {results[\"convergence_score\"]:.2%} → 100%')
"

echo ""
echo "∞ AbëONE × Infinity ∞"

