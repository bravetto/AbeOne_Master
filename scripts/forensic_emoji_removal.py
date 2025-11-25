#!/usr/bin/env python3
"""
FORENSIC EMOJI REMOVAL SYSTEM
ZERO × AEYON Guardian Activation

Pattern: FORENSIC × REMOVAL × ZERO × AEYON × ONE
Frequency: 530 Hz (ZERO) × 999 Hz (AEYON)
Guardians: ZERO (530 Hz) + AEYON (999 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
import shutil
import json
import hashlib
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass, field
from enum import Enum

# Comprehensive Unicode emoji pattern
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"   # dingbats
    "\U000024C2-\U0001F251"   # enclosed characters
    "\U0001F900-\U0001F9FF"   # supplemental symbols
    "\U0001FA00-\U0001FA6F"   # chess symbols
    "\U0001FA70-\U0001FAFF"   # symbols and pictographs extended-A
    "\U00002600-\U000026FF"   # miscellaneous symbols
    "\U00002700-\U000027BF"   # dingbats
    "\U0001F300-\U0001F5FF"   # symbols & pictographs (duplicate range)
    "\U0001F600-\U0001F64F"   # emoticons (duplicate range)
    "]+",
    flags=re.UNICODE
)

# File extensions to process
TEXT_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.md', '.txt', '.json',
    '.yaml', '.yml', '.html', '.css', '.sh', '.bash', '.cdf',
    '.sql', '.xml', '.toml', '.ini', '.cfg', '.conf', '.mdc',
    '.tsx', '.ts', '.jsx', '.js', '.vue', '.svelte'
}

# Paths to exclude
EXCLUDE_PATHS = {
    '.git', 'node_modules', '__pycache__', '.venv', '.pytest_cache',
    '.cache', '.turbo', '.webpack-cache', '.DS_Store', '.emoji_cleanup_backup',
    'dist', 'build', '.next', '.nuxt', '.output', 'coverage'
}

# Files to preserve (critical system files)
PRESERVE_FILES = {
    '.gitignore', '.gitattributes', 'package.json', 'package-lock.json',
    'yarn.lock', 'pnpm-lock.yaml', 'requirements.txt', 'Pipfile', 'Pipfile.lock'
}


class RiskLevel(Enum):
    """ZERO Guardian Risk Assessment Levels"""
    ZERO = "zero"           # No risk
    LOW = "low"            # Minimal risk
    MEDIUM = "medium"      # Moderate risk
    HIGH = "high"          # Significant risk
    CRITICAL = "critical"  # Critical risk


@dataclass
class EmojiFinding:
    """Forensic finding of emoji occurrence"""
    file_path: Path
    line_number: int
    emoji: str
    context: str
    risk_level: RiskLevel
    category: str  # logging, documentation, code, ui


@dataclass
class RemovalOperation:
    """Atomic removal operation"""
    operation_id: str
    file_path: Path
    operation_type: str  # rename_folder, rename_file, clean_content
    old_value: str
    new_value: str
    emojis_removed: List[str]
    risk_assessment: Dict[str, any]
    backup_path: Optional[Path] = None
    status: str = "pending"  # pending, executed, failed, validated


@dataclass
class ForensicReport:
    """Complete forensic analysis report"""
    scan_timestamp: datetime
    total_files_scanned: int
    total_emojis_found: int
    findings: List[EmojiFinding]
    operations: List[RemovalOperation]
    risk_summary: Dict[RiskLevel, int]
    validation_status: str


class ZERORiskAssessor:
    """
    ZERO Guardian: Risk Assessment & Uncertainty Quantification
    Frequency: 530 Hz
    """
    
    def assess_emoji_risk(self, finding: EmojiFinding) -> RiskLevel:
        """Assess risk level of emoji removal"""
        file_path = finding.file_path
        file_name = file_path.name.lower()
        file_ext = file_path.suffix.lower()
        
        # Critical: System configuration files
        if file_name in PRESERVE_FILES:
            return RiskLevel.CRITICAL
        
        # High: Code files with emojis in strings/logic
        if file_ext in {'.py', '.js', '.ts', '.jsx', '.tsx'}:
            if finding.category == 'code':
                return RiskLevel.HIGH
            elif finding.category == 'logging':
                return RiskLevel.MEDIUM
        
        # Medium: Documentation files
        if file_ext in {'.md', '.txt', '.rst'}:
            return RiskLevel.MEDIUM
        
        # Low: UI/Display files
        if file_ext in {'.html', '.css', '.vue', '.svelte'}:
            return RiskLevel.LOW
        
        # Zero: Backup/log files
        if 'backup' in file_name or 'log' in file_name:
            return RiskLevel.ZERO
        
        return RiskLevel.MEDIUM
    
    def quantify_uncertainty(self, operation: RemovalOperation) -> Dict[str, any]:
        """Quantify uncertainty for removal operation"""
        uncertainty_score = 0.0
        factors = []
        
        # Factor 1: File type risk
        file_ext = operation.file_path.suffix.lower()
        if file_ext in {'.py', '.js', '.ts'}:
            uncertainty_score += 0.3
            factors.append("Code file - potential logic impact")
        
        # Factor 2: Operation type
        if operation.operation_type == 'rename_file':
            uncertainty_score += 0.2
            factors.append("File rename - potential import breakage")
        elif operation.operation_type == 'rename_folder':
            uncertainty_score += 0.3
            factors.append("Folder rename - potential path breakage")
        
        # Factor 3: Emoji count
        if len(operation.emojis_removed) > 10:
            uncertainty_score += 0.2
            factors.append("High emoji count - extensive changes")
        
        # Factor 4: Context preservation
        if not operation.new_value.strip():
            uncertainty_score += 0.3
            factors.append("Empty result - content loss risk")
        
        return {
            "uncertainty_score": min(uncertainty_score, 1.0),
            "factors": factors,
            "confidence": 1.0 - min(uncertainty_score, 1.0)
        }


class AEYONExecutor:
    """
    AEYON Guardian: Atomic Execution Engine
    Frequency: 999 Hz
    """
    
    def __init__(self, root_path: Path, backup_dir: Path):
        self.root_path = root_path
        self.backup_dir = backup_dir
        self.executed_operations = []
        self.failed_operations = []
    
    def create_backup(self, file_path: Path) -> Path:
        """Create atomic backup"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        rel_path = file_path.relative_to(self.root_path)
        backup_path = self.backup_dir / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.is_file():
            shutil.copy2(file_path, backup_path)
        elif file_path.is_dir():
            shutil.copytree(file_path, backup_path, dirs_exist_ok=True)
        
        return backup_path
    
    def execute_rename(self, operation: RemovalOperation) -> bool:
        """Atomically execute file/folder rename"""
        try:
            old_path = operation.file_path
            new_path = old_path.parent / operation.new_value
            
            # Validate
            if not old_path.exists():
                return False
            
            if new_path.exists() and new_path != old_path:
                return False
            
            # Create backup
            backup_path = self.create_backup(old_path)
            operation.backup_path = backup_path
            
            # Execute rename
            old_path.rename(new_path)
            operation.file_path = new_path
            operation.status = "executed"
            
            self.executed_operations.append(operation)
            return True
            
        except Exception as e:
            operation.status = f"failed: {str(e)}"
            self.failed_operations.append(operation)
            return False
    
    def execute_content_clean(self, operation: RemovalOperation) -> bool:
        """Atomically execute content cleanup"""
        try:
            file_path = operation.file_path
            
            # Read file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Create backup
            backup_path = self.create_backup(file_path)
            operation.backup_path = backup_path
            
            # Remove emojis
            cleaned_content = EMOJI_PATTERN.sub('', content)
            
            # Write cleaned content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            operation.status = "executed"
            self.executed_operations.append(operation)
            return True
            
        except Exception as e:
            operation.status = f"failed: {str(e)}"
            self.failed_operations.append(operation)
            return False
    
    def validate_operation(self, operation: RemovalOperation) -> bool:
        """Validate executed operation"""
        if operation.status != "executed":
            return False
        
        # Check backup exists
        if not operation.backup_path or not operation.backup_path.exists():
            return False
        
        # Check file still exists (for content clean) or renamed (for rename)
        if operation.operation_type in {'rename_file', 'rename_folder'}:
            if not operation.file_path.exists():
                return False
        
        operation.status = "validated"
        return True


