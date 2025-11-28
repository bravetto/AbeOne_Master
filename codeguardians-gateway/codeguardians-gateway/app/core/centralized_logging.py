"""
Centralized Logging System for AIGuardian
Unified logging across all services with Elasticsearch integration
"""

import json
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

import structlog
from elasticsearch import Elasticsearch
from pythonjsonlogger import jsonlogger


class CentralizedLogging:
    """Centralized logging system for all AIGuardian services."""
    
    def __init__(self, config):
        self.config = config
        self.elasticsearch_client = None
        self.logger = None
        
    async def initialize(self):
        """Initialize the centralized logging system."""
        try:
            # Initialize Elasticsearch client
            self.elasticsearch_client = Elasticsearch(
                [self.config.get_elasticsearch_url()],
                timeout=30,
                max_retries=3,
                retry_on_timeout=True
            )
            
            # Configure structured logging
            self._configure_structlog()
            
            # Create main logger
            self.logger = structlog.get_logger("aiguardian")
            
            # Test Elasticsearch connection
            if self.elasticsearch_client.ping():
                self.logger.info("Elasticsearch connection established")
            else:
                self.logger.warning("Elasticsearch connection failed, using file logging only")
                
        except Exception as e:
            print(f"Failed to initialize centralized logging: {e}")
            # Fallback to basic logging
            self._configure_basic_logging()
    
    def _configure_structlog(self):
        """Configure structured logging with JSON output."""
        # Configure structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                self._add_service_context,
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    
    def _configure_basic_logging(self):
        """Configure basic logging as fallback."""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('/app/logs/aiguardian.log')
            ]
        )
    
    def _add_service_context(self, logger, method_name, event_dict):
        """Add service context to log entries."""
        event_dict['service'] = 'aiguardian-gateway'
        event_dict['environment'] = self.config.ENVIRONMENT
        event_dict['version'] = '2.0.0'
        return event_dict
    
    async def log_guard_operation(self, guard_name: str, operation: str, 
                                input_data: Dict[str, Any], 
                                output_data: Dict[str, Any],
                                processing_time: float,
                                success: bool = True,
                                error: Optional[str] = None):
        """Log a guard service operation."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'aiguardian-gateway',
            'guard_service': guard_name,
            'operation': operation,
            'input_size': len(str(input_data)),
            'output_size': len(str(output_data)),
            'processing_time_ms': processing_time * 1000,
            'success': success,
            'error': error,
            'level': 'error' if error else 'info'
        }
        
        # Add to Elasticsearch if available
        if self.elasticsearch_client and self.elasticsearch_client.ping():
            try:
                self.elasticsearch_client.index(
                    index=f"aiguardian-guard-operations-{datetime.now().strftime('%Y.%m.%d')}",
                    body=log_entry
                )
            except Exception as e:
                self.logger.warning(f"Failed to log to Elasticsearch: {e}")
        
        # Log locally
        if error:
            self.logger.error(f"Guard operation failed: {guard_name}.{operation}", **log_entry)
        else:
            self.logger.info(f"Guard operation completed: {guard_name}.{operation}", **log_entry)
    
    async def log_api_request(self, method: str, path: str, status_code: int,
                            processing_time: float, user_id: Optional[str] = None,
                            request_size: int = 0, response_size: int = 0):
        """Log an API request."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'aiguardian-gateway',
            'type': 'api_request',
            'method': method,
            'path': path,
            'status_code': status_code,
            'processing_time_ms': processing_time * 1000,
            'user_id': user_id,
            'request_size': request_size,
            'response_size': response_size,
            'level': 'error' if status_code >= 400 else 'info'
        }
        
        # Add to Elasticsearch if available
        if self.elasticsearch_client and self.elasticsearch_client.ping():
            try:
                self.elasticsearch_client.index(
                    index=f"aiguardian-api-requests-{datetime.now().strftime('%Y.%m.%d')}",
                    body=log_entry
                )
            except Exception as e:
                self.logger.warning(f"Failed to log to Elasticsearch: {e}")
        
        # Log locally
        self.logger.info(f"API request: {method} {path}", **log_entry)
    
    async def log_system_event(self, event_type: str, message: str, 
                             details: Optional[Dict[str, Any]] = None):
        """Log a system event."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'aiguardian-gateway',
            'type': 'system_event',
            'event_type': event_type,
            'message': message,
            'details': details or {},
            'level': 'info'
        }
        
        # Add to Elasticsearch if available
        if self.elasticsearch_client and self.elasticsearch_client.ping():
            try:
                self.elasticsearch_client.index(
                    index=f"aiguardian-system-events-{datetime.now().strftime('%Y.%m.%d')}",
                    body=log_entry
                )
            except Exception as e:
                self.logger.warning(f"Failed to log to Elasticsearch: {e}")
        
        # Log locally
        self.logger.info(f"System event: {event_type}", **log_entry)
    
    async def log_metrics(self, metrics_type: str, metrics_data: Dict[str, Any]):
        """Log metrics data."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'aiguardian-gateway',
            'type': 'metrics',
            'metrics_type': metrics_type,
            'data': metrics_data,
            'level': 'info'
        }
        
        # Add to Elasticsearch if available
        if self.elasticsearch_client and self.elasticsearch_client.ping():
            try:
                self.elasticsearch_client.index(
                    index=f"aiguardian-metrics-{datetime.now().strftime('%Y.%m.%d')}",
                    body=log_entry
                )
            except Exception as e:
                self.logger.warning(f"Failed to log to Elasticsearch: {e}")
        
        # Log locally
        self.logger.info(f"Metrics: {metrics_type}", **log_entry)
    
    def get_logger(self, name: str = "aiguardian"):
        """Get a logger instance."""
        return structlog.get_logger(name)
    
    async def cleanup(self):
        """Cleanup logging resources."""
        if self.elasticsearch_client:
            self.elasticsearch_client.close()


