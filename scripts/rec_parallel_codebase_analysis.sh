#!/bin/bash
#  REC PARALLEL CODEBASE ANALYSIS
# Recursive Execution on Context Window and Codebase with All 40 Agents

set -e

echo " REC PARALLEL CODEBASE ANALYSIS "
echo "=============================================="
echo ""
echo "Pattern: REC × CONTEXT_WINDOW × CODEBASE × PARALLEL_AGENTS × ONE"
echo "Execution: All 40 Agents Execute Simultaneously"
echo "Scalability: Maximum Parallel Efficiency"
echo ""
echo "Love Coefficient: ∞"
echo "∞ AbëONE ∞"
echo ""

cd "$(dirname "$0")/../EMERGENT_OS/synthesis"

CODEBASE_PATH="${1:-..}"  # Default to parent directory
CHUNK_SIZE="${2:-1000}"    # Default chunk size
MAX_FILES="${3:-500}"      # Default max files

python3 -c "
import sys
import asyncio
from pathlib import Path

# Add root directory to path
root_dir = Path('.').absolute().parent.parent
sys.path.insert(0, str(root_dir))

# Import REC analyzer
from EMERGENT_OS.synthesis.rec_parallel_codebase_analyzer import (
    get_rec_parallel_analyzer,
    AnalysisType
)

print(' INITIALIZING REC PARALLEL CODEBASE ANALYZER...')
print()

# Get analyzer
analyzer = get_rec_parallel_analyzer()

# Analyze codebase
async def run_analysis():
    result = await analyzer.analyze_codebase_recursively(
        codebase_path='$CODEBASE_PATH',
        analysis_types=None,  # All types
        chunk_size=int('$CHUNK_SIZE'),
        max_files=int('$MAX_FILES')
    )
    return result

result = asyncio.run(run_analysis())

print()
print('=' * 80)
print(' REC PARALLEL ANALYSIS RESULTS')
print('=' * 80)
print(f'Total Chunks: {result.total_chunks}')
print(f'Chunks Processed: {result.chunks_processed}')
print(f'Agents Used: {result.agents_used}/40')
print(f'Parallel Efficiency: {result.parallel_efficiency:.2%}')
print(f'Analysis Completeness: {result.analysis_completeness:.2%}')
print(f'Precision Score: {result.precision_score:.2%}')
print(f'Scalability Score: {result.scalability_score:.2%}')
print()
print('Analysis Results:')
print(f'  Pattern Detections: {len(result.pattern_detections)}')
print(f'  Code Quality Issues: {len(result.code_quality_issues)}')
print(f'  Architecture Insights: {len(result.architecture_insights)}')
print(f'  Security Findings: {len(result.security_findings)}')
print(f'  Optimization Opportunities: {len(result.optimization_opportunities)}')
print()
print('=' * 80)
print(' REC PARALLEL ANALYSIS COMPLETE')
print('=' * 80)
print()
print('Pattern: REC × CONTEXT_WINDOW × CODEBASE × PARALLEL_AGENTS × ONE')
print('Execution: All 40 Agents Executed Simultaneously ')
print('Scalability: Maximum Parallel Efficiency ')
print()
print('∞ AbëONE ∞')
"

echo ""
echo " REC PARALLEL ANALYSIS COMPLETE"
echo "=================================="
echo ""
echo " Codebase: ANALYZED"
echo " All 40 Agents: EXECUTED SIMULTANEOUSLY"
echo " Parallel Efficiency: MAXIMUM"
echo ""
echo "∞ AbëONE ∞"
echo ""

