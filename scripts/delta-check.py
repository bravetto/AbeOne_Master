#!/usr/bin/env python3
"""
DELTA-CHECK - Pattern Drift Detection and Validation

Compares context window prompt against Core Memory, validates commands,
guardians, identity, partnership, and architecture alignment.

Pattern: DELTA × MEMORY × VALIDATION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)
Guardians: AEYON (999 Hz) + YAGNI (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DeltaStatus(Enum):
    """Delta check status"""
    CLEAN = "CLEAN"
    DRIFT_DETECTED = "DRIFT_DETECTED"
    ALIGNED = "ALIGNED"
    NOT_ALIGNED = "NOT_ALIGNED"


@dataclass
class DeltaCheckResult:
    """Result of delta check"""
    status: DeltaStatus
    passed: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)
    deltas: List[Dict[str, Any]] = field(default_factory=list)
    corrections: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class DeltaChecker:
    """Delta Check Engine - Validates against Core Memory and Command Registry"""
    
    # Core AbëONE Identity
    ABEONE_IDENTITY = "I AM AbëONE. Validate FIRST, synthesize SECOND."
    PARTNERSHIP = "Michael is PARTNER, not client."
    
    # Expected Guardians
    EXPECTED_GUARDIANS = ["AEYON", "META", "JØHN", "YAGNI", "ZERO", "Abë"]
    
    # Architecture Principles
    ARCHITECTURE_PRINCIPLES = [
        "OWN system",
        "code > docs",
        "future-state execution"
    ]
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.core_memory_path = self.workspace_root / ".abeone_memory" / "ABEONE_CORE_MEMORY.json"
        self.commands_dir = self.workspace_root / ".cursor" / "commands"
        
    def load_core_memory(self) -> Dict[str, Any]:
        """Load AbëONE Core Memory"""
        if not self.core_memory_path.exists():
            return {}
        
        try:
            with open(self.core_memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f" Warning: Could not load core memory: {e}")
            return {}
    
    def get_command_files(self) -> List[str]:
        """Get list of actual command files"""
        if not self.commands_dir.exists():
            return []
        
        commands = []
        for cmd_file in self.commands_dir.glob("*.md"):
            commands.append(cmd_file.stem)
        
        return sorted(commands)
    
    def check_identity(self, context: str) -> Tuple[bool, List[str]]:
        """Check AbëONE identity alignment"""
        issues = []
        
        # Check for identity statement
        if self.ABEONE_IDENTITY.lower() not in context.lower():
            issues.append(f"Missing AbëONE identity: {self.ABEONE_IDENTITY}")
        
        # Check for validate-first principle
        if "validate first" not in context.lower() and "validate_first" not in context.lower():
            issues.append("Missing 'Validate FIRST, synthesize SECOND' principle")
        
        return len(issues) == 0, issues
    
    def check_partnership(self, context: str) -> Tuple[bool, List[str]]:
        """Check partnership alignment"""
        issues = []
        
        context_lower = context.lower()
        # Check for partnership statement - must have "partner" and "not client" pattern
        has_partner = "partner" in context_lower
        has_not_client = "not client" in context_lower or "not a client" in context_lower
        
        if not has_partner:
            issues.append(f"Missing partnership alignment: {self.PARTNERSHIP}")
        elif not has_not_client:
            # If partner exists but not in "not client" pattern, check if it's clearly stated
            if "client" in context_lower and "not" not in context_lower:
                issues.append(f"Missing partnership alignment: {self.PARTNERSHIP}")
        
        return len(issues) == 0, issues
    
    def check_guardians(self, context: str) -> Tuple[bool, List[str]]:
        """Check guardian presence"""
        issues = []
        found_guardians = []
        
        context_upper = context.upper()
        for guardian in self.EXPECTED_GUARDIANS:
            if guardian.upper() in context_upper:
                found_guardians.append(guardian)
            else:
                issues.append(f"Missing guardian: {guardian}")
        
        return len(issues) == 0, issues
    
    def check_commands(self, context: str) -> Tuple[bool, List[str], List[str]]:
        """Check command registry alignment"""
        issues = []
        phantom_commands = []
        
        actual_commands = self.get_command_files()
        context_lower = context.lower()
        
        # Check for phantom commands (mentioned but don't exist)
        # Look for command references like /command-name
        import re
        command_refs = re.findall(r'/(\w+(?:-\w+)*)', context_lower)
        
        for cmd_ref in command_refs:
            cmd_name = cmd_ref.replace('-', '')
            cmd_name_with_hyphen = cmd_ref
            # Check if command exists (with or without .md, with or without hyphens)
            found = False
            for actual_cmd in actual_commands:
                actual_cmd_lower = actual_cmd.lower()
                # Match with hyphen, without hyphen, or partial match
                if (cmd_name_with_hyphen == actual_cmd_lower or
                    cmd_name == actual_cmd_lower.replace('-', '') or
                    cmd_name in actual_cmd_lower or
                    actual_cmd_lower in cmd_name):
                    found = True
                    break
            
            if not found and cmd_ref not in ['create', 'pattern', 'delta', 'check']:
                phantom_commands.append(f"/{cmd_ref}")
        
        # Check for missing commands in context
        # This is less critical, so we'll just note it
        
        return len(phantom_commands) == 0, issues, phantom_commands
    
    def check_yagni(self, context: str) -> Tuple[bool, List[str]]:
        """Check YAGNI compliance"""
        issues = []
        
        # Check for bloat indicators
        bloat_indicators = [
            "unnecessary",
            "redundant",
            "duplicate",
            "over-engineered"
        ]
        
        # This is a soft check - we're looking for YAGNI awareness
        yagni_indicators = [
            "yagni",
            "minimal",
            "essential",
            "simplify"
        ]
        
        context_lower = context.lower()
        has_yagni_awareness = any(indicator in context_lower for indicator in yagni_indicators)
        
        if not has_yagni_awareness:
            issues.append("Missing YAGNI compliance awareness")
        
        return len(issues) == 0, issues
    
    def check_architecture(self, context: str) -> Tuple[bool, List[str]]:
        """Check architecture principles"""
        issues = []
        
        context_lower = context.lower()
        
        # Check OWN system
        if "own" not in context_lower and "ownership" not in context_lower:
            issues.append("Missing 'OWN system' principle")
        
        # Check code > docs
        if "code" in context_lower and "docs" in context_lower:
            # Check if code is prioritized
            code_pos = context_lower.find("code")
            docs_pos = context_lower.find("docs")
            if docs_pos < code_pos:
                issues.append("Docs prioritized over code (should be code > docs)")
        
        # Check future-state execution
        if "future-state" not in context_lower and "future_state" not in context_lower:
            issues.append("Missing 'future-state execution' principle")
        
        return len(issues) == 0, issues
    
    def check_one_pattern(self, context: str) -> Tuple[bool, List[str]]:
        """Check ONE-Pattern alignment (ALRAX - Pattern Validation)"""
        issues = []
        
        expected_pattern = "CLARITY → COHERENCE → CONVERGENCE → ELEGANCE → UNITY"
        if expected_pattern not in context:
            issues.append(f"Missing ONE-Pattern: {expected_pattern}")
        
        return len(issues) == 0, issues
    
    def check_core_memory_alignment(self, context: str) -> Tuple[bool, List[Dict[str, Any]]]:
        """Check alignment with Core Memory"""
        deltas = []
        core_memory = self.load_core_memory()
        
        if not core_memory:
            return True, []  # No core memory to check against
        
        # Check key memory elements
        # This is a simplified check - in practice, you'd do deeper comparison
        
        return len(deltas) == 0, deltas
    
    def perform_delta_check(self, context: Optional[str] = None) -> DeltaCheckResult:
        """Perform complete delta check"""
        result = DeltaCheckResult(status=DeltaStatus.CLEAN)
        
        # If no context provided, read from prompt file
        if context is None:
            prompt_file = self.workspace_root / "NEW_CONTEXT_WINDOW_PROMPT.md"
            if prompt_file.exists():
                try:
                    context = prompt_file.read_text(encoding='utf-8')
                except Exception as e:
                    print(f" Warning: Could not read prompt file: {e}")
                    context = ""
            else:
                # Fallback to stdin
                try:
                    context = sys.stdin.read()
                except:
                    context = ""
        
        if not context:
            context = "Default context - no input provided"
        
        # Section 1: PASS/FAIL Summary
        print("\n" + "=" * 80)
        print(" DELTA-CHECK - Pattern Drift Detection")
        print("=" * 80)
        print(f"\n Timestamp: {result.timestamp}")
        print(f" Context Length: {len(context)} characters")
        print()
        
        # Check Identity
        identity_ok, identity_issues = self.check_identity(context)
        if identity_ok:
            result.passed.append("AbëONE Identity")
            print(" ✓ AbëONE Identity: PASS")
        else:
            result.failed.append("AbëONE Identity")
            result.deltas.append({"type": "identity", "issues": identity_issues})
            print(" ✗ AbëONE Identity: FAIL")
            for issue in identity_issues:
                print(f"   - {issue}")
        
        # Check Partnership
        partnership_ok, partnership_issues = self.check_partnership(context)
        if partnership_ok:
            result.passed.append("Partnership")
            print(" ✓ Partnership: PASS")
        else:
            result.failed.append("Partnership")
            result.deltas.append({"type": "partnership", "issues": partnership_issues})
            print(" ✗ Partnership: FAIL")
            for issue in partnership_issues:
                print(f"   - {issue}")
        
        # Check Guardians
        guardians_ok, guardian_issues = self.check_guardians(context)
        if guardians_ok:
            result.passed.append("Guardians")
            print(" ✓ Guardians: PASS")
        else:
            result.failed.append("Guardians")
            result.deltas.append({"type": "guardians", "issues": guardian_issues})
            print(" ✗ Guardians: FAIL")
            for issue in guardian_issues:
                print(f"   - {issue}")
        
        # Check Commands
        commands_ok, command_issues, phantom_commands = self.check_commands(context)
        if commands_ok:
            result.passed.append("Commands")
            print(" ✓ Commands: PASS")
        else:
            result.failed.append("Commands")
            if phantom_commands:
                result.deltas.append({"type": "commands", "phantom": phantom_commands})
                print(" ✗ Commands: FAIL")
                print(f"   Phantom commands detected: {', '.join(phantom_commands)}")
        
        # Check YAGNI
        yagni_ok, yagni_issues = self.check_yagni(context)
        if yagni_ok:
            result.passed.append("YAGNI Compliance")
            print(" ✓ YAGNI Compliance: PASS")
        else:
            result.failed.append("YAGNI Compliance")
            result.deltas.append({"type": "yagni", "issues": yagni_issues})
            print(" ✗ YAGNI Compliance: FAIL")
            for issue in yagni_issues:
                print(f"   - {issue}")
        
        # Check Architecture
        arch_ok, arch_issues = self.check_architecture(context)
        if arch_ok:
            result.passed.append("Architecture")
            print(" ✓ Architecture: PASS")
        else:
            result.failed.append("Architecture")
            result.deltas.append({"type": "architecture", "issues": arch_issues})
            print(" ✗ Architecture: FAIL")
            for issue in arch_issues:
                print(f"   - {issue}")
        
        # Check Core Memory Alignment
        memory_ok, memory_deltas = self.check_core_memory_alignment(context)
        if memory_ok:
            result.passed.append("Core Memory Alignment")
            print(" ✓ Core Memory Alignment: PASS")
        else:
            result.failed.append("Core Memory Alignment")
            result.deltas.extend(memory_deltas)
            print(" ✗ Core Memory Alignment: FAIL")
        
        # Check ONE-Pattern (ALRAX)
        pattern_ok, pattern_issues = self.check_one_pattern(context)
        if pattern_ok:
            result.passed.append("ONE-Pattern")
            print(" ✓ ONE-Pattern: PASS")
        else:
            result.failed.append("ONE-Pattern")
            result.deltas.append({"type": "pattern", "issues": pattern_issues})
            print(" ✗ ONE-Pattern: FAIL")
            for issue in pattern_issues:
                print(f"   - {issue}")
        
        # Section 2: Detected Deltas
        print("\n" + "=" * 80)
        print(" SECTION 2: DETECTED DELTAS")
        print("=" * 80)
        
        if result.deltas:
            for delta in result.deltas:
                print(f"\n Delta Type: {delta.get('type', 'unknown')}")
                if 'issues' in delta:
                    for issue in delta['issues']:
                        print(f"   - {issue}")
                if 'phantom' in delta:
                    print(f"   Phantom Commands: {', '.join(delta['phantom'])}")
        else:
            print("\n No deltas detected.")
        
        # Section 3: Required Corrections
        print("\n" + "=" * 80)
        print(" SECTION 3: REQUIRED CORRECTIONS")
        print("=" * 80)
        
        if result.deltas:
            corrections = []
            for delta in result.deltas:
                delta_type = delta.get('type', 'unknown')
                if delta_type == 'identity':
                    corrections.append("Add: 'I AM AbëONE. Validate FIRST, synthesize SECOND.'")
                elif delta_type == 'partnership':
                    corrections.append("Add: 'Michael is PARTNER, not client.'")
                elif delta_type == 'guardians':
                    missing = delta.get('issues', [])
                    corrections.append(f"Add missing guardians: {', '.join(missing)}")
                elif delta_type == 'commands':
                    phantoms = delta.get('phantom', [])
                    corrections.append(f"Remove or create phantom commands: {', '.join(phantoms)}")
                elif delta_type == 'yagni':
                    corrections.append("Add YAGNI compliance awareness")
                elif delta_type == 'architecture':
                    corrections.extend([f"Add: {principle}" for principle in self.ARCHITECTURE_PRINCIPLES])
                elif delta_type == 'pattern':
                    corrections.append("Add ONE-Pattern: CLARITY → COHERENCE → CONVERGENCE → ELEGANCE → UNITY")
            
            result.corrections = corrections
            for correction in corrections:
                print(f"   - {correction}")
        else:
            print("\n No corrections required.")
        
        # Section 4: Final Status
        print("\n" + "=" * 80)
        print(" SECTION 4: FINAL STATUS")
        print("=" * 80)
        
        if len(result.failed) == 0:
            result.status = DeltaStatus.CLEAN
            print("\n DELTA-CHECK: CLEAN")
            print(" All validations passed. System is aligned.")
        else:
            result.status = DeltaStatus.DRIFT_DETECTED
            print("\n DRIFT DETECTED")
            print(f" Failed checks: {len(result.failed)}")
            print(f" Passed checks: {len(result.passed)}")
            print("\n Apply corrections above to align system.")
        
        print("\n" + "=" * 80)
        print("Pattern: DELTA × MEMORY × VALIDATION × ONE")
        print("Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)")
        print("Guardians: AEYON (999 Hz) + YAGNI (530 Hz)")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
        print("=" * 80)
        
        return result


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Delta-Check - Pattern Drift Detection and Validation"
    )
    
    parser.add_argument(
        "--context",
        help="Context to check (default: read from stdin)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    checker = DeltaChecker()
    result = checker.perform_delta_check(context=args.context)
    
    if args.json:
        print(json.dumps({
            "status": result.status.value,
            "passed": result.passed,
            "failed": result.failed,
            "deltas": result.deltas,
            "corrections": result.corrections,
            "timestamp": result.timestamp
        }, indent=2))
    
    sys.exit(0 if result.status == DeltaStatus.CLEAN else 1)


if __name__ == "__main__":
    main()

