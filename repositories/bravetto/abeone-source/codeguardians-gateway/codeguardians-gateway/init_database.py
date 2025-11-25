"""
Startup script to initialize database tables and run migrations.

This script should be run when the application starts to ensure
all required database tables exist.
"""

import asyncio
import logging
from app.core.guard_metrics_migration import run_guard_metrics_migration
from app.core.database import get_engine

logger = logging.getLogger(__name__)


async def initialize_database():
    """Initialize database tables and run migrations."""
    try:
        logger.info("Starting database initialization...")
        
        # Check if database engine is available
        engine = get_engine()
        if not engine:
            logger.warning("Database engine not available. Skipping database initialization.")
            return False
        
        # Test database connection
        try:
            async with engine.begin() as conn:
                await conn.execute("SELECT 1")
            logger.info("Database connection successful")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
        
        # Run guard metrics migration
        success = await run_guard_metrics_migration()
        if success:
            logger.info("Database initialization completed successfully")
        else:
            logger.error("Database initialization failed")
        
        return success
        
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        return False


if __name__ == "__main__":
    # Run the initialization
    asyncio.run(initialize_database())
