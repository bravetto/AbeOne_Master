#!/usr/bin/env python3
"""
Find TLDR Newsletters in Mac Mail
Quick script to find and display TLDR newsletters
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.analyze_email_from_mailapp import read_emlx_file
from email.utils import parsedate_to_datetime

def find_tldr_emails(days=30):
    """Find TLDR newsletters in Mail.app."""
    mail_dir = Path.home() / 'Library' / 'Mail'
    tldr_emails = []
    cutoff = datetime.now() - timedelta(days=days)
    
    if cutoff.tzinfo is None:
        from datetime import timezone
        cutoff = cutoff.replace(tzinfo=timezone.utc)
    
    print(f" Searching for TLDR newsletters in last {days} days...")
    print()
    
    count = 0
    for emlx_file in mail_dir.rglob('*.emlx'):
        if '.partial.' in str(emlx_file):
            continue
        
        count += 1
        if count % 1000 == 0:
            print(f"   Processed {count} emails...")
        
        try:
            msg = read_emlx_file(emlx_file)
            if not msg:
                continue
            
            # Get sender and subject
            sender = str(msg.get('From', '')).lower()
            subject = str(msg.get('Subject', '')).lower()
            
            # Check for TLDR
            if 'tldr' in sender or 'tldr' in subject or 'daily read' in sender:
                date_str = msg.get('Date', '')
                if date_str:
                    try:
                        msg_date = parsedate_to_datetime(date_str)
                        if msg_date.tzinfo is None:
                            from datetime import timezone
                            msg_date = msg_date.replace(tzinfo=timezone.utc)
                        
                        if msg_date >= cutoff:
                            # Get body preview
                            body_preview = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == 'text/plain':
                                        try:
                                            body_preview = part.get_payload(decode=True).decode('utf-8', errors='ignore')[:200]
                                            break
                                        except:
                                            pass
                            else:
                                try:
                                    body_preview = msg.get_payload(decode=True).decode('utf-8', errors='ignore')[:200]
                                except:
                                    pass
                            
                            tldr_emails.append({
                                'sender': msg.get('From', ''),
                                'subject': msg.get('Subject', ''),
                                'date': date_str,
                                'body_preview': body_preview
                            })
                    except Exception as e:
                        continue
        except:
            continue
    
    return tldr_emails

def main():
    """Main execution."""
    print("=" * 80)
    print("TLDR NEWSLETTER FINDER")
    print("=" * 80)
    print()
    
    tldr_emails = find_tldr_emails(days=30)
    
    print()
    print("=" * 80)
    print(f" FOUND {len(tldr_emails)} TLDR NEWSLETTERS")
    print("=" * 80)
    print()
    
    if tldr_emails:
        for i, email in enumerate(tldr_emails[:20], 1):
            print(f"{i}. {email['subject']}")
            print(f"   From: {email['sender'][:60]}")
            print(f"   Date: {email['date']}")
            if email['body_preview']:
                print(f"   Preview: {email['body_preview'][:100]}...")
            print()
    else:
        print("  No TLDR newsletters found in last 30 days")
        print("   They may be in a different folder or older than 30 days")
    
    print()
    print("Pattern: OBSERVER × TRUTH × DETECTION × ONE")
    print("∞ AbëONE ∞")

if __name__ == '__main__':
    main()

