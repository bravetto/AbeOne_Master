"""
Centralized Database Management for AIGuardian
Unified database access for all guard services
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, JSON, Float, Boolean, Text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()


class GuardOperation(Base):
    """Unified table for all guard operations."""
    __tablename__ = "guard_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    guard_name = Column(String(50), nullable=False, index=True)
    operation_type = Column(String(100), nullable=False)
    input_data = Column(JSON)
    output_data = Column(JSON)
    processing_time_ms = Column(Float)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    user_id = Column(String(100), index=True)
    session_id = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class GuardMetrics(Base):
    """Unified table for guard metrics."""
    __tablename__ = "guard_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    guard_name = Column(String(50), nullable=False, index=True)
    metric_type = Column(String(100), nullable=False)
    metric_value = Column(Float)
    metric_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class SystemHealth(Base):
    """System health monitoring."""
    __tablename__ = "system_health"
    
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), nullable=False, index=True)
    status = Column(String(20), nullable=False)
    health_data = Column(JSON)
    last_check = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)


class CentralizedDatabase:
    """Centralized database management for all AIGuardian services."""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.engine = None
        self.async_session = None
        self.session_factory = None
        
    async def initialize(self):
        """Initialize the centralized database."""
        try:
            # Create async engine
            self.engine = create_async_engine(
                self.config.get_database_url(),
                echo=False,
                poolclass=NullPool,
                future=True
            )
            
            # Create session factory
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Create tables
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            self.logger.info("Centralized database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize centralized database: {e}")
            raise
    
    async def get_session(self) -> AsyncSession:
        """Get a database session."""
        return self.session_factory()
    
    async def log_guard_operation(self, guard_name: str, operation_type: str,
                                input_data: Dict[str, Any], output_data: Dict[str, Any],
                                processing_time: float, success: bool = True,
                                error_message: Optional[str] = None,
                                user_id: Optional[str] = None,
                                session_id: Optional[str] = None):
        """Log a guard operation to the database."""
        async with self.get_session() as session:
            try:
                operation = GuardOperation(
                    guard_name=guard_name,
                    operation_type=operation_type,
                    input_data=input_data,
                    output_data=output_data,
                    processing_time_ms=processing_time * 1000,
                    success=success,
                    error_message=error_message,
                    user_id=user_id,
                    session_id=session_id
                )
                session.add(operation)
                await session.commit()
                
            except Exception as e:
                await session.rollback()
                self.logger.error(f"Failed to log guard operation: {e}")
                raise
    
    async def log_guard_metrics(self, guard_name: str, metric_type: str,
                              metric_value: float, metric_data: Optional[Dict[str, Any]] = None):
        """Log guard metrics to the database."""
        async with self.get_session() as session:
            try:
                metrics = GuardMetrics(
                    guard_name=guard_name,
                    metric_type=metric_type,
                    metric_value=metric_value,
                    metric_data=metric_data or {}
                )
                session.add(metrics)
                await session.commit()
                
            except Exception as e:
                await session.rollback()
                self.logger.error(f"Failed to log guard metrics: {e}")
                raise
    
    async def update_system_health(self, service_name: str, status: str,
                                 health_data: Optional[Dict[str, Any]] = None):
        """Update system health status."""
        async with self.get_session() as session:
            try:
                # Check if record exists
                from sqlalchemy import select
                result = await session.execute(
                    select(SystemHealth).where(SystemHealth.service_name == service_name)
                )
                health_record = result.scalar_one_or_none()
                
                if health_record:
                    health_record.status = status
                    health_record.health_data = health_data or {}
                    health_record.last_check = datetime.now(timezone.utc)
                else:
                    health_record = SystemHealth(
                        service_name=service_name,
                        status=status,
                        health_data=health_data or {}
                    )
                    session.add(health_record)
                
                await session.commit()
                
            except Exception as e:
                await session.rollback()
                self.logger.error(f"Failed to update system health: {e}")
                raise
    
    async def get_guard_operations(self, guard_name: Optional[str] = None,
                                 limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get guard operations from the database."""
        async with self.get_session() as session:
            try:
                from sqlalchemy import select
                query = select(GuardOperation)
                
                if guard_name:
                    query = query.where(GuardOperation.guard_name == guard_name)
                
                query = query.order_by(GuardOperation.created_at.desc()).limit(limit).offset(offset)
                
                result = await session.execute(query)
                operations = result.scalars().all()
                
                return [
                    {
                        'id': op.id,
                        'guard_name': op.guard_name,
                        'operation_type': op.operation_type,
                        'processing_time_ms': op.processing_time_ms,
                        'success': op.success,
                        'error_message': op.error_message,
                        'user_id': op.user_id,
                        'session_id': op.session_id,
                        'created_at': op.created_at.isoformat()
                    }
                    for op in operations
                ]
                
            except Exception as e:
                self.logger.error(f"Failed to get guard operations: {e}")
                return []
    
    async def get_guard_metrics(self, guard_name: Optional[str] = None,
                              metric_type: Optional[str] = None,
                              limit: int = 100) -> List[Dict[str, Any]]:
        """Get guard metrics from the database."""
        async with self.get_session() as session:
            try:
                from sqlalchemy import select
                query = select(GuardMetrics)
                
                if guard_name:
                    query = query.where(GuardMetrics.guard_name == guard_name)
                if metric_type:
                    query = query.where(GuardMetrics.metric_type == metric_type)
                
                query = query.order_by(GuardMetrics.timestamp.desc()).limit(limit)
                
                result = await session.execute(query)
                metrics = result.scalars().all()
                
                return [
                    {
                        'id': m.id,
                        'guard_name': m.guard_name,
                        'metric_type': m.metric_type,
                        'metric_value': m.metric_value,
                        'metric_data': m.metric_data,
                        'timestamp': m.timestamp.isoformat()
                    }
                    for m in metrics
                ]
                
            except Exception as e:
                self.logger.error(f"Failed to get guard metrics: {e}")
                return []
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        async with self.get_session() as session:
            try:
                from sqlalchemy import select
                result = await session.execute(select(SystemHealth))
                health_records = result.scalars().all()
                
                return {
                    record.service_name: {
                        'status': record.status,
                        'health_data': record.health_data,
                        'last_check': record.last_check.isoformat()
                    }
                    for record in health_records
                }
                
            except Exception as e:
                self.logger.error(f"Failed to get system health: {e}")
                return {}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform database health check."""
        try:
            async with self.get_session() as session:
                # Simple query to test connection
                from sqlalchemy import text
                result = await session.execute(text("SELECT 1"))
                result.scalar()
                
                return {
                    'status': 'healthy',
                    'database_url': self.config.get_database_url(),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def cleanup(self):
        """Cleanup database resources."""
        if self.engine:
            await self.engine.dispose()


