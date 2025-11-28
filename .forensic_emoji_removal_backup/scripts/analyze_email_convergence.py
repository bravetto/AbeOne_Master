#!/usr/bin/env python3
"""
Email Convergence Analysis Script
Analyzes last 3 days of email for AI newsletters and convergence/emergence opportunities.

Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Resonance)
"""

import os
import json
import re
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from email.header import decode_header
import imaplib
import email
from email.utils import parsedate_to_datetime

# Try Gmail API first, fallback to IMAP
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import pickle
    GMAIL_API_AVAILABLE = True
except ImportError:
    GMAIL_API_AVAILABLE = False

# Newsletter patterns (AI-focused)
AI_NEWSLETTER_PATTERNS = [
    r'(?i)(ai|artificial intelligence|machine learning|ml|llm|gpt|claude|anthropic|openai)',
    r'(?i)(newsletter|digest|weekly|daily|roundup)',
]

# Known AI newsletter senders (common patterns)
KNOWN_AI_NEWSLETTER_SENDERS = [
    # Major AI/ML Platforms
    'thebatch', 'deeplearning', 'towardsdatascience', 'kdnuggets',
    'fast.ai', 'huggingface', 'openai', 'anthropic', 'cohere',
    'langchain', 'llamaindex', 'replicate', 'runway', 'stability',
    
    # AI Newsletter Brands
    'ai newsletter', 'ai digest', 'ml news', 'ai research',
    'the decoder', 'last week in ai', 'ben\'s bites', 'the neuron',
    'ai tool report', 'futurepedia', 'there\'s an ai for that',
    'tldr', 'tldr newsletter', 'tldr.tech', 'the daily read', 'daily read',
    'the rundown ai', 'rundown ai', 'ai breakfast', 'superhuman',
    
    # Tech Newsletter Platforms
    'substack', 'substack.com', 'medium digest', 'medium.com',
    'dev.to', 'hacker news', 'product hunt',
    
    # Tech News Outlets
    'techcrunch', 'the verge', 'wired', 'ars technica',
    
    # Developer Platforms
    'github', 'gitlab', 'stack overflow', 'reddit',
    
    # VC/Startup Newsletters
    'y combinator', 'ycombinator', 'a16z', 'sequoia', 'first round',
    
    # Developer Tools
    'cursor', 'replit', 'codesandbox', 'vercel', 'netlify',
    
    # Cloud Platforms
    'aws', 'google cloud', 'azure', 'digitalocean', 'cloudflare'
]

# Convergence opportunity keywords
CONVERGENCE_KEYWORDS = [
    'convergence', 'emergence', 'integration', 'unification', 'synthesis',
    'pattern', 'architecture', 'framework', 'platform', 'ecosystem',
    'neuromorphic', 'epistemic', 'validation', 'truth', 'certainty',
    'guardian', 'agent', 'orchestration', 'mesh', 'network',
    'consciousness', 'resonance', 'frequency', 'atomic', 'one'
]

# Emergence opportunity keywords
EMERGENCE_KEYWORDS = [
    'breakthrough', 'discovery', 'innovation', 'novel', 'new',
    'emerging', 'trend', 'shift', 'transformation', 'evolution',
    'opportunity', 'potential', 'future', 'next', 'upcoming',
    'beta', 'launch', 'release', 'announcement', 'partnership'
]


@dataclass
class NewsletterEmail:
    """Represents an AI newsletter email."""
    sender: str
    subject: str
    date: datetime
    body_text: str
    body_html: Optional[str]
    links: List[str]
    ai_score: float  # 0-1, how AI-focused
    convergence_score: float  # 0-1, convergence opportunity
    emergence_score: float  # 0-1, emergence opportunity
    key_themes: List[str]
    convergence_opportunities: List[Dict[str, Any]]


@dataclass
class ConvergenceOpportunity:
    """Represents a convergence/emergence opportunity."""
    type: str  # 'convergence' or 'emergence'
    title: str
    description: str
    source_newsletter: str
    source_date: datetime
    themes: List[str]
    relevance_score: float  # 0-1
    action_items: List[str]
    alignment_patterns: List[str]  # Patterns from AbeOne system


