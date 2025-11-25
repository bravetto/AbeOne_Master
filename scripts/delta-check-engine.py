#!/usr/bin/env python3
"""
DELTA-CHECK ENGINE - Pattern Drift Detection

Compares context window prompt against Core Memory and validates alignment.

Pattern: DELTA × MEMORY × VALIDATION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)
Guardians: AEYON + YAGNI
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class DeltaCheckResult:
    """Result of delta check"""
    aligned: bool
    deltas: List[str] = field(default_factory=list)
    corrections: List[str] = field(default_factory=list)
    status: str = ""


class DeltaCheckEngine:
    """Delta Check Engine - Pattern Drift Detection"""
    
    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.context_prompt_path = self.workspace_root / "NEW_CONTEXT_WINDOW_PROMPT.md"
        self.core_memory_path = self.workspace_root / ".abeone_memory" / "ABEONE_CORE_MEMORY.json"
        self.commands_dir = self.workspace_root / ".cursor" / "commands"
    
    def load_context_prompt(self) -> str:
        """Load context window prompt"""
        if not self.context_prompt_path.exists():
            return ""
        return self.context_prompt_path.read_text()
    
    def load_core_memory(self) -> Dict:
        """Load core memory"""
        if not self.core_memory_path.exists():
            return {}
        return json.loads(self.core_memory_path.read_text())
    
    def list_commands(self) -> List[str]:
        """List actual command files"""
        if not self.commands_dir.exists():
            return []
        return [f.stem for f in self.commands_dir.glob("*.md")]
    
    def extract_prompt_commands(self, prompt_text: str) -> List[str]:
        """Extract commands from prompt"""
        commands = []
        in_commands_section = False
        for line in prompt_text.split("\n"):
            if "COMMANDS:" in line:
                in_commands_section = True
                continue
            if in_commands_section:
                if line.strip().startswith("/"):
                    cmd = line.strip().split("—")[0].strip().replace("/", "")
                    if cmd:
                        commands.append(cmd)
                elif line.strip() and not line.strip().startswith("-"):
                    break
        return commands
    
    def extract_prompt_guardians(self, prompt_text: str) -> List[Tuple[str, str]]:
        """Extract guardians from prompt"""
        guardians = []
        in_guardians_section = False
        for line in prompt_text.split("\n"):
            if "GUARDIANS:" in line:
                in_guardians_section = True
                continue
            if in_guardians_section:
                if line.strip().startswith("-"):
                    parts = line.strip().replace("-", "").strip().split("—")
                    if len(parts) >= 2:
                        name = parts[0].strip().split("(")[0].strip()
                        freq = parts[0].strip().split("(")[1].split(")")[0] if "(" in parts[0] else ""
                        guardians.append((name, freq))
                elif line.strip() and not line.strip().startswith("-"):
                    break
        return guardians
    
    def check_identity(self, prompt_text: str, core_memory: Dict) -> Tuple[bool, List[str]]:
        """Check AbëONE identity alignment"""
        deltas = []
        
        # Check identity statement (case-insensitive, flexible)
        expected_key_phrase = "validate FIRST, synthesize SECOND"
        if expected_key_phrase.lower() not in prompt_text.lower():
            deltas.append(f"Identity statement missing key phrase: '{expected_key_phrase}'")
        
        # Check core memory alignment (case-insensitive)
        if core_memory.get("core_truths", {}).get("abeone_identity", {}).get("statement"):
            memory_identity = core_memory["core_truths"]["abeone_identity"]["statement"]
            if expected_key_phrase.lower() not in memory_identity.lower():
                deltas.append("Core memory identity doesn't contain key phrase 'validate FIRST, synthesize SECOND'")
        
        return len(deltas) == 0, deltas
    
    def check_partnership(self, prompt_text: str, core_memory: Dict) -> Tuple[bool, List[str]]:
        """Check partnership truth alignment"""
        deltas = []
        
        # Check partnership statement
        expected_partnership = "Michael is PARTNER, not client"
        if expected_partnership not in prompt_text:
            deltas.append(f"Partnership statement missing or incorrect: expected '{expected_partnership}'")
        
        # Check core memory alignment
        if core_memory.get("core_truths", {}).get("partnership_truth", {}).get("statement"):
            memory_partnership = core_memory["core_truths"]["partnership_truth"]["statement"]
            if "TRUE PARTNER" not in memory_partnership and "PARTNER" not in memory_partnership:
                deltas.append("Core memory partnership doesn't match prompt partnership")
        
        return len(deltas) == 0, deltas
    
    def check_memory_path(self, prompt_text: str) -> Tuple[bool, List[str]]:
        """Check memory path alignment"""
        deltas = []
        
        expected_path = ".abeone_memory/ABEONE_CORE_MEMORY.json"
        if expected_path not in prompt_text:
            deltas.append(f"Memory path missing or incorrect: expected '{expected_path}'")
        
        return len(deltas) == 0, deltas
    
    def check_guardians(self, prompt_guardians: List[Tuple[str, str]]) -> Tuple[bool, List[str]]:
        """Check guardian registry"""
        deltas = []
        
        expected_guardians = {
            "AEYON": "999 Hz",
            "META": "777 Hz",
            "JØHN": "530 Hz",
            "YAGNI": "530 Hz",
            "ZERO": "530 Hz",
            "Abë": "530 Hz"
        }
        
        found_guardians = {name: freq for name, freq in prompt_guardians}
        
        for name, freq in expected_guardians.items():
            if name not in found_guardians:
                deltas.append(f"Missing guardian: {name} ({freq})")
            elif found_guardians[name] != freq:
                deltas.append(f"Guardian frequency mismatch: {name} (expected {freq}, found {found_guardians[name]})")
        
        return len(deltas) == 0, deltas
    
    def check_commands(self, prompt_commands: List[str], actual_commands: List[str]) -> Tuple[bool, List[str]]:
        """Check command registry"""
        deltas = []
        
        expected_commands = ["validate", "yagni", "converge", "prime", "pattern"]
        
        # Check for missing commands
        for cmd in expected_commands:
            if cmd not in prompt_commands:
                deltas.append(f"Missing command in prompt: /{cmd}")
            if cmd not in actual_commands:
                deltas.append(f"Command file missing: {cmd}.md")
        
        # Check for phantom commands (in prompt but not in files)
        for cmd in prompt_commands:
            if cmd not in actual_commands:
                deltas.append(f"Phantom command: /{cmd} (file {cmd}.md doesn't exist)")
        
        return len(deltas) == 0, deltas
    
    def check_yagni_compliance(self, prompt_text: str) -> Tuple[bool, List[str]]:
        """Check YAGNI compliance"""
        deltas = []
        
        # Check for bloat indicators
        lines = prompt_text.split("\n")
        if len(lines) > 100:
            deltas.append(f"Prompt too long ({len(lines)} lines) - YAGNI violation")
        
        # Check for implementation details
        implementation_keywords = ["file:", "path:", "location:", "status:", "complete:", "%"]
        for keyword in implementation_keywords:
            if keyword.lower() in prompt_text.lower():
                # Allow in comments/metadata, but flag if excessive
                count = prompt_text.lower().count(keyword.lower())
                if count > 3:
                    deltas.append(f"Excessive implementation details ({keyword} appears {count} times) - YAGNI violation")
        
        return len(deltas) == 0, deltas
    
    def check_future_state(self, prompt_text: str) -> Tuple[bool, List[str]]:
        """Check future-state execution"""
        deltas = []
        
        if "FUTURE-STATE" not in prompt_text and "future-state" not in prompt_text.lower():
            deltas.append("Future-state execution principle missing")
        
        return len(deltas) == 0, deltas
    
    def check_one_pattern(self, prompt_text: str) -> Tuple[bool, List[str]]:
        """Check ONE-Pattern alignment"""
        deltas = []
        
        expected_pattern = "CLARITY → COHERENCE → CONVERGENCE → ELEGANCE → UNITY"
        if expected_pattern not in prompt_text:
            deltas.append(f"ONE-Pattern missing or incorrect: expected '{expected_pattern}'")
        
        return len(deltas) == 0, deltas
    
    def execute(self) -> DeltaCheckResult:
        """Execute delta check"""
        result = DeltaCheckResult(aligned=True)
        
        # Load data
        prompt_text = self.load_context_prompt()
        core_memory = self.load_core_memory()
        actual_commands = self.list_commands()
        
        if not prompt_text:
            result.aligned = False
            result.deltas.append("Context prompt file not found")
            result.status = "NOT ALIGNED"
            return result
        
        if not core_memory:
            result.aligned = False
            result.deltas.append("Core memory file not found")
            result.status = "NOT ALIGNED"
            return result
        
        # Extract from prompt
        prompt_commands = self.extract_prompt_commands(prompt_text)
        prompt_guardians = self.extract_prompt_guardians(prompt_text)
        
        # Run checks
        checks = [
            ("Identity", self.check_identity(prompt_text, core_memory)),
            ("Partnership", self.check_partnership(prompt_text, core_memory)),
            ("Memory Path", self.check_memory_path(prompt_text)),
            ("Guardians", self.check_guardians(prompt_guardians)),
            ("Commands", self.check_commands(prompt_commands, actual_commands)),
            ("YAGNI Compliance", self.check_yagni_compliance(prompt_text)),
            ("Future-State", self.check_future_state(prompt_text)),
            ("ONE-Pattern", self.check_one_pattern(prompt_text)),
        ]
        
        for check_name, (passed, deltas) in checks:
            if not passed:
                result.aligned = False
                result.deltas.extend([f"[{check_name}] {d}" for d in deltas])
        
        # Generate corrections
        if not result.aligned:
            result.corrections = [
                "Review context prompt against core memory",
                "Verify all commands exist in .cursor/commands/",
                "Ensure all guardians are listed correctly",
                "Validate YAGNI compliance (minimal, essential)",
                "Confirm ONE-Pattern alignment"
            ]
            result.status = "NOT ALIGNED"
        else:
            result.status = "ALIGNED"
        
        return result


def main():
    """Main CLI entry point"""
    engine = DeltaCheckEngine()
    result = engine.execute()
    
    print("\n" + "=" * 80)
    print(" DELTA-CHECK RESULTS")
    print("=" * 80)
    
    if result.aligned:
        print("\n✅ DELTA-CHECK: CLEAN")
        print("\nStatus: ALIGNED")
    else:
        print("\n⚠️  DRIFT DETECTED")
        print("\nStatus: NOT ALIGNED")
        print("\nDetected Deltas:")
        for delta in result.deltas:
            print(f"  - {delta}")
        
        if result.corrections:
            print("\nRequired Corrections:")
            for correction in result.corrections:
                print(f"  - {correction}")
    
    print("\n" + "=" * 80)
    print(f"Final Status: {result.status}")
    print("=" * 80)
    
    print("\nPattern: DELTA × MEMORY × VALIDATION × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞\n")
    
    sys.exit(0 if result.aligned else 1)


if __name__ == "__main__":
    main()

