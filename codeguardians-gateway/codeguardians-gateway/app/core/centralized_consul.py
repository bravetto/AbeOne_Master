"""
Centralized Configuration Management with Consul
Dynamic configuration updates for all AIGuardian services
"""

import json
import os
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

import consul.aio


class CentralizedConsul:
    """Centralized Consul configuration management."""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.consul_client = None
        self.watch_tasks = []
        
    async def initialize(self):
        """Initialize the Consul client."""
        try:
            # Create Consul client
            self.consul_client = consul.aio.Consul(
                host=self.config.CONSUL_HOST,
                port=self.config.CONSUL_PORT
            )
            
            # Test connection
            await self.consul_client.agent.self()
            self.logger.info("Centralized Consul initialized successfully")
            
            # Register this service
            await self._register_service()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize centralized Consul: {e}")
            raise
    
    async def _register_service(self):
        """Register this service with Consul."""
        try:
            service_id = f"aiguardian-gateway-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            await self.consul_client.agent.service.register(
                name="aiguardian-gateway",
                service_id=service_id,
                address=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", os.getenv("GATEWAY_PORT", "8000"))),
                check={
                    "HTTP": f"http://{'localhost' if os.getenv('HOST', 'localhost') == '0.0.0.0' else os.getenv('HOST', 'localhost')}:{os.getenv('PORT', os.getenv('GATEWAY_PORT', '8000'))}/health",
                    "Interval": "30s",
                    "Timeout": "10s"
                }
            )
            
            self.logger.info(f"Service registered with Consul: {service_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to register service with Consul: {e}")
    
    async def set_config(self, key: str, value: Any, service: str = "aiguardian"):
        """Set a configuration value in Consul."""
        try:
            full_key = f"{service}/config/{key}"
            await self.consul_client.kv.put(
                full_key,
                json.dumps(value, default=str)
            )
            self.logger.info(f"Configuration set: {full_key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to set configuration: {e}")
            return False
    
    async def get_config(self, key: str, service: str = "aiguardian", default: Any = None) -> Any:
        """Get a configuration value from Consul."""
        try:
            full_key = f"{service}/config/{key}"
            _, data = await self.consul_client.kv.get(full_key)
            
            if data and data['Value']:
                return json.loads(data['Value'].decode('utf-8'))
            return default
        except Exception as e:
            self.logger.error(f"Failed to get configuration: {e}")
            return default
    
    async def get_all_configs(self, service: str = "aiguardian") -> Dict[str, Any]:
        """Get all configuration values for a service."""
        try:
            prefix = f"{service}/config/"
            _, data = await self.consul_client.kv.get(prefix, recurse=True)
            
            configs = {}
            if data:
                for item in data:
                    key = item['Key'].replace(prefix, '')
                    configs[key] = json.loads(item['Value'].decode('utf-8'))
            
            return configs
        except Exception as e:
            self.logger.error(f"Failed to get all configurations: {e}")
            return {}
    
    async def delete_config(self, key: str, service: str = "aiguardian"):
        """Delete a configuration value from Consul."""
        try:
            full_key = f"{service}/config/{key}"
            await self.consul_client.kv.delete(full_key)
            self.logger.info(f"Configuration deleted: {full_key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete configuration: {e}")
            return False
    
    async def watch_config(self, key: str, callback, service: str = "aiguardian"):
        """Watch a configuration key for changes."""
        try:
            full_key = f"{service}/config/{key}"
            
            async def watch_loop():
                index = None
                while True:
                    try:
                        _, data = await self.consul_client.kv.get(
                            full_key,
                            index=index,
                            wait="30s"
                        )
                        
                        if data:
                            new_value = json.loads(data['Value'].decode('utf-8'))
                            await callback(key, new_value)
                            index = data['ModifyIndex']
                        else:
                            await callback(key, None)
                            
                    except Exception as e:
                        self.logger.error(f"Error watching configuration: {e}")
                        await asyncio.sleep(5)
            
            # Start watching in background
            task = asyncio.create_task(watch_loop())
            self.watch_tasks.append(task)
            
            self.logger.info(f"Started watching configuration: {full_key}")
            return task
            
        except Exception as e:
            self.logger.error(f"Failed to watch configuration: {e}")
            return None
    
    async def set_guard_config(self, guard_name: str, config_data: Dict[str, Any]):
        """Set configuration for a specific guard service."""
        try:
            for key, value in config_data.items():
                await self.set_config(f"guards/{guard_name}/{key}", value)
            
            self.logger.info(f"Guard configuration set: {guard_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to set guard configuration: {e}")
            return False
    
    async def get_guard_config(self, guard_name: str) -> Dict[str, Any]:
        """Get configuration for a specific guard service."""
        try:
            prefix = f"aiguardian/config/guards/{guard_name}/"
            _, data = await self.consul_client.kv.get(prefix, recurse=True)
            
            config = {}
            if data:
                for item in data:
                    key = item['Key'].replace(prefix, '')
                    config[key] = json.loads(item['Value'].decode('utf-8'))
            
            return config
        except Exception as e:
            self.logger.error(f"Failed to get guard configuration: {e}")
            return {}
    
    async def set_feature_flag(self, feature: str, enabled: bool, service: str = "aiguardian"):
        """Set a feature flag."""
        try:
            await self.set_config(f"features/{feature}", enabled, service)
            self.logger.info(f"Feature flag set: {feature} = {enabled}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to set feature flag: {e}")
            return False
    
    async def get_feature_flag(self, feature: str, service: str = "aiguardian", default: bool = False) -> bool:
        """Get a feature flag value."""
        try:
            return await self.get_config(f"features/{feature}", service, default)
        except Exception as e:
            self.logger.error(f"Failed to get feature flag: {e}")
            return default
    
    async def get_services(self) -> List[Dict[str, Any]]:
        """Get all registered services."""
        try:
            _, services = await self.consul_client.agent.services()
            return list(services.values())
        except Exception as e:
            self.logger.error(f"Failed to get services: {e}")
            return []
    
    async def get_service_health(self, service_name: str) -> List[Dict[str, Any]]:
        """Get health status for a service."""
        try:
            _, checks = await self.consul_client.health.service(service_name)
            return checks
        except Exception as e:
            self.logger.error(f"Failed to get service health: {e}")
            return []
    
    async def set_lock(self, key: str, value: str, ttl: int = 30) -> bool:
        """Set a distributed lock."""
        try:
            full_key = f"locks/{key}"
            success = await self.consul_client.kv.put(
                full_key,
                value,
                acquire=value,
                ttl=f"{ttl}s"
            )
            return success
        except Exception as e:
            self.logger.error(f"Failed to set lock: {e}")
            return False
    
    async def release_lock(self, key: str, value: str) -> bool:
        """Release a distributed lock."""
        try:
            full_key = f"locks/{key}"
            success = await self.consul_client.kv.put(
                full_key,
                value,
                release=value
            )
            return success
        except Exception as e:
            self.logger.error(f"Failed to release lock: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform Consul health check."""
        try:
            # Test connection
            leader = await self.consul_client.status.leader()
            peers = await self.consul_client.status.peers()
            
            return {
                'status': 'healthy',
                'consul_url': self.config.get_consul_url(),
                'leader': leader,
                'peers': len(peers),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def cleanup(self):
        """Cleanup Consul resources."""
        # Cancel all watch tasks
        for task in self.watch_tasks:
            if not task.done():
                task.cancel()
        
        # Close Consul client
        if self.consul_client:
            await self.consul_client.close()


