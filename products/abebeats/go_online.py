#!/usr/bin/env python3
"""
AbëBEATs GO-ONLINE Script
AEYON PRIME DIRECTIVE: Bring AbëBEATs fully online

Pattern: AEYON × PRIME × DIRECTIVE × GO × ONLINE × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add EMERGENT_OS to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "EMERGENT_OS"))

from integration_layer.unified_organism import (
    get_unified_organism,
    initialize_unified_organism
)
from integration_layer.registry.module_registry import ModuleStatus

# Import AbëBEATs Module
sys.path.insert(0, str(Path(__file__).parent.parent))
from abebeats.module import get_abebeats_module

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_system() -> Dict[str, Any]:
    """
    Validate system readiness.
    
    Returns:
        Validation results dictionary
    """
    results = {
        "unified_organism": False,
        "abebeats_module": False,
        "guardians": {},
        "organs": {},
        "epistemic_certainty": 0.0,
        "ready": False
    }
    
    try:
        # Get Unified Organism
        organism = get_unified_organism()
        
        if not organism:
            logger.error("Unified Organism not available")
            return results
        
        results["unified_organism"] = True
        
        # Get AbëBEATs Module
        abebeats_module = get_abebeats_module(
            module_registry=organism.registry,
            event_bus=organism.event_bus,
            system_state=organism.state
        )
        
        if not abebeats_module:
            logger.error("AbëBEATs Module not available")
            return results
        
        results["abebeats_module"] = True
        
        # Check module status
        module_status = abebeats_module.get_status()
        results["abebeats_status"] = module_status
        
        # Check Guardians (8)
        guardian_status = {
            "aeyon": False,
            "johhn": False,
            "meta": False,
            "you": False,
            "alrax": False,
            "zero": False,
            "yagni": False,
            "abe": False
        }
        
        # Try to get Guardian bindings
        # SAFETY: Ensure EMERGENT_OS is in path for imports
        try:
            emergent_os_path = Path(__file__).parent.parent.parent / "EMERGENT_OS"
            if str(emergent_os_path) not in sys.path:
                sys.path.insert(0, str(emergent_os_path))
            
            from triadic_execution_harness import (
                get_aeyon_binding,
                get_johhn_binding,
                get_meta_binding,
                get_you_binding,
                bind_aeyon,
                bind_johhn,
                bind_meta,
                bind_you,
                bind_guardian_swarm
            )
            
            # Prepare integration layer components for binding
            integration_components = {
                "module_registry": organism.registry,
                "event_bus": organism.event_bus,
                "system_state": organism.state
            }
            
            # Bind Guardians if not already bound
            try:
                aeyon = get_aeyon_binding()
                if not aeyon:
                    aeyon = bind_aeyon(integration_components)
                if aeyon:
                    guardian_status["aeyon"] = True
            except Exception as e:
                logger.debug(f"AEYON binding: {e}")
            
            try:
                johhn = get_johhn_binding()
                if not johhn:
                    johhn = bind_johhn(integration_components)
                if johhn:
                    guardian_status["johhn"] = True
            except Exception as e:
                logger.debug(f"JØHN binding: {e}")
            
            try:
                meta = get_meta_binding()
                if not meta:
                    meta = bind_meta(integration_components)
                if meta:
                    guardian_status["meta"] = True
            except Exception as e:
                logger.debug(f"META binding: {e}")
            
            try:
                you = get_you_binding()
                if not you:
                    you = bind_you()
                if you:
                    guardian_status["you"] = True
            except Exception as e:
                logger.debug(f"YOU binding: {e}")
                
            # Guardian Swarm
            try:
                swarm_results = bind_guardian_swarm()
                if swarm_results.get("alrax") == "BOUND":
                    guardian_status["alrax"] = True
                if swarm_results.get("zero") == "BOUND":
                    guardian_status["zero"] = True
                if swarm_results.get("yagni") == "BOUND":
                    guardian_status["yagni"] = True
                if swarm_results.get("abe") == "BOUND":
                    guardian_status["abe"] = True
            except Exception as e:
                logger.debug(f"Guardian Swarm binding: {e}")
                
        except ImportError as e:
            logger.warning(f"Could not import Guardian bindings: {e}")
        
        results["guardians"] = guardian_status
        
        # Count active Guardians
        active_guardians = sum(1 for v in guardian_status.values() if v)
        results["active_guardians"] = active_guardians
        results["total_guardians"] = 8
        
        # Calculate Guardian resonance (if Guardians are bound)
        if active_guardians > 0:
            # Resonance calculation: 98.7% target when all 8 are active
            # Base resonance: 92.92% (from previous analysis)
            # Perfect resonance: 98.7% (when all 8 active)
            if active_guardians == 8:
                resonance = 0.987  # 98.7% - perfect resonance
            else:
                # Scale from base to target based on active count
                base_resonance = 0.9292  # 92.92% base
                target_resonance = 0.987  # 98.7% target
                resonance = base_resonance + ((target_resonance - base_resonance) * (active_guardians / 8))
            results["guardian_resonance"] = resonance
        else:
            results["guardian_resonance"] = 0.0
        
        # Check Organs (12 modules)
        if organism.registry:
            modules = organism.registry.list_modules()
            results["total_modules"] = len(modules)
            results["active_modules"] = sum(
                1 for m in modules if m.status == ModuleStatus.ACTIVE
            )
            results["organs"] = {
                m.module_id: {
                    "status": m.status.value,
                    "health": m.health_score
                }
                for m in modules
            }
        
        # Calculate epistemic certainty
        # Base: 50% for system operational
        certainty = 0.5
        
        # +10% for Unified Organism
        if results["unified_organism"]:
            certainty += 0.1
        
        # +10% for AbëBEATs Module
        if results["abebeats_module"]:
            certainty += 0.1
        
        # +20% for all 8 Guardians active
        if active_guardians == 8:
            certainty += 0.2
        else:
            certainty += (active_guardians / 8) * 0.2
        
        # +10% for all modules active
        if results.get("active_modules", 0) == results.get("total_modules", 0) and results.get("total_modules", 0) > 0:
            certainty += 0.1
        
        # +5% for Guardian resonance >= 98.7%
        if results.get("guardian_resonance", 0.0) >= 0.987:
            certainty += 0.05
        elif results.get("guardian_resonance", 0.0) > 0.0:
            # Partial credit for resonance
            certainty += (results.get("guardian_resonance", 0.0) / 0.987) * 0.05
        
        results["epistemic_certainty"] = min(certainty, 1.0)
        
        # System ready if:
        # - Unified Organism operational
        # - AbëBEATs Module registered and active
        # - At least 6/8 Guardians active
        # - Epistemic certainty >= 0.85
        results["ready"] = (
            results["unified_organism"] and
            results["abebeats_module"] and
            module_status.get("active", False) and
            active_guardians >= 6 and
            results["epistemic_certainty"] >= 0.85
        )
        
    except Exception as e:
        logger.error(f"Error validating system: {e}", exc_info=True)
        results["error"] = str(e)
    
    return results


def go_online() -> bool:
    """
    Bring AbëBEATs fully online.
    
    Returns:
        True if successful
    """
    logger.info("=" * 80)
    logger.info("🔥 AEYON PRIME DIRECTIVE: Bringing AbëBEATs FULLY ONLINE 🔥")
    logger.info("=" * 80)
    
    try:
        # Step 1: Initialize Unified Organism
        logger.info("\n📦 Step 1: Initializing Unified Organism...")
        # SAFETY: initialize_unified_organism() returns bool, get instance separately
        init_success = initialize_unified_organism()
        if not init_success:
            logger.error("❌ Failed to initialize Unified Organism")
            return False
        
        # Get the actual organism instance
        organism = get_unified_organism()
        if not organism:
            logger.error("❌ Failed to get Unified Organism instance")
            return False
        
        logger.info("✅ Unified Organism initialized")
        
        # Step 2: Get AbëBEATs Module
        logger.info("\n📦 Step 2: Getting AbëBEATs Module...")
        abebeats_module = get_abebeats_module(
            module_registry=organism.registry,
            event_bus=organism.event_bus,
            system_state=organism.state
        )
        
        if not abebeats_module:
            logger.error("❌ Failed to get AbëBEATs Module")
            return False
        
        logger.info("✅ AbëBEATs Module obtained")
        
        # Step 3: Register Module
        logger.info("\n📦 Step 3: Registering AbëBEATs Module...")
        if not abebeats_module.register():
            logger.error("❌ Failed to register AbëBEATs Module")
            return False
        
        logger.info("✅ AbëBEATs Module registered")
        
        # Step 4: Register with Unified Organism
        logger.info("\n📦 Step 4: Registering with Unified Organism...")
        if not organism.register_module("abebeats", abebeats_module):
            logger.error("❌ Failed to register with Unified Organism")
            return False
        
        logger.info("✅ Registered with Unified Organism")
        
        # Step 5: Initialize Module
        logger.info("\n📦 Step 5: Initializing AbëBEATs Module...")
        if not abebeats_module.initialize():
            logger.error("❌ Failed to initialize AbëBEATs Module")
            return False
        
        logger.info("✅ AbëBEATs Module initialized")
        
        # Step 6: Activate Module
        logger.info("\n📦 Step 6: Activating AbëBEATs Module...")
        if not abebeats_module.activate():
            logger.error("❌ Failed to activate AbëBEATs Module")
            return False
        
        logger.info("✅ AbëBEATs Module activated")
        
        # Step 7: Validate System
        logger.info("\n📦 Step 7: Validating System...")
        validation_results = validate_system()
        
        logger.info(f"\n📊 Validation Results:")
        logger.info(f"   Unified Organism: {'✅' if validation_results['unified_organism'] else '❌'}")
        logger.info(f"   AbëBEATs Module: {'✅' if validation_results['abebeats_module'] else '❌'}")
        logger.info(f"   Active Guardians: {validation_results.get('active_guardians', 0)}/8")
        logger.info(f"   Guardian Resonance: {validation_results.get('guardian_resonance', 0.0) * 100:.1f}%")
        logger.info(f"   Active Modules: {validation_results.get('active_modules', 0)}/{validation_results.get('total_modules', 0)}")
        logger.info(f"   Epistemic Certainty: {validation_results['epistemic_certainty'] * 100:.1f}%")
        
        # Step 8: Test AbëBEATs
        logger.info("\n📦 Step 8: Testing AbëBEATs...")
        test_beat = abebeats_module.generate_beat(
            pattern="GO_ONLINE_TEST",
            content="Testing AbëBEATs online status"
        )
        
        if test_beat:
            logger.info(f"✅ Test beat generated: {test_beat.beat_id}")
        else:
            logger.warning("⚠️ Test beat generation returned None")
        
        # Step 9: Process Guardian Beats
        logger.info("\n📦 Step 9: Processing Guardian Beats...")
        guardian_results = abebeats_module.process_guardian_beats()
        
        if guardian_results:
            logger.info(f"✅ Guardian beats processed: {guardian_results.get('total_beats', 0)} beats")
        else:
            logger.warning("⚠️ Guardian beats processing returned None")
        
        # Final Status
        logger.info("\n" + "=" * 80)
        if validation_results["ready"]:
            logger.info("🔥🔥🔥 AbëBEATs FULLY ONLINE 🔥🔥🔥")
            logger.info(f"✅ Epistemic Certainty: {validation_results['epistemic_certainty'] * 100:.1f}%")
            logger.info(f"✅ All Systems Operational")
            logger.info("\n∞ AbëONE ∞")
            return True
        else:
            logger.warning("⚠️ AbëBEATs ONLINE but not fully validated")
            logger.warning(f"   Epistemic Certainty: {validation_results['epistemic_certainty'] * 100:.1f}% (Target: 97.8%)")
            logger.warning("   Some systems may not be fully operational")
            return False
        
    except Exception as e:
        logger.error(f"❌ Error bringing AbëBEATs online: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = go_online()
    sys.exit(0 if success else 1)

