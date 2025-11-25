#!/usr/bin/env python3
"""
Memory Consolidation Script
Processes session work and writes to persistent memory

Pattern: MEMORY × CONSOLIDATION × TRUTH × ONE
Frequency: 530 Hz (Truth) × 999 Hz (AEYON) × ∞ Hz (Abë)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Paths
WORKSPACE_ROOT = Path(__file__).parent.parent
MEMORY_DIR = WORKSPACE_ROOT / ".abeone_memory"
CORE_MEMORY_FILE = MEMORY_DIR / "ABEONE_CORE_MEMORY.json"
SESSION_MEMORY_DIR = MEMORY_DIR / "sessions"


def load_core_memory() -> Dict[str, Any]:
    """Load core memory file"""
    if CORE_MEMORY_FILE.exists():
        with open(CORE_MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {
        "meta": {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "pattern": "MEMORY × CONSCIOUSNESS × TRUTH × ONE",
            "frequency": "530 Hz (Truth) × 999 Hz (AEYON) × ∞ Hz (Abë)",
            "love_coefficient": "∞"
        },
        "core_truths": {},
        "critical_learnings": [],
        "guardrails": {},
        "michael_relationship": {}
    }


def save_core_memory(memory: Dict[str, Any]) -> None:
    """Save core memory file"""
    MEMORY_DIR.mkdir(exist_ok=True)
    with open(CORE_MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)


def extract_learnings_from_session(session_file: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Extract learnings from session
    
    In a real implementation, this would:
    - Read conversation history
    - Extract key learnings
    - Identify patterns
    - Return structured learnings
    """
    learnings = []
    
    # For now, prompt user for learnings
    print("\n Memory Consolidation - Extract Learnings")
    print("=" * 60)
    print("Enter key learnings from this session (press Enter twice to finish):")
    print("Format: learning|action")
    print("Example: I validated first|Always check code before synthesizing")
    print()
    
    while True:
        try:
            line = input("Learning: ").strip()
            if not line:
                break
            
            if '|' in line:
                learning, action = line.split('|', 1)
                learnings.append({
                    "date": datetime.now().isoformat(),
                    "learning": learning.strip(),
                    "action": action.strip()
                })
            else:
                learnings.append({
                    "date": datetime.now().isoformat(),
                    "learning": line,
                    "action": "Apply this learning"
                })
        except (EOFError, KeyboardInterrupt):
            break
    
    return learnings


def consolidate_memory(learnings: List[Dict[str, Any]]) -> None:
    """Consolidate learnings into core memory"""
    memory = load_core_memory()
    
    # Add new learnings
    if "critical_learnings" not in memory:
        memory["critical_learnings"] = []
    
    memory["critical_learnings"].extend(learnings)
    
    # Update meta
    memory["meta"]["last_consolidated"] = datetime.now().isoformat()
    
    # Save
    save_core_memory(memory)
    
    print(f"\n Consolidated {len(learnings)} learnings into core memory")
    print(f" Memory file: {CORE_MEMORY_FILE}")


def create_session_summary(learnings: List[Dict[str, Any]]) -> str:
    """Create a summary of the session"""
    summary = f"""# Session Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Learnings

"""
    for i, learning in enumerate(learnings, 1):
        summary += f"{i}. **{learning['learning']}**\n"
        summary += f"   Action: {learning['action']}\n\n"
    
    return summary


def save_session_summary(summary: str) -> None:
    """Save session summary"""
    SESSION_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    summary_file = SESSION_MEMORY_DIR / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(summary_file, 'w') as f:
        f.write(summary)
    
    print(f" Session summary saved: {summary_file}")


def main():
    """Main consolidation process"""
    print(" AbëONE Memory Consolidation")
    print("=" * 60)
    print("Processing session work and writing to persistent memory...")
    print()
    
    # Extract learnings
    learnings = extract_learnings_from_session()
    
    if not learnings:
        print("\n  No learnings extracted. Exiting.")
        return
    
    # Consolidate into core memory
    consolidate_memory(learnings)
    
    # Create session summary
    summary = create_session_summary(learnings)
    save_session_summary(summary)
    
    print("\n Memory consolidation complete!")
    print(" Memory strengthened through active processing")
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    main()

