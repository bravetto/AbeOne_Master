#!/usr/bin/env python3
"""
 WORKFLOW REALITY ANALYSIS 
Analyzes what workflows exist, what's documented, what aligns with reality.

Pattern: REALITY × TRUTH × WORKFLOW × ANALYSIS × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (META) × ∞ Hz (Abë)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set
import yaml

WORKSPACE_ROOT = Path(__file__).parent.parent
WORKFLOWS_DIR = WORKSPACE_ROOT / ".github" / "workflows"
DOCS_DIR = WORKSPACE_ROOT / "docs"


class WorkflowRealityAnalyzer:
    """
    Analyzes workflow reality vs documentation.
    """
    
    def __init__(self):
        self.analysis = {
            "meta": {
                "created": datetime.now().isoformat(),
                "pattern": "REALITY × TRUTH × WORKFLOW × ANALYSIS × ONE",
                "frequency": "999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (META) × ∞ Hz (Abë)",
                "love_coefficient": "∞"
            },
            "workflows": {
                "actual": [],
                "documented": [],
                "running": [],
                "not_running": []
            },
            "reality_alignment": {
                "aligned": [],
                "misaligned": [],
                "unknown": []
            },
            "requires_discovery": [],
            "requires_emergence": [],
            "requires_convergence": []
        }
    
    def analyze(self):
        """Run complete analysis."""
        print(" WORKFLOW REALITY ANALYSIS ")
        print("=" * 60)
        print()
        
        # 1. Find actual workflows
        self.find_actual_workflows()
        
        # 2. Find documented workflows
        self.find_documented_workflows()
        
        # 3. Analyze reality alignment
        self.analyze_reality_alignment()
        
        # 4. Identify what requires discovery/emergence/convergence
        self.identify_requirements()
        
        # 5. Generate report
        self.generate_report()
        
        return self.analysis
    
    def find_actual_workflows(self):
        """Find actual workflows in .github/workflows/."""
        print(" Finding actual workflows...")
        
        if not WORKFLOWS_DIR.exists():
            print("     .github/workflows/ does not exist")
            return
        
        workflows = []
        for workflow_file in WORKFLOWS_DIR.glob("*.yml"):
            workflows.append({
                "name": workflow_file.stem,
                "path": str(workflow_file),
                "exists": True
            })
        
        for workflow_file in WORKFLOWS_DIR.glob("*.yaml"):
            workflows.append({
                "name": workflow_file.stem,
                "path": str(workflow_file),
                "exists": True
            })
        
        self.analysis["workflows"]["actual"] = workflows
        print(f"    Found {len(workflows)} actual workflows")
        print()
    
    def find_documented_workflows(self):
        """Find documented workflows in docs/."""
        print(" Finding documented workflows...")
        
        documented = []
        
        # Search docs for workflow references
        for doc_file in DOCS_DIR.rglob("*.md"):
            try:
                content = doc_file.read_text()
                if "workflow" in content.lower() or "github actions" in content.lower():
                    documented.append({
                        "file": str(doc_file),
                        "mentions_workflows": True
                    })
            except:
                pass
        
        self.analysis["workflows"]["documented"] = documented
        print(f"    Found {len(documented)} documents mentioning workflows")
        print()
    
    def analyze_reality_alignment(self):
        """Analyze what aligns with reality."""
        print(" Analyzing reality alignment...")
        
        actual_names = {w["name"] for w in self.analysis["workflows"]["actual"]}
        
        # Check each workflow
        for workflow in self.analysis["workflows"]["actual"]:
            name = workflow["name"]
            
            # Try to parse workflow to see if it's valid
            workflow_path = Path(workflow["path"])
            try:
                with open(workflow_path, 'r') as f:
                    workflow_content = yaml.safe_load(f)
                
                # Check if workflow has jobs
                has_jobs = "jobs" in workflow_content
                has_runs_on = False
                has_steps = False
                
                if has_jobs:
                    for job_name, job_content in workflow_content.get("jobs", {}).items():
                        if "runs-on" in job_content:
                            has_runs_on = True
                        if "steps" in job_content:
                            has_steps = True
                
                workflow["valid"] = has_jobs and has_runs_on and has_steps
                workflow["has_jobs"] = has_jobs
                workflow["has_runs_on"] = has_runs_on
                workflow["has_steps"] = has_steps
                
                if workflow["valid"]:
                    self.analysis["reality_alignment"]["aligned"].append(name)
                else:
                    self.analysis["reality_alignment"]["misaligned"].append(name)
                    
            except Exception as e:
                workflow["valid"] = False
                workflow["error"] = str(e)
                self.analysis["reality_alignment"]["misaligned"].append(name)
        
        print(f"    Aligned: {len(self.analysis['reality_alignment']['aligned'])}")
        print(f"     Misaligned: {len(self.analysis['reality_alignment']['misaligned'])}")
        print()
    
    def identify_requirements(self):
        """Identify what requires discovery/emergence/convergence."""
        print(" Identifying requirements...")
        
        # What requires DISCOVERY (unknown state)
        self.analysis["requires_discovery"] = [
            "Which workflows are actually running in GitHub",
            "Which workflows are triggered by what events",
            "Which workflows have failed recently",
            "Which workflows are blocked",
            "What the actual execution state is"
        ]
        
        # What requires EMERGENCE (needs to be created)
        self.analysis["requires_emergence"] = [
            "Workflow monitoring system",
            "Workflow execution tracking",
            "Workflow failure alerts",
            "Workflow performance metrics",
            "Integration between workflows and actual systems"
        ]
        
        # What requires CONVERGENCE (needs to be unified)
        self.analysis["requires_convergence"] = [
            "Documentation vs actual workflows",
            "Workflow patterns across satellites",
            "CI/CD pipeline unification",
            "Deployment workflow convergence",
            "Testing workflow convergence"
        ]
        
        print(f"    Discovery: {len(self.analysis['requires_discovery'])} items")
        print(f"    Emergence: {len(self.analysis['requires_emergence'])} items")
        print(f"    Convergence: {len(self.analysis['requires_convergence'])} items")
        print()
    
    def generate_report(self):
        """Generate analysis report."""
        report_file = WORKSPACE_ROOT / ".abeone_memory" / "WORKFLOW_REALITY_ANALYSIS.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.analysis, f, indent=2)
        
        print("=" * 60)
        print(" WORKFLOW REALITY ANALYSIS COMPLETE ")
        print("=" * 60)
        print()
        print("SUMMARY:")
        print(f"  Actual Workflows: {len(self.analysis['workflows']['actual'])}")
        print(f"  Documented: {len(self.analysis['workflows']['documented'])}")
        print(f"  Aligned: {len(self.analysis['reality_alignment']['aligned'])}")
        print(f"  Misaligned: {len(self.analysis['reality_alignment']['misaligned'])}")
        print()
        print("REQUIRES DISCOVERY:")
        for item in self.analysis["requires_discovery"]:
            print(f"  - {item}")
        print()
        print("REQUIRES EMERGENCE:")
        for item in self.analysis["requires_emergence"]:
            print(f"  - {item}")
        print()
        print("REQUIRES CONVERGENCE:")
        for item in self.analysis["requires_convergence"]:
            print(f"  - {item}")
        print()
        print(f"Report: {report_file}")
        print("=" * 60)
        print()
        print("LOVE = LIFE = ONE")
        print("Michael  AbëONE = ∞")
        print("FOREVER AND EVER")
        print("∞ AbëONE ∞")


def main():
    """Main analysis execution."""
    analyzer = WorkflowRealityAnalyzer()
    analysis = analyzer.analyze()
    return analysis


if __name__ == '__main__':
    main()

