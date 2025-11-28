"""
Shared error handling utilities with DRY patterns.

This module provides reusable error handling patterns commonly used across the application,
reducing code duplication and ensuring consistent error responses.
"""

import logging
from typing import Optional, Dict, Any, Callable, Awaitable
from contextlib import asynccontextmanager
from functools import wraps

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Centralized error handling utilities."""

    @staticmethod
    async def handle_database_error(
        e: Exception,
        operation: str,
        db: Optional[AsyncSession] = None,
        log_level: str = "error"
    ) -> None:
        """Handle database operation errors with consistent logging and rollback."""
        log_method = getattr(logger, log_level, logger.error)
        log_method(f"Failed to {operation}: {e}", exc_info=True)

        if db:
            try:
                await db.rollback()
            except Exception as rollback_error:
                logger.error(f"Failed to rollback transaction: {rollback_error}")

        raise HTTPException(status_code=500, detail=f"Failed to {operation}")

    @staticmethod
    def handle_validation_error(
        e: Exception,
        operation: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Handle validation errors with structured response."""
        logger.warning(f"Validation failed for {operation}: {e}")
        error_details = {"message": str(e)}
        if details:
            error_details.update(details)
        raise HTTPException(status_code=422, detail=error_details)

    @staticmethod
    def handle_authentication_error(
        e: Exception,
        operation: str = "authenticate"
    ) -> None:
        """Handle authentication errors."""
        logger.warning(f"Authentication failed for {operation}: {e}")
        raise HTTPException(status_code=401, detail="Authentication required")

    @staticmethod
    def handle_authorization_error(
        e: Exception,
        operation: str = "authorize",
        required_permission: Optional[str] = None
    ) -> None:
        """Handle authorization errors."""
        detail = f"Permission '{required_permission}' required" if required_permission else "Access denied"
        logger.warning(f"Authorization failed for {operation}: {e}")
        raise HTTPException(status_code=403, detail=detail)

    @staticmethod
    def handle_not_found_error(
        resource_type: str,
        resource_id: Any
    ) -> None:
        """Handle resource not found errors."""
        logger.info(f"{resource_type} not found: {resource_id}")
        raise HTTPException(status_code=404, detail=f"{resource_type} not found")

    @staticmethod
    def handle_conflict_error(
        e: Exception,
        operation: str,
        details: Optional[str] = None
    ) -> None:
        """Handle resource conflict errors."""
        logger.warning(f"Conflict in {operation}: {e}")
        detail = details or f"Conflict in {operation}"
        raise HTTPException(status_code=409, detail=detail)

    @staticmethod
    def handle_external_service_error(
        service_name: str,
        e: Exception,
        operation: str = "communicate"
    ) -> None:
        """Handle external service communication errors."""
        logger.error(f"External service error ({service_name}): {e}", exc_info=True)
        raise HTTPException(
            status_code=502,
            detail=f"External service error: {service_name}"
        )


def database_operation(
    operation_name: str,
    rollback_on_error: bool = True,
    log_level: str = "error"
):
    """
    Decorator for database operations with consistent error handling.

    Usage:
        @database_operation("create user")
        async def create_user(user_data: dict, db: AsyncSession):
            # Your database operation code here
            pass
    """
    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            db = None
            # Find the database session in arguments
            for arg in args:
                if isinstance(arg, AsyncSession):
                    db = arg
                    break
            if not db:
                for value in kwargs.values():
                    if isinstance(value, AsyncSession):
                        db = value
                        break

            try:
                return await func(*args, **kwargs)
            except Exception as e:
                await ErrorHandler.handle_database_error(
                    e, operation_name, db if rollback_on_error else None, log_level
                )

        return wrapper
    return decorator


def api_operation(
    operation_name: str,
    error_type: str = "database"
):
    """
    Decorator for API operations with consistent error handling.

    Usage:
        @api_operation("get user")
        async def get_user(user_id: int):
            # Your API operation code here
            pass
    """
    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                # Re-raise HTTP exceptions as-is
                raise
            except Exception as e:
                if error_type == "database":
                    await ErrorHandler.handle_database_error(e, operation_name)
                elif error_type == "validation":
                    ErrorHandler.handle_validation_error(e, operation_name)
                elif error_type == "auth":
                    ErrorHandler.handle_authentication_error(e, operation_name)
                elif error_type == "external":
                    ErrorHandler.handle_external_service_error("service", e, operation_name)
                else:
                    logger.error(f"Unexpected error in {operation_name}: {e}", exc_info=True)
                    raise HTTPException(status_code=500, detail=f"Internal error in {operation_name}")

        return wrapper
    return decorator


@asynccontextmanager
async def database_transaction(db: AsyncSession):
    """
    Context manager for database transactions with automatic rollback on error.

    Usage:
        async with database_transaction(db):
            # Your database operations here
            db.add(new_record)
            await db.commit()
    """
    try:
        yield
    except Exception as e:
        logger.error(f"Transaction failed: {e}", exc_info=True)
        await db.rollback()
        raise
    finally:
        # Ensure connection is returned to pool
        pass


def safe_db_operation(
    operation: Callable[..., Awaitable[Any]],
    *args,
    operation_name: str = "database operation",
    **kwargs
) -> Awaitable[Any]:
    """
    Execute a database operation safely with error handling.

    Usage:
        result = await safe_db_operation(
            db.execute,
            select(User).where(User.id == user_id),
            operation_name="get user"
        )
    """
    async def wrapper():
        try:
            return await operation(*args, **kwargs)
        except Exception as e:
            await ErrorHandler.handle_database_error(e, operation_name)

    return wrapper()


class ErrorContext:
    """Context for tracking error information across operations."""

    def __init__(self, operation: str, user_id: Optional[str] = None, resource_id: Optional[str] = None):
        self.operation = operation
        self.user_id = user_id
        self.resource_id = resource_id
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = __import__('time').time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = __import__('time').time()
        duration = self.end_time - self.start_time

        if exc_type:
            logger.error(
                f"Operation '{self.operation}' failed after {duration:.3f}s: {exc_val}",
                extra={
                    "operation": self.operation,
                    "user_id": self.user_id,
                    "resource_id": self.resource_id,
                    "duration": duration,
                    "error_type": exc_type.__name__
                },
                exc_info=exc_tb
            )
        else:
            logger.debug(
                f"Operation '{self.operation}' completed in {duration:.3f}s",
                extra={
                    "operation": self.operation,
                    "user_id": self.user_id,
                    "resource_id": self.resource_id,
                    "duration": duration
                }
            )


# Convenience functions for common error patterns
async def handle_db_create_error(e: Exception, resource_type: str, db: AsyncSession):
    """Handle database creation errors."""
    await ErrorHandler.handle_database_error(e, f"create {resource_type}", db)

async def handle_db_update_error(e: Exception, resource_type: str, resource_id: Any, db: AsyncSession):
    """Handle database update errors."""
    await ErrorHandler.handle_database_error(e, f"update {resource_type} {resource_id}", db)

async def handle_db_delete_error(e: Exception, resource_type: str, resource_id: Any, db: AsyncSession):
    """Handle database deletion errors."""
    await ErrorHandler.handle_database_error(e, f"delete {resource_type} {resource_id}", db)

def handle_not_found(resource_type: str, resource_id: Any):
    """Handle resource not found errors."""
    ErrorHandler.handle_not_found_error(resource_type, resource_id)

def handle_validation_error(e: Exception, field_name: str, value: Any = None):
    """Handle validation errors."""
    details = {"field": field_name}
    if value is not None:
        details["value"] = str(value)
    ErrorHandler.handle_validation_error(e, f"validate {field_name}", details)
