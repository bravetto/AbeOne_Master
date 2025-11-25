"""
Shared database utilities to eliminate duplication in database operations.

This module provides common database patterns and transaction handling
to reduce code duplication across API endpoints.
"""

import logging
from typing import Any, Dict, List, Optional, Type, TypeVar
from contextlib import asynccontextmanager

from sqlalchemy import select, update, delete, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from shared.utils.error_handling import ErrorHandler

logger = logging.getLogger(__name__)

T = TypeVar('T')


class DatabaseUtils:
    """Utility class for common database operations."""

    @staticmethod
    @asynccontextmanager
    async def transaction(db: AsyncSession):
        """
        Context manager for database transactions with automatic rollback on error.

        Usage:
            async with DatabaseUtils.transaction(db):
                # Perform database operations
                await db.execute(...)
                await db.commit()
        """
        try:
            yield db
        except Exception as e:
            await db.rollback()
            logger.error(f"Transaction rolled back due to error: {e}")
            raise

    @staticmethod
    async def execute_with_commit(
        db: AsyncSession,
        operation: str,
        *queries
    ) -> None:
        """
        Execute database queries and commit with error handling.

        Args:
            db: Database session
            operation: Description of the operation for logging
            *queries: SQLAlchemy queries to execute
        """
        try:
            for query in queries:
                await db.execute(query)
            await db.commit()
            logger.debug(f"Successfully executed {operation}")
        except Exception as e:
            await db.rollback()
            await ErrorHandler.handle_database_error(e, operation, db)

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        model: Type[T],
        id_value: Any,
        id_field: str = "id"
    ) -> Optional[T]:
        """
        Generic function to get a record by ID.

        Args:
            db: Database session
            model: SQLAlchemy model class
            id_value: ID value to search for
            id_field: Name of the ID field (default: "id")

        Returns:
            Model instance or None if not found
        """
        try:
            query = select(model).where(getattr(model, id_field) == id_value)
            result = await db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting {model.__name__} by {id_field}={id_value}: {e}")
            return None

    @staticmethod
    async def get_by_field(
        db: AsyncSession,
        model: Type[T],
        field_name: str,
        field_value: Any
    ) -> Optional[T]:
        """
        Generic function to get a record by any field.

        Args:
            db: Database session
            model: SQLAlchemy model class
            field_name: Name of the field to search
            field_value: Value to search for

        Returns:
            Model instance or None if not found
        """
        try:
            query = select(model).where(getattr(model, field_name) == field_value)
            result = await db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting {model.__name__} by {field_name}={field_value}: {e}")
            return None

    @staticmethod
    async def get_all(
        db: AsyncSession,
        model: Type[T],
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[T]:
        """
        Generic function to get all records with optional filtering.

        Args:
            db: Database session
            model: SQLAlchemy model class
            filters: Optional dict of field filters
            order_by: Optional field name to order by
            limit: Optional limit for results
            offset: Optional offset for pagination

        Returns:
            List of model instances
        """
        try:
            query = select(model)

            # Apply filters
            if filters:
                conditions = []
                for field, value in filters.items():
                    if isinstance(value, list):
                        conditions.append(getattr(model, field).in_(value))
                    else:
                        conditions.append(getattr(model, field) == value)
                if conditions:
                    query = query.where(and_(*conditions))

            # Apply ordering
            if order_by:
                query = query.order_by(getattr(model, order_by))

            # Apply pagination
            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            result = await db.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error getting all {model.__name__} records: {e}")
            return []

    @staticmethod
    async def count_records(
        db: AsyncSession,
        model: Type[T],
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Count records with optional filtering.

        Args:
            db: Database session
            model: SQLAlchemy model class
            filters: Optional dict of field filters

        Returns:
            Number of matching records
        """
        try:
            query = select(func.count()).select_from(model)

            if filters:
                conditions = []
                for field, value in filters.items():
                    if isinstance(value, list):
                        conditions.append(getattr(model, field).in_(value))
                    else:
                        conditions.append(getattr(model, field) == value)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await db.execute(query)
            return result.scalar() or 0
        except Exception as e:
            logger.error(f"Error counting {model.__name__} records: {e}")
            return 0

    @staticmethod
    async def create_record(
        db: AsyncSession,
        model: Type[T],
        data: Dict[str, Any]
    ) -> Optional[T]:
        """
        Create a new record.

        Args:
            db: Database session
            model: SQLAlchemy model class
            data: Data to create the record with

        Returns:
            Created model instance or None on error
        """
        try:
            record = model(**data)
            db.add(record)
            await db.commit()
            await db.refresh(record)
            logger.info(f"Created {model.__name__} record with ID {record.id}")
            return record
        except Exception as e:
            await db.rollback()
            await ErrorHandler.handle_database_error(e, f"create {model.__name__}", db)
            return None

    @staticmethod
    async def update_record(
        db: AsyncSession,
        model: Type[T],
        record_id: Any,
        data: Dict[str, Any],
        id_field: str = "id"
    ) -> bool:
        """
        Update an existing record.

        Args:
            db: Database session
            model: SQLAlchemy model class
            record_id: ID of the record to update
            data: Data to update
            id_field: Name of the ID field

        Returns:
            True if update successful, False otherwise
        """
        try:
            query = (
                update(model)
                .where(getattr(model, id_field) == record_id)
                .values(**data)
            )
            result = await db.execute(query)
            await db.commit()

            if result.rowcount > 0:
                logger.info(f"Updated {model.__name__} record {record_id}")
                return True
            else:
                logger.warning(f"No {model.__name__} record found with {id_field}={record_id}")
                return False
        except Exception as e:
            await db.rollback()
            await ErrorHandler.handle_database_error(e, f"update {model.__name__}", db)
            return False

    @staticmethod
    async def delete_record(
        db: AsyncSession,
        model: Type[T],
        record_id: Any,
        id_field: str = "id"
    ) -> bool:
        """
        Delete a record.

        Args:
            db: Database session
            model: SQLAlchemy model class
            record_id: ID of the record to delete
            id_field: Name of the ID field

        Returns:
            True if deletion successful, False otherwise
        """
        try:
            query = delete(model).where(getattr(model, id_field) == record_id)
            result = await db.execute(query)
            await db.commit()

            if result.rowcount > 0:
                logger.info(f"Deleted {model.__name__} record {record_id}")
                return True
            else:
                logger.warning(f"No {model.__name__} record found with {id_field}={record_id}")
                return False
        except Exception as e:
            await db.rollback()
            await ErrorHandler.handle_database_error(e, f"delete {model.__name__}", db)
            return False

    @staticmethod
    async def exists(
        db: AsyncSession,
        model: Type[T],
        filters: Dict[str, Any]
    ) -> bool:
        """
        Check if a record exists with given filters.

        Args:
            db: Database session
            model: SQLAlchemy model class
            filters: Dict of field filters

        Returns:
            True if record exists, False otherwise
        """
        try:
            query = select(func.count()).select_from(model)

            conditions = []
            for field, value in filters.items():
                if isinstance(value, list):
                    conditions.append(getattr(model, field).in_(value))
                else:
                    conditions.append(getattr(model, field) == value)

            if conditions:
                query = query.where(and_(*conditions))

            result = await db.execute(query)
            count = result.scalar() or 0
            return count > 0
        except Exception as e:
            logger.error(f"Error checking existence in {model.__name__}: {e}")
            return False
