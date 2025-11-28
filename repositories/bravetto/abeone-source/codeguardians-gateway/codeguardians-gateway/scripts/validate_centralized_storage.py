#!/usr/bin/env python3
"""
Centralized Storage Validation Script

This script validates that all services are properly configured for centralized storage
and can connect to shared PostgreSQL and Redis instances.
"""

import os
import sys
import asyncio
import logging
from typing import Dict, List, Any
import psycopg2
import redis
import boto3
from botocore.exceptions import ClientError

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import get_settings
from app.core.session_manager import initialize_session_manager
from app.core.session_service import initialize_session_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StorageValidator:
    """Validates centralized storage configuration and connectivity."""
    
    def __init__(self):
        self.settings = get_settings()
        self.results = {
            "postgresql": {"status": "unknown", "details": {}},
            "redis": {"status": "unknown", "details": {}},
            "s3": {"status": "unknown", "details": {}},
            "sessions": {"status": "unknown", "details": {}},
            "contextguard": {"status": "unknown", "details": {}}
        }
    
    async def validate_all(self) -> Dict[str, Any]:
        """Validate all storage components."""
        logger.info("Starting centralized storage validation...")
        
        # Validate PostgreSQL
        await self.validate_postgresql()
        
        # Validate Redis
        await self.validate_redis()
        
        # Validate S3
        await self.validate_s3()
        
        # Validate Session Management
        await self.validate_sessions()
        
        # Validate ContextGuard
        await self.validate_contextguard()
        
        return self.results
    
    async def validate_postgresql(self):
        """Validate PostgreSQL connectivity and configuration."""
        logger.info("Validating PostgreSQL...")
        
        try:
            # Parse database URL
            db_url = self.settings.DATABASE_URL
            if not db_url.startswith("postgresql"):
                raise ValueError("Invalid database URL format")
            
            # Extract connection parameters
            import urllib.parse
            parsed = urllib.parse.urlparse(db_url)
            
            # Test connection
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                database=parsed.path[1:],  # Remove leading slash
                user=parsed.username,
                REPLACE_ME
            )
            
            # Test query
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            # Check if required tables exist
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('users', 'sessions', 'organizations')
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            self.results["postgresql"] = {
                "status": "healthy",
                "details": {
                    "version": version,
                    "host": parsed.hostname,
                    "port": parsed.port or 5432,
                    "database": parsed.path[1:],
                    "tables_found": tables,
                    "connection_test": "passed"
                }
            }
            
            logger.info(" PostgreSQL validation passed")
            
        except Exception as e:
            self.results["postgresql"] = {
                "status": "unhealthy",
                "details": {
                    "error": str(e),
                    "connection_test": "failed"
                }
            }
            logger.error(f" PostgreSQL validation failed: {e}")
    
    async def validate_redis(self):
        """Validate Redis connectivity and configuration."""
        logger.info("Validating Redis...")
        
        try:
            # Test Redis connection
            redis_client = redis.Redis(
                host=self.settings.REDIS_HOST,
                port=self.settings.REDIS_PORT,
                db=self.settings.REDIS_DB,
                decode_responses=True
            )
            
            # Test basic operations
            test_key = "validation_test"
            test_value = "test_value"
            
            # Set and get
            redis_client.set(test_key, test_value, ex=60)
            retrieved_value = redis_client.get(test_key)
            
            # Test ping
            ping_result = redis_client.ping()
            
            # Get Redis info
            info = redis_client.info()
            
            # Cleanup
            redis_client.delete(test_key)
            
            self.results["redis"] = {
                "status": "healthy",
                "details": {
                    "host": self.settings.REDIS_HOST,
                    "port": self.settings.REDIS_PORT,
                    "db": self.settings.REDIS_DB,
                    "ping": ping_result,
                    "set_get_test": retrieved_value == test_value,
                    "version": info.get("redis_version"),
                    "memory_usage": info.get("used_memory_human"),
                    "connected_clients": info.get("connected_clients")
                }
            }
            
            logger.info(" Redis validation passed")
            
        except Exception as e:
            self.results["redis"] = {
                "status": "unhealthy",
                "details": {
                    "error": str(e),
                    "host": self.settings.REDIS_HOST,
                    "port": self.settings.REDIS_PORT,
                    "db": self.settings.REDIS_DB
                }
            }
            logger.error(f" Redis validation failed: {e}")
    
    async def validate_s3(self):
        """Validate S3 connectivity and configuration."""
        logger.info("Validating S3...")
        
        if not self.settings.S3_ENABLED:
            self.results["s3"] = {
                "status": "disabled",
                "details": {"message": "S3 is disabled in configuration"}
            }
            logger.info("ℹ S3 is disabled")
            return
        
        try:
            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                region_name=self.settings.S3_REGION,
                aws_access_key_id=self.settings.S3_ACCESS_KEY_ID,
                aws_secret_access_key=self.settings.S3_SECRET_ACCESS_KEY,
                aws_session_token=self.settings.S3_SESSION_TOKEN,
                endpoint_url=self.settings.S3_ENDPOINT_URL if self.settings.S3_ENDPOINT_URL else None
            )
            
            # Test bucket access
            try:
                response = s3_client.head_bucket(Bucket=self.settings.S3_BUCKET_NAME)
                bucket_exists = True
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    bucket_exists = False
                else:
                    raise
            
            # Test list objects (with limit to avoid large responses)
            try:
                response = s3_client.list_objects_v2(
                    Bucket=self.settings.S3_BUCKET_NAME,
                    MaxKeys=1
                )
                list_test = True
                object_count = response.get('KeyCount', 0)
            except ClientError:
                list_test = False
                object_count = 0
            
            # Test presigned URL generation
            try:
                presigned_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.settings.S3_BUCKET_NAME, 'Key': 'test'},
                    ExpiresIn=60
                )
                presigned_test = True
            except ClientError:
                presigned_test = False
                presigned_url = None
            
            self.results["s3"] = {
                "status": "healthy",
                "details": {
                    "bucket_name": self.settings.S3_BUCKET_NAME,
                    "region": self.settings.S3_REGION,
                    "bucket_exists": bucket_exists,
                    "list_objects_test": list_test,
                    "object_count": object_count,
                    "presigned_url_test": presigned_test,
                    "endpoint_url": self.settings.S3_ENDPOINT_URL
                }
            }
            
            logger.info(" S3 validation passed")
            
        except Exception as e:
            self.results["s3"] = {
                "status": "unhealthy",
                "details": {
                    "error": str(e),
                    "bucket_name": self.settings.S3_BUCKET_NAME,
                    "region": self.settings.S3_REGION
                }
            }
            logger.error(f" S3 validation failed: {e}")
    
    async def validate_sessions(self):
        """Validate session management configuration."""
        logger.info("Validating Session Management...")
        
        try:
            # Initialize session service
            session_service = initialize_session_service(use_redis=True)
            
            # Test session creation
            test_user_id = 999999  # Use a test user ID
            session_id = session_service.create_session(
                user_id=test_user_id,
                session_data={"test": "data"},
                ttl=60
            )
            
            # Test session retrieval
            session_data = session_service.get_session(session_id)
            
            # Test session update
            update_success = session_service.update_session_data(
                session_id, 
                {"updated": "data"}
            )
            
            # Test session deletion
            delete_success = session_service.delete_session(session_id)
            
            # Test health check
            health_check = session_service.health_check()
            
            # Get session stats
            stats = session_service.get_session_stats()
            
            self.results["sessions"] = {
                "status": "healthy",
                "details": {
                    "storage_type": "redis" if session_service.use_redis else "database",
                    "session_creation": bool(session_id),
                    "session_retrieval": session_data is not None,
                    "session_update": update_success,
                    "session_deletion": delete_success,
                    "health_check": health_check,
                    "stats": stats
                }
            }
            
            logger.info(" Session Management validation passed")
            
        except Exception as e:
            self.results["sessions"] = {
                "status": "unhealthy",
                "details": {
                    "error": str(e),
                    "storage_type": "unknown"
                }
            }
            logger.error(f" Session Management validation failed: {e}")
    
    async def validate_contextguard(self):
        """Validate ContextGuard Redis integration."""
        logger.info("Validating ContextGuard...")
        
        try:
            # Set environment variables for ContextGuard
            os.environ["CONTEXTGUARD_USE_REDIS"] = "true"
            os.environ["CONTEXTGUARD_REDIS_URL"] = f"redis://{self.settings.REDIS_HOST}:{self.settings.REDIS_PORT}/{self.settings.REDIS_DB}"
            
            # Import ContextGuard
            from guards.contextguard.src.contextguard.guard import ContextGuard
            
            # Initialize ContextGuard
            guard = ContextGuard()
            
            # Test memory operations
            test_key = "validation_test"
            test_value = {"test": "data", "timestamp": "2023-01-01T00:00:00Z"}
            
            # Add to memory
            guard.add_to_memory(test_key, test_value)
            
            # Get from memory
            retrieved_value = guard.get_from_memory(test_key)
            
            # Test memory snapshot
            snapshot = guard.memory_snapshot()
            
            # Test context window
            context_window = guard.get_context_window(max_items=10)
            
            # Test Redis health if available
            redis_health = False
            if guard.use_redis and guard.redis_storage:
                redis_health = guard.redis_storage.health_check()
            
            # Cleanup
            guard.clear_memory()
            
            self.results["contextguard"] = {
                "status": "healthy",
                "details": {
                    "redis_enabled": guard.use_redis,
                    "redis_health": redis_health,
                    "memory_add": retrieved_value == test_value,
                    "memory_snapshot": len(snapshot) > 0,
                    "context_window": len(context_window) > 0,
                    "storage_type": "redis" if guard.use_redis else "in-memory"
                }
            }
            
            logger.info(" ContextGuard validation passed")
            
        except Exception as e:
            self.results["contextguard"] = {
                "status": "unhealthy",
                "details": {
                    "error": str(e),
                    "redis_enabled": False
                }
            }
            logger.error(f" ContextGuard validation failed: {e}")
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "="*60)
        print("CENTRALIZED STORAGE VALIDATION SUMMARY")
        print("="*60)
        
        for component, result in self.results.items():
            status = result["status"]
            details = result["details"]
            
            if status == "healthy":
                print(f" {component.upper()}: {status}")
            elif status == "disabled":
                print(f"ℹ  {component.upper()}: {status}")
            else:
                print(f" {component.upper()}: {status}")
            
            # Print key details
            if "error" in details:
                print(f"   Error: {details['error']}")
            elif status == "healthy":
                if component == "postgresql":
                    print(f"   Version: {details.get('version', 'Unknown')}")
                    print(f"   Tables: {len(details.get('tables_found', []))}")
                elif component == "redis":
                    print(f"   Version: {details.get('version', 'Unknown')}")
                    print(f"   Memory: {details.get('memory_usage', 'Unknown')}")
                elif component == "s3":
                    print(f"   Bucket: {details.get('bucket_name', 'Unknown')}")
                    print(f"   Objects: {details.get('object_count', 0)}")
                elif component == "sessions":
                    print(f"   Storage: {details.get('storage_type', 'Unknown')}")
                    print(f"   Health: {details.get('health_check', False)}")
                elif component == "contextguard":
                    print(f"   Redis: {details.get('redis_enabled', False)}")
                    print(f"   Storage: {details.get('storage_type', 'Unknown')}")
            
            print()
        
        # Overall status
        healthy_count = sum(1 for r in self.results.values() if r["status"] == "healthy")
        total_count = len(self.results)
        
        print(f"Overall Status: {healthy_count}/{total_count} components healthy")
        
        if healthy_count == total_count:
            print(" All components are properly configured for centralized storage!")
        else:
            print("  Some components need attention. Check the details above.")


async def main():
    """Main validation function."""
    validator = StorageValidator()
    await validator.validate_all()
    validator.print_summary()
    
    # Return exit code based on results
    unhealthy_count = sum(1 for r in validator.results.values() if r["status"] == "unhealthy")
    return 0 if unhealthy_count == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
