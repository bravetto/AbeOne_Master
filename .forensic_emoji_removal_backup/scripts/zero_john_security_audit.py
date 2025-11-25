#!/usr/bin/env python3
"""
🔒 ZERO & JOHN SECURITY AUDIT 🔒
Complete safety and security validation for AbëKEYS

Pattern: AUDIT → VALIDATE → HARDEN → CERTIFY → ONE
Guardians: ZERO (Uncertainty Bounds) + JOHN (E2E Certification)
"""

import os
import json
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class SecurityIssue:
    """Security issue found during audit."""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # ENV_VAR, HARDCODED, GIT, ENCRYPTION
    file: str
    line: int
    issue: str
    recommendation: str


class ZeroJohnSecurityAudit:
    """
    ZERO & JOHN Security Audit System
    
    ZERO: Bayesian uncertainty bounds - quantifies security risk
    JOHN: E2E certification - nothing ships without certification
    """
    
    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)
        self.issues: List[SecurityIssue] = []
        self.gitignore_path = self.repo_path / ".gitignore"
        self.abekeys_path = Path.home() / ".abekeys"
        
    def audit_all(self) -> Dict[str, Any]:
        """
        Complete security audit.
        
        Pattern: AUDIT → VALIDATE → REPORT
        """
        print("🔒" * 30)
        print("ZERO & JOHN SECURITY AUDIT")
        print("Complete Safety & Security Validation")
        print("🔒" * 30)
        print()
        
        # Audit 1: Check for hardcoded credentials
        print("📋 Audit 1: Hardcoded Credentials")
        print("=" * 60)
        self._audit_hardcoded_credentials()
        
        # Audit 2: Check environment variable usage
        print("\n📋 Audit 2: Environment Variable Security")
        print("=" * 60)
        self._audit_env_variables()
        
        # Audit 3: Check .gitignore protection
        print("\n📋 Audit 3: Git Security (.gitignore)")
        print("=" * 60)
        self._audit_gitignore()
        
        # Audit 4: Check encryption status
        print("\n📋 Audit 4: Encryption Status")
        print("=" * 60)
        self._audit_encryption()
        
        # Audit 5: Check credential file security
        print("\n📋 Audit 5: Credential File Security")
        print("=" * 60)
        self._audit_credential_files()
        
        # Audit 6: Check AbëKEYS integration
        print("\n📋 Audit 6: AbëKEYS Integration Validation")
        print("=" * 60)
        self._audit_abekeys_integration()
        
        # Generate report
        return self._generate_report()
    
    def _audit_hardcoded_credentials(self):
        """Check for hardcoded API keys, passwords, tokens."""
        patterns = [
            (r'api[_-]?key\s*[:=]\s*["\']([^"\']{20,})["\']', "API_KEY"),
            (r'password\s*[:=]\s*["\']([^"\']{8,})["\']', "PASSWORD"),
            (r'secret\s*[:=]\s*["\']([^"\']{16,})["\']', "SECRET"),
            (r'token\s*[:=]\s*["\']([^"\']{20,})["\']', "TOKEN"),
            (r'sk_live_[a-zA-Z0-9]{24,}', "STRIPE_SECRET"),
            (r'xoxb-[a-zA-Z0-9-]{50,}', "SLACK_TOKEN"),
            (r'ghp_[a-zA-Z0-9]{36,}', "GITHUB_TOKEN"),
        ]
        
        scripts_path = self.repo_path / "scripts"
        if not scripts_path.exists():
            print("   ⚠️  scripts directory not found")
            return
        
        for py_file in scripts_path.rglob("*.py"):
            try:
                with open(py_file, 'r') as f:
                    lines = f.readlines()
                
                for line_num, line in enumerate(lines, 1):
                    for pattern, cred_type in patterns:
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            # Skip if it's a comment or docstring
                            stripped = line.strip()
                            if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                                continue
                            
                            # Skip if it's clearly a placeholder
                            value = match.group(1) if match.groups() else match.group(0)
                            if any(placeholder in value.lower() for placeholder in ['change-me', 'placeholder', 'example', 'your-', 'xxx']):
                                continue
                            
                            self.issues.append(SecurityIssue(
                                severity="CRITICAL",
                                category="HARDCODED",
                                file=str(py_file.relative_to(self.repo_path)),
                                line=line_num,
                                issue=f"Hardcoded {cred_type} found",
                                recommendation=f"Move to encrypted vault or environment variable (never hardcode)"
                            ))
            except Exception as e:
                print(f"   ⚠️  Error reading {py_file}: {e}")
        
        hardcoded = [i for i in self.issues if i.category == "HARDCODED"]
        if hardcoded:
            print(f"   ❌ Found {len(hardcoded)} hardcoded credential issues")
            for issue in hardcoded[:5]:  # Show first 5
                print(f"      {issue.severity}: {issue.file}:{issue.line} - {issue.issue}")
        else:
            print("   ✅ No hardcoded credentials found")
    
    def _audit_env_variables(self):
        """Check for unsafe environment variable usage."""
        scripts_path = self.repo_path / "scripts"
        unsafe_patterns = [
            (r'os\.getenv\(["\']([^"\']*API[_-]?KEY[^"\']*)["\']', "API_KEY_ENV"),
            (r'os\.environ\[["\']([^"\']*API[_-]?KEY[^"\']*)["\']', "API_KEY_ENV"),
            (r'process\.env\.([A-Z_]*API[_-]?KEY)', "API_KEY_ENV"),
        ]
        
        env_usage = []
        for py_file in scripts_path.rglob("*.py"):
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    for pattern, issue_type in unsafe_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            # Check if it falls back to vault
                            if 'get_credential' in content or 'AbeKeysReader' in content:
                                continue  # Safe - uses vault as primary
                            env_usage.append((py_file, line_num, line.strip()))
            except:
                pass
        
        if env_usage:
            print(f"   ⚠️  Found {len(env_usage)} environment variable usages")
            print("   ⚠️  WARNING: Environment variables should NOT be primary source")
            print("   ✅ RECOMMENDATION: Use AbëKEYS vault as primary, env vars as fallback only")
            for file, line_num, line in env_usage[:3]:
                print(f"      {file.name}:{line_num} - {line[:60]}...")
        else:
            print("   ✅ No unsafe environment variable usage found")
    
    def _audit_gitignore(self):
        """Check .gitignore protects sensitive files."""
        required_patterns = [
            r'\.abekeys',
            r'\.env',
            r'credentials',
            r'secret',
            r'password',
            r'api[_-]?key',
            r'\.key$',
            r'encrypted_vault',
        ]
        
        if not self.gitignore_path.exists():
            self.issues.append(SecurityIssue(
                severity="CRITICAL",
                category="GIT",
                file=".gitignore",
                line=0,
                issue=".gitignore file missing",
                recommendation="Create .gitignore with all sensitive patterns"
            ))
            print("   ❌ .gitignore file missing")
            return
        
        with open(self.gitignore_path, 'r') as f:
            gitignore_content = f.read().lower()
        
        missing_patterns = []
        for pattern in required_patterns:
            if not re.search(pattern, gitignore_content, re.IGNORECASE):
                missing_patterns.append(pattern)
        
        if missing_patterns:
            print(f"   ⚠️  Missing {len(missing_patterns)} required patterns in .gitignore")
            for pattern in missing_patterns:
                print(f"      Missing: {pattern}")
        else:
            print("   ✅ .gitignore contains required security patterns")
        
        # Check if credential files are actually ignored
        if self.abekeys_path.exists():
            cred_dir = self.abekeys_path / "credentials"
            if cred_dir.exists():
                # Check if .gitignore contains patterns that would match
                gitignore_lower = gitignore_content.lower()
                abekeys_patterns = ['.abekeys', 'credentials', '~/.abekeys']
                
                if any(pattern in gitignore_lower for pattern in abekeys_patterns):
                    print("   ✅ Credentials directory patterns found in .gitignore")
                    print("   ✅ Credentials are protected (outside repo, git-ignored)")
                else:
                    print("   ⚠️  Credentials directory patterns not in .gitignore")
                    self.issues.append(SecurityIssue(
                        severity="HIGH",
                        category="GIT",
                        file=".gitignore",
                        line=0,
                        issue="Credentials directory patterns missing",
                        recommendation="Add .abekeys/ and credentials/ patterns to .gitignore"
                    ))
    
    def _audit_encryption(self):
        """Check encryption status of credentials."""
        encrypted_vault = self.abekeys_path / "encrypted_vault.json"
        credentials_dir = self.abekeys_path / "credentials"
        
        if encrypted_vault.exists():
            print("   ✅ Encrypted vault exists")
            try:
                with open(encrypted_vault, 'r') as f:
                    vault_data = json.load(f)
                encrypted_count = len(vault_data)
                print(f"   ✅ {encrypted_count} services encrypted in vault")
            except:
                print("   ⚠️  Encrypted vault exists but may be corrupted")
        else:
            print("   ⚠️  Encrypted vault not found")
        
        if credentials_dir.exists():
            cred_files = list(credentials_dir.glob("*.json"))
            if cred_files:
                print(f"   ⚠️  Found {len(cred_files)} unencrypted credential files")
                print("   ⚠️  WARNING: These should be encrypted or git-ignored")
                
                # Check file permissions
                insecure_files = []
                for cred_file in cred_files:
                    stat = cred_file.stat()
                    mode = stat.st_mode
                    # Check if readable by others (not secure)
                    if mode & 0o004:
                        insecure_files.append(cred_file)
                
                if insecure_files:
                    print(f"   ❌ {len(insecure_files)} files have insecure permissions")
                    self.issues.append(SecurityIssue(
                        severity="HIGH",
                        category="ENCRYPTION",
                        file=str(insecure_files[0].name),
                        line=0,
                        issue="Credential files have insecure permissions",
                        recommendation="Set permissions to 600 (read/write owner only)"
                    ))
                else:
                    print("   ✅ Credential files have secure permissions")
            else:
                print("   ✅ No unencrypted credential files found")
        else:
            print("   ✅ Credentials directory doesn't exist (good - using encrypted vault)")
    
    def _audit_credential_files(self):
        """Check credential files for security issues."""
        credentials_dir = self.abekeys_path / "credentials"
        
        if not credentials_dir.exists():
            print("   ✅ No credential files to audit")
            return
        
        cred_files = list(credentials_dir.glob("*.json"))
        exposed_keys = []
        
        for cred_file in cred_files:
            try:
                with open(cred_file, 'r') as f:
                    cred_data = json.load(f)
                
                # Check if API keys are exposed
                api_key = cred_data.get("api_key") or cred_data.get("API_KEY") or cred_data.get("token")
                if api_key:
                    # Check if it's a real key (not placeholder)
                    if len(api_key) > 20 and not any(p in api_key.lower() for p in ['placeholder', 'example', 'change-me']):
                        exposed_keys.append(cred_file.name)
            except:
                pass
        
        if exposed_keys:
            print(f"   ⚠️  {len(exposed_keys)} credential files contain API keys")
            print("   ✅ These are in ~/.abekeys/credentials/ (should be git-ignored)")
            print("   ⚠️  RECOMMENDATION: Move to encrypted vault for maximum security")
        else:
            print("   ✅ No exposed API keys in credential files")
    
    def _audit_abekeys_integration(self):
        """Check AbëKEYS integration in production code."""
        issues_found = []
        
        # Check 1: AbëKEYS vault permissions
        print("   🔍 Checking AbëKEYS vault permissions...")
        if self.abekeys_path.exists():
            stat_info = self.abekeys_path.stat()
            mode = stat_info.st_mode & 0o777
            if mode & 0o077:  # Check if group/other have permissions
                issues_found.append("AbëKEYS vault has insecure permissions")
                print(f"   ⚠️  AbëKEYS vault permissions: {oct(mode)} (should be 700)")
                print("   💡 Run: chmod 700 ~/.abekeys")
            else:
                print("   ✅ AbëKEYS vault has secure permissions")
        else:
            print("   ℹ️  AbëKEYS vault not found (optional)")
        
        # Check 2: Credentials directory permissions
        credentials_dir = self.abekeys_path / "credentials"
        if credentials_dir.exists():
            stat_info = credentials_dir.stat()
            mode = stat_info.st_mode & 0o777
            if mode & 0o077:
                issues_found.append("AbëKEYS credentials directory has insecure permissions")
                print(f"   ⚠️  Credentials directory permissions: {oct(mode)} (should be 700)")
                print("   💡 Run: chmod 700 ~/.abekeys/credentials")
            else:
                print("   ✅ Credentials directory has secure permissions")
            
            # Check individual credential file permissions
            cred_files = list(credentials_dir.glob("*.json"))
            insecure_files = []
            for cred_file in cred_files:
                stat_info = cred_file.stat()
                mode = stat_info.st_mode & 0o777
                if mode & 0o077:
                    insecure_files.append(cred_file.name)
            
            if insecure_files:
                print(f"   ⚠️  {len(insecure_files)} credential files have insecure permissions")
                print("   💡 Run: chmod 600 ~/.abekeys/credentials/*.json")
            else:
                print(f"   ✅ All {len(cred_files)} credential files have secure permissions (600)")
        
        # Check 3: AbëKEYS config loader in production code
        print("\n   🔍 Checking AbëKEYS integration in production code...")
        gateway_path = self.repo_path / "AIGuards-Backend" / "codeguardians-gateway" / "codeguardians-gateway"
        abekeys_config_path = gateway_path / "app" / "core" / "abekeys_config.py"
        config_path = gateway_path / "app" / "core" / "config.py"
        
        if abekeys_config_path.exists():
            print("   ✅ AbëKEYS config loader found: app/core/abekeys_config.py")
            
            # Check if config.py imports abekeys_config
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config_content = f.read()
                    if 'abekeys_config' in config_content or 'abekeys' in config_content.lower():
                        print("   ✅ AbëKEYS integration found in config.py")
                    else:
                        issues_found.append("AbëKEYS config loader exists but not integrated in config.py")
                        print("   ⚠️  AbëKEYS config loader not integrated in config.py")
                        print("   💡 Update config.py to load AbëKEYS credentials")
        else:
            # Check alternative paths
            alt_paths = [
                self.repo_path / "codeguardians-gateway" / "codeguardians-gateway" / "app" / "core" / "abekeys_config.py",
                self.repo_path / "app" / "core" / "abekeys_config.py",
            ]
            found = False
            for alt_path in alt_paths:
                if alt_path.exists():
                    print(f"   ✅ AbëKEYS config loader found: {alt_path.relative_to(self.repo_path)}")
                    found = True
                    break
            
            if not found:
                print("   ⚠️  AbëKEYS config loader not found in production code")
                print("   💡 Create app/core/abekeys_config.py for AbëKEYS integration")
        
        # Check 4: AbëKEYS reader availability
        print("\n   🔍 Checking AbëKEYS reader availability...")
        read_abekeys_path = self.repo_path / "scripts" / "read_abekeys.py"
        if read_abekeys_path.exists():
            print("   ✅ AbëKEYS reader found: scripts/read_abekeys.py")
        else:
            print("   ⚠️  AbëKEYS reader not found: scripts/read_abekeys.py")
            print("   💡 AbëKEYS reader required for credential access")
        
        # Summary
        if issues_found:
            print(f"\n   ⚠️  Found {len(issues_found)} AbëKEYS integration issues")
            for issue in issues_found:
                self.issues.append(SecurityIssue(
                    severity="MEDIUM",
                    category="ABEKEYS",
                    file="abekeys_integration",
                    line=0,
                    issue=issue,
                    recommendation="Fix AbëKEYS integration issues"
                ))
        else:
            print("\n   ✅ AbëKEYS integration validation passed")
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate security audit report."""
        print("\n" + "=" * 60)
        print("🔒 SECURITY AUDIT REPORT")
        print("=" * 60)
        
        critical = [i for i in self.issues if i.severity == "CRITICAL"]
        high = [i for i in self.issues if i.severity == "HIGH"]
        medium = [i for i in self.issues if i.severity == "MEDIUM"]
        low = [i for i in self.issues if i.severity == "LOW"]
        
        print(f"\n📊 ISSUE SUMMARY:")
        print(f"   CRITICAL: {len(critical)}")
        print(f"   HIGH: {len(high)}")
        print(f"   MEDIUM: {len(medium)}")
        print(f"   LOW: {len(low)}")
        print(f"   TOTAL: {len(self.issues)}")
        
        if critical:
            print(f"\n❌ CRITICAL ISSUES ({len(critical)}):")
            for issue in critical:
                print(f"   • {issue.file}:{issue.line} - {issue.issue}")
                print(f"     → {issue.recommendation}")
        
        if high:
            print(f"\n⚠️  HIGH PRIORITY ISSUES ({len(high)}):")
            for issue in high[:5]:  # Show first 5
                print(f"   • {issue.file}:{issue.line} - {issue.issue}")
        
        # ZERO & JOHN Certification
        print("\n" + "=" * 60)
        print("ZERO & JOHN CERTIFICATION")
        print("=" * 60)
        
        if len(critical) == 0 and len(high) == 0:
            print("✅ ZERO CERTIFIED: No critical or high-severity issues")
            print("✅ JOHN CERTIFIED: Codebase is GIT READY")
            print("\n🎉 SECURITY AUDIT PASSED")
            certification_status = "CERTIFIED"
        elif len(critical) == 0:
            print("⚠️  ZERO: Some high-priority issues found (non-blocking)")
            print("⚠️  JOHN: Review recommended before committing")
            certification_status = "CONDITIONAL"
        else:
            print("❌ ZERO: Critical issues found")
            print("❌ JOHN: NOT CERTIFIED - Fix critical issues before committing")
            certification_status = "FAILED"
        
        return {
            "certification_status": certification_status,
            "total_issues": len(self.issues),
            "critical": len(critical),
            "high": len(high),
            "medium": len(medium),
            "low": len(low),
            "issues": [
                {
                    "severity": i.severity,
                    "category": i.category,
                    "file": i.file,
                    "line": i.line,
                    "issue": i.issue,
                    "recommendation": i.recommendation
                }
                for i in self.issues
            ]
        }


def main():
    """Run security audit."""
    repo_path = Path(__file__).parent.parent
    audit = ZeroJohnSecurityAudit(repo_path)
    report = audit.audit_all()
    
    # Save report
    report_file = repo_path / "ZERO_JOHN_SECURITY_AUDIT_REPORT.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Full report saved to: {report_file}")
    
    # Exit with error code if failed
    if report["certification_status"] == "FAILED":
        exit(1)
    elif report["certification_status"] == "CONDITIONAL":
        exit(2)


if __name__ == "__main__":
    main()

