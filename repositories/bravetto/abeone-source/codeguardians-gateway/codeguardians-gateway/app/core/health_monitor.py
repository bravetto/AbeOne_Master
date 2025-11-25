"""
AI Guardians Health Monitoring

Comprehensive health monitoring for all services with enhanced checks.
"""

import asyncio
import time
import psutil
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Health check result."""
    service: str
    status: HealthStatus
    response_time: float
    timestamp: float
    details: Dict[str, Any]
    error: Optional[str] = None


class ServiceHealthMonitor:
    """Comprehensive service health monitoring."""
    
    def __init__(self):
        # Use environment variables with fallback to docker-compose service names
        import os
        from urllib.parse import urlparse, urlunparse
        
        # Extract base URLs from environment variables, defaulting to docker-compose service names
        tokenguard_url = os.getenv("TOKENGUARD_URL", "http://tokenguard:8000")
        trustguard_url = os.getenv("TRUSTGUARD_URL", "http://trustguard:8000")
        contextguard_url = os.getenv("CONTEXTGUARD_URL", "http://contextguard:8003")  # Fixed: Standardized to port 8003 (matches docs/tests)
        biasguard_url = os.getenv("BIASGUARD_URL", "http://biasguard:8000")
        healthguard_url = os.getenv("HEALTHGUARD_URL", "http://healthguard:8000")
        securityguard_url = os.getenv("SECURITYGUARD_URL", "http://securityguard:8000")
        
        # Remove any path components and preserve protocol (http/https)
        def get_base_url(url):
            """
            Extract base URL preserving the original protocol.

            Args:
                url: Full URL that may include protocol, path, query params, etc.

            Returns:
                Base URL with original protocol (http://host:port or https://host:port)
            """
            # Handle URLs without schemes properly
            if not url:
                return "http://"

            # If URL starts with '//', it's scheme-relative, add http
            if url.startswith('//'):
                url = 'http:' + url
            # If URL doesn't contain '://' at all, assume it's host:port and add http://
            elif '://' not in url:
                # Remove leading slash if present (invalid URL format)
                if url.startswith('/'):
                    url = url[1:]
                url = 'http://' + url

            # Parse URL to extract components
            parsed = urlparse(url)

            # Preserve scheme or default to http
            scheme = parsed.scheme or "http"

            # Reconstruct URL with only scheme, netloc (host:port)
            # This preserves http/https and removes path, query, fragment
            base_url = urlunparse((scheme, parsed.netloc, "", "", "", ""))

            return base_url
        
        # Get gateway URL from environment or construct from host/port
        gateway_host = os.getenv("HOST", "localhost")
        gateway_port = os.getenv("PORT", os.getenv("GATEWAY_PORT", "8000"))
        gateway_url = f"http://{gateway_host}:{gateway_port}"
        
        self.services = {
            "codeguardians-gateway": f"{gateway_url}/health/live",
            "tokenguard": f"{get_base_url(tokenguard_url)}/health",
            "trustguard": f"{get_base_url(trustguard_url)}/health",
            "contextguard": f"{get_base_url(contextguard_url)}/health",
            "biasguard": f"{get_base_url(biasguard_url)}/health",
            "healthguard": f"{get_base_url(healthguard_url)}/health",
            "securityguard": f"{get_base_url(securityguard_url)}/health",
            "postgres": "REPLACE_MEpostgres:5432/codeguardians-gateway_db",
            "redis": "REPLACE_MEredis:6379/0"
        }
        self.health_history = []
        self.max_history = 100
    
    async def check_service_health(self, service_name: str, endpoint: str) -> HealthCheck:
        """Check health of a single service."""
        start_time = time.time()
        
        try:
            if service_name in ["postgres", "redis"]:
                return await self._check_database_health(service_name, endpoint)
            else:
                return await self._check_http_health(service_name, endpoint)
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Health check failed for {service_name}: {e}")
            
            return HealthCheck(
                service=service_name,
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                timestamp=time.time(),
                details={},
                error=str(e)
            )
    
    async def _check_http_health(self, service_name: str, endpoint: str) -> HealthCheck:
        """Check HTTP service health."""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                # Increase timeout for TrustGuard which can be slow
                timeout_seconds = 40 if service_name == "trustguard" else 5
                async with session.get(endpoint, timeout=timeout_seconds) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        status = HealthStatus.HEALTHY
                        
                        # Check for degraded status based on response
                        if response_time > 2.0:
                            status = HealthStatus.DEGRADED
                        
                        return HealthCheck(
                            service=service_name,
                            status=status,
                            response_time=response_time,
                            timestamp=time.time(),
                            details=data
                        )
                    else:
                        return HealthCheck(
                            service=service_name,
                            status=HealthStatus.UNHEALTHY,
                            response_time=response_time,
                            timestamp=time.time(),
                            details={"status_code": response.status},
                            error=f"HTTP {response.status}"
                        )
        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            return HealthCheck(
                service=service_name,
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                timestamp=time.time(),
                details={},
                error="Timeout"
            )
    
    async def _check_database_health(self, service_name: str, endpoint: str) -> HealthCheck:
        """Check database service health."""
        start_time = time.time()
        
        try:
            if service_name == "postgres":
                return await self._check_postgres_health(endpoint)
            elif service_name == "redis":
                return await self._check_redis_health(endpoint)
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                service=service_name,
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                timestamp=time.time(),
                details={},
                error=str(e)
            )
    
    async def _check_postgres_health(self, connection_string: str) -> HealthCheck:
        """Check PostgreSQL health."""
        start_time = time.time()
        
        try:
            import asyncpg
            conn = await asyncpg.connect(connection_string)
            
            # Test basic query
            result = await conn.fetchval("SELECT 1")
            await conn.close()
            
            response_time = time.time() - start_time
            
            return HealthCheck(
                service="postgres",
                status=HealthStatus.HEALTHY,
                response_time=response_time,
                timestamp=time.time(),
                details={"query_result": result}
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                service="postgres",
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                timestamp=time.time(),
                details={},
                error=str(e)
            )
    
    async def _check_redis_health(self, connection_string: str) -> HealthCheck:
        """Check Redis health."""
        start_time = time.time()
        
        try:
            import redis.asyncio as redis
            client = redis.from_url(connection_string)
            
            # Test basic operation
            await client.ping()
            await client.close()
            
            response_time = time.time() - start_time
            
            return HealthCheck(
                service="redis",
                status=HealthStatus.HEALTHY,
                response_time=response_time,
                timestamp=time.time(),
                details={"ping": "PONG"}
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                service="redis",
                status=HealthStatus.UNHEALTHY,
                response_time=response_time,
                timestamp=time.time(),
                details={},
                error=str(e)
            )
    
    async def check_all_services(self) -> List[HealthCheck]:
        """Check health of all services."""
        tasks = []
        for service_name, endpoint in self.services.items():
            task = self.check_service_health(service_name, endpoint)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and convert to HealthCheck objects
        health_checks = []
        for result in results:
            if isinstance(result, HealthCheck):
                health_checks.append(result)
            else:
                logger.error(f"Health check failed with exception: {result}")
        
        # Store in history
        self.health_history.extend(health_checks)
        if len(self.health_history) > self.max_history:
            self.health_history = self.health_history[-self.max_history:]
        
        return health_checks
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get health summary for all services."""
        if not self.health_history:
            return {"status": "unknown", "services": []}
        
        # Get latest health checks
        latest_checks = {}
        for check in self.health_history:
            if check.service not in latest_checks or check.timestamp > latest_checks[check.service].timestamp:
                latest_checks[check.service] = check
        
        # Calculate overall status
        statuses = [check.status for check in latest_checks.values()]
        if HealthStatus.UNHEALTHY in statuses:
            overall_status = "unhealthy"
        elif HealthStatus.DEGRADED in statuses:
            overall_status = "degraded"
        elif all(status == HealthStatus.HEALTHY for status in statuses):
            overall_status = "healthy"
        else:
            overall_status = "unknown"
        
        return {
            "status": overall_status,
            "timestamp": time.time(),
            "services": [
                {
                    "name": check.service,
                    "status": check.status.value,
                    "response_time": check.response_time,
                    "error": check.error
                }
                for check in latest_checks.values()
            ]
        }
    
    def get_health_history(self, service_name: Optional[str] = None) -> List[HealthCheck]:
        """Get health check history."""
        if service_name:
            return [check for check in self.health_history if check.service == service_name]
        return self.health_history


class SystemResourceMonitor:
    """System resource monitoring."""
    
    def __init__(self):
        self.cpu_threshold = 80.0
        self.memory_threshold = 80.0
        self.disk_threshold = 90.0
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            
            return {
                "cpu": {
                    "percent": cpu_percent,
                    "status": "healthy" if cpu_percent < self.cpu_threshold else "degraded"
                },
                "memory": {
                    "percent": memory_percent,
                    "total": memory.total,
                    "available": memory.available,
                    "status": "healthy" if memory_percent < self.memory_threshold else "degraded"
                },
                "disk": {
                    "percent": disk_percent,
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "status": "healthy" if disk_percent < self.disk_threshold else "degraded"
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv
                },
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return {"error": str(e), "timestamp": time.time()}


class ComprehensiveHealthMonitor:
    """Comprehensive health monitoring combining all checks."""
    
    def __init__(self):
        self.service_monitor = ServiceHealthMonitor()
        self.resource_monitor = SystemResourceMonitor()
    
    async def get_comprehensive_health(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        # Check all services
        service_health = await self.service_monitor.check_all_services()
        
        # Get system resources
        system_metrics = self.resource_monitor.get_system_metrics()
        
        # Get health summary
        health_summary = self.service_monitor.get_health_summary()
        
        return {
            "overall_status": health_summary["status"],
            "timestamp": time.time(),
            "services": health_summary["services"],
            "system_metrics": system_metrics,
            "alerts": self._generate_alerts(service_health, system_metrics)
        }
    
    def _generate_alerts(self, service_health: List[HealthCheck], system_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate alerts based on health checks."""
        alerts = []
        
        # Service alerts
        for check in service_health:
            if check.status == HealthStatus.UNHEALTHY:
                alerts.append({
                    "type": "service_down",
                    "severity": "critical",
                    "message": f"Service {check.service} is down",
                    "service": check.service,
                    "timestamp": check.timestamp
                })
            elif check.status == HealthStatus.DEGRADED:
                alerts.append({
                    "type": "service_degraded",
                    "severity": "warning",
                    "message": f"Service {check.service} is degraded",
                    "service": check.service,
                    "timestamp": check.timestamp
                })
        
        # System resource alerts
        if "error" not in system_metrics:
            if system_metrics["cpu"]["percent"] > self.resource_monitor.cpu_threshold:
                alerts.append({
                    "type": "high_cpu",
                    "severity": "warning",
                    "message": f"High CPU usage: {system_metrics['cpu']['percent']:.1f}%",
                    "timestamp": time.time()
                })
            
            if system_metrics["memory"]["percent"] > self.resource_monitor.memory_threshold:
                alerts.append({
                    "type": "high_memory",
                    "severity": "warning",
                    "message": f"High memory usage: {system_metrics['memory']['percent']:.1f}%",
                    "timestamp": time.time()
                })
            
            if system_metrics["disk"]["percent"] > self.resource_monitor.disk_threshold:
                alerts.append({
                    "type": "high_disk",
                    "severity": "critical",
                    "message": f"High disk usage: {system_metrics['disk']['percent']:.1f}%",
                    "timestamp": time.time()
                })
        
        return alerts


# Global health monitor instance
health_monitor = ComprehensiveHealthMonitor()
