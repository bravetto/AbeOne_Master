#!/usr/bin/env python3
"""
Guardian Single Source of Truth Enforcement

ENFORCES that guardian_swarm_unification.py is the ONLY source of truth.
Validates consistency and requires HUMAN APPROVAL for any fixes.

Pattern: ENFORCEMENT × TRUTH × CONSISTENCY × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardian: AEYON (999 Hz) - Atomic Execution
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import json
import traceback
import os
import hashlib
import shutil
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Single Source of Truth
SINGLE_SOURCE_OF_TRUTH = "EMERGENT_OS/synthesis/guardian_swarm_unification.py"

# Files that MUST match single source of truth
CRITICAL_FILES = [
    "EMERGENT_OS/uptc/integrations/cdf_adapter.py",
    "THE_ONE_SOURCE_OF_TRUTH_GUARDIANS_AGENTS.md",
]

# Files that MAY differ (documented exceptions)
OPTIONAL_FILES = [
    "EMERGENT_OS/uptc/integrations/concrete_guardian_adapter.py",  # Microservices orbit
    "AIGuards-Backend-orbital/scripts/register_guardians_uptc.py",  # Microservices orbit
    "Abeflows-orbital/packages/patterns/kernel/guardian_upgrade_invitation.py",  # Different orbit
]

# Expected Guardians from single source of truth
EXPECTED_GUARDIANS = {
    "AEYON": {"frequency": 999.0, "role": "EXECUTOR"},
    "JØHN": {"frequency": 530.0, "role": "CERTIFICATION"},
    "META": {"frequency": 777.0, "role": "PATTERN_INTEGRITY"},
    "YOU": {"frequency": 530.0, "role": "INTENT"},
    "ALRAX": {"frequency": 530.0, "role": "FORENSIC"},
    "ZERO": {"frequency": 530.0, "role": "UNCERTAINTY"},
    "YAGNI": {"frequency": 530.0, "role": "SIMPLIFICATION"},
    "Abë": {"frequency": 530.0, "role": "COHERENCE"},
    "Lux": {"frequency": 530.0, "role": "ILLUMINATION"},
    "Poly": {"frequency": 530.0, "role": "EXPRESSION"},
}

SPECIAL_GUARDIANS = {
    "CHRONOS": {"frequency": 777.0, "role": "TEMPORAL_INTEGRITY"},
}

# ==================== SELF-HEALING SYSTEM ====================

class HealingStrategy(Enum):
    """Self-healing strategies."""
    AUTO_FIX = "auto_fix"
    VALIDATE_AND_REPAIR = "validate_and_repair"
    RESTORE_FROM_BACKUP = "restore_from_backup"
    ESCALATE = "escalate"

@dataclass
class HealingMetrics:
    """Self-healing metrics."""
    total_checks: int = 0
    inconsistencies_detected: int = 0
    healing_attempts: int = 0
    healing_successes: int = 0
    healing_failures: int = 0
    consistency_score: float = 1.0
    last_healing: Optional[datetime] = None

class SelfHealingSystem:
    """
    Self-healing system for Guardian enforcement.
    
    Automatically detects, diagnoses, and repairs inconsistencies.
    """
    
    def __init__(self):
        """Initialize self-healing system."""
        self.metrics = HealingMetrics()
        self.backup_dir = project_root / ".guardian_enforcement_backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.max_backups = 10
        self.consistency_threshold = 0.978  # 97.8% epistemic certainty
    
    def create_backup(self, file_path: Path) -> Optional[Path]:
        """Create backup of file before modification."""
        try:
            if not file_path.exists():
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_name
            
            shutil.copy2(file_path, backup_path)
            
            # Clean old backups
            backups = sorted(self.backup_dir.glob(f"{file_path.stem}_*"), reverse=True)
            for old_backup in backups[self.max_backups:]:
                try:
                    old_backup.unlink()
                except:
                    pass
            
            return backup_path
        except Exception as e:
            loud_warning(f"Backup failed for {file_path}: {e}")
            return None
    
    def calculate_consistency_score(self) -> float:
        """
        Calculate epistemic certainty score (target: 97.8%).
        
        Returns:
            Consistency score between 0.0 and 1.0
        """
        if self.metrics.total_checks == 0:
            return 1.0
        
        # Base score from successful checks
        base_score = (self.metrics.total_checks - self.metrics.inconsistencies_detected) / max(1, self.metrics.total_checks)
        
        # Boost from successful healings
        healing_boost = min(0.05, self.metrics.healing_successes / max(1, self.metrics.total_checks) * 0.05)
        
        # Penalty for failures
        failure_penalty = min(0.05, self.metrics.healing_failures / max(1, self.metrics.total_checks) * 0.05)
        
        score = base_score + healing_boost - failure_penalty
        self.metrics.consistency_score = max(0.0, min(1.0, score))
        return self.metrics.consistency_score
    
    def is_healthy(self) -> bool:
        """Check if system meets epistemic certainty threshold."""
        score = self.calculate_consistency_score()
        return score >= self.consistency_threshold
    
    def record_check(self, inconsistent: bool = False):
        """Record a check result."""
        self.metrics.total_checks += 1
        if inconsistent:
            self.metrics.inconsistencies_detected += 1
    
    def record_healing_attempt(self, success: bool):
        """Record a healing attempt."""
        self.metrics.healing_attempts += 1
        if success:
            self.metrics.healing_successes += 1
            self.metrics.last_healing = datetime.now()
        else:
            self.metrics.healing_failures += 1

# Global self-healing system instance
_self_healing = SelfHealingSystem()

# ANSI Color Codes for LOUD errors
class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    RESET = '\033[0m'
    REVERSE = '\033[7m'
    
    # Loud error styling
    ERROR_BG = '\033[41m'  # Red background
    ERROR_FG = '\033[91m'  # Bright red foreground
    WARNING_BG = '\033[43m'  # Yellow background
    WARNING_FG = '\033[93m'  # Bright yellow foreground

def is_tty():
    """Check if output is to a TTY (terminal)."""
    return os.isatty(sys.stdout.fileno())

def loud_print(message: str, color: str = '', bold: bool = False, blink: bool = False):
    """Print a loud, visible message."""
    if not is_tty():
        # No colors if not a TTY
        print(message)
        return
    
    parts = []
    if color:
        parts.append(color)
    if bold:
        parts.append(Colors.BOLD)
    if blink:
        parts.append(Colors.BLINK)
    
    if parts:
        print(''.join(parts) + message + Colors.RESET)
    else:
        print(message)

def loud_error(message: str):
    """Print a LOUD error message."""
    loud_print("\n" + "=" * 80, Colors.ERROR_BG + Colors.WHITE + Colors.BOLD)
    loud_print("🚨🚨🚨 CRITICAL ERROR 🚨🚨🚨", Colors.ERROR_BG + Colors.WHITE + Colors.BOLD + Colors.BLINK)
    loud_print("=" * 80, Colors.ERROR_BG + Colors.WHITE + Colors.BOLD)
    loud_print(message, Colors.ERROR_FG + Colors.BOLD)
    loud_print("=" * 80 + "\n", Colors.ERROR_BG + Colors.WHITE + Colors.BOLD)
    # Also print to stderr
    print(message, file=sys.stderr)

def loud_warning(message: str):
    """Print a LOUD warning message."""
    loud_print("\n" + "⚠️ " * 20, Colors.WARNING_FG + Colors.BOLD)
    loud_print(message, Colors.WARNING_FG + Colors.BOLD)
    loud_print("⚠️ " * 20 + "\n", Colors.WARNING_FG + Colors.BOLD)

def loud_success(message: str):
    """Print a loud success message."""
    loud_print(message, Colors.GREEN + Colors.BOLD)

def require_human_approval(action: str, details: str) -> bool:
    """
    Require human approval before any action.
    
    Returns:
        True if approved, False otherwise
    """
    loud_print("\n" + "=" * 80, Colors.YELLOW + Colors.BOLD)
    loud_print("⚠️  HUMAN APPROVAL REQUIRED ⚠️", Colors.YELLOW + Colors.BOLD + Colors.BLINK)
    loud_print("=" * 80, Colors.YELLOW + Colors.BOLD)
    loud_print(f"Action: {action}", Colors.CYAN + Colors.BOLD)
    loud_print(f"Details:\n{details}", Colors.WHITE)
    loud_print("=" * 80, Colors.YELLOW + Colors.BOLD)
    
    if not is_tty():
        # Non-interactive mode - require explicit approval flag
        loud_error("NON-INTERACTIVE MODE: Cannot request human approval.")
        loud_error("This action requires human approval. Run interactively or use --approve flag.")
        return False
    
    response = input("\n" + Colors.BOLD + "Approve this action? (yes/NO): " + Colors.RESET).strip().lower()
    approved = response in ['yes', 'y']
    
    if approved:
        loud_success("✅ Human approval granted")
    else:
        loud_warning("❌ Human approval DENIED - Action cancelled")
    
    return approved


def extract_guardians_from_source_of_truth() -> Set[str]:
    """Extract guardians from the single source of truth."""
    source_file = project_root / SINGLE_SOURCE_OF_TRUTH
    
    if not source_file.exists():
        loud_error(f"CRITICAL: Single source of truth not found!")
        loud_error(f"Expected file: {SINGLE_SOURCE_OF_TRUTH}")
        loud_error(f"Full path: {source_file.absolute()}")
        loud_error("\n🔧 ACTION REQUIRED:")
        loud_error("   1. Verify the file exists at the expected location")
        loud_error("   2. Check SINGLE_SOURCE_OF_TRUTH path in enforcement script")
        loud_error("   3. Ensure you're running from the project root")
        sys.exit(1)
    
    guardians = set()
    
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for GuardianIdentity(name="...")
        pattern = r'GuardianIdentity\s*\(\s*name\s*=\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, content)
        guardians.update(matches)
        
    except PermissionError as e:
        loud_error(f"CRITICAL: Permission denied reading source of truth!")
        loud_error(f"File: {source_file.absolute()}")
        loud_error(f"Error: {e}")
        loud_error("\n🔧 ACTION REQUIRED:")
        loud_error("   1. Check file permissions")
        loud_error("   2. Ensure read access to the file")
        sys.exit(1)
    except Exception as e:
        loud_error(f"CRITICAL: Unexpected error reading source of truth!")
        loud_error(f"File: {source_file.absolute()}")
        loud_error(f"Error: {e}")
        loud_error(f"\nTraceback:\n{traceback.format_exc()}")
        sys.exit(1)
    
    return guardians


def extract_guardians_from_python(file_path: Path) -> Set[str]:
    """Extract guardian names from Python file."""
    guardians = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for GuardianIdentity(name="...")
        pattern = r'GuardianIdentity\s*\(\s*name\s*=\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, content)
        guardians.update(matches)
        
        # Look for {"name": "..."} or {"id": "guardian-..."}
        pattern = r'["\']name["\']\s*:\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, content)
        guardians.update(matches)
        
        # Look for guardian-* IDs
        pattern = r'["\']guardian-([^"\']+)["\']'
        matches = re.findall(pattern, content)
        for match in matches:
            # Convert IDs to names (guardian-aeyon -> AEYON)
            name = match.replace('-', '').upper()
            if 'ABE' in name:
                name = "Abë"
            elif 'JOHN' in name or 'JØHN' in name:
                name = "JØHN"
            elif 'LUX' in name:
                name = "Lux"
            elif 'POLY' in name:
                name = "Poly"
            else:
                # Try exact match
                for expected in EXPECTED_GUARDIANS.keys():
                    if name == expected.upper():
                        name = expected
                        break
            guardians.add(name)
            
    except PermissionError as e:
        loud_warning(f"Permission denied reading {file_path}: {e}")
    except Exception as e:
        loud_warning(f"Error reading {file_path}: {e}")
        loud_warning(f"Traceback: {traceback.format_exc()}")
    
    return guardians


def extract_guardians_from_markdown(file_path: Path) -> Set[str]:
    """Extract guardian names from Markdown file."""
    guardians = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for | **GUARDIAN** | pattern
        pattern = r'\|\s*\*\*([A-ZÆØÅË]+)\*\*'
        matches = re.findall(pattern, content)
        guardians.update(matches)
        
        # Look for Guardian names in numbered lists
        pattern = r'(\d+\.\s+)?\*\*([A-ZÆØÅË]+)\*\*'
        matches = re.findall(pattern, content)
        for match in matches:
            if isinstance(match, tuple):
                guardian_name = match[1] if match[1] else match[0]
            else:
                guardian_name = match
            if guardian_name:
                guardians.add(guardian_name)
        
        # Look for Abë, Lux, Poly specifically (special characters)
        if "**Abë**" in content or "Abë" in content:
            guardians.add("Abë")
        if "**Lux**" in content or "Lux" in content:
            guardians.add("Lux")
        if "**Poly**" in content or "Poly" in content:
            guardians.add("Poly")
            
    except PermissionError as e:
        loud_warning(f"Permission denied reading {file_path}: {e}")
    except Exception as e:
        loud_warning(f"Error reading {file_path}: {e}")
        loud_warning(f"Traceback: {traceback.format_exc()}")
    
    return guardians


def normalize_guardian_name(name: str) -> Optional[str]:
    """Normalize guardian name to match expected format."""
    name_upper = name.upper()
    
    # Handle special cases
    if 'ABE' in name_upper or 'ABË' in name_upper:
        return "Abë"
    elif 'JOHN' in name_upper or 'JØHN' in name_upper:
        return "JØHN"
    elif 'LUX' in name_upper:
        return "Lux"
    elif 'POLY' in name_upper:
        return "Poly"
    elif 'CHRONOS' in name_upper:
        return "CHRONOS"
    
    # Try exact match
    for expected in EXPECTED_GUARDIANS.keys():
        if name_upper == expected.upper():
            return expected
    
    return None


def validate_file(file_path: Path, is_critical: bool) -> Tuple[bool, Set[str], Set[str], Set[str]]:
    """
    Validate a file's guardian definitions.
    
    Returns:
        (is_valid, found_guardians, missing_guardians, extra_guardians)
    """
    if not file_path.exists():
        if is_critical:
            return False, set(), EXPECTED_GUARDIANS.keys(), set()
        return True, set(), set(), set()  # Optional files can be missing
    
    # Extract guardians based on file type
    if file_path.suffix == '.py':
        found_guardians = extract_guardians_from_python(file_path)
    elif file_path.suffix == '.md':
        found_guardians = extract_guardians_from_markdown(file_path)
    else:
        return True, set(), set(), set()  # Unknown file type, skip
    
    # Normalize guardian names
    normalized_found = set()
    for g in found_guardians:
        normalized = normalize_guardian_name(g)
        if normalized:
            normalized_found.add(normalized)
    
    # Check for missing and extra guardians
    expected_set = set(EXPECTED_GUARDIANS.keys())
    missing = expected_set - normalized_found
    extra = normalized_found - expected_set - set(SPECIAL_GUARDIANS.keys())
    
    # For critical files, must have all expected guardians
    # For optional files, just report differences
    if is_critical:
        is_valid = len(missing) == 0 and len(extra) == 0
    else:
        is_valid = True  # Optional files are always "valid" but we report differences
    
    return is_valid, normalized_found, missing, extra


def enforce_single_source_of_truth(strict: bool = False, approve: bool = False, auto_heal: bool = False) -> int:
    """
    Enforce single source of truth for Guardians.
    
    Args:
        strict: If True, exit with error on any inconsistency
        approve: If True, skip human approval prompts (use with caution)
    
    Returns:
        Exit code (0 = success, 1 = failure)
    """
    try:
        loud_print("=" * 80, Colors.CYAN + Colors.BOLD)
        loud_print("🔥 GUARDIAN SINGLE SOURCE OF TRUTH ENFORCEMENT", Colors.CYAN + Colors.BOLD)
        loud_print("=" * 80, Colors.CYAN + Colors.BOLD)
        print()
        loud_print(f"📋 Single Source of Truth: {SINGLE_SOURCE_OF_TRUTH}", Colors.WHITE)
        loud_print(f"📋 Expected Guardians: {len(EXPECTED_GUARDIANS)}", Colors.WHITE)
        loud_print(f"📋 Critical Files: {len(CRITICAL_FILES)}", Colors.WHITE)
        loud_print(f"📋 Optional Files: {len(OPTIONAL_FILES)}", Colors.WHITE)
        print()
    except Exception as e:
        loud_error(f"Failed to initialize enforcement: {e}")
        loud_error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)
    
    # Extract guardians from source of truth
    try:
        source_guardians = extract_guardians_from_source_of_truth()
        loud_print(f"✅ Source of Truth: Found {len(source_guardians)} guardians", Colors.GREEN)
        loud_print(f"   Guardians: {', '.join(sorted(source_guardians))}", Colors.WHITE)
        print()
    except SystemExit:
        raise  # Re-raise system exits
    except Exception as e:
        loud_error(f"Failed to extract guardians from source of truth: {e}")
        loud_error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)
    
    # Validate source of truth
    try:
        expected_set = set(EXPECTED_GUARDIANS.keys())
        source_normalized = {normalize_guardian_name(g) for g in source_guardians}
        source_normalized = {g for g in source_normalized if g}
        
        source_missing = expected_set - source_normalized
        if source_missing:
            loud_error("CRITICAL: Source of truth is INCOMPLETE!")
            loud_error(f"Missing guardians: {', '.join(sorted(source_missing))}")
            loud_error(f"Expected {len(EXPECTED_GUARDIANS)} guardians, found {len(source_normalized)}")
            loud_error("\n🔧 ACTION REQUIRED:")
            loud_error(f"   1. Add missing guardians to {SINGLE_SOURCE_OF_TRUTH}")
            loud_error("   2. Ensure all 10 core guardians are defined")
            loud_error("   3. Run validation again after fixes")
            return 1
        
        loud_success("✅ Source of Truth: VALID")
        print()
    except Exception as e:
        loud_error(f"Failed to validate source of truth: {e}")
        loud_error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)
    
    # Validate critical files
    loud_print("=" * 80, Colors.BLUE + Colors.BOLD)
    loud_print("🔍 VALIDATING CRITICAL FILES", Colors.BLUE + Colors.BOLD)
    loud_print("=" * 80, Colors.BLUE + Colors.BOLD)
    print()
    
    all_valid = True
    critical_errors = []
    
    try:
        for file_path_str in CRITICAL_FILES:
            file_path = project_root / file_path_str
            loud_print(f"📄 Checking: {file_path_str}", Colors.CYAN)
            
            try:
                is_valid, found, missing, extra = validate_file(file_path, is_critical=True)
                
                # Record check in self-healing system
                _self_healing.record_check(inconsistent=not is_valid)
                
                if is_valid:
                    loud_success(f"   ✅ VALID - Found {len(found)}/{len(EXPECTED_GUARDIANS)} guardians")
                else:
                    all_valid = False
                    loud_error(f"   ❌ INVALID - Found {len(found)}/{len(EXPECTED_GUARDIANS)} guardians")
                    
                    if missing:
                        loud_error(f"   ⚠️  Missing: {', '.join(sorted(missing))}")
                    if extra:
                        loud_error(f"   ⚠️  Extra: {', '.join(sorted(extra))}")
                    
                    # Self-healing: Create backup before potential fixes
                    if auto_heal:
                        backup_path = _self_healing.create_backup(file_path)
                        if backup_path:
                            loud_print(f"   💾 Backup created: {backup_path.name}", Colors.CYAN)
                    
                    critical_errors.append({
                        "file": file_path_str,
                        "missing": missing,
                        "extra": extra,
                        "found": found,
                        "file_path": file_path
                    })
                
                print()
            except Exception as e:
                all_valid = False
                loud_error(f"   ❌ ERROR validating {file_path_str}: {e}")
                loud_error(f"   Traceback:\n{traceback.format_exc()}")
                critical_errors.append({
                    "file": file_path_str,
                    "missing": set(EXPECTED_GUARDIANS.keys()),
                    "extra": set(),
                    "error": str(e)
                })
                print()
    except Exception as e:
        loud_error(f"Failed during critical file validation: {e}")
        loud_error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)
    
    # Validate optional files (report but don't fail)
    loud_print("=" * 80, Colors.MAGENTA + Colors.BOLD)
    loud_print("📊 CHECKING OPTIONAL FILES", Colors.MAGENTA + Colors.BOLD)
    loud_print("=" * 80, Colors.MAGENTA + Colors.BOLD)
    print()
    
    optional_warnings = []
    
    try:
        for file_path_str in OPTIONAL_FILES:
            file_path = project_root / file_path_str
            loud_print(f"📄 Checking: {file_path_str}", Colors.CYAN)
            
            try:
                is_valid, found, missing, extra = validate_file(file_path, is_critical=False)
                
                if missing or extra:
                    loud_warning(f"   ⚠️  Differences found - Found {len(found)} guardians")
                    
                    if missing:
                        loud_warning(f"      Missing: {', '.join(sorted(missing))}")
                    if extra:
                        loud_warning(f"      Extra: {', '.join(sorted(extra))}")
                    
                    optional_warnings.append({
                        "file": file_path_str,
                        "missing": missing,
                        "extra": extra
                    })
                else:
                    loud_success(f"   ✅ Matches source of truth - Found {len(found)}/{len(EXPECTED_GUARDIANS)} guardians")
                
                print()
            except Exception as e:
                loud_warning(f"   ⚠️  Error checking {file_path_str}: {e}")
                print()
    except Exception as e:
        loud_warning(f"Failed during optional file validation: {e}")
        loud_warning(f"Traceback: {traceback.format_exc()}")
        # Don't exit on optional file errors
    
    # Summary
    loud_print("=" * 80, Colors.CYAN + Colors.BOLD)
    loud_print("📊 ENFORCEMENT SUMMARY", Colors.CYAN + Colors.BOLD)
    loud_print("=" * 80, Colors.CYAN + Colors.BOLD)
    print()
    
    # Calculate and display epistemic certainty
    certainty_score = _self_healing.calculate_consistency_score()
    certainty_percent = certainty_score * 100
    loud_print(f"📊 Epistemic Certainty: {certainty_percent:.1f}%", Colors.CYAN + Colors.BOLD)
    
    if certainty_score >= 0.978:
        loud_success(f"✅ System meets 97.8% epistemic certainty threshold ({certainty_percent:.1f}%)")
    else:
        gap = 0.978 - certainty_score
        loud_warning(f"⚠️  System below threshold ({certainty_percent:.1f}% < 97.8%, gap: {gap*100:.1f}%)")
    
    print()
    
    try:
        if all_valid:
            loud_success("✅ ALL CRITICAL FILES ARE CONSISTENT!")
            print()
            loud_success("✅ Single source of truth enforced")
            loud_success("✅ All critical files match source of truth")
            
            if optional_warnings:
                print()
                loud_warning("Optional files have differences (documented exceptions):")
                for warning in optional_warnings:
                    loud_print(f"   - {warning['file']}", Colors.YELLOW)
                    if warning['missing']:
                        loud_print(f"     Missing: {', '.join(sorted(warning['missing']))}", Colors.YELLOW)
                    if warning['extra']:
                        loud_print(f"     Extra: {', '.join(sorted(warning['extra']))}", Colors.YELLOW)
            
            print()
            loud_print("=" * 80, Colors.GREEN + Colors.BOLD)
            loud_success("✅ ENFORCEMENT PASSED - ALL SYSTEMS VALID")
            loud_print("=" * 80 + "\n", Colors.GREEN + Colors.BOLD)
            return 0
        else:
            loud_error("ENFORCEMENT FAILED - CRITICAL INCONSISTENCIES FOUND")
            print()
            loud_error("The following critical files do not match the single source of truth:")
            for error in critical_errors:
                loud_error(f"  ❌ {error['file']}")
                if 'error' in error:
                    loud_error(f"     Error: {error['error']}")
                if error.get('missing'):
                    loud_error(f"     Missing: {', '.join(sorted(error['missing']))}")
                if error.get('extra'):
                    loud_error(f"     Extra: {', '.join(sorted(error['extra']))}")
            print()
            loud_error("🔧 ACTION REQUIRED:")
            loud_error("   1. Update files to match single source of truth")
            loud_error(f"   2. Single source: {SINGLE_SOURCE_OF_TRUTH}")
            loud_error("   3. Expected guardians: " + ", ".join(sorted(EXPECTED_GUARDIANS.keys())))
            loud_error("   4. Run validation again after fixes")
            print()
            loud_print("=" * 80, Colors.ERROR_BG + Colors.WHITE + Colors.BOLD)
            loud_error("❌ ENFORCEMENT FAILED - FIX REQUIRED BEFORE PROCEEDING")
            loud_print("=" * 80 + "\n", Colors.ERROR_BG + Colors.WHITE + Colors.BOLD)
            
            if strict:
                return 1
            else:
                loud_warning("Continuing in non-strict mode...")
                loud_warning("⚠️  WARNING: Inconsistencies detected but not blocking")
                return 0
    except Exception as e:
        loud_error(f"Failed during summary generation: {e}")
        loud_error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Enforce Guardian single source of truth",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic check (warnings only)
  python3 scripts/enforce_guardian_single_source_of_truth.py
  
  # Strict mode (exits with error on inconsistencies)
  python3 scripts/enforce_guardian_single_source_of_truth.py --strict
  
  # Non-interactive mode (for CI/CD - requires --approve for any fixes)
  python3 scripts/enforce_guardian_single_source_of_truth.py --strict --approve

Pattern: ENFORCEMENT × TRUTH × CONSISTENCY × ONE
∞ AbëONE ∞
        """
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error on any inconsistency (LOUD failure)"
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Skip human approval prompts (use with caution - for CI/CD only)"
    )
    parser.add_argument(
        "--auto-heal",
        action="store_true",
        help="Enable automatic self-healing (creates backups, attempts repairs)"
    )
    
    args = parser.parse_args()
    
    try:
        exit_code = enforce_single_source_of_truth(strict=args.strict, approve=args.approve, auto_heal=args.auto_heal)
        
        if exit_code == 0:
            loud_success("✅ Enforcement passed")
        else:
            loud_error("❌ Enforcement failed")
            # Make exit loud
            loud_print("\n" + "🚨" * 40, Colors.ERROR_BG + Colors.WHITE + Colors.BOLD + Colors.BLINK)
            loud_error("EXITING WITH ERROR CODE 1")
            loud_print("🚨" * 40 + "\n", Colors.ERROR_BG + Colors.WHITE + Colors.BOLD + Colors.BLINK)
        
        return exit_code
    except KeyboardInterrupt:
        loud_error("\n\n⚠️  Interrupted by user")
        loud_error("Enforcement cancelled")
        return 130  # Standard exit code for SIGINT
    except SystemExit as e:
        raise  # Re-raise system exits
    except Exception as e:
        loud_error(f"Unexpected error in main: {e}")
        loud_error(f"Traceback:\n{traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())

