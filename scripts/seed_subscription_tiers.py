#!/usr/bin/env python3
"""
Seed subscription tiers for CodeGuardians Gateway.
"""

import asyncio
import sys
import os

# Add the directory containing the app module to the Python path
app_parent_path = os.path.join(os.path.dirname(__file__), 'codeguardians-gateway', 'codeguardians-gateway')
sys.path.insert(0, app_parent_path)

from app.core.database import get_db
from app.core.models import SubscriptionTier
from sqlalchemy import select

async def seed_subscription_tiers():
    """Seed the database with subscription tiers."""
    async for db in get_db():
        try:
            # Check if tiers already exist
            result = await db.execute(select(SubscriptionTier))
            existing_tiers = result.scalars().all()

            if existing_tiers:
                print(f"Subscription tiers already exist: {len(existing_tiers)} tiers found")
                return

            # Create default subscription tiers
            tiers_data = [
                {
                    "name": "Free",
                    "description": "Basic access for individual developers",
                    "price_monthly": 0.0,
                    "price_yearly": 0.0,
                    "limits": {
                        "api_calls_limit": 100,
                        "tokens_limit": 10000,
                        "guards_limit": 3,
                        "analytics_retention_days": 7
                    },
                    "features": [
                        "TokenGuard Basic",
                        "BiasGuard Basic",
                        "ContextGuard Basic",
                        "Basic Analytics",
                        "Community Support"
                    ],
                    "is_active": True
                },
                {
                    "name": "Pro",
                    "description": "Advanced features for growing teams",
                    "price_monthly": 29.99,
                    "price_yearly": 299.99,
                    "limits": {
                        "api_calls_limit": 10000,
                        "tokens_limit": 1000000,
                        "guards_limit": 5,
                        "analytics_retention_days": 90
                    },
                    "features": [
                        "All Guard Services",
                        "Advanced Analytics",
                        "Priority Support",
                        "Custom Integrations",
                        "API Rate Limiting",
                        "Usage Analytics"
                    ],
                    "is_active": True
                },
                {
                    "name": "Enterprise",
                    "description": "Full-featured solution for large organizations",
                    "price_monthly": 99.99,
                    "price_yearly": 999.99,
                    "limits": {
                        "api_calls_limit": 100000,
                        "tokens_limit": 10000000,
                        "guards_limit": -1,  # Unlimited
                        "analytics_retention_days": 365
                    },
                    "features": [
                        "All Pro Features",
                        "Custom Guard Development",
                        "Dedicated Support",
                        "SLA Guarantee",
                        "Advanced Security",
                        "Custom Analytics",
                        "Enterprise Integrations",
                        "Audit Logs"
                    ],
                    "is_active": True
                }
            ]

            # Insert tiers
            for tier_data in tiers_data:
                tier = SubscriptionTier(**tier_data)
                db.add(tier)

            await db.commit()

            print(f"Successfully seeded {len(tiers_data)} subscription tiers:")
            for tier_data in tiers_data:
                print(f"  - {tier_data['name']}: ${tier_data['price_monthly']}/month")

        except Exception as e:
            print(f"Error seeding subscription tiers: {e}")
            await db.rollback()
        finally:
            await db.close()
        break

if __name__ == "__main__":
    asyncio.run(seed_subscription_tiers())
