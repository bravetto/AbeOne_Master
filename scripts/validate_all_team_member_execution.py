#!/usr/bin/env python3
"""
Epistemic Validation: ALL Team Member Execution of ALL Goals

Comprehensive epistemic validation of team member execution against all defined goals.

Pattern: AEYON × EPISTEMIC × VALIDATION × TEAM × EXECUTION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × 777 Hz (ARXON)
Guardians: AEYON (999 Hz) + ARXON (777 Hz) + Abë (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from orbitals.EMERGENT_OS_orbital.emergence_core.epistemic_validator import (
        EpistemicStatus,
        EpistemicPatternValidator
    )
    EPISTEMIC_FRAMEWORK_AVAILABLE = True
except ImportError:
    EPISTEMIC_FRAMEWORK_AVAILABLE = False
    print("  Epistemic framework not available, using simplified validation")


class ExecutionStatus(Enum):
    """Execution status levels."""
    COMPLETE = "complete"  # Goal fully executed with evidence
    IN_PROGRESS = "in_progress"  # Goal partially executed
    NOT_STARTED = "not_started"  # Goal not yet started
    BLOCKED = "blocked"  # Goal blocked by dependencies
    UNKNOWN = "unknown"  # Insufficient evidence


@dataclass
class Goal:
    """Goal definition with epistemic validation."""
    goal_id: str
    title: str
    description: str
    team_member: str
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    source_document: str
    expected_outcomes: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    deadline: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ExecutionEvidence:
    """Evidence of goal execution."""
    evidence_type: str  # CODE, DOCUMENTATION, DEPLOYMENT, TEST, METRIC
    evidence_path: str
    evidence_description: str
    timestamp: Optional[str] = None
    confidence: float = 0.0  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class GoalExecution:
    """Goal execution with epistemic validation."""
    goal: Goal
    execution_status: ExecutionStatus
    epistemic_status: EpistemicStatus
    certainty: float  # 0.0 to 1.0
    evidence: List[ExecutionEvidence] = field(default_factory=list)
    execution_percentage: float = 0.0  # 0.0 to 100.0
    blockers: List[str] = field(default_factory=list)
    validation_timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "goal": self.goal.to_dict(),
            "execution_status": self.execution_status.value,
            "epistemic_status": self.epistemic_status.value if isinstance(self.epistemic_status, EpistemicStatus) else str(self.epistemic_status),
            "certainty": self.certainty,
            "evidence": [e.to_dict() for e in self.evidence],
            "execution_percentage": self.execution_percentage,
            "blockers": self.blockers,
            "validation_timestamp": self.validation_timestamp.isoformat()
        }


class TeamMemberExecutionValidator:
    """
    Comprehensive epistemic validator for ALL team member execution of ALL goals.
    
    Validates:
    1. Goal definitions (epistemic certainty)
    2. Execution evidence (source validation)
    3. Execution status (epistemic classification)
    4. Completion percentage (certainty calculation)
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize validator."""
        self.workspace_root = workspace_root or project_root
        self.team_members = [
            "Danny", "Ben", "Jimmy", "PHANI", "Bryan", "Jacob", "Bill", "Michael"
        ]
        self.goals: List[Goal] = []
        self.executions: List[GoalExecution] = []
        
        if EPISTEMIC_FRAMEWORK_AVAILABLE:
            self.epistemic_validator = EpistemicPatternValidator(min_certainty_threshold=0.5)
        else:
            self.epistemic_validator = None
    
    def discover_all_goals(self) -> List[Goal]:
        """Discover all goals from codebase."""
        print(" Discovering all goals...")
        print("-" * 80)
        
        goals = []
        
        # Danny's Goals (from BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md and DANNY_REQUIREMENTS_COMPLETE_ANALYSIS.md)
        goals.extend([
            Goal(
                goal_id="DANNY-001",
                title="AWS Infrastructure Production Deployment",
                description="Deploy production-ready AWS infrastructure with EKS clusters, ECR registry, Linkerd service mesh",
                team_member="Danny",
                priority="CRITICAL",
                source_document="BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md",
                expected_outcomes=[
                    "EKS clusters running (dev/prod)",
                    "ECR registry operational",
                    "Linkerd service mesh deployed",
                    "IRSA authentication configured"
                ],
                success_criteria=[
                    "All guard services running on EKS",
                    "Container registry accessible",
                    "Service mesh operational"
                ]
            ),
            Goal(
                goal_id="DANNY-002",
                title="CI/CD Automation Pipeline",
                description="Implement GitHub Actions workflows with security checks and automated deployment",
                team_member="Danny",
                priority="HIGH",
                source_document="DANNY_REQUIREMENTS_COMPLETE_ANALYSIS.md",
                expected_outcomes=[
                    "GitHub Actions workflows operational",
                    "Pre-commit hooks configured",
                    "Code scanning automated",
                    "Security checks integrated"
                ],
                success_criteria=[
                    "Workflows pass validation",
                    "Automated deployments working",
                    "Security checks passing"
                ]
            ),
            Goal(
                goal_id="DANNY-003",
                title="Security Foundation Implementation",
                description="Implement security-first infrastructure with IAM roles, MFA, least privilege",
                team_member="Danny",
                priority="CRITICAL",
                source_document="DANNY_REQUIREMENTS_COMPLETE_ANALYSIS.md",
                expected_outcomes=[
                    "Google Workspace MFA enabled",
                    "IAM roles configured (not users)",
                    "Least privilege security model",
                    "Secure GitHub/Slack apps"
                ],
                success_criteria=[
                    "MFA enforced",
                    "No IAM users, only roles",
                    "Security model validated"
                ]
            ),
        ])
        
        # Ben's Goals
        goals.extend([
            Goal(
                goal_id="BEN-001",
                title="Unified API Gateway Implementation",
                description="Build scalable FastAPI gateway with 149-agent swarm orchestration",
                team_member="Ben",
                priority="CRITICAL",
                source_document="BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md",
                expected_outcomes=[
                    "Unified API gateway operational",
                    "149-agent swarm system running",
                    "Service orchestration with circuit breakers",
                    "Rate limiting and health monitoring"
                ],
                success_criteria=[
                    "Gateway handles all guard services",
                    "Swarm orchestration functional",
                    "Circuit breakers operational"
                ]
            ),
            Goal(
                goal_id="BEN-002",
                title="Service Orchestration System",
                description="Implement service orchestration with circuit breakers, timeouts, retries",
                team_member="Ben",
                priority="HIGH",
                source_document="BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md",
                expected_outcomes=[
                    "Circuit breakers implemented",
                    "Timeout handling configured",
                    "Retry logic operational",
                    "Health monitoring active"
                ],
                success_criteria=[
                    "Services resilient to failures",
                    "Health checks passing",
                    "Orchestration validated"
                ]
            ),
        ])
        
        # Jimmy's Goals
        goals.extend([
            Goal(
                goal_id="JIMMY-001",
                title="NeuroForge Neuromorphic Intelligence",
                description="Deploy neuromorphic RAG system with neural codemaps and safety layers",
                team_member="Jimmy",
                priority="CRITICAL",
                source_document="BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md",
                expected_outcomes=[
                    "Neural AST Builder operational",
                    "Enhanced Neuromorphic RAG deployed",
                    "Neuronal Codemap Processor running",
                    "Safety layers (1213 lines) implemented"
                ],
                success_criteria=[
                    "Neuromorphic processing functional",
                    "Neural codemaps generated",
                    "Safety layers validated"
                ]
            ),
            Goal(
                goal_id="JIMMY-002",
                title="Spike-BERT Integration",
                description="Integrate Spike-BERT hybrid neuromorphic + transformer architecture",
                team_member="Jimmy",
                priority="HIGH",
                source_document="BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md",
                expected_outcomes=[
                    "Spike-BERT integrated",
                    "Hybrid processing operational",
                    "Research-backed implementation"
                ],
                success_criteria=[
                    "Integration validated",
                    "Performance metrics met",
                    "Research compliance verified"
                ]
            ),
        ])
        
        # PHANI's Goals
        goals.extend([
            Goal(
                goal_id="PHANI-001",
                title="Unified Health Monitoring System",
                description="Implement comprehensive health monitoring with Prometheus metrics and Kubernetes probes",
                team_member="PHANI",
                priority="HIGH",
                source_document="BRAVETTO_TEAM_CONVERGENCE_ANALYSIS.md",
                expected_outcomes=[
                    "Unified health monitor operational",
                    "System resource monitoring active",
                    "Dependency validation implemented",
                    "Prometheus metrics exposed",
                    "Kubernetes health probes configured"
                ],
                success_criteria=[
                    "All services monitored",
                    "Metrics accessible",
                    "Health probes functional"
                ]
            ),
        ])
        
        # Bryan's Goals
        goals.extend([
            Goal(
                goal_id="BRYAN-001",
                title="Digital Marketing Automation",
                description="Build comprehensive automation for SEO, Google Ads, Social Media, Content, Email",
                team_member="Bryan",
                priority="MEDIUM",
                source_document="google-ads-automation/PROJECT_SUMMARY.md",
                expected_outcomes=[
                    "Multi-channel automation operational",
                    "Lead quality improvement",
                    "Analytics & attribution implemented"
                ],
                success_criteria=[
                    "20-30% CPA reduction",
                    "20-30% ROAS improvement",
                    "15-25% conversion rate increase"
                ]
            ),
        ])
        
        # Michael's Goals (from collaboration documents)
        goals.extend([
            Goal(
                goal_id="MICHAEL-001",
                title="Human-Centric Collaboration System",
                description="Implement Michael-AEYON collaboration workflow with 5 validation gates",
                team_member="Michael",
                priority="CRITICAL",
                source_document="AEYON_MICHAEL_HUMAN_CENTRIC_COLLABORATION_NEXT_STEPS.md",
                expected_outcomes=[
                    "Collaboration workflow operational",
                    "5 validation gates implemented",
                    "Feedback loops active",
                    "Collaboration metrics tracked"
                ],
                success_criteria=[
                    "Workflow validated",
                    "Gates functional",
                    "Metrics collected"
                ]
            ),
        ])
        
        print(f" Discovered {len(goals)} goals across {len(set(g.team_member for g in goals))} team members")
        print()
        
        self.goals = goals
        return goals
    
    def validate_execution_epistemically(self, goal: Goal) -> GoalExecution:
        """
        Validate goal execution with epistemic certainty.
        
        Uses epistemic framework to:
        1. Assess evidence quality
        2. Classify epistemic status
        3. Calculate certainty
        4. Determine execution status
        """
        # Search for evidence
        evidence = self._gather_evidence(goal)
        
        # Assess evidence quality
        evidence_quality = self._assess_evidence_quality(evidence)
        
        # Classify epistemic status
        epistemic_status = self._classify_epistemic_status(evidence_quality, evidence)
        
        # Calculate certainty
        certainty = self._calculate_certainty(evidence_quality, evidence)
        
        # Determine execution status
        execution_status = self._determine_execution_status(evidence, certainty)
        
        # Calculate execution percentage
        execution_percentage = self._calculate_execution_percentage(goal, evidence)
        
        # Identify blockers
        blockers = self._identify_blockers(goal, evidence)
        
        return GoalExecution(
            goal=goal,
            execution_status=execution_status,
            epistemic_status=epistemic_status,
            certainty=certainty,
            evidence=evidence,
            execution_percentage=execution_percentage,
            blockers=blockers
        )
    
    def _gather_evidence(self, goal: Goal) -> List[ExecutionEvidence]:
        """Gather evidence of goal execution."""
        evidence = []
        
        # Search for code evidence
        code_evidence = self._search_code_evidence(goal)
        evidence.extend(code_evidence)
        
        # Search for documentation evidence
        doc_evidence = self._search_documentation_evidence(goal)
        evidence.extend(doc_evidence)
        
        # Search for deployment evidence
        deploy_evidence = self._search_deployment_evidence(goal)
        evidence.extend(deploy_evidence)
        
        # Search for test evidence
        test_evidence = self._search_test_evidence(goal)
        evidence.extend(test_evidence)
        
        return evidence
    
    def _search_code_evidence(self, goal: Goal) -> List[ExecutionEvidence]:
        """Search for code evidence of goal execution."""
        evidence = []
        
        # Map goals to expected code locations
        code_mappings = {
            "DANNY-001": [
                "AIGuards-Backend-orbital/.github/workflows",
                "AIGuards-Backend-orbital/terraform",
                "AIGuards-Backend-orbital/kubernetes"
            ],
            "DANNY-002": [
                ".github/workflows",
                "scripts/validate_danny_workflow_pattern.py"
            ],
            "BEN-001": [
                "AIGuards-Backend-orbital/codeguardians-gateway",
                "AIGuards-Backend-orbital/guards"
            ],
            "JIMMY-001": [
                "orbital/EMERGENT_OS-orbital/neuromorphic_alignment",
                "orbital/EMERGENT_OS-orbital/emergence_core"
            ],
            "PHANI-001": [
                "AIGuards-Backend-orbital/guards/healthguard",
                "AIGuards-Backend-orbital/shared/health_monitoring.py"
            ],
        }
        
        if goal.goal_id in code_mappings:
            for path_pattern in code_mappings[goal.goal_id]:
                path = self.workspace_root / path_pattern
                if path.exists():
                    evidence.append(ExecutionEvidence(
                        evidence_type="CODE",
                        evidence_path=str(path),
                        evidence_description=f"Code found at {path_pattern}",
                        confidence=0.8
                    ))
        
        return evidence
    
    def _search_documentation_evidence(self, goal: Goal) -> List[ExecutionEvidence]:
        """Search for documentation evidence."""
        evidence = []
        
        # Check source document exists
        source_path = self.workspace_root / goal.source_document
        if source_path.exists():
            evidence.append(ExecutionEvidence(
                evidence_type="DOCUMENTATION",
                evidence_path=str(source_path),
                evidence_description=f"Goal documented in {goal.source_document}",
                confidence=0.7
            ))
        
        return evidence
    
    def _search_deployment_evidence(self, goal: Goal) -> List[ExecutionEvidence]:
        """Search for deployment evidence."""
        evidence = []
        
        # Check for deployment-related files
        deployment_indicators = {
            "DANNY-001": ["terraform", "kubernetes", "eks"],
            "BEN-001": ["docker-compose", "kubernetes", "deployment"],
            "PHANI-001": ["prometheus", "kubernetes", "health"]
        }
        
        if goal.goal_id in deployment_indicators:
            for indicator in deployment_indicators[goal.goal_id]:
                # Search for files containing indicator
                for path in self.workspace_root.rglob(f"*{indicator}*"):
                    if path.is_file() and path.suffix in [".yaml", ".yml", ".tf", ".py"]:
                        evidence.append(ExecutionEvidence(
                            evidence_type="DEPLOYMENT",
                            evidence_path=str(path),
                            evidence_description=f"Deployment config found: {path.name}",
                            confidence=0.6
                        ))
                        break
        
        return evidence
    
    def _search_test_evidence(self, goal: Goal) -> List[ExecutionEvidence]:
        """Search for test evidence."""
        evidence = []
        
        # Look for test files related to goal
        test_patterns = {
            "BEN-001": ["test_gateway", "test_orchestration"],
            "JIMMY-001": ["test_neuromorphic", "test_rag"],
            "PHANI-001": ["test_health", "test_monitoring"]
        }
        
        if goal.goal_id in test_patterns:
            for pattern in test_patterns[goal.goal_id]:
                for path in self.workspace_root.rglob(f"*{pattern}*"):
                    if path.is_file() and "test" in path.name.lower():
                        evidence.append(ExecutionEvidence(
                            evidence_type="TEST",
                            evidence_path=str(path),
                            evidence_description=f"Test found: {path.name}",
                            confidence=0.7
                        ))
        
        return evidence
    
    def _assess_evidence_quality(self, evidence: List[ExecutionEvidence]) -> float:
        """Assess overall evidence quality (0.0 to 1.0)."""
        if not evidence:
            return 0.0
        
        # Weight different evidence types
        type_weights = {
            "CODE": 0.4,
            "TEST": 0.3,
            "DEPLOYMENT": 0.2,
            "DOCUMENTATION": 0.1
        }
        
        weighted_sum = sum(
            type_weights.get(e.evidence_type, 0.1) * e.confidence
            for e in evidence
        )
        
        total_weight = sum(type_weights.get(e.evidence_type, 0.1) for e in evidence)
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _classify_epistemic_status(self, evidence_quality: float, evidence: List[ExecutionEvidence]) -> EpistemicStatus:
        """Classify epistemic status based on evidence."""
        if not EPISTEMIC_FRAMEWORK_AVAILABLE:
            # Simplified classification
            if evidence_quality >= 0.9:
                return EpistemicStatus.VALIDATED
            elif evidence_quality >= 0.5:
                return EpistemicStatus.INFERRED
            elif evidence_quality > 0.0:
                return EpistemicStatus.UNKNOWN
            else:
                return EpistemicStatus.UNKNOWN
        
        # Use epistemic framework
        if evidence_quality >= 0.9 and len(evidence) >= 3:
            return EpistemicStatus.VALIDATED
        elif evidence_quality >= 0.5 and len(evidence) >= 2:
            return EpistemicStatus.INFERRED
        elif evidence_quality > 0.0:
            return EpistemicStatus.UNKNOWN
        else:
            return EpistemicStatus.UNKNOWN
    
    def _calculate_certainty(self, evidence_quality: float, evidence: List[ExecutionEvidence]) -> float:
        """Calculate epistemic certainty (0.0 to 1.0)."""
        if not evidence:
            return 0.0
        
        # Base certainty from evidence quality
        base_certainty = evidence_quality
        
        # Boost for multiple evidence types
        evidence_types = set(e.evidence_type for e in evidence)
        type_bonus = min(len(evidence_types) * 0.1, 0.3)
        
        # Boost for high-confidence evidence
        high_confidence_count = sum(1 for e in evidence if e.confidence >= 0.8)
        confidence_bonus = min(high_confidence_count * 0.05, 0.2)
        
        certainty = min(base_certainty + type_bonus + confidence_bonus, 1.0)
        
        return certainty
    
    def _determine_execution_status(self, evidence: List[ExecutionEvidence], certainty: float) -> ExecutionStatus:
        """Determine execution status based on evidence and certainty."""
        if certainty >= 0.9:
            return ExecutionStatus.COMPLETE
        elif certainty >= 0.5:
            return ExecutionStatus.IN_PROGRESS
        elif certainty > 0.0:
            return ExecutionStatus.NOT_STARTED
        else:
            return ExecutionStatus.UNKNOWN
    
    def _calculate_execution_percentage(self, goal: Goal, evidence: List[ExecutionEvidence]) -> float:
        """Calculate execution percentage (0.0 to 100.0)."""
        if not evidence:
            return 0.0
        
        # Check expected outcomes against evidence
        outcomes_met = 0
        for outcome in goal.expected_outcomes:
            # Simple keyword matching (could be enhanced)
            outcome_lower = outcome.lower()
            for e in evidence:
                if any(keyword in e.evidence_description.lower() for keyword in outcome_lower.split()):
                    outcomes_met += 1
                    break
        
        if goal.expected_outcomes:
            percentage = (outcomes_met / len(goal.expected_outcomes)) * 100.0
        else:
            # Fallback to certainty-based calculation
            certainty = self._calculate_certainty(
                self._assess_evidence_quality(evidence),
                evidence
            )
            percentage = certainty * 100.0
        
        return min(percentage, 100.0)
    
    def _identify_blockers(self, goal: Goal, evidence: List[ExecutionEvidence]) -> List[str]:
        """Identify blockers preventing goal completion."""
        blockers = []
        
        # Check for missing expected outcomes
        outcomes_met = set()
        for outcome in goal.expected_outcomes:
            outcome_lower = outcome.lower()
            for e in evidence:
                if any(keyword in e.evidence_description.lower() for keyword in outcome_lower.split()):
                    outcomes_met.add(outcome)
                    break
        
        missing_outcomes = set(goal.expected_outcomes) - outcomes_met
        if missing_outcomes:
            blockers.append(f"Missing outcomes: {', '.join(list(missing_outcomes)[:3])}")
        
        # Check for low evidence quality
        evidence_quality = self._assess_evidence_quality(evidence)
        if evidence_quality < 0.5:
            blockers.append(f"Insufficient evidence quality: {evidence_quality:.2f}")
        
        return blockers
    
    def validate_all(self) -> Dict[str, Any]:
        """Validate ALL team member execution of ALL goals."""
        print(" EPISTEMIC VALIDATION: ALL TEAM MEMBER EXECUTION")
        print("=" * 80)
        print()
        
        # Discover all goals
        goals = self.discover_all_goals()
        
        # Validate each goal
        print(" Validating goal execution...")
        print("-" * 80)
        
        executions = []
        for goal in goals:
            execution = self.validate_execution_epistemically(goal)
            executions.append(execution)
            
            status_icon = {
                ExecutionStatus.COMPLETE: "",
                ExecutionStatus.IN_PROGRESS: "⏳",
                ExecutionStatus.NOT_STARTED: "",
                ExecutionStatus.BLOCKED: "",
                ExecutionStatus.UNKNOWN: ""
            }.get(execution.execution_status, "")
            
            print(f"{status_icon} {goal.goal_id}: {goal.title}")
            print(f"   Status: {execution.execution_status.value}")
            print(f"   Certainty: {execution.certainty:.2%}")
            print(f"   Execution: {execution.execution_percentage:.1f}%")
            print(f"   Evidence: {len(execution.evidence)} items")
            if execution.blockers:
                print(f"   Blockers: {', '.join(execution.blockers[:2])}")
            print()
        
        self.executions = executions
        
        # Generate summary
        summary = self._generate_summary(executions)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "team_members": self.team_members,
            "total_goals": len(goals),
            "executions": [e.to_dict() for e in executions],
            "summary": summary
        }
    
    def _generate_summary(self, executions: List[GoalExecution]) -> Dict[str, Any]:
        """Generate validation summary."""
        total = len(executions)
        
        by_status = {}
        for status in ExecutionStatus:
            by_status[status.value] = sum(1 for e in executions if e.execution_status == status)
        
        by_member = {}
        for member in self.team_members:
            member_executions = [e for e in executions if e.goal.team_member == member]
            if member_executions:
                by_member[member] = {
                    "total_goals": len(member_executions),
                    "complete": sum(1 for e in member_executions if e.execution_status == ExecutionStatus.COMPLETE),
                    "in_progress": sum(1 for e in member_executions if e.execution_status == ExecutionStatus.IN_PROGRESS),
                    "not_started": sum(1 for e in member_executions if e.execution_status == ExecutionStatus.NOT_STARTED),
                    "avg_certainty": sum(e.certainty for e in member_executions) / len(member_executions),
                    "avg_execution": sum(e.execution_percentage for e in member_executions) / len(member_executions)
                }
        
        avg_certainty = sum(e.certainty for e in executions) / total if total > 0 else 0.0
        avg_execution = sum(e.execution_percentage for e in executions) / total if total > 0 else 0.0
        
        return {
            "total_goals": total,
            "by_status": by_status,
            "by_member": by_member,
            "avg_certainty": avg_certainty,
            "avg_execution_percentage": avg_execution,
            "epistemic_framework_available": EPISTEMIC_FRAMEWORK_AVAILABLE
        }


def main():
    """CLI Entry Point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Epistemic Validation: ALL Team Member Execution of ALL Goals"
    )
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace) if args.workspace else None
    validator = TeamMemberExecutionValidator(workspace_root)
    results = validator.validate_all()
    
    # Print summary
    print("=" * 80)
    print(" VALIDATION SUMMARY")
    print("=" * 80)
    print()
    
    summary = results["summary"]
    print(f"Total Goals: {summary['total_goals']}")
    print(f"Average Certainty: {summary['avg_certainty']:.2%}")
    print(f"Average Execution: {summary['avg_execution_percentage']:.1f}%")
    print()
    
    print("By Status:")
    for status, count in summary["by_status"].items():
        print(f"  {status}: {count}")
    print()
    
    print("By Team Member:")
    for member, stats in summary["by_member"].items():
        print(f"  {member}:")
        print(f"    Goals: {stats['total_goals']}")
        print(f"    Complete: {stats['complete']}")
        print(f"    In Progress: {stats['in_progress']}")
        print(f"    Not Started: {stats['not_started']}")
        print(f"    Avg Certainty: {stats['avg_certainty']:.2%}")
        print(f"    Avg Execution: {stats['avg_execution']:.1f}%")
        print()
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(results, indent=2, default=str))
        print(f" Saved: {output_path}")
    
    print("=" * 80)
    print(" EPISTEMIC VALIDATION COMPLETE")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    main()

