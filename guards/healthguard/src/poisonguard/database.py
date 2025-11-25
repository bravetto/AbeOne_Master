"""
Database models and operations for PoisonGuard.
Provides audit trail and persistence for analysis results.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Float, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import uuid
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class AnalysisAudit(Base):
    """Audit trail for analysis operations."""
    __tablename__ = 'analysis_audit'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sample_id = Column(String, nullable=False, index=True)
    is_poisoned = Column(Boolean, nullable=False)
    confidence = Column(Float, nullable=False)
    details = Column(JSON)
    correlation_id = Column(String, nullable=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    processing_time_ms = Column(Integer, nullable=True)
    plugin_results = Column(JSON, nullable=True)


class MitigationAudit(Base):
    """Audit trail for mitigation operations."""
    __tablename__ = 'mitigation_audit'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sample_id = Column(String, nullable=False, index=True)
    action_taken = Column(String, nullable=False)
    details = Column(JSON)
    correlation_id = Column(String, nullable=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    processing_time_ms = Column(Integer, nullable=True)


class SystemMetrics(Base):
    """System metrics storage."""
    __tablename__ = 'system_metrics'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    memory_usage_bytes = Column(Integer, nullable=False)
    cpu_usage_percent = Column(Float, nullable=False)
    active_requests = Column(Integer, nullable=False, default=0)
    health_status = Column(String, nullable=False, default='healthy')


class DatabaseManager:
    """Database manager for PoisonGuard operations."""
    
    def __init__(self, database_url: str = "sqlite:///poisonguard.db"):
        """Initialize database connection."""
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)
        logger.info(f"Database initialized with URL: {database_url}")
    
    def get_session(self) -> Session:
        """Get database session."""
        return self.SessionLocal()
    
    def store_analysis_result(self, 
                            sample_id: str, 
                            is_poisoned: bool, 
                            confidence: float, 
                            details: Dict[str, Any],
                            correlation_id: Optional[str] = None,
                            processing_time_ms: Optional[int] = None,
                            plugin_results: Optional[Dict[str, Any]] = None) -> str:
        """Store analysis result in audit trail."""
        with self.get_session() as session:
            audit = AnalysisAudit(
                sample_id=sample_id,
                is_poisoned=is_poisoned,
                confidence=confidence,
                details=details,
                correlation_id=correlation_id,
                processing_time_ms=processing_time_ms,
                plugin_results=plugin_results
            )
            session.add(audit)
            session.commit()
            logger.info(f"Stored analysis result for sample {sample_id}")
            return audit.id
    
    def store_mitigation_result(self,
                               sample_id: str,
                               action_taken: str,
                               details: Dict[str, Any],
                               correlation_id: Optional[str] = None,
                               processing_time_ms: Optional[int] = None) -> str:
        """Store mitigation result in audit trail."""
        with self.get_session() as session:
            audit = MitigationAudit(
                sample_id=sample_id,
                action_taken=action_taken,
                details=details,
                correlation_id=correlation_id,
                processing_time_ms=processing_time_ms
            )
            session.add(audit)
            session.commit()
            logger.info(f"Stored mitigation result for sample {sample_id}")
            return audit.id
    
    def store_system_metrics(self,
                           memory_usage_bytes: int,
                           cpu_usage_percent: float,
                           active_requests: int = 0,
                           health_status: str = 'healthy') -> str:
        """Store system metrics."""
        with self.get_session() as session:
            metrics = SystemMetrics(
                memory_usage_bytes=memory_usage_bytes,
                cpu_usage_percent=cpu_usage_percent,
                active_requests=active_requests,
                health_status=health_status
            )
            session.add(metrics)
            session.commit()
            return metrics.id
    
    def get_analysis_history(self, 
                           sample_id: Optional[str] = None,
                           correlation_id: Optional[str] = None,
                           limit: int = 100) -> List[Dict[str, Any]]:
        """Get analysis history with optional filters."""
        with self.get_session() as session:
            query = session.query(AnalysisAudit)
            
            if sample_id:
                query = query.filter(AnalysisAudit.sample_id == sample_id)
            if correlation_id:
                query = query.filter(AnalysisAudit.correlation_id == correlation_id)
            
            results = query.order_by(AnalysisAudit.timestamp.desc()).limit(limit).all()
            
            return [
                {
                    'id': result.id,
                    'sample_id': result.sample_id,
                    'is_poisoned': result.is_poisoned,
                    'confidence': result.confidence,
                    'details': result.details,
                    'correlation_id': result.correlation_id,
                    'timestamp': result.timestamp.isoformat(),
                    'processing_time_ms': result.processing_time_ms,
                    'plugin_results': result.plugin_results
                }
                for result in results
            ]
    
    def get_mitigation_history(self,
                             sample_id: Optional[str] = None,
                             correlation_id: Optional[str] = None,
                             limit: int = 100) -> List[Dict[str, Any]]:
        """Get mitigation history with optional filters."""
        with self.get_session() as session:
            query = session.query(MitigationAudit)
            
            if sample_id:
                query = query.filter(MitigationAudit.sample_id == sample_id)
            if correlation_id:
                query = query.filter(MitigationAudit.correlation_id == correlation_id)
            
            results = query.order_by(MitigationAudit.timestamp.desc()).limit(limit).all()
            
            return [
                {
                    'id': result.id,
                    'sample_id': result.sample_id,
                    'action_taken': result.action_taken,
                    'details': result.details,
                    'correlation_id': result.correlation_id,
                    'timestamp': result.timestamp.isoformat(),
                    'processing_time_ms': result.processing_time_ms
                }
                for result in results
            ]
    
    def get_system_metrics_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get system metrics history."""
        with self.get_session() as session:
            results = session.query(SystemMetrics).order_by(
                SystemMetrics.timestamp.desc()
            ).limit(limit).all()
            
            return [
                {
                    'id': result.id,
                    'timestamp': result.timestamp.isoformat(),
                    'memory_usage_bytes': result.memory_usage_bytes,
                    'cpu_usage_percent': result.cpu_usage_percent,
                    'active_requests': result.active_requests,
                    'health_status': result.health_status
                }
                for result in results
            ]
    
    def cleanup_old_records(self, days_to_keep: int = 30) -> int:
        """Clean up old audit records."""
        cutoff_date = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - timedelta(days=days_to_keep)
        
        with self.get_session() as session:
            # Clean up analysis audit
            analysis_deleted = session.query(AnalysisAudit).filter(
                AnalysisAudit.timestamp < cutoff_date
            ).delete()
            
            # Clean up mitigation audit
            mitigation_deleted = session.query(MitigationAudit).filter(
                MitigationAudit.timestamp < cutoff_date
            ).delete()
            
            # Clean up old system metrics (keep more recent ones)
            metrics_cutoff = datetime.now(timezone.utc) - timedelta(days=7)
            metrics_deleted = session.query(SystemMetrics).filter(
                SystemMetrics.timestamp < metrics_cutoff
            ).delete()
            
            session.commit()
            
            total_deleted = analysis_deleted + mitigation_deleted + metrics_deleted
            logger.info(f"Cleaned up {total_deleted} old records")
            return total_deleted


# Global database manager instance
db_manager = DatabaseManager()
