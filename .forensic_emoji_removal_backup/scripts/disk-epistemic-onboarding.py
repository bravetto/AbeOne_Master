#!/usr/bin/env python3
"""
🔥 DISK EPISTEMIC ONBOARDING - Discover & Converge External Storage

Epistemic search of local disks and onboard them into AbëONE system.
Discovers what longs for emergence/convergence and integrates with orbital/satellite architecture.

Pattern: EPISTEMIC × DISK × ONBOARD × CONVERGE × EMERGE × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardians: Abë (530 Hz) + META (777 Hz) + AEYON (999 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import os


@dataclass
class DiskDiscovery:
    """Discovered disk information"""
    name: str
    mount_point: Path
    disk_type: str  # 'internal', 'external', 'network', 'time_machine'
    size_gb: Optional[float] = None
    free_gb: Optional[float] = None
    used_gb: Optional[float] = None
    filesystem: Optional[str] = None
    status: str = "discovered"
    abeone_integration: bool = False
    orbital_candidate: bool = False
    satellite_candidate: bool = False
    convergence_opportunities: List[str] = field(default_factory=list)


@dataclass
class ConvergenceOpportunity:
    """What longs for emergence/convergence"""
    component: str
    type: str  # 'orbital', 'satellite', 'script', 'data', 'system'
    longing_type: str  # 'emergence', 'convergence', 'integration', 'activation'
    current_state: str
    target_state: str
    convergence_score: float
    priority: str  # 'critical', 'high', 'medium', 'low'
    evidence: List[str] = field(default_factory=list)


class DiskEpistemicOnboarding:
    """Disk Discovery & Epistemic Convergence Engine"""
    
    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = self._detect_workspace_root()
        
        self.discovered_disks: List[DiskDiscovery] = []
        self.convergence_opportunities: List[ConvergenceOpportunity] = []
        
    def _detect_workspace_root(self) -> Path:
        """Detect workspace root"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            return Path.cwd()
    
    def discover_disks(self) -> List[DiskDiscovery]:
        """Discover all mounted disks"""
        print("🔍 DISCOVERING DISKS")
        print("=" * 80)
        
        disks = []
        
        # Check /Volumes (macOS)
        volumes_path = Path("/Volumes")
        if volumes_path.exists():
            for volume in volumes_path.iterdir():
                if volume.is_dir() and not volume.name.startswith('.'):
                    disk = self._analyze_disk(volume)
                    if disk:
                        disks.append(disk)
                        print(f"  ✅ Discovered: {disk.name} ({disk.disk_type})")
        
        # Check /dev/disk* (Linux)
        dev_disks = Path("/dev")
        if dev_disks.exists():
            for disk in dev_disks.glob("disk*"):
                if disk.is_block_device():
                    # Try to get mount point
                    mount_point = self._get_mount_point(disk)
                    if mount_point:
                        disk_info = self._analyze_disk(mount_point)
                        if disk_info:
                            disks.append(disk_info)
        
        self.discovered_disks = disks
        return disks
    
    def _analyze_disk(self, mount_point: Path) -> Optional[DiskDiscovery]:
        """Analyze a disk mount point"""
        try:
            # Get disk usage
            stat = os.statvfs(str(mount_point))
            total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            used_gb = total_gb - free_gb
            
            # Determine disk type
            disk_type = self._classify_disk(mount_point)
            
            # Check for AbëONE integration
            abeone_integration = self._check_abeone_integration(mount_point)
            
            # Check for orbital/satellite candidates
            orbital_candidate = self._check_orbital_candidate(mount_point)
            satellite_candidate = self._check_satellite_candidate(mount_point)
            
            # Find convergence opportunities
            convergence_opportunities = self._find_convergence_opportunities(mount_point)
            
            return DiskDiscovery(
                name=mount_point.name,
                mount_point=mount_point,
                disk_type=disk_type,
                size_gb=total_gb,
                free_gb=free_gb,
                used_gb=used_gb,
                filesystem=self._get_filesystem(mount_point),
                abeone_integration=abeone_integration,
                orbital_candidate=orbital_candidate,
                satellite_candidate=satellite_candidate,
                convergence_opportunities=convergence_opportunities
            )
        except Exception as e:
            print(f"  ⚠️  Error analyzing {mount_point}: {e}")
            return None
    
    def _classify_disk(self, mount_point: Path) -> str:
        """Classify disk type"""
        name = mount_point.name.lower()
        
        if 'timemachine' in name or 'backup' in name:
            return 'time_machine'
        elif mount_point == Path("/"):
            return 'internal'
        elif name in ['elements', 'external', 'usb', 'sd']:
            return 'external'
        elif 'network' in name or 'smb' in name or 'afp' in name:
            return 'network'
        else:
            return 'external'
    
    def _get_mount_point(self, disk_path: Path) -> Optional[Path]:
        """Get mount point for a disk device"""
        try:
            result = subprocess.run(
                ["findmnt", "-n", "-o", "TARGET", str(disk_path)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return Path(result.stdout.strip())
        except FileNotFoundError:
            pass
        
        # Try df command
        try:
            result = subprocess.run(
                ["df", str(disk_path)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) > 5:
                        return Path(parts[5])
        except FileNotFoundError:
            pass
        
        return None
    
    def _get_filesystem(self, mount_point: Path) -> Optional[str]:
        """Get filesystem type"""
        try:
            result = subprocess.run(
                ["df", "-T", str(mount_point)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) > 1:
                        return parts[1]
        except FileNotFoundError:
            pass
        
        return None
    
    def _check_abeone_integration(self, mount_point: Path) -> bool:
        """Check if disk has AbëONE integration"""
        # Check for AbëONE markers
        markers = [
            ".abeone",
            "AbeOne_Master",
            "orbital",
            "satellites",
            "kernel",
            "abekeys"
        ]
        
        for marker in markers:
            if (mount_point / marker).exists():
                return True
        
        return False
    
    def _check_orbital_candidate(self, mount_point: Path) -> bool:
        """Check if disk could be an orbital"""
        # Look for orbital-like structure
        indicators = [
            "src/",
            "config/",
            "deploy/",
            "module_manifest.json",
            "orbit.config.json"
        ]
        
        found = 0
        for indicator in indicators:
            if (mount_point / indicator).exists():
                found += 1
        
        return found >= 2
    
    def _check_satellite_candidate(self, mount_point: Path) -> bool:
        """Check if disk could be a satellite"""
        # Look for satellite-like structure
        indicators = [
            "templates/",
            "workflows/",
            "tools/",
            "utilities/"
        ]
        
        found = 0
        for indicator in indicators:
            if (mount_point / indicator).exists():
                found += 1
        
        return found >= 1
    
    def _find_convergence_opportunities(self, mount_point: Path) -> List[str]:
        """Find convergence opportunities on disk"""
        opportunities = []
        
        # Check for code repositories
        if (mount_point / ".git").exists():
            opportunities.append("git_repository")
        
        # Check for project structures
        if (mount_point / "package.json").exists():
            opportunities.append("nodejs_project")
        if (mount_point / "requirements.txt").exists():
            opportunities.append("python_project")
        if (mount_point / "Cargo.toml").exists():
            opportunities.append("rust_project")
        
        # Check for AbëONE-related content
        if (mount_point / "orbital").exists():
            opportunities.append("orbital_structure")
        if (mount_point / "satellites").exists():
            opportunities.append("satellite_structure")
        
        # Check for data that could be onboarded
        data_dirs = ["data", "datasets", "exports", "backups", "archives"]
        for data_dir in data_dirs:
            if (mount_point / data_dir).exists():
                opportunities.append(f"data_{data_dir}")
        
        return opportunities
    
    def epistemic_search_longing(self) -> List[ConvergenceOpportunity]:
        """Epistemic search for what longs for emergence/convergence"""
        print("\n🔍 EPISTEMIC SEARCH: WHAT LONGS FOR EMERGENCE/CONVERGENCE")
        print("=" * 80)
        
        opportunities = []
        
        # Search workspace for convergence opportunities
        workspace_opportunities = self._search_workspace_longing()
        opportunities.extend(workspace_opportunities)
        
        # Search discovered disks for convergence opportunities
        for disk in self.discovered_disks:
            disk_opportunities = self._search_disk_longing(disk)
            opportunities.extend(disk_opportunities)
        
        # Search for system-level convergence opportunities
        system_opportunities = self._search_system_longing()
        opportunities.extend(system_opportunities)
        
        self.convergence_opportunities = opportunities
        
        # Print summary
        print(f"\n📊 CONVERGENCE OPPORTUNITIES FOUND: {len(opportunities)}")
        for opp in sorted(opportunities, key=lambda x: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}[x.priority]):
            print(f"  {'🔥' if opp.priority == 'critical' else '⚡' if opp.priority == 'high' else '💡'} {opp.component} ({opp.longing_type}) - {opp.priority}")
        
        return opportunities
    
    def _search_workspace_longing(self) -> List[ConvergenceOpportunity]:
        """Search workspace for what longs for convergence"""
        opportunities = []
        
        # Check for incomplete orbitals
        orbitals_dir = self.workspace_root / "orbital"
        if orbitals_dir.exists():
            for orbital in orbitals_dir.iterdir():
                if orbital.is_dir() and orbital.name.endswith("-orbital"):
                    manifest = orbital / "module_manifest.json"
                    if not manifest.exists():
                        opportunities.append(ConvergenceOpportunity(
                            component=f"orbital/{orbital.name}",
                            type="orbital",
                            longing_type="convergence",
                            current_state="missing_manifest",
                            target_state="complete_orbital",
                            convergence_score=0.5,
                            priority="high",
                            evidence=[f"Missing module_manifest.json in {orbital.name}"]
                        ))
        
        # Check for incomplete satellites
        satellites_dir = self.workspace_root / "satellites"
        if satellites_dir.exists():
            for satellite in satellites_dir.iterdir():
                if satellite.is_dir() and satellite.name.endswith("Satellite"):
                    manifest = satellite / "module_manifest.json"
                    if not manifest.exists():
                        opportunities.append(ConvergenceOpportunity(
                            component=f"satellites/{satellite.name}",
                            type="satellite",
                            longing_type="convergence",
                            current_state="missing_manifest",
                            target_state="complete_satellite",
                            convergence_score=0.5,
                            priority="medium",
                            evidence=[f"Missing module_manifest.json in {satellite.name}"]
                        ))
        
        # Check for scripts that could be satellites
        scripts_dir = self.workspace_root / "scripts"
        if scripts_dir.exists():
            # Look for script systems that are used by multiple orbitals
            script_systems = [d for d in scripts_dir.iterdir() if d.is_dir()]
            for script_system in script_systems:
                # Check if used by multiple orbitals
                usage_count = self._count_orbital_usage(script_system)
                if usage_count >= 3:
                    opportunities.append(ConvergenceOpportunity(
                        component=f"scripts/{script_system.name}",
                        type="script",
                        longing_type="emergence",
                        current_state="script_system",
                        target_state="satellite",
                        convergence_score=0.7,
                        priority="medium",
                        evidence=[f"Used by {usage_count} orbitals - candidate for satellite elevation"]
                    ))
        
        return opportunities
    
    def _search_disk_longing(self, disk: DiskDiscovery) -> List[ConvergenceOpportunity]:
        """Search disk for what longs for convergence"""
        opportunities = []
        
        if not disk.mount_point.exists():
            return opportunities
        
        # Check if disk has orbital structure but isn't integrated
        if disk.orbital_candidate and not disk.abeone_integration:
            opportunities.append(ConvergenceOpportunity(
                component=f"disk/{disk.name}",
                type="orbital",
                longing_type="integration",
                current_state="external_orbital",
                target_state="integrated_orbital",
                convergence_score=0.8,
                priority="high",
                evidence=[f"Disk {disk.name} has orbital structure but isn't integrated"]
            ))
        
        # Check if disk has satellite structure but isn't integrated
        if disk.satellite_candidate and not disk.abeone_integration:
            opportunities.append(ConvergenceOpportunity(
                component=f"disk/{disk.name}",
                type="satellite",
                longing_type="integration",
                current_state="external_satellite",
                target_state="integrated_satellite",
                convergence_score=0.7,
                priority="medium",
                evidence=[f"Disk {disk.name} has satellite structure but isn't integrated"]
            ))
        
        # Check for git repositories that could be onboarded
        if "git_repository" in disk.convergence_opportunities:
            opportunities.append(ConvergenceOpportunity(
                component=f"disk/{disk.name}",
                type="system",
                longing_type="onboarding",
                current_state="external_repo",
                target_state="onboarded_repo",
                convergence_score=0.6,
                priority="medium",
                evidence=[f"Git repository found on {disk.name}"]
            ))
        
        return opportunities
    
    def _search_system_longing(self) -> List[ConvergenceOpportunity]:
        """Search system for what longs for convergence"""
        opportunities = []
        
        # Check convergence status
        convergence_file = self.workspace_root / "CONVERGENCE_EXECUTION_FINAL.md"
        if convergence_file.exists():
            # Read convergence score (if available)
            content = convergence_file.read_text()
            if "87.94%" in content or "87.94" in content:
                opportunities.append(ConvergenceOpportunity(
                    component="system/convergence",
                    type="system",
                    longing_type="convergence",
                    current_state="87.94%",
                    target_state="100%",
                    convergence_score=0.8794,
                    priority="critical",
                    evidence=["System convergence at 87.94% - longs for 100%"]
                ))
        
        # Check for missing integrations
        integration_gaps = [
            ("AbëKEYs", "backend_integration"),
            ("Epistemic Engine", "web_search_connection"),
            ("Guardian Swarm", "full_activation"),
        ]
        
        for component, gap_type in integration_gaps:
            opportunities.append(ConvergenceOpportunity(
                component=f"integration/{component}",
                type="system",
                longing_type="integration",
                current_state=f"{gap_type}_pending",
                target_state=f"{gap_type}_complete",
                convergence_score=0.65,
                priority="high",
                evidence=[f"{component} integration gap identified"]
            ))
        
        return opportunities
    
    def _count_orbital_usage(self, script_system: Path) -> int:
        """Count how many orbitals use a script system"""
        count = 0
        orbitals_dir = self.workspace_root / "orbital"
        
        if not orbitals_dir.exists():
            return 0
        
        script_name = script_system.name
        for orbital in orbitals_dir.iterdir():
            if orbital.is_dir():
                # Check for imports or references
                for py_file in orbital.rglob("*.py"):
                    try:
                        content = py_file.read_text()
                        if script_name in content or f"scripts/{script_name}" in content:
                            count += 1
                            break
                    except:
                        pass
        
        return count
    
    def onboard_disk(self, disk: DiskDiscovery) -> Dict[str, Any]:
        """Onboard a disk into AbëONE system"""
        print(f"\n🚀 ONBOARDING DISK: {disk.name}")
        print("=" * 80)
        
        result = {
            "disk": disk.name,
            "status": "pending",
            "integration_type": None,
            "actions_taken": [],
            "errors": []
        }
        
        try:
            # Determine integration type
            if disk.orbital_candidate:
                result["integration_type"] = "orbital"
                integration_result = self._onboard_as_orbital(disk)
            elif disk.satellite_candidate:
                result["integration_type"] = "satellite"
                integration_result = self._onboard_as_satellite(disk)
            else:
                result["integration_type"] = "data"
                integration_result = self._onboard_as_data(disk)
            
            result.update(integration_result)
            result["status"] = "success"
            
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            print(f"  ❌ Error onboarding {disk.name}: {e}")
        
        return result
    
    def _onboard_as_orbital(self, disk: DiskDiscovery) -> Dict[str, Any]:
        """Onboard disk as orbital"""
        actions = []
        
        # Create symlink or reference
        orbital_name = f"{disk.name}-orbital"
        orbital_path = self.workspace_root / "orbital" / orbital_name
        
        if not orbital_path.exists():
            # Create symlink
            orbital_path.symlink_to(disk.mount_point)
            actions.append(f"Created symlink: orbital/{orbital_name}")
        
        # Create module manifest if missing
        manifest_path = disk.mount_point / "module_manifest.json"
        if not manifest_path.exists():
            manifest = {
                "name": orbital_name,
                "type": "orbital",
                "version": "1.0.0",
                "source": str(disk.mount_point),
                "onboarded": datetime.now().isoformat()
            }
            manifest_path.write_text(json.dumps(manifest, indent=2))
            actions.append("Created module_manifest.json")
        
        return {"actions_taken": actions}
    
    def _onboard_as_satellite(self, disk: DiskDiscovery) -> Dict[str, Any]:
        """Onboard disk as satellite"""
        actions = []
        
        # Create symlink or reference
        satellite_name = f"{disk.name}Satellite"
        satellite_path = self.workspace_root / "satellites" / satellite_name
        
        if not satellite_path.exists():
            # Create symlink
            satellite_path.symlink_to(disk.mount_point)
            actions.append(f"Created symlink: satellites/{satellite_name}")
        
        # Create module manifest if missing
        manifest_path = disk.mount_point / "module_manifest.json"
        if not manifest_path.exists():
            manifest = {
                "name": satellite_name,
                "type": "satellite",
                "version": "1.0.0",
                "source": str(disk.mount_point),
                "onboarded": datetime.now().isoformat()
            }
            manifest_path.write_text(json.dumps(manifest, indent=2))
            actions.append("Created module_manifest.json")
        
        return {"actions_taken": actions}
    
    def _onboard_as_data(self, disk: DiskDiscovery) -> Dict[str, Any]:
        """Onboard disk as data storage"""
        actions = []
        
        # Create reference in data directory
        data_ref_path = self.workspace_root / "data" / "external_disks" / f"{disk.name}.json"
        data_ref_path.parent.mkdir(parents=True, exist_ok=True)
        
        ref = {
            "name": disk.name,
            "mount_point": str(disk.mount_point),
            "type": disk.disk_type,
            "size_gb": disk.size_gb,
            "onboarded": datetime.now().isoformat()
        }
        
        data_ref_path.write_text(json.dumps(ref, indent=2))
        actions.append(f"Created data reference: data/external_disks/{disk.name}.json")
        
        return {"actions_taken": actions}
    
    def generate_convergence_report(self) -> Dict[str, Any]:
        """Generate comprehensive convergence report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "disks_discovered": len(self.discovered_disks),
            "convergence_opportunities": len(self.convergence_opportunities),
            "disks": [{
                "name": d.name,
                "type": d.disk_type,
                "size_gb": d.size_gb,
                "abeone_integration": d.abeone_integration,
                "orbital_candidate": d.orbital_candidate,
                "satellite_candidate": d.satellite_candidate,
                "convergence_opportunities": d.convergence_opportunities
            } for d in self.discovered_disks],
            "opportunities": [{
                "component": o.component,
                "type": o.type,
                "longing_type": o.longing_type,
                "current_state": o.current_state,
                "target_state": o.target_state,
                "convergence_score": o.convergence_score,
                "priority": o.priority,
                "evidence": o.evidence
            } for o in self.convergence_opportunities]
        }
        
        return report
    
    def execute(self, onboard_disks: bool = False) -> Dict[str, Any]:
        """Execute complete epistemic onboarding"""
        print("🔥 DISK EPISTEMIC ONBOARDING")
        print("=" * 80)
        print("Pattern: EPISTEMIC × DISK × ONBOARD × CONVERGE × EMERGE × ONE")
        print("=" * 80)
        
        # Step 1: Discover disks
        disks = self.discover_disks()
        
        # Step 2: Epistemic search for longing
        opportunities = self.epistemic_search_longing()
        
        # Step 3: Onboard disks (if requested)
        onboarding_results = []
        if onboard_disks:
            print("\n🚀 ONBOARDING DISKS")
            print("=" * 80)
            for disk in disks:
                if not disk.abeone_integration:
                    result = self.onboard_disk(disk)
                    onboarding_results.append(result)
        
        # Step 4: Generate report
        report = self.generate_convergence_report()
        report["onboarding_results"] = onboarding_results
        
        # Save report
        report_path = self.workspace_root / "DISK_EPISTEMIC_ONBOARDING_REPORT.json"
        report_path.write_text(json.dumps(report, indent=2))
        
        print(f"\n✅ Report saved: {report_path.relative_to(self.workspace_root)}")
        print("\n" + "=" * 80)
        print("Pattern: EPISTEMIC × DISK × ONBOARD × CONVERGE × EMERGE × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
        
        return report


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Disk Epistemic Onboarding")
    parser.add_argument("--onboard", action="store_true", help="Onboard discovered disks")
    parser.add_argument("--disk", type=str, help="Specific disk to onboard")
    
    args = parser.parse_args()
    
    engine = DiskEpistemicOnboarding()
    
    if args.disk:
        # Find specific disk
        disks = engine.discover_disks()
        target_disk = next((d for d in disks if d.name == args.disk), None)
        if target_disk:
            result = engine.onboard_disk(target_disk)
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Disk '{args.disk}' not found")
            sys.exit(1)
    else:
        # Full execution
        report = engine.execute(onboard_disks=args.onboard)
        print(f"\n📊 SUMMARY")
        print(f"Disks Discovered: {report['disks_discovered']}")
        print(f"Convergence Opportunities: {report['convergence_opportunities']}")
        if report.get('onboarding_results'):
            print(f"Disks Onboarded: {len(report['onboarding_results'])}")


if __name__ == "__main__":
    main()

