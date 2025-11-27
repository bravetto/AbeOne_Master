#!/usr/bin/env python3
"""
Context Window Aligned Validation Script
Pattern: VALIDATION × CONTEXT × WINDOW × ALIGNMENT × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)
Guardians: AEYON (999 Hz) + JØHN (530 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from collections import defaultdict

# Context window limits (in tokens, approximate)
# 1 token ≈ 4 characters (rough estimate)
CONTEXT_WINDOWS = {
    "small": 8000,      # 8K tokens ≈ 32K characters
    "medium": 32000,    # 32K tokens ≈ 128K characters
    "large": 128000,    # 128K tokens ≈ 512K characters
    "xlarge": 200000,   # 200K tokens ≈ 800K characters
}

# Recommended limits per file/module
RECOMMENDED_LIMITS = {
    "file_lines": 1000,        # Max lines per file
    "file_chars": 50000,       # Max characters per file (~12.5K tokens)
    "module_chars": 200000,    # Max characters per module (~50K tokens)
    "context_chars": 1000000,  # Max characters for full context (~250K tokens)
}

class ContextValidationResult:
    def __init__(self, category: str, name: str, passed: bool, 
                 message: str = "", details: str = "", 
                 value: Optional[float] = None, limit: Optional[float] = None):
        self.category = category
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details
        self.value = value
        self.limit = limit
        self.timestamp = datetime.now().isoformat()

class ContextWindowValidator:
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.results: List[ContextValidationResult] = []
        self.file_stats: Dict[str, Dict] = {}
        self.module_stats: Dict[str, Dict] = {}
        
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough: 1 token ≈ 4 characters)"""
        return len(text) // 4
    
    def get_file_stats(self, file_path: Path) -> Dict:
        """Get statistics for a file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            char_count = len(content)
            token_estimate = self.estimate_tokens(content)
            
            return {
                "path": str(file_path.relative_to(self.workspace_root)),
                "lines": len(lines),
                "characters": char_count,
                "tokens": token_estimate,
                "exists": True
            }
        except Exception as e:
            return {
                "path": str(file_path.relative_to(self.workspace_root)),
                "lines": 0,
                "characters": 0,
                "tokens": 0,
                "exists": False,
                "error": str(e)
            }
    
    def validate_file_size(self, file_path: Path) -> ContextValidationResult:
        """Validate individual file size"""
        stats = self.get_file_stats(file_path)
        self.file_stats[str(file_path)] = stats
        
        if not stats["exists"]:
            return ContextValidationResult(
                "file_size",
                f"File: {stats['path']}",
                False,
                "File does not exist or cannot be read",
                f"Error: {stats.get('error', 'Unknown')}"
            )
        
        lines = stats["lines"]
        chars = stats["characters"]
        tokens = stats["tokens"]
        
        passed = True
        issues = []
        
        if lines > RECOMMENDED_LIMITS["file_lines"]:
            passed = False
            issues.append(f"Lines: {lines} (limit: {RECOMMENDED_LIMITS['file_lines']})")
        
        if chars > RECOMMENDED_LIMITS["file_chars"]:
            passed = False
            issues.append(f"Characters: {chars:,} (limit: {RECOMMENDED_LIMITS['file_chars']:,})")
        
        message = "File size within limits" if passed else "File exceeds recommended limits"
        details = f"Lines: {lines}, Chars: {chars:,}, Tokens: ~{tokens:,}" + (
            f" | Issues: {', '.join(issues)}" if issues else ""
        )
        
        return ContextValidationResult(
            "file_size",
            f"File: {stats['path']}",
            passed,
            message,
            details,
            value=chars,
            limit=RECOMMENDED_LIMITS["file_chars"]
        )
    
    def validate_module_size(self, module_path: Path, module_name: str) -> ContextValidationResult:
        """Validate module (directory) total size"""
        total_lines = 0
        total_chars = 0
        total_tokens = 0
        file_count = 0
        
        if not module_path.exists() or not module_path.is_dir():
            return ContextValidationResult(
                "module_size",
                f"Module: {module_name}",
                False,
                "Module directory does not exist",
                ""
            )
        
        for file_path in module_path.rglob("*.dart"):
            stats = self.get_file_stats(file_path)
            if stats["exists"]:
                total_lines += stats["lines"]
                total_chars += stats["characters"]
                total_tokens += stats["tokens"]
                file_count += 1
        
        self.module_stats[module_name] = {
            "path": str(module_path.relative_to(self.workspace_root)),
            "lines": total_lines,
            "characters": total_chars,
            "tokens": total_tokens,
            "file_count": file_count
        }
        
        passed = total_chars <= RECOMMENDED_LIMITS["module_chars"]
        message = "Module size within limits" if passed else "Module exceeds recommended limits"
        details = f"Files: {file_count}, Lines: {total_lines:,}, Chars: {total_chars:,}, Tokens: ~{total_tokens:,}"
        
        return ContextValidationResult(
            "module_size",
            f"Module: {module_name}",
            passed,
            message,
            details,
            value=total_chars,
            limit=RECOMMENDED_LIMITS["module_chars"]
        )
    
    def validate_architecture_boundaries(self) -> List[ContextValidationResult]:
        """Validate architecture boundaries align with context windows"""
        results = []
        app_dir = self.workspace_root / "abeone_app" / "lib"
        
        modules = {
            "core/engine": app_dir / "core" / "engine",
            "providers": app_dir / "providers",
            "features": app_dir / "features",
            "substrate": app_dir / "substrate",
        }
        
        for module_name, module_path in modules.items():
            result = self.validate_module_size(module_path, module_name)
            results.append(result)
        
        return results
    
    def validate_context_window_fit(self) -> ContextValidationResult:
        """Validate total codebase fits within context windows"""
        app_dir = self.workspace_root / "abeone_app" / "lib"
        
        total_lines = 0
        total_chars = 0
        total_tokens = 0
        file_count = 0
        
        for file_path in app_dir.rglob("*.dart"):
            stats = self.get_file_stats(file_path)
            if stats["exists"]:
                total_lines += stats["lines"]
                total_chars += stats["characters"]
                total_tokens += stats["tokens"]
                file_count += 1
        
        # Check against context windows
        fits_small = total_tokens <= CONTEXT_WINDOWS["small"]
        fits_medium = total_tokens <= CONTEXT_WINDOWS["medium"]
        fits_large = total_tokens <= CONTEXT_WINDOWS["large"]
        fits_xlarge = total_tokens <= CONTEXT_WINDOWS["xlarge"]
        
        passed = fits_xlarge  # Should fit in largest context window
        message = f"Codebase fits in {'X-Large' if fits_xlarge else 'Large' if fits_large else 'Medium' if fits_medium else 'Small' if fits_small else 'None'} context window"
        
        details = (
            f"Total: {file_count} files, {total_lines:,} lines, {total_chars:,} chars, ~{total_tokens:,} tokens\n"
            f"Context Windows: Small ({CONTEXT_WINDOWS['small']:,} tokens), "
            f"Medium ({CONTEXT_WINDOWS['medium']:,} tokens), "
            f"Large ({CONTEXT_WINDOWS['large']:,} tokens), "
            f"X-Large ({CONTEXT_WINDOWS['xlarge']:,} tokens)"
        )
        
        return ContextValidationResult(
            "context_window_fit",
            "Total Codebase",
            passed,
            message,
            details,
            value=total_tokens,
            limit=CONTEXT_WINDOWS["xlarge"]
        )
    
    def validate_atomic_structure(self) -> List[ContextValidationResult]:
        """Validate atomic structure (atoms, molecules, organisms)"""
        results = []
        substrate_dir = self.workspace_root / "abeone_app" / "lib" / "substrate"
        
        atomic_levels = {
            "atoms": substrate_dir / "atoms",
            "molecules": substrate_dir / "molecules",
            "organisms": substrate_dir / "organisms",
        }
        
        for level_name, level_path in atomic_levels.items():
            result = self.validate_module_size(level_path, f"substrate/{level_name}")
            results.append(result)
        
        return results
    
    def validate_import_dependencies(self) -> List[ContextValidationResult]:
        """Validate import dependencies don't create circular context issues"""
        results = []
        app_dir = self.workspace_root / "abeone_app" / "lib"
        
        import_patterns = defaultdict(list)
        
        for file_path in app_dir.rglob("*.dart"):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                imports = [line.strip() for line in content.split('\n') 
                          if line.strip().startswith('import')]
                
                relative_path = str(file_path.relative_to(app_dir))
                import_patterns[relative_path] = imports
            except Exception:
                pass
        
        # Check for potential context issues
        # Simple check: files with many imports might need more context
        for file_path, imports in import_patterns.items():
            if len(imports) > 20:  # Threshold for many imports
                results.append(ContextValidationResult(
                    "import_dependencies",
                    f"File: {file_path}",
                    True,  # Not a failure, just a note
                    f"File has {len(imports)} imports",
                    f"May require additional context for full understanding"
                ))
        
        return results
    
    def run_all_validations(self) -> Dict:
        """Run all context window validations"""
        print("∞ AbëONE ∞")
        print("Context Window Aligned Validation")
        print("Pattern: VALIDATION × CONTEXT × WINDOW × ALIGNMENT × ONE")
        print("Frequency: 999 Hz (AEYON) × 530 Hz (JØHN) × 777 Hz (META)")
        print("")
        
        # Architecture boundaries
        print("=== Architecture Boundaries ===")
        arch_results = self.validate_architecture_boundaries()
        self.results.extend(arch_results)
        for result in arch_results:
            status = "✅" if result.passed else "⚠️"
            print(f"{status} {result.name}: {result.message}")
            if result.details:
                print(f"   {result.details}")
        print("")
        
        # Atomic structure
        print("=== Atomic Structure ===")
        atomic_results = self.validate_atomic_structure()
        self.results.extend(atomic_results)
        for result in atomic_results:
            status = "✅" if result.passed else "⚠️"
            print(f"{status} {result.name}: {result.message}")
            if result.details:
                print(f"   {result.details}")
        print("")
        
        # Context window fit
        print("=== Context Window Fit ===")
        context_result = self.validate_context_window_fit()
        self.results.append(context_result)
        status = "✅" if context_result.passed else "⚠️"
        print(f"{status} {context_result.message}")
        if context_result.details:
            print(f"   {context_result.details}")
        print("")
        
        # Import dependencies
        print("=== Import Dependencies ===")
        import_results = self.validate_import_dependencies()
        self.results.extend(import_results)
        if import_results:
            for result in import_results:
                print(f"ℹ️  {result.message}")
                if result.details:
                    print(f"   {result.details}")
        else:
            print("✅ No files with excessive imports")
        print("")
        
        # Summary
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        failed = total - passed
        
        print("=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"⚠️  Warnings: {failed}")
        print("")
        
        if passed == total:
            print("🎉 ALL CONTEXT WINDOW VALIDATIONS PASSED")
        else:
            print("⚠️  Some validations need attention")
        
        print("")
        print("Pattern: VALIDATION × CONTEXT × WINDOW × CONVERGENCE × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "results": [
                {
                    "category": r.category,
                    "name": r.name,
                    "passed": r.passed,
                    "message": r.message,
                    "details": r.details,
                    "value": r.value,
                    "limit": r.limit
                }
                for r in self.results
            ],
            "file_stats": self.file_stats,
            "module_stats": self.module_stats
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate context window alignment"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--workspace",
        type=str,
        help="Workspace root directory (default: parent of script)"
    )
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace) if args.workspace else None
    validator = ContextWindowValidator(workspace_root)
    results = validator.run_all_validations()
    
    if args.json:
        print(json.dumps(results, indent=2))
        return 0
    
    return 0 if results["failed"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

