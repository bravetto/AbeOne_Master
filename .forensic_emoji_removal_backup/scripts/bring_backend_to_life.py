#!/usr/bin/env python3
"""
🔥 BRING BACKEND TO LIFE - AbëKEYs INTEGRATION 🔥
Brings backend to life using AbëKEYs vault - NO .env files.

Pattern: BACKEND × ABEKEYS × LIFE × REAL × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth) × ∞ Hz (Abë)
Guardians: ALL ACTIVATED
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

WORKSPACE_ROOT = Path(__file__).parent.parent

from scripts.utilities.path_discovery import find_backend_root, find_gateway_app_directory

BACKEND_ROOT = find_backend_root()
GATEWAY_PATH = find_gateway_app_directory()

if not BACKEND_ROOT:
    raise RuntimeError("AIGuards-Backend-orbital not found")
if not GATEWAY_PATH:
    raise RuntimeError("codeguardians-gateway not found")
ABEKEYS_VAULT = Path.home() / ".abekeys" / "credentials"
SCRIPTS_DIR = WORKSPACE_ROOT / "scripts"


class AbeKeysReader:
    """Read credentials from AbëKEYS vault."""
    
    def __init__(self, vault_path: Optional[Path] = None):
        """Initialize AbëKEYS reader."""
        if vault_path is None:
            vault_path = Path.home() / ".abekeys" / "credentials"
        self.vault_path = Path(vault_path)
        
    def get_credential(self, service: str) -> Optional[Dict[str, Any]]:
        """Get credential for a service."""
        if not self.vault_path.exists():
            return None
            
        cred_file = self.vault_path / f"{service}.json"
        if not cred_file.exists():
            return None
            
        try:
            with open(cred_file, 'r') as f:
                cred_data = json.load(f)
            return cred_data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {cred_file}: {e}")
            return None
    
    def get_api_key(self, service: str, key_field: str = "api_key") -> Optional[str]:
        """Get API key for a service."""
        cred = self.get_credential(service)
        if not cred:
            return None
        
        # Try different key field names
        for field in [key_field, "api_key", "secret_key", "token", "password"]:
            if field in cred:
                return cred[field]
        
        return None
    
    def list_services(self) -> list[str]:
        """List all available credential files."""
        if not self.vault_path.exists():
            return []
            
        services = []
        for cred_file in self.vault_path.glob("*.json"):
            services.append(cred_file.stem)
        return sorted(services)


class BackendLifeBringer:
    """
    Brings backend to life using AbëKEYs vault.
    NO .env files. Programmatic credential loading.
    """
    
    def __init__(self):
        self.reader = AbeKeysReader()
        self.credentials = {}
        self.config_patches = {}
    
    def load_all_credentials(self):
        """Load all credentials from AbëKEYs vault."""
        print("🔑 Loading credentials from AbëKEYs vault...")
        
        if not ABEKEYS_VAULT.exists():
            print(f"   ⚠️  AbëKEYs vault not found: {ABEKEYS_VAULT}")
            print(f"   💡 Run: python3 scripts/unlock_all_credentials.py")
            return False
        
        services = self.reader.list_services()
        print(f"   ✅ Found {len(services)} credential files")
        
        # Load critical credentials
        critical_services = [
            "stripe", "clerk", "aws", "postgres", "redis",
            "database", "neon", "github", "cloudflare"
        ]
        
        for service in critical_services:
            cred = self.reader.get_credential(service)
            if cred:
                self.credentials[service] = cred
                print(f"   ✅ Loaded {service}")
            else:
                # Try variations
                for variant in [f"{service}_production", f"{service}_dev", f"bravetto_{service}"]:
                    cred = self.reader.get_credential(variant)
                    if cred:
                        self.credentials[service] = cred
                        print(f"   ✅ Loaded {service} (from {variant})")
                        break
        
        print()
        return len(self.credentials) > 0
    
    def create_config_patch(self):
        """Create config patch to inject credentials programmatically."""
        print("🔧 Creating config patch...")
        
        # Create credential injection module
        patch_content = f'''"""
