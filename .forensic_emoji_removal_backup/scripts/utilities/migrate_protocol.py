#!/usr/bin/env python3
"""
Protocol Unification Migration Script

Migrates all files from old protocol system (EMERGENT_OS/uptc/protocol)
to new protocol system (protocol/).

This script:
1. Updates imports from old protocol to new protocol
2. Replaces UPTCMessage with ProtocolMessage
3. Replaces UPTCContract with ProtocolContracts
4. Updates ProtocolValidationError imports
5. Reports all changes made
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Migration mappings
IMPORT_MAPPINGS = [
    (
        r'from\s+\.\.protocol\.schema\s+import\s+UPTCMessage',
        'from protocol.schema import ProtocolMessage'
    ),
    (
        r'from\s+\.\.protocol\.contracts\s+import\s+UPTCContract',
        'from protocol.contracts import ProtocolContracts'
    ),
    (
        r'from\s+\.\.protocol\.contracts\s+import\s+UPTCContract,\s*ProtocolValidationError',
        'from protocol.contracts import ProtocolContracts, ContractViolationError'
    ),
    (
        r'from\s+\.\.protocol\.contracts\s+import\s+ProtocolValidationError',
        'from protocol.contracts import ContractViolationError'
    ),
    (
        r'from\s+uptc\.protocol\.schema\s+import\s+UPTCMessage',
        'from protocol.schema import ProtocolMessage'
    ),
    (
        r'from\s+EMERGENT_OS\.uptc\.protocol\.schema\s+import\s+UPTCMessage',
        'from protocol.schema import ProtocolMessage'
    ),
]

CLASS_MAPPINGS = [
    ('UPTCMessage', 'ProtocolMessage'),
    ('UPTCContract', 'ProtocolContracts'),
]

EXCEPTION_MAPPINGS = [
    ('ProtocolValidationError', 'ContractViolationError'),
]

def migrate_file(filepath: Path) -> Tuple[bool, List[str]]:
    """
    Migrate a single file.
    
    Returns:
        (changed, changes_made)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # Apply import mappings
        for pattern, replacement in IMPORT_MAPPINGS:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes.append(f"Updated import: {pattern} → {replacement}")
        
        # Apply class name mappings
        for old_name, new_name in CLASS_MAPPINGS:
            if old_name in content:
                # Only replace if it's a class reference, not part of a string
                # Simple approach: replace whole word
                content = re.sub(r'\b' + old_name + r'\b', new_name, content)
                if content != original_content:
                    changes.append(f"Replaced class: {old_name} → {new_name}")
        
        # Apply exception mappings
        for old_name, new_name in EXCEPTION_MAPPINGS:
            if old_name in content:
                content = re.sub(r'\b' + old_name + r'\b', new_name, content)
                if content != original_content:
                    changes.append(f"Replaced exception: {old_name} → {new_name}")
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes
        
        return False, []
    
    except Exception as e:
        return False, [f"ERROR: {e}"]


def find_python_files(directory: Path) -> List[Path]:
    """Find all Python files in directory."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip __pycache__ and .git directories
        dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', 'node_modules')]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    
    return python_files


def main():
    """Execute migration."""
    print("🚀 PROTOCOL UNIFICATION MIGRATION")
    print("=" * 60)
    
    # Find all Python files in EMERGENT_OS/uptc
    base_dir = Path('EMERGENT_OS/uptc')
    if not base_dir.exists():
        print(f"❌ Directory not found: {base_dir}")
        return
    
    python_files = find_python_files(base_dir)
    print(f"\n📁 Found {len(python_files)} Python files to migrate")
    
    migrated_count = 0
    error_count = 0
    total_changes = []
    
    for filepath in python_files:
        changed, changes = migrate_file(filepath)
        if changed:
            migrated_count += 1
            total_changes.extend([f"{filepath}: {c}" for c in changes])
            print(f"✅ Migrated: {filepath}")
        elif changes and "ERROR" in str(changes):
            error_count += 1
            print(f"❌ Error in {filepath}: {changes}")
    
    print("\n" + "=" * 60)
    print(f"📊 Migration Summary:")
    print(f"   ✅ Files migrated: {migrated_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📝 Total changes: {len(total_changes)}")
    
    if total_changes:
        print("\n📋 Changes made:")
        for change in total_changes[:20]:  # Show first 20
            print(f"   • {change}")
        if len(total_changes) > 20:
            print(f"   ... and {len(total_changes) - 20} more")
    
    print("\n✅ Migration complete!")
    print("\n⚠️  Next steps:")
    print("   1. Run tests to verify migration")
    print("   2. Delete EMERGENT_OS/uptc/protocol/ directory")
    print("   3. Delete protocol/router_adapter.py")
    print("   4. Update any remaining references")


if __name__ == '__main__':
    main()

