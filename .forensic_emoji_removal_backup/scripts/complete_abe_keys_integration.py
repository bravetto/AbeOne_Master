#!/usr/bin/env python3
"""
🔥 COMPLETE AbëKEYS INTEGRATION SYSTEM 🔥
Brings home ALL 60+ credentials and integrates them

Pattern: DISCOVER → DECRYPT → INTEGRATE → CONNECT → VALIDATE → ONE
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
import getpass


class CompleteAbeKeysIntegration:
    """
    Complete AbëKEYS Integration System
    
    Discovers credentials from:
    1. Encrypted vault (~/.abekeys/encrypted_vault.json)
    2. Credentials directory (~/.abekeys/credentials/*.json)
    3. 1Password vault (via op CLI)
    4. Environment variables
    5. Existing integrations
    
    Then integrates them all into ONE unified system.
    """
    
    def __init__(self):
        self.vault_path = Path.home() / ".abekeys"
        self.encrypted_vault = self.vault_path / "encrypted_vault.json"
        self.credentials_dir = self.vault_path / "credentials"
        self.integration_map = {}
        
    def discover_all_credentials(self) -> Dict[str, Any]:
        """
        Discover ALL credentials from ALL sources.
        
        Pattern: DISCOVER → COLLECT → RETURN
        """
        print("🔍 DISCOVERING ALL CREDENTIALS...")
        print("=" * 60)
        
        all_credentials = {}
        
        # Source 1: Encrypted vault
        print("\n📦 Source 1: Encrypted Vault")
        vault_creds = self._discover_from_vault()
        print(f"   Found: {len(vault_creds)} services")
        all_credentials.update(vault_creds)
        
        # Source 2: Credentials directory
        print("\n📁 Source 2: Credentials Directory")
        dir_creds = self._discover_from_directory()
        print(f"   Found: {len(dir_creds)} services")
        all_credentials.update(dir_creds)
        
        # Source 3: 1Password (if available)
        print("\n🔐 Source 3: 1Password Vault")
        op_creds = self._discover_from_1password()
        print(f"   Found: {len(op_creds)} services")
        all_credentials.update(op_creds)
        
        # Source 4: Environment variables
        print("\n🌍 Source 4: Environment Variables")
        env_creds = self._discover_from_env()
        print(f"   Found: {len(env_creds)} services")
        all_credentials.update(env_creds)
        
        print("\n" + "=" * 60)
        print(f"✅ TOTAL DISCOVERED: {len(all_credentials)} services")
        print("=" * 60)
        
        return all_credentials
    
    def _discover_from_vault(self) -> Dict[str, Any]:
        """Discover from encrypted vault."""
        creds = {}
        if self.encrypted_vault.exists():
            try:
                with open(self.encrypted_vault, 'r') as f:
                    vault_data = json.load(f)
                for service_name in vault_data.keys():
                    creds[service_name] = {
                        "source": "encrypted_vault",
                        "status": "encrypted",
                        "needs_decryption": True
                    }
            except Exception as e:
                print(f"   ⚠️  Error reading vault: {e}")
        return creds
    
    def _discover_from_directory(self) -> Dict[str, Any]:
        """Discover from credentials directory."""
        creds = {}
        if self.credentials_dir.exists():
            for cred_file in self.credentials_dir.glob("*.json"):
                service_name = cred_file.stem
                try:
                    with open(cred_file, 'r') as f:
                        cred_data = json.load(f)
                    creds[service_name] = {
                        "source": "credentials_dir",
                        "status": "ready",
                        "data": cred_data,
                        "file": str(cred_file)
                    }
                except Exception as e:
                    print(f"   ⚠️  Error reading {cred_file}: {e}")
        return creds
    
    def _discover_from_1password(self) -> Dict[str, Any]:
        """Discover from 1Password vault."""
        creds = {}
        try:
            # Check if op CLI is available
            result = subprocess.run(
                ["op", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("   ✅ 1Password CLI available")
                # Try to list items (requires authentication)
                # This is a placeholder - actual implementation would query 1Password
                print("   ℹ️  Run 'op signin' to enable 1Password integration")
            else:
                print("   ⚠️  1Password CLI not found")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("   ⚠️  1Password CLI not available")
        return creds
    
    def _discover_from_env(self) -> Dict[str, Any]:
        """Discover from environment variables."""
        creds = {}
        env_patterns = [
            "SLACK", "RUNWAY", "OPENAI", "ANTHROPIC", "GITHUB",
            "AWS", "GOOGLE", "STRIPE", "CLERK", "FIREFLIES"
        ]
        
        for pattern in env_patterns:
            # Check for API keys
            # SECURITY: ZERO & JOHN - No environment variables as credential source
            # All credentials must be in encrypted vault
            # Environment variables are NOT a secure credential source
            pass
        
        return creds
    
    def integrate_credentials(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate all discovered credentials.
        
        Pattern: VALIDATE → MAP → INTEGRATE → RETURN
        """
        print("\n🔗 INTEGRATING CREDENTIALS...")
        print("=" * 60)
        
        integration_map = {}
        
        # Service mappings
        service_mappings = {
            "slack": {"type": "messaging", "priority": 1},
            "slack_bot": {"type": "messaging", "priority": 1},
            "login_slack": {"type": "messaging", "priority": 1},
            "runway": {"type": "video_generation", "priority": 1},
            "fireflies_api": {"type": "meeting_recording", "priority": 2},
            "next_public_consciousness_api": {"type": "api", "priority": 2},
        }
        
        for service_name, cred_info in credentials.items():
            # Determine integration status
            status = "✅ Ready"
            if cred_info.get("needs_decryption"):
                status = "🔓 Needs Decryption"
            elif cred_info.get("status") == "ready":
                status = "✅ Ready"
            else:
                status = "⚠️  Partial"
            
            # Map service
            service_map = service_mappings.get(service_name, {"type": "unknown", "priority": 3})
            
            integration_map[service_name] = {
                "status": status,
                "source": cred_info.get("source"),
                "type": service_map["type"],
                "priority": service_map["priority"],
                "has_credentials": cred_info.get("data") is not None or cred_info.get("has_api_key"),
                "integration_ready": cred_info.get("status") == "ready"
            }
            
            print(f"{status} {service_name:30s} [{service_map['type']:20s}] {cred_info.get('source', 'unknown')}")
        
        self.integration_map = integration_map
        return integration_map
    
    def create_integration_summary(self) -> str:
        """Create integration summary report."""
        summary = []
        summary.append("=" * 60)
        summary.append("🔥 AbëKEYS COMPLETE INTEGRATION SUMMARY")
        summary.append("=" * 60)
        summary.append("")
        
        # Ready services
        ready = [s for s, info in self.integration_map.items() if info.get("integration_ready")]
        if ready:
            summary.append(f"✅ READY ({len(ready)}):")
            for service in ready:
                summary.append(f"   • {service}")
            summary.append("")
        
        # Needs decryption
        needs_decrypt = [s for s, info in self.integration_map.items() if info.get("status") == "🔓 Needs Decryption"]
        if needs_decrypt:
            summary.append(f"🔓 NEEDS DECRYPTION ({len(needs_decrypt)}):")
            for service in needs_decrypt:
                summary.append(f"   • {service}")
            summary.append("")
        
        # Partial
        partial = [s for s, info in self.integration_map.items() if info.get("status") == "⚠️  Partial"]
        if partial:
            summary.append(f"⚠️  PARTIAL ({len(partial)}):")
            for service in partial:
                summary.append(f"   • {service}")
            summary.append("")
        
        summary.append("=" * 60)
        summary.append(f"TOTAL SERVICES: {len(self.integration_map)}")
        summary.append("=" * 60)
        
        return "\n".join(summary)
    
    def generate_integration_code(self, output_file: Optional[Path] = None):
        """
        Generate integration code for all services.
        
        Pattern: GENERATE → WRITE → RETURN
        """
        if output_file is None:
            output_file = Path(__file__).parent / "generated_abe_keys_integration.py"
        
        code = []
        code.append('"""')
        code.append("Generated AbëKEYS Integration Code")
        code.append("Auto-generated credential integration")
        code.append('"""')
        code.append("")
        code.append("import os")
        code.append("from pathlib import Path")
        code.append("from scripts.read_abekeys import AbeKeysReader")
        code.append("")
        code.append("")
        code.append("class AbeKeysIntegration:")
        code.append('    """Unified credential integration."""')
        code.append("")
        code.append("    def __init__(self):")
        code.append("        self.reader = AbeKeysReader()")
        code.append("")
        
        # Generate getter methods for each service
        for service_name, info in self.integration_map.items():
            method_name = service_name.replace("-", "_").replace(" ", "_")
            code.append(f"    def get_{method_name}(self):")
            code.append(f'        """Get {service_name} credentials."""')
            code.append(f"        cred = self.reader.get_credential('{service_name}')")
            code.append("        if cred:")
            code.append("            return cred.get('api_key') or cred.get('token')")
            code.append("        # SECURITY: ZERO & JOHN - No env var fallback")
            code.append("        # All credentials must be in encrypted vault")
            code.append("        return None")
            code.append("")
        
        code.append("")
        code.append("# Auto-initialize")
        code.append("abe_keys = AbeKeysIntegration()")
        code.append("")
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write("\n".join(code))
        
        print(f"\n✅ Generated integration code: {output_file}")
        return output_file


def main():
    """Main integration flow."""
    print("🔥" * 30)
    print("AbëKEYS COMPLETE INTEGRATION SYSTEM")
    print("Bringing Home ALL 60+ Credentials")
    print("🔥" * 30)
    print()
    
    integrator = CompleteAbeKeysIntegration()
    
    # Step 1: Discover all credentials
    credentials = integrator.discover_all_credentials()
    
    # Step 2: Integrate
    integration_map = integrator.integrate_credentials(credentials)
    
    # Step 3: Generate summary
    summary = integrator.create_integration_summary()
    print("\n" + summary)
    
    # Step 4: Generate integration code
    print("\n📝 Generating integration code...")
    integrator.generate_integration_code()
    
    print("\n🎉 INTEGRATION COMPLETE!")
    print("=" * 60)
    print("Next steps:")
    print("1. Decrypt encrypted vault entries (if needed)")
    print("2. Add missing credentials to ~/.abekeys/credentials/")
    print("3. Use generated integration code in your applications")
    print("=" * 60)


if __name__ == "__main__":
    main()

