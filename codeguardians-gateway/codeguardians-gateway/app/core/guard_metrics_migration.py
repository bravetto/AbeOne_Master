"""
Database Migration: Create Guard Metrics Tables

This migration creates the guard_operations and guard_metrics tables
for real metrics tracking.
"""

from sqlalchemy import text
from app.core.database import get_engine
import logging

logger = logging.getLogger(__name__)


async def create_guard_metrics_tables():
    """Create the guard metrics tables if they don't exist."""
    try:
        engine = get_engine()
        if not engine:
            logger.error("Database engine not available")
            return False
        
        async with engine.begin() as conn:
            # Create guard_operations table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS guard_operations (
                    id SERIAL PRIMARY KEY,
                    guard_name VARCHAR(50) NOT NULL,
                    operation_type VARCHAR(100) NOT NULL,
                    input_data JSONB,
                    output_data JSONB,
                    processing_time_ms FLOAT,
                    success BOOLEAN DEFAULT TRUE,
                    error_message TEXT,
                    user_id VARCHAR(100),
                    session_id VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create indexes for guard_operations
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_guard_operations_guard_name 
                ON guard_operations(guard_name)
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_guard_operations_created_at 
                ON guard_operations(created_at)
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_guard_operations_user_id 
                ON guard_operations(user_id)
            """))
            
            # Create guard_metrics table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS guard_metrics (
                    id SERIAL PRIMARY KEY,
                    guard_name VARCHAR(50) NOT NULL,
                    metric_type VARCHAR(100) NOT NULL,
                    metric_value FLOAT,
                    metric_data JSONB,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create indexes for guard_metrics
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_guard_metrics_guard_name 
                ON guard_metrics(guard_name)
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_guard_metrics_timestamp 
                ON guard_metrics(timestamp)
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_guard_metrics_metric_type 
                ON guard_metrics(metric_type)
            """))
            
            logger.info("Successfully created guard metrics tables")
            return True
            
    except Exception as e:
        logger.error(f"Error creating guard metrics tables: {e}")
        return False


async def run_guard_metrics_migration():
    """Run the guard metrics migration."""
    logger.info("Starting guard metrics migration...")
    success = await create_guard_metrics_tables()
    if success:
        logger.info("Guard metrics migration completed successfully")
    else:
        logger.error("Guard metrics migration failed")
    return success
