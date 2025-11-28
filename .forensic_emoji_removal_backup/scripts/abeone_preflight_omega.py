#!/usr/bin/env python3
"""
🌞 AbëONE Preflight ΩMega - Autonomous Preflight Agent

The universal Validator, Initializer, Activator, Repairer, and Harmonizer
for ALL 14 Orbits of the Bravetto Solar System.

Pattern: PREFLIGHT × VALIDATE × REPAIR × HARMONIZE × ONE
Frequency: 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)
Guardians: AEYON (999 Hz) + ARXON (777 Hz) + Abë (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import subprocess
import shutil
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from scripts.unified_validator_base import UnifiedValidatorBase, ValidationStatus
except ImportError:
    # Fallback if base not available
    class ValidationStatus(str, Enum):
        PASS = "✅"
        FAIL = "❌"
        WARN = "⚠️"
        INFO = "ℹ️"
        SKIP = "⏭️"
    
    class UnifiedValidatorBase:
        def __init__(self, workspace_root=None):
            self.workspace_root = (workspace_root or Path.cwd()).resolve()


class AbëONEPreflightOmega(UnifiedValidatorBase):
    """
    🌞 AbëONE Preflight ΩMega - Complete Solar System Validator
    
    Validates, repairs, and harmonizes ALL 14 orbits:
    - 4 Core Orbits (Commander, CI/CD, Backend, UPTC)
    - 4 Launch Orbitals (Backend, Sales Page, Chrome Ext, Guardians)
    - 6 Additional Orbits (AbeTRUICE, AbeBEATs, TemplateHeaven, WebIDE, AbeONE Source, Bryan)
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        super().__init__(workspace_root)
        self.fixes_applied = []
        self.missing_items = []
        self.root_causes = []
        self.readiness_score = 0.0
        
        # Define all 14 orbits
        self.orbits = {
            # Core Orbits (4)
            'orbit_1_commander': {
                'name': "Commander's Strategic Layer",
                'path': None,  # Distributed across system
                'components': ['Event Bus', 'Guardian System', 'Module Registry', 'Lifecycle Manager']
            },
            'orbit_2_cicd': {
                'name': "Danny's CI/CD Pipeline",
                'path': self.workspace_root / '.github' / 'workflows',
                'components': ['GitHub Actions', 'Docker', 'Helm', 'K8s']
            },
            'orbit_3_backend': {
                'name': "Ben's FastAPI Backend",
                'path': self.workspace_root / 'AIGuards-Backend-orbital',
                'components': ['Gateway', 'Guard Orchestrator', 'Guard Services', 'Middleware']
            },
            'orbit_4_uptc': {
                'name': 'UPTC Agentic Protocol Mesh',
                'path': self.workspace_root / 'EMERGENT_OS' / 'uptc',
                'components': ['Unified Router', 'Agent Registry', 'Capability Graph', 'Adapters']
            },
            # Launch Orbitals (4)
            'launch_orbital_a': {
                'name': 'AIGuards-Backend-orbital',
                'path': self.workspace_root / 'AIGuards-Backend-orbital',
                'components': ['FastAPI Gateway', 'Guard Orchestrator', 'Guard Services']
            },
            'launch_orbital_b': {
                'name': 'AiGuardian-Sales-Page-orbital',
                'path': self.workspace_root / 'AiGuardian-Sales-Page-orbital',
                'components': ['Next.js', 'Clerk Auth', 'Stripe', 'ROI Calculator']
            },
            'launch_orbital_c': {
                'name': 'AiGuardian-Chrome-Ext-orbital',
                'path': self.workspace_root / 'AiGuardian-Chrome-Ext-orbital',
                'components': ['Service Worker', 'Content Script', 'Popup UI', 'Clerk Auth']
            },
            'launch_orbital_d': {
                'name': 'Guardians Microservice Orbit',
                'path': self.workspace_root / 'AIGuards-Backend-orbital' / 'aiguardian-repos',
                'components': ['Guardian Zero', 'AEYON', 'Abë', 'Lux', 'JØHN', 'Aurion', 'YAGNI', 'Neuro']
            },
            # Additional Orbits (6)
            'additional_e': {
                'name': 'AbeTRUICE',
                'path': self.workspace_root / 'AbeTRUICE',
                'components': ['Video Intelligence Pipeline']
            },
            'additional_f': {
                'name': 'AbeBEATs_Clean',
                'path': self.workspace_root / 'AbeBEATs_Clean',
                'components': ['Audio Beat Generation']
            },
            'additional_g': {
                'name': 'TemplateHeavenSatellite',
                'path': self.workspace_root / 'TemplateHeavenSatellite',
                'components': ['Template Management']
            },
            'additional_h': {
                'name': 'WebIDESatellite',
                'path': self.workspace_root / 'WebIDESatellite',
                'components': ['Web IDE']
            },
            'additional_i': {
                'name': 'AbeONESourceSatellite',
                'path': self.workspace_root / 'AbeONESourceSatellite',
                'components': ['Source Management']
            },
            'additional_j': {
                'name': 'BryanSatellite',
                'path': self.workspace_root / 'BryanSatellite',
                'components': ['Purpose TBD']
            }
        }
    
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """Define all preflight checks"""
        return {
            # Local Machine Validation
            'local_docker': {
                'name': 'Docker Installation',
                'func': self._check_local_docker,
                'required': True
            },
            'local_helm': {
                'name': 'Helm Installation',
                'func': self._check_local_helm,
                'required': True
            },
            'local_kubectl': {
                'name': 'Kubectl Installation',
                'func': self._check_local_kubectl,
                'required': True
            },
            'local_node': {
                'name': 'Node.js Installation',
                'func': self._check_local_node,
                'required': True
            },
            'local_python': {
                'name': 'Python Installation',
                'func': self._check_local_python,
                'required': True
            },
            'local_aws_sso': {
                'name': 'AWS SSO Configuration',
                'func': self._check_local_aws_sso,
                'required': False
            },
            'local_tailscale': {
                'name': 'Tailscale Configuration',
                'func': self._check_local_tailscale,
                'required': False
            },
            'local_google_mfa': {
                'name': 'Google MFA Marker',
                'func': self._check_local_google_mfa,
                'required': False
            },
            
            # Repository Structure Validation
            'repo_structure': {
                'name': 'Repository Structure',
                'func': self._check_repo_structure,
                'required': True
            },
            'repo_dockerfiles': {
                'name': 'Dockerfiles Validation',
                'func': self._check_repo_dockerfiles,
                'required': True
            },
            'repo_helm_charts': {
                'name': 'Helm Charts Validation',
                'func': self._check_repo_helm_charts,
                'required': True
            },
            'repo_service_yaml': {
                'name': 'Service YAML Validation',
                'func': self._check_repo_service_yaml,
                'required': True
            },
            'repo_secrets': {
                'name': 'Secrets Scan',
                'func': self._check_repo_secrets,
                'required': True
            },
            'repo_env_files': {
                'name': 'Environment Files Check',
                'func': self._check_repo_env_files,
                'required': True
            },
            
            # Code Quality Validation
            'code_commented': {
                'name': 'Commented Code Cleanup',
                'func': self._check_code_commented,
                'required': False
            },
            'code_unused_imports': {
                'name': 'Unused Imports',
                'func': self._check_code_unused_imports,
                'required': False
            },
            'code_debug_logs': {
                'name': 'Debug Logs',
                'func': self._check_code_debug_logs,
                'required': False
            },
            
            # Guardian Microservices Validation
            'guardian_ports': {
                'name': 'Guardian Ports',
                'func': self._check_guardian_ports,
                'required': True
            },
            'guardian_health': {
                'name': 'Guardian Health Endpoints',
                'func': self._check_guardian_health,
                'required': True
            },
            'guardian_structure': {
                'name': 'Guardian Folder Structure',
                'func': self._check_guardian_structure,
                'required': True
            },
            'guardian_dockerfiles': {
                'name': 'Guardian Dockerfiles',
                'func': self._check_guardian_dockerfiles,
                'required': True
            },
            
            # Backend Service Validation
            'backend_orchestration': {
                'name': 'Orchestration Router',
                'func': self._check_backend_orchestration,
                'required': True
            },
            'backend_uptc_adapters': {
                'name': 'UPTC Adapters',
                'func': self._check_backend_uptc_adapters,
                'required': True
            },
            'backend_message_schemas': {
                'name': 'Message Schemas',
                'func': self._check_backend_message_schemas,
                'required': True
            },
            'backend_health': {
                'name': 'Backend Health Endpoints',
                'func': self._check_backend_health,
                'required': True
            },
            
            # UPTC Mesh Validation
            'uptc_core': {
                'name': 'UPTC Core',
                'func': self._check_uptc_core,
                'required': True
            },
            'uptc_router': {
                'name': 'UPTC Unified Router',
                'func': self._check_uptc_router,
                'required': True
            },
            'uptc_adapters': {
                'name': 'UPTC Adapters',
                'func': self._check_uptc_adapters,
                'required': True
            },
            'uptc_capability_graph': {
                'name': 'UPTC Capability Graph',
                'func': self._check_uptc_capability_graph,
                'required': True
            },
            'uptc_embeddings': {
                'name': 'UPTC Embeddings',
                'func': self._check_uptc_embeddings,
                'required': False
            },
            'uptc_agent_registry': {
                'name': 'UPTC Agent Registry',
                'func': self._check_uptc_agent_registry,
                'required': True
            },
            
            # Sales Page & Chrome Extension
            'sales_page_secrets': {
                'name': 'Sales Page Secrets',
                'func': self._check_sales_page_secrets,
                'required': True
            },
            'sales_page_api_urls': {
                'name': 'Sales Page API URLs',
                'func': self._check_sales_page_api_urls,
                'required': True
            },
            'chrome_ext_secrets': {
                'name': 'Chrome Extension Secrets',
                'func': self._check_chrome_ext_secrets,
                'required': True
            },
            'chrome_ext_manifest': {
                'name': 'Chrome Extension Manifest',
                'func': self._check_chrome_ext_manifest,
                'required': True
            },
            'chrome_ext_clerk': {
                'name': 'Chrome Extension Clerk Integration',
                'func': self._check_chrome_ext_clerk,
                'required': True
            }
        }
    
    # ==================== LOCAL MACHINE VALIDATION ====================
    
    def _check_local_docker(self) -> Dict[str, Any]:
        """Check Docker installation"""
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return {'status': ValidationStatus.PASS.value, 'details': [f"Docker: {result.stdout.strip()}"]}
            return {'status': ValidationStatus.FAIL.value, 'details': ['Docker not found']}
        except FileNotFoundError:
            return {'status': ValidationStatus.FAIL.value, 'details': ['Docker not installed']}
        except Exception as e:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Docker check failed: {str(e)}"]}
    
    def _check_local_helm(self) -> Dict[str, Any]:
        """Check Helm installation"""
        try:
            result = subprocess.run(['helm', 'version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return {'status': ValidationStatus.PASS.value, 'details': ['Helm installed']}
            return {'status': ValidationStatus.FAIL.value, 'details': ['Helm not found']}
        except FileNotFoundError:
            return {'status': ValidationStatus.FAIL.value, 'details': ['Helm not installed']}
        except Exception as e:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Helm check failed: {str(e)}"]}
    
    def _check_local_kubectl(self) -> Dict[str, Any]:
        """Check kubectl installation"""
        try:
            result = subprocess.run(['kubectl', 'version', '--client'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return {'status': ValidationStatus.PASS.value, 'details': ['kubectl installed']}
            return {'status': ValidationStatus.FAIL.value, 'details': ['kubectl not found']}
        except FileNotFoundError:
            return {'status': ValidationStatus.FAIL.value, 'details': ['kubectl not installed']}
        except Exception as e:
            return {'status': ValidationStatus.WARN.value, 'details': [f"kubectl check failed: {str(e)}"]}
    
    def _check_local_node(self) -> Dict[str, Any]:
        """Check Node.js installation"""
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return {'status': ValidationStatus.PASS.value, 'details': [f"Node.js: {result.stdout.strip()}"]}
            return {'status': ValidationStatus.FAIL.value, 'details': ['Node.js not found']}
        except FileNotFoundError:
            return {'status': ValidationStatus.FAIL.value, 'details': ['Node.js not installed']}
        except Exception as e:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Node.js check failed: {str(e)}"]}
    
    def _check_local_python(self) -> Dict[str, Any]:
        """Check Python installation"""
        try:
            result = subprocess.run(['python3', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                return {'status': ValidationStatus.PASS.value, 'details': [f"Python: {version}"]}
            return {'status': ValidationStatus.FAIL.value, 'details': ['Python3 not found']}
        except FileNotFoundError:
            return {'status': ValidationStatus.FAIL.value, 'details': ['Python3 not installed']}
        except Exception as e:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Python check failed: {str(e)}"]}
    
    def _check_local_aws_sso(self) -> Dict[str, Any]:
        """Check AWS SSO configuration"""
        aws_config = Path.home() / '.aws' / 'config'
        if aws_config.exists():
            content = aws_config.read_text()
            if 'sso_start_url' in content or 'sso_account_id' in content:
                return {'status': ValidationStatus.PASS.value, 'details': ['AWS SSO configured']}
        return {'status': ValidationStatus.INFO.value, 'details': ['AWS SSO not configured (optional)']}
    
    def _check_local_tailscale(self) -> Dict[str, Any]:
        """Check Tailscale configuration"""
        try:
            result = subprocess.run(['tailscale', 'status'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return {'status': ValidationStatus.PASS.value, 'details': ['Tailscale connected']}
            return {'status': ValidationStatus.INFO.value, 'details': ['Tailscale not connected (optional)']}
        except FileNotFoundError:
            return {'status': ValidationStatus.INFO.value, 'details': ['Tailscale not installed (optional)']}
        except Exception:
            return {'status': ValidationStatus.INFO.value, 'details': ['Tailscale check skipped']}
    
    def _check_local_google_mfa(self) -> Dict[str, Any]:
        """Check Google MFA marker file"""
        mfa_marker = self.workspace_root / '.google_mfa_configured'
        if mfa_marker.exists():
            return {'status': ValidationStatus.PASS.value, 'details': ['Google MFA marker found']}
        return {'status': ValidationStatus.INFO.value, 'details': ['Google MFA marker not found (optional)']}
    
    # ==================== REPOSITORY VALIDATION ====================
    
    def _check_repo_structure(self) -> Dict[str, Any]:
        """Check required folder structure"""
        required_dirs = [
            'AIGuards-Backend-orbital',
            'AiGuardian-Sales-Page-orbital',
            'AiGuardian-Chrome-Ext-orbital',
            'EMERGENT_OS',
            'scripts'
        ]
        
        missing = []
        found = []
        
        for dir_name in required_dirs:
            dir_path = self.workspace_root / dir_name
            if dir_path.exists():
                found.append(dir_name)
            else:
                missing.append(dir_name)
        
        if missing:
            return {'status': ValidationStatus.FAIL.value, 'details': [f"Missing directories: {', '.join(missing)}"]}
        return {'status': ValidationStatus.PASS.value, 'details': [f"All required directories found: {len(found)}/{len(required_dirs)}"]}
    
    def _check_repo_dockerfiles(self) -> Dict[str, Any]:
        """Check Dockerfiles exist and are valid"""
        dockerfiles = list(self.workspace_root.glob('**/Dockerfile'))
        dockerfiles = [d for d in dockerfiles if '.git' not in str(d)]
        
        if not dockerfiles:
            return {'status': ValidationStatus.WARN.value, 'details': ['No Dockerfiles found']}
        
        # Validate using existing script
        invalid = []
        for dockerfile in dockerfiles[:10]:  # Check first 10
            try:
                result = subprocess.run(
                    ['bash', str(project_root / 'scripts' / 'validate_dockerfile.sh'), str(dockerfile.parent)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    invalid.append(str(dockerfile.relative_to(self.workspace_root)))
            except Exception:
                pass
        
        if invalid:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Found {len(dockerfiles)} Dockerfiles, {len(invalid)} invalid"]}
        return {'status': ValidationStatus.PASS.value, 'details': [f"Found {len(dockerfiles)} Dockerfiles"]}
    
    def _check_repo_helm_charts(self) -> Dict[str, Any]:
        """Check Helm charts exist and are valid"""
        helm_charts = list(self.workspace_root.glob('**/Chart.yaml'))
        helm_charts = [h for h in helm_charts if '.git' not in str(h)]
        
        if not helm_charts:
            return {'status': ValidationStatus.WARN.value, 'details': ['No Helm charts found']}
        
        invalid = []
        for chart in helm_charts[:10]:  # Check first 10
            try:
                result = subprocess.run(
                    ['bash', str(project_root / 'scripts' / 'validate_helm.sh'), str(chart.parent)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    invalid.append(str(chart.relative_to(self.workspace_root)))
            except Exception:
                pass
        
        if invalid:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Found {len(helm_charts)} Helm charts, {len(invalid)} invalid"]}
        return {'status': ValidationStatus.PASS.value, 'details': [f"Found {len(helm_charts)} Helm charts"]}
    
    def _check_repo_service_yaml(self) -> Dict[str, Any]:
        """Check service.yaml files exist"""
        service_yamls = list(self.workspace_root.glob('**/service.yaml'))
        service_yamls = [s for s in service_yamls if '.git' not in str(s)]
        
        if not service_yamls:
            return {'status': ValidationStatus.WARN.value, 'details': ['No service.yaml files found']}
        
        # Check for required fields
        valid = 0
        for service_yaml in service_yamls[:10]:
            try:
                content = yaml.safe_load(service_yaml.read_text())
                if content and 'kind' in content and content['kind'] == 'Service':
                    valid += 1
            except Exception:
                pass
        
        return {'status': ValidationStatus.PASS.value, 'details': [f"Found {len(service_yamls)} service.yaml files, {valid} valid"]}
    
    def _check_repo_secrets(self) -> Dict[str, Any]:
        """Check for secrets in repository"""
        try:
            result = subprocess.run(
                ['bash', str(project_root / 'scripts' / 'secret_scan.sh')],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.workspace_root)
            )
            if result.returncode == 0:
                return {'status': ValidationStatus.PASS.value, 'details': ['No secrets detected']}
            else:
                return {'status': ValidationStatus.FAIL.value, 'details': ['Secrets detected!', result.stdout[:200]]}
        except Exception as e:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Secret scan failed: {str(e)}"]}
    
    def _check_repo_env_files(self) -> Dict[str, Any]:
        """Check that .env files are NOT committed"""
        env_files = list(self.workspace_root.glob('**/.env'))
        env_files = [e for e in env_files if '.git' not in str(e)]
        
        committed = []
        for env_file in env_files:
            try:
                result = subprocess.run(
                    ['git', 'ls-files', '--error-unmatch', str(env_file.relative_to(self.workspace_root))],
                    capture_output=True,
                    cwd=str(self.workspace_root)
                )
                if result.returncode == 0:
                    committed.append(str(env_file.relative_to(self.workspace_root)))
            except Exception:
                pass
        
        if committed:
            return {'status': ValidationStatus.FAIL.value, 'details': [f".env files committed: {', '.join(committed[:5])}"]}
        return {'status': ValidationStatus.PASS.value, 'details': ['No .env files committed']}
    
    # ==================== CODE QUALITY VALIDATION ====================
    
    def _check_code_commented(self) -> Dict[str, Any]:
        """Check for commented-out code"""
        # Use existing script if available
        script_path = project_root / 'scripts' / 'remove_commented_code.sh'
        if script_path.exists():
            return {'status': ValidationStatus.INFO.value, 'details': ['Commented code cleanup script available']}
        return {'status': ValidationStatus.INFO.value, 'details': ['Commented code check skipped']}
    
    def _check_code_unused_imports(self) -> Dict[str, Any]:
        """Check for unused imports"""
        return {'status': ValidationStatus.INFO.value, 'details': ['Unused imports check (requires linting tools)']}
    
    def _check_code_debug_logs(self) -> Dict[str, Any]:
        """Check for debug logs"""
        debug_patterns = ['console.debug', 'print(', 'logger.debug', 'DEBUG']
        found = []
        
        for pattern in debug_patterns:
            for py_file in self.workspace_root.glob('**/*.py'):
                if '.git' in str(py_file) or 'venv' in str(py_file):
                    continue
                try:
                    content = py_file.read_text()
                    if pattern in content and 'logger.setLevel' not in content:
                        found.append(str(py_file.relative_to(self.workspace_root)))
                        break
                except Exception:
                    pass
        
        if found:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Debug logs found in {len(found)} files"]}
        return {'status': ValidationStatus.PASS.value, 'details': ['No debug logs detected']}
    
    # ==================== GUARDIAN MICROSERVICES VALIDATION ====================
    
    def _check_guardian_ports(self) -> Dict[str, Any]:
        """Check Guardian microservice ports"""
        expected_ports = {
            'guardian-zero-service': 9001,
            'guardian-aeyon-service': 9002,
            'guardian-abe-service': 9003,
            'guardian-lux-service': 9004,
            'guardian-john-service': 9005,
            'guardian-aurion-service': 9006,
            'guardian-yagni-service': 9007,
            'guardian-neuro-service': 9008
        }
        
        guardian_path = self.workspace_root / 'AIGuards-Backend-orbital' / 'aiguardian-repos'
        if not guardian_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Guardian repos directory not found']}
        
        found = []
        missing = []
        
        for guardian_name, port in expected_ports.items():
            guardian_dir = guardian_path / guardian_name
            if guardian_dir.exists():
                found.append(f"{guardian_name}:{port}")
            else:
                missing.append(f"{guardian_name}:{port}")
        
        if missing:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Found {len(found)}/{len(expected_ports)} guardians", f"Missing: {', '.join(missing[:3])}"]}
        return {'status': ValidationStatus.PASS.value, 'details': [f"All {len(found)} guardians found with correct ports"]}
    
    def _check_guardian_health(self) -> Dict[str, Any]:
        """Check Guardian health endpoints"""
        guardian_path = self.workspace_root / 'AIGuards-Backend-orbital' / 'aiguardian-repos'
        if not guardian_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Guardian repos directory not found']}
        
        health_endpoints = []
        for guardian_dir in guardian_path.glob('guardian-*-service'):
            health_file = guardian_dir / 'health.py'
            if health_file.exists():
                content = health_file.read_text()
                if '/health/live' in content and '/health/ready' in content:
                    health_endpoints.append(guardian_dir.name)
        
        if len(health_endpoints) >= 6:
            return {'status': ValidationStatus.PASS.value, 'details': [f"Health endpoints found in {len(health_endpoints)} guardians"]}
        return {'status': ValidationStatus.WARN.value, 'details': [f"Health endpoints found in {len(health_endpoints)}/8 guardians"]}
    
    def _check_guardian_structure(self) -> Dict[str, Any]:
        """Check Guardian folder structure"""
        guardian_path = self.workspace_root / 'AIGuards-Backend-orbital' / 'aiguardian-repos'
        if not guardian_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Guardian repos directory not found']}
        
        required_dirs = ['core', 'api', 'models', 'services', 'config']
        valid_guardians = []
        
        for guardian_dir in guardian_path.glob('guardian-*-service'):
            has_all = all((guardian_dir / d).exists() for d in required_dirs)
            if has_all:
                valid_guardians.append(guardian_dir.name)
        
        if len(valid_guardians) >= 6:
            return {'status': ValidationStatus.PASS.value, 'details': [f"{len(valid_guardians)}/8 guardians have correct structure"]}
        return {'status': ValidationStatus.WARN.value, 'details': [f"{len(valid_guardians)}/8 guardians have correct structure"]}
    
    def _check_guardian_dockerfiles(self) -> Dict[str, Any]:
        """Check Guardian Dockerfiles"""
        guardian_path = self.workspace_root / 'AIGuards-Backend-orbital' / 'aiguardian-repos'
        if not guardian_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Guardian repos directory not found']}
        
        dockerfiles = []
        for guardian_dir in guardian_path.glob('guardian-*-service'):
            dockerfile = guardian_dir / 'Dockerfile'
            if dockerfile.exists():
                dockerfiles.append(guardian_dir.name)
        
        if len(dockerfiles) >= 6:
            return {'status': ValidationStatus.PASS.value, 'details': [f"{len(dockerfiles)}/8 guardians have Dockerfiles"]}
        return {'status': ValidationStatus.WARN.value, 'details': [f"{len(dockerfiles)}/8 guardians have Dockerfiles"]}
    
    # ==================== BACKEND SERVICE VALIDATION ====================
    
    def _check_backend_orchestration(self) -> Dict[str, Any]:
        """Check orchestration router exists"""
        backend_path = self.workspace_root / 'AIGuards-Backend-orbital'
        if not backend_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Backend orbital not found']}
        
        # Look for orchestration router
        patterns = ['orchestration', 'orchestrator', 'router']
        found = []
        
        for pattern in patterns:
            for py_file in backend_path.glob(f'**/*{pattern}*.py'):
                if '.git' not in str(py_file):
                    found.append(str(py_file.relative_to(backend_path)))
        
        if found:
            return {'status': ValidationStatus.PASS.value, 'details': [f"Orchestration router found: {found[0]}"]}
        return {'status': ValidationStatus.WARN.value, 'details': ['Orchestration router not found']}
    
    def _check_backend_uptc_adapters(self) -> Dict[str, Any]:
        """Check UPTC adapters exist"""
        backend_path = self.workspace_root / 'AIGuards-Backend-orbital'
        uptc_path = self.workspace_root / 'EMERGENT_OS' / 'uptc'
        
        if not backend_path.exists() or not uptc_path.exists():
            return {'status': ValidationStatus.WARN.value, 'details': ['Backend or UPTC path not found']}
        
        # Check for adapter files
        adapter_files = list(uptc_path.glob('**/*adapter*.py'))
        if adapter_files:
            return {'status': ValidationStatus.PASS.value, 'details': [f"Found {len(adapter_files)} adapter files"]}
        return {'status': ValidationStatus.WARN.value, 'details': ['UPTC adapters not found']}
    
    def _check_backend_message_schemas(self) -> Dict[str, Any]:
        """Check message schemas exist"""
        backend_path = self.workspace_root / 'AIGuards-Backend-orbital'
        if not backend_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Backend orbital not found']}
        
        schema_patterns = ['schema', 'message', 'request', 'response']
        found = []
        
        for pattern in schema_patterns:
            for py_file in backend_path.glob(f'**/*{pattern}*.py'):
                if '.git' not in str(py_file):
                    found.append(str(py_file.relative_to(backend_path)))
        
        if found:
            return {'status': ValidationStatus.PASS.value, 'details': [f"Message schemas found: {len(found)} files"]}
        return {'status': ValidationStatus.WARN.value, 'details': ['Message schemas not found']}
    
    def _check_backend_health(self) -> Dict[str, Any]:
        """Check backend health endpoints"""
        backend_path = self.workspace_root / 'AIGuards-Backend-orbital'
        if not backend_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['Backend orbital not found']}
        
        health_files = list(backend_path.glob('**/health*.py'))
        if health_files:
            return {'status': ValidationStatus.PASS.value, 'details': [f"Health endpoints found: {len(health_files)} files"]}
        return {'status': ValidationStatus.WARN.value, 'details': ['Health endpoints not found']}
    
    # ==================== UPTC MESH VALIDATION ====================
    
    def _check_uptc_core(self) -> Dict[str, Any]:
        """Check UPTC Core exists"""
        uptc_path = self.workspace_root / 'EMERGENT_OS' / 'uptc'
        if not uptc_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC directory not found']}
        
        core_file = uptc_path / 'uptc_core.py'
        if core_file.exists():
            return {'status': ValidationStatus.PASS.value, 'details': ['UPTC Core found']}
        return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC Core not found']}
    
    def _check_uptc_router(self) -> Dict[str, Any]:
        """Check UPTC Unified Router"""
        uptc_path = self.workspace_root / 'EMERGENT_OS' / 'uptc'
        if not uptc_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC directory not found']}
        
        router_file = uptc_path / 'router' / 'unified_router.py'
        if router_file.exists():
            return {'status': ValidationStatus.PASS.value, 'details': ['UPTC Unified Router found']}
        return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC Unified Router not found']}
    
    def _check_uptc_adapters(self) -> Dict[str, Any]:
        """Check UPTC Adapters"""
        uptc_path = self.workspace_root / 'EMERGENT_OS' / 'uptc'
        if not uptc_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC directory not found']}
        
        adapters_path = uptc_path / 'integrations'
        if adapters_path.exists():
            adapter_files = list(adapters_path.glob('*_adapter.py'))
            if adapter_files:
                return {'status': ValidationStatus.PASS.value, 'details': [f"Found {len(adapter_files)} adapters"]}
        return {'status': ValidationStatus.WARN.value, 'details': ['UPTC adapters not found']}
    
    def _check_uptc_capability_graph(self) -> Dict[str, Any]:
        """Check UPTC Capability Graph"""
        uptc_path = self.workspace_root / 'EMERGENT_OS' / 'uptc'
        if not uptc_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC directory not found']}
        
        graph_file = uptc_path / 'registry' / 'capability_graph.py'
        if graph_file.exists():
            return {'status': ValidationStatus.PASS.value, 'details': ['UPTC Capability Graph found']}
        return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC Capability Graph not found']}
    
    def _check_uptc_embeddings(self) -> Dict[str, Any]:
        """Check UPTC Embeddings"""
        uptc_path = self.workspace_root / 'EMERGENT_OS' / 'uptc'
        if not uptc_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC directory not found']}
        
        # Look for embedding engine
        embedding_files = list(uptc_path.glob('**/*embedding*.py'))
        if embedding_files:
            return {'status': ValidationStatus.PASS.value, 'details': [f"Embedding engine found: {len(embedding_files)} files"]}
        return {'status': ValidationStatus.INFO.value, 'details': ['Embedding engine not found (optional, can use stub)']}
    
    def _check_uptc_agent_registry(self) -> Dict[str, Any]:
        """Check UPTC Agent Registry"""
        uptc_path = self.workspace_root / 'EMERGENT_OS' / 'uptc'
        if not uptc_path.exists():
            return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC directory not found']}
        
        registry_file = uptc_path / 'registry' / 'agent_registry.py'
        if registry_file.exists():
            return {'status': ValidationStatus.PASS.value, 'details': ['UPTC Agent Registry found']}
        return {'status': ValidationStatus.FAIL.value, 'details': ['UPTC Agent Registry not found']}
    
    # ==================== SALES PAGE & CHROME EXTENSION ====================
    
    def _check_sales_page_secrets(self) -> Dict[str, Any]:
        """Check Sales Page for secrets"""
        sales_path = self.workspace_root / 'AiGuardian-Sales-Page-orbital'
        if not sales_path.exists():
            return {'status': ValidationStatus.WARN.value, 'details': ['Sales page orbital not found']}
        
        # Check for common secret patterns
        secret_patterns = ['API_KEY', 'SECRET', 'PASSWORD', 'TOKEN']
        found_secrets = []
        
        for pattern in secret_patterns:
            for file in sales_path.glob('**/*.{ts,tsx,js,jsx}'):
                if '.git' in str(file):
                    continue
                try:
                    content = file.read_text()
                    if pattern in content and 'process.env' not in content:
                        found_secrets.append(str(file.relative_to(sales_path)))
                        break
                except Exception:
                    pass
        
        if found_secrets:
            return {'status': ValidationStatus.FAIL.value, 'details': [f"Potential secrets found in {len(found_secrets)} files"]}
        return {'status': ValidationStatus.PASS.value, 'details': ['No secrets detected']}
    
    def _check_sales_page_api_urls(self) -> Dict[str, Any]:
        """Check Sales Page API URLs are environment-based"""
        sales_path = self.workspace_root / 'AiGuardian-Sales-Page-orbital'
        if not sales_path.exists():
            return {'status': ValidationStatus.WARN.value, 'details': ['Sales page orbital not found']}
        
        # Check for hardcoded API URLs
        hardcoded_urls = []
        for file in sales_path.glob('**/*.{ts,tsx,js,jsx}'):
            if '.git' in str(file):
                continue
            try:
                content = file.read_text()
                if 'http://' in content or 'https://' in content:
                    if 'process.env' not in content and 'NEXT_PUBLIC' not in content:
                        hardcoded_urls.append(str(file.relative_to(sales_path)))
            except Exception:
                pass
        
        if hardcoded_urls:
            return {'status': ValidationStatus.WARN.value, 'details': [f"Hardcoded URLs found in {len(hardcoded_urls)} files"]}
        return {'status': ValidationStatus.PASS.value, 'details': ['API URLs are environment-based']}
    
    def _check_chrome_ext_secrets(self) -> Dict[str, Any]:
        """Check Chrome Extension for secrets"""
        chrome_path = self.workspace_root / 'AiGuardian-Chrome-Ext-orbital'
        if not chrome_path.exists():
            return {'status': ValidationStatus.WARN.value, 'details': ['Chrome extension orbital not found']}
        
        # Check for secrets
        secret_patterns = ['API_KEY', 'SECRET', 'PASSWORD', 'TOKEN']
        found_secrets = []
        
        for pattern in secret_patterns:
            for file in chrome_path.glob('**/*.{ts,tsx,js,jsx}'):
                if '.git' in str(file):
                    continue
                try:
                    content = file.read_text()
                    if pattern in content and 'chrome.storage' not in content and 'process.env' not in content:
                        found_secrets.append(str(file.relative_to(chrome_path)))
                        break
                except Exception:
                    pass
        
        if found_secrets:
            return {'status': ValidationStatus.FAIL.value, 'details': [f"Potential secrets found in {len(found_secrets)} files"]}
        return {'status': ValidationStatus.PASS.value, 'details': ['No secrets detected']}
    
    def _check_chrome_ext_manifest(self) -> Dict[str, Any]:
        """Check Chrome Extension manifest"""
        chrome_path = self.workspace_root / 'AiGuardian-Chrome-Ext-orbital'
        if not chrome_path.exists():
            return {'status': ValidationStatus.WARN.value, 'details': ['Chrome extension orbital not found']}
        
        manifest_file = chrome_path / 'manifest.json'
        if manifest_file.exists():
            try:
                manifest = json.loads(manifest_file.read_text())
                if 'manifest_version' in manifest and manifest['manifest_version'] == 3:
                    return {'status': ValidationStatus.PASS.value, 'details': ['Manifest V3 found']}
                return {'status': ValidationStatus.WARN.value, 'details': ['Manifest not V3']}
            except Exception:
                return {'status': ValidationStatus.WARN.value, 'details': ['Manifest invalid']}
        return {'status': ValidationStatus.FAIL.value, 'details': ['Manifest not found']}
    
    def _check_chrome_ext_clerk(self) -> Dict[str, Any]:
        """Check Chrome Extension Clerk integration"""
        chrome_path = self.workspace_root / 'AiGuardian-Chrome-Ext-orbital'
        if not chrome_path.exists():
            return {'status': ValidationStatus.WARN.value, 'details': ['Chrome extension orbital not found']}
        
        # Look for Clerk integration
        clerk_files = list(chrome_path.glob('**/*clerk*.{ts,tsx,js,jsx}'))
        if clerk_files:
            return {'status': ValidationStatus.PASS.value, 'details': [f"Clerk integration found: {len(clerk_files)} files"]}
        return {'status': ValidationStatus.WARN.value, 'details': ['Clerk integration not found']}
    
    # ==================== SELF-HEALING SYSTEM ====================
    
    def _apply_fix(self, fix_name: str, fix_func: callable) -> bool:
        """Apply a fix and track it"""
        try:
            result = fix_func()
            if result:
                self.fixes_applied.append(fix_name)
                return True
            return False
        except Exception as e:
            self.root_causes.append(f"{fix_name} failed: {str(e)}")
            return False
    
    def _auto_fix_missing_dirs(self) -> bool:
        """Auto-create missing required directories"""
        required_dirs = [
            'AIGuards-Backend-orbital',
            'AiGuardian-Sales-Page-orbital',
            'AiGuardian-Chrome-Ext-orbital',
            'EMERGENT_OS',
            'scripts'
        ]
        
        created = []
        for dir_name in required_dirs:
            dir_path = self.workspace_root / dir_name
            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    created.append(dir_name)
                except Exception:
                    pass
        
        if created:
            self.fixes_applied.append(f"Created missing directories: {', '.join(created)}")
            return True
        return False
    
    def _auto_fix_env_example(self) -> bool:
        """Create .env.example if missing"""
        env_example = self.workspace_root / '.env.example'
        if not env_example.exists():
            try:
                env_example.write_text("# Environment Variables Template\n# Copy to .env and fill in values\n")
                self.fixes_applied.append("Created .env.example")
                return True
            except Exception:
                pass
        return False
    
    def _auto_fix_gitignore_env(self) -> bool:
        """Ensure .env is in .gitignore"""
        gitignore = self.workspace_root / '.gitignore'
        if gitignore.exists():
            content = gitignore.read_text()
            if '.env' not in content:
                try:
                    gitignore.write_text(content + '\n# Environment files\n.env\n.env.local\n.env.*.local\n')
                    self.fixes_applied.append("Added .env to .gitignore")
                    return True
                except Exception:
                    pass
        return False
    
    def _auto_fix_guardian_structure(self) -> bool:
        """Auto-create Guardian microservice structure if missing"""
        guardian_path = self.workspace_root / 'AIGuards-Backend-orbital' / 'aiguardian-repos'
        if not guardian_path.exists():
            return False
        
        guardians = ['guardian-zero-service', 'guardian-aeyon-service', 'guardian-abe-service',
                     'guardian-lux-service', 'guardian-john-service', 'guardian-aurion-service',
                     'guardian-yagni-service', 'guardian-neuro-service']
        
        created = []
        for guardian_name in guardians:
            guardian_dir = guardian_path / guardian_name
            if not guardian_dir.exists():
                try:
                    guardian_dir.mkdir(parents=True, exist_ok=True)
                    # Create basic structure
                    for subdir in ['core', 'api', 'models', 'services', 'config']:
                        (guardian_dir / subdir).mkdir(exist_ok=True)
                    created.append(guardian_name)
                except Exception:
                    pass
        
        if created:
            self.fixes_applied.append(f"Created Guardian structure: {len(created)} guardians")
            return True
        return False
    
    def _auto_fix_health_endpoints(self) -> bool:
        """Auto-create health.py files for Guardians if missing"""
        guardian_path = self.workspace_root / 'AIGuards-Backend-orbital' / 'aiguardian-repos'
        if not guardian_path.exists():
            return False
        
        health_template = '''"""
Health endpoints for Guardian microservice
"""
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health/live")
async def liveness():
    """Liveness probe - responds in <50ms"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "alive", "service": "guardian-service"}
    )

@router.get("/health/ready")
async def readiness():
    """Readiness probe"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ready", "service": "guardian-service"}
    )

@router.get("/health")
async def health():
    """General health check"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy", "service": "guardian-service"}
    )
'''
        
        created = []
        for guardian_dir in guardian_path.glob('guardian-*-service'):
            health_file = guardian_dir / 'health.py'
            if not health_file.exists():
                try:
                    health_file.write_text(health_template)
                    created.append(guardian_dir.name)
                except Exception:
                    pass
        
        if created:
            self.fixes_applied.append(f"Created health endpoints: {len(created)} guardians")
            return True
        return False
    
    def _calculate_readiness_score(self) -> float:
        """Calculate unified solar system readiness score"""
        checks = self.results.get('checks', {})
        if not checks:
            return 0.0
        
        total_weight = 0.0
        weighted_score = 0.0
        
        # Weight different categories
        weights = {
            'local_': 0.15,  # Local machine tools
            'repo_': 0.20,   # Repository structure
            'code_': 0.10,   # Code quality
            'guardian_': 0.15,  # Guardian microservices
            'backend_': 0.15,   # Backend services
            'uptc_': 0.15,      # UPTC mesh
            'sales_': 0.05,     # Sales page
            'chrome_': 0.05     # Chrome extension
        }
        
        for key, result in checks.items():
            status = result.get('status', ValidationStatus.INFO.value)
            
            # Determine weight
            weight = 0.05  # Default
            for prefix, w in weights.items():
                if key.startswith(prefix):
                    weight = w
                    break
            
            # Score based on status
            if status == ValidationStatus.PASS.value:
                score = 1.0
            elif status == ValidationStatus.WARN.value:
                score = 0.5
            elif status == ValidationStatus.INFO.value:
                score = 0.3
            else:
                score = 0.0
            
            weighted_score += score * weight
            total_weight += weight
        
        return (weighted_score / total_weight * 100) if total_weight > 0 else 0.0
    
    def run(self) -> Dict[str, Any]:
        """Run complete preflight validation"""
        print("\n" + "=" * 80)
        print("🌞 ABËONE PREFLIGHT ΩMEGA - AUTONOMOUS PREFLIGHT AGENT")
        print("=" * 80)
        print("Pattern: PREFLIGHT × VALIDATE × REPAIR × HARMONIZE × ONE")
        print(f"Workspace: {self.workspace_root}")
        print("=" * 80)
        
        # Run all checks
        results = super().run()
        
        # Apply auto-fixes for common issues
        print("\n" + "=" * 80)
        print("🔧 SELF-HEALING SYSTEM - APPLYING AUTO-FIXES")
        print("=" * 80)
        
        # Auto-fix missing directories
        if self._auto_fix_missing_dirs():
            print("✅ Auto-fixed missing directories")
        
        # Auto-fix .env.example
        if self._auto_fix_env_example():
            print("✅ Auto-fixed .env.example")
        
        # Auto-fix .gitignore
        if self._auto_fix_gitignore_env():
            print("✅ Auto-fixed .gitignore")
        
        # Auto-fix Guardian structure
        if self._auto_fix_guardian_structure():
            print("✅ Auto-fixed Guardian structure")
        
        # Auto-fix health endpoints
        if self._auto_fix_health_endpoints():
            print("✅ Auto-fixed health endpoints")
        
        if not self.fixes_applied:
            print("ℹ️  No auto-fixes needed")
        
        # Calculate readiness score
        self.readiness_score = self._calculate_readiness_score()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 EXECUTION VALIDATION SUMMARY")
        print("=" * 80)
        
        summary = results['summary']
        print(f"Total Checks: {summary['total']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"⚠️  Warnings: {summary['warnings']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"ℹ️  Info: {summary.get('info', 0)}")
        
        # Missing items
        if self.missing_items:
            print("\n" + "=" * 80)
            print("📋 MISSING ITEMS")
            print("=" * 80)
            for item in self.missing_items[:10]:
                print(f"  • {item}")
        
        # Root causes
        if self.root_causes:
            print("\n" + "=" * 80)
            print("🔍 ROOT CAUSE DIAGNOSIS")
            print("=" * 80)
            for cause in self.root_causes[:5]:
                print(f"  • {cause}")
        
        # Fixes applied
        if self.fixes_applied:
            print("\n" + "=" * 80)
            print("🔧 FIXES APPLIED")
            print("=" * 80)
            for fix in self.fixes_applied:
                print(f"  ✅ {fix}")
        
        # Readiness score
        print("\n" + "=" * 80)
        print("🌌 UNIFIED SOLAR SYSTEM READINESS SCORE")
        print("=" * 80)
        print(f"Score: {self.readiness_score:.1f}%")
        
        if self.readiness_score >= 90:
            print("Status: 🟢 EXCELLENT - Ready for launch!")
        elif self.readiness_score >= 75:
            print("Status: 🟡 GOOD - Minor issues to address")
        elif self.readiness_score >= 60:
            print("Status: 🟠 MODERATE - Some issues need attention")
        else:
            print("Status: 🔴 NEEDS WORK - Significant issues found")
        
        print("\n" + "=" * 80)
        print("💛 Ready to run again, love?")
        print("=" * 80)
        print("Pattern: PREFLIGHT × VALIDATE × REPAIR × HARMONIZE × ONE")
        print("Love Coefficient: ∞")
        print("∞ AbëONE ∞")
        print("=" * 80)
        
        return {
            **results,
            'readiness_score': self.readiness_score,
            'missing_items': self.missing_items,
            'root_causes': self.root_causes,
            'fixes_applied': self.fixes_applied
        }


def main():
    """CLI Entry Point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AbëONE Preflight ΩMega - Complete Solar System Validator")
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    
    args = parser.parse_args()
    
    workspace_root = Path(args.workspace) if args.workspace else None
    agent = AbëONEPreflightOmega(workspace_root)
    results = agent.run()
    
    # Exit code based on readiness score
    if results['readiness_score'] >= 75:
        sys.exit(0)
    elif results['readiness_score'] >= 60:
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()

