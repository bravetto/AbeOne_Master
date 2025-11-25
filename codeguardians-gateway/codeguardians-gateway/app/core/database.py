"""
Database configuration and session management.

This module provides database connection, session management, and
initialization for the application.
"""

from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
import logging

from app.core.config import get_settings
from app.core.models import Base
from app.core.aws_secrets import aws_secrets

logger = logging.getLogger(__name__)

# Global variables for database engine and session
_engine: Optional[create_async_engine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        settings = get_settings()

        # Try to get database URL from AWS Secrets Manager first
        database_url = None
        if settings.AWS_SECRETS_ENABLED:
            try:
                database_url = aws_secrets.get_database_url()
                if database_url:
                    logger.info("Using database URL from AWS Secrets Manager")
            except Exception as e:
                logger.warning(f"Failed to get database URL from AWS Secrets Manager: {e}")
        
        # Fallback to environment variable
        if not database_url:
            database_url = settings.database_url

        # Check if database is enabled
        if not settings.DATABASE_ENABLED or not database_url:
            logger.warning("Database is disabled or DATABASE_URL not provided. Database features will be unavailable.")
            return None

        # Ensure asyncpg driver is used for async operations
        if database_url and database_url.startswith("postgresql://"):
            # Replace postgresql:// with postgresql+asyncpg:// for async support
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            logger.info("Converted postgresql:// to postgresql+asyncpg:// for async support")
        elif database_url and database_url.startswith("postgres://"):
            # Replace postgres:// with postgresql+asyncpg:// for async support
            database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
            logger.info("Converted postgres:// to postgresql+asyncpg:// for async support")

        # Handle SSL parameters for Neon and other cloud databases
        # asyncpg doesn't support sslmode in URL, so we extract it and use connect_args
        ssl_required = False
        if database_url and '?' in database_url:
            url_parts = database_url.split('?')
            base_url = url_parts[0]
            query_params = url_parts[1] if len(url_parts) > 1 else ""
            
            # Check if SSL is required
            if 'sslmode=require' in query_params or 'sslmode=prefer' in query_params:
                ssl_required = True
                # Remove query parameters for asyncpg (it doesn't support them in URL)
                database_url = base_url
            elif 'sslmode' in query_params:
                # Other sslmode values - remove query string
                database_url = base_url
            else:
                # No SSL params, remove query string for compatibility
                database_url = base_url
        
        # Build connect_args with SSL if required
        connect_args = {
            "server_settings": {
                "application_name": "codeguardians-gateway"
            }
        }
        
        # Add SSL configuration if required (asyncpg uses ssl=True for SSL connections)
        if ssl_required:
            # For Neon and other cloud databases requiring SSL
            # asyncpg automatically uses SSL when connecting to cloud databases
            # but we can explicitly enable it
            connect_args["ssl"] = True
        
        _engine = create_async_engine(
            database_url,
            echo=settings.DEBUG,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_recycle=settings.DATABASE_POOL_RECYCLE,
            pool_pre_ping=True,
            future=True,
            connect_args=connect_args
        )
        logger.info("Database engine created")
    return _engine


def get_session_factory():
    """Get or create the session factory."""
    global _session_factory
    if _session_factory is None:
        engine = get_engine()
        if engine is None:
            logger.warning("Cannot create session factory: Database engine is not available")
            return None
        _session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=True,
            autocommit=False
        )
        logger.info("Session factory created")
    return _session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.

    Yields:
        AsyncSession: Database session

    Raises:
        HTTPException: If database is not enabled (503 Service Unavailable)
    """
    from fastapi import HTTPException
    
    try:
        session_factory = get_session_factory()
        if session_factory is None:
            logger.warning("Database is not enabled - get_db() called but database unavailable")
            raise HTTPException(
                status_code=503,
                detail="Service temporarily unavailable - database connection not available"
            )

        async with session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    except HTTPException:
        # Re-raise HTTP exceptions (like the 503 above)
        raise
    except RuntimeError as e:
        # Convert RuntimeError from get_session_factory to HTTPException
        logger.error(f"Database runtime error: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable - database connection failed"
        )


async def init_db() -> None:
    """Initialize database tables."""
    try:
        engine = get_engine()
        if engine is None:
            logger.info("Database initialization skipped: Database not enabled")
            return

        async with engine.begin() as conn:
            # Create all tables (ignore if they already exist)
            try:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Database tables created successfully")
            except Exception as create_error:
                # If tables already exist, that's okay - just log it
                if "already exists" in str(create_error) or "DuplicateTableError" in str(create_error):
                    logger.info("Database tables already exist, skipping creation")
                else:
                    raise create_error

            # Run any initialization queries
            await _run_init_queries(conn)

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def _run_init_queries(conn) -> None:
    """Run initialization queries."""
    try:
        # Create indexes that might not be created by SQLAlchemy
        init_queries = [
            # Add any custom indexes or constraints here
            "CREATE INDEX IF NOT EXISTS ix_users_email_lower ON users (LOWER(email));",
            "CREATE INDEX IF NOT EXISTS ix_posts_title_search ON posts USING gin(to_tsvector('english', title));",
            "CREATE INDEX IF NOT EXISTS ix_posts_content_search ON posts USING gin(to_tsvector('english', content));",
        ]
        
        for query in init_queries:
            try:
                await conn.execute(text(query))
            except Exception as e:
                logger.warning(f"Failed to execute init query '{query}': {e}")
        
        logger.info("Database initialization queries completed")
        
    except Exception as e:
        logger.error(f"Failed to run initialization queries: {e}")
        raise


async def close_db() -> None:
    """Close database connections."""
    global _engine, _session_factory
    
    if _engine:
        await _engine.dispose()
        _engine = None
        logger.info("Database engine disposed")
    
    _session_factory = None


async def run_migrations() -> None:
    """
    Run Alembic database migrations.
    
    This function runs all pending migrations on startup to ensure
    the database schema is up to date.
    """
    try:
        import subprocess
        import sys
        from pathlib import Path
        
        # Get the alembic directory path
        alembic_dir = Path(__file__).parent.parent.parent / "alembic"
        
        logger.info(f"Running database migrations from {alembic_dir}")
        
        # Run alembic upgrade
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=str(alembic_dir.parent),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("Database migrations completed successfully")
            if result.stdout:
                logger.debug(f"Migration output: {result.stdout}")
        else:
            logger.error(f"Database migrations failed: {result.stderr}")
            # Don't raise error to allow app to continue
            
    except Exception as e:
        logger.warning(f"Failed to run migrations: {e}. This may be expected in development.")


async def check_db_connection() -> bool:
    """Check if database connection is working."""
    try:
        engine = get_engine()
        if engine is None:
            logger.info("Database connection check skipped: Database not enabled")
            return False

        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


async def get_db_stats() -> dict:
    """Get database statistics."""
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            # Get table counts
            stats = {}
            
            # Count users
            result = await conn.execute(text("SELECT COUNT(*) FROM users"))
            stats['users'] = result.scalar()
            
            # Count posts
            result = await conn.execute(text("SELECT COUNT(*) FROM posts"))
            stats['posts'] = result.scalar()
            
            # Count active sessions
            result = await conn.execute(text("SELECT COUNT(*) FROM sessions WHERE is_active = true"))
            stats['active_sessions'] = result.scalar()
            
            # Count API keys
            result = await conn.execute(text("SELECT COUNT(*) FROM api_keys WHERE is_active = true"))
            stats['active_api_keys'] = result.scalar()
            
            return stats
            
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {}


class DatabaseManager:
    """Database management utilities."""
    
    def __init__(self):
        self.engine = get_engine()
        self.session_factory = get_session_factory()
    
    async def create_tables(self) -> None:
        """Create all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self) -> None:
        """Drop all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    async def reset_database(self) -> None:
        """Reset database by dropping and recreating all tables."""
        await self.drop_tables()
        await self.create_tables()
    
    async def backup_database(self, backup_path: str) -> None:
        """Create a database backup."""
        try:
            import subprocess
            import os
            from urllib.parse import urlparse
            
            # Get database URL from engine
            db_url = str(self.engine.url)
            parsed_url = urlparse(db_url)
            
            if parsed_url.scheme == "postgresql+asyncpg":
                # PostgreSQL backup using pg_dump
                host = parsed_url.hostname or "localhost"
                port = parsed_url.port or 5432
                database = parsed_url.path.lstrip('/')
                username = parsed_url.username
                password = parsed_url.password
                
                # Set PGPASSWORD environment variable
                env = os.environ.copy()
                if password:
                    env['PGPASSWORD'] = password
                
                # Create pg_dump command
                cmd = [
                    'pg_dump',
                    '-h', host,
                    '-p', str(port),
                    '-U', username or 'postgres',
                    '-d', database,
                    '-f', backup_path,
                    '--verbose'
                ]
                
                # Run pg_dump
                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise Exception(f"pg_dump failed: {result.stderr}")
                
                logger.info(f"Database backup created successfully: {backup_path}")
                
            elif parsed_url.scheme == "sqlite+aiosqlite":
                # SQLite backup - copy the database file
                import shutil
                db_file = parsed_url.path
                if not os.path.exists(db_file):
                    raise Exception(f"SQLite database file not found: {db_file}")
                
                shutil.copy2(db_file, backup_path)
                logger.info(f"SQLite database backup created: {backup_path}")
                
            else:
                raise NotImplementedError(f"Backup not implemented for database type: {parsed_url.scheme}")
                
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            raise
    
    async def restore_database(self, backup_path: str) -> None:
        """Restore database from backup."""
        try:
            import subprocess
            import os
            from urllib.parse import urlparse
            
            # Check if backup file exists
            if not os.path.exists(backup_path):
                raise Exception(f"Backup file not found: {backup_path}")
            
            # Get database URL from engine
            db_url = str(self.engine.url)
            parsed_url = urlparse(db_url)
            
            if parsed_url.scheme == "postgresql+asyncpg":
                # PostgreSQL restore using pg_restore
                host = parsed_url.hostname or "localhost"
                port = parsed_url.port or 5432
                database = parsed_url.path.lstrip('/')
                username = parsed_url.username
                password = parsed_url.password
                
                # Set PGPASSWORD environment variable
                env = os.environ.copy()
                if password:
                    env['PGPASSWORD'] = password
                
                # Drop existing database and recreate
                drop_cmd = [
                    'psql',
                    '-h', host,
                    '-p', str(port),
                    '-U', username or 'postgres',
                    '-d', 'postgres',  # Connect to postgres database to drop target
                    '-c', f'DROP DATABASE IF EXISTS {database};'
                ]
                
                create_cmd = [
                    'psql',
                    '-h', host,
                    '-p', str(port),
                    '-U', username or 'postgres',
                    '-d', 'postgres',
                    '-c', f'CREATE DATABASE {database};'
                ]
                
                restore_cmd = [
                    'pg_restore',
                    '-h', host,
                    '-p', str(port),
                    '-U', username or 'postgres',
                    '-d', database,
                    '--verbose',
                    '--clean',
                    '--if-exists',
                    backup_path
                ]
                
                # Execute commands
                for cmd in [drop_cmd, create_cmd, restore_cmd]:
                    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                    if result.returncode != 0:
                        logger.warning(f"Command {' '.join(cmd)} had warnings: {result.stderr}")
                
                logger.info(f"Database restored successfully from: {backup_path}")
                
            elif parsed_url.scheme == "sqlite+aiosqlite":
                # SQLite restore - copy the backup file over the database file
                import shutil
                db_file = parsed_url.path
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(db_file), exist_ok=True)
                
                # Copy backup to database location
                shutil.copy2(backup_path, db_file)
                logger.info(f"SQLite database restored from: {backup_path}")
                
            else:
                raise NotImplementedError(f"Restore not implemented for database type: {parsed_url.scheme}")
                
        except Exception as e:
            logger.error(f"Database restore failed: {e}")
            raise
