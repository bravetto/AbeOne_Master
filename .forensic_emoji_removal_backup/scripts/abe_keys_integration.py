#!/usr/bin/env python3
"""
AbëKEYS Complete Integration System
Decrypts vault, integrates all credentials, connects all services

Pattern: DECRYPT → INTEGRATE → CONNECT → VALIDATE → ONE
"""

import json
import base64
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import getpass


class AbeKeysVault:
    """Complete AbëKEYS vault decryption and integration system."""
    
    def __init__(self, vault_path: Optional[Path] = None):
        """Initialize vault system."""
        if vault_path is None:
            vault_path = Path.home() / ".abekeys"
        self.vault_path = Path(vault_path)
        self.encrypted_vault = self.vault_path / "encrypted_vault.json"
        self.credentials_dir = self.vault_path / "credentials"
        self.hmac_key_file = self.vault_path / "hmac_key.key"
        self.kdf_salt_file = self.vault_path / "kdf_salt.key"
        
        # Load keys
        self.hmac_key = self._load_key(self.hmac_key_file)
        self.kdf_salt = self._load_key(self.kdf_salt_file)
        
    def _load_key(self, key_file: Path) -> Optional[bytes]:
        """Load encryption key from file."""
        if not key_file.exists():
            return None
        try:
            with open(key_file, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"⚠️  Warning: Could not load {key_file}: {e}")
            return None
    
    def _derive_key(self, password=REPLACE_ME = None) -> bytes:
        """
        Derive encryption key from password or use stored keys.
        
        Pattern: VALIDATE → DERIVE → RETURN
        """
        if password:
            # Derive from password using KDF
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.kdf_salt or b'abekeys_salt_default',
                iterations=100000,
                backend=default_backend()
            )
            return kdf.derive(password.encode())
        elif self.hmac_key:
            # Use stored HMAC key (first 32 bytes)
            return self.hmac_key[:32] if len(self.hmac_key) >= 32 else self.hmac_key.ljust(32, b'\0')
        else:
            raise ValueError("No password provided and no key files found")
    
    def decrypt_entry(self, entry: Dict[str, Any], password=REPLACE_ME = None) -> Optional[Dict[str, Any]]:
        """
        Decrypt a single vault entry.
        
        Pattern: VALIDATE → DECRYPT → PARSE → RETURN
        """
        try:
            # VALIDATE: Check encryption scheme
            if entry.get("scheme") != "AES-256-GCM":
                print(f"⚠️  Unsupported scheme: {entry.get('scheme')}")
                return None
            
            # DECRYPT: Decode base64 components
            nonce = base64.b64decode(entry["nonce_b64"])
            ciphertext = base64.b64decode(entry["ciphertext_b64"])
            tag = base64.b64decode(entry["tag_b64"])
            associated_data = base64.b64decode(entry["associated_data_b64"])
            
            # Combine ciphertext + tag for AES-GCM
            encrypted_data = ciphertext + tag
            
            # Derive key
            key = self._derive_key(password)
            
            # Decrypt
            aesgcm = AESGCM(key)
            decrypted = aesgcm.decrypt(nonce, encrypted_data, associated_data)
            
            # PARSE: Try to parse as JSON
            try:
                return json.loads(decrypted.decode())
            except json.JSONDecodeError:
                return {"raw": decrypted.decode()}
                
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return None
    
    def decrypt_vault(self, password=REPLACE_ME = None) -> Dict[str, Any]:
        """
        Decrypt entire vault.
        
        Pattern: VALIDATE → LOAD → DECRYPT → RETURN
        """
        if not self.encrypted_vault.exists():
            print(f"❌ Vault not found: {self.encrypted_vault}")
            return {}
        
        # LOAD: Read encrypted vault
        with open(self.encrypted_vault, 'r') as f:
            encrypted_data = json.load(f)
        
        # DECRYPT: Decrypt all entries
        decrypted = {}
        for service_name, entry in encrypted_data.items():
            print(f"🔓 Decrypting {service_name}...")
            decrypted_entry = self.decrypt_entry(entry, password)
            if decrypted_entry:
                decrypted[service_name] = decrypted_entry
                print(f"   ✅ {service_name} decrypted")
            else:
                print(f"   ❌ {service_name} failed")
        
        return decrypted
    
    def export_to_credentials(self, decrypted: Dict[str, Any], overwrite: bool = False):
        """
        Export decrypted credentials to credentials directory.
        
        Pattern: VALIDATE → EXPORT → SAVE
        """
        # VALIDATE: Ensure credentials directory exists
        self.credentials_dir.mkdir(parents=True, exist_ok=True)
        
        # EXPORT: Save each service as JSON file
        exported = []
        for service_name, cred_data in decrypted.items():
            cred_file = self.credentials_dir / f"{service_name}.json"
            
            if cred_file.exists() and not overwrite:
                print(f"⚠️  Skipping {service_name} (already exists)")
                continue
            
            # Format credential data
            formatted = {
                "service": service_name,
                "source": "abekeys_vault",
                **cred_data
            }
            
            # SAVE: Write to file
            with open(cred_file, 'w') as f:
                json.dump(formatted, f, indent=2)
            
            exported.append(service_name)
            print(f"✅ Exported {service_name} → {cred_file}")
        
        return exported
    
    def integrate_all(self, password=REPLACE_ME = None, export: bool = True):
        """
        Complete integration: Decrypt → Export → Integrate
        
        Pattern: DECRYPT → EXPORT → INTEGRATE → VALIDATE
        """
        print("🔥 AbëKEYS Complete Integration")
        print("=" * 60)
        
        # DECRYPT
        print("\n📦 Step 1: Decrypting vault...")
        decrypted = self.decrypt_vault(password)
        
        if not decrypted:
            print("❌ No credentials decrypted")
            return {}
        
        print(f"\n✅ Decrypted {len(decrypted)} services")
        
        # EXPORT
        if export:
            print("\n📤 Step 2: Exporting to credentials directory...")
            exported = self.export_to_credentials(decrypted, overwrite=True)
            print(f"✅ Exported {len(exported)} services")
        
        # INTEGRATE: Create integration summary
        print("\n🔗 Step 3: Integration Summary")
        print("=" * 60)
        
        integration_map = {}
        for service_name, cred_data in decrypted.items():
            # Extract API keys/tokens
            api_key = None
            if isinstance(cred_data, dict):
                api_key = cred_data.get("api_key") or cred_data.get("token") or cred_data.get("access_token")
            
            integration_map[service_name] = {
                "status": "✅ Ready" if api_key else "⚠️  No API key found",
                "has_credentials": bool(api_key),
                "credential_file": f"~/.abekeys/credentials/{service_name}.json" if export else None
            }
            
            status_icon = "✅" if api_key else "⚠️"
            print(f"{status_icon} {service_name:30s} {'Ready' if api_key else 'Needs API key'}")
        
        return {
            "decrypted": decrypted,
            "exported": exported if export else [],
            "integration_map": integration_map,
            "total_services": len(decrypted)
        }


