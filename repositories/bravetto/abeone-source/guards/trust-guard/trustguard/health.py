"""
Trust Guard Health Check System

Implements comprehensive health checks for Kubernetes deployment:
- Liveness probes
- Readiness probes
- Component health checks
- Resource monitoring
- Dependency checks
"""

import time
import psutil
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class ComponentHealth:
    """Health status for a component."""
    
    def __init__(self, name: str, status: HealthStatus, message: str = "", 
                 details: Optional[Dict[str, Any]] = None):
        self.name = name
        self.status = status
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now(timezone.utc)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }


class HealthChecker:
    """Comprehensive health checker for Trust Guard components."""
    
    def __init__(self):
        self.start_time = time.time()
        self.health_history: List[Dict[str, Any]] = []
        self.max_history = 100
        
        logger.info("Health checker initialized")
    
    def check_system_resources(self) -> ComponentHealth:
        """Check system resource availability."""
        try:
            # Check memory usage
            memory = psutil.virtual_memory()
            memory_usage_percent = memory.percent
            
            # Check disk usage
            disk = psutil.disk_usage('/')
            disk_usage_percent = disk.percent
            
            # Check CPU usage (non-blocking)
            cpu_percent = psutil.cpu_percent(interval=None)
            
            # Determine status based on thresholds (adjusted for development)
            if memory_usage_percent > 95 or disk_usage_percent > 95 or cpu_percent > 95:
                status = HealthStatus.UNHEALTHY
                message = "Critical resource usage detected"
            elif memory_usage_percent > 90 or disk_usage_percent > 90 or cpu_percent > 90:
                status = HealthStatus.DEGRADED
                message = "High resource usage detected"
            else:
                status = HealthStatus.HEALTHY
                message = "Resources within normal limits"
            
            details = {
                "memory_usage_percent": memory_usage_percent,
                "disk_usage_percent": disk_usage_percent,
                "cpu_usage_percent": cpu_percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_free_gb": disk.free / (1024**3)
            }
            
            return ComponentHealth("system_resources", status, message, details)
            
        except Exception as e:
            logger.error(f"System resource check failed: {e}")
            return ComponentHealth(
                "system_resources", 
                HealthStatus.UNKNOWN, 
                f"Resource check failed: {str(e)}"
            )
    
    def check_detector_health(self, detector) -> ComponentHealth:
        """Check Trust Guard detector health."""
        try:
            if hasattr(detector, 'is_healthy'):
                is_healthy = detector.is_healthy()
                if is_healthy:
                    return ComponentHealth("detector", HealthStatus.HEALTHY, "Detector operational")
                else:
                    return ComponentHealth("detector", HealthStatus.UNHEALTHY, "Detector not responding")
            else:
                return ComponentHealth("detector", HealthStatus.UNKNOWN, "Detector health check not available")
                
        except Exception as e:
            logger.error(f"Detector health check failed: {e}")
            return ComponentHealth("detector", HealthStatus.UNHEALTHY, f"Detector error: {str(e)}")
    
    def check_validator_health(self, validator) -> ComponentHealth:
        """Check validation engine health."""
        try:
            if hasattr(validator, 'is_healthy'):
                is_healthy = validator.is_healthy()
                if is_healthy:
                    return ComponentHealth("validator", HealthStatus.HEALTHY, "Validator operational")
                else:
                    return ComponentHealth("validator", HealthStatus.UNHEALTHY, "Validator not responding")
            else:
                return ComponentHealth("validator", HealthStatus.UNKNOWN, "Validator health check not available")
                
        except Exception as e:
            logger.error(f"Validator health check failed: {e}")
            return ComponentHealth("validator", HealthStatus.UNHEALTHY, f"Validator error: {str(e)}")
    
    def check_constitutional_health(self, constitutional) -> ComponentHealth:
        """Check constitutional prompting health."""
        try:
            if hasattr(constitutional, 'is_healthy'):
                is_healthy = constitutional.is_healthy()
                if is_healthy:
                    return ComponentHealth("constitutional", HealthStatus.HEALTHY, "Constitutional system operational")
                else:
                    return ComponentHealth("constitutional", HealthStatus.UNHEALTHY, "Constitutional system not responding")
            else:
                return ComponentHealth("constitutional", HealthStatus.UNKNOWN, "Constitutional health check not available")
                
        except Exception as e:
            logger.error(f"Constitutional health check failed: {e}")
            return ComponentHealth("constitutional", HealthStatus.UNHEALTHY, f"Constitutional error: {str(e)}")
    
    def check_metrics_health(self, metrics) -> ComponentHealth:
        """Check metrics system health."""
        try:
            if hasattr(metrics, 'is_healthy'):
                is_healthy = metrics.is_healthy()
                if is_healthy:
                    return ComponentHealth("metrics", HealthStatus.HEALTHY, "Metrics system operational")
                else:
                    return ComponentHealth("metrics", HealthStatus.UNHEALTHY, "Metrics system not responding")
            else:
                return ComponentHealth("metrics", HealthStatus.UNKNOWN, "Metrics health check not available")
                
        except Exception as e:
            logger.error(f"Metrics health check failed: {e}")
            return ComponentHealth("metrics", HealthStatus.UNHEALTHY, f"Metrics error: {str(e)}")
    
    def check_auth_health(self, auth_manager) -> ComponentHealth:
        """Check authentication system health."""
        try:
            # Test API key manager validation
            if hasattr(auth_manager, 'api_key_manager'):
                # Test with a dummy key - should return None but not crash
                result = auth_manager.api_key_manager.validate_api_key("dummy_key")
                return ComponentHealth("authentication", HealthStatus.HEALTHY, "Authentication system operational")
            else:
                return ComponentHealth("authentication", HealthStatus.UNKNOWN, "Authentication system not available")
            
        except Exception as e:
            logger.error(f"Authentication health check failed: {e}")
            return ComponentHealth("authentication", HealthStatus.UNHEALTHY, f"Authentication error: {str(e)}")
    
    def check_database_health(self) -> ComponentHealth:
        """Check database connectivity (placeholder for future database integration)."""
        # For now, return healthy since we don't have a database
        return ComponentHealth("database", HealthStatus.HEALTHY, "No database dependencies")
    
    def check_external_dependencies(self) -> ComponentHealth:
        """Check external service dependencies."""
        # For now, return healthy since we don't have external dependencies
        return ComponentHealth("external_dependencies", HealthStatus.HEALTHY, "No external dependencies")
    
    def perform_comprehensive_check(self, components: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive health check of all components."""
        start_time = time.time()
        health_results = []
        
        # Validate components input
        if not isinstance(components, dict):
            components = {}
        
        # Check system resources
        health_results.append(self.check_system_resources())
        
        # Check core components
        if 'detector' in components:
            health_results.append(self.check_detector_health(components['detector']))
        
        if 'validator' in components:
            health_results.append(self.check_validator_health(components['validator']))
        
        if 'constitutional' in components:
            health_results.append(self.check_constitutional_health(components['constitutional']))
        
        if 'metrics' in components:
            health_results.append(self.check_metrics_health(components['metrics']))
        
        if 'auth_manager' in components:
            health_results.append(self.check_auth_health(components['auth_manager']))
        
        # Check any other components
        for component_name, component in components.items():
            if component_name not in ['detector', 'validator', 'constitutional', 'metrics', 'auth_manager']:
                try:
                    if hasattr(component, 'is_healthy'):
                        is_healthy = component.is_healthy()
                        status = HealthStatus.HEALTHY if is_healthy else HealthStatus.UNHEALTHY
                        health_results.append(ComponentHealth(component_name, status, f"Component {component_name} health check"))
                    else:
                        health_results.append(ComponentHealth(component_name, HealthStatus.UNKNOWN, f"Component {component_name} has no health check method"))
                except Exception as e:
                    health_results.append(ComponentHealth(component_name, HealthStatus.UNHEALTHY, f"Component {component_name} health check failed: {str(e)}"))
        
        # Check infrastructure
        health_results.append(self.check_database_health())
        health_results.append(self.check_external_dependencies())
        
        # Calculate overall health
        overall_status = self._calculate_overall_health(health_results)
        
        # Prepare response
        response = {
            "status": overall_status.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": time.time() - self.start_time,
            "check_duration_ms": (time.time() - start_time) * 1000,
            "components": [result.to_dict() for result in health_results],
            "summary": {
                "total_components": len(health_results),
                "healthy": len([r for r in health_results if r.status == HealthStatus.HEALTHY]),
                "degraded": len([r for r in health_results if r.status == HealthStatus.DEGRADED]),
                "unhealthy": len([r for r in health_results if r.status == HealthStatus.UNHEALTHY]),
                "unknown": len([r for r in health_results if r.status == HealthStatus.UNKNOWN])
            }
        }
        
        # Store in history
        self.health_history.append(response)
        if len(self.health_history) > self.max_history:
            self.health_history.pop(0)
        
        return response
    
    def _calculate_overall_health(self, health_results: List[ComponentHealth]) -> HealthStatus:
        """Calculate overall health status from component results."""
        if not health_results:
            return HealthStatus.UNKNOWN
        
        # Count statuses
        status_counts = {}
        for result in health_results:
            status_counts[result.status] = status_counts.get(result.status, 0) + 1
        
        # Determine overall status
        if HealthStatus.UNHEALTHY in status_counts:
            return HealthStatus.UNHEALTHY
        elif HealthStatus.DEGRADED in status_counts:
            return HealthStatus.DEGRADED
        elif HealthStatus.UNKNOWN in status_counts:
            return HealthStatus.UNKNOWN
        else:
            return HealthStatus.HEALTHY
    
    def get_health_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent health check history."""
        return self.health_history[-limit:]
    
    def is_ready(self, components: Dict[str, Any]) -> bool:
        """Check if the service is ready to serve traffic."""
        health_result = self.perform_comprehensive_check(components)
        return health_result["status"] in ["healthy", "degraded"]
    
    def is_alive(self) -> bool:
        """Check if the service is alive (basic liveness check)."""
        try:
            # Basic check - if we can respond, we're alive
            return True
        except Exception:
            return False


# Global health checker instance
_health_checker = None


def get_health_checker() -> HealthChecker:
    """Get the global health checker instance."""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
    return _health_checker
