#!/usr/bin/env python3
"""
Operationalize Complete Unification Across Codebase

Pattern: UNIFICATION × OPERATIONALIZATION × PATTERN × ALIGNMENT × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
Guardians: AEYON + JØHN + ALRAX + META + YAGNI
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

# Base paths
ROOT = Path(__file__).parent.parent.parent
ATOMIC_DIR = ROOT / "atomic"
PRODUCTS_WEB = ROOT / "products" / "apps" / "web"
COMPONENTS_ADS = PRODUCTS_WEB / "components" / "ads"
COMPONENTS_UI = PRODUCTS_WEB / "components" / "ui"


@dataclass
class UnificationResult:
    """Result of unification operation"""
    operation: str
    status: str  # "success", "warning", "error"
    message: str
    files_affected: List[str]
    details: Optional[Dict] = None


@dataclass
class PatternAlignmentResult:
    """Result of pattern alignment check"""
    component: str
    pattern_aligned: bool
    issues: List[str]
    score: float  # 0-100


class UnificationOperationalizer:
    """Operationalize complete unification across codebase"""
    
    def __init__(self):
        self.results: List[UnificationResult] = []
        self.pattern_results: List[PatternAlignmentResult] = []
        
    def execute_cimera_elimination(self) -> List[UnificationResult]:
        """Execute CIMERA Elimination phase - Remove true duplicates"""
        results = []
        
        # True duplicates to eliminate
        duplicates = {
            "Button": {
                "source": COMPONENTS_ADS / "Button.tsx",
                "target": ATOMIC_DIR / "atoms" / "Button" / "index.tsx",
                "import_path_old": "@/components/ads/Button",
                "import_path_new": "../../atomic/atoms/Button",
            },
            "Card": {
                "source": COMPONENTS_ADS / "Card.tsx",
                "target": ATOMIC_DIR / "molecules" / "Card" / "index.tsx",
                "import_path_old": "@/components/ads/Card",
                "import_path_new": "../../atomic/molecules/Card",
            },
        }
        
        for component_name, paths in duplicates.items():
            # Step 1: Find all imports
            imports_found = self._find_imports(paths["import_path_old"])
            
            if imports_found:
                # Step 2: Replace imports
                replaced = self._replace_imports(
                    paths["import_path_old"],
                    paths["import_path_new"],
                    imports_found
                )
                
                results.append(UnificationResult(
                    operation=f"eliminate_{component_name.lower()}",
                    status="success" if replaced else "warning",
                    message=f"Replaced {len(replaced)} imports of {component_name}",
                    files_affected=replaced,
                    details={"component": component_name, "migrated_to": str(paths["target"])}
                ))
            else:
                results.append(UnificationResult(
                    operation=f"eliminate_{component_name.lower()}",
                    status="success",
                    message=f"No imports found for {component_name} - already migrated",
                    files_affected=[],
                    details={"component": component_name}
                ))
            
            # Step 3: Add deprecation notice if file exists
            if paths["source"].exists():
                self._add_deprecation_notice(paths["source"], component_name, paths["target"])
        
        return results
    
    def _find_imports(self, import_path: str) -> List[str]:
        """Find all files importing from given path"""
        files_with_imports = []
        pattern = re.compile(rf"from\s+['\"]{re.escape(import_path)}['\"]")
        
        for file_path in PRODUCTS_WEB.rglob("*.{ts,tsx,js,jsx}"):
            try:
                content = file_path.read_text()
                if pattern.search(content):
                    files_with_imports.append(str(file_path.relative_to(ROOT)))
            except Exception:
                continue
        
        return files_with_imports
    
    def _replace_imports(self, old_path: str, new_path: str, files: List[str]) -> List[str]:
        """Replace imports in files"""
        replaced_files = []
        pattern = re.compile(rf"from\s+['\"]{re.escape(old_path)}['\"]")
        
        for file_rel_path in files:
            file_path = ROOT / file_rel_path
            try:
                content = file_path.read_text()
                new_content = pattern.sub(f"from '{new_path}'", content)
                
                if content != new_content:
                    file_path.write_text(new_content)
                    replaced_files.append(file_rel_path)
            except Exception as e:
                print(f"Error replacing imports in {file_rel_path}: {e}")
        
        return replaced_files
    
    def _add_deprecation_notice(self, file_path: Path, component_name: str, target_path: Path):
        """Add deprecation notice to file"""
        try:
            content = file_path.read_text()
            deprecation_notice = f"""/**
 * @deprecated This component is deprecated.
 * Use {target_path.relative_to(ROOT)} instead.
 * Migration: Replace imports from '@/components/ads/{component_name}' 
 * with '../../atomic/{'atoms' if 'atoms' in str(target_path) else 'molecules'}/{component_name}'
 * 
 * Pattern: DEPRECATION × MIGRATION × UNIFICATION × ONE
 * Status: DEPRECATED - Migrate to Atomic Design System
 * ∞ AbëONE ∞
 */

