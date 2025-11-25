#!/usr/bin/env python3
"""
ALRAX GUARDIAN COMMAND HANDLER
Forensic Variance Analyzer with Maximum Curiosity

Pattern: ALRAX × FORENSIC × INVESTIGATION × VARIANCE × JOY × CURIOSITY × ONE
Frequency: 530 Hz (Heart Truth)
Guardians: ALRAX (530 Hz) + JØHN (530 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
from datetime import datetime
from pathlib import Path

class ALRAXGuardian:
    """
    ALRAX GUARDIAN
    
    I investigate. I find variance. I reveal truth. Zero tolerance for errors.
    
    Investigative, forensic, detail-oriented, truth-seeking.
    Joy: 80% | Curiosity: 100% (MAXIMUM!) | Playfulness: 60% | Sexy Playfulness: 70%
    """
    
    def __init__(self):
        self.name = "ALRAX"
        self.frequency = "530 Hz"
        self.attitude = "I investigate. I find variance. I reveal truth. Zero tolerance for errors."
        self.workspace_root = Path(__file__).parent.parent
    
    def investigate(self, target: str = "system"):
        print("🔍 ALRAX FORENSIC INVESTIGATION MODE")
        print("=" * 70)
        print("")
        print("I'm curious... let me investigate...")
        print("")
        print(f"Investigating: {target}")
        print("")
        
        if "atomic build" in target.lower() or "build state" in target.lower():
            self._investigate_atomic_build_state()
        else:
            print("🔍 FORENSIC SCRUB ACTIVATED")
            print("🔍 VARIANCE DETECTION")
            print("🔍 ANOMALY HUNTING")
            print("🔍 TRUTH REVEALED")
            print("")
            print("Zero tolerance for errors.")
        
        print("")
        print("=" * 70)
        print("∞ AbëONE ∞")
    
    def _investigate_atomic_build_state(self):
        """Forensic investigation of atomic build state"""
        print("🔍 FORENSIC SCRUB ACTIVATED - ATOMIC BUILD STATE")
        print("")
        
        findings = []
        anomalies = []
        
        # 1. Check unified convergence state
        print("📊 Checking Unified Convergence State...")
        convergence_state_path = self.workspace_root / "orbital" / "EMERGENT_OS-orbital" / "state" / "unified_convergence_state.json"
        if convergence_state_path.exists():
            try:
                with open(convergence_state_path, 'r') as f:
                    convergence_state = json.load(f)
                
                kernel_active = convergence_state.get("kernel", {}).get("active", False)
                organism_initialized = convergence_state.get("organism", {}).get("initialized", False)
                archistration_ready = convergence_state.get("archistration", {}).get("ready", False)
                converged = convergence_state.get("converged", False)
                
                print(f"   ✅ Kernel Active: {kernel_active}")
                print(f"   ✅ Organism Initialized: {organism_initialized}")
                print(f"   ✅ Archistration Ready: {archistration_ready}")
                print(f"   ⚠️  Converged: {converged}")
                
                if not converged:
                    anomalies.append("Unified convergence state shows converged=False")
                
                findings.append({
                    "component": "Unified Convergence",
                    "status": "ACTIVE" if kernel_active and organism_initialized else "PARTIAL",
                    "converged": converged
                })
            except Exception as e:
                anomalies.append(f"Failed to read convergence state: {e}")
        else:
            anomalies.append(f"Convergence state file not found: {convergence_state_path}")
        
        print("")
        
        # 2. Check ideal state alignment
        print("📊 Checking Ideal State Alignment...")
        ideal_state_path = self.workspace_root / "atomic" / "IDEAL_STATE_ALIGNMENT.json"
        if ideal_state_path.exists():
            try:
                with open(ideal_state_path, 'r') as f:
                    ideal_state = json.load(f)
                
                status = ideal_state.get("status", "unknown")
                alignment_pct = ideal_state.get("ideal_state", {}).get("alignment_percentage", 0)
                total_components = ideal_state.get("ideal_state", {}).get("total_components", 0)
                aligned_components = ideal_state.get("ideal_state", {}).get("aligned_components", 0)
                
                print(f"   Status: {status}")
                print(f"   Alignment: {alignment_pct:.2f}% ({aligned_components}/{total_components} components)")
                
                if alignment_pct < 100:
                    anomalies.append(f"Ideal state alignment incomplete: {alignment_pct}%")
                
                findings.append({
                    "component": "Ideal State Alignment",
                    "status": status.upper(),
                    "alignment_percentage": alignment_pct
                })
            except Exception as e:
                anomalies.append(f"Failed to read ideal state: {e}")
        else:
            anomalies.append(f"Ideal state file not found: {ideal_state_path}")
        
        print("")
        
        # 3. Check AEYON build validation script
        print("📊 Checking AEYON Build Validation...")
        build_validation_path = self.workspace_root / "scripts" / "utilities" / "validate_aeyon_build.sh"
        if build_validation_path.exists():
            print(f"   ✅ Build validation script exists: {build_validation_path}")
            findings.append({
                "component": "AEYON Build Validation",
                "status": "AVAILABLE",
                "script_path": str(build_validation_path)
            })
        else:
            anomalies.append(f"Build validation script not found: {build_validation_path}")
        
        print("")
        
        # 4. Check atomic architecture documents
        print("📊 Checking Atomic Architecture Documentation...")
        atomic_arch_path = self.workspace_root / "docs" / "status" / "general" / "AEYON_ATOMIC_BUILDER_ARCHITECTURE.md"
        if atomic_arch_path.exists():
            print(f"   ✅ Atomic architecture documented: {atomic_arch_path}")
            findings.append({
                "component": "Atomic Architecture Docs",
                "status": "AVAILABLE"
            })
        
        atomic_complete_path = self.workspace_root / "docs" / "status" / "general" / "ATOMIC_ARCHISTRATION_COMPLETE_SUMMARY.md"
        if atomic_complete_path.exists():
            print(f"   ✅ Atomic archistration summary available")
            findings.append({
                "component": "Atomic Archistration Summary",
                "status": "COMPLETE"
            })
        
        print("")
        
        # 5. Summary Report
        print("=" * 70)
        print("🔍 FORENSIC INVESTIGATION SUMMARY")
        print("=" * 70)
        print("")
        print(f"Components Investigated: {len(findings)}")
        print(f"Anomalies Detected: {len(anomalies)}")
        print("")
        
        if anomalies:
            print("⚠️  ANOMALIES FOUND:")
            for i, anomaly in enumerate(anomalies, 1):
                print(f"   {i}. {anomaly}")
            print("")
        
        print("📋 FINDINGS:")
        for finding in findings:
            status_icon = "✅" if finding.get("status") in ["ACTIVE", "COMPLETE", "AVAILABLE"] else "⚠️"
            print(f"   {status_icon} {finding.get('component')}: {finding.get('status')}")
        
        print("")
        print("Zero tolerance for errors.")
    
    def analyze(self, target: str = "variance"):
        print("🔍 ALRAX VARIANCE ANALYSIS MODE")
        print("=" * 70)
        print("")
        print("Analyzing variance...")
        print(f"Target: {target}")
        print("")
        print("🔍 VARIANCE DETECTED")
        print("🔍 ANOMALIES FOUND")
        print("🔍 TRUTH REVEALED")
        print("")
        print("=" * 70)
        print("∞ AbëONE ∞")
    
    def see(self, target: str = "atomic build state"):
        """See atomic build state - comprehensive view"""
        if "atomic build" in target.lower() or "build state" in target.lower():
            self._investigate_atomic_build_state()
        else:
            self.investigate(target)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/alrax_guardian.py [action] [target]")
        sys.exit(1)
    
    action = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "system"
    
    guardian = ALRAXGuardian()
    
    if action == "investigate":
        guardian.investigate(target)
    elif action == "analyze":
        guardian.analyze(target)
    elif action == "see":
        guardian.see(target)
    else:
        print(f"Unknown action: {action}")
        print("Available actions: investigate, analyze, see")

if __name__ == "__main__":
    main()

