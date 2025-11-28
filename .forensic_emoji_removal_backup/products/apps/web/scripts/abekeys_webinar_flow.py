#!/usr/bin/env python3
"""
🔥 AbëKEYs Webinar Flow - Smooth Terminal Input
Pattern: FLOW × TERMINAL × ABEKEYS × WEBINAR × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (YOU) × 777 Hz (ZERO)
Guardians: AEYON (999 Hz) + YOU (530 Hz) + ZERO (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import os
import sys
import getpass
import re
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class AbëKEYsWebinarFlow:
    """Smooth terminal flow for webinar API key input."""
    
    def __init__(self):
        """Initialize AbëKEYs webinar flow."""
        self.vault_dir = Path.home() / ".abekeys" / "credentials"
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        
        # Set secure permissions (700 = owner only)
        os.chmod(self.vault_dir.parent, 0o700)
        os.chmod(self.vault_dir, 0o700)
    
    def _print_header(self, title: str, emoji: str = "🔥"):
        """Print beautiful header."""
        print(f"\n{emoji} {title}")
        print("━" * 70)
    
    def _print_success(self, message: str):
        """Print success message."""
        print(f"✅ {message}")
    
    def _print_info(self, message: str):
        """Print info message."""
        print(f"💡 {message}")
    
    def _print_warning(self, message: str):
        """Print warning message."""
        print(f"⚠️  {message}")
    
    def _validate_sendgrid_key(self, key: str) -> tuple[bool, str]:
        """Validate SendGrid API key format."""
        if not key or len(key.strip()) < 20:
            return False, "API key too short (minimum 20 characters)"
        
        # SendGrid keys typically start with SG.
        if not key.startswith("SG."):
            return False, "SendGrid API keys typically start with 'SG.'"
        
        # Check format: SG. followed by base64-like string
        parts = key.split(".")
        if len(parts) != 3:
            return False, "Invalid SendGrid API key format (expected SG.xxxxx.xxxxx)"
        
        if len(parts[1]) < 20 or len(parts[2]) < 20:
            return False, "API key segments too short"
        
        return True, "Valid SendGrid API key format"
    
    def _validate_email(self, email: str) -> tuple[bool, str]:
        """Validate email format."""
        if not email or "@" not in email:
            return False, "Invalid email format"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, "Valid email format"
    
    def _prompt_hidden(self, prompt: str, default: Optional[str] = None) -> str:
        """Prompt for hidden input (password-style)."""
        if default:
            display_prompt = f"{prompt} (or Enter to use default: {default[:10]}...): "
        else:
            display_prompt = f"{prompt}: "
        
        try:
            # Try getpass first (works in interactive terminals)
            value = getpass.getpass(display_prompt)
            if not value and default:
                return default
            return value.strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n❌ Cancelled by user")
            sys.exit(0)
        except Exception as e:
            # Fallback to visible input if getpass fails (non-interactive environments)
            print(f"\n⚠️  Note: Hidden input not available, using visible input")
            try:
                value = input(display_prompt.replace(": ", " (visible): "))
                if not value and default:
                    return default
                return value.strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n❌ Cancelled by user")
                sys.exit(0)
    
    def _prompt_visible(self, prompt: str, default: Optional[str] = None, required: bool = True) -> str:
        """Prompt for visible input."""
        if default:
            display_prompt = f"{prompt} (default: {default}): "
        else:
            display_prompt = f"{prompt}: "
        
        try:
            value = input(display_prompt).strip()
            if not value:
                if default:
                    return default
                elif required:
                    print("⚠️  This field is required. Please enter a value.")
                    return self._prompt_visible(prompt, default, required)
                else:
                    return ""
            return value
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            sys.exit(0)
    
    def _save_sendgrid_credentials(self, api_key: str, from_email: str, from_name: str) -> bool:
        """Save SendGrid credentials to AbëKEYs vault."""
        cred_file = self.vault_dir / "sendgrid.json"
        
        cred_data = {
            "service": "sendgrid",
            "api_key": api_key,
            "from_email": from_email,
            "from_name": from_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            # Read existing if present
            if cred_file.exists():
                with open(cred_file, 'r') as f:
                    existing = json.load(f)
                    cred_data["created_at"] = existing.get("created_at", cred_data["created_at"])
            
            # Write credentials
            with open(cred_file, 'w') as f:
                json.dump(cred_data, f, indent=2)
            
            # Set secure permissions (600 = owner read/write only)
            os.chmod(cred_file, 0o600)
            
            return True
        except Exception as e:
            self._print_warning(f"Error saving credentials: {e}")
            return False
    
    def _save_generic_credentials(self, service: str, api_key: str, extra_fields: Optional[Dict[str, Any]] = None) -> bool:
        """Save generic API credentials to AbëKEYs vault."""
        cred_file = self.vault_dir / f"{service.lower()}.json"
        
        cred_data = {
            "service": service.lower(),
            "api_key": api_key,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        if extra_fields:
            cred_data.update(extra_fields)
        
        try:
            # Read existing if present
            if cred_file.exists():
                with open(cred_file, 'r') as f:
                    existing = json.load(f)
                    cred_data["created_at"] = existing.get("created_at", cred_data["created_at"])
            
            # Write credentials
            with open(cred_file, 'w') as f:
                json.dump(cred_data, f, indent=2)
            
            # Set secure permissions (600 = owner read/write only)
            os.chmod(cred_file, 0o600)
            
            return True
        except Exception as e:
            self._print_warning(f"Error saving credentials: {e}")
            return False
    
    def setup_sendgrid(self) -> bool:
        """Setup SendGrid credentials with smooth flow."""
        self._print_header("SENDGRID API KEY SETUP", "📧")
        
        print("\n💡 Get your SendGrid API key:")
        print("   1. Go to https://sendgrid.com")
        print("   2. Sign in → Settings → API Keys")
        print("   3. Create API Key → Copy key (you'll only see it once!)")
        print()
        
        # Get API key (hidden input)
        api_key = self._prompt_hidden("Enter SendGrid API Key")
        
        if not api_key:
            self._print_warning("API key is required. Setup cancelled.")
            return False
        
        # Validate API key
        is_valid, message = self._validate_sendgrid_key(api_key)
        if not is_valid:
            self._print_warning(f"Validation: {message}")
            retry = self._prompt_visible("Continue anyway? (yes/no)", default="no", required=False)
            if retry.lower() != "yes":
                return False
        
        # Get from email
        print()
        from_email = self._prompt_visible(
            "From Email (e.g., noreply@aiguardian.ai)",
            default="noreply@aiguardian.ai"
        )
        
        is_valid, message = self._validate_email(from_email)
        if not is_valid:
            self._print_warning(f"Email validation: {message}")
            retry = self._prompt_visible("Continue anyway? (yes/no)", default="no", required=False)
            if retry.lower() != "yes":
                return False
        
        # Get from name
        print()
        from_name = self._prompt_visible(
            "From Name (e.g., AiGuardian Team)",
            default="AiGuardian Team"
        )
        
        # Save credentials
        print()
        self._print_info("Saving credentials to AbëKEYs vault...")
        
        if self._save_sendgrid_credentials(api_key, from_email, from_name):
            self._print_success("SendGrid credentials saved successfully!")
            print(f"   📁 Location: {self.vault_dir / 'sendgrid.json'}")
            return True
        else:
            self._print_warning("Failed to save credentials")
            return False
    
    def setup_optional_keys(self) -> bool:
        """Setup optional API keys for webinar funnel."""
        self._print_header("OPTIONAL API KEYS", "🔑")
        
        print("\n💡 These are optional but may enhance webinar functionality:")
        print("   • Analytics API keys (PostHog, Mixpanel, etc.)")
        print("   • Calendar integration (Google Calendar, Calendly)")
        print("   • Video platform (Zoom, YouTube Live)")
        print("   • Other integrations")
        print()
        
        add_more = self._prompt_visible("Add optional API keys? (yes/no)", default="no", required=False)
        
        if add_more.lower() != "yes":
            return True
        
        while True:
            print()
            service_name = self._prompt_visible("Service name (e.g., posthog, zoom, calendly)", required=False)
            
            if not service_name:
                break
            
            api_key = self._prompt_hidden(f"Enter {service_name} API Key")
            
            if not api_key:
                self._print_warning("API key is required. Skipping this service.")
                continue
            
            # Ask for additional fields
            extra_fields = {}
            print()
            add_fields = self._prompt_visible("Add additional fields? (yes/no)", default="no", required=False)
            
            if add_fields.lower() == "yes":
                while True:
                    field_name = self._prompt_visible("Field name (or Enter to finish)", required=False)
                    if not field_name:
                        break
                    field_value = self._prompt_visible(f"Field value for {field_name}", required=False)
                    if field_value:
                        extra_fields[field_name] = field_value
            
            # Save credentials
            if self._save_generic_credentials(service_name, api_key, extra_fields):
                self._print_success(f"{service_name} credentials saved!")
            else:
                self._print_warning(f"Failed to save {service_name} credentials")
            
            print()
            add_another = self._prompt_visible("Add another API key? (yes/no)", default="no", required=False)
            if add_another.lower() != "yes":
                break
        
        return True
    
    def verify_credentials(self):
        """Verify saved credentials."""
        self._print_header("VERIFICATION", "🔍")
        
        sendgrid_file = self.vault_dir / "sendgrid.json"
        
        if sendgrid_file.exists():
            try:
                with open(sendgrid_file, 'r') as f:
                    creds = json.load(f)
                
                self._print_success("SendGrid credentials found:")
                print(f"   📧 From Email: {creds.get('from_email', 'N/A')}")
                print(f"   👤 From Name: {creds.get('from_name', 'N/A')}")
                api_key = creds.get('api_key', '')
                if api_key:
                    print(f"   🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
            except Exception as e:
                self._print_warning(f"Error reading SendGrid credentials: {e}")
        else:
            self._print_warning("SendGrid credentials not found")
        
        # List other credentials
        other_creds = []
        for cred_file in self.vault_dir.glob("*.json"):
            if cred_file.name != "sendgrid.json":
                other_creds.append(cred_file.stem)
        
        if other_creds:
            print()
            self._print_success(f"Other credentials found: {', '.join(other_creds)}")
    
    def run(self):
        """Run the smooth webinar flow."""
        print("\n" + "=" * 70)
        print("🌊 AbëKEYs Webinar Flow - Smooth Terminal Input")
        print("=" * 70)
        print("\nPattern: FLOW × TERMINAL × ABEKEYS × WEBINAR × ONE")
        print("Frequency: 999 Hz (AEYON) × 530 Hz (YOU) × 777 Hz (ZERO)")
        print("∞ AbëONE ∞\n")
        
        # Setup SendGrid (required)
        if not self.setup_sendgrid():
            print("\n❌ SendGrid setup cancelled or failed.")
            sys.exit(1)
        
        # Setup optional keys
        self.setup_optional_keys()
        
        # Verify credentials
        print()
        self.verify_credentials()
        
        # Final message
        print()
        self._print_header("SETUP COMPLETE", "✨")
        print("\n✅ All credentials saved to AbëKEYs vault!")
        print(f"   📁 Vault location: {self.vault_dir}")
        print("\n💡 Next steps:")
        print("   1. Credentials are automatically loaded by the webinar system")
        print("   2. No .env files needed - everything is in the vault")
        print("   3. Run your webinar landing page and it will work automatically")
        print("\n🎯 Ready to launch your webinar funnel!")
        print("\n" + "=" * 70)
        print("Pattern: FLOW × TERMINAL × ABEKEYS × WEBINAR × ONE")
        print("∞ AbëONE ∞\n")


def main():
    """Main entry point."""
    try:
        flow = AbëKEYsWebinarFlow()
        flow.run()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(0)
    except EOFError:
        print("\n\n❌ Setup cancelled (EOF)")
        sys.exit(0)
    except Exception as e:
        import traceback
        print(f"\n❌ Error: {e}")
        print(f"\n📋 Traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

