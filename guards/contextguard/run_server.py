#!/usr/bin/env python3
"""
Shared server startup script for AIGuardian guard services.

This script provides a standardized way to start FastAPI applications
across all guard services with proper configuration and logging.
"""

import os
import uvicorn
import logging
from pathlib import Path

# Configure basic logging for startup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_app_module():
    """
    Determine the FastAPI app module to import based on service structure.

    Returns:
        tuple: (module_path, app_instance_name)
    """
    # Check for common patterns
    current_dir = Path.cwd()

    # Pattern 1: poisonguard.api:app (for shared library services)
    try:
        import poisonguard.api
        if hasattr(poisonguard.api, 'app'):
            return 'poisonguard.api', 'app'
    except ImportError:
        pass

    # Pattern 2: main:app (for standalone services)
    try:
        import main
        if hasattr(main, 'app'):
            return 'main', 'app'
    except ImportError:
        pass

    # Pattern 3: Service-specific imports
    service_name = os.getenv('SERVICE_NAME', current_dir.name)
    module_name = f"{service_name}.api"
    try:
        module = __import__(module_name, fromlist=['app'])
        if hasattr(module, 'app'):
            return module_name, 'app'
    except ImportError:
        pass

    # Fallback: try to find main.py in current directory
    if (current_dir / 'main.py').exists():
        try:
            import main
            if hasattr(main, 'app'):
                return 'main', 'app'
        except ImportError:
            pass

    raise RuntimeError(
        "Could not find FastAPI app. "
        "Expected one of: poisonguard.api:app, main:app, or {service}.api:app"
    )

def main():
    """Main entry point for starting the server."""

    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '8000'))
    reload = os.getenv('RELOAD', 'false').lower() == 'true'
    log_level = os.getenv('LOG_LEVEL', 'info')

    # Get the app module
    try:
        module_path, app_name = get_app_module()
        logger.info(f"Found FastAPI app: {module_path}:{app_name}")
    except RuntimeError as e:
        logger.error(f"Failed to locate FastAPI app: {e}")
        return 1

    # Import the app dynamically
    try:
        module = __import__(module_path, fromlist=[app_name])
        app = getattr(module, app_name)
    except (ImportError, AttributeError) as e:
        logger.error(f"Failed to import app from {module_path}: {e}")
        return 1

    # Log startup information
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Reload mode: {reload}")
    logger.info(f"Log level: {log_level}")

    # Start the server
    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
            access_log=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
