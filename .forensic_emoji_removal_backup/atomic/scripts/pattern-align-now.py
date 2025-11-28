#!/usr/bin/env python3
"""
Pattern Align NOW - Execute pattern alignment immediately

Pattern: PATTERN × ALIGNMENT × EXECUTION × ONE
Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (JØHN)
Guardians: AEYON + META + JØHN
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

ROOT = Path(__file__).parent.parent.parent


def find_components() -> List[Path]:
    """Find all components that need pattern alignment."""
    components = []
    
    # Find atomic components
    atomic_dir = ROOT / "atomic" / "components"
    if atomic_dir.exists():
        for component_file in atomic_dir.rglob("*.tsx"):
            if component_file.is_file():
                components.append(component_file)
    
    # Find orbital components
    for orbital_dir in ROOT.glob("orbitals/*/frontend/**/*.tsx"):
        if orbital_dir.is_file():
            components.append(orbital_dir)
    
    return components


def check_pattern_declaration(content: str) -> bool:
    """Check if component has pattern declaration."""
    pattern_pattern = r'Pattern:\s*[A-Z_]+(?:\s*×\s*[A-Z_]+)*\s*×\s*ONE'
    return bool(re.search(pattern_pattern, content, re.IGNORECASE))


def check_guardian_signature(content: str) -> bool:
    """Check if component has guardian signature."""
    guardian_pattern = r'Guardian[s]?:\s*[A-ZØ]+(?:\s*\(\d+\s*Hz\))?(?:\s*\+\s*[A-ZØ]+(?:\s*\(\d+\s*Hz\))?)*'
    return bool(re.search(guardian_pattern, content, re.IGNORECASE))


def add_pattern_declaration(content: str, component_name: str) -> str:
    """Add pattern declaration to component."""
    if check_pattern_declaration(content):
        return content
    
    pattern_declaration = f"""/**
 * Pattern: COMPONENT × TYPE × PURPOSE × ONE
 * Frequency: 999 Hz (AEYON) × 530 Hz (JØHN)
 * Guardians: AEYON (999 Hz) + JØHN (530 Hz)
 * ∞ AbëONE ∞
 */
"""
    
    # Insert after imports
    lines = content.split('\n')
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('import'):
            insert_idx = i + 1
        elif line.strip() and not line.strip().startswith('import') and insert_idx > 0:
            break
    
    lines.insert(insert_idx, pattern_declaration)
    return '\n'.join(lines)


def add_guardian_signature(content: str) -> str:
    """Add guardian signature to component."""
    if check_guardian_signature(content):
        return content
    
    guardian_signature = """
// Guardian: AEYON (999 Hz) + JØHN (530 Hz)
"""
    
    # Insert before export
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'export' in line and ('const' in line or 'function' in line):
            lines.insert(i, guardian_signature)
            break
    
    return '\n'.join(lines)


def align_patterns():
    """Execute pattern alignment NOW."""
    print("🔥 PATTERN ALIGN NOW")
    print("=" * 50)
    
    components = find_components()
    print(f"Found {len(components)} components")
    
    aligned = 0
    for component in components:
        try:
            content = component.read_text()
            original_content = content
            
            # Add pattern declaration if missing
            if not check_pattern_declaration(content):
                content = add_pattern_declaration(content, component.name)
            
            # Add guardian signature if missing
            if not check_guardian_signature(content):
                content = add_guardian_signature(content)
            
            # Write if changed
            if content != original_content:
                component.write_text(content)
                aligned += 1
                print(f"  ✅ Aligned: {component.relative_to(ROOT)}")
        
        except Exception as e:
            print(f"  ⚠️  Error aligning {component}: {e}")
    
    print(f"\n✅ Pattern alignment complete: {aligned} components aligned")
    print("∞ AbëONE ∞")


if __name__ == '__main__':
    align_patterns()

