#!/usr/bin/env python3
"""
∞ AbëKEYs Encrypted Vault - Git-Safe Credential Storage ∞

Pattern: ENCRYPTION × VAULT × GIT × ONE
Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ZERO)
Guardians: AEYON (999 Hz) + META (777 Hz) + ZERO (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞

ENCRYPTED KEYS IN GIT: Yes, if properly encrypted
- Uses Fernet (symmetric encryption)
- Encryption key stored separately (NOT in git)
- Encrypted vault CAN be committed to git
- Decryption happens at runtime with key
"""

import json
import base64
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptedVault:
    """Encrypted vault for git-safe credential storage"""
    
    def __init__(self, vault_path: Optional[Path] = None, key_path: Optional[Path] = None):
        """
        Initialize encrypted vault.
        
        Args:
            vault_path: Path to encrypted vault JSON file (can be in git)
            key_path: Path to encryption key file (MUST NOT be in git)
        """
        if vault_path is None:
            vault_path = Path("abekeys_vault.encrypted.json")  # Can be in git
        if key_path is None:
            key_path = Path.home() / ".abekeys" / "vault_key.key"  # NOT in git
        
        self.vault_path = Path(vault_path)
        self.key_path = Path(key_path)
        self._fernet: Optional[Fernet] = None
    
    def _get_fernet(self) -> Fernet:
        """Get or create Fernet instance"""
        if self._fernet is not None:
            return self._fernet
        
        # Load or generate key
        if self.key_path.exists():
            with open(self.key_path, 'rb') as f:
                key = f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            self.key_path.parent.mkdir(parents=True, exist_ok=True)
            self.key_path.write_bytes(key)
            self.key_path.chmod(0o600)  # Secure permissions
            print(f"⚠️  Generated new encryption key at: {self.key_path}")
            print(f"⚠️  IMPORTANT: Backup this key! It's NOT in git.")
        
        self._fernet = Fernet(key)
        return self._fernet
    
    def _derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_credential(self, service: str, data: Dict[str, Any]) -> bytes:
        """Encrypt a single credential"""
        fernet = self._get_fernet()
        json_data = json.dumps(data).encode()
        return fernet.encrypt(json_data)
    
    def decrypt_credential(self, encrypted_data: bytes) -> Dict[str, Any]:
        """Decrypt a single credential"""
        fernet = self._get_fernet()
        decrypted = fernet.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
    
    def load_vault(self) -> Dict[str, bytes]:
        """Load encrypted vault from file"""
        if not self.vault_path.exists():
            return {}
        
        with open(self.vault_path, 'rb') as f:
            vault_data = json.load(f)
        
        # Convert base64 strings back to bytes
        return {
            service: base64.b64decode(encrypted)
            for service, encrypted in vault_data.items()
        }
    
    def save_vault(self, vault_data: Dict[str, bytes]):
        """Save encrypted vault to file"""
        # Convert bytes to base64 strings for JSON
        vault_json = {
            service: base64.b64encode(encrypted).decode()
            for service, encrypted in vault_data.items()
        }
        
        with open(self.vault_path, 'w') as f:
            json.dump(vault_json, f, indent=2)
    
    def get(self, service: str) -> Optional[Dict[str, Any]]:
        """Get decrypted credential"""
        vault = self.load_vault()
        if service not in vault:
            return None
        
        try:
            return self.decrypt_credential(vault[service])
        except Exception as e:
            raise ValueError(f"Failed to decrypt credential '{service}': {e}")
    
    def set(self, service: str, data: Dict[str, Any]):
        """Set encrypted credential"""
        vault = self.load_vault()
        encrypted = self.encrypt_credential(service, data)
        vault[service] = encrypted
        self.save_vault(vault)
    
    def list_services(self) -> List[str]:
        """List all services in vault"""
        vault = self.load_vault()
        return sorted(vault.keys())
    
    def has(self, service: str) -> bool:
        """Check if service exists"""
        vault = self.load_vault()
        return service in vault


class AbekeysEncrypted:
    """AbëKEYs with encrypted vault support (git-safe)"""
    
    def __init__(self, vault_path: Optional[Path] = None, key_path: Optional[Path] = None):
        """
        Initialize encrypted AbëKEYs.
        
        Args:
            vault_path: Path to encrypted vault (can be in git repo)
            key_path: Path to encryption key (MUST be outside git)
        """
        self.encrypted_vault = EncryptedVault(vault_path, key_path)
        self.local_vault_path = Path.home() / ".abekeys" / "credentials"
    
    def get(self, service: str) -> Optional[Dict[str, Any]]:
        """
        Get credential - tries encrypted vault first, then local vault.
        
        This allows:
        - Encrypted credentials in git (shared with team)
        - Local overrides (personal credentials)
        """
        # Try encrypted vault first (from git)
        cred = self.encrypted_vault.get(service)
        if cred:
            return cred
        
        # Fall back to local vault
        local_file = self.local_vault_path / f"{service}.json"
        if local_file.exists():
            with open(local_file) as f:
                return json.load(f)
        
        return None
    
    def set_encrypted(self, service: str, data: Dict[str, Any]):
        """Add credential to encrypted vault (git-safe)"""
        self.encrypted_vault.set(service, data)
        print(f"✅ Encrypted credential '{service}' saved to {self.encrypted_vault.vault_path}")
        print(f"   This file CAN be committed to git (it's encrypted)")
        print(f"   Encryption key is at: {self.encrypted_vault.key_path} (NOT in git)")
    
    def list_all(self) -> List[str]:
        """List all services from both vaults"""
        encrypted = set(self.encrypted_vault.list_services())
        local = set()
        if self.local_vault_path.exists():
            local = {f.stem for f in self.local_vault_path.glob("*.json")}
        return sorted(encrypted | local)


if __name__ == "__main__":
    """CLI for encrypted vault management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AbëKEYs Encrypted Vault")
    parser.add_argument("command", choices=["encrypt", "decrypt", "list", "get", "set"])
    parser.add_argument("service", nargs="?", help="Service name")
    parser.add_argument("--vault", help="Path to encrypted vault file")
    parser.add_argument("--key", help="Path to encryption key file")
    
    args = parser.parse_args()
    
    vault = AbekeysEncrypted(
        vault_path=Path(args.vault) if args.vault else None,
        key_path=Path(args.key) if args.key else None
    )
    
    if args.command == "list":
        services = vault.list_all()
        print(f"Available services ({len(services)}):")
        for svc in services:
            source = "encrypted" if vault.encrypted_vault.has(svc) else "local"
            print(f"  • {svc} ({source})")
    
    elif args.command == "get":
        if not args.service:
            print("Error: Service name required")
            exit(1)
        cred = vault.get(args.service)
        if cred:
            print(json.dumps(cred, indent=2))
        else:
            print(f"Credential '{args.service}' not found")
            exit(1)
    
    elif args.command == "encrypt":
        if not args.service:
            print("Error: Service name required")
            exit(1)
        
        # Load from local vault
        local_file = vault.local_vault_path / f"{args.service}.json"
        if not local_file.exists():
            print(f"Error: Local credential '{args.service}' not found")
            exit(1)
        
        with open(local_file) as f:
            data = json.load(f)
        
        vault.set_encrypted(args.service, data)
        print(f"\n✅ Encrypted and saved to: {vault.encrypted_vault.vault_path}")
        print(f"   You can now commit this file to git!")

