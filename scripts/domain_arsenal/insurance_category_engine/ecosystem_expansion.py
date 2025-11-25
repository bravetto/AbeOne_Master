#!/usr/bin/env python3
"""
Insurance Category Engine - Ecosystem Expansion
Cross-Funnel Connections

Pattern: ECOSYSTEM × EXPANSION × REVENUE × ONE
"""

import json
from typing import Dict, List

class EcosystemExpansion:
    """Cross-funnel ecosystem expansion"""
    
    def __init__(self):
        self.connections = {}
    
    def build_ecosystem(self):
        """Build cross-funnel ecosystem"""
        print(" Building Ecosystem Expansion...")
        
        # Connection 1: Life Insurance → Travel Insurance
        connection_1 = self._build_travel_insurance_connection()
        
        # Connection 2: Life Insurance → Job Board
        connection_2 = self._build_job_board_connection()
        
        # Shared Email List Strategy
        email_strategy = self._build_email_list_strategy()
        
        return {
            "connections": {
                "life_to_travel": connection_1,
                "life_to_jobs": connection_2
            },
            "email_strategy": email_strategy,
            "revenue_multiplier": "2x-3x per lead"
        }
    
    def _build_travel_insurance_connection(self) -> Dict:
        """Life Insurance → Travel Insurance Cross-Sell"""
        return {
            "source": "lifequotes.ai",
            "target": "cruisedeals.ai",
            "trigger": "Email sequence day 14",
            "offer": "Travel Insurance - Protect Your Trips",
            "rationale": "People buying life insurance travel → Cross-sell travel insurance",
            "funnel": {
                "step_1": "Life insurance quote completed",
                "step_2": "Email sequence: Day 14 - Travel insurance offer",
                "step_3": "Link to cruisedeals.ai travel insurance",
                "step_4": "Conversion to travel insurance"
            },
            "expected_conversion": "5-10%"
        }
    
    def _build_job_board_connection(self) -> Dict:
        """Life Insurance → Job Board Cross-Sell"""
        return {
            "source": "lifequotes.ai",
            "target": "technologyjobs.ai",
            "trigger": "Email sequence day 21",
            "offer": "Find Your Next Tech Job",
            "rationale": "People buying insurance = employed → Job board audience",
            "funnel": {
                "step_1": "Life insurance quote completed",
                "step_2": "Email sequence: Day 21 - Job board offer",
                "step_3": "Link to technologyjobs.ai",
                "step_4": "Job board signup"
            },
            "expected_conversion": "3-7%"
        }
    
    def _build_email_list_strategy(self) -> Dict:
        """Shared email list strategy"""
        return {
            "shared_list": True,
            "segmentation": {
                "life_insurance_leads": "Segment for life insurance offers",
                "travel_interested": "Segment for travel insurance offers",
                "job_seekers": "Segment for job board offers"
            },
            "cross_promotion": {
                "frequency": "Weekly",
                "offers": [
                    "Life insurance → Travel insurance",
                    "Life insurance → Job board",
                    "Travel insurance → Life insurance",
                    "Job board → Life insurance (benefits package)"
                ]
            },
            "revenue_impact": "2x-3x revenue per lead through cross-selling"
        }
    
    def generate_cross_sell_email(self, source: str, target: str) -> str:
        """Generate cross-sell email"""
        emails = {
            "life_to_travel": """Subject: Protect Your Travel Plans Too

Hi there!

You recently compared life insurance quotes. Did you know you can also protect your travel plans?

Get travel insurance quotes for your next trip:
[Link to cruisedeals.ai]

Compare rates from top providers in minutes.

Best,
The InsuranceHub Team""",
            
            "life_to_jobs": """Subject: Find Your Next Opportunity

Hi there!

You're protecting your family with life insurance. Are you also protecting your career?

Find your next tech job opportunity:
[Link to technologyjobs.ai]

Browse thousands of tech jobs from top companies.

Best,
The InsuranceHub Team"""
        }
        
        key = f"{source}_to_{target}"
        return emails.get(key, "Cross-sell email template")

if __name__ == "__main__":
    expansion = EcosystemExpansion()
    ecosystem = expansion.build_ecosystem()
    
    print(f"\n Ecosystem Built")
    print(f" Connections: {len(ecosystem['connections'])}")
    print(f" Revenue Multiplier: {ecosystem['revenue_multiplier']}")

