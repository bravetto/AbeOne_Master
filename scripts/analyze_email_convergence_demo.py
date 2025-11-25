#!/usr/bin/env python3
"""
Email Convergence Analysis - DEMO MODE
Shows sample output format with mock data

Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.analyze_email_convergence import EmailAnalyzer, NewsletterEmail

def create_demo_data():
    """Create demo newsletter data for testing."""
    analyzer = EmailAnalyzer()
    
    # Sample AI newsletters with convergence opportunities
    demo_newsletters = [
        NewsletterEmail(
            sender="The Batch (deeplearning.ai)",
            subject="Neuromorphic AI Breakthrough: New SNN Framework Released",
            date=datetime.now() - timedelta(days=1),
            body_text="""
            Exciting news in neuromorphic computing! A new spiking neural network 
            framework has been released that enables real-time pattern recognition 
            with unprecedented efficiency. This breakthrough converges multiple 
            research directions into a unified platform.
            
            Key features:
            - Temporal pattern detection
            - Epistemic validation layer
            - Integration with existing AI systems
            - Open source release next week
            
            This represents a convergence opportunity for AI safety and validation 
            systems. The framework includes built-in truth-first validation mechanisms.
            """,
            body_html=None,
            links=["https://example.com/neuromorphic-framework"],
            ai_score=0.95,
            convergence_score=0.0,
            emergence_score=0.0,
            key_themes=[],
            convergence_opportunities=[]
        ),
        NewsletterEmail(
            sender="Ben's Bites AI Newsletter",
            subject="AI Safety: New Epistemic Validation Tools Launch",
            date=datetime.now() - timedelta(days=2),
            body_text="""
            The AI safety community is buzzing about new epistemic validation tools 
            that help detect hallucinations and ensure truth-first AI responses.
            
            These tools converge multiple validation approaches:
            - Pattern detection systems
            - Failure mode analysis
            - Real-time truth validation
            - Guardian agent integration
            
            Beta access available now. This could be a game-changer for AI systems 
            requiring high certainty and validation.
            """,
            body_html=None,
            links=["https://example.com/epistemic-tools"],
            ai_score=0.90,
            convergence_score=0.0,
            emergence_score=0.0,
            key_themes=[],
            convergence_opportunities=[]
        ),
        NewsletterEmail(
            sender="AI Research Digest",
            subject="Emergence: Multi-Agent Orchestration Platforms",
            date=datetime.now() - timedelta(days=1),
            body_text="""
            A new wave of multi-agent orchestration platforms is emerging, enabling 
            complex AI systems to work together seamlessly.
            
            Key trends:
            - Service mesh architectures for AI agents
            - Guardian network patterns
            - Atomic execution frameworks
            - Consciousness-aware coordination
            
            This represents an emergence opportunity for unified AI systems. 
            Multiple companies are converging on similar architectural patterns.
            """,
            body_html=None,
            links=["https://example.com/orchestration"],
            ai_score=0.85,
            convergence_score=0.0,
            emergence_score=0.0,
            key_themes=[],
            convergence_opportunities=[]
        ),
        NewsletterEmail(
            sender="The Decoder",
            subject="Pattern Intelligence: New Detection Systems",
            date=datetime.now() - timedelta(days=0),
            body_text="""
            Pattern intelligence systems are becoming critical for AI safety and 
            validation. New frameworks enable real-time pattern detection across 
            multiple dimensions.
            
            Features:
            - Multi-module pattern recognition
            - Failure pattern matching
            - Temporal pattern analysis
            - Universal pattern validation
            
            Launch announcement next week. This could integrate with existing 
            epistemic frameworks for comprehensive validation.
            """,
            body_html=None,
            links=["https://example.com/pattern-intelligence"],
            ai_score=0.88,
            convergence_score=0.0,
            emergence_score=0.0,
            key_themes=[],
            convergence_opportunities=[]
        ),
    ]
    
    # Analyze each newsletter
    for newsletter in demo_newsletters:
        convergence_opps = analyzer.analyze_convergence_opportunities(newsletter)
        newsletter.convergence_opportunities = convergence_opps
        
        convergence_score = max([o['score'] for o in convergence_opps], default=0.0)
        emergence_score = max([o['score'] for o in convergence_opps if o['type'] == 'emergence'], default=0.0)
        themes = list(set([t for o in convergence_opps for t in o['themes']]))
        
        newsletter.convergence_score = convergence_score
        newsletter.emergence_score = emergence_score
        newsletter.key_themes = themes
        
        analyzer.newsletters.append(newsletter)
    
    return analyzer

def main():
    """Run demo analysis."""
    print("=" * 80)
    print("EMAIL CONVERGENCE ANALYSIS - DEMO MODE")
    print("Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE")
    print("=" * 80)
    print()
    print("  Running in DEMO MODE with sample data")
    print("   To analyze your actual email, run: python3 scripts/analyze_email_convergence.py")
    print()
    
    analyzer = create_demo_data()
    
    print(f" Found {len(analyzer.newsletters)} AI newsletters (demo data)")
    print()
    
    # Generate report
    report = analyzer.generate_report()
    
    # Save report
    report_file = f"EMAIL_CONVERGENCE_ANALYSIS_DEMO_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print("=" * 80)
    print("CONVERGENCE ANALYSIS REPORT")
    print("=" * 80)
    print()
    print(f" Analysis Period: Last 3 days (DEMO)")
    print(f" Total AI Newsletters: {report['total_newsletters']}")
    print(f" Total Opportunities: {report['total_opportunities']}")
    print(f"   - Convergence: {report['convergence_opportunities']}")
    print(f"   - Emergence: {report['emergence_opportunities']}")
    print()
    
    if report['key_themes']:
        print(" Key Themes:")
        for theme, count in list(report['key_themes'].items())[:10]:
            print(f"   - {theme}: {count} occurrences")
        print()
    
    if report['top_convergence_opportunities']:
        print(" TOP CONVERGENCE OPPORTUNITIES:")
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
        print(" TOP EMERGENCE OPPORTUNITIES:")
        print()
        for i, opp in enumerate(report['top_emergence_opportunities'][:5], 1):
            print(f"{i}. {opp['title']}")
            print(f"   Source: {opp['source']}")
            print(f"   Relevance: {opp['relevance']:.2%}")
            print(f"   Themes: {', '.join(opp['themes'][:5])}")
            if opp['action_items']:
                print(f"   Action: {opp['action_items'][0][:100]}...")
            print()
    
    print(f" Full report saved to: {report_file}")
    print()
    print("To generate markdown report:")
    print(f"python3 scripts/generate_email_convergence_report.py {report_file}")
    print()
    print("Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE")
    print("∞ AbëONE ∞")

if __name__ == '__main__':
    main()

