"""Clerk integration utilities."""

import jwt
import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.core.config import get_settings
from app.core.models import User
from app.core.exceptions import AuthenticationError, ClerkTokenError, ClerkJWKSFetchError, ClerkError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.logging import get_logger
from app.utils.retry import retry_async, circuit_breaker

logger = get_logger(__name__)
settings = get_settings()

async def verify_clerk_token(token: str) -> Dict[str, Any]:
    """Verify Clerk JWT token and return user data using proper JWKS verification."""

    if not settings.CLERK_PUBLISHABLE_KEY:
        raise ClerkError("Clerk frontend API key not configured")

    try:
        # Extract header to get kid (key ID)
        header = jwt.get_unverified_header(token)
        kid = header.get('kid')

        if not kid:
            raise ClerkTokenError("Invalid Clerk token: missing key ID")

        # Get the JWKS endpoint
        jwks_url = f"https://{settings.CLERK_PUBLISHABLE_KEY}/.well-known/jwks.json"

        # Fetch JWKS with retry and circuit breaker
        @circuit_breaker("clerk_jwks", failure_threshold=3, recovery_timeout=30.0)
        async def fetch_jwks():
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                response = await client.get(jwks_url)
                response.raise_for_status()
                return response.json()

        try:
            jwks = await retry_async(
                fetch_jwks,
                max_attempts=2,
                delay=0.5,
                exceptions=(httpx.RequestError, httpx.TimeoutException)
            )
        except Exception as e:
            logger.error(f"Failed to fetch JWKS from {jwks_url}: {e}")
            raise ClerkJWKSFetchError(
                message="Unable to fetch Clerk public keys",
                details={"url": jwks_url, "error": str(e)}
            ) from e

        # Find the key with matching kid
        key = None
        for jwk_key in jwks.get('keys', []):
            if jwk_key.get('kid') == kid:
                key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk_key)
                break

        if not key:
            raise ClerkJWKSFetchError("Invalid Clerk token: key not found in JWKS")

        # Verify and decode the token
        payload = jwt.decode(
            token,
            key=key,
            algorithms=['RS256'],
            audience=None,  # Clerk tokens don't have a specific audience
            issuer=f"https://{settings.CLERK_PUBLISHABLE_KEY}",
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "verify_nbf": True,
                "require": ["exp", "iat", "sub"]
            }
        )

        # Validate required fields
        if not payload.get("sub"):
            raise ClerkTokenError("Invalid Clerk token: missing subject")

        # Additional Clerk-specific validations
        if payload.get("azp") != settings.CLERK_PUBLISHABLE_KEY:
            raise ClerkTokenError("Invalid Clerk token: invalid authorized party")

        return payload

    except jwt.ExpiredSignatureError:
        raise ClerkTokenError("Clerk token has expired")
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid Clerk token: {e}")
        raise ClerkTokenError("Invalid Clerk token")
    except httpx.RequestError as e:
        logger.error(f"Failed to fetch JWKS: {e}")
        raise ClerkJWKSFetchError("Token verification service unavailable")
    except Exception as e:
        logger.error(f"Error verifying Clerk token: {e}")
        raise ClerkTokenError("Token verification failed")

async def get_or_create_user_from_clerk(clerk_user: Dict[str, Any], db: AsyncSession) -> User:
    """Get or create user from Clerk user data."""
    try:
        clerk_user_id = clerk_user["sub"]
        email = clerk_user["email"]
        
        # Check if user exists by clerk_user_id
        result = await db.execute(
            select(User).where(User.clerk_user_id == clerk_user_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # Update existing user if needed
            if user.email != email:
                user.email = email
            if user.full_name != clerk_user.get("name", ""):
                user.full_name = clerk_user.get("name", "")
            if user.is_verified != clerk_user.get("email_verified", False):
                user.is_verified = clerk_user.get("email_verified", False)
            
            await db.commit()
            await db.refresh(user)
            logger.info(f"Updated existing user: {user.id} - {email}")
            return user
        
        # Check if user exists by email (for migration purposes)
        result = await db.execute(
            select(User).where(User.email == email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            # Link existing user to Clerk
            existing_user.clerk_user_id = clerk_user_id
            existing_user.is_verified = clerk_user.get("email_verified", False)
            await db.commit()
            await db.refresh(existing_user)
            logger.info(f"Linked existing user to Clerk: {existing_user.id} - {email}")
            return existing_user
        
        # Create new user
        new_user = User(
            clerk_user_id=clerk_user_id,
            email=email,
            full_name=clerk_user.get("name", ""),
            is_active=True,
            is_verified=clerk_user.get("email_verified", False),
            is_superuser=False
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info(f"Created new user from Clerk: {new_user.id} - {email}")
        return new_user
        
    except Exception as e:
        logger.error(f"Error creating/updating user from Clerk: {e}")
        await db.rollback()
        raise

async def get_user_by_clerk_id(clerk_user_id: str, db: AsyncSession) -> Optional[User]:
    """Get user by Clerk user ID."""
    try:
        result = await db.execute(
            select(User).where(User.clerk_user_id == clerk_user_id)
        )
        return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error getting user by Clerk ID: {e}")
        return None

async def link_user_to_stripe_customer(user_id: int, stripe_customer_id: str, db: AsyncSession) -> bool:
    """Link user to Stripe customer."""
    try:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.error(f"User {user_id} not found for Stripe linking")
            return False
        
        user.stripe_customer_id = stripe_customer_id
        await db.commit()
        
        logger.info(f"Linked user {user_id} to Stripe customer {stripe_customer_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error linking user to Stripe customer: {e}")
        await db.rollback()
        return False

def extract_clerk_user_from_token(token: str) -> Dict[str, Any]:
    """Extract user information from Clerk token without verification."""
    try:
        # Decode without verification to extract user data
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        
        return {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "name": payload.get("name", ""),
            "email_verified": payload.get("email_verified", False),
            "picture": payload.get("picture"),
            "given_name": payload.get("given_name"),
            "family_name": payload.get("family_name")
        }
        
    except Exception as e:
        logger.error(f"Error extracting user from Clerk token: {e}")
        return {}