def main():
    """CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AbëKEYS Complete Integration System")
    parser.add_argument("--password", help="Vault password (will prompt if not provided)")
    parser.add_argument("--no-export", action="store_true", help="Don't export to credentials directory")
    parser.add_argument("--service", help="Decrypt specific service only")
    
    args = parser.parse_args()
    
    vault = AbeKeysVault()
    
    # Get password if needed
    password = args.password
    if not password and vault.hmac_key is None:
        password = getpass.getpass("Enter vault password: ")
    
    # Integrate
    if args.service:
        # Decrypt single service
        with open(vault.encrypted_vault, 'r') as f:
            encrypted_data = json.load(f)
        
        if args.service not in encrypted_data:
            print(f"❌ Service '{args.service}' not found in vault")
            sys.exit(1)
        
        decrypted = vault.decrypt_entry(encrypted_data[args.service], password)
        if decrypted:
            print(json.dumps(decrypted, indent=2))
        else:
            print(f"❌ Failed to decrypt {args.service}")
            sys.exit(1)
    else:
        # Full integration
        result = vault.integrate_all(password, export=not args.no_export)
        
        print("\n" + "=" * 60)
        print(f"🎉 Integration Complete!")
        print(f"   Total Services: {result['total_services']}")
        print(f"   Exported: {len(result.get('exported', []))}")
        print("=" * 60)


if __name__ == "__main__":
    main()

