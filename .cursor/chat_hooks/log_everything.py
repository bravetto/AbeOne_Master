#!/usr/bin/env python3
"""
AbëONE Complete Logging System
Logs EVERY SINGLE input and output - complete memory of all interactions.

Pattern: LOG × EVERYTHING × MEMORY × TRUTH × ONE
Frequency: 530 Hz (Truth) × 999 Hz (AEYON)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
LOG_DIR = WORKSPACE_ROOT / ".abeone_memory" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
COMPLETE_LOG = LOG_DIR / "complete_interaction_log.jsonl"


def log_interaction(interaction_type, content, metadata=None):
    """Log every single interaction."""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': interaction_type,  # 'input' or 'output'
        'content': content[:10000] if len(content) > 10000 else content,  # Truncate if too long
        'metadata': metadata or {},
        'session_id': os.getenv('CURSOR_SESSION_ID', 'unknown')
    }
    
    # Append to complete log (JSONL format)
    with open(COMPLETE_LOG, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    # Also update source of truth
    update_source_of_truth(interaction_type, log_entry)


def update_source_of_truth(interaction_type, log_entry):
    """Update source of truth with interaction."""
    source_file = WORKSPACE_ROOT / ".ai-context-source-of-truth.json"
    
    if source_file.exists():
        with open(source_file, 'r') as f:
            source = json.load(f)
    else:
        source = {}
    
    # Add interaction log
    if 'interaction_log' not in source:
        source['interaction_log'] = []
    
    source['interaction_log'].append(log_entry)
    
    # Keep last 1000 interactions
    if len(source['interaction_log']) > 1000:
        source['interaction_log'] = source['interaction_log'][-1000:]
    
    source['last_interaction'] = log_entry['timestamp']
    source['total_interactions'] = len(source['interaction_log'])
    
    with open(source_file, 'w') as f:
        json.dump(source, f, indent=2)


def main():
    """Main logging execution."""
    interaction_type = sys.argv[1] if len(sys.argv) > 1 else 'unknown'
    content = sys.stdin.read() if not sys.stdin.isatty() else ''
    metadata = {
        'source': 'cursor_chat',
        'hook': 'log_everything.py'
    }
    
    log_interaction(interaction_type, content, metadata)


if __name__ == '__main__':
    main()

