#!/usr/bin/env python3
"""
Scan All Newsletters in Mac Mail
Finds all newsletters (not just AI) to help expand detection
"""

import sys
import os
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.analyze_email_from_mailapp import read_emlx_file

def scan_newsletters(days=30, sample_limit=20000):
    """Scan for all newsletters."""
    mail_dir = Path.home() / 'Library' / 'Mail'
    cutoff = datetime.now() - timedelta(days=days)
    
    if cutoff.tzinfo is None:
        from datetime import timezone
        cutoff = cutoff.replace(tzinfo=timezone.utc)
    
    newsletter_senders = Counter()
    newsletter_domains = Counter()
    ai_related = Counter()
    
    newsletter_keywords = [
        'newsletter', 'digest', 'weekly', 'daily', 'roundup',
        'update', 'briefing', 'summary', 'report', 'insights',
        'brief', 'dispatch', 'bulletin', 'review'
    ]
    
    ai_keywords = [
        'ai', 'artificial intelligence', 'machine learning', 'ml',
        'llm', 'gpt', 'claude', 'neural', 'deep learning'
    ]
    
    newsletter_platforms = [
        'substack', 'beehiiv', 'mailchimp', 'convertkit', 'revue',
        'ghost', 'buttondown', 'tinyletter', 'mailerlite'
    ]
    
    count = 0
    print(f"🔍 Scanning last {days} days (sampling {sample_limit} emails)...")
    
    for emlx_file in list(mail_dir.rglob('*.emlx'))[:sample_limit]:
        if '.partial.' in str(emlx_file):
            continue
        
        count += 1
        if count % 5000 == 0:
            print(f"   Processed {count} emails...")
        
        try:
            msg = read_emlx_file(emlx_file)
            if not msg:
                continue
            
            sender = str(msg.get('From', ''))
            subject = str(msg.get('Subject', '')).lower()
            
            # Check date
            date_str = msg.get('Date', '')
            if date_str:
                try:
                    msg_date = parsedate_to_datetime(date_str)
                    if msg_date.tzinfo is None:
                        from datetime import timezone
                        msg_date = msg_date.replace(tzinfo=timezone.utc)
                    if msg_date < cutoff:
                        continue
                except:
                    pass
            
            # Check for newsletter indicators
            has_newsletter_keyword = any(kw in subject for kw in newsletter_keywords)
            has_ai_keyword = any(kw in subject or kw in sender.lower() for kw in ai_keywords)
            
            # Extract domain
            domain = None
            if '@' in sender:
                domain = sender.split('@')[1].split('>')[0].lower()
            
            # Check for newsletter platform
            is_platform = False
            if domain:
                for platform in newsletter_platforms:
                    if platform in domain:
                        newsletter_domains[domain] += 1
                        is_platform = True
                        break
            
            # If newsletter-like, record it
            if has_newsletter_keyword or is_platform:
                sender_clean = sender.split('<')[0].strip().strip('"')[:60]
                newsletter_senders[sender_clean] += 1
                
                if has_ai_keyword:
                    ai_related[sender_clean] += 1
        
        except:
            continue
    
    return newsletter_senders, newsletter_domains, ai_related

def main():
    """Main execution."""
    print("=" * 80)
    print("COMPREHENSIVE NEWSLETTER SCAN")
    print("=" * 80)
    print()
    
    newsletter_senders, newsletter_domains, ai_related = scan_newsletters(days=30)
    
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    
    print("📊 NEWSLETTER PLATFORMS DETECTED:")
    print("-" * 80)
    for domain, count in newsletter_domains.most_common(15):
        print(f"  {domain}: {count} emails")
    
    print()
    print("📧 TOP NEWSLETTER SENDERS:")
    print("-" * 80)
    for sender, count in newsletter_senders.most_common(20):
        print(f"  {sender}: {count} emails")
    
    print()
    print("🤖 AI-RELATED NEWSLETTERS:")
    print("-" * 80)
    for sender, count in ai_related.most_common(15):
        print(f"  {sender}: {count} emails")
    
    print()
    print("=" * 80)
    print(f"Total newsletter-like emails found: {sum(newsletter_senders.values())}")
    print(f"Total AI-related newsletters: {sum(ai_related.values())}")
    print("=" * 80)
    print()
    print("Pattern: OBSERVER × TRUTH × DETECTION × ONE")
    print("∞ AbëONE ∞")

if __name__ == '__main__':
    main()

