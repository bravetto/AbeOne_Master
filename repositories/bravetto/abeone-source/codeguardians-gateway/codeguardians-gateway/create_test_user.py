#!/usr/bin/env python3
"""
Create a test user for authentication testing.
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.core.database import get_db
from app.core.models import User
from app.core.security import get_password_hash
from sqlalchemy import select

async def create_test_user():
    """Create a test user for authentication testing."""
    async for db in get_db():
        try:
            # Check if test user already exists
            result = await db.execute(
                select(User).where(User.email == "test@example.com")
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print("Test user already exists")
                return
            
            # Create test user
            test_user = User(
                email="test@example.com",
                hashed_REPLACE_MEtest"),
                full_name="Test User",
                is_active=True,
                is_verified=True,
                is_superuser=False
            )
            
            db.add(test_user)
            await db.commit()
            await db.refresh(test_user)
            
            print(f"Test user created successfully: {test_user.email}")
            print("Credentials:")
            print("  Email: test@example.com")
            print("  Password: test")
            
        except Exception as e:
            print(f"Error creating test user: {e}")
            await db.rollback()
        finally:
            await db.close()
        break

if __name__ == "__main__":
    asyncio.run(create_test_user())
