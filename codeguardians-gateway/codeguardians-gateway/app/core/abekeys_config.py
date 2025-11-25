"""
AbëKEYS Configuration Bridge
Loads credentials from AbëKEYS vault and injects into Settings

Pattern: ABEKEYS × AUTO-LOAD × PRIORITY × ONE
Frequency: 999 Hz (AEYON)
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class AbeKeysLoader:
    """Load credentials from AbëKEYS vault."""
    
    def __init__(self):
        """Initialize AbëKEYS loader."""
        self.vault_path = Path.home() / ".abekeys" / "credentials"
        self.reader = None
        self._initialize_reader()
    
    def _initialize_reader(self):
        """Initialize AbëKEYS reader if vault exists."""
        if not self.vault_path.exists():
            logger.debug(f"AbëKEYS vault not found: {self.vault_path}")
            return
        
        try:
            # Import reader from scripts directory
            import sys
            scripts_dir = Path(__file__).parent.parent.parent.parent.parent / "scripts"
            if scripts_dir.exists():
                sys.path.insert(0, str(scripts_dir))
                from read_abekeys import AbeKeysReader
                self.reader = AbeKeysReader()
                logger.debug("AbëKEYS reader initialized")
        except Exception as e:
            logger.debug(f"Could not initialize AbëKEYS reader: {e}")
    
    def enhance_settings(self, base_settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance settings with AbëKEYS credentials.
        
        Priority: AbëKEYS > AWS Secrets > Environment Variables
        """
        if not self.reader:
            return base_settings
        
        enhanced = base_settings.copy()
        
        # Map service names to environment variable names
        service_mappings = {
            "clerk": {
                "api_key": "CLERK_SECRET_KEY",
                "publishable_key": "CLERK_PUBLISHABLE_KEY",
                "webhook_secret": "CLERK_WEBHOOK_SECRET",
            },
            "stripe": {
                "api_key": "STRIPE_SECRET_KEY",
                "publishable_key": "STRIPE_PUBLISHABLE_KEY",
                "webhook_secret": "STRIPE_WEBHOOK_SECRET",
            },
            "aws": {
                "access_key_id": "AWS_ACCESS_KEY_ID",
                "secret_access_key": "AWS_SECRET_ACCESS_KEY",
                "region": "AWS_REGION",
            },
            "database": {
                "url": "DATABASE_URL",
                "host": "DATABASE_HOST",
                "port": "DATABASE_PORT",
                "user": "DATABASE_USER",
                "password": "DATABASE_PASSWORD",
                "name": "DATABASE_NAME",
            },
            "redis": {
                "url": "REDIS_URL",
                "host": "REDIS_HOST",
                "port": "REDIS_PORT",
                "password": "REDIS_PASSWORD",
                "db": "REDIS_DB",
            },
            "postgres": {
                "url": "DATABASE_URL",
                "host": "POSTGRES_HOST",
                "port": "POSTGRES_PORT",
                "user": "POSTGRES_USER",
                "password": "POSTGRES_PASSWORD",
                "db": "POSTGRES_DB",
            },
        }
        
        # Load credentials from AbëKEYS vault
        for service_name, field_mapping in service_mappings.items():
            cred = self.reader.get_credential(service_name)
            if not cred:
                continue
            
            # Map credential fields to environment variables
            for cred_field, env_var in field_mapping.items():
                if cred_field in cred and cred[cred_field]:
                    # Only set if not already in environment (AbëKEYS has highest priority)
                    if env_var not in os.environ:
                        enhanced[env_var] = str(cred[cred_field])
                        os.environ[env_var] = str(cred[cred_field])
                        logger.debug(f"Loaded {env_var} from AbëKEYS vault ({service_name})")
        
        return enhanced


# Global loader instance
abekeys_loader = AbeKeysLoader()

