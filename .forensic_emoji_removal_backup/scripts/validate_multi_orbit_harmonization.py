#!/usr/bin/env python3
"""
AbëONE Multi-Orbit Workspace Harmonization Validation Script

Validates harmonization across entire multi-orbit workspace:
- Kernel version lock consistency
- Orbit repo compliance
- Adapter contract validation
- Guardian frequency harmonization
- Event bus coherence
- Cross-repo integration

Pattern: VALIDATION × HARMONIZATION × MULTI-ORBIT × ONE
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class ValidationResult:
    """Validation result container."""
    
    def __init__(self, name: str, passed: bool, message: str = "", details: Dict[str, Any] = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or {}


class MultiOrbitHarmonizationValidator:
    """Validates multi-orbit workspace harmonization."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.results: List[ValidationResult] = []
        self.orbit_repos: List[Path] = []
        self.kernel_path: Optional[Path] = None
    
    def validate(self) -> bool:
        """Run all validation checks."""
        print("🛡️  AbëONE Multi-Orbit Workspace Harmonization Validation")
        print("=" * 70)
        print()
        
        # Discover Orbit repos and kernel
        self.discover_components()
        
        # Run all validations
        self.validate_kernel_presence()
        self.validate_kernel_version_lock()
        self.validate_orbit_repos()
        self.validate_adapter_contracts()
        self.validate_guardian_frequencies()
        self.validate_event_bus_coherence()
        self.validate_cross_repo_integration()
        
        # Print results
        self.print_results()
        
        # Return overall status
        return all(r.passed for r in self.results)
    
    def discover_components(self):
        """Discover Orbit repos and kernel in workspace."""
        print("🔍 Discovering components...")
        
        # Look for kernel
        kernel_candidates = [
            self.project_root / "abëone",
            self.project_root / "abëone" / "ONE_KERNEL.py",
        ]
        
        for candidate in kernel_candidates:
            if candidate.exists():
                if candidate.is_file():
                    self.kernel_path = candidate.parent
                else:
                    self.kernel_path = candidate
                print(f"  ✅ Kernel found: {self.kernel_path}")
                break
        
        # Look for Orbit repos (directories with orbit.config.json or module_manifest.json)
        potential_orbit_repos = [
            self.project_root / "AbeTRUICE",
            self.project_root / "AbeBEATs_Clean",
            self.project_root / "AbeBEATs",
        ]
        
        for repo_path in potential_orbit_repos:
            if repo_path.exists() and repo_path.is_dir():
                # Check for Orbit-Spec indicators
                orbit_config = repo_path / "config" / "orbit.config.json"
                manifest = repo_path / "module_manifest.json"
                
                if orbit_config.exists() or manifest.exists():
                    self.orbit_repos.append(repo_path)
                    print(f"  ✅ Orbit repo found: {repo_path.name}")
        
        print(f"  📊 Found {len(self.orbit_repos)} Orbit repo(s)")
        print()
    
    def validate_kernel_presence(self):
        """Validate kernel presence."""
        print("📋 Validating kernel presence...")
        
        all_passed = True
        details = {}
        
        if self.kernel_path and self.kernel_path.exists():
            # Check kernel components
            kernel_files = {
                "ONE_KERNEL.py": self.kernel_path / "ONE_KERNEL.py",
                "EVENT_BUS.py": self.kernel_path / "EVENT_BUS.py",
                "GUARDIANS_REGISTRY.py": self.kernel_path / "GUARDIANS_REGISTRY.py",
                "MODULE_REGISTRY.py": self.kernel_path / "MODULE_REGISTRY.py",
            }
            
            for name, path in kernel_files.items():
                if path.exists():
                    details[name] = "✅ Present"
                    print(f"  ✅ {name} - Present")
                else:
                    all_passed = False
                    details[name] = "❌ MISSING"
                    print(f"  ❌ {name} - Missing")
            
            # Check guardians directory
            guardians_dir = self.kernel_path / "guardians"
            if guardians_dir.exists():
                details["guardians/"] = "✅ Present"
                print(f"  ✅ guardians/ - Present")
            else:
                details["guardians/"] = "⚠️  Missing (optional)"
                print(f"  ⚠️  guardians/ - Missing (optional)")
        else:
            all_passed = False
            details["kernel"] = "❌ NOT FOUND"
            print(f"  ❌ Kernel not found")
        
        self.results.append(ValidationResult(
            "Kernel Presence",
            all_passed,
            "Kernel components present" if all_passed else "Kernel components missing",
            details
        ))
        print()
    
    def validate_kernel_version_lock(self):
        """Validate kernel version lock consistency."""
        print("📋 Validating kernel version lock consistency...")
        
        all_passed = True
        details = {}
        expected_version = "v0.9.0-stable"
        versions_found = set()
        
        # Check kernel version in Orbit repos
        for repo_path in self.orbit_repos:
            repo_name = repo_path.name
            
            # Check orbit.config.json
            orbit_config = repo_path / "config" / "orbit.config.json"
            if orbit_config.exists():
                try:
                    with open(orbit_config) as f:
                        config = json.load(f)
                    kernel_version = config.get("kernelVersion")
                    if kernel_version:
                        versions_found.add(kernel_version)
                        if kernel_version == expected_version:
                            details[f"{repo_name}.orbit.config.json"] = f"✅ {kernel_version}"
                            print(f"  ✅ {repo_name} orbit.config.json: {kernel_version}")
                        else:
                            all_passed = False
                            details[f"{repo_name}.orbit.config.json"] = f"❌ Expected {expected_version}, got {kernel_version}"
                            print(f"  ❌ {repo_name} orbit.config.json: {kernel_version} (Expected {expected_version})")
                except Exception as e:
                    all_passed = False
                    details[f"{repo_name}.orbit.config.json"] = f"❌ FAILED: {e}"
                    print(f"  ❌ {repo_name} orbit.config.json: Invalid")
            
            # Check module_manifest.json
            manifest = repo_path / "module_manifest.json"
            if manifest.exists():
                try:
                    with open(manifest) as f:
                        manifest_data = json.load(f)
                    kernel_version = manifest_data.get("kernelVersion")
                    if kernel_version:
                        versions_found.add(kernel_version)
                        if kernel_version == expected_version:
                            details[f"{repo_name}.module_manifest.json"] = f"✅ {kernel_version}"
                            print(f"  ✅ {repo_name} module_manifest.json: {kernel_version}")
                        else:
                            all_passed = False
                            details[f"{repo_name}.module_manifest.json"] = f"❌ Expected {expected_version}, got {kernel_version}"
                            print(f"  ❌ {repo_name} module_manifest.json: {kernel_version} (Expected {expected_version})")
                except Exception as e:
                    all_passed = False
                    details[f"{repo_name}.module_manifest.json"] = f"❌ FAILED: {e}"
                    print(f"  ❌ {repo_name} module_manifest.json: Invalid")
        
        # Check version consistency
        if len(versions_found) == 1 and expected_version in versions_found:
            details["version_consistency"] = f"✅ All repos use {expected_version}"
            print(f"  ✅ Version consistency: All repos use {expected_version}")
        elif len(versions_found) > 1:
            all_passed = False
            details["version_consistency"] = f"❌ Multiple versions found: {versions_found}"
            print(f"  ❌ Version inconsistency: {versions_found}")
        
        self.results.append(ValidationResult(
            "Kernel Version Lock",
            all_passed,
            f"Kernel version locked at {expected_version}" if all_passed else "Kernel version lock issues",
            details
        ))
        print()
    
    def validate_orbit_repos(self):
        """Validate Orbit repo compliance."""
        print("📋 Validating Orbit repo compliance...")
        
        all_passed = True
        details = {}
        
        required_dirs = ["src", "adapters", "config", "docs", "deploy", "tests"]
        required_files = [
            "config/orbit.config.json",
            "module_manifest.json",
        ]
        
        for repo_path in self.orbit_repos:
            repo_name = repo_path.name
            repo_passed = True
            repo_details = {}
            
            # Check required directories
            for dir_name in required_dirs:
                dir_path = repo_path / dir_name
                if dir_path.exists():
                    repo_details[f"dir.{dir_name}"] = "✅ Present"
                else:
                    repo_passed = False
                    all_passed = False
                    repo_details[f"dir.{dir_name}"] = "❌ MISSING"
            
            # Check required files
            for file_path in required_files:
                full_path = repo_path / file_path
                if full_path.exists():
                    repo_details[f"file.{file_path}"] = "✅ Present"
                else:
                    repo_passed = False
                    all_passed = False
                    repo_details[f"file.{file_path}"] = "❌ MISSING"
            
            details[repo_name] = repo_details
            
            if repo_passed:
                print(f"  ✅ {repo_name} - Orbit-Spec compliant")
            else:
                print(f"  ❌ {repo_name} - Orbit-Spec compliance issues")
        
        self.results.append(ValidationResult(
            "Orbit Repo Compliance",
            all_passed,
            "All Orbit repos compliant" if all_passed else "Orbit repo compliance issues",
            details
        ))
        print()
    
    def validate_adapter_contracts(self):
        """Validate adapter contracts across Orbit repos."""
        print("📋 Validating adapter contracts...")
        
        all_passed = True
        details = {}
        
        required_adapters = [
            "adapter.kernel.py",
            "adapter.guardians.py",
            "adapter.module.py",
            "adapter.bus.py",
        ]
        
        for repo_path in self.orbit_repos:
            repo_name = repo_path.name
            adapters_dir = repo_path / "adapters"
            repo_passed = True
            repo_details = {}
            
            if adapters_dir.exists():
                for adapter_name in required_adapters:
                    adapter_path = adapters_dir / adapter_name
                    if adapter_path.exists():
                        repo_details[adapter_name] = "✅ Present"
                    else:
                        repo_passed = False
                        all_passed = False
                        repo_details[adapter_name] = "❌ MISSING"
            else:
                repo_passed = False
                all_passed = False
                repo_details["adapters/"] = "❌ MISSING"
            
            details[repo_name] = repo_details
            
            if repo_passed:
                print(f"  ✅ {repo_name} - All adapters present")
            else:
                print(f"  ❌ {repo_name} - Adapter issues")
        
        self.results.append(ValidationResult(
            "Adapter Contracts",
            all_passed,
            "All adapters present" if all_passed else "Adapter contract issues",
            details
        ))
        print()
    
    def validate_guardian_frequencies(self):
        """Validate Guardian frequency harmonization."""
        print("📋 Validating Guardian frequency harmonization...")
        
        all_passed = True
        details = {}
        
        expected_frequencies = {
            "AbeTRUICE": 777.0,
            "AbeBEATs_Clean": 530.0,
        }
        
        for repo_path in self.orbit_repos:
            repo_name = repo_path.name
            manifest = repo_path / "module_manifest.json"
            
            if manifest.exists():
                try:
                    with open(manifest) as f:
                        manifest_data = json.load(f)
                    
                    frequency = manifest_data.get("frequency")
                    expected_freq = expected_frequencies.get(repo_name)
                    
                    if expected_freq:
                        if frequency == expected_freq:
                            details[f"{repo_name}.frequency"] = f"✅ {frequency} Hz"
                            print(f"  ✅ {repo_name} frequency: {frequency} Hz")
                        else:
                            all_passed = False
                            details[f"{repo_name}.frequency"] = f"❌ Expected {expected_freq} Hz, got {frequency}"
                            print(f"  ❌ {repo_name} frequency: {frequency} Hz (Expected {expected_freq} Hz)")
                    else:
                        details[f"{repo_name}.frequency"] = f"⚠️  {frequency} Hz (no expected value)"
                        print(f"  ⚠️  {repo_name} frequency: {frequency} Hz (no expected value)")
                except Exception as e:
                    all_passed = False
                    details[f"{repo_name}.frequency"] = f"❌ FAILED: {e}"
                    print(f"  ❌ {repo_name} frequency validation failed: {e}")
        
        self.results.append(ValidationResult(
            "Guardian Frequency Harmonization",
            all_passed,
            "Guardian frequencies harmonized" if all_passed else "Guardian frequency issues",
            details
        ))
        print()
    
    def validate_event_bus_coherence(self):
        """Validate event bus coherence."""
        print("📋 Validating event bus coherence...")
        
        all_passed = True
        details = {}
        
        for repo_path in self.orbit_repos:
            repo_name = repo_path.name
            manifest = repo_path / "module_manifest.json"
            
            if manifest.exists():
                try:
                    with open(manifest) as f:
                        manifest_data = json.load(f)
                    
                    events = manifest_data.get("events", {})
                    subscribed = events.get("subscribed", [])
                    published = events.get("published", [])
                    
                    if subscribed and published:
                        details[f"{repo_name}.events"] = f"✅ {len(subscribed)} subscribed, {len(published)} published"
                        print(f"  ✅ {repo_name} events: {len(subscribed)} subscribed, {len(published)} published")
                    else:
                        all_passed = False
                        details[f"{repo_name}.events"] = "❌ Missing events"
                        print(f"  ❌ {repo_name} events: Missing")
                except Exception as e:
                    all_passed = False
                    details[f"{repo_name}.events"] = f"❌ FAILED: {e}"
                    print(f"  ❌ {repo_name} event bus validation failed: {e}")
        
        self.results.append(ValidationResult(
            "Event Bus Coherence",
            all_passed,
            "Event bus coherent" if all_passed else "Event bus coherence issues",
            details
        ))
        print()
    
    def validate_cross_repo_integration(self):
        """Validate cross-repo integration."""
        print("📋 Validating cross-repo integration...")
        
        all_passed = True
        details = {}
        
        # Check if multiple Orbit repos exist
        if len(self.orbit_repos) >= 2:
            details["multi_orbit"] = f"✅ {len(self.orbit_repos)} Orbit repos detected"
            print(f"  ✅ Multi-orbit workspace: {len(self.orbit_repos)} Orbit repos")
        else:
            details["multi_orbit"] = "⚠️  Single Orbit repo (multi-orbit not detected)"
            print(f"  ⚠️  Single Orbit repo detected")
        
        # Check kernel submodule references
        for repo_path in self.orbit_repos:
            repo_name = repo_path.name
            kernel_submodule = repo_path / "kernel" / "abeone"
            
            if kernel_submodule.exists():
                details[f"{repo_name}.kernel_submodule"] = "✅ Present"
                print(f"  ✅ {repo_name} kernel submodule: Present")
            else:
                details[f"{repo_name}.kernel_submodule"] = "⚠️  Missing (may require initialization)"
                print(f"  ⚠️  {repo_name} kernel submodule: Missing (may require initialization)")
        
        self.results.append(ValidationResult(
            "Cross-Repo Integration",
            all_passed,
            "Cross-repo integration validated" if all_passed else "Cross-repo integration issues",
            details
        ))
        print()
    
    def print_results(self):
        """Print validation results summary."""
        print("=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)
        print()
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"{status} - {result.name}")
            if result.message:
                print(f"      {result.message}")
            print()
        
        print("=" * 70)
        print(f"Overall: {passed}/{total} checks passed")
        
        if passed == total:
            print("✅ ALL VALIDATIONS PASSED - Multi-orbit workspace harmonized")
        else:
            print(f"❌ {total - passed} VALIDATION(S) FAILED - Review required")
        print("=" * 70)


def main():
    """Main entry point."""
    validator = MultiOrbitHarmonizationValidator()
    success = validator.validate()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

