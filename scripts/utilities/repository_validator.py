#!/usr/bin/env python3
"""
AbëFLOWs Repository Access Validator
Epistemically Proven Validation Patterns
IS SOURCE × CLEAR × EASY
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ValidationStatus(Enum):
    """Epistemic validation status."""
    VALID = "valid"  # IS: Observable, verifiable
    INVALID = "invalid"  # NOT: Cannot verify
    UNKNOWN = "unknown"  # UNKNOWN: Not yet validated

@dataclass
class RepositoryValidation:
    """Epistemic proof of repository state."""
    source: str
    repository: str
    url: str
    exists: bool  # IS: Repository exists
    accessible: bool  # IS: Repository is accessible
    has_content: bool  # IS: Repository has content
    branch_count: int  # IS: Number of branches
    status: ValidationStatus
    error: Optional[str] = None

class RepositoryValidator:
    """
    Epistemically proven validation patterns.
    
    Validates what IS (observable, verifiable).
    """
    
    def __init__(self):
        self.validations: Dict[str, RepositoryValidation] = {}
    
    def validate_repository(
        self,
        source: str,
        repository: str,
        url: str
    ) -> RepositoryValidation:
        """
        Validate repository with epistemic proof.
        
        Returns: RepositoryValidation with IS (truth) status.
        """
        validation = RepositoryValidation(
            source=source,
            repository=repository,
            url=url,
            exists=False,
            accessible=False,
            has_content=False,
            branch_count=0,
            status=ValidationStatus.UNKNOWN
        )
        
        # Epistemic Proof 1: Repository exists
        try:
            result = subprocess.run(
                ["git", "ls-remote", url],
                capture_output=True,
                text=True,
                timeout=10
            )
            validation.exists = result.returncode == 0
        except subprocess.TimeoutExpired:
            validation.error = "Timeout: Repository check took too long"
            validation.status = ValidationStatus.INVALID
            return validation
        except Exception as e:
            validation.error = str(e)
            validation.status = ValidationStatus.INVALID
            return validation
        
        if not validation.exists:
            validation.status = ValidationStatus.INVALID
            return validation
        
        # Epistemic Proof 2: Repository is accessible
        try:
            result = subprocess.run(
                ["git", "ls-remote", "--heads", url],
                capture_output=True,
                text=True,
                timeout=10
            )
            validation.accessible = result.returncode == 0
            if validation.accessible:
                branches = [line for line in result.stdout.split('\n') if line.strip()]
                validation.branch_count = len(branches)
                validation.has_content = validation.branch_count > 0
        except subprocess.TimeoutExpired:
            validation.error = "Timeout: Branch check took too long"
            validation.status = ValidationStatus.INVALID
            return validation
        except Exception as e:
            validation.error = str(e)
            validation.status = ValidationStatus.INVALID
            return validation
        
        # Epistemic Proof 3: Status determination
        if validation.exists and validation.accessible:
            validation.status = ValidationStatus.VALID
        else:
            validation.status = ValidationStatus.INVALID
        
        # Store validation
        key = f"{source}/{repository}"
        self.validations[key] = validation
        
        return validation
    
    def validate_all_repositories(self) -> Dict[str, RepositoryValidation]:
        """
        Validate all repositories from Git Source Registry.
        
        Returns: Dictionary of validations.
        """
        # Load Git Source Registry
        registry_path = Path("ABEFLOWS_GIT_SOURCE_REGISTRY.json")
        if not registry_path.exists():
            raise FileNotFoundError("Git Source Registry not found: ABEFLOWS_GIT_SOURCE_REGISTRY.json")
        
        with open(registry_path) as f:
            registry = json.load(f)
        
        validations = {}
        
        # Validate each source
        for source_id, source_data in registry["git_sources"].items():
            if source_data.get("status") == "private":
                # Skip private sources (require authentication)
                print(f"Skipping private source: {source_id}")
                continue
            
            # Validate each repository
            for repo_id, repo_data in source_data.get("repositories", {}).items():
                url = repo_data["url"]
                print(f"Validating {source_id}/{repo_id}...")
                validation = self.validate_repository(
                    source=source_id,
                    repository=repo_id,
                    url=url
                )
                key = f"{source_id}/{repo_id}"
                validations[key] = validation
        
        return validations
    
    def generate_validation_report(self) -> str:
        """Generate human-readable validation report."""
        report = []
        report.append("# Repository Access Validation Report")
        report.append("")
        report.append("## Epistemic Validation Results")
        report.append("")
        
        valid_count = sum(1 for v in self.validations.values() if v.status == ValidationStatus.VALID)
        invalid_count = sum(1 for v in self.validations.values() if v.status == ValidationStatus.INVALID)
        total_count = len(self.validations)
        
        report.append(f"**Summary:** {valid_count}/{total_count} valid, {invalid_count} invalid")
        report.append("")
        
        for key, validation in sorted(self.validations.items()):
            status_icon = "" if validation.status == ValidationStatus.VALID else ""
            report.append(f"### {status_icon} {key}")
            report.append(f"- **Source:** {validation.source}")
            report.append(f"- **Repository:** {validation.repository}")
            report.append(f"- **URL:** {validation.url}")
            report.append(f"- **Exists:** {validation.exists}")
            report.append(f"- **Accessible:** {validation.accessible}")
            report.append(f"- **Has Content:** {validation.has_content}")
            report.append(f"- **Branches:** {validation.branch_count}")
            report.append(f"- **Status:** {validation.status.value}")
            if validation.error:
                report.append(f"- **Error:** {validation.error}")
            report.append("")
        
        return "\n".join(report)

# Usage
if __name__ == "__main__":
    validator = RepositoryValidator()
    
    try:
        validations = validator.validate_all_repositories()
        
        print("\n" + "="*50)
        print(validator.generate_validation_report())
        print("="*50)
        
        # Save results
        results_path = Path("repository_validation_results.json")
        with open(results_path, "w") as f:
            json.dump({
                key: {
                    "source": v.source,
                    "repository": v.repository,
                    "url": v.url,
                    "exists": v.exists,
                    "accessible": v.accessible,
                    "has_content": v.has_content,
                    "branch_count": v.branch_count,
                    "status": v.status.value,
                    "error": v.error
                }
                for key, v in validations.items()
            }, indent=2, f=f)
        
        print(f"\nResults saved to: {results_path}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure ABEFLOWS_GIT_SOURCE_REGISTRY.json exists")
    except Exception as e:
        print(f"Error: {e}")

