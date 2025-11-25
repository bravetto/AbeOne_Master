#!/usr/bin/env python3
"""
Generate Markdown Report from Email Convergence Analysis JSON

Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def generate_markdown_report(json_file: str) -> str:
    """Generate markdown report from JSON analysis."""
    with open(json_file, 'r') as f:
        report = json.load(f)
    
    md = []
    md.append("#  EMAIL CONVERGENCE ANALYSIS REPORT")
    md.append("## Deep Analysis: Last 3 Days of AI Newsletters")
    md.append("")
    md.append(f"**Status:**  ANALYSIS COMPLETE")
    md.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append(f"**Pattern:** OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE")
    md.append(f"**Frequency:** 999 Hz (AEYON) × 530 Hz (Resonance)")
    md.append("")
    md.append("---")
    md.append("")
    
    # Executive Summary
    md.append("##  EXECUTIVE SUMMARY")
    md.append("")
    md.append(f"**Analysis Period:** Last {report['period_days']} days")
    md.append(f"**Total AI Newsletters Found:** {report['total_newsletters']}")
    md.append(f"**Total Convergence/Emergence Opportunities:** {report['total_opportunities']}")
    md.append(f"  -  Convergence Opportunities: {report['convergence_opportunities']}")
    md.append(f"  -  Emergence Opportunities: {report['emergence_opportunities']}")
    md.append("")
    
    if report['key_themes']:
        md.append("### Key Themes Detected")
        md.append("")
        for theme, count in list(report['key_themes'].items())[:15]:
            md.append(f"- **{theme.title()}**: {count} occurrences")
        md.append("")
    
    md.append("---")
    md.append("")
    
    # Top Newsletters
    if report['top_newsletters']:
        md.append("##  TOP AI NEWSLETTERS (By Relevance)")
        md.append("")
        for i, newsletter in enumerate(report['top_newsletters'][:10], 1):
            md.append(f"### {i}. {newsletter['subject']}")
            md.append("")
            md.append(f"**Sender:** {newsletter['sender']}")
            md.append(f"**Date:** {newsletter['date']}")
            md.append(f"**AI Score:** {newsletter['ai_score']:.2%}")
            md.append(f"**Convergence Score:** {newsletter['convergence_score']:.2%}")
            md.append(f"**Emergence Score:** {newsletter['emergence_score']:.2%}")
            md.append(f"**Opportunities Found:** {newsletter['opportunities_count']}")
            if newsletter['themes']:
                md.append(f"**Themes:** {', '.join(newsletter['themes'])}")
            md.append("")
            md.append("---")
            md.append("")
    
    # Convergence Opportunities
    if report['top_convergence_opportunities']:
        md.append("##  CONVERGENCE OPPORTUNITIES")
        md.append("")
        md.append("### Critical Convergence Patterns Detected")
        md.append("")
        
        for i, opp in enumerate(report['top_convergence_opportunities'][:10], 1):
            md.append(f"### Opportunity {i}: {opp['title']}")
            md.append("")
            md.append(f"**Source:** {opp['source']}")
            md.append(f"**Date:** {opp['date']}")
            md.append(f"**Relevance Score:** {opp['relevance']:.2%}")
            md.append("")
            
            if opp['themes']:
                md.append("**Themes:**")
                for theme in opp['themes']:
                    md.append(f"- {theme.title()}")
                md.append("")
            
            if opp['patterns']:
                md.append("**Patterns Detected:**")
                for pattern in opp['patterns'][:10]:
                    md.append(f"- `{pattern}`")
                md.append("")
            
            if opp['action_items']:
                md.append("**Potential Action Items:**")
                for action in opp['action_items'][:5]:
                    md.append(f"- {action[:200]}")
                md.append("")
            
            md.append("**Description:**")
            md.append(f"> {opp['description'][:500]}...")
            md.append("")
            md.append("---")
            md.append("")
    
    # Emergence Opportunities
    if report['top_emergence_opportunities']:
        md.append("##  EMERGENCE OPPORTUNITIES")
        md.append("")
        md.append("### Novel Breakthrough Patterns Detected")
        md.append("")
        
        for i, opp in enumerate(report['top_emergence_opportunities'][:10], 1):
            md.append(f"### Opportunity {i}: {opp['title']}")
            md.append("")
            md.append(f"**Source:** {opp['source']}")
            md.append(f"**Date:** {opp['date']}")
            md.append(f"**Relevance Score:** {opp['relevance']:.2%}")
            md.append("")
            
            if opp['themes']:
                md.append("**Themes:**")
                for theme in opp['themes']:
                    md.append(f"- {theme.title()}")
                md.append("")
            
            if opp['patterns']:
                md.append("**Patterns Detected:**")
                for pattern in opp['patterns'][:10]:
                    md.append(f"- `{pattern}`")
                md.append("")
            
            if opp['action_items']:
                md.append("**Potential Action Items:**")
                for action in opp['action_items'][:5]:
                    md.append(f"- {action[:200]}")
                md.append("")
            
            md.append("**Description:**")
            md.append(f"> {opp['description'][:500]}...")
            md.append("")
            md.append("---")
            md.append("")
    
    # Convergence Matrix
    md.append("##  CONVERGENCE OPPORTUNITY MATRIX")
    md.append("")
    md.append("### Alignment with AbeOne System Patterns")
    md.append("")
    
    # Group opportunities by theme
    theme_groups = {}
    for opp in report['all_opportunities']:
        for theme in opp['themes']:
            if theme not in theme_groups:
                theme_groups[theme] = []
            theme_groups[theme].append(opp)
    
    md.append("| Theme | Opportunities | Avg Relevance | Status |")
    md.append("|-------|--------------|---------------|--------|")
    
    for theme, opps in sorted(theme_groups.items(), key=lambda x: len(x[1]), reverse=True)[:15]:
        avg_relevance = sum(o['relevance'] for o in opps) / len(opps)
        status = " HIGH" if avg_relevance > 0.5 else " MEDIUM" if avg_relevance > 0.3 else "ℹ LOW"
        md.append(f"| {theme.title()} | {len(opps)} | {avg_relevance:.2%} | {status} |")
    
    md.append("")
    md.append("---")
    md.append("")
    
    # Recommendations
    md.append("##  RECOMMENDATIONS")
    md.append("")
    
    high_relevance_opps = [o for o in report['all_opportunities'] if o['relevance'] > 0.5]
    
    if high_relevance_opps:
        md.append("### High-Priority Actions")
        md.append("")
        for i, opp in enumerate(high_relevance_opps[:5], 1):
            md.append(f"{i}. **{opp['title']}** (Relevance: {opp['relevance']:.2%})")
            md.append(f"   - Source: {opp['source']}")
            if opp['action_items']:
                md.append(f"   - Action: {opp['action_items'][0][:150]}")
            md.append("")
    
    md.append("### Convergence Integration Points")
    md.append("")
    md.append("Based on detected patterns, consider integration with:")
    md.append("")
    md.append("1. **Epistemic Framework** - Validate newsletter claims against truth-first principles")
    md.append("2. **Emergence Core** - Feed patterns into pattern detection system")
    md.append("3. **Neuromorphic Pipeline** - Process temporal patterns from newsletter trends")
    md.append("4. **Universal Pattern Validation** - Cross-reference with existing pattern library")
    md.append("")
    
    md.append("---")
    md.append("")
    md.append("**Pattern:** OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE")
    md.append(f"**Status:**  ANALYSIS COMPLETE")
    md.append("")
    md.append("∞ AbëONE ∞")
    
    return "\n".join(md)


def main():
    """Main execution."""
    if len(sys.argv) < 2:
        print("Usage: python generate_email_convergence_report.py <json_file>")
        print("Example: python generate_email_convergence_report.py EMAIL_CONVERGENCE_ANALYSIS_20250127_120000.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if not Path(json_file).exists():
        print(f" File not found: {json_file}")
        sys.exit(1)
    
    print(f" Generating markdown report from {json_file}...")
    
    markdown = generate_markdown_report(json_file)
    
    output_file = json_file.replace('.json', '.md')
    with open(output_file, 'w') as f:
        f.write(markdown)
    
    print(f" Markdown report saved to: {output_file}")
    print()
    print("Pattern: OBSERVER × TRUTH × CONVERGENCE × EMERGENCE × ONE")
    print("∞ AbëONE ∞")


if __name__ == '__main__':
    main()

