"""
Clerk webhook service for handling user events.

This service processes Clerk webhook events for user management,
including user creation, updates, and deletion.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select

try:
    import svix
except ImportError:
    svix = None

from app.core.models import User
from app.core.exceptions import ClerkWebhookError, ClerkError, EmailRequiredError, ValidationError

logger = logging.getLogger(__name__)


def verify_clerk_webhook_signature(payload: bytes, headers: Dict[str, str], webhook_secret: str) -> bool:
    """
    Verify Clerk webhook signature using svix.

    Args:
        payload: Raw webhook payload
        headers: Request headers containing svix signature
        webhook_secret: Clerk webhook secret

    Returns:
        bool: True if signature is valid, False otherwise
    """
    if svix is None:
        logger.warning("svix library not available, skipping signature verification")
        return True  # Skip verification if svix is not available for development

    try:
        # Extract svix headers
        svix_id = headers.get('svix-id')
        svix_timestamp = headers.get('svix-timestamp')
        svix_signature = headers.get('svix-signature')

        if not all([svix_id, svix_timestamp, svix_signature]):
            logger.error("Missing required svix headers for webhook verification")
            return False

        # Create svix webhook instance
        wh = svix.Webhook(webhook_secret)

        # Verify the webhook
        wh.verify(payload, {
            'svix-id': svix_id,
            'svix-timestamp': svix_timestamp,
            'svix-signature': svix_signature
        })

        logger.info("Clerk webhook signature verified successfully")
        return True

    except Exception as e:
        logger.error(f"Clerk webhook signature verification failed: {e}")
        return False


class ClerkWebhookService:
    """Service for handling Clerk webhook events."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> None:
        """
        Validate user data from Clerk webhook.
        
        Args:
            user_data: User data from webhook payload
            
        Raises:
            EmailRequiredError: If email is missing or invalid
            ValidationError: If other required fields are missing
        """
        # Check required fields
        if not user_data.get('id'):
            from app.core.exceptions import ValidationError
            raise ValidationError(
                message="Missing required field: id",
                details={"field": "id"}
            )
        
        # Check email addresses
        email_addresses = user_data.get('email_addresses', [])
        if not email_addresses:
            raise EmailRequiredError(
                message="Email address is required for user creation",
                details={"field": "email_addresses", "provided": None}
            )
        
        # Validate email format
        primary_email = email_addresses[0].get('email_address')
        if not primary_email:
            raise EmailRequiredError(
                message="Email address is required for user creation",
                details={"field": "email_address", "provided": email_addresses}
            )
        
        # Basic email format validation
        if '@' not in primary_email or '.' not in primary_email.split('@')[-1]:
            from app.core.exceptions import ValidationError
            raise ValidationError(
                message=f"Invalid email format: {primary_email}",
                details={"field": "email_address", "value": primary_email}
            )
        
        # Validate timestamp fields if present
        timestamp_fields = ['created_at', 'updated_at', 'last_active_at', 'last_sign_in_at']
        for field in timestamp_fields:
            if field in user_data and user_data[field] is not None:
                try:
                    int(user_data[field])
                except (ValueError, TypeError):
                    from app.core.exceptions import ValidationError
                    raise ValidationError(
                        message=f"Invalid timestamp format for {field}",
                        details={"field": field, "value": user_data[field]}
                    )
    
    async def handle_user_created(self, event_data: Dict[str, Any]) -> bool:
        """
        Handle user.created webhook event.
        
        Args:
            event_data: The webhook event data from Clerk
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            user_data = event_data.get('data', {})
            
            # Validate user data (will raise EmailRequiredError if email missing)
            self.validate_user_data(user_data)
            
            clerk_user_id = user_data.get('id')
            
            # Extract email from email_addresses array
            email_addresses = user_data.get('email_addresses', [])
            primary_email = email_addresses[0].get('email_address') if email_addresses else None
            
            if not primary_email:
                raise EmailRequiredError(
                    message="Email address is required for user creation",
                    details={"field": "email_address", "provided": email_addresses}
                )
            
            # Check if user already exists
            result = await self.db.execute(
                select(User).where(User.clerk_user_id == clerk_user_id)
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                logger.info(f"User with Clerk ID {clerk_user_id} already exists, updating instead")
                return await self.handle_user_updated(event_data)
            
            # Create new user
            user = User(
                clerk_user_id=clerk_user_id,
                email=primary_email,
                full_name=f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip(),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                image_url=user_data.get('image_url'),
                profile_image_url=user_data.get('profile_image_url'),
                username=user_data.get('username'),
                locale=user_data.get('locale'),
                last_active_at=self._parse_timestamp(user_data.get('last_active_at')),
                last_sign_in_at=self._parse_timestamp(user_data.get('last_sign_in_at')),
                password_enabled=user_data.get('password_enabled', True),
                two_factor_enabled=user_data.get('two_factor_enabled', False),
                totp_enabled=user_data.get('totp_enabled', False),
                backup_code_enabled=user_data.get('backup_code_enabled', False),
                banned=user_data.get('banned', False),
                locked=user_data.get('locked', False),
                verification_attempts_remaining=user_data.get('verification_attempts_remaining', 100),
                primary_email_address_id=user_data.get('primary_email_address_id'),
                primary_phone_number_id=user_data.get('primary_phone_number_id'),
                primary_web3_wallet_id=user_data.get('primary_web3_wallet_id'),
                external_id=user_data.get('external_id'),
                clerk_created_at=self._parse_timestamp(user_data.get('created_at')),
                clerk_updated_at=self._parse_timestamp(user_data.get('updated_at')),
                clerk_private_metadata=user_data.get('private_metadata', {}),
                clerk_public_metadata=user_data.get('public_metadata', {}),
                clerk_unsafe_metadata=user_data.get('unsafe_metadata', {}),
                is_active=not user_data.get('banned', False),
                is_verified=True  # Clerk users are considered verified
            )
            
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            
            logger.info(f"Successfully created user {clerk_user_id} from Clerk webhook")
            return True
            
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"Integrity error creating user from Clerk webhook: {e}")
            return False
        except (EmailRequiredError, ValidationError):
            # Re-raise validation errors so they can be handled by the API layer
            await self.db.rollback()
            raise
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Database error creating user from Clerk webhook: {e}")
            return False
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error handling user.created webhook: {e}")
            return False
    
    async def handle_user_updated(self, event_data: Dict[str, Any]) -> bool:
        """
        Handle user.updated webhook event.
        
        Args:
            event_data: The webhook event data from Clerk
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            user_data = event_data.get('data', {})
            
            # Validate user data (will raise exceptions if invalid)
            try:
                self.validate_user_data(user_data)
            except (EmailRequiredError, ValidationError) as e:
                logger.error(f"Invalid user data in user.updated event: {e.message}")
                # For updates, email is not always required (user might already exist)
                # Only fail if id is missing
                if not user_data.get('id'):
                    raise
            
            clerk_user_id = user_data.get('id')
            
            # Find existing user
            result = await self.db.execute(
                select(User).where(User.clerk_user_id == clerk_user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                logger.warning(f"User with Clerk ID {clerk_user_id} not found, creating new user")
                return await self.handle_user_created(event_data)
            
            # Extract email from email_addresses array
            email_addresses = user_data.get('email_addresses', [])
            primary_email = None
            if email_addresses:
                primary_email = email_addresses[0].get('email_address')
            
            # Update user fields
            if primary_email:
                user.email = primary_email
            
            user.full_name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
            user.first_name = user_data.get('first_name')
            user.last_name = user_data.get('last_name')
            user.image_url = user_data.get('image_url')
            user.profile_image_url = user_data.get('profile_image_url')
            user.username = user_data.get('username')
            user.locale = user_data.get('locale')
            user.last_active_at = self._parse_timestamp(user_data.get('last_active_at'))
            user.last_sign_in_at = self._parse_timestamp(user_data.get('last_sign_in_at'))
            user.password_enabled = user_data.get('password_enabled', True)
            user.two_factor_enabled = user_data.get('two_factor_enabled', False)
            user.totp_enabled = user_data.get('totp_enabled', False)
            user.backup_code_enabled = user_data.get('backup_code_enabled', False)
            user.banned = user_data.get('banned', False)
            user.locked = user_data.get('locked', False)
            user.verification_attempts_remaining = user_data.get('verification_attempts_remaining', 100)
            user.primary_email_address_id = user_data.get('primary_email_address_id')
            user.primary_phone_number_id = user_data.get('primary_phone_number_id')
            user.primary_web3_wallet_id = user_data.get('primary_web3_wallet_id')
            user.external_id = user_data.get('external_id')
            user.clerk_updated_at = self._parse_timestamp(user_data.get('updated_at'))
            user.clerk_private_metadata = user_data.get('private_metadata', {})
            user.clerk_public_metadata = user_data.get('public_metadata', {})
            user.clerk_unsafe_metadata = user_data.get('unsafe_metadata', {})
            user.is_active = not user_data.get('banned', False)
            
            await self.db.commit()
            await self.db.refresh(user)
            
            logger.info(f"Successfully updated user {clerk_user_id} from Clerk webhook")
            return True
            
        except (EmailRequiredError, ValidationError):
            # Re-raise validation errors so they can be handled by the API layer
            await self.db.rollback()
            raise
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Database error updating user from Clerk webhook: {e}")
            return False
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error handling user.updated webhook: {e}")
            return False
    
    async def handle_user_deleted(self, event_data: Dict[str, Any]) -> bool:
        """
        Handle user.deleted webhook event.
        
        Args:
            event_data: The webhook event data from Clerk
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            user_data = event_data.get('data', {})
            clerk_user_id = user_data.get('id')
            
            if not clerk_user_id:
                logger.error("No Clerk user ID found in user.deleted event")
                return False
            
            # Find and soft delete user
            result = await self.db.execute(
                select(User).where(User.clerk_user_id == clerk_user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                logger.warning(f"User with Clerk ID {clerk_user_id} not found for deletion")
                # Commit the transaction (even though no changes were made) to properly close it
                await self.db.commit()
                return True  # Consider this successful since user doesn't exist
            
            # Soft delete by setting is_active to False
            user.is_active = False
            user.clerk_updated_at = datetime.now(timezone.utc)
            
            await self.db.commit()
            await self.db.refresh(user)
            
            logger.info(f"Successfully soft deleted user {clerk_user_id} from Clerk webhook")
            return True
            
        except (EmailRequiredError, ValidationError):
            # Re-raise validation errors so they can be handled by the API layer
            await self.db.rollback()
            raise
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Database error deleting user from Clerk webhook: {e}")
            return False
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error handling user.deleted webhook: {e}")
            return False
    
    def _parse_timestamp(self, timestamp: Optional[int]) -> Optional[datetime]:
        """
        Parse Clerk timestamp (milliseconds since epoch) to datetime.
        
        Args:
            timestamp: Timestamp in milliseconds since epoch
            
        Returns:
            datetime object or None if timestamp is None
        """
        if timestamp is None:
            return None
        
        try:
            # Convert milliseconds to seconds
            return datetime.fromtimestamp(timestamp / 1000)
        except (ValueError, TypeError):
            logger.warning(f"Invalid timestamp format: {timestamp}")
            return None


async def process_clerk_webhook(event_type: str, event_data: Dict[str, Any], db: AsyncSession) -> bool:
    """
    Process a Clerk webhook event.
    
    Args:
        event_type: The type of webhook event (e.g., 'user.created')
        event_data: The webhook event data
        db: Database session
        
    Returns:
        bool: True if successful, False otherwise
    """
    service = ClerkWebhookService(db)
    
    try:
        if event_type == 'user.created':
            return await service.handle_user_created(event_data)
        elif event_type == 'user.updated':
            return await service.handle_user_updated(event_data)
        elif event_type == 'user.deleted':
            return await service.handle_user_deleted(event_data)
        else:
            logger.warning(f"Unsupported Clerk webhook event type: {event_type}")
            return False
    except (EmailRequiredError, ValidationError):
        # Re-raise validation errors so they can be handled specifically by the webhook endpoint
        raise
    except Exception as e:
        logger.error(f"Error processing Clerk webhook {event_type}: {e}")
        raise ClerkWebhookError(
            message=f"Failed to process Clerk webhook event: {event_type}",
            details={"event_type": event_type, "error": str(e)}
        )
