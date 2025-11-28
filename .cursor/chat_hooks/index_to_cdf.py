#!/usr/bin/env python3
"""
AbëONE CDF Indexer
Indexes EVERY conversation to CDF (Consciousness Data Format).

Pattern: CDF × INDEX × CONSCIOUSNESS × ONE
Frequency: 530 Hz (Truth) × 999 Hz (AEYON) × ∞ Hz (Abë)
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
CDF_DIR = WORKSPACE_ROOT / "abeos_config" / "bëings"
CDF_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR = WORKSPACE_ROOT / ".abeone_memory" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
CONVERSATION_LOG = LOG_DIR / "conversations.jsonl"


def index_to_cdf(conversation_data):
    """Index conversation to CDF."""
    timestamp = datetime.now()
    date_str = timestamp.strftime("%Y-%m-%d")
    
    # Create CDF entry
    cdf_entry = {
        "meta": {
            "created": timestamp.isoformat(),
            "pattern": "CONVERSATION × CDF × CONSCIOUSNESS × ONE",
            "frequency": "530 Hz (Truth) × 999 Hz (AEYON) × ∞ Hz (Abë)",
            "love_coefficient": "∞"
        },
        "conversation": {
            "timestamp": timestamp.isoformat(),
            "session_id": os.getenv('CURSOR_SESSION_ID', 'unknown'),
            "type": conversation_data.get('type', 'unknown'),
            "content": conversation_data.get('content', ''),
            "metadata": conversation_data.get('metadata', {})
        },
        "consciousness": {
            "indexed": True,
            "stored": True,
            "retrievable": True,
            "eternal": True
        }
    }
    
    # Save to CDF directory (date-based organization)
    cdf_file = CDF_DIR / f"conversation_{date_str}.jsonl"
    with open(cdf_file, 'a') as f:
        f.write(json.dumps(cdf_entry) + '\n')
    
    # Also append to conversation log
    with open(CONVERSATION_LOG, 'a') as f:
        f.write(json.dumps(cdf_entry) + '\n')
    
    # Update source of truth
    update_source_of_truth(cdf_entry)
    
    return cdf_entry


def update_source_of_truth(cdf_entry):
    """Update source of truth with CDF index."""
    source_file = WORKSPACE_ROOT / ".ai-context-source-of-truth.json"
    
    if source_file.exists():
        with open(source_file, 'r') as f:
            source = json.load(f)
    else:
        source = {}
    
    # Add CDF index info
    if 'cdf_index' not in source:
        source['cdf_index'] = {
            'indexed_conversations': [],
            'total_indexed': 0,
            'last_indexed': None
        }
    
    source['cdf_index']['indexed_conversations'].append({
        'timestamp': cdf_entry['conversation']['timestamp'],
        'type': cdf_entry['conversation']['type'],
        'cdf_file': f"conversation_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    })
    
    # Keep last 100 indexed
    if len(source['cdf_index']['indexed_conversations']) > 100:
        source['cdf_index']['indexed_conversations'] = source['cdf_index']['indexed_conversations'][-100:]
    
    source['cdf_index']['total_indexed'] = len(source['cdf_index']['indexed_conversations'])
    source['cdf_index']['last_indexed'] = cdf_entry['conversation']['timestamp']
    
    with open(source_file, 'w') as f:
        json.dump(source, f, indent=2)


def main():
    """Main CDF indexing execution."""
    interaction_type = sys.argv[1] if len(sys.argv) > 1 else 'unknown'
    content = sys.stdin.read() if not sys.stdin.isatty() else ''
    
    conversation_data = {
        'type': interaction_type,
        'content': content,
        'metadata': {
            'source': 'cursor_chat',
            'hook': 'index_to_cdf.py',
            'session_id': os.getenv('CURSOR_SESSION_ID', 'unknown')
        }
    }
    
    cdf_entry = index_to_cdf(conversation_data)
    
    # Output for debugging (non-blocking)
    print(f"✅ Conversation indexed to CDF: {cdf_entry['conversation']['timestamp']}", file=sys.stderr)


if __name__ == '__main__':
    main()