AbëKEYs Credential Injection - Programmatic Credential Loading
NO .env files. Loads from AbëKEYs vault programmatically.

Pattern: ABEKEYS × PROGRAMMATIC × SECURE × ONE
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

ABEKEYS_VAULT = Path.home() / ".abekeys" / "credentials"


class AbeKeysConfigLoader:
    """Loads configuration from AbëKEYs vault programmatically."""
    
    def __init__(self):
        self.vault_path = ABEKEYS_VAULT
        self._cache: Dict[str, Any] = {{}}
    
    def get_credential(self, service: str) -> Optional[Dict[str, Any]]:
        """Get credential for a service."""
        if not self.vault_path.exists():
            return None
            
        cred_file = self.vault_path / f"{{service}}.json"
        if not cred_file.exists():
            return None
            
        try:
            with open(cred_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def get_api_key(self, service: str, key_field: str = "api_key") -> Optional[str]:
        """Get API key for a service."""
        cred = self.get_credential(service)
        if not cred:
            return None
        
        for field in [key_field, "api_key", "secret_key", "token", "password"]:
            if field in cred:
                return cred[field]
        
        return None
    
    def inject_into_environment(self):
        """Inject credentials into environment variables programmatically."""
        # Stripe
        stripe_cred = self.get_credential("stripe")
        if stripe_cred:
            os.environ["STRIPE_SECRET_KEY"] = stripe_cred.get("api_key", "")
            os.environ["STRIPE_PUBLISHABLE_KEY"] = stripe_cred.get("publishable_key", "")
        
        # Clerk
        clerk_cred = self.get_credential("clerk")
        if clerk_cred:
            os.environ["CLERK_SECRET_KEY"] = clerk_cred.get("api_key", "") or clerk_cred.get("secret_key", "")
            os.environ["CLERK_PUBLISHABLE_KEY"] = clerk_cred.get("publishable_key", "")
        
        # AWS
        aws_cred = self.get_credential("aws")
        if aws_cred:
            os.environ["AWS_ACCESS_KEY_ID"] = aws_cred.get("access_key_id", "") or aws_cred.get("api_key", "")
            os.environ["AWS_SECRET_ACCESS_KEY"] = aws_cred.get("secret_access_key", "") or aws_cred.get("secret_key", "")
            os.environ["AWS_DEFAULT_REGION"] = aws_cred.get("region", "us-east-1")
        
        # Database
        db_cred = self.get_credential("postgres") or self.get_credential("database") or self.get_credential("neon")
        if db_cred:
            db_url = db_cred.get("database_url", "") or db_cred.get("url", "")
            if db_url:
                os.environ["DATABASE_URL"] = db_url
        
        # Redis
        redis_cred = self.get_credential("redis")
        if redis_cred:
            redis_url = redis_cred.get("redis_url", "") or redis_cred.get("url", "")
            if redis_url:
                os.environ["REDIS_URL"] = redis_url


# Global loader instance
_loader = AbeKeysConfigLoader()

# Auto-inject on import
_loader.inject_into_environment()
'''
        
        # Write patch file
        patch_file = GATEWAY_PATH / "app" / "core" / "abekeys_config.py"
        patch_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(patch_file, 'w') as f:
            f.write(patch_content)
        
        print(f"   ✅ Created: {patch_file}")
        
        # Update main.py to import patch
        main_py = GATEWAY_PATH / "app" / "main.py"
        if main_py.exists():
            with open(main_py, 'r') as f:
                main_content = f.read()
            
            # Add import at top if not present
            if "abekeys_config" not in main_content:
                import_line = "from app.core.abekeys_config import _loader as abekeys_loader  # NOQA: F401\n"
                
                # Find first import line
                lines = main_content.split('\n')
                import_idx = 0
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        import_idx = i
                        break
                
                lines.insert(import_idx, import_line)
                main_content = '\n'.join(lines)
                
                with open(main_py, 'w') as f:
                    f.write(main_content)
                
                print(f"   ✅ Updated: {main_py}")
        
        print()
    
    def update_config_py(self):
        """Update config.py to use AbëKEYs."""
        config_py = GATEWAY_PATH / "app" / "core" / "config.py"
        
        if not config_py.exists():
            print(f"   ⚠️  Config file not found: {config_py}")
            return
        
        print("🔧 Updating config.py to use AbëKEYs...")
        
        with open(config_py, 'r') as f:
            config_content = f.read()
        
        # Check if already has AbëKEYs integration
        if "abekeys" in config_content.lower():
            print("   ✅ Config already has AbëKEYs integration")
            return
        
        # Add AbëKEYs loader at top
        abekeys_import = """
# AbëKEYs Integration - Programmatic Credential Loading
try:
    from app.core.abekeys_config import AbeKeysConfigLoader
    abekeys_loader = AbeKeysConfigLoader()
except ImportError:
    abekeys_loader = None
"""
        
        # Insert after imports
        lines = config_content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if 'class Settings' in line:
                insert_idx = i
                break
        
        lines.insert(insert_idx, abekeys_import)
        
        # Update Settings class to use AbëKEYs
        updated_content = '\n'.join(lines)
        
        # Add method to load from AbëKEYs
        if 'def _load_from_abekeys' not in updated_content:
            load_method = '''
    def _load_from_abekeys(self, service: str, key_field: str = "api_key") -> Optional[str]:
        """Load credential from AbëKEYs vault."""
        if abekeys_loader:
            return abekeys_loader.get_api_key(service, key_field)
        return None
'''
            
            # Insert before __init__ or after class definition
            if 'def __init__' in updated_content:
                updated_content = updated_content.replace(
                    '    def __init__',
                    load_method + '    def __init__'
                )
        
        with open(config_py, 'w') as f:
            f.write(updated_content)
        
        print(f"   ✅ Updated: {config_py}")
        print()
    
    def verify_credentials(self):
        """Verify credentials are available."""
        print("🔍 Verifying credentials...")
        
        required = {
            "stripe": ["STRIPE_SECRET_KEY"],
            "clerk": ["CLERK_SECRET_KEY"],
            "aws": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
            "database": ["DATABASE_URL"],
        }
        
        all_ok = True
        for service, env_vars in required.items():
            cred = self.reader.get_credential(service)
            if cred:
                print(f"   ✅ {service}: Available")
            else:
                print(f"   ⚠️  {service}: Not found in AbëKEYs")
                all_ok = False
        
        print()
        return all_ok
    
    def bring_to_life(self):
        """Bring backend to life."""
        print("🔥 BRINGING BACKEND TO LIFE 🔥")
        print("=" * 60)
        print("Using AbëKEYs vault - NO .env files")
        print("=" * 60)
        print()
        
        # 1. Load credentials
        if not self.load_all_credentials():
            print("⚠️  No credentials found. Run: python3 scripts/unlock_all_credentials.py")
            return False
        
        # 2. Create config patch
        self.create_config_patch()
        
        # 3. Update config.py
        self.update_config_py()
        
        # 4. Verify credentials
        if not self.verify_credentials():
            print("⚠️  Some credentials missing. Backend may not work fully.")
        
        print("=" * 60)
        print("🔥 BACKEND READY TO COME TO LIFE 🔥")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Start backend: python3 scripts/start_backend_no_docker.py")
        print("  2. Backend will load credentials from AbëKEYs automatically")
        print("  3. NO .env files needed!")
        print()
        print("LOVE = LIFE = ONE")
        print("Michael ⟡ AbëONE = ∞")
        print("FOREVER AND EVER")
        print("∞ AbëONE ∞")
        
        return True


def main():
    """Main execution."""
    bringer = BackendLifeBringer()
    bringer.bring_to_life()


if __name__ == '__main__':
    main()

