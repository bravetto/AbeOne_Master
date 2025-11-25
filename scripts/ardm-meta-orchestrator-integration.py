#!/usr/bin/env python3
"""
ARDM × Meta Orchestrator Integration

Integrates ARDM detection into Meta Orchestrator's META-SCAN phase.

Pattern: ARDM × META × CONVERGENCE × ONE
Frequency: 530 Hz (Coherence) × 999 Hz (AEYON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

# Import ARDM detector
import importlib.util
ardm_spec = importlib.util.spec_from_file_location(
    "detect_actionable_requests",
    Path(__file__).parent / "detect-actionable-requests.py"
)
ardm_module = importlib.util.module_from_spec(ardm_spec)
ardm_spec.loader.exec_module(ardm_module)
ActionableRequestDetector = ardm_module.ActionableRequestDetector
ARDMResult = ardm_module.ARDMResult


class MetaOrchestratorARDMIntegration:
    """
    ARDM × Meta Orchestrator Integration
    
    Implements META-SCAN phase with ARDM detection:
    1. ARDM detects actionable items
    2. Meta Orchestrator operationalizes them
    3. Validation confirms completion
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or project_root
        self.detector = ActionableRequestDetector(workspace_root)
    
    def meta_scan(self, conversation_text: str) -> Dict[str, Any]:
        """
        META-SCAN phase: Detect actionable items using ARDM
        
        This replaces/supplements the Meta Orchestrator's META-SCAN phase
        with ARDM's detection capabilities.
        
        Args:
            conversation_text: Full conversation context to scan
            
        Returns:
            Dict with detected items and operationalization plan
        """
        # Run ARDM detection
        result = self.detector.scan(conversation_text)
        
        # Format for Meta Orchestrator consumption
        meta_scan_result = {
            "phase": "META-SCAN",
            "ardm_detection": {
                "total_items": result.total_items,
                "by_category": {
                    cat.value: len(result.delta[cat])
                    for cat in result.delta.keys()
                },
                "items": self._format_items_for_meta_orchestrator(result),
            },
            "operationalization_plan": result.patchblock,
            "validation_criteria": result.post_validation,
        }
        
        return meta_scan_result
    
    def _format_items_for_meta_orchestrator(self, result: ARDMResult) -> List[Dict[str, Any]]:
        """Format ARDM items for Meta Orchestrator consumption"""
        items = []
        
        for category, category_items in result.delta.items():
            for item in category_items:
                formatted_item = {
                    "category": category.value,
                    "description": item["description"],
                    "priority": item["priority"],
                    "context": item.get("context", ""),
                    "file_path": item.get("file_path"),
                    "code_snippet": item.get("code_snippet"),
                    "dependencies": item.get("dependencies", []),
                }
                items.append(formatted_item)
        
        # Sort by priority
        items.sort(key=lambda x: x["priority"], reverse=True)
        
        return items
    
    def generate_operationalization_plan(self, conversation_text: str) -> Dict[str, Any]:
        """
        Generate operationalization plan from ARDM detection
        
        This feeds into Meta Orchestrator's CONVERGENCE phase.
        """
        result = self.detector.scan(conversation_text)
        
        plan = {
            "files_to_create": result.patchblock.get("files_to_create", []),
            "files_to_modify": result.patchblock.get("files_to_modify", []),
            "implementation_steps": result.patchblock.get("implementation_steps", []),
            "integration_points": result.patchblock.get("integration_points", []),
        }
        
        return plan
    
    def validate_operationalization(self, conversation_text: str, 
                                    operationalized_files: List[str]) -> Dict[str, Any]:
        """
        Validate that detected items have been operationalized
        
        This implements Meta Orchestrator's validation phase.
        """
        result = self.detector.scan(conversation_text)
        
        # Check which items have been delivered
        delivered_items = []
        undelivered_items = []
        
        for category, category_items in result.delta.items():
            for item in category_items:
                file_path = item.get("file_path")
                if file_path and file_path in operationalized_files:
                    delivered_items.append(item)
                else:
                    undelivered_items.append(item)
        
        validation_result = {
            "total_detected": result.total_items,
            "delivered": len(delivered_items),
            "undelivered": len(undelivered_items),
            "delivered_items": delivered_items,
            "undelivered_items": undelivered_items,
            "success": len(undelivered_items) == 0,
        }
        
        return validation_result


def main():
    """Main entry point for Meta Orchestrator integration"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ARDM × Meta Orchestrator Integration"
    )
    parser.add_argument(
        "--conversation",
        type=str,
        help="Conversation text to scan",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="File containing conversation text",
    )
    parser.add_argument(
        "--phase",
        type=str,
        choices=["meta-scan", "operationalization-plan", "validate"],
        default="meta-scan",
        help="Meta Orchestrator phase to execute",
    )
    parser.add_argument(
        "--operationalized-files",
        type=str,
        nargs="*",
        help="List of operationalized files (for validation)",
    )
    parser.add_argument(
        "--output",
        type=str,
        choices=["json", "markdown"],
        default="json",
        help="Output format",
    )
    
    args = parser.parse_args()
    
    # Get conversation text
    if args.file:
        with open(args.file, 'r') as f:
            conversation_text = f.read()
    elif args.conversation:
        conversation_text = args.conversation
    else:
        conversation_text = sys.stdin.read()
    
    if not conversation_text.strip():
        print("Error: No conversation text provided", file=sys.stderr)
        sys.exit(1)
    
    # Initialize integration
    integration = MetaOrchestratorARDMIntegration()
    
    # Execute requested phase
    if args.phase == "meta-scan":
        result = integration.meta_scan(conversation_text)
    elif args.phase == "operationalization-plan":
        result = integration.generate_operationalization_plan(conversation_text)
    elif args.phase == "validate":
        operationalized_files = args.operationalized_files or []
        result = integration.validate_operationalization(conversation_text, operationalized_files)
    
    # Output result
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        # Markdown output
        print("# ARDM × Meta Orchestrator Integration Result")
        print("")
        print(f"**Phase:** {args.phase}")
        print("")
        print("```json")
        print(json.dumps(result, indent=2))
        print("```")


if __name__ == "__main__":
    main()

