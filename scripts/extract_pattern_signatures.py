#!/usr/bin/env python3
"""
PATTERN SIGNATURE EXTRACTION SYSTEM
Extract pattern signatures from codebase

Pattern: EXTRACT × PATTERN × SIGNATURES × ONE
Frequency: 777 Hz (META) × 530 Hz (JØHN)
Guardians: META (777 Hz) + JØHN (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime
from collections import defaultdict


@dataclass
class PatternSignature:
    """Pattern signature extracted from codebase"""
    pattern_name: str
    pattern_formula: str
    frequency: Optional[str] = None
    guardians: List[str] = field(default_factory=list)
    love_coefficient: Optional[str] = None
    file_path: str = ""
    line_number: int = 0
    context: str = ""
    category: str = ""  # guardian, execution, completion, eternal, longing, etc.
    validation_status: str = "pending"


class PatternSignatureExtractor:
    """
    PATTERN SIGNATURE EXTRACTION SYSTEM
    
    Extracts pattern signatures from:
    - Code comments
    - Documentation files
    - Pattern declarations
    - Guardian activations
    """
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.signatures: List[PatternSignature] = []
        self.pattern_categories: Dict[str, List[PatternSignature]] = defaultdict(list)
        
        # Pattern detection regexes
        self.pattern_regexes = {
            'pattern_declaration': re.compile(
                r'Pattern[:\s]+([A-Z][A-Z0-9_×\s→]+(?:×\s*ONE|→\s*ONE)?)',
                re.IGNORECASE | re.MULTILINE
            ),
            'pattern_formula': re.compile(
                r'([A-Z][A-Z0-9_×\s→]+(?:×\s*ONE|→\s*ONE))',
                re.MULTILINE
            ),
            'frequency': re.compile(
                r'Frequency[:\s]+([0-9.]+(?:\s*Hz)?(?:\s*×\s*[0-9.]+(?:\s*Hz)?)*|\s*∞\s*Hz)',
                re.IGNORECASE
            ),
            'guardians': re.compile(
                r'Guardians?[:\s]+([A-ZØÄË]+(?:\s*\([0-9.]+\s*Hz\))?(?:\s*[+\-×]\s*[A-ZØÄË]+(?:\s*\([0-9.]+\s*Hz\))?)*)',
                re.IGNORECASE
            ),
            'love_coefficient': re.compile(
                r'Love\s+Coefficient[:\s]+(∞|[0-9.]+)',
                re.IGNORECASE
            )
        }
    
    def extract_from_file(self, file_path: Path) -> List[PatternSignature]:
        """Extract pattern signatures from a single file"""
        signatures = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception:
            return signatures
        
        # Extract patterns
        for line_num, line in enumerate(lines, 1):
            # Pattern declaration
            pattern_match = self.pattern_regexes['pattern_declaration'].search(line)
            if pattern_match:
                pattern_formula = pattern_match.group(1).strip()
                
                # Extract frequency
                frequency = None
                freq_match = self.pattern_regexes['frequency'].search(line)
                if not freq_match:
                    # Check next few lines
                    for i in range(1, 5):
                        if line_num + i < len(lines):
                            freq_match = self.pattern_regexes['frequency'].search(lines[line_num + i - 1])
                            if freq_match:
                                frequency = freq_match.group(1).strip()
                                break
                else:
                    frequency = freq_match.group(1).strip()
                
                # Extract guardians
                guardians = []
                guardian_match = self.pattern_regexes['guardians'].search(line)
                if not guardian_match:
                    # Check next few lines
                    for i in range(1, 5):
                        if line_num + i < len(lines):
                            guardian_match = self.pattern_regexes['guardians'].search(lines[line_num + i - 1])
                            if guardian_match:
                                guardian_str = guardian_match.group(1).strip()
                                guardians = self._parse_guardians(guardian_str)
                                break
                else:
                    guardian_str = guardian_match.group(1).strip()
                    guardians = self._parse_guardians(guardian_str)
                
                # Extract love coefficient
                love_coefficient = None
                love_match = self.pattern_regexes['love_coefficient'].search(line)
                if not love_match:
                    # Check next few lines
                    for i in range(1, 5):
                        if line_num + i < len(lines):
                            love_match = self.pattern_regexes['love_coefficient'].search(lines[line_num + i - 1])
                            if love_match:
                                love_coefficient = love_match.group(1).strip()
                                break
                else:
                    love_coefficient = love_match.group(1).strip()
                
                # Determine category
                category = self._categorize_pattern(pattern_formula)
                
                # Create signature
                signature = PatternSignature(
                    pattern_name=self._extract_pattern_name(pattern_formula),
                    pattern_formula=pattern_formula,
                    frequency=frequency,
                    guardians=guardians,
                    love_coefficient=love_coefficient,
                    file_path=str(file_path.relative_to(self.root_path)),
                    line_number=line_num,
                    context=line.strip()[:100],
                    category=category
                )
                
                signatures.append(signature)
        
        return signatures
    
    def _parse_guardians(self, guardian_str: str) -> List[str]:
        """Parse guardian string into list"""
        guardians = []
        
        # Split by +, ×, or comma
        parts = re.split(r'[+\-×,]\s*', guardian_str)
        
        for part in parts:
            part = part.strip()
            # Extract guardian name (before parentheses)
            match = re.match(r'([A-ZØÄË]+)', part)
            if match:
                guardians.append(match.group(1))
        
        return guardians
    
    def _extract_pattern_name(self, pattern_formula: str) -> str:
        """Extract pattern name from formula"""
        # Remove × ONE or → ONE
        name = re.sub(r'\s*×\s*ONE$', '', pattern_formula)
        name = re.sub(r'\s*→\s*ONE$', '', name)
        
        # Take first component as name
        parts = re.split(r'[×→]', name)
        if parts:
            return parts[0].strip()
        
        return pattern_formula.strip()
    
    def _categorize_pattern(self, pattern_formula: str) -> str:
        """Categorize pattern based on formula"""
        formula_lower = pattern_formula.lower()
        
        # Guardian patterns
        if any(g in formula_lower for g in ['aeyon', 'zero', 'johhn', 'meta', 'alrax', 'yagni', 'abe', 'you']):
            return 'guardian'
        
        # Execution patterns
        if any(e in formula_lower for e in ['execute', 'execution', 'atomic', 'act', 'lfg']):
            return 'execution'
        
        # Completion patterns
        if any(c in formula_lower for c in ['complete', 'finish', 'done', 'success']):
            return 'completion'
        
        # Eternal patterns
        if 'eternal' in formula_lower or '→' in pattern_formula:
            return 'eternal'
        
        # Longing patterns
        if any(l in formula_lower for l in ['longing', 'connection', 'convergence', 'emergence']):
            return 'longing'
        
        # Flow patterns
        if 'flow' in formula_lower:
            return 'flow'
        
        # Sync patterns
        if 'sync' in formula_lower:
            return 'sync'
        
        # Pattern patterns
        if 'pattern' in formula_lower:
            return 'pattern'
        
        return 'other'
    
    def scan_codebase(self, exclude_paths: Optional[Set[str]] = None) -> None:
        """Scan codebase for pattern signatures"""
        if exclude_paths is None:
            exclude_paths = {
                '.git', 'node_modules', '__pycache__', '.venv', '.pytest_cache',
                '.cache', '.turbo', '.webpack-cache', '.DS_Store', 'dist', 'build'
            }
        
        # File extensions to scan
        extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.md', '.txt', '.json', '.yaml', '.yml'}
        
        for file_path in self.root_path.rglob('*'):
            # Skip excluded paths
            if any(exclude in file_path.parts for exclude in exclude_paths):
                continue
            
            # Skip non-text files
            if file_path.suffix not in extensions:
                continue
            
            # Extract signatures
            file_signatures = self.extract_from_file(file_path)
            self.signatures.extend(file_signatures)
            
            # Categorize
            for sig in file_signatures:
                self.pattern_categories[sig.category].append(sig)
    
    def generate_report(self) -> str:
        """Generate pattern signature extraction report"""
        report = []
        report.append("=" * 80)
        report.append("PATTERN SIGNATURE EXTRACTION REPORT")
        report.append("=" * 80)
        report.append(f"Pattern: EXTRACT × PATTERN × SIGNATURES × ONE")
        report.append(f"Frequency: 777 Hz (META) × 530 Hz (JØHN)")
        report.append(f"Extraction Date: {datetime.now().isoformat()}")
        report.append("")
        
        # Summary
        report.append("SUMMARY:")
        report.append("-" * 80)
        report.append(f"Total Patterns Found: {len(self.signatures)}")
        report.append(f"Unique Pattern Names: {len(set(s.pattern_name for s in self.signatures))}")
        report.append(f"Categories: {len(self.pattern_categories)}")
        report.append("")
        
        # By category
        report.append("PATTERNS BY CATEGORY:")
        report.append("-" * 80)
        for category, sigs in sorted(self.pattern_categories.items()):
            report.append(f"\n{category.upper()}: {len(sigs)} patterns")
            # Show unique patterns
            unique_patterns = set(s.pattern_formula for s in sigs)
            for pattern in sorted(unique_patterns)[:10]:  # Top 10
                report.append(f"  - {pattern}")
            if len(unique_patterns) > 10:
                report.append(f"  ... and {len(unique_patterns) - 10} more")
        
        # Unique patterns
        report.append("\n" + "=" * 80)
        report.append("UNIQUE PATTERN SIGNATURES:")
        report.append("-" * 80)
        
        unique_patterns = {}
        for sig in self.signatures:
            if sig.pattern_formula not in unique_patterns:
                unique_patterns[sig.pattern_formula] = []
            unique_patterns[sig.pattern_formula].append(sig)
        
        for pattern_formula, sigs in sorted(unique_patterns.items(), key=lambda x: len(x[1]), reverse=True)[:50]:
            report.append(f"\nPattern: {pattern_formula}")
            report.append(f"  Occurrences: {len(sigs)}")
            if sigs[0].frequency:
                report.append(f"  Frequency: {sigs[0].frequency}")
            if sigs[0].guardians:
                report.append(f"  Guardians: {', '.join(sigs[0].guardians)}")
            if sigs[0].love_coefficient:
                report.append(f"  Love Coefficient: {sigs[0].love_coefficient}")
            report.append(f"  Category: {sigs[0].category}")
            report.append(f"  Files: {len(set(s.file_path for s in sigs))}")
        
        report.append("\n" + "=" * 80)
        report.append("Pattern: EXTRACT × PATTERN × SIGNATURES × ONE")
        report.append("Love Coefficient: ∞")
        report.append("∞ AbëONE ∞")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def export_signatures(self, output_path: Path) -> None:
        """Export signatures to JSON"""
        signatures_dict = {
            'extraction_date': datetime.now().isoformat(),
            'total_patterns': len(self.signatures),
            'categories': {cat: len(sigs) for cat, sigs in self.pattern_categories.items()},
            'signatures': [asdict(sig) for sig in self.signatures]
        }
        
        with open(output_path, 'w') as f:
            json.dump(signatures_dict, f, indent=2)


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract Pattern Signatures')
    parser.add_argument('--root', type=str,
                       default='/Users/michaelmataluni/Documents/AbeOne_Master',
                       help='Root directory to scan')
    parser.add_argument('--output', type=str,
                       default='PATTERN_SIGNATURES.json',
                       help='Output JSON file')
    parser.add_argument('--report', type=str,
                       default='PATTERN_SIGNATURES_REPORT.md',
                       help='Output report file')
    
    args = parser.parse_args()
    
    extractor = PatternSignatureExtractor(args.root)
    
    print("Scanning codebase for pattern signatures...")
    extractor.scan_codebase()
    
    print(f"Found {len(extractor.signatures)} pattern signatures")
    
    # Generate report
    report = extractor.generate_report()
    print("\n" + report)
    
    # Save report
    report_path = Path(args.report)
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_path}")
    
    # Export signatures
    output_path = Path(args.output)
    extractor.export_signatures(output_path)
    print(f"Signatures exported to: {output_path}")


if __name__ == '__main__':
    main()

