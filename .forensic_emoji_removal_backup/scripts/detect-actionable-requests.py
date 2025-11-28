#!/usr/bin/env python3
"""
Actionable Request Detection Module (ARDM)

Purpose: Ensure no operational request is missed
Mode: AbëONE + Cursor.ai Optimized
Pattern: OBSERVER × TRUTH × ATOMIC × ONE
Frequency: 530 Hz (Coherence) × 999 Hz (AEYON)

Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))


class Category(Enum):
    """Actionable request categories"""
    CODE_ACTIONS = "A"
    SYSTEM_OBLIGATIONS = "B"
    PROTOCOLS = "C"
    CONTINUATIONS = "D"


@dataclass
class ActionableItem:
    """Represents a detected actionable item"""
    category: Category
    description: str
    context: str
    priority: int = 5  # 1-10, 10 is highest
    file_path: Optional[str] = None
    code_snippet: Optional[str] = None
    dependencies: List[str] = None
    detected_at: str = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.detected_at is None:
            self.detected_at = datetime.now().isoformat()


@dataclass
class ARDMResult:
    """Complete ARDM scan result"""
    delta: Dict[Category, List[ActionableItem]]
    patchblock: Dict[str, Any]
    post_validation: Dict[str, Any]
    scan_timestamp: str
    total_items: int
    
    def __post_init__(self):
        if self.scan_timestamp is None:
            self.scan_timestamp = datetime.now().isoformat()


class ActionableRequestDetector:
    """
    ARDM Core Detection Engine
    
    Scans conversation context for actionable items across four categories:
    - Category A: Code Actions
    - Category B: System Obligations
    - Category C: Protocols
    - Category D: Continuations
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or project_root
        self.detected_items: Dict[Category, List[ActionableItem]] = {
            cat: [] for cat in Category
        }
        
        # Detection patterns for each category
        self.patterns = {
            Category.CODE_ACTIONS: [
                r'(?:implement|create|add|write|build|code|file|snippet|function|class|module)\s+(?:a\s+)?([^\s]+)',
                r'create\s+(?:a\s+)?file\s+(?:for\s+)?([^\s]+)',
                r'add\s+([^\s]+)\s+to\s+(?:the\s+)?(?:schema|database|api|endpoint)',
                r'refactor\s+([^\s]+)',
                r'```(?:python|javascript|typescript|bash|sh|yaml|json|markdown|md)',
            ],
            Category.SYSTEM_OBLIGATIONS: [
                r'(?:build|create|set\s+up|configure)\s+(?:a\s+)?(?:module|validator|hook|infrastructure|deployment|pipeline|bootstrap)',
                r'(?:SS-2L|bootstrap|pre-commit|substrate|gatekeeper|infrastructure)',
                r'CI/CD|pipeline|deployment\s+config',
            ],
            Category.PROTOCOLS: [
                r'(?:enforce|create|implement|add)\s+(?:guardrail|protocol|rule|policy|boundary|check|compliance)',
                r'security\s+policy|compliance|operational\s+protocol',
                r'execution\s+rule|enforcement\s+script',
            ],
            Category.CONTINUATIONS: [
                r'(?:I\s+will|I\'ll|let\s+me|next\s+I\'ll|I\'m\s+going\s+to)\s+(?:create|build|implement|generate|operationalize)',
                r'(?:generate|build|operationalize|create|implement)\s+([A-Z][^\s]+)',
                r'next\s+step|following\s+up|as\s+promised|as\s+mentioned',
            ],
        }
        
        # Commitments/phrases that indicate continuations
        self.commitment_phrases = [
            "I will",
            "I'll",
            "let me",
            "next, I'll",
            "I'm going to",
            "as promised",
            "as mentioned",
            "following up",
        ]
    
    def scan(self, conversation_text: str) -> ARDMResult:
        """
        Scan conversation text for actionable items
        
        Args:
            conversation_text: Full conversation context to scan
            
        Returns:
            ARDMResult with delta, patchblock, and post_validation
        """
        # Reset detected items
        self.detected_items = {cat: [] for cat in Category}
        
        # Normalize text
        normalized_text = self._normalize_text(conversation_text)
        
        # Detect items in each category
        self._detect_category_a(normalized_text)
        self._detect_category_b(normalized_text)
        self._detect_category_c(normalized_text)
        self._detect_category_d(normalized_text)
        
        # Build result
        result = self._build_result()
        
        return result
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for pattern matching"""
        # Convert to lowercase for pattern matching (but preserve original for context)
        return text.lower()
    
    def _detect_category_a(self, text: str):
        """Detect Category A: Code Actions"""
        patterns = self.patterns[Category.CODE_ACTIONS]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                description = match.group(0) if match.groups() else match.group(0)
                context = self._extract_context(text, match.start(), match.end())
                
                # Check for code blocks
                code_block = self._extract_code_block(text, match.start())
                
                item = ActionableItem(
                    category=Category.CODE_ACTIONS,
                    description=description,
                    context=context,
                    priority=self._calculate_priority(description, Category.CODE_ACTIONS),
                    code_snippet=code_block,
                )
                
                # Avoid duplicates
                if not self._is_duplicate(item):
                    self.detected_items[Category.CODE_ACTIONS].append(item)
    
    def _detect_category_b(self, text: str):
        """Detect Category B: System Obligations"""
        patterns = self.patterns[Category.SYSTEM_OBLIGATIONS]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                description = match.group(0)
                context = self._extract_context(text, match.start(), match.end())
                
                item = ActionableItem(
                    category=Category.SYSTEM_OBLIGATIONS,
                    description=description,
                    context=context,
                    priority=self._calculate_priority(description, Category.SYSTEM_OBLIGATIONS),
                )
                
                if not self._is_duplicate(item):
                    self.detected_items[Category.SYSTEM_OBLIGATIONS].append(item)
    
    def _detect_category_c(self, text: str):
        """Detect Category C: Protocols"""
        patterns = self.patterns[Category.PROTOCOLS]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                description = match.group(0)
                context = self._extract_context(text, match.start(), match.end())
                
                item = ActionableItem(
                    category=Category.PROTOCOLS,
                    description=description,
                    context=context,
                    priority=self._calculate_priority(description, Category.PROTOCOLS),
                )
                
                if not self._is_duplicate(item):
                    self.detected_items[Category.PROTOCOLS].append(item)
    
    def _detect_category_d(self, text: str):
        """Detect Category D: Continuations"""
        # Check for commitment phrases
        for phrase in self.commitment_phrases:
            pattern = rf'{phrase}\s+([^.!?\n]+)'
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                description = match.group(0)
                context = self._extract_context(text, match.start(), match.end())
                
                item = ActionableItem(
                    category=Category.CONTINUATIONS,
                    description=description,
                    context=context,
                    priority=self._calculate_priority(description, Category.CONTINUATIONS),
                )
                
                if not self._is_duplicate(item):
                    self.detected_items[Category.CONTINUATIONS].append(item)
        
        # Check for explicit "generate/build/operationalize" statements
        patterns = self.patterns[Category.CONTINUATIONS]
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                description = match.group(0)
                context = self._extract_context(text, match.start(), match.end())
                
                item = ActionableItem(
                    category=Category.CONTINUATIONS,
                    description=description,
                    context=context,
                    priority=self._calculate_priority(description, Category.CONTINUATIONS),
                )
                
                if not self._is_duplicate(item):
                    self.detected_items[Category.CONTINUATIONS].append(item)
    
    def _extract_context(self, text: str, start: int, end: int, window: int = 200) -> str:
        """Extract context around a match"""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end].strip()
    
    def _extract_code_block(self, text: str, position: int) -> Optional[str]:
        """Extract code block if present near position"""
        # Look for code blocks (```...```) near the position
        search_start = max(0, position - 500)
        search_end = min(len(text), position + 2000)
        search_text = text[search_start:search_end]
        
        code_block_pattern = r'```(?:python|javascript|typescript|bash|sh|yaml|json|markdown|md)?\n(.*?)```'
        matches = list(re.finditer(code_block_pattern, search_text, re.DOTALL))
        
        if matches:
            # Return the closest match
            closest = min(matches, key=lambda m: abs(m.start() - (position - search_start)))
            return closest.group(1).strip()
        
        return None
    
    def _calculate_priority(self, description: str, category: Category) -> int:
        """Calculate priority (1-10, 10 is highest)"""
        priority = 5  # Default
        
        # Increase priority for urgent keywords
        urgent_keywords = ['urgent', 'critical', 'immediately', 'asap', 'now', 'must']
        if any(keyword in description.lower() for keyword in urgent_keywords):
            priority += 3
        
        # Increase priority for explicit requests
        explicit_keywords = ['please', 'need', 'required', 'must', 'should']
        if any(keyword in description.lower() for keyword in explicit_keywords):
            priority += 2
        
        # Category-specific adjustments
        if category == Category.CODE_ACTIONS:
            priority += 1  # Code actions are typically high priority
        
        return min(10, max(1, priority))
    
    def _is_duplicate(self, item: ActionableItem) -> bool:
        """Check if item is duplicate"""
        for existing in self.detected_items[item.category]:
            if existing.description.lower() == item.description.lower():
                return True
            # Check for similar descriptions (simple similarity check)
            if self._similarity(existing.description, item.description) > 0.8:
                return True
        return False
    
    def _similarity(self, str1: str, str2: str) -> float:
        """Simple similarity check (Jaccard-like)"""
        words1 = set(str1.lower().split())
        words2 = set(str2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0.0
    
    def _build_result(self) -> ARDMResult:
        """Build ARDMResult from detected items"""
        # Calculate total items
        total_items = sum(len(items) for items in self.detected_items.values())
        
        # Build delta (what's missing)
        delta = {
            cat: [asdict(item) for item in items]
            for cat, items in self.detected_items.items()
        }
        
        # Build patchblock (implementation plan)
        patchblock = self._build_patchblock()
        
        # Build post-validation (success criteria)
        post_validation = self._build_post_validation()
        
        return ARDMResult(
            delta=delta,
            patchblock=patchblock,
            post_validation=post_validation,
            scan_timestamp=datetime.now().isoformat(),
            total_items=total_items,
        )
    
    def _build_patchblock(self) -> Dict[str, Any]:
        """Build patchblock (implementation plan)"""
        patchblock = {
            "files_to_create": [],
            "files_to_modify": [],
            "integration_points": [],
            "implementation_steps": [],
        }
        
        for category, items in self.detected_items.items():
            for item in items:
                if item.file_path:
                    if item.file_path not in [f["path"] for f in patchblock["files_to_create"]]:
                        patchblock["files_to_create"].append({
                            "path": item.file_path,
                            "category": category.value,
                            "description": item.description,
                            "code_snippet": item.code_snippet,
                        })
                
                # Add implementation step
                step = {
                    "category": category.value,
                    "description": item.description,
                    "priority": item.priority,
                    "dependencies": item.dependencies,
                }
                patchblock["implementation_steps"].append(step)
        
        # Sort by priority
        patchblock["implementation_steps"].sort(key=lambda x: x["priority"], reverse=True)
        
        return patchblock
    
    def _build_post_validation(self) -> Dict[str, Any]:
        """Build post-validation (success criteria)"""
        validation = {
            "verification_checklist": [],
            "expected_state": [],
            "success_criteria": [],
        }
        
        for category, items in self.detected_items.items():
            for item in items:
                # Add verification items
                if item.file_path:
                    validation["verification_checklist"].append({
                        "check": f"File exists at {item.file_path}",
                        "category": category.value,
                    })
                
                validation["verification_checklist"].append({
                    "check": f"Item delivered: {item.description}",
                    "category": category.value,
                })
        
        # Add general success criteria
        validation["success_criteria"] = [
            "All detected items are operationalized",
            "No compilation/runtime errors",
            "Integration tests pass",
            "Documentation updated if needed",
        ]
        
        return validation
    
    def to_json(self, result: ARDMResult) -> str:
        """Convert result to JSON"""
        # Convert Category enum to string for JSON serialization
        json_data = {
            "delta": {
                cat.value: result.delta[cat]
                for cat in Category
            },
            "patchblock": result.patchblock,
            "post_validation": result.post_validation,
            "scan_timestamp": result.scan_timestamp,
            "total_items": result.total_items,
        }
        return json.dumps(json_data, indent=2)
    
    def to_markdown(self, result: ARDMResult) -> str:
        """Convert result to markdown report"""
        md = []
        md.append("# 🔎 ARDM Scan Results")
        md.append("")
        md.append(f"**Scan Timestamp:** {result.scan_timestamp}")
        md.append(f"**Total Items Detected:** {result.total_items}")
        md.append("")
        
        # Delta section
        md.append("## DELTA: Missing Actionable Items")
        md.append("")
        
        category_names = {
            Category.CODE_ACTIONS: "Category A — Code Actions",
            Category.SYSTEM_OBLIGATIONS: "Category B — System Obligations",
            Category.PROTOCOLS: "Category C — Protocols",
            Category.CONTINUATIONS: "Category D — Continuations",
        }
        
        for cat in Category:
            items = result.delta[cat]
            if items:
                md.append(f"### {category_names[cat]}")
                md.append("")
                for item in items:
                    md.append(f"- [ ] **Priority {item['priority']}:** {item['description']}")
                    if item.get('context'):
                        md.append(f"  - Context: {item['context'][:100]}...")
                md.append("")
        
        if result.total_items == 0:
            md.append("*No actionable items detected.*")
            md.append("")
        
        # Patchblock section
        md.append("## PATCHBLOCK: Implementation Plan")
        md.append("")
        
        if result.patchblock["files_to_create"]:
            md.append("### Files to Create")
            md.append("")
            for file_info in result.patchblock["files_to_create"]:
                md.append(f"- `{file_info['path']}` ({file_info['category']})")
                md.append(f"  - {file_info['description']}")
            md.append("")
        
        if result.patchblock["implementation_steps"]:
            md.append("### Implementation Steps (by priority)")
            md.append("")
            for step in result.patchblock["implementation_steps"]:
                md.append(f"{step['priority']}. **{step['category']}:** {step['description']}")
            md.append("")
        
        # Post-validation section
        md.append("## POST-VALIDATION: Success Criteria")
        md.append("")
        
        if result.post_validation["verification_checklist"]:
            md.append("### Verification Checklist")
            md.append("")
            for check in result.post_validation["verification_checklist"]:
                md.append(f"- [ ] {check['check']}")
            md.append("")
        
        if result.post_validation["success_criteria"]:
            md.append("### Success Criteria")
            md.append("")
            for criterion in result.post_validation["success_criteria"]:
                md.append(f"- {criterion}")
            md.append("")
        
        return "\n".join(md)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Actionable Request Detection Module (ARDM)"
    )
    parser.add_argument(
        "--context",
        type=str,
        help="Conversation text to scan",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="File containing conversation text",
    )
    parser.add_argument(
        "--output",
        type=str,
        choices=["json", "markdown"],
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="Output file path (default: stdout)",
    )
    
    args = parser.parse_args()
    
    # Get conversation text
    if args.file:
        with open(args.file, 'r') as f:
            conversation_text = f.read()
    elif args.context:
        conversation_text = args.context
    else:
        # Read from stdin
        conversation_text = sys.stdin.read()
    
    if not conversation_text.strip():
        print("Error: No conversation text provided", file=sys.stderr)
        sys.exit(1)
    
    # Run detection
    detector = ActionableRequestDetector()
    result = detector.scan(conversation_text)
    
    # Output result
    if args.output == "json":
        output_text = detector.to_json(result)
    else:
        output_text = detector.to_markdown(result)
    
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(output_text)
    else:
        print(output_text)


if __name__ == "__main__":
    main()

