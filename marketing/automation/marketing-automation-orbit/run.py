#!/usr/bin/env python3
"""
Marketing Automation Orbit - Startup Script
Run this to start the automation system.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import MarketingAutomationOrbit
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point."""
    logger.info("🚀 Starting Marketing Automation Orbit...")
    
    orbit = MarketingAutomationOrbit()
    
    if not orbit.initialize():
        logger.error("❌ Failed to initialize Marketing Automation Orbit")
        sys.exit(1)
    
    # Start scheduler
    orbit.start_scheduler()
    
    logger.info("✅ Marketing Automation Orbit running")
    logger.info(f"📊 Status: {orbit.get_status()}")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down...")
        orbit.stop_scheduler()
        logger.info("✅ Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())