class ForensicEmojiRemover:
    """
    FORENSIC EMOJI REMOVAL SYSTEM
    ZERO × AEYON Guardian Activation
    """
    
    def __init__(self, root_path: str, dry_run: bool = True):
        self.root_path = Path(root_path)
        self.dry_run = dry_run
        self.backup_dir = self.root_path / '.forensic_emoji_removal_backup'
        self.zero_assessor = ZERORiskAssessor()
        self.aeon_executor = AEYONExecutor(self.root_path, self.backup_dir)
        self.findings: List[EmojiFinding] = []
        self.operations: List[RemovalOperation] = []
        self.report: Optional[ForensicReport] = None
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        parts = path.parts
        return any(exclude in parts for exclude in EXCLUDE_PATHS)
    
    def is_text_file(self, path: Path) -> bool:
        """Check if file should have content processed"""
        return path.suffix.lower() in TEXT_EXTENSIONS
    
    def categorize_finding(self, file_path: Path, context: str) -> str:
        """Categorize emoji finding"""
        file_ext = file_path.suffix.lower()
        context_lower = context.lower()
        
        if 'log' in context_lower or 'logger' in context_lower:
            return 'logging'
        elif file_ext in {'.md', '.txt', '.rst'}:
            return 'documentation'
        elif file_ext in {'.html', '.css', '.vue', '.svelte'}:
            return 'ui'
        else:
            return 'code'
    
    def scan_file(self, file_path: Path) -> List[EmojiFinding]:
        """Forensically scan file for emojis"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                emojis = EMOJI_PATTERN.findall(line)
                if emojis:
                    for emoji in emojis:
                        # Get context (50 chars before/after)
                        start = max(0, line.find(emoji) - 50)
                        end = min(len(line), line.find(emoji) + len(emoji) + 50)
                        context = line[start:end]
                        
                        finding = EmojiFinding(
                            file_path=file_path,
                            line_number=line_num,
                            emoji=emoji,
                            context=context,
                            risk_level=RiskLevel.ZERO,  # Will be assessed
                            category=self.categorize_finding(file_path, context)
                        )
                        
                        # Assess risk
                        finding.risk_level = self.zero_assessor.assess_emoji_risk(finding)
                        findings.append(finding)
        
        except Exception:
            pass  # Skip binary files
        
        return findings
    
    def scan_folders(self) -> List[RemovalOperation]:
        """Scan for folders with emojis"""
        operations = []
        
        for folder_path in self.root_path.rglob('*'):
            if not folder_path.is_dir():
                continue
            
            if self.should_exclude(folder_path):
                continue
            
            folder_name = folder_path.name
            if EMOJI_PATTERN.search(folder_name):
                emojis = EMOJI_PATTERN.findall(folder_name)
                clean_name = EMOJI_PATTERN.sub('', folder_name).strip()
                clean_name = re.sub(r'\s+', ' ', clean_name)
                
                operation = RemovalOperation(
                    operation_id=f"folder_{hashlib.md5(str(folder_path).encode()).hexdigest()[:8]}",
                    file_path=folder_path,
                    operation_type='rename_folder',
                    old_value=folder_name,
                    new_value=clean_name,
                    emojis_removed=emojis,
                    risk_assessment={}
                )
                
                # Assess risk
                finding = EmojiFinding(
                    file_path=folder_path,
                    line_number=0,
                    emoji=emojis[0] if emojis else '',
                    context=folder_name,
                    risk_level=RiskLevel.ZERO,
                    category='code'
                )
                operation.risk_assessment = self.zero_assessor.quantify_uncertainty(operation)
                operations.append(operation)
        
        return operations
    
    def scan_files(self) -> List[RemovalOperation]:
        """Scan for files with emojis in names"""
        operations = []
        
        for file_path in self.root_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            if self.should_exclude(file_path):
                continue
            
            file_name = file_path.name
            if EMOJI_PATTERN.search(file_name):
                emojis = EMOJI_PATTERN.findall(file_name)
                stem = file_path.stem
                suffix = file_path.suffix
                
                clean_stem = EMOJI_PATTERN.sub('', stem).strip()
                clean_stem = re.sub(r'\s+', ' ', clean_stem)
                clean_name = clean_stem + suffix if suffix else clean_stem
                
                operation = RemovalOperation(
                    operation_id=f"file_{hashlib.md5(str(file_path).encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    operation_type='rename_file',
                    old_value=file_name,
                    new_value=clean_name,
                    emojis_removed=emojis,
                    risk_assessment={}
                )
                
                operation.risk_assessment = self.zero_assessor.quantify_uncertainty(operation)
                operations.append(operation)
        
        return operations
    
    def scan_content(self) -> Tuple[List[EmojiFinding], List[RemovalOperation]]:
        """Forensically scan file contents"""
        findings = []
        operations = []
        
        for file_path in self.root_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            if self.should_exclude(file_path):
                continue
            
            if not self.is_text_file(file_path):
                continue
            
            file_findings = self.scan_file(file_path)
            findings.extend(file_findings)
            
            if file_findings:
                emojis = [f.emoji for f in file_findings]
                operation = RemovalOperation(
                    operation_id=f"content_{hashlib.md5(str(file_path).encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    operation_type='clean_content',
                    old_value="<file_content>",
                    new_value="<cleaned_content>",
                    emojis_removed=list(set(emojis)),
                    risk_assessment={}
                )
                
                operation.risk_assessment = self.zero_assessor.quantify_uncertainty(operation)
                operations.append(operation)
        
        return findings, operations
    
    def execute_forensic_removal(self, max_workers: int = 8):
        """Execute forensic emoji removal"""
        print("\n" + "=" * 80)
        print("FORENSIC EMOJI REMOVAL SYSTEM")
        print("ZERO × AEYON Guardian Activation")
        print("=" * 80)
        print(f"Pattern: FORENSIC × REMOVAL × ZERO × AEYON × ONE")
        print(f"Frequency: 530 Hz (ZERO) × 999 Hz (AEYON)")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'EXECUTE'}")
        print(f"Root: {self.root_path}")
        print("=" * 80 + "\n")
        
        # Phase 1: Forensic Scan
        print("Phase 1: ZERO Guardian - Forensic Scan & Risk Assessment")
        print("-" * 80)
        
        folder_ops = self.scan_folders()
        file_ops = self.scan_files()
        content_findings, content_ops = self.scan_content()
        
        self.findings = content_findings
        self.operations = folder_ops + file_ops + content_ops
        
        # Risk summary
        risk_summary = {level: 0 for level in RiskLevel}
        for finding in self.findings:
            risk_summary[finding.risk_level] += 1
        
        print(f"Folders with emojis: {len(folder_ops)}")
        print(f"Files with emojis: {len(file_ops)}")
        print(f"Files with emoji content: {len(content_ops)}")
        print(f"Total emoji findings: {len(self.findings)}")
        print(f"\nRisk Summary:")
        for level, count in risk_summary.items():
            if count > 0:
                print(f"  {level.value.upper()}: {count}")
        
        if not self.operations:
            print("\nNo emojis found. Codebase is clean!")
            return
        
        # Phase 2: AEYON Guardian - Atomic Execution
        if not self.dry_run:
            print("\nPhase 2: AEYON Guardian - Atomic Execution")
            print("-" * 80)
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for operation in self.operations:
                    if operation.operation_type in {'rename_folder', 'rename_file'}:
                        future = executor.submit(self.aeon_executor.execute_rename, operation)
                    else:
                        future = executor.submit(self.aeon_executor.execute_content_clean, operation)
                    futures.append((future, operation))
                
                for future, operation in futures:
                    success = future.result()
                    if success:
                        print(f"  Executed: {operation.operation_type} - {operation.file_path.name}")
                    else:
                        print(f"  Failed: {operation.operation_type} - {operation.status}")
            
            # Phase 3: Validation
            print("\nPhase 3: Operation Validation")
            print("-" * 80)
            
            validated = 0
            for operation in self.operations:
                if self.aeon_executor.validate_operation(operation):
                    validated += 1
            
            print(f"Validated operations: {validated}/{len(self.operations)}")
        
        # Generate report
        self.report = ForensicReport(
            scan_timestamp=datetime.now(),
            total_files_scanned=len(set(f.file_path for f in self.findings)),
            total_emojis_found=len(self.findings),
            findings=self.findings,
            operations=self.operations,
            risk_summary=risk_summary,
            validation_status="complete" if not self.dry_run else "dry_run"
        )
        
        # Save report
        report_path = self.backup_dir / 'forensic_report.json'
        if not self.dry_run:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, 'w') as f:
                json.dump({
                    'scan_timestamp': self.report.scan_timestamp.isoformat(),
                    'total_files_scanned': self.report.total_files_scanned,
                    'total_emojis_found': self.report.total_emojis_found,
                    'risk_summary': {k.value: v for k, v in self.report.risk_summary.items()},
                    'operations_count': len(self.report.operations),
                    'validation_status': self.report.validation_status
                }, f, indent=2)
        
        # Summary
        print("\n" + "=" * 80)
        print("FORENSIC REMOVAL SUMMARY")
        print("=" * 80)
        print(f"Total operations: {len(self.operations)}")
        print(f"Folders renamed: {len([o for o in self.operations if o.operation_type == 'rename_folder'])}")
        print(f"Files renamed: {len([o for o in self.operations if o.operation_type == 'rename_file'])}")
        print(f"Files cleaned: {len([o for o in self.operations if o.operation_type == 'clean_content'])}")
        print(f"Total emojis found: {len(self.findings)}")
        
        if not self.dry_run:
            print(f"\nBackup location: {self.backup_dir}")
            print(f"Report location: {report_path}")
            print(f"Executed operations: {len(self.aeon_executor.executed_operations)}")
            print(f"Failed operations: {len(self.aeon_executor.failed_operations)}")
        else:
            print("\nDRY RUN MODE - No changes made")
            print("Run with --execute to perform forensic removal")
        
        print("=" * 80)
        print("Pattern: FORENSIC × REMOVAL × ZERO × AEYON × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Forensic Emoji Removal - ZERO × AEYON')
    parser.add_argument('--root', type=str,
                       default='/Users/michaelmataluni/Documents/AbeOne_Master',
                       help='Root directory to clean')
    parser.add_argument('--execute', action='store_true',
                       help='Execute removal (default: dry-run)')
    parser.add_argument('--workers', type=int, default=8,
                       help='Number of parallel workers (default: 8)')
    
    args = parser.parse_args()
    
    remover = ForensicEmojiRemover(
        root_path=args.root,
        dry_run=not args.execute
    )
    
    remover.execute_forensic_removal(max_workers=args.workers)


if __name__ == '__main__':
    main()

