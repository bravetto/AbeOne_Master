"""
Shared user service to eliminate duplication in user operations.

This module provides centralized user management functions that can be
reused across different parts of the application.
"""

import logging
from typing import Dict, Any, List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.services.database_utils import DatabaseUtils
from shared.services.error_handling import ErrorHandler

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related operations."""

    @staticmethod
    async def get_user_by_id(
        user_id: int,
        db: AsyncSession
    ) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.

        Args:
            user_id: User ID to retrieve
            db: Database session

        Returns:
            User data as dict or None if not found
        """
        try:
            from app.core.models import User  # Import here to avoid circular imports
            user = await DatabaseUtils.get_by_id(db, User, user_id)
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "is_superuser": user.is_superuser,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                }
            return None
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            return None

    @staticmethod
    async def get_user_by_email(
        email: str,
        db: AsyncSession
    ) -> Optional[Dict[str, Any]]:
        """
        Get user by email address.

        Args:
            email: Email address to search for
            db: Database session

        Returns:
            User data as dict or None if not found
        """
        try:
            from app.core.models import User
            user = await DatabaseUtils.get_by_field(db, User, "email", email)
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "is_superuser": user.is_superuser,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                }
            return None
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None

    @staticmethod
    async def get_user_by_clerk_id(
        clerk_user_id: str,
        db: AsyncSession
    ) -> Optional[Dict[str, Any]]:
        """
        Get user by Clerk user ID.

        Args:
            clerk_user_id: Clerk user ID to search for
            db: Database session

        Returns:
            User data as dict or None if not found
        """
        try:
            from app.core.models import User
            user = await DatabaseUtils.get_by_field(db, User, "clerk_user_id", clerk_user_id)
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "is_superuser": user.is_superuser,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                }
            return None
        except Exception as e:
            logger.error(f"Error getting user by Clerk ID {clerk_user_id}: {e}")
            return None

    @staticmethod
    async def update_user_profile(
        user_id: int,
        update_data: Dict[str, Any],
        db: AsyncSession
    ) -> bool:
        """
        Update user profile information.

        Args:
            user_id: User ID to update
            update_data: Data to update
            db: Database session

        Returns:
            True if update successful, False otherwise
        """
        try:
            from app.core.models import User

            # Validate update data
            allowed_fields = {"full_name", "email"}
            filtered_data = {k: v for k, v in update_data.items() if k in allowed_fields}

            if not filtered_data:
                logger.warning(f"No valid fields to update for user {user_id}")
                return False

            # Check if email is already taken (if email is being updated)
            if "email" in filtered_data:
                existing_user = await DatabaseUtils.get_by_field(
                    db, User, "email", filtered_data["email"]
                )
                if existing_user and existing_user.id != user_id:
                    logger.warning(f"Email {filtered_data['email']} already taken")
                    return False

            success = await DatabaseUtils.update_record(
                db, User, user_id, filtered_data
            )

            if success:
                logger.info(f"Updated profile for user {user_id}")
            return success

        except Exception as e:
            logger.error(f"Error updating user profile {user_id}: {e}")
            return False

    @staticmethod
    async def get_user_sessions(
        user_id: int,
        db: AsyncSession,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent sessions for a user.

        Args:
            user_id: User ID to get sessions for
            db: Database session
            limit: Maximum number of sessions to return

        Returns:
            List of session data
        """
        try:
            from app.core.models import UserSession

            sessions = await DatabaseUtils.get_all(
                db, UserSession,
                filters={"user_id": user_id},
                order_by="created_at",
                limit=limit
            )

            return [
                {
                    "id": session.id,
                    "session_id": session.session_id,
                    "ip_address": session.ip_address,
                    "user_agent": session.user_agent,
                    "created_at": session.created_at.isoformat() if session.created_at else None,
                    "last_activity": session.last_activity.isoformat() if session.last_activity else None,
                    "is_active": session.is_active,
                }
                for session in sessions
            ]

        except Exception as e:
            logger.error(f"Error getting sessions for user {user_id}: {e}")
            return []

    @staticmethod
    async def deactivate_user(
        user_id: int,
        db: AsyncSession
    ) -> bool:
        """
        Deactivate a user account.

        Args:
            user_id: User ID to deactivate
            db: Database session

        Returns:
            True if deactivation successful, False otherwise
        """
        try:
            success = await DatabaseUtils.update_record(
                db, User, user_id, {"is_active": False}
            )

            if success:
                logger.info(f"Deactivated user account {user_id}")
                # Could also deactivate all sessions, send notification, etc.

            return success

        except Exception as e:
            logger.error(f"Error deactivating user {user_id}: {e}")
            return False

    @staticmethod
    async def check_user_exists(
        filters: Dict[str, Any],
        db: AsyncSession
    ) -> bool:
        """
        Check if a user exists with given filters.

        Args:
            filters: Filters to check (e.g., {"email": "user@example.com"})
            db: Database session

        Returns:
            True if user exists, False otherwise
        """
        try:
            from app.core.models import User
            return await DatabaseUtils.exists(db, User, filters)
        except Exception as e:
            logger.error(f"Error checking user existence: {e}")
            return False

    @staticmethod
    async def get_user_count(
        db: AsyncSession,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Get count of users with optional filters.

        Args:
            db: Database session
            filters: Optional filters

        Returns:
            Number of users matching filters
        """
        try:
            from app.core.models import User
            return await DatabaseUtils.count_records(db, User, filters)
        except Exception as e:
            logger.error(f"Error counting users: {e}")
            return 0
