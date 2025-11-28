#!/usr/bin/env python3
"""
Docker Networking Diagnostic Script for CodeGuardians Gateway

This script helps diagnose Docker networking issues by testing:
1. Database connectivity from within containers
2. Service discovery between containers
3. Network configuration validation
4. Environment variable validation

Usage:
    python diagnose_docker_networking.py [--verbose]
"""

import asyncio
import os
import sys
import time
import subprocess
import json
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import asyncpg
import redis
import httpx
from datetime import datetime


class DockerNetworkingDiagnostic:
    """Comprehensive Docker networking diagnostic tool."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": {},
            "network_tests": {},
            "connectivity_tests": {},
            "recommendations": []
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def log_verbose(self, message: str):
        """Log verbose message if verbose mode is enabled."""
        if self.verbose:
            self.log(f"VERBOSE: {message}", "DEBUG")
    
    async def check_environment_variables(self) -> Dict[str, any]:
        """Check and validate environment variables."""
        self.log("Checking environment variables...")
        
        env_vars = {
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "REDIS_URL": os.getenv("REDIS_URL"),
            "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "REDIS_PASSWORD": os.getenv("REDIS_PASSWORD"),
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
            "DEBUG": os.getenv("DEBUG", "false")
        }
        
        issues = []
        
        # Check DATABASE_URL
        if not env_vars["DATABASE_URL"]:
            issues.append("DATABASE_URL is not set")
        else:
            parsed_url = urlparse(env_vars["DATABASE_URL"])
            if not parsed_url.hostname:
                issues.append("DATABASE_URL missing hostname")
            elif parsed_url.hostname not in ["postgres", "localhost", "host.docker.internal"]:
                issues.append(f"DATABASE_URL hostname '{parsed_url.hostname}' may not be accessible from container")
        
        # Check REDIS_URL
        if not env_vars["REDIS_URL"]:
            issues.append("REDIS_URL is not set")
        else:
            parsed_redis = urlparse(env_vars["REDIS_URL"])
            if not parsed_redis.hostname:
                issues.append("REDIS_URL missing hostname")
            elif parsed_redis.hostname not in ["redis", "localhost", "host.docker.internal"]:
                issues.append(f"REDIS_URL hostname '{parsed_redis.hostname}' may not be accessible from container")
        
        self.results["environment"] = {
            "variables": env_vars,
            "issues": issues,
            "status": "PASS" if not issues else "FAIL"
        }
        
        if issues:
            self.log(f"Environment issues found: {', '.join(issues)}", "WARNING")
        else:
            self.log("Environment variables look good")
        
        return self.results["environment"]
    
    async def test_database_connectivity(self) -> Dict[str, any]:
        """Test database connectivity."""
        self.log("Testing database connectivity...")
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return {
                "status": "SKIP",
                "error": "DATABASE_URL not set"
            }
        
        try:
            # Parse the database URL
            parsed_url = urlparse(database_url)
            
            # Convert to asyncpg format
            if "+asyncpg" in database_url:
                # Remove the +asyncpg part for asyncpg connection
                asyncpg_url = database_url.replace("+asyncpg", "")
            else:
                asyncpg_url = database_url
            
            self.log_verbose(f"Attempting connection to: {parsed_url.hostname}:{parsed_url.port}")
            
            # Test connection
            start_time = time.time()
            conn = await asyncpg.connect(asyncpg_url)
            response_time = time.time() - start_time
            
            # Test query
            result = await conn.fetchval("SELECT 1")
            await conn.close()
            
            self.log(f"Database connection successful (response time: {response_time:.3f}s)")
            
            return {
                "status": "PASS",
                "hostname": parsed_url.hostname,
                "port": parsed_url.port,
                "database": parsed_url.path[1:],  # Remove leading slash
                "response_time": response_time,
                "test_query_result": result
            }
            
        except Exception as e:
            self.log(f"Database connection failed: {str(e)}", "ERROR")
            return {
                "status": "FAIL",
                "error": str(e),
                "hostname": parsed_url.hostname if 'parsed_url' in locals() else "unknown",
                "port": parsed_url.port if 'parsed_url' in locals() else "unknown"
            }
    
    async def test_redis_connectivity(self) -> Dict[str, any]:
        """Test Redis connectivity."""
        self.log("Testing Redis connectivity...")
        
        redis_url = os.getenv("REDIS_URL")
        if not redis_url:
            return {
                "status": "SKIP",
                "error": "REDIS_URL not set"
            }
        
        try:
            # Parse Redis URL
            parsed_url = urlparse(redis_url)
            
            self.log_verbose(f"Attempting Redis connection to: {parsed_url.hostname}:{parsed_url.port}")
            
            # Test connection
            start_time = time.time()
            r = redis.from_url(redis_url)
            r.ping()  # Test connection
            response_time = time.time() - start_time
            
            # Test set/get
            test_key = f"diagnostic_test_{int(time.time())}"
            r.set(test_key, "test_value", ex=60)  # Expire in 60 seconds
            result = r.get(test_key)
            r.delete(test_key)
            
            self.log(f"Redis connection successful (response time: {response_time:.3f}s)")
            
            return {
                "status": "PASS",
                "hostname": parsed_url.hostname,
                "port": parsed_url.port,
                "response_time": response_time,
                "test_operation": "PASS" if result == b"test_value" else "FAIL"
            }
            
        except Exception as e:
            self.log(f"Redis connection failed: {str(e)}", "ERROR")
            return {
                "status": "FAIL",
                "error": str(e),
                "hostname": parsed_url.hostname if 'parsed_url' in locals() else "unknown",
                "port": parsed_url.port if 'parsed_url' in locals() else "unknown"
            }
    
    async def test_service_discovery(self) -> Dict[str, any]:
        """Test service discovery between containers."""
        self.log("Testing service discovery...")
        
        services_to_test = [
            ("postgres", 5432),
            ("redis", 6379),
            ("codeguardians-gateway", 8000)
        ]
        
        results = {}
        
        for service_name, port in services_to_test:
            try:
                self.log_verbose(f"Testing connectivity to {service_name}:{port}")
                
                # Use httpx for HTTP services, or basic socket test for others
                if port == 8000:  # Gateway service
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        start_time = time.time()
                        response = await client.get(f"http://{service_name}:{port}/health/live")
                        response_time = time.time() - start_time
                        
                        results[service_name] = {
                            "status": "PASS" if response.status_code == 200 else "FAIL",
                            "response_time": response_time,
                            "status_code": response.status_code
                        }
                else:
                    # For non-HTTP services, we'll use a simple approach
                    # In a real implementation, you might use socket testing
                    results[service_name] = {
                        "status": "SKIP",
                        "note": "Non-HTTP service - use database/redis specific tests"
                    }
                    
            except Exception as e:
                self.log(f"Service discovery test failed for {service_name}: {str(e)}", "WARNING")
                results[service_name] = {
                    "status": "FAIL",
                    "error": str(e)
                }
        
        return results
    
    async def check_docker_network(self) -> Dict[str, any]:
        """Check Docker network configuration."""
        self.log("Checking Docker network configuration...")
        
        try:
            # Get current container info
            container_id = os.getenv("HOSTNAME", "unknown")
            self.log_verbose(f"Running in container: {container_id}")
            
            # Check if we're in Docker
            is_docker = os.path.exists("/.dockerenv")
            
            # Get network info
            network_info = {}
            if is_docker:
                try:
                    # Try to get network info from /proc/net/route
                    with open("/proc/net/route", "r") as f:
                        routes = f.readlines()
                    network_info["routes"] = len(routes)
                except:
                    network_info["routes"] = "unavailable"
            
            return {
                "is_docker": is_docker,
                "container_id": container_id,
                "network_info": network_info
            }
            
        except Exception as e:
            return {
                "error": str(e)
            }
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        # Check environment issues
        env_issues = self.results.get("environment", {}).get("issues", [])
        if env_issues:
            recommendations.extend([
                "Fix environment variable issues:",
                *[f"  - {issue}" for issue in env_issues]
            ])
        
        # Check database connectivity
        db_test = self.results.get("connectivity_tests", {}).get("database", {})
        if db_test.get("status") == "FAIL":
            error = db_test.get("error", "Unknown error")
            if "connection refused" in error.lower():
                recommendations.append("Database connection refused - check if PostgreSQL container is running")
            elif "hostname" in error.lower():
                recommendations.append("Database hostname resolution failed - check service name in docker-compose.yml")
            elif "authentication" in error.lower():
                recommendations.append("Database authentication failed - check credentials in environment")
        
        # Check Redis connectivity
        redis_test = self.results.get("connectivity_tests", {}).get("redis", {})
        if redis_test.get("status") == "FAIL":
            error = redis_test.get("error", "Unknown error")
            if "connection refused" in error.lower():
                recommendations.append("Redis connection refused - check if Redis container is running")
            elif "hostname" in error.lower():
                recommendations.append("Redis hostname resolution failed - check service name in docker-compose.yml")
        
        # General recommendations
        if not recommendations:
            recommendations.append("All connectivity tests passed! Your Docker networking is configured correctly.")
        else:
            recommendations.insert(0, "Docker networking issues detected. Recommended fixes:")
        
        return recommendations
    
    async def run_full_diagnostic(self) -> Dict[str, any]:
        """Run complete diagnostic suite."""
        self.log("Starting Docker networking diagnostic...")
        self.log("=" * 60)
        
        # Environment check
        self.results["environment"] = await self.check_environment_variables()
        
        # Connectivity tests
        self.results["connectivity_tests"] = {
            "database": await self.test_database_connectivity(),
            "redis": await self.test_redis_connectivity()
        }
        
        # Network tests
        self.results["network_tests"] = {
            "service_discovery": await self.test_service_discovery(),
            "docker_network": await self.check_docker_network()
        }
        
        # Generate recommendations
        self.results["recommendations"] = self.generate_recommendations()
        
        # Print summary
        self.log("=" * 60)
        self.log("DIAGNOSTIC SUMMARY")
        self.log("=" * 60)
        
        # Environment status
        env_status = self.results["environment"]["status"]
        self.log(f"Environment Variables: {env_status}")
        
        # Database status
        db_status = self.results["connectivity_tests"]["database"]["status"]
        self.log(f"Database Connectivity: {db_status}")
        
        # Redis status
        redis_status = self.results["connectivity_tests"]["redis"]["status"]
        self.log(f"Redis Connectivity: {redis_status}")
        
        # Recommendations
        self.log("\nRECOMMENDATIONS:")
        for rec in self.results["recommendations"]:
            self.log(f"  {rec}")
        
        return self.results


async def main():
    """Main diagnostic function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Docker Networking Diagnostic Tool")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--output", "-o", help="Output file for JSON results")
    args = parser.parse_args()
    
    diagnostic = DockerNetworkingDiagnostic(verbose=args.verbose)
    
    try:
        results = await diagnostic.run_full_diagnostic()
        
        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            diagnostic.log(f"Results saved to {args.output}")
        
        # Exit with appropriate code
        has_failures = any(
            test.get("status") == "FAIL" 
            for test in results.get("connectivity_tests", {}).values()
        )
        
        sys.exit(1 if has_failures else 0)
        
    except KeyboardInterrupt:
        diagnostic.log("Diagnostic interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        diagnostic.log(f"Diagnostic failed: {str(e)}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
