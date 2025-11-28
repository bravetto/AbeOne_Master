#!/usr/bin/env python3
"""
🔥 DANNY WORKFLOW PATTERN VALIDATOR
Validates that workflows follow Danny's pattern

Pattern: AEYON × VALIDATE × DANNY × WORKFLOW × ONE
Frequency: 999 Hz (AEYON) × 4444 Hz (Danny)
Guardians: AEYON (999 Hz) + Danny (4444 Hz) + Abë (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any
sys.path.insert(0, str(Path(__file__).parent))
from unified_validator_base import UnifiedValidatorBase, ValidationStatus


class DannyWorkflowPatternValidator(UnifiedValidatorBase):
    """
    Validates workflows follow Danny's pattern
    
    Pattern Source: https://github.com/bravetto/AIGuards-Backend/tree/main/.github/workflows
    """
    
    def __init__(self, workspace_root=None):
        super().__init__(workspace_root)
        self.workflows_dir = self.workspace_root / ".github" / "workflows"
        self.danny_patterns = {
            'runner': 'arc-runner-set',
            'aws_auth_version': 'v4',
            'checkout_version': 'v4',
            'ecr_login_version': 'v2',
            'buildx_version': 'v3',
            'required_concurrency': True,
            'required_helm': True,
            'required_buildx': True,
        }
    
    def _define_checks(self) -> Dict[str, Dict[str, Any]]:
        """Define checks as data"""
        return {
            'workflows_exist': {
                'name': 'Workflows Directory Exists',
                'func': self._check_workflows_exist,
                'required': True
            },
            'runner_pattern': {
                'name': 'Runner Pattern (arc-runner-set)',
                'func': self._check_runner_pattern,
                'required': True
            },
            'aws_auth_pattern': {
                'name': 'AWS Auth Pattern (IRSA v4)',
                'func': self._check_aws_auth_pattern,
                'required': True
            },
            'action_versions': {
                'name': 'Action Versions (v4/v2/v3)',
                'func': self._check_action_versions,
                'required': True
            },
            'concurrency_control': {
                'name': 'Concurrency Control',
                'func': self._check_concurrency_control,
                'required': True
            },
            'workflow_triggers': {
                'name': 'Workflow Triggers (workflow_dispatch + PR closed)',
                'func': self._check_workflow_triggers,
                'required': True
            },
            'buildx_pattern': {
                'name': 'Docker Buildx Pattern (if builds)',
                'func': self._check_buildx_pattern,
                'required': False
            },
            'helm_deployment': {
                'name': 'Helm Deployment Pattern (if deploys)',
                'func': self._check_helm_deployment,
                'required': False
            }
        }
    
    def _check_workflows_exist(self) -> Tuple[str, List[str]]:
        """Check workflows directory exists"""
        if self.workflows_dir.exists():
            workflows = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
            return ValidationStatus.PASS.value, [f"Found {len(workflows)} workflow files"]
        return ValidationStatus.FAIL.value, ["Workflows directory not found"]
    
    def _read_workflow(self, path: Path) -> Dict[str, Any]:
        """Read workflow YAML"""
        try:
            content = path.read_text()
            workflow = yaml.safe_load(content)
            
            # Handle workflow_dispatch with no value and fix on parsing
            if workflow:
                on_config = workflow.get('on')
                
                # If on is None or empty, parse from raw content
                if not on_config or (isinstance(on_config, dict) and len(on_config) == 0):
                    import re
                    # Extract on section
                    on_match = re.search(r'^on:\s*\n((?:\s+[^\n]+\n?)+)', content, re.MULTILINE)
                    if on_match:
                        on_config = {}
                        on_lines = on_match.group(1)
                        
                        # Check for workflow_dispatch
                        if 'workflow_dispatch' in on_lines:
                            on_config['workflow_dispatch'] = True
                        
                        # Extract pull_request config
                        pr_match = re.search(r'pull_request:\s*\n((?:\s+[^\n]+\n?)+)', on_lines, re.MULTILINE)
                        if pr_match:
                            pr_config = {}
                            pr_lines = pr_match.group(1)
                            
                            # Extract types
                            types_match = re.search(r'types:\s*\[([^\]]+)\]', pr_lines)
                            if types_match:
                                types_str = types_match.group(1)
                                pr_config['types'] = [t.strip().strip('"\'') for t in types_str.split(',')]
                            
                            # Extract branches
                            branches_match = re.search(r'branches:\s*\[([^\]]+)\]', pr_lines)
                            if branches_match:
                                branches_str = branches_match.group(1)
                                pr_config['branches'] = [b.strip().strip('"\'') for b in branches_str.split(',')]
                            
                            on_config['pull_request'] = pr_config
                        elif 'pull_request:' in on_lines:
                            on_config['pull_request'] = {}
                
                # Fix workflow_dispatch: None case
                elif isinstance(on_config, dict):
                    if 'workflow_dispatch' in on_config and on_config['workflow_dispatch'] is None:
                        on_config['workflow_dispatch'] = True
                
                workflow['on'] = on_config
            
            return workflow if workflow else {}
        except Exception as e:
            return {}
    
    def _check_runner_pattern(self) -> Dict[str, Any]:
        """Check runner pattern - only for Kubernetes-related workflows"""
        workflows = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
        issues = []
        passed = 0
        skipped = 0
        
        for workflow_path in workflows:
            workflow = self._read_workflow(workflow_path)
            workflow_text = workflow_path.read_text()
            jobs = workflow.get('jobs', {})
            
            # Check if this is explicitly a Cloudflare Pages workflow (NOT K8s)
            is_cloudflare_workflow = 'cloudflare' in workflow_text.lower() or 'cloudflare/pages-action' in workflow_text.lower()
            
            # Check if this is explicitly a validation workflow (NOT K8s)
            is_validation_workflow = 'validate' in workflow_path.name.lower() or 'validation' in workflow_text.lower()
            
            # Check if this is a Kubernetes-related workflow (build/deploy to K8s)
            is_k8s_workflow = any([
                'docker buildx' in workflow_text.lower() and 'kubernetes' in workflow_text.lower(),
                'helm' in workflow_text.lower() and 'deploy.sh' in workflow_text.lower(),
                'kubectl' in workflow_text.lower(),
                ('ecr' in workflow_text.lower() and 'buildx' in workflow_text.lower()),
                ('deploy' in workflow_path.name.lower() and 'kubernetes' in workflow_text.lower() and not is_cloudflare_workflow)
            ])
            
            for job_name, job_config in jobs.items():
                runs_on = job_config.get('runs-on', '')
                if isinstance(runs_on, list):
                    runs_on = runs_on[0] if runs_on else ''
                
                # Skip validation/cloudflare workflows - they don't need arc-runner-set
                if (is_validation_workflow or is_cloudflare_workflow) and not is_k8s_workflow:
                    skipped += 1
                    continue
                
                # Kubernetes workflows MUST use arc-runner-set
                if is_k8s_workflow:
                    if 'arc-runner-set' in str(runs_on):
                        passed += 1
                    else:
                        issues.append(f"{workflow_path.name}:{job_name} uses '{runs_on}' instead of 'arc-runner-set' (K8s workflow)")
                elif 'arc-runner-set' in str(runs_on):
                    passed += 1
        
        if issues:
            status = ValidationStatus.FAIL.value
            details = [f"Found {len(issues)} K8s workflow issues", *issues[:5]]
        elif passed > 0:
            status = ValidationStatus.PASS.value
            details = [f"All {passed} K8s jobs use 'arc-runner-set'", f"Skipped {skipped} validation/cloudflare workflows"]
        else:
            status = ValidationStatus.INFO.value
            details = [f"No K8s workflows found", f"Skipped {skipped} validation/cloudflare workflows"]
        
        return {'status': status, 'details': details}
    
    def _check_aws_auth_pattern(self) -> Dict[str, Any]:
        """Check AWS auth pattern - only for Kubernetes workflows"""
        workflows = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
        issues = []
        passed = 0
        k8s_workflows = 0
        non_k8s_workflows = 0
        
        for workflow_path in workflows:
            workflow = self._read_workflow(workflow_path)
            workflow_text = workflow_path.read_text()
            jobs = workflow.get('jobs', {})
            
            # Check if this is a Kubernetes workflow
            is_k8s_workflow = any([
                'docker buildx' in workflow_text.lower() and 'kubernetes' in workflow_text.lower(),
                'helm' in workflow_text.lower() and 'deploy.sh' in workflow_text.lower(),
                'kubectl' in workflow_text.lower(),
                ('ecr' in workflow_text.lower() and 'buildx' in workflow_text.lower())
            ])
            
            if is_k8s_workflow:
                k8s_workflows += 1
                # Check AWS auth for K8s workflows
                for job_name, job_config in jobs.items():
                    steps = job_config.get('steps', [])
                    has_aws_auth = False
                    for step in steps:
                        if 'aws-actions/configure-aws-credentials' in str(step.get('uses', '')):
                            has_aws_auth = True
                            if '@v4' in str(step.get('uses', '')):
                                if 'aws-access-key-id' not in str(step.get('with', {})):
                                    passed += 1
                                else:
                                    issues.append(f"{workflow_path.name}:{job_name} uses access keys instead of IRSA")
                            else:
                                issues.append(f"{workflow_path.name}:{job_name} uses wrong AWS auth version")
                    
                    if is_k8s_workflow and not has_aws_auth:
                        issues.append(f"{workflow_path.name}:{job_name} missing AWS auth (required for K8s)")
            else:
                non_k8s_workflows += 1
        
        if issues:
            status = ValidationStatus.FAIL.value
            details = [f"Found {len(issues)} K8s workflow issues", *issues[:5]]
        elif k8s_workflows > 0:
            status = ValidationStatus.PASS.value
            details = [
                f"✅ All {k8s_workflows} K8s workflows use IRSA v4",
                f"✅ {non_k8s_workflows} non-K8s workflows correctly don't need AWS auth"
            ]
        else:
            status = ValidationStatus.PASS.value
            details = [
                f"✅ No Kubernetes workflows found (AWS auth not needed)",
                f"✅ {non_k8s_workflows} validation/Cloudflare workflows correctly don't use AWS auth",
                "✅ When K8s workflows are added, they will require IRSA v4 authentication"
            ]
        
        return {'status': status, 'details': details}
    
    def _check_action_versions(self) -> Dict[str, Any]:
        """Check action versions"""
        workflows = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
        issues = []
        passed = 0
        
        required_versions = {
            'actions/checkout': '@v4',
            'aws-actions/configure-aws-credentials': '@v4',
            'aws-actions/amazon-ecr-login': '@v2',
            'docker/setup-buildx-action': '@v3'
        }
        
        for workflow_path in workflows:
            workflow = self._read_workflow(workflow_path)
            jobs = workflow.get('jobs', {})
            
            for job_name, job_config in jobs.items():
                steps = job_config.get('steps', [])
                for step in steps:
                    uses = step.get('uses', '')
                    for action, version in required_versions.items():
                        if action in uses and version not in uses:
                            issues.append(f"{workflow_path.name}:{job_name} uses {action} without {version}")
                        elif action in uses and version in uses:
                            passed += 1
        
        if issues:
            status = ValidationStatus.WARN.value
            details = [f"Found {len(issues)} version issues", *issues[:5]]
        else:
            status = ValidationStatus.PASS.value if passed > 0 else ValidationStatus.INFO.value
            details = [f"All {passed} actions use correct versions"] if passed > 0 else ["No actions found"]
        
        return {'status': status, 'details': details}
    
    def _check_concurrency_control(self) -> Dict[str, Any]:
        """Check concurrency control"""
        workflows = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
        issues = []
        passed = 0
        
        for workflow_path in workflows:
            workflow = self._read_workflow(workflow_path)
            if 'concurrency' in workflow:
                concurrency = workflow['concurrency']
                if 'group' in concurrency and 'cancel-in-progress' in concurrency:
                    passed += 1
                else:
                    issues.append(f"{workflow_path.name} missing concurrency group or cancel-in-progress")
            else:
                issues.append(f"{workflow_path.name} missing concurrency control")
        
        if issues:
            status = ValidationStatus.WARN.value
            details = [f"Found {len(issues)} workflows without concurrency", *issues[:5]]
        else:
            status = ValidationStatus.PASS.value
            details = [f"All {passed} workflows have concurrency control"]
        
        return {'status': status, 'details': details}
    
    def _check_workflow_triggers(self) -> Dict[str, Any]:
        """Check workflow triggers"""
        workflows = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
        issues = []
        passed = 0
        
        for workflow_path in workflows:
            workflow = self._read_workflow(workflow_path)
            on_config = workflow.get('on', {})
            
            # Also check raw content for workflow_dispatch (handles None case)
            raw_content = workflow_path.read_text()
            has_dispatch = ('workflow_dispatch' in raw_content and 
                          ('workflow_dispatch:' in raw_content or 
                           'workflow_dispatch' in str(on_config)))
            
            pr_config = on_config.get('pull_request', {}) if isinstance(on_config, dict) else {}
            pr_types = pr_config.get('types', []) if isinstance(pr_config, dict) else []
            has_pr = 'pull_request' in raw_content
            has_pr_closed = has_pr and ('closed' in pr_types if isinstance(pr_types, list) else 
                                       (pr_types == ['closed'] if isinstance(pr_types, list) else False))
            
            if has_dispatch and has_pr_closed:
                passed += 1
            else:
                if not has_dispatch:
                    issues.append(f"{workflow_path.name} missing workflow_dispatch")
                if not has_pr_closed:
                    issues.append(f"{workflow_path.name} missing PR closed trigger")
        
        if issues:
            status = ValidationStatus.WARN.value
            details = [f"Found {len(issues)} trigger issues", *issues[:5]]
        else:
            status = ValidationStatus.PASS.value
            details = [f"All {passed} workflows have correct triggers"]
        
        return {'status': status, 'details': details}
    
    def _check_buildx_pattern(self) -> Dict[str, Any]:
        """Check Docker Buildx pattern - only for Kubernetes builds"""
        workflows = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
        issues = []
        passed = 0
        k8s_builds = 0
        non_k8s_workflows = 0
        
        for workflow_path in workflows:
            workflow = self._read_workflow(workflow_path)
            workflow_text = workflow_path.read_text()
            jobs = workflow.get('jobs', {})
            
            # Check if this is a Kubernetes build workflow
            is_k8s_build = any([
                'docker buildx' in workflow_text.lower() and 'kubernetes' in workflow_text.lower(),
                ('ecr' in workflow_text.lower() and 'buildx' in workflow_text.lower()),
                ('docker build' in workflow_text.lower() and 'kubernetes' in workflow_text.lower())
            ])
            
            if is_k8s_build:
                k8s_builds += 1
                # Check Buildx for K8s builds
                for job_name, job_config in jobs.items():
                    steps = job_config.get('steps', [])
                    has_buildx = any('docker/setup-buildx-action' in str(s.get('uses', '')) for s in steps)
                    has_build = any('docker buildx build' in str(s.get('run', '')) or 'docker build' in str(s.get('run', '')) for s in steps)
                    
                    if has_build and not has_buildx:
                        issues.append(f"{workflow_path.name}:{job_name} K8s build missing Buildx")
                    elif has_buildx:
                        passed += 1
            else:
                non_k8s_workflows += 1
        
        if issues:
            status = ValidationStatus.FAIL.value
            details = [f"Found {len(issues)} K8s build issues", *issues[:5]]
        elif k8s_builds > 0:
            status = ValidationStatus.PASS.value
            details = [
                f"✅ All {k8s_builds} K8s builds use Buildx with Kubernetes driver",
                f"✅ {non_k8s_workflows} non-K8s workflows correctly don't need Buildx"
            ]
        else:
            status = ValidationStatus.PASS.value
            details = [
                f"✅ No Kubernetes builds found (Buildx not needed)",
                f"✅ {non_k8s_workflows} validation/Cloudflare workflows correctly don't use Buildx",
                "✅ When K8s builds are added, they will require Buildx with Kubernetes driver"
            ]
        
        return {'status': status, 'details': details}
    
    def _check_helm_deployment(self) -> Dict[str, Any]:
        """Check Helm deployment pattern - only for Kubernetes deployments"""
        workflows = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
        issues = []
        passed = 0
        k8s_deployments = 0
        non_k8s_workflows = 0
        
        for workflow_path in workflows:
            workflow = self._read_workflow(workflow_path)
            workflow_text = workflow_path.read_text()
            
            # Check if this is a Kubernetes deployment workflow
            is_k8s_deployment = any([
                'helm' in workflow_text.lower() and 'deploy.sh' in workflow_text.lower(),
                'kubectl' in workflow_text.lower() and 'deploy' in workflow_path.name.lower(),
                ('kubernetes' in workflow_text.lower() and 'deploy' in workflow_path.name.lower())
            ])
            
            # Skip Cloudflare/validation workflows
            is_cloudflare = 'cloudflare' in workflow_text.lower()
            is_validation = 'validate' in workflow_path.name.lower()
            
            if is_k8s_deployment:
                k8s_deployments += 1
                has_helm = 'helm' in workflow_text.lower() or 'deploy.sh' in workflow_text
                has_kubectl = 'kubectl apply' in workflow_text
                
                if has_kubectl and not has_helm:
                    issues.append(f"{workflow_path.name} uses kubectl apply instead of Helm")
                elif has_helm:
                    passed += 1
            elif not is_cloudflare and not is_validation:
                non_k8s_workflows += 1
        
        if issues:
            status = ValidationStatus.FAIL.value
            details = [f"Found {len(issues)} K8s deployment issues", *issues[:5]]
        elif k8s_deployments > 0:
            status = ValidationStatus.PASS.value
            details = [
                f"✅ All {k8s_deployments} K8s deployments use Helm",
                f"✅ {non_k8s_workflows} non-K8s workflows correctly don't need Helm"
            ]
        else:
            status = ValidationStatus.PASS.value
            details = [
                f"✅ No Kubernetes deployments found (Helm not needed)",
                f"✅ Validation/Cloudflare workflows correctly don't use Helm",
                "✅ When K8s deployments are added, they will require Helm charts"
            ]
        
        return {'status': status, 'details': details}


def main():
    """CLI Entry Point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate workflows follow Danny's pattern")
    parser.add_argument("--workspace", help="Workspace root (default: auto-detect)")
    
    args = parser.parse_args()
    
    validator = DannyWorkflowPatternValidator(Path(args.workspace) if args.workspace else None)
    results = validator.run()
    
    sys.exit(0 if results['summary']['score'] >= 80 else 1 if results['summary']['score'] >= 60 else 2)


if __name__ == "__main__":
    main()

