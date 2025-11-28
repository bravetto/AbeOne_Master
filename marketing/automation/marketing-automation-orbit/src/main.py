"""
Marketing Automation Orbit - Main Entry Point
Programmatic marketing automation system.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engine.automation_engine import AutomationEngine
from src.scheduler.execution_scheduler import ExecutionScheduler
from adapters.kernel_adapter import KernelAdapter
from adapters.guardian_adapter import GuardianAdapter
from adapters.module_adapter import ModuleAdapter
from adapters.bus_adapter import BusAdapter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MarketingAutomationOrbit:
    """
    Main Marketing Automation Orbit system.
    
    Orchestrates:
    - Automation engine
    - Execution scheduler
    - AbëONE integrations
    - Channel handlers
    """
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        kernel_registry=None,
        kernel_event_bus=None,
        kernel_state=None,
        kernel_lifecycle=None,
        kernel_boundary=None,
        kernel_validation=None
    ):
        """Initialize Marketing Automation Orbit."""
        self.config_path = config_path or Path(__file__).parent.parent
        
        # Initialize core components
        self.engine = AutomationEngine(config_path=self.config_path / "config")
        self.scheduler = ExecutionScheduler(self.engine)
        
        # Initialize adapters
        self.kernel_adapter = KernelAdapter(
            module_registry=kernel_registry,
            event_bus=kernel_event_bus,
            system_state=kernel_state,
            lifecycle_manager=kernel_lifecycle,
            boundary_enforcer=kernel_boundary,
            validation_gate=kernel_validation
        )
        
        self.guardian_adapter = GuardianAdapter()
        self.module_adapter = ModuleAdapter(config_path=self.config_path / "config")
        self.bus_adapter = BusAdapter(event_bus=kernel_event_bus)
        
        # Initialize status
        self.initialized = False
        self.running = False
    
    def initialize(self) -> bool:
        """
        Initialize the system.
        
        Returns:
            True if initialization successful
        """
        if self.initialized:
            return True
        
        try:
            # Validate dependencies
            deps = self.module_adapter.validate_dependencies()
            if not deps["all_dependencies_met"]:
                logger.warning(f"Missing dependencies: {deps['missing_packages']}")
            
            # Register with kernel
            if not self.kernel_adapter.register():
                logger.warning("Failed to register with kernel, continuing anyway")
            
            # Activate kernel integration
            if not self.kernel_adapter.activate():
                logger.warning("Failed to activate kernel integration, continuing anyway")
            
            # Set up event subscriptions
            self._setup_event_subscriptions()
            
            self.initialized = True
            logger.info("Marketing Automation Orbit initialized")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing system: {e}")
            return False
    
    def _setup_event_subscriptions(self) -> None:
        """Set up event bus subscriptions."""
        # Subscribe to relevant events
        for event_type in self.bus_adapter.MARKETING_EVENTS:
            self.bus_adapter.subscribe(event_type, self._handle_marketing_event)
    
    def _handle_marketing_event(self, event: dict) -> None:
        """Handle marketing event."""
        logger.debug(f"Handling marketing event: {event.get('event_type')}")
        # Process event
        pass
    
    async def execute_strategy_from_file(self, strategy_path: Path) -> dict:
        """
        Load and execute strategy from file.
        
        Args:
            strategy_path: Path to strategy file
            
        Returns:
            Execution result
        """
        if not self.initialized:
            self.initialize()
        
        # Load strategy
        strategy = self.engine.load_strategy(strategy_path)
        
        # Validate with guardians
        validation = self.guardian_adapter.validate_with_guardians({
            "strategy": strategy.to_dict(),
            "action": "execute"
        })
        
        if not validation["valid"]:
            logger.warning(f"Guardian validation failed: {validation}")
        
        # Execute strategy
        result = await self.engine.execute_strategy(strategy.id)
        
        # Publish event
        self.bus_adapter.publish(
            "marketing.strategy.executed",
            {
                "strategy_id": strategy.id,
                "result": result
            }
        )
        
        return result
    
    def start_scheduler(self) -> None:
        """Start execution scheduler."""
        if not self.initialized:
            self.initialize()
        
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        logger.info("Starting execution scheduler")
        
        # Start scheduler in background
        import threading
        scheduler_thread = threading.Thread(target=self.scheduler.start, daemon=True)
        scheduler_thread.start()
    
    def stop_scheduler(self) -> None:
        """Stop execution scheduler."""
        if not self.running:
            return
        
        self.scheduler.stop()
        self.running = False
        logger.info("Execution scheduler stopped")
    
    def get_status(self) -> dict:
        """Get system status."""
        return {
            "initialized": self.initialized,
            "running": self.running,
            "module_info": self.module_adapter.get_module_info(),
            "guardian_status": self.guardian_adapter.get_guardian_status(),
            "kernel_registered": self.kernel_adapter._registered,
            "kernel_active": self.kernel_adapter._active,
            "strategies_loaded": len(self.engine.strategies),
            "campaigns_active": len([c for c in self.engine.campaigns.values() if c.status.value == "active"])
        }


async def main():
    """Main entry point."""
    orbit = MarketingAutomationOrbit()
    
    if not orbit.initialize():
        logger.error("Failed to initialize Marketing Automation Orbit")
        sys.exit(1)
    
    # Start scheduler
    orbit.start_scheduler()
    
    logger.info("Marketing Automation Orbit running")
    logger.info(f"Status: {orbit.get_status()}")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        orbit.stop_scheduler()


if __name__ == "__main__":
    asyncio.run(main())

