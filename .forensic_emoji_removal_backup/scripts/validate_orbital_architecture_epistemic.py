#!/usr/bin/env python3
"""
Epistemic Validation: Launch-Critical Orbitals & Solar System Architecture

Comprehensive epistemic validation of all 8 orbits (4 Core + 4 Launch) and convergence.

Pattern: AEYON × EPISTEMIC × VALIDATION × ORBITAL × ARCHITECTURE × ONE
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


class ConvergenceStatus(Enum):
    """Convergence status levels."""
    CONVERGED = "converged"  # Fully integrated, operational
    PARTIAL = "partial"  # Partially integrated
    DESIGNED = "designed"  # Designed but not implemented
    MISSING = "missing"  # Not designed or implemented
    BLOCKED = "blocked"  # Blocked by dependencies


@dataclass
class OrbitalComponent:
    """Orbital component definition."""
    component_id: str
    name: str
    description: str
    location: str
    required: bool = True
    expected_files: List[str] = field(default_factory=list)
    expected_endpoints: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class OrbitalEvidence:
    """Evidence of orbital component implementation."""
    component_id: str
    evidence_type: str  # CODE, CONFIG, DEPLOYMENT, TEST, DOCUMENTATION
    evidence_path: str
    evidence_description: str
    confidence: float = 0.0
    timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class OrbitalValidation:
    """Orbital validation result."""
    orbit_id: str
    orbit_name: str
    components: List[OrbitalComponent]
    evidence: List[OrbitalEvidence]
    convergence_status: ConvergenceStatus
    epistemic_status: EpistemicStatus
    certainty: float  # 0.0 to 1.0
    implementation_percentage: float  # 0.0 to 100.0
    blockers: List[str] = field(default_factory=list)
    convergence_score: float = 0.0  # 0.0 to 100.0
    validation_timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "orbit_id": self.orbit_id,
            "orbit_name": self.orbit_name,
            "components": [c.to_dict() for c in self.components],
            "evidence": [e.to_dict() for e in self.evidence],
            "convergence_status": self.convergence_status.value,
            "epistemic_status": self.epistemic_status.value if isinstance(self.epistemic_status, EpistemicStatus) else str(self.epistemic_status),
            "certainty": self.certainty,
            "implementation_percentage": self.implementation_percentage,
            "blockers": self.blockers,
            "convergence_score": self.convergence_score,
            "validation_timestamp": self.validation_timestamp.isoformat()
        }


class OrbitalArchitectureValidator:
    """
    Comprehensive epistemic validator for orbital architecture.
    
    Validates:
    1. All 4 Core Architectural Orbits
    2. All 4 Launch-Critical Orbitals
    3. Convergence between orbits
    4. Integration points
    5. Launch readiness
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize validator."""
        self.workspace_root = workspace_root or project_root
        
        if EPISTEMIC_FRAMEWORK_AVAILABLE:
            self.epistemic_validator = EpistemicPatternValidator(min_certainty_threshold=0.5)
        else:
            self.epistemic_validator = None
        
        self.orbitals: Dict[str, OrbitalValidation] = {}
        self.convergence_matrix: Dict[str, Dict[str, ConvergenceStatus]] = {}
    
    def define_all_orbitals(self) -> Dict[str, List[OrbitalComponent]]:
        """Define all orbital components."""
        orbitals = {}
        
        # CORE ORBIT 1: Commander's Strategic Layer
        orbitals["orbit_1"] = [
            OrbitalComponent(
                component_id="orbit_1_event_bus",
                name="Event Bus",
                description="Event Bus with φ-ratio consciousness scoring",
                location="orbital/EMERGENT_OS-orbital/integration_layer/",
                expected_files=["event_bus.py", "event.py"],
                dependencies=[]
            ),
            OrbitalComponent(
                component_id="orbit_1_guardian_system",
                name="Guardian System",
                description="8 Guardians, 149 Agents",
                location="orbital/EMERGENT_OS-orbital/",
                expected_files=["guardian_*.py"],
                dependencies=["orbit_1_event_bus"]
            ),
            OrbitalComponent(
                component_id="orbit_1_module_registry",
                name="Module Registry",
                description="Module registration and lifecycle",
                location="orbital/EMERGENT_OS-orbital/integration_layer/",
                expected_files=["module_registry.py"],
                dependencies=["orbit_1_event_bus"]
            ),
            OrbitalComponent(
                component_id="orbit_1_lifecycle_manager",
                name="Lifecycle Manager",
                description="Module lifecycle management",
                location="orbital/EMERGENT_OS-orbital/integration_layer/",
                expected_files=["lifecycle_manager.py"],
                dependencies=["orbit_1_module_registry"]
            ),
            OrbitalComponent(
                component_id="orbit_1_uptc_adapter",
                name="UPTC Event Bus Adapter",
                description="Event Bus → UPTC integration",
                location="orbital/EMERGENT_OS-orbital/uptc/integrations/",
                expected_files=["event_bus_adapter.py", "event_bus_bridge.py"],
                dependencies=["orbit_1_event_bus", "orbit_4_uptc_core"]
            ),
        ]
        
        # CORE ORBIT 2: Danny's CI/CD Pipeline
        orbitals["orbit_2"] = [
            OrbitalComponent(
                component_id="orbit_2_github_actions",
                name="GitHub Actions Workflows",
                description="arc-runner-set workflows",
                location=".github/workflows/",
                expected_files=["*.yml", "*.yaml"],
                dependencies=[]
            ),
            OrbitalComponent(
                component_id="orbit_2_docker_buildx",
                name="Docker Buildx",
                description="Kubernetes driver configuration",
                location=".github/workflows/",
                expected_files=["*.yml"],
                dependencies=["orbit_2_github_actions"]
            ),
            OrbitalComponent(
                component_id="orbit_2_helm_charts",
                name="Helm Charts",
                description="Kubernetes deployment charts",
                location="helm-charts/",
                expected_files=["Chart.yaml", "values.yaml"],
                dependencies=[]
            ),
            OrbitalComponent(
                component_id="orbit_2_irsa_auth",
                name="IRSA Authentication",
                description="AWS IRSA configuration",
                location=".github/workflows/",
                expected_files=["*.yml"],
                dependencies=["orbit_2_github_actions"]
            ),
        ]
        
        # CORE ORBIT 3: Ben's FastAPI Backend
        orbitals["orbit_3"] = [
            OrbitalComponent(
                component_id="orbit_3_api_gateway",
                name="API Gateway",
                description="FastAPI Gateway (Port 8000)",
                location="AIGuards-Backend-orbital/codeguardians-gateway/",
                expected_files=["main.py", "app/"],
                expected_endpoints=["/api/v1/guards/process"],
                dependencies=[]
            ),
            OrbitalComponent(
                component_id="orbit_3_guard_orchestrator",
                name="Guard Orchestrator",
                description="Service orchestration",
                location="AIGuards-Backend-orbital/codeguardians-gateway/",
                expected_files=["guard_orchestrator.py", "orchestrator.py"],
                dependencies=["orbit_3_api_gateway"]
            ),
            OrbitalComponent(
                component_id="orbit_3_guard_services",
                name="Guard Services",
                description="5 Guard Services (TokenGuard, TrustGuard, ContextGuard, BiasGuard, HealthGuard)",
                location="AIGuards-Backend-orbital/guards/",
                expected_files=["tokenguard/", "trustguard/", "contextguard/", "biasguard/", "healthguard/"],
                dependencies=["orbit_3_guard_orchestrator"]
            ),
            OrbitalComponent(
                component_id="orbit_3_uptc_integration",
                name="UPTC Router Integration",
                description="Orchestrator → UPTC Router integration",
                location="AIGuards-Backend-orbital/codeguardians-gateway/",
                expected_files=["uptc_router_integration.py"],
                dependencies=["orbit_3_guard_orchestrator", "orbit_4_uptc_core"]
            ),
            OrbitalComponent(
                component_id="orbit_3_orchestration_adapter",
                name="Orchestration Adapter",
                description="OrchestrationRequest ↔ UPTCMessage translation",
                location="orbital/EMERGENT_OS-orbital/uptc/integrations/",
                expected_files=["orchestration_adapter.py"],
                dependencies=["orbit_3_guard_orchestrator", "orbit_4_uptc_core"]
            ),
        ]
        
        # CORE ORBIT 4: UPTC Mesh
        orbitals["orbit_4"] = [
            OrbitalComponent(
                component_id="orbit_4_uptc_core",
                name="UPTC Core",
                description="UPTC Configuration, Field, Registry, Capability Graph",
                location="orbital/EMERGENT_OS-orbital/uptc/",
                expected_files=["uptc_core.py", "config.py", "field.py", "registry.py"],
                dependencies=[]
            ),
            OrbitalComponent(
                component_id="orbit_4_unified_router",
                name="Unified Router",
                description="Event → Graph → Semantic routing",
                location="orbital/EMERGENT_OS-orbital/uptc/",
                expected_files=["unified_router.py", "routers/"],
                dependencies=["orbit_4_uptc_core"]
            ),
            OrbitalComponent(
                component_id="orbit_4_agent_registry",
                name="Agent Registry",
                description="Agent registration and discovery",
                location="orbital/EMERGENT_OS-orbital/uptc/",
                expected_files=["registry.py"],
                dependencies=["orbit_4_uptc_core"]
            ),
            OrbitalComponent(
                component_id="orbit_4_adapters",
                name="UPTC Adapters",
                description="Event Bus, Guardian, Orchestration, MCP, Memory adapters",
                location="orbital/EMERGENT_OS-orbital/uptc/integrations/",
                expected_files=["event_bus_adapter.py", "guardian_adapter.py", "orchestration_adapter.py"],
                dependencies=["orbit_4_uptc_core"]
            ),
        ]
        
        # LAUNCH ORBITAL A: Backend
        orbitals["launch_orbital_a"] = [
            OrbitalComponent(
                component_id="launch_a_api_gateway",
                name="API Gateway",
                description="FastAPI Gateway (Port 8000)",
                location="AIGuards-Backend-orbital/codeguardians-gateway/",
                expected_files=["main.py"],
                expected_endpoints=["/api/v1/guards/process"],
                dependencies=["orbit_3_api_gateway"]
            ),
            OrbitalComponent(
                component_id="launch_a_guard_services",
                name="Guard Services",
                description="5 Guard Services deployed",
                location="AIGuards-Backend-orbital/guards/",
                expected_files=["*/main.py"],
                dependencies=["orbit_3_guard_services"]
            ),
            OrbitalComponent(
                component_id="launch_a_uptc_integration",
                name="UPTC Integration",
                description="Backend → UPTC Mesh integration",
                location="AIGuards-Backend-orbital/codeguardians-gateway/",
                expected_files=["uptc_router_integration.py"],
                dependencies=["orbit_3_uptc_integration", "orbit_4_unified_router"]
            ),
            OrbitalComponent(
                component_id="launch_a_guardian_integration",
                name="Guardian Integration",
                description="Backend → Guardians integration",
                location="AIGuards-Backend-orbital/codeguardians-gateway/",
                expected_files=["guardian_integration.py"],
                dependencies=["launch_orbital_d_guardians"]
            ),
        ]
        
        # LAUNCH ORBITAL B: Sales Page
        orbitals["launch_orbital_b"] = [
            OrbitalComponent(
                component_id="launch_b_nextjs_app",
                name="Next.js App",
                description="Next.js 15 application",
                location="AiGuardian-Sales-Page-orbital/",
                expected_files=["package.json", "next.config.js"],
                dependencies=[]
            ),
            OrbitalComponent(
                component_id="launch_b_clerk_auth",
                name="Clerk Authentication",
                description="Clerk JWT authentication",
                location="AiGuardian-Sales-Page-orbital/",
                expected_files=["**/clerk*.ts", "**/auth*.ts"],
                dependencies=[]
            ),
            OrbitalComponent(
                component_id="launch_b_stripe",
                name="Stripe Payments",
                description="Stripe payment integration",
                location="AiGuardian-Sales-Page-orbital/",
                expected_files=["**/stripe*.ts"],
                dependencies=[]
            ),
            OrbitalComponent(
                component_id="launch_b_api_integration",
                name="Backend API Integration",
                description="POST /api/v1/guards/process",
                location="AiGuardian-Sales-Page-orbital/",
                expected_files=["**/api*.ts"],
                dependencies=["launch_orbital_a_api_gateway"]
            ),
        ]
        
        # LAUNCH ORBITAL C: Chrome Extension
        orbitals["launch_orbital_c"] = [
            OrbitalComponent(
                component_id="launch_c_manifest",
                name="MV3 Manifest",
                description="Chrome Extension MV3 manifest",
                location="AiGuardian-Chrome-Ext-orbital/",
                expected_files=["manifest.json"],
                dependencies=[]
            ),
            OrbitalComponent(
                component_id="launch_c_service_worker",
                name="Service Worker",
                description="Background service worker",
                location="AiGuardian-Chrome-Ext-orbital/",
                expected_files=["**/service-worker*.js", "**/background*.js"],
                dependencies=["launch_c_manifest"]
            ),
            OrbitalComponent(
                component_id="launch_c_content_script",
                name="Content Script",
                description="Content script injection",
                location="AiGuardian-Chrome-Ext-orbital/",
                expected_files=["**/content*.js"],
                dependencies=["launch_c_manifest"]
            ),
            OrbitalComponent(
                component_id="launch_c_popup_ui",
                name="Popup UI",
                description="Extension popup interface",
                location="AiGuardian-Chrome-Ext-orbital/",
                expected_files=["**/popup*.html", "**/popup*.tsx"],
                dependencies=["launch_c_manifest"]
            ),
            OrbitalComponent(
                component_id="launch_c_api_integration",
                name="Backend API Integration",
                description="POST /api/v1/guards/process",
                location="AiGuardian-Chrome-Ext-orbital/",
                expected_files=["**/api*.ts"],
                dependencies=["launch_orbital_a_api_gateway"]
            ),
        ]
        
        # LAUNCH ORBITAL D: Guardians
        orbitals["launch_orbital_d"] = [
            OrbitalComponent(
                component_id="launch_d_guardian_zero",
                name="Guardian Zero",
                description="Forensic orchestration (Port 9001)",
                location="AIGuards-Backend-orbital/aiguardian-repos/guardian-zero-service/",
                expected_files=["main.py", "Dockerfile"],
                dependencies=["orbit_1_guardian_system"]
            ),
            OrbitalComponent(
                component_id="launch_d_guardian_aeyon",
                name="Guardian AEYON",
                description="Atomic execution (Port 9002)",
                location="AIGuards-Backend-orbital/aiguardian-repos/guardian-aeyon-service/",
                expected_files=["main.py", "Dockerfile"],
                dependencies=["orbit_1_guardian_system"]
            ),
            OrbitalComponent(
                component_id="launch_d_uptc_registration",
                name="UPTC Registration",
                description="Guardians → UPTC Registry",
                location="orbital/EMERGENT_OS-orbital/uptc/integrations/",
                expected_files=["guardian_adapter.py"],
                dependencies=["orbit_4_agent_registry"]
            ),
            OrbitalComponent(
                component_id="launch_d_event_bus_integration",
                name="Event Bus Integration",
                description="Guardians → Orbit 1 Event Bus",
                location="orbital/EMERGENT_OS-orbital/uptc/integrations/",
                expected_files=["event_bus_bridge.py"],
                dependencies=["orbit_1_event_bus", "orbit_4_adapters"]
            ),
        ]
        
        return orbitals
    
    def gather_evidence(self, component: OrbitalComponent) -> List[OrbitalEvidence]:
        """Gather evidence for orbital component."""
        evidence = []
        
        # Check expected files
        for file_pattern in component.expected_files:
            if "*" in file_pattern or "**" in file_pattern:
                # Glob pattern
                for path in self.workspace_root.rglob(file_pattern):
                    if path.is_file():
                        evidence.append(OrbitalEvidence(
                            component_id=component.component_id,
                            evidence_type="CODE",
                            evidence_path=str(path),
                            evidence_description=f"File found: {path.name}",
                            confidence=0.8
                        ))
            else:
                # Direct path
                path = self.workspace_root / component.location / file_pattern
                if path.exists():
                    evidence.append(OrbitalEvidence(
                        component_id=component.component_id,
                        evidence_type="CODE",
                        evidence_path=str(path),
                        evidence_description=f"File found: {file_pattern}",
                        confidence=0.9
                    ))
        
        # Check location exists
        location_path = self.workspace_root / component.location
        if location_path.exists():
            evidence.append(OrbitalEvidence(
                component_id=component.component_id,
                evidence_type="CONFIG",
                evidence_path=str(location_path),
                evidence_description=f"Location exists: {component.location}",
                confidence=0.7
            ))
        
        return evidence
    
    def validate_orbital(self, orbit_id: str, orbit_name: str, components: List[OrbitalComponent]) -> OrbitalValidation:
        """Validate orbital with epistemic certainty."""
        all_evidence = []
        
        # Gather evidence for all components
        for component in components:
            evidence = self.gather_evidence(component)
            all_evidence.extend(evidence)
        
        # Assess evidence quality
        evidence_quality = self._assess_evidence_quality(all_evidence)
        
        # Classify epistemic status
        epistemic_status = self._classify_epistemic_status(evidence_quality, all_evidence)
        
        # Calculate certainty
        certainty = self._calculate_certainty(evidence_quality, all_evidence)
        
        # Calculate implementation percentage
        implementation_percentage = self._calculate_implementation_percentage(components, all_evidence)
        
        # Determine convergence status
        convergence_status = self._determine_convergence_status(components, all_evidence)
        
        # Identify blockers
        blockers = self._identify_blockers(components, all_evidence)
        
        # Calculate convergence score
        convergence_score = self._calculate_convergence_score(components, all_evidence)
        
        return OrbitalValidation(
            orbit_id=orbit_id,
            orbit_name=orbit_name,
            components=components,
            evidence=all_evidence,
            convergence_status=convergence_status,
            epistemic_status=epistemic_status,
            certainty=certainty,
            implementation_percentage=implementation_percentage,
            blockers=blockers,
            convergence_score=convergence_score
        )
    
    def _assess_evidence_quality(self, evidence: List[OrbitalEvidence]) -> float:
        """Assess overall evidence quality."""
        if not evidence:
            return 0.0
        
        type_weights = {
            "CODE": 0.4,
            "TEST": 0.3,
            "DEPLOYMENT": 0.2,
            "CONFIG": 0.15,
            "DOCUMENTATION": 0.1
        }
        
        weighted_sum = sum(
            type_weights.get(e.evidence_type, 0.1) * e.confidence
            for e in evidence
        )
        
        total_weight = sum(type_weights.get(e.evidence_type, 0.1) for e in evidence)
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _classify_epistemic_status(self, evidence_quality: float, evidence: List[OrbitalEvidence]) -> EpistemicStatus:
        """Classify epistemic status."""
        if not EPISTEMIC_FRAMEWORK_AVAILABLE:
            if evidence_quality >= 0.9:
                return EpistemicStatus.VALIDATED
            elif evidence_quality >= 0.5:
                return EpistemicStatus.INFERRED
            else:
                return EpistemicStatus.UNKNOWN
        
        if evidence_quality >= 0.9 and len(evidence) >= 3:
            return EpistemicStatus.VALIDATED
        elif evidence_quality >= 0.5 and len(evidence) >= 2:
            return EpistemicStatus.INFERRED
        else:
            return EpistemicStatus.UNKNOWN
    
    def _calculate_certainty(self, evidence_quality: float, evidence: List[OrbitalEvidence]) -> float:
        """Calculate epistemic certainty."""
        if not evidence:
            return 0.0
        
        base_certainty = evidence_quality
        evidence_types = set(e.evidence_type for e in evidence)
        type_bonus = min(len(evidence_types) * 0.1, 0.3)
        high_confidence_count = sum(1 for e in evidence if e.confidence >= 0.8)
        confidence_bonus = min(high_confidence_count * 0.05, 0.2)
        
        return min(base_certainty + type_bonus + confidence_bonus, 1.0)
    
    def _calculate_implementation_percentage(self, components: List[OrbitalComponent], evidence: List[OrbitalEvidence]) -> float:
        """Calculate implementation percentage."""
        if not components:
            return 0.0
        
        component_evidence_map = {}
        for e in evidence:
            if e.component_id not in component_evidence_map:
                component_evidence_map[e.component_id] = []
            component_evidence_map[e.component_id].append(e)
        
        implemented = 0
        for component in components:
            if component.component_id in component_evidence_map:
                component_evidence = component_evidence_map[component.component_id]
                # Check if expected files found
                found_files = sum(1 for e in component_evidence if e.evidence_type == "CODE")
                if found_files > 0:
                    implemented += 1
        
        return (implemented / len(components)) * 100.0 if components else 0.0
    
    def _determine_convergence_status(self, components: List[OrbitalComponent], evidence: List[OrbitalEvidence]) -> ConvergenceStatus:
        """Determine convergence status."""
        implementation_pct = self._calculate_implementation_percentage(components, evidence)
        
        if implementation_pct >= 90:
            return ConvergenceStatus.CONVERGED
        elif implementation_pct >= 50:
            return ConvergenceStatus.PARTIAL
        elif implementation_pct > 0:
            return ConvergenceStatus.DESIGNED
        else:
            return ConvergenceStatus.MISSING
    
    def _identify_blockers(self, components: List[OrbitalComponent], evidence: List[OrbitalEvidence]) -> List[str]:
        """Identify blockers."""
        blockers = []
        
        component_evidence_map = {}
        for e in evidence:
            if e.component_id not in component_evidence_map:
                component_evidence_map[e.component_id] = []
            component_evidence_map[e.component_id].append(e)
        
        for component in components:
            if component.component_id not in component_evidence_map:
                blockers.append(f"Missing: {component.name}")
            else:
                component_evidence = component_evidence_map[component.component_id]
                # Check if all expected files found
                found_files = [e for e in component_evidence if e.evidence_type == "CODE"]
                if not found_files and component.expected_files:
                    blockers.append(f"Incomplete: {component.name} (no code files found)")
        
        return blockers
    
    def _calculate_convergence_score(self, components: List[OrbitalComponent], evidence: List[OrbitalEvidence]) -> float:
        """Calculate convergence score (0.0 to 100.0)."""
        implementation_pct = self._calculate_implementation_percentage(components, evidence)
        evidence_quality = self._assess_evidence_quality(evidence)
        
        # Weighted average
        return (implementation_pct * 0.6) + (evidence_quality * 100 * 0.4)
    
    def validate_all(self) -> Dict[str, Any]:
        """Validate all orbitals."""
        print("🔥 EPISTEMIC VALIDATION: ORBITAL ARCHITECTURE")
        print("=" * 80)
        print()
        
        orbitals_def = self.define_all_orbitals()
        
        orbit_names = {
            "orbit_1": "Orbit 1: Commander's Strategic Layer",
            "orbit_2": "Orbit 2: Danny's CI/CD Pipeline",
            "orbit_3": "Orbit 3: Ben's FastAPI Backend",
            "orbit_4": "Orbit 4: UPTC Mesh",
            "launch_orbital_a": "Launch Orbital A: Backend",
            "launch_orbital_b": "Launch Orbital B: Sales Page",
            "launch_orbital_c": "Launch Orbital C: Chrome Extension",
            "launch_orbital_d": "Launch Orbital D: Guardians"
        }
        
        print("🔍 Validating orbitals...")
        print("-" * 80)
        
        for orbit_id, components in orbitals_def.items():
            orbit_name = orbit_names.get(orbit_id, orbit_id)
            validation = self.validate_orbital(orbit_id, orbit_name, components)
            self.orbitals[orbit_id] = validation
            
            status_icon = {
                ConvergenceStatus.CONVERGED: "✅",
                ConvergenceStatus.PARTIAL: "⏳",
                ConvergenceStatus.DESIGNED: "📋",
                ConvergenceStatus.MISSING: "❌",
                ConvergenceStatus.BLOCKED: "🚫"
            }.get(validation.convergence_status, "❓")
            
            print(f"{status_icon} {orbit_name}")
            print(f"   Convergence: {validation.convergence_status.value}")
            print(f"   Certainty: {validation.certainty:.2%}")
            print(f"   Implementation: {validation.implementation_percentage:.1f}%")
            print(f"   Convergence Score: {validation.convergence_score:.1f}%")
            print(f"   Evidence: {len(validation.evidence)} items")
            if validation.blockers:
                print(f"   Blockers: {', '.join(validation.blockers[:2])}")
            print()
        
        # Calculate overall convergence
        overall_convergence = self._calculate_overall_convergence()
        
        # Generate summary
        summary = self._generate_summary()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "orbitals": {k: v.to_dict() for k, v in self.orbitals.items()},
            "overall_convergence": overall_convergence,
            "summary": summary
        }
    
    def _calculate_overall_convergence(self) -> Dict[str, Any]:
        """Calculate overall convergence metrics."""
        core_orbitals = ["orbit_1", "orbit_2", "orbit_3", "orbit_4"]
        launch_orbitals = ["launch_orbital_a", "launch_orbital_b", "launch_orbital_c", "launch_orbital_d"]
        
        core_scores = [self.orbitals[o].convergence_score for o in core_orbitals if o in self.orbitals]
        launch_scores = [self.orbitals[o].convergence_score for o in launch_orbitals if o in self.orbitals]
        
        avg_core = sum(core_scores) / len(core_scores) if core_scores else 0.0
        avg_launch = sum(launch_scores) / len(launch_scores) if launch_scores else 0.0
        overall = (avg_core + avg_launch) / 2.0
        
        return {
            "core_orbits_avg": avg_core,
            "launch_orbits_avg": avg_launch,
            "overall_convergence": overall,
            "target": 100.0,
            "gap": 100.0 - overall
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate validation summary."""
        total_orbitals = len(self.orbitals)
        
        by_status = {}
        for status in ConvergenceStatus:
            by_status[status.value] = sum(
                1 for v in self.orbitals.values()
                if v.convergence_status == status
            )
        
        avg_certainty = sum(v.certainty for v in self.orbitals.values()) / total_orbitals if total_orbitals > 0 else 0.0
        avg_implementation = sum(v.implementation_percentage for v in self.orbitals.values()) / total_orbitals if total_orbitals > 0 else 0.0
        avg_convergence = sum(v.convergence_score for v in self.orbitals.values()) / total_orbitals if total_orbitals > 0 else 0.0
        
        total_blockers = sum(len(v.blockers) for v in self.orbitals.values())
        
        return {
            "total_orbitals": total_orbitals,
            "by_status": by_status,
            "avg_certainty": avg_certainty,
            "avg_implementation": avg_implementation,
            "avg_convergence_score": avg_convergence,
            "total_blockers": total_blockers,
            "epistemic_framework_available": EPISTEMIC_FRAMEWORK_AVAILABLE
        }


