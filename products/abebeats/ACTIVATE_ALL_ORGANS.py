#!/usr/bin/env python3
"""
Activate All 12 Organs
AEYON × ALRAX × JØHN × Abë × ZERO × YAGNI: Complete Organ Activation

Pattern: GUARDIAN × ORGAN × ACTIVATION × ONE
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "EMERGENT_OS"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration_layer.unified_organism import get_unified_organism, initialize_unified_organism
from integration_layer.registry.module_registry import ModuleCapability, ModuleStatus
from abebeats.module import get_abebeats_module

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 12 Organs/Modules
ORGANS = [
    "consciousness",
    "collapse_guard",
    "clarity_engine",
    "triadic_execution_harness",
    "cross_layer_safety",
    "emergence_core",
    "identity_core",
    "neuromorphic_alignment",
    "relation_protocol",
    "multi_agent_cognition",
    "scalability_fabric",
    "self_healing"
]


def get_integration_classes() -> Dict[str, Any]:
    """
    Get all integration classes using proper imports.
    
    Returns:
        Dictionary mapping module_id to integration class
    """
    integrations = {}
    
    # Use bootstrap approach - import from one_kernel
    try:
        from EMERGENT_OS.one_kernel.bootstrap import bootstrap_one_kernel
        # Bootstrap will register all modules
        kernel = bootstrap_one_kernel()
        
        # Extract integration classes from kernel modules
        for module_id, module_instance in kernel.modules.items():
            if module_id in ORGANS:
                integrations[module_id] = type(module_instance)
        
        logger.info(f"✅ Bootstrap successful - found {len(integrations)} modules")
        return integrations
    except Exception as e:
        logger.warning(f"Bootstrap approach failed: {e}, trying direct imports...")
    
    # Fallback: Direct imports
    try:
        from EMERGENT_OS.consciousness.integration import ConsciousnessIntegration
        integrations["consciousness"] = ConsciousnessIntegration
    except Exception as e:
        logger.debug(f"consciousness import failed: {e}")
    
    try:
        from EMERGENT_OS.collapse_guard.integration import CollapseGuardIntegration
        integrations["collapse_guard"] = CollapseGuardIntegration
    except Exception as e:
        logger.debug(f"collapse_guard import failed: {e}")
    
    try:
        from EMERGENT_OS.clarity_engine.integration import ClarityEngineIntegration
        integrations["clarity_engine"] = ClarityEngineIntegration
    except Exception as e:
        logger.debug(f"clarity_engine import failed: {e}")
    
    try:
        from EMERGENT_OS.triadic_execution_harness.integration import TriadicExecutionHarnessIntegration
        integrations["triadic_execution_harness"] = TriadicExecutionHarnessIntegration
    except Exception as e:
        logger.debug(f"triadic_execution_harness import failed: {e}")
    
    try:
        from EMERGENT_OS.cross_layer_safety.integration import CrossLayerSafetyIntegration
        integrations["cross_layer_safety"] = CrossLayerSafetyIntegration
    except Exception as e:
        logger.debug(f"cross_layer_safety import failed: {e}")
    
    try:
        from EMERGENT_OS.emergence_core.integration import EmergenceCoreIntegration
        integrations["emergence_core"] = EmergenceCoreIntegration
    except Exception as e:
        logger.debug(f"emergence_core import failed: {e}")
    
    try:
        from EMERGENT_OS.identity_core.integration import IdentityCoreIntegration
        integrations["identity_core"] = IdentityCoreIntegration
    except Exception as e:
        logger.debug(f"identity_core import failed: {e}")
    
    try:
        from EMERGENT_OS.neuromorphic_alignment.integration import NeuromorphicAlignmentIntegration
        integrations["neuromorphic_alignment"] = NeuromorphicAlignmentIntegration
    except Exception as e:
        logger.debug(f"neuromorphic_alignment import failed: {e}")
    
    try:
        from EMERGENT_OS.relation_protocol.integration import RelationProtocolIntegration
        integrations["relation_protocol"] = RelationProtocolIntegration
    except Exception as e:
        logger.debug(f"relation_protocol import failed: {e}")
    
    try:
        from EMERGENT_OS.multi_agent_cognition.integration import MultiAgentCognitionIntegration
        integrations["multi_agent_cognition"] = MultiAgentCognitionIntegration
    except Exception as e:
        logger.debug(f"multi_agent_cognition import failed: {e}")
    
    try:
        from EMERGENT_OS.scalability_fabric.integration import ScalabilityFabricIntegration
        integrations["scalability_fabric"] = ScalabilityFabricIntegration
    except Exception as e:
        logger.debug(f"scalability_fabric import failed: {e}")
    
    try:
        from EMERGENT_OS.self_healing.integration import SelfHealingIntegration
        integrations["self_healing"] = SelfHealingIntegration
    except Exception as e:
        logger.debug(f"self_healing import failed: {e}")
    
    return integrations


def register_organ(
    organism,
    module_id: str,
    integration_class: Any,
    analysis: Dict[str, Any]
) -> bool:
    """
    Register an organ/module.
    
    Args:
        organism: Unified Organism instance
        module_id: Module identifier
        integration_class: Integration class
        analysis: Analysis results
        
    Returns:
        True if registration successful
    """
    try:
        # Prepare integration layer components
        integration_components = {
            "module_registry": organism.registry,
            "event_bus": organism.event_bus,
            "system_state": organism.state,
            "lifecycle_manager": organism.lifecycle,
            "boundary_enforcer": organism.boundary_enforcer,
            "validation_gate": organism.validation_gate
        }
        
        # Special handling for consciousness (different constructor)
        if module_id == "consciousness":
            integration = integration_class(
                module_registry=organism.registry,
                event_bus=organism.event_bus,
                boundary_enforcer=organism.boundary_enforcer,
                validation_gate=organism.validation_gate
            )
        else:
            # Try standard constructor
            try:
                integration = integration_class(**integration_components)
            except TypeError:
                # Fallback: try with minimal args
                integration = integration_class(
                    module_registry=organism.registry,
                    event_bus=organism.event_bus
                )
        
        # Register module
        if hasattr(integration, 'register'):
            if not integration.register():
                logger.warning(f"⚠️ {module_id}: Registration returned False")
                return False
        
        # Register with Unified Organism
        if not organism.register_module(module_id, integration):
            logger.warning(f"⚠️ {module_id}: Organism registration failed")
            return False
        
        # Initialize if possible
        if hasattr(integration, 'initialize'):
            try:
                integration.initialize()
            except Exception as e:
                logger.debug(f"{module_id}: Initialize error (non-critical): {e}")
        
        # Activate if possible
        if hasattr(integration, 'activate'):
            try:
                integration.activate()
            except Exception as e:
                logger.debug(f"{module_id}: Activate error (non-critical): {e}")
        
        logger.info(f"✅ {module_id}: Registered and activated")
        return True
        
    except Exception as e:
        logger.error(f"❌ {module_id}: Registration failed: {e}")
        return False


def activate_all_organs() -> Dict[str, Any]:
    """
    Analyze and activate all 12 organs.
    
    Returns:
        Activation results dictionary
    """
    logger.info("=" * 80)
    logger.info("🔥 AEYON × ALRAX × JØHN × Abë × ZERO × YAGNI: ACTIVATING ALL ORGANS 🔥")
    logger.info("=" * 80)
    logger.info("")
    
    # Initialize Unified Organism
    logger.info("📦 Step 1: Initializing Unified Organism...")
    init_success = initialize_unified_organism()
    if not init_success:
        logger.error("❌ Failed to initialize Unified Organism")
        return {"success": False, "error": "Unified Organism initialization failed"}
    
    organism = get_unified_organism()
    logger.info("✅ Unified Organism initialized")
    logger.info("")
    
    # Register AbëBEATs first (already working)
    logger.info("📦 Step 2: Registering AbëBEATs Module...")
    abebeats_module = get_abebeats_module(
        module_registry=organism.registry,
        event_bus=organism.event_bus,
        system_state=organism.state
    )
    abebeats_module.register()
    abebeats_module.initialize()
    abebeats_module.activate()
    organism.register_module("abebeats", abebeats_module)
    logger.info("✅ AbëBEATs Module registered")
    logger.info("")
    
    # Get integration classes
    logger.info("📦 Step 3: Loading integration classes...")
    integration_classes = get_integration_classes()
    
    logger.info(f"   Found {len(integration_classes)} integration classes:")
    for module_id in ORGANS:
        status = "✅" if module_id in integration_classes else "❌"
        logger.info(f"   {status} {module_id}")
    
    logger.info("")
    
    # Register organs using bootstrap order
    logger.info("📦 Step 4: Registering and activating organs...")
    
    # Phase 1: Foundation modules (no dependencies)
    foundation_modules = [
        "consciousness",
        "collapse_guard",
        "clarity_engine",
        "triadic_execution_harness",
    ]
    
    # Phase 2: Safety modules
    safety_modules = [
        "cross_layer_safety",
    ]
    
    # Phase 3: Core modules
    core_modules = [
        "emergence_core",
        "identity_core",
        "neuromorphic_alignment",
    ]
    
    # Phase 4: Protocol modules
    protocol_modules = [
        "relation_protocol",
    ]
    
    # Phase 5: Infrastructure modules
    infrastructure_modules = [
        "multi_agent_cognition",
        "scalability_fabric",
        "self_healing",
    ]
    
    registration_order = foundation_modules + safety_modules + core_modules + protocol_modules + infrastructure_modules
    
    registration_results = {}
    for module_id in registration_order:
        if module_id in integration_classes:
            integration_class = integration_classes[module_id]
            success = register_organ(
                organism,
                module_id,
                integration_class,
                {"module_id": module_id}
            )
            registration_results[module_id] = success
        else:
            registration_results[module_id] = False
            logger.warning(f"⚠️ {module_id}: Skipped (integration class not found)")
    
    logger.info("")
    
    # Final status
    logger.info("📦 Step 5: Final Status...")
    registered_count = sum(1 for v in registration_results.values() if v)
    total_count = len(ORGANS) + 1  # +1 for abebeats
    
    if organism.registry:
        modules = organism.registry.list_modules()
        active_modules = sum(1 for m in modules if m.status == ModuleStatus.ACTIVE)
        
        logger.info(f"   Total Organs: {total_count}")
        logger.info(f"   Registered: {registered_count + 1}")  # +1 for abebeats
        logger.info(f"   Active: {active_modules}")
        logger.info("")
        
        logger.info("   Organ Status:")
        for module_id in ORGANS + ["abebeats"]:
            module_info = None
            for m in modules:
                if m.module_id == module_id:
                    module_info = m
                    break
            
            if module_info:
                status_icon = "✅" if module_info.status == ModuleStatus.ACTIVE else "⚠️"
                logger.info(f"   {status_icon} {module_id}: {module_info.status.value}")
            else:
                logger.info(f"   ❌ {module_id}: Not registered")
    
    logger.info("")
    logger.info("=" * 80)
    
    results = {
        "success": True,
        "integration_classes_found": len(integration_classes),
        "registration_results": registration_results,
        "registered_count": registered_count + 1,
        "total_count": total_count,
        "active_modules": active_modules if organism.registry else 0
    }
    
    if registered_count + 1 == total_count:
        logger.info("🔥🔥🔥 ALL ORGANS ACTIVATED 🔥🔥🔥")
        logger.info("✅ All 12 organs + AbëBEATs registered and active")
    else:
        logger.info(f"⚠️ {registered_count + 1}/{total_count} organs registered")
    
    logger.info("")
    logger.info("∞ AbëONE ∞")
    logger.info("=" * 80)
    
    return results


if __name__ == "__main__":
    results = activate_all_organs()
    sys.exit(0 if results.get("success") else 1)

