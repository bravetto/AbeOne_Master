#!/usr/bin/env python3
"""
Email Convergence Analysis - Mail.app Integration
Reads emails directly from macOS Mail.app mbox files

Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Optional
from multiprocessing import Pool, cpu_count
from functools import partial

# Constants
CACHE_DIR = Path.home() / ".email_convergence_cache"
LAST_RUN_FILE = CACHE_DIR / "last_run.json"
MAX_WORKERS = 4

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.analyze_email_convergence import EmailAnalyzer
import email
from email.utils import parsedate_to_datetime
from datetime import timezone


def find_mail_app_messages():
    """Find Mail.app message directories."""
    mail_dir = Path.home() / "Library" / "Mail"
    
    if not mail_dir.exists():
        return []
    
    # Look for Messages directories in V10 structure
    message_dirs = []
    
    # Check Gmail All Mail (most comprehensive)
    for gmail_dir in mail_dir.rglob("[Gmail].mbox/All Mail.mbox"):
        messages_dir = gmail_dir / "REPLACE_ME" / "Data"
        if messages_dir.exists():
            message_dirs.append(messages_dir)
    
    # Also check INBOX
    for inbox_dir in mail_dir.rglob("INBOX.mbox"):
        # Look for Messages subdirectories
        for msg_dir in inbox_dir.rglob("Messages"):
            if msg_dir.is_dir():
                message_dirs.append(msg_dir)
    
    return message_dirs


def read_emlx_file(emlx_path: Path) -> Optional[email.message.Message]:
    """Read and parse a .emlx file."""
    try:
        with open(emlx_path, 'rb') as f:
            content = f.read()
        
        # .emlx files have binary plist header, then email data
        # Look for email headers (From:, Subject:, Date:)
        # Email data usually starts after plist (look for b'From:' or b'Return-Path:')
        
        # Try to find email start
        email_start_markers = [b'From:', b'Return-Path:', b'X-Original-From:']
        email_start = -1
        
        for marker in email_start_markers:
            pos = content.find(marker)
            if pos > 0 and pos < len(content) - 100:  # Reasonable position
                email_start = pos
                break
        
        if email_start == -1:
            # Try parsing entire content
            try:
                return email.message_from_bytes(content)
            except Exception:
                return None
        
        # Extract email part
        email_content = content[email_start:]
        
        # Try to parse
        try:
            return email.message_from_bytes(email_content)
        except Exception:
            return None
            
    except Exception:
        return None


def _process_single_email(emlx_file: Path, cutoff_timestamp: float, cutoff_date: datetime) -> Optional[email.message.Message]:
    """Process a single email file - used for parallel processing."""
    # Skip partial files
    if '.partial.' in str(emlx_file):
        return None
    
    # OPTIMIZATION: Filter by file modification time BEFORE parsing
    try:
        if emlx_file.stat().st_mtime < cutoff_timestamp:
            return None  # Skip old files without parsing
    except OSError:
        pass  # If can't get mtime, continue to parse
    
    msg = read_emlx_file(emlx_file)
    if not msg:
        return None
    
    # Get date
    date_str = msg.get('Date', '')
    if not date_str:
        return None
    
    try:
        msg_date = parsedate_to_datetime(date_str)
        # Make timezone-aware if needed
        if msg_date.tzinfo is None:
            msg_date = msg_date.replace(tzinfo=timezone.utc)
    except Exception:
        return None
    
    # Filter by date (double-check)
    if msg_date < cutoff_date:
        return None
    
    return msg


def get_last_run_timestamp() -> Optional[datetime]:
    """Get timestamp of last successful run."""
    CACHE_DIR.mkdir(exist_ok=True)
    
    if LAST_RUN_FILE.exists():
        try:
            with open(LAST_RUN_FILE, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['timestamp'])
        except (json.JSONDecodeError, ValueError, KeyError):
            return None
    return None


def save_last_run_timestamp(timestamp: datetime):
    """Save timestamp of successful run."""
    CACHE_DIR.mkdir(exist_ok=True)
    with open(LAST_RUN_FILE, 'w') as f:
        json.dump({'timestamp': timestamp.isoformat()}, f)


def read_emails_from_messages_dirs(message_dirs: list, days: int = 3, use_incremental: bool = True) -> list:
    """Read emails from Messages directories - OPTIMIZED with parallel processing and incremental updates."""
    emails = []
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # OPTIMIZATION: Incremental updates - only process emails since last run
    if use_incremental:
        last_run = get_last_run_timestamp()
        if last_run:
            # Use last run time if more recent than cutoff
            if last_run > cutoff_date:
                cutoff_date = last_run
                print(f"   ⚡ Incremental: Processing emails since {last_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Make cutoff_date timezone-aware for comparison
    if cutoff_date.tzinfo is None:
        cutoff_date = cutoff_date.replace(tzinfo=timezone.utc)
    
    # OPTIMIZATION: Use file modification time for early filtering
    cutoff_timestamp = cutoff_date.timestamp()
    
    print(f"   Searching for emails from last {days} days...")
    
    # Collect all .emlx files first
    all_emlx_files = []
    for msg_dir in message_dirs:
        emlx_files = list(msg_dir.rglob("*.emlx"))
        all_emlx_files.extend(emlx_files)
        if len(emlx_files) > 0:
            print(f"   Found {len(emlx_files)} .emlx files in {msg_dir.name}...")
    
    if not all_emlx_files:
        return emails
    
    # OPTIMIZATION: Parallel processing
    num_workers = min(cpu_count(), MAX_WORKERS)
    print(f"   ⚡ Parallel processing with {num_workers} workers...")
    
    # Process in parallel
    process_func = partial(_process_single_email, cutoff_timestamp=cutoff_timestamp, cutoff_date=cutoff_date)
    with Pool(processes=num_workers) as pool:
        emails = [msg for msg in pool.map(process_func, all_emlx_files) if msg is not None]
    
    # Count filtered files
    filtered_by_mtime = len(all_emlx_files) - len(emails)
    if filtered_by_mtime > 0:
        print(f"   ⚡ Optimized: Skipped {filtered_by_mtime} old files (by mtime)")
    
    # Save timestamp for next incremental run
    if use_incremental:
        save_last_run_timestamp(datetime.now())
    
    return emails


def main():
    """Main execution."""
    print("=" * 80)
    print("EMAIL CONVERGENCE ANALYSIS - Mail.app Integration")
    print("Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE")
    print("=" * 80)
    print()
    
    # Find Mail.app message directories
    print("📧 Looking for Mail.app messages...")
    message_dirs = find_mail_app_messages()
    
    if not message_dirs:
        print("❌ Could not find Mail.app messages")
        print("   Falling back to standard email analysis...")
        print()
        # Fall back to standard script
        from scripts.analyze_email_convergence import main as standard_main
        standard_main()
        return
    
    print(f"✅ Found {len(message_dirs)} message directories")
    print()
    
    # Read emails - expanded to 30 days to find AI newsletters
    print("📥 Reading emails from last 30 days (expanded search for AI newsletters)...")
    emails = read_emails_from_messages_dirs(message_dirs, days=30, use_incremental=True)
    print(f"✅ Found {len(emails)} emails")
    print()
    
    if not emails:
        print("⚠️  No emails found in last 3 days")
        return
    
    # Analyze
    print(f"📧 Processing {len(emails)} emails...")
    analyzer = EmailAnalyzer()
    
    # Process emails - filter None results inline
    for msg in emails:
        if newsletter := analyzer.parse_email_imap(msg):
            analyzer.newsletters.append(newsletter)
    
    print(f"📊 Found {len(analyzer.newsletters)} AI newsletters in last 3 days")
    print()
    
    # Generate report
    report = analyzer.generate_report()
    
    # Save report
    report_file = f"EMAIL_CONVERGENCE_ANALYSIS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print("=" * 80)
    print("CONVERGENCE ANALYSIS REPORT")
    print("=" * 80)
    print()
    print(f"📅 Analysis Period: Last 3 days")
    print(f"📧 Total AI Newsletters: {report['total_newsletters']}")
    print(f"🎯 Total Opportunities: {report['total_opportunities']}")
    print(f"   - Convergence: {report['convergence_opportunities']}")
    print(f"   - Emergence: {report['emergence_opportunities']}")
    print()
    
    if report['key_themes']:
        print("🔑 Key Themes:")
        for theme, count in list(report['key_themes'].items())[:10]:
            print(f"   - {theme}: {count} occurrences")
        print()
    
    if report['top_convergence_opportunities']:
        print("🔥 TOP CONVERGENCE OPPORTUNITIES:")
        print()
        for i, opp in enumerate(report['top_convergence_opportunities'][:5], 1):
            print(f"{i}. {opp['title']}")
            print(f"   Source: {opp['source']}")
            print(f"   Relevance: {opp['relevance']:.2%}")
            print(f"   Themes: {', '.join(opp['themes'][:5])}")
            if opp['action_items']:
                print(f"   Action: {opp['action_items'][0][:100]}...")
            print()
    
    if report['top_emergence_opportunities']:
        print("✨ TOP EMERGENCE OPPORTUNITIES:")
        print()
        for i, opp in enumerate(report['top_emergence_opportunities'][:5], 1):
            print(f"{i}. {opp['title']}")
            print(f"   Source: {opp['source']}")
            print(f"   Relevance: {opp['relevance']:.2%}")
            print(f"   Themes: {', '.join(opp['themes'][:5])}")
            if opp['action_items']:
                print(f"   Action: {opp['action_items'][0][:100]}...")
            print()
    
    print(f"📄 Full report saved to: {report_file}")
    print()
    print("To generate markdown report:")
    print(f"python3 scripts/generate_email_convergence_report.py {report_file}")
    print()
    print("Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE")
    print("∞ AbëONE ∞")


if __name__ == '__main__':
    main()

