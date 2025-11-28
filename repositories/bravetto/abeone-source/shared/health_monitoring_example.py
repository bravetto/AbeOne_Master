"""
Example usage of the Unified Health Monitoring Library

This shows how to integrate the unified health monitoring into any AI Guardian service.
"""

from shared.health_monitoring import create_health_monitor, HealthStatus
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Example of using the unified health monitoring library."""
    
    # Create health monitor for a service
    health_monitor = create_health_monitor("example-service", "1.0.0")
    
    # Add service dependencies
    health_monitor.add_dependency("database", "REPLACE_MElocalhost:5432/db")
    health_monitor.add_dependency("redis", "redis://localhost:6379/0")
    health_monitor.add_dependency("api-gateway", "http://localhost:8000/health")
    
    # Check individual health probes
    print("=== Liveness Probe ===")
    liveness = health_monitor.get_liveness_probe()
    print(f"Status: {liveness['status']}")
    print(f"Uptime: {liveness['uptime_seconds']:.2f} seconds")
    
    print("\n=== Readiness Probe ===")
    readiness = health_monitor.get_readiness_probe()
    print(f"Status: {readiness['status']}")
    print(f"System Health: {readiness['checks']['system']}")
    
    print("\n=== System Metrics ===")
    metrics = health_monitor.get_system_metrics()
    print(f"CPU: {metrics.cpu_percent:.1f}%")
    print(f"Memory: {metrics.memory_percent:.1f}%")
    print(f"Uptime: {metrics.uptime_seconds:.2f} seconds")
    
    print("\n=== Dependency Health ===")
    dependencies = await health_monitor.check_all_dependencies()
    for dep in dependencies:
        print(f"{dep.service}: {dep.status.value} ({dep.response_time:.3f}s)")
        if dep.error:
            print(f"  Error: {dep.error}")
    
    print("\n=== Comprehensive Health ===")
    comprehensive = await health_monitor.get_comprehensive_health()
    print(f"Overall Status: {comprehensive['overall_status']}")
    print(f"System CPU: {comprehensive['system_metrics']['cpu_percent']:.1f}%")
    print(f"System Memory: {comprehensive['system_metrics']['memory_percent']:.1f}%")
    
    if comprehensive['alerts']:
        print("\n=== Alerts ===")
        for alert in comprehensive['alerts']:
            print(f"{alert['severity'].upper()}: {alert['message']}")
    
    print("\n=== Prometheus Metrics ===")
    prometheus_metrics = health_monitor.get_prometheus_metrics()
    print("Available metrics:")
    for line in prometheus_metrics.split('\n'):
        if line.startswith('# HELP'):
            print(f"  {line}")


if __name__ == "__main__":
    asyncio.run(main())