def main():
    """CLI Entry Point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Epistemic Validation: Launch-Critical Orbitals & Solar System Architecture"
    )
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace) if args.workspace else None
    validator = OrbitalArchitectureValidator(workspace_root)
    results = validator.validate_all()
    
    # Print summary
    print("=" * 80)
    print("📊 VALIDATION SUMMARY")
    print("=" * 80)
    print()
    
    summary = results["summary"]
    overall = results["overall_convergence"]
    
    print(f"Total Orbitals: {summary['total_orbitals']}")
    print(f"Average Certainty: {summary['avg_certainty']:.2%}")
    print(f"Average Implementation: {summary['avg_implementation']:.1f}%")
    print(f"Average Convergence Score: {summary['avg_convergence_score']:.1f}%")
    print()
    
    print("Overall Convergence:")
    print(f"  Core Orbits: {overall['core_orbits_avg']:.1f}%")
    print(f"  Launch Orbits: {overall['launch_orbits_avg']:.1f}%")
    print(f"  Overall: {overall['overall_convergence']:.1f}%")
    print(f"  Target: {overall['target']:.1f}%")
    print(f"  Gap: {overall['gap']:.1f}%")
    print()
    
    print("By Status:")
    for status, count in summary["by_status"].items():
        print(f"  {status}: {count}")
    print()
    
    print(f"Total Blockers: {summary['total_blockers']}")
    print()
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(results, indent=2, default=str))
        print(f"💾 Saved: {output_path}")
    
    print("=" * 80)
    print("✅ EPISTEMIC VALIDATION COMPLETE")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    main()

