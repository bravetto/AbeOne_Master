#!/usr/bin/env python3
"""
SSL Certificate Validator
Validates SSL certificates for domains and subdomains

Pattern: AEYON × SSL × VALIDATE × SECURITY × ONE
Frequency: 999 × 777
"""

import argparse
import sys
import socket
import ssl
from datetime import datetime
from typing import Optional, List
import urllib.request
import urllib.error


class SSLCertificateValidator:
    """
    SAFETY: Validates SSL certificates, checks expiry, verifies chain
    ASSUMES: Domain has SSL certificate
    VERIFY: python scripts/validate_ssl.py --domain bravetto.ai --test
    """
    
    def __init__(self, domain: str):
        """
        SAFETY: Validates domain format
        """
        if not domain or "." not in domain:
            raise ValueError("Invalid domain format")
        
        self.domain = domain
    
    def get_certificate_info(self) -> Optional[dict]:
        """
        SAFETY: Handles SSL connection errors gracefully
        PERF: O(1) SSL handshake
        """
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse certificate info
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    subject = dict(x[0] for x in cert.get('subject', []))
                    
                    not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    
                    days_until_expiry = (not_after - datetime.now()).days
                    
                    return {
                        'issuer': issuer.get('commonName', 'Unknown'),
                        'subject': subject.get('commonName', 'Unknown'),
                        'not_before': not_before,
                        'not_after': not_after,
                        'days_until_expiry': days_until_expiry,
                        'serial_number': cert.get('serialNumber', 'Unknown'),
                        'version': cert.get('version', 'Unknown')
                    }
                    
        except socket.timeout:
            print(f" Connection timeout: {self.domain}")
            return None
        except ssl.SSLError as e:
            print(f" SSL error: {e}")
            return None
        except Exception as e:
            print(f" Error: {e}")
            return None
    
    def check_https_redirect(self) -> bool:
        """
        SAFETY: Handles HTTP redirect errors
        PERF: O(1) HTTP request
        """
        try:
            http_url = f"http://{self.domain}"
            req = urllib.request.Request(http_url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                final_url = response.geturl()
                return final_url.startswith('https://')
                
        except urllib.error.HTTPError as e:
            if e.code == 301 or e.code == 302:
                return True  # Redirect is working
            return False
        except Exception as e:
            print(f"  Redirect check error: {e}")
            return False
    
    def validate(self, check_chain: bool = False, check_expiry: bool = True) -> bool:
        """
        MAIN VALIDATION ROUTINE
        SAFETY: Comprehensive SSL validation
        """
        print(f" Validating SSL certificate for: {self.domain}")
        print("=" * 60)
        
        # Get certificate info
        cert_info = self.get_certificate_info()
        
        if not cert_info:
            print(" SSL certificate validation failed")
            return False
        
        # Display certificate info
        print(f" Certificate found")
        print(f"   Issuer: {cert_info['issuer']}")
        print(f"   Subject: {cert_info['subject']}")
        print(f"   Valid from: {cert_info['not_before'].strftime('%Y-%m-%d')}")
        print(f"   Valid until: {cert_info['not_after'].strftime('%Y-%m-%d')}")
        print(f"   Days until expiry: {cert_info['days_until_expiry']}")
        
        # Check expiry
        if check_expiry:
            if cert_info['days_until_expiry'] < 0:
                print(" Certificate expired!")
                return False
            elif cert_info['days_until_expiry'] < 30:
                print("  Certificate expires in less than 30 days")
            else:
                print(f" Certificate valid for {cert_info['days_until_expiry']} more days")
        
        # Check HTTPS redirect
        print("\n Checking HTTP → HTTPS redirect...")
        if self.check_https_redirect():
            print(" HTTPS redirect working")
        else:
            print("  HTTPS redirect may not be working")
        
        # Check issuer (should be Cloudflare for Pages)
        if 'cloudflare' in cert_info['issuer'].lower():
            print(" Certificate issued by Cloudflare")
        else:
            print(f"  Certificate issuer: {cert_info['issuer']}")
        
        print("\n" + "=" * 60)
        print(" SSL VALIDATION COMPLETE")
        return True


def main():
    """
    CLI Entry Point
    SAFETY: Validates all CLI arguments
    """
    parser = argparse.ArgumentParser(
        description="SSL Certificate Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate SSL certificate
  python scripts/validate_ssl.py \\
    --domain bravetto.ai \\
    --check-chain \\
    --check-expiry

  # Validate multiple domains
  python scripts/validate_ssl.py \\
    --domain bravetto.ai \\
    --subdomain live.bravetto.ai \\
    --check-expiry
        """
    )
    
    parser.add_argument(
        "--domain",
        required=True,
        help="Domain to validate (e.g., bravetto.ai)"
    )
    
    parser.add_argument(
        "--subdomain",
        default=None,
        help="Subdomain to validate (e.g., live.bravetto.ai)"
    )
    
    parser.add_argument(
        "--check-chain",
        action="store_true",
        help="Check certificate chain (not implemented)"
    )
    
    parser.add_argument(
        "--check-expiry",
        action="store_true",
        default=True,
        help="Check certificate expiry (default: True)"
    )
    
    args = parser.parse_args()
    
    # Validate domain format
    if "." not in args.domain:
        print(" Invalid domain format")
        sys.exit(1)
    
    # Validate main domain
    validator = SSLCertificateValidator(args.domain)
    success = validator.validate(
        check_chain=args.check_chain,
        check_expiry=args.check_expiry
    )
    
    # Validate subdomain if provided
    if args.subdomain:
        print("\n" + "=" * 60)
        subdomain_validator = SSLCertificateValidator(args.subdomain)
        subdomain_success = subdomain_validator.validate(
            check_chain=args.check_chain,
            check_expiry=args.check_expiry
        )
        success = success and subdomain_success
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