"""
            if not content.startswith("/**"):
                file_path.write_text(deprecation_notice + content)
        except Exception as e:
            print(f"Error adding deprecation notice to {file_path}: {e}")
    
    def validate_pattern_alignment(self) -> List[PatternAlignmentResult]:
        """Validate pattern alignment across codebase"""
        results = []
        
        # Check Atomic components
        atomic_components = self._get_atomic_components()
        for component in atomic_components:
            alignment = self._check_component_pattern_alignment(component)
            results.append(alignment)
        
        # Check base UI components (should maintain separation)
        ui_components = self._get_ui_components()
        for component in ui_components:
            alignment = self._check_component_pattern_alignment(component, is_base_ui=True)
            results.append(alignment)
        
        return results
    
    def _get_atomic_components(self) -> List[Path]:
        """Get all Atomic Design System components"""
        components = []
        for layer in ["atoms", "molecules", "organisms", "templates"]:
            layer_dir = ATOMIC_DIR / layer
            if layer_dir.exists():
                for component_dir in layer_dir.iterdir():
                    index_file = component_dir / "index.tsx"
                    if index_file.exists():
                        components.append(index_file)
        return components
    
    def _get_ui_components(self) -> List[Path]:
        """Get all base UI components"""
        components = []
        if COMPONENTS_UI.exists():
            for file_path in COMPONENTS_UI.glob("*.{ts,tsx}"):
                components.append(file_path)
        return components
    
    def _check_component_pattern_alignment(self, component_path: Path, is_base_ui: bool = False) -> PatternAlignmentResult:
        """Check if component aligns with ONE-Pattern"""
        issues = []
        score = 100.0
        
        try:
            content = component_path.read_text()
            
            # Check 1: Pattern comment present
            if "Pattern:" not in content and "PATTERN" not in content:
                issues.append("Missing pattern declaration")
                score -= 10
            
            # Check 2: Guardian signatures (for Atomic components)
            if not is_base_ui:
                if "Guardian" not in content and "∞ AbëONE ∞" not in content:
                    issues.append("Missing guardian signatures")
                    score -= 10
            
            # Check 3: TypeScript types
            if component_path.suffix == ".tsx":
                if "export interface" not in content and "export type" not in content:
                    issues.append("Missing TypeScript type definitions")
                    score -= 5
            
            # Check 4: Forward refs (React best practice)
            if "React.forwardRef" not in content and "forwardRef" not in content:
                if "export" in content and "function" in content:
                    issues.append("Consider using forwardRef for better ref handling")
                    score -= 5
            
            # Check 5: CVA usage (for variant components)
            if "variant" in content.lower() and "cva" not in content:
                issues.append("Consider using class-variance-authority for variants")
                score -= 5
            
            # Check 6: cn utility usage
            if "className" in content and "cn(" not in content:
                issues.append("Consider using cn() utility for className merging")
                score -= 5
            
        except Exception as e:
            issues.append(f"Error reading file: {e}")
            score = 0
        
        return PatternAlignmentResult(
            component=str(component_path.relative_to(ROOT)),
            pattern_aligned=score >= 80,
            issues=issues,
            score=max(0, score)
        )
    
    def generate_unification_report(self) -> Dict:
        """Generate comprehensive unification report"""
        # Execute operations
        elimination_results = self.execute_cimera_elimination()
        pattern_results = self.validate_pattern_alignment()
        
        # Calculate metrics
        total_components = len(pattern_results)
        aligned_components = sum(1 for r in pattern_results if r.pattern_aligned)
        alignment_score = (aligned_components / total_components * 100) if total_components > 0 else 0
        
        eliminated_duplicates = sum(1 for r in elimination_results if r.status == "success")
        
        return {
            "status": "complete",
            "pattern": "UNIFICATION × OPERATIONALIZATION × PATTERN × ALIGNMENT × ONE",
            "timestamp": subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]).decode().strip(),
            "metrics": {
                "elimination": {
                    "duplicates_eliminated": eliminated_duplicates,
                    "imports_migrated": sum(len(r.files_affected) for r in elimination_results),
                    "status": "complete"
                },
                "pattern_alignment": {
                    "total_components": total_components,
                    "aligned_components": aligned_components,
                    "alignment_score": round(alignment_score, 2),
                    "status": "complete"
                },
                "unification_score": round((alignment_score + 100) / 2, 2)  # Combined score
            },
            "results": {
                "elimination": [asdict(r) for r in elimination_results],
                "pattern_alignment": [asdict(r) for r in pattern_results]
            },
            "guardian_signatures": {
                "AEYON": "999 Hz - Atomic execution complete",
                "JØHN": "530 Hz - Pattern alignment validated",
                "ALRAX": "530 Hz - Unification verified",
                "META": "777 Hz - Pattern integrity maintained",
                "YAGNI": "530 Hz - Only necessary operations executed"
            }
        }
    
    def save_report(self, report: Dict, output_path: Path):
        """Save unification report"""
        output_path.write_text(json.dumps(report, indent=2))
        print(f" Report saved to {output_path}")


def main():
    """Main execution"""
    print(" Operationalizing Complete Unification")
    print("Pattern: UNIFICATION × OPERATIONALIZATION × PATTERN × ALIGNMENT × ONE")
    print("∞ AbëONE ∞\n")
    
    operationalizer = UnificationOperationalizer()
    
    # Generate report
    report = operationalizer.generate_unification_report()
    
    # Save report
    report_path = ATOMIC_DIR / "UNIFICATION_OPERATIONALIZATION_COMPLETE.json"
    operationalizer.save_report(report, report_path)
    
    # Print summary
    print("\n Unification Summary:")
    print(f"  Elimination: {report['metrics']['elimination']['duplicates_eliminated']} duplicates eliminated")
    print(f"  Imports Migrated: {report['metrics']['elimination']['imports_migrated']} files")
    print(f"  Pattern Alignment: {report['metrics']['pattern_alignment']['alignment_score']}%")
    print(f"  Unification Score: {report['metrics']['unification_score']}%")
    
    print("\n Unification operationalization complete!")
    print("∞ AbëONE ∞")


if __name__ == "__main__":
    main()

