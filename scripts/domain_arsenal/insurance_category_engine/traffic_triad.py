#!/usr/bin/env python3
"""
Insurance Category Engine - Traffic Triad
3 Traffic Streams: Organic + Paid + AI Social

Pattern: TRAFFIC × TRIAD × GROWTH × ONE
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict

class TrafficTriad:
    """3 Traffic Streams for Insurance Category Engine"""
    
    def __init__(self):
        self.content_calendar = {}
        self.reddit_posts = []
        self.quora_answers = []
        self.social_posts = []
    
    def generate_organic_content(self):
        """Stream A: Organic Content (SEO + Reddit + Quora)"""
        print(" Generating Organic Content...")
        
        # SEO Content
        seo_content = self._generate_seo_content()
        
        # Reddit Posts
        reddit_posts = self._generate_reddit_posts()
        
        # Quora Answers
        quora_answers = self._generate_quora_answers()
        
        return {
            "seo_content": seo_content,
            "reddit_posts": reddit_posts,
            "quora_answers": quora_answers
        }
    
    def generate_paid_campaigns(self):
        """Stream B: Paid Campaigns (Retargeting + Cold Traffic)"""
        print(" Generating Paid Campaigns...")
        
        campaigns = {
            "retargeting": {
                "platform": "Facebook + Google",
                "budget": "$50/day",
                "angles": [
                    "Save money on insurance - Compare quotes in 2 minutes",
                    "Find the best life insurance rates - Get quotes now",
                    "Protect your family - Compare insurance options"
                ],
                "audience": "Website visitors (last 30 days)"
            },
            "cold_traffic": {
                "platform": "Google Ads",
                "budget": "$100/day",
                "keywords": [
                    "life insurance quotes",
                    "compare life insurance",
                    "best life insurance rates",
                    "life insurance comparison"
                ],
                "ad_copy": "Compare Life Insurance Quotes - Find the Best Rates in 2 Minutes"
            }
        }
        
        return campaigns
    
    def generate_ai_social_content(self):
        """Stream C: AI Social Content (90-Day Plan)"""
        print(" Generating AI Social Content...")
        
        content_plan = {}
        
        # Week 1-4: Educational Content
        for week in range(1, 5):
            content_plan[f"week_{week}"] = {
                "theme": "Insurance Basics",
                "posts": [
                    "What is term life insurance?",
                    "How much life insurance do I need?",
                    "Term vs whole life insurance explained",
                    "Life insurance for young families"
                ]
            }
        
        # Week 5-8: Comparison Content
        for week in range(5, 9):
            content_plan[f"week_{week}"] = {
                "theme": "Company Reviews",
                "posts": [
                    "Best life insurance companies 2025",
                    "Policygenius vs SelectQuote comparison",
                    "Affordable life insurance options",
                    "Top-rated life insurance providers"
                ]
            }
        
        # Week 9-12: Case Studies
        for week in range(9, 13):
            content_plan[f"week_{week}"] = {
                "theme": "Success Stories",
                "posts": [
                    "How I saved $500/year on life insurance",
                    "Family protected with $1M policy",
                    "Life insurance claim success story",
                    "Why I switched insurance providers"
                ]
            }
        
        return content_plan
    
    def _generate_seo_content(self) -> List[Dict]:
        """Generate SEO blog posts"""
        posts = [
            {
                "title": "Life Insurance Quotes: How to Compare and Save Money",
                "keywords": ["life insurance quotes", "compare life insurance", "best life insurance rates"],
                "publish_date": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "title": "Best Life Insurance Companies 2025: Complete Comparison Guide",
                "keywords": ["best life insurance", "life insurance companies", "insurance comparison"],
                "publish_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            },
            {
                "title": "How Much Life Insurance Do I Need? Calculator and Guide",
                "keywords": ["life insurance calculator", "how much life insurance", "life insurance needs"],
                "publish_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            }
        ]
        return posts
    
    def _generate_reddit_posts(self) -> List[Dict]:
        """Generate Reddit post templates"""
        posts = [
            {
                "subreddit": "r/insurance",
                "title": "Life Insurance Quotes: How to Compare and Save",
                "content": "I've been comparing life insurance quotes and found some great tips. Here's what I learned...",
                "link": "https://lifequotes.ai"
            },
            {
                "subreddit": "r/personalfinance",
                "title": "Life Insurance for Young Families - What You Need to Know",
                "content": "If you're starting a family, life insurance is crucial. Here's how to get the best rates...",
                "link": "https://lifequotes.ai"
            }
        ]
        return posts
    
    def _generate_quora_answers(self) -> List[Dict]:
        """Generate Quora answer templates"""
        answers = [
            {
                "question": "How do I compare life insurance quotes?",
                "answer": "The best way to compare life insurance quotes is to use a comparison tool like LifeQuotes.ai. It lets you compare rates from multiple providers in minutes...",
                "link": "https://lifequotes.ai"
            },
            {
                "question": "What's the best life insurance company?",
                "answer": "The best life insurance company depends on your needs. Use LifeQuotes.ai to compare rates from top providers and find the best fit...",
                "link": "https://lifequotes.ai"
            }
        ]
        return answers

if __name__ == "__main__":
    triad = TrafficTriad()
    
    organic = triad.generate_organic_content()
    paid = triad.generate_paid_campaigns()
    social = triad.generate_ai_social_content()
    
    print(f"\n Organic Content: {len(organic['seo_content'])} posts")
    print(f" Paid Campaigns: {len(paid)} campaigns")
    print(f" Social Content: {len(social)} weeks planned")