class EmailAnalyzer:
    """Analyzes emails for convergence/emergence opportunities."""
    
    def __init__(self):
        self.newsletters: List[NewsletterEmail] = []
        self.opportunities: List[ConvergenceOpportunity] = []
    
    def get_email_credentials_from_1password(self) -> Optional[tuple[str, str]]:
        """Try to get email credentials from 1Password."""
        try:
            # Check if signed in to 1Password
            result = subprocess.run(
                ["op", "whoami"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                return None
            
            # Search for email/Gmail items
            result = subprocess.run(
                ["op", "item", "list", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return None
            
            items = json.loads(result.stdout)
            
            # Look for email-related items
            email_keywords = ["gmail", "email", "mail", "outlook", "imap"]
            email_items = [
                item for item in items
                if any(kw in item.get("title", "").lower() for kw in email_keywords)
            ]
            
            if not email_items:
                return None
            
            # Try to get credentials from first email item
            item_id = email_items[0].get("id")
            result = subprocess.run(
                ["op", "item", "get", item_id, "--format", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
            item_data = json.loads(result.stdout)
            fields = item_data.get("fields", [])
            
            email_address = None
            password = None
            
            for field in fields:
                label = field.get("label", "").lower()
                value = field.get("value", "")
                
                if "email" in label or label == "username":
                    email_address = value
                elif "password" in label:
                    password = value
            
            if email_address and password:
                return (email_address, password)
            
            return None
            
        except Exception as e:
            print(f"   ⚠️  1Password lookup failed: {e}")
            return None
        
    def fetch_emails_gmail_api(self, days: int = 3) -> List[Dict[str, Any]]:
        """Fetch emails using Gmail API."""
        if not GMAIL_API_AVAILABLE:
            raise ImportError("Gmail API libraries not available")
        
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        
        # Token file
        token_file = os.path.expanduser('~/.gmail_token.pickle')
        creds_file = os.path.expanduser('~/.gmail_credentials.json')
        
        # Load existing token
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(creds_file):
                    print("⚠️  Gmail credentials not found.")
                    print("   Please download credentials.json from Google Cloud Console")
                    print("   and save as ~/.gmail_credentials.json")
                    return []
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build service
        service = build('gmail', 'v1', credentials=creds)
        
        # Calculate date
        date_cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
        
        # Search query
        query = f'after:{date_cutoff}'
        
        # Fetch messages
        results = service.users().messages().list(userId='me', q=query, maxResults=500).execute()
        messages = results.get('messages', [])
        
        emails = []
        for msg in messages:
            try:
                message = service.users().messages().get(userId='me', id=msg['id']).execute()
                emails.append(message)
            except Exception as e:
                print(f"⚠️  Error fetching message {msg['id']}: {e}")
        
        return emails
    
    def fetch_emails_imap(self, email_address: str, password: str, days: int = 3) -> List[Dict[str, Any]]:
        """Fetch emails using IMAP (fallback)."""
        # Determine IMAP server
        if 'gmail.com' in email_address.lower():
            imap_server = 'imap.gmail.com'
        elif 'outlook.com' in email_address.lower() or 'hotmail.com' in email_address.lower():
            imap_server = 'outlook.office365.com'
        else:
            imap_server = 'imap.' + email_address.split('@')[1]
        
        try:
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(email_address, password)
            mail.select('inbox')
            
            # Calculate date
            date_cutoff = (datetime.now() - timedelta(days=days)).strftime('%d-%b-%Y')
            
            # Search
            status, messages = mail.search(None, f'SINCE {date_cutoff}')
            email_ids = messages[0].split()
            
            emails = []
            for email_id in email_ids:
                try:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    emails.append(email_message)
                except Exception as e:
                    print(f"⚠️  Error fetching email {email_id}: {e}")
            
            mail.close()
            mail.logout()
            return emails
            
        except Exception as e:
            print(f"❌ IMAP error: {e}")
            return []
    
    def is_ai_newsletter(self, sender: str, subject: str, body: str) -> tuple[bool, float]:
        """Determine if email is an AI newsletter and score it."""
        sender_lower = sender.lower()
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Check known senders
        for known_sender in KNOWN_AI_NEWSLETTER_SENDERS:
            if known_sender.lower() in sender_lower:
                return True, 0.9
        
        # Check patterns
        ai_matches = 0
        newsletter_matches = 0
        
        for pattern in AI_NEWSLETTER_PATTERNS:
            if re.search(pattern, sender_lower + ' ' + subject_lower + ' ' + body_lower[:500]):
                if 'newsletter' in pattern or 'digest' in pattern:
                    newsletter_matches += 1
                else:
                    ai_matches += 1
        
        # Score calculation
        score = min(1.0, (ai_matches * 0.3 + newsletter_matches * 0.4))
        
        # OPTIMIZATION: Lower threshold from 0.3 to 0.2 for better detection
        is_newsletter = score > 0.2 or 'newsletter' in subject_lower or 'digest' in subject_lower
        
        return is_newsletter, score
    
    def extract_links(self, html_content: str) -> List[str]:
        """Extract links from HTML content."""
        if not html_content:
            return []
        
        links = re.findall(r'href=["\']([^"\']+)["\']', html_content)
        return [link for link in links if link.startswith('http')]
    
    def analyze_convergence_opportunities(self, newsletter: NewsletterEmail) -> List[Dict[str, Any]]:
        """Analyze newsletter for convergence opportunities."""
        opportunities = []
        
        text = (newsletter.subject + ' ' + newsletter.body_text).lower()
        
        # Check for convergence keywords
        convergence_matches = sum(1 for kw in CONVERGENCE_KEYWORDS if kw in text)
        emergence_matches = sum(1 for kw in EMERGENCE_KEYWORDS if kw in text)
        
        # Pattern matching
        patterns_found = []
        for pattern in CONVERGENCE_KEYWORDS + EMERGENCE_KEYWORDS:
            if pattern in text:
                patterns_found.append(pattern)
        
        # Extract themes
        themes = []
        theme_patterns = {
            'neuromorphic': r'neuromorphic|spike|snn|spiking',
            'epistemic': r'epistemic|truth|validation|certainty',
            'guardian': r'guardian|agent|orchestr|mesh',
            'consciousness': r'consciousness|awareness|resonance|frequency',
            'atomic': r'atomic|one|unified|convergence',
            'integration': r'integration|unification|synthesis|convergence',
            'platform': r'platform|ecosystem|framework|architecture',
            'ai_safety': r'safety|guard|protect|secure|trust',
            'pattern': r'pattern|detection|recognition|intelligence',
            'emergence': r'emergence|breakthrough|discovery|novel'
        }
        
        for theme, pattern in theme_patterns.items():
            if re.search(pattern, text):
                themes.append(theme)
        
        # Calculate scores
        convergence_score = min(1.0, convergence_matches / 5.0)
        emergence_score = min(1.0, emergence_matches / 5.0)
        
        # Create opportunities
        if convergence_score > 0.2 or emergence_score > 0.2:
            opp_type = 'convergence' if convergence_score > emergence_score else 'emergence'
            
            # Extract potential action items (sentences with opportunity keywords)
            sentences = re.split(r'[.!?]+', newsletter.body_text)
            action_items = []
            for sentence in sentences[:20]:  # Limit to first 20 sentences
                if any(kw in sentence.lower() for kw in ['opportunity', 'potential', 'launch', 'release', 'beta', 'new']):
                    action_items.append(sentence.strip()[:200])
            
            opportunities.append({
                'type': opp_type,
                'score': max(convergence_score, emergence_score),
                'themes': themes,
                'patterns': patterns_found,
                'action_items': action_items[:5],  # Top 5
                'relevance': newsletter.ai_score * max(convergence_score, emergence_score)
            })
        
        return opportunities
    
    def parse_email_gmail_api(self, message: Dict[str, Any]) -> Optional[NewsletterEmail]:
        """Parse email from Gmail API format."""
        try:
            headers = message['payload'].get('headers', [])
            
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Parse date
            try:
                date = parsedate_to_datetime(date_str)
            except:
                date = datetime.now()
            
            # Extract body
            body_text = ''
            body_html = None
            links = []
            
            def extract_body(part):
                nonlocal body_text, body_html, links
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data', '')
                    if data:
                        import base64
                        body_text += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif part.get('mimeType') == 'text/html':
                    data = part.get('body', {}).get('data', '')
                    if data:
                        import base64
                        body_html = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                        links = self.extract_links(body_html)
                
                if 'parts' in part:
                    for subpart in part['parts']:
                        extract_body(subpart)
            
            extract_body(message['payload'])
            
            # Clean sender
            sender_clean = re.sub(r'<[^>]+>', '', sender).strip()
            
            # Check if AI newsletter
            is_newsletter, ai_score = self.is_ai_newsletter(sender_clean, subject, body_text)
            
            if not is_newsletter:
                return None
            
            # Analyze
            convergence_opps = self.analyze_convergence_opportunities(
                NewsletterEmail(
                    sender=sender_clean,
                    subject=subject,
                    date=date,
                    body_text=body_text,
                    body_html=body_html,
                    links=links,
                    ai_score=ai_score,
                    convergence_score=0.0,
                    emergence_score=0.0,
                    key_themes=[],
                    convergence_opportunities=[]
                )
            )
            
            # Calculate scores
            convergence_score = max([o['score'] for o in convergence_opps], default=0.0)
            emergence_score = max([o['score'] for o in convergence_opps if o['type'] == 'emergence'], default=0.0)
            themes = list(set([t for o in convergence_opps for t in o['themes']]))
            
            return NewsletterEmail(
                sender=sender_clean,
                subject=subject,
                date=date,
                body_text=body_text,
                body_html=body_html,
                links=links,
                ai_score=ai_score,
                convergence_score=convergence_score,
                emergence_score=emergence_score,
                key_themes=themes,
                convergence_opportunities=convergence_opps
            )
            
        except Exception as e:
            print(f"⚠️  Error parsing email: {e}")
            return None
    
    def parse_email_imap(self, email_message) -> Optional[NewsletterEmail]:
        """Parse email from IMAP format."""
        try:
            # Decode headers
            subject = ''
            if email_message.get('Subject'):
                for part in decode_header(email_message['Subject']):
                    if part[1]:
                        subject += part[0].decode(part[1])
                    else:
                        if isinstance(part[0], bytes):
                            subject += part[0].decode('utf-8', errors='ignore')
                        else:
                            subject += str(part[0])
            else:
                subject = ''
            
            sender = email_message['From']
            date_str = email_message['Date']
            
            # Parse date
            try:
                date = parsedate_to_datetime(date_str)
            except:
                date = datetime.now()
            
            # Extract body
            body_text = ''
            body_html = None
            links = []
            
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        body_text = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    elif content_type == 'text/html':
                        body_html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        links = self.extract_links(body_html)
            else:
                body_text = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Clean sender
            sender_clean = re.sub(r'<[^>]+>', '', sender).strip()
            
            # Check if AI newsletter
            is_newsletter, ai_score = self.is_ai_newsletter(sender_clean, subject, body_text)
            
            if not is_newsletter:
                return None
            
            # Analyze
            temp_newsletter = NewsletterEmail(
                sender=sender_clean,
                subject=subject,
                date=date,
                body_text=body_text,
                body_html=body_html,
                links=links,
                ai_score=ai_score,
                convergence_score=0.0,
                emergence_score=0.0,
                key_themes=[],
                convergence_opportunities=[]
            )
            
            convergence_opps = self.analyze_convergence_opportunities(temp_newsletter)
            
            # Calculate scores
            convergence_score = max([o['score'] for o in convergence_opps], default=0.0)
            emergence_score = max([o['score'] for o in convergence_opps if o['type'] == 'emergence'], default=0.0)
            themes = list(set([t for o in convergence_opps for t in o['themes']]))
            
            return NewsletterEmail(
                sender=sender_clean,
                subject=subject,
                date=date,
                body_text=body_text,
                body_html=body_html,
                links=links,
                ai_score=ai_score,
                convergence_score=convergence_score,
                emergence_score=emergence_score,
                key_themes=themes,
                convergence_opportunities=convergence_opps
            )
            
        except Exception as e:
            print(f"⚠️  Error parsing email: {e}")
            return None
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive convergence analysis report."""
        # Sort by relevance
        sorted_newsletters = sorted(
            self.newsletters,
            key=lambda x: x.ai_score * max(x.convergence_score, x.emergence_score),
            reverse=True
        )
        
        # Aggregate opportunities
        all_opportunities = []
        for newsletter in self.newsletters:
            for opp in newsletter.convergence_opportunities:
                all_opportunities.append({
                    'type': opp['type'],
                    'title': newsletter.subject,
                    'description': newsletter.body_text[:500],
                    'source': newsletter.sender,
                    'date': newsletter.date.isoformat(),
                    'themes': opp['themes'],
                    'relevance': opp['relevance'],
                    'action_items': opp['action_items'],
                    'patterns': opp['patterns']
                })
        
        # Sort opportunities by relevance
        all_opportunities.sort(key=lambda x: x['relevance'], reverse=True)
        
        # Group by type
        convergence_opps = [o for o in all_opportunities if o['type'] == 'convergence']
        emergence_opps = [o for o in all_opportunities if o['type'] == 'emergence']
        
        # Extract key themes across all newsletters
        all_themes = {}
        for newsletter in self.newsletters:
            for theme in newsletter.key_themes:
                all_themes[theme] = all_themes.get(theme, 0) + 1
        
        return {
            'analysis_date': datetime.now().isoformat(),
            'period_days': 3,
            'total_newsletters': len(self.newsletters),
            'total_opportunities': len(all_opportunities),
            'convergence_opportunities': len(convergence_opps),
            'emergence_opportunities': len(emergence_opps),
            'key_themes': dict(sorted(all_themes.items(), key=lambda x: x[1], reverse=True)),
            'top_newsletters': [
                {
                    'sender': n.sender,
                    'subject': n.subject,
                    'date': n.date.isoformat(),
                    'ai_score': n.ai_score,
                    'convergence_score': n.convergence_score,
                    'emergence_score': n.emergence_score,
                    'themes': n.key_themes,
                    'opportunities_count': len(n.convergence_opportunities)
                }
                for n in sorted_newsletters[:10]
            ],
            'top_convergence_opportunities': convergence_opps[:10],
            'top_emergence_opportunities': emergence_opps[:10],
            'all_opportunities': all_opportunities
        }


def main():
    """Main execution function."""
    print("=" * 80)
    print("EMAIL CONVERGENCE ANALYSIS")
    print("Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE")
    print("=" * 80)
    print()
    
    analyzer = EmailAnalyzer()
    
    # Try Gmail API first
    emails = []
    try:
        print("📧 Attempting Gmail API access...")
        emails = analyzer.fetch_emails_gmail_api(days=3)
        print(f"✅ Fetched {len(emails)} emails via Gmail API")
        
        for msg in emails:
            newsletter = analyzer.parse_email_gmail_api(msg)
            if newsletter:
                analyzer.newsletters.append(newsletter)
    
    except Exception as e:
        print(f"⚠️  Gmail API failed: {e}")
        print()
        print("📧 Attempting IMAP access...")
        
        # Check environment variables first
        email_address = os.getenv('EMAIL_ADDRESS', '').strip()
        password = os.getenv('EMAIL_PASSWORD', '').strip()
        
        # Try 1Password if not in env
        if not email_address or not password:
            print("   Checking 1Password for email credentials...")
            creds = analyzer.get_email_credentials_from_1password()
            if creds:
                email_address, password = creds
                print(f"   ✅ Found email credentials in 1Password")
        
        # If still not found, try interactive (but handle non-interactive gracefully)
        if not email_address or not password:
            try:
                print("   Please provide email credentials:")
                email_address = input("Email address: ").strip()
                password = input("Password (or app password for Gmail): ").strip()
            except EOFError:
                print("⚠️  Non-interactive mode detected.")
                print("   Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables")
                print("   Example: export EMAIL_ADDRESS='your@email.com'")
                print("           export EMAIL_PASSWORD='REPLACE_ME'")
                print()
                print("❌ Cannot proceed without credentials. Exiting.")
                return
        
        if email_address and password:
            emails = analyzer.fetch_emails_imap(email_address, password, days=3)
            print(f"✅ Fetched {len(emails)} emails via IMAP")
            
            for msg in emails:
                newsletter = analyzer.parse_email_imap(msg)
                if newsletter:
                    analyzer.newsletters.append(newsletter)
        else:
            print("❌ No credentials provided. Exiting.")
            return
    
    print()
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
    print("Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE")
    print("∞ AbëONE ∞")


if __name__ == '__main__':
    main()

