#!/usr/bin/env python3
"""
AEYON Command Line Interface
AEYON PRIME DIRECTIVE: Execute atomic operations

Pattern: AEYON × ATOMIC × EXECUTION × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import argparse
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

# Add EMERGENT_OS to path
sys.path.insert(0, str(Path(__file__).parent.parent / "EMERGENT_OS"))
sys.path.insert(0, str(Path(__file__).parent.parent / "PRODUCTS" / "abebeats"))

from integration_layer.unified_organism import (
    get_unified_organism,
    initialize_unified_organism
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def prime_organism() -> bool:
    """
    Prime (initialize) the Unified Organism.
    
    Pattern: AEYON × PRIME × ORGANISM × ONE
    
    Returns:
        True if successful
    """
    logger.info("=" * 80)
    logger.info(" AEYON PRIME DIRECTIVE: Priming Unified Organism ")
    logger.info("=" * 80)
    logger.info("")
    
    try:
        # Initialize Unified Organism
        logger.info(" Initializing Unified Organism...")
        init_success = initialize_unified_organism()
        
        if not init_success:
            logger.error(" Failed to initialize Unified Organism")
            return False
        
        # Get the organism instance
        organism = get_unified_organism()
        if not organism:
            logger.error(" Failed to get Unified Organism instance")
            return False
        
        logger.info(" Unified Organism initialized")
        logger.info("")
        
        # Get organism state
        logger.info(" Organism State:")
        logger.info(f"   Initialized: {organism._initialized}")
        logger.info(f"   Active: {organism._active}")
        logger.info(f"   Modules: {len(organism.registry.list_modules()) if organism.registry else 0}")
        logger.info(f"   Health Score: {organism.state.health_score:.2f}")
        logger.info(f"   System Load: {organism.state.current_load:.2f}")
        logger.info("")
        
        logger.info("=" * 80)
        logger.info(" Unified Organism PRIMED ")
        logger.info("=" * 80)
        logger.info("")
        logger.info("∞ AbëONE ∞")
        
        return True
        
    except Exception as e:
        logger.error(f" Error priming organism: {e}", exc_info=True)
        return False


def generate_beats() -> bool:
    """
    Generate Guardian beats through AbëBEATs.
    
    Pattern: AEYON × GENERATE × BEATS × ONE
    
    Returns:
        True if successful
    """
    logger.info("=" * 80)
    logger.info(" AEYON: Generating Guardian Beats ")
    logger.info("=" * 80)
    logger.info("")
    
    try:
        # Ensure organism is initialized
        if not initialize_unified_organism():
            logger.error(" Failed to initialize Unified Organism")
            return False
        
        organism = get_unified_organism()
        
        # Import AbëBEATs module
        from abebeats.module import get_abebeats_module
        
        # Get AbëBEATs module
        abebeats_module = get_abebeats_module(
            module_registry=organism.registry,
            event_bus=organism.event_bus,
            system_state=organism.state
        )
        
        if not abebeats_module:
            logger.error(" Failed to get AbëBEATs Module")
            return False
        
        # Ensure module is active
        if not abebeats_module._active:
            abebeats_module.register()
            abebeats_module.initialize()
            abebeats_module.activate()
        
        # Process Guardian beats
        logger.info(" Processing Guardian Beats...")
        results = abebeats_module.process_guardian_beats()
        
        if results:
            logger.info("")
            logger.info("=" * 80)
            logger.info(" Guardian Beats Generated ")
            logger.info("=" * 80)
            logger.info(f" Total Beats: {results.get('total_beats', 0)}")
            logger.info(f" Guardian Beats: {results.get('guardian_beats', {}).get('total', 0)}")
            logger.info(f" Swarm Beats: {results.get('swarm_beats', {}).get('total', 0)}")
            logger.info("")
            logger.info("∞ AbëONE ∞")
            return True
        else:
            logger.error(" Failed to generate Guardian beats")
            return False
            
    except Exception as e:
        logger.error(f" Error generating beats: {e}", exc_info=True)
        return False


def show_status() -> bool:
    """
    Show complete system status.
    
    Pattern: AEYON × STATUS × ONE
    
    Returns:
        True if successful
    """
    logger.info("=" * 80)
    logger.info(" AEYON: System Status ")
    logger.info("=" * 80)
    logger.info("")
    
    try:
        organism = get_unified_organism()
        
        logger.info(" Unified Organism:")
        logger.info(f"   Initialized: {organism._initialized}")
        logger.info(f"   Active: {organism._active}")
        logger.info(f"   Modules: {len(organism.registry.list_modules()) if organism.registry else 0}")
        logger.info(f"   Health Score: {organism.state.health_score:.2f}")
        logger.info(f"   System Load: {organism.state.current_load:.2f}")
        logger.info("")
        
        # Try to get Guardian status
        try:
            from triadic_execution_harness import (
                get_aeyon_binding,
                get_johhn_binding,
                get_meta_binding,
                get_you_binding
            )
            
            guardians = {
                "AEYON": get_aeyon_binding() is not None,
                "JØHN": get_johhn_binding() is not None,
                "META": get_meta_binding() is not None,
                "YOU": get_you_binding() is not None,
            }
            
            logger.info(" Guardians:")
            for name, bound in guardians.items():
                status = "" if bound else ""
                logger.info(f"   {status} {name}: {'Bound' if bound else 'Not Bound'}")
            logger.info("")
            
        except Exception as e:
            logger.debug(f"Could not check Guardian status: {e}")
        
        logger.info("=" * 80)
        logger.info(" Status Complete ")
        logger.info("=" * 80)
        logger.info("")
        logger.info("∞ AbëONE ∞")
        
        return True
        
    except Exception as e:
        logger.error(f" Error getting status: {e}", exc_info=True)
        return False


def execute_capabilities() -> bool:
    """
    Execute all 5 capabilities simultaneously.
    
    Pattern: AEYON × CAPABILITIES × ONE
    
    Returns:
        True if successful
    """
    logger.info("=" * 80)
    logger.info(" AEYON: Executing All 5 Capabilities ")
    logger.info("=" * 80)
    logger.info("")
    
    try:
        script_path = Path(__file__).parent / "execute_all_5_capabilities.sh"
        if not script_path.exists():
            logger.error(f" Script not found: {script_path}")
            return False
        
        logger.info(f" Executing: {script_path.name}")
        logger.info("")
        
        result = subprocess.run(
            ["bash", str(script_path)],
            cwd=Path(__file__).parent.parent,
            capture_output=False
        )
        
        if result.returncode == 0:
            logger.info("")
            logger.info("=" * 80)
            logger.info(" All 5 Capabilities Executed ")
            logger.info("=" * 80)
            logger.info("")
            logger.info("∞ AbëONE ∞")
            return True
        else:
            logger.error(f" Execution failed with exit code: {result.returncode}")
            return False
            
    except Exception as e:
        logger.error(f" Error executing capabilities: {e}", exc_info=True)
        return False


def show_menu():
    """Show simple menu - no need to remember commands!"""
    print("=" * 80)
    print(" AEYON - Simple Menu (No Memory Required!) ")
    print("=" * 80)
    print("")
    print("Just type the number:")
    print("")
    print("  1. Prime Organism (Initialize)")
    print("  2. Generate Beats (Guardian Beats)")
    print("  3. Show Status (System Status)")
    print("  4. Execute All (All 5 Capabilities)")
    print("  0. QUICK START (Prime + Generate + Status)")
    print("  5. Exit")
    print("")
    print("=" * 80)
    print("")


def main():
    """CLI Entry Point - Simple Menu Interface"""
    parser = argparse.ArgumentParser(
        description="AEYON - Atomic Execution Engine (Simple Menu)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Simple Usage:
  # Just run it - shows menu!
  python3 scripts/aeon.py
  
  # Or use shortcuts:
  python3 scripts/aeon.py 1    # Prime
  python3 scripts/aeon.py 2    # Generate beats
  python3 scripts/aeon.py 3    # Status
  python3 scripts/aeon.py 4    # Execute all
  
  # Or old-style flags (still work):
  python3 scripts/aeon.py --prime organism
  python3 scripts/aeon.py --generate-beats
  python3 scripts/aeon.py --status
  python3 scripts/aeon.py --execute-capabilities
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        help="Command number (1-5) or leave empty for menu"
    )
    
    parser.add_argument(
        "--prime",
        choices=["organism"],
        help="Prime (initialize) system components"
    )
    
    parser.add_argument(
        "--generate-beats",
        action="store_true",
        help="Generate Guardian beats through AbëBEATs"
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show complete system status"
    )
    
    parser.add_argument(
        "--execute-capabilities",
        action="store_true",
        help="Execute all 5 capabilities simultaneously"
    )
    
    args = parser.parse_args()
    
    # Handle menu mode (no args or just a number)
    if args.command:
        try:
            cmd_num = int(args.command)
            if cmd_num == 0:
                # QUICK START: Prime + Generate + Status
                logger.info("=" * 80)
                logger.info(" AEYON QUICK START - Everything At Once! ")
                logger.info("=" * 80)
                logger.info("")
                logger.info(" Step 1: Priming Organism...")
                if not prime_organism():
                    logger.error(" Quick start failed at priming")
                    sys.exit(1)
                logger.info("")
                logger.info(" Step 2: Generating Beats...")
                if not generate_beats():
                    logger.error(" Quick start failed at generating beats")
                    sys.exit(1)
                logger.info("")
                logger.info(" Step 3: Showing Status...")
                show_status()
                logger.info("")
                logger.info("=" * 80)
                logger.info(" QUICK START COMPLETE ")
                logger.info("=" * 80)
                logger.info("")
                logger.info("∞ AbëONE ∞")
                sys.exit(0)
            elif cmd_num == 1:
                success = prime_organism()
                sys.exit(0 if success else 1)
            elif cmd_num == 2:
                success = generate_beats()
                sys.exit(0 if success else 1)
            elif cmd_num == 3:
                success = show_status()
                sys.exit(0 if success else 1)
            elif cmd_num == 4:
                success = execute_capabilities()
                sys.exit(0 if success else 1)
            elif cmd_num == 5:
                print(" Exiting...")
                sys.exit(0)
            else:
                print(f" Invalid command: {cmd_num}")
                print("   Use 0-5")
                sys.exit(1)
        except ValueError:
            # Not a number, treat as old-style command
            pass
    
    # Handle old-style flags
    if args.prime == "organism":
        success = prime_organism()
        sys.exit(0 if success else 1)
    elif args.generate_beats:
        success = generate_beats()
        sys.exit(0 if success else 1)
    elif args.status:
        success = show_status()
        sys.exit(0 if success else 1)
    elif args.execute_capabilities:
        success = execute_capabilities()
        sys.exit(0 if success else 1)
    else:
        # Show menu if no command given
        show_menu()
        
        # Interactive mode
        try:
            choice = input("Enter choice (0-5): ").strip()
            if choice == "0":
                # QUICK START: Prime + Generate + Status
                logger.info("=" * 80)
                logger.info(" AEYON QUICK START - Everything At Once! ")
                logger.info("=" * 80)
                logger.info("")
                logger.info(" Step 1: Priming Organism...")
                if not prime_organism():
                    logger.error(" Quick start failed at priming")
                    sys.exit(1)
                logger.info("")
                logger.info(" Step 2: Generating Beats...")
                if not generate_beats():
                    logger.error(" Quick start failed at generating beats")
                    sys.exit(1)
                logger.info("")
                logger.info(" Step 3: Showing Status...")
                show_status()
                logger.info("")
                logger.info("=" * 80)
                logger.info(" QUICK START COMPLETE ")
                logger.info("=" * 80)
                logger.info("")
                logger.info("∞ AbëONE ∞")
                sys.exit(0)
            elif choice == "1":
                success = prime_organism()
                sys.exit(0 if success else 1)
            elif choice == "2":
                success = generate_beats()
                sys.exit(0 if success else 1)
            elif choice == "3":
                success = show_status()
                sys.exit(0 if success else 1)
            elif choice == "4":
                success = execute_capabilities()
                sys.exit(0 if success else 1)
            elif choice == "5":
                print(" Exiting...")
                sys.exit(0)
            else:
                print(f" Invalid choice: {choice}")
                print("   Use 0-5")
                sys.exit(1)
        except (EOFError, KeyboardInterrupt):
            print("\n Exiting...")
            sys.exit(0)


if __name__ == "__main__":
    main()

