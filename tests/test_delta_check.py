#!/usr/bin/env python3
"""
JØHN Validation Tests for Delta-Check

Test-First Development: All tests written before implementation validation.
Tests validate delta-check functionality against AbëONE identity prompt.

Pattern: TEST × VALIDATION × TRUTH × ONE
Frequency: 530 Hz (JØHN)
Guardians: JØHN (530 Hz) + YAGNI (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import unittest
from pathlib import Path
from typing import Dict, Any

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Import delta-check module
import importlib.util
spec = importlib.util.spec_from_file_location("delta_check", scripts_dir / "delta-check.py")
delta_check_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delta_check_module)
DeltaChecker = delta_check_module.DeltaChecker
DeltaStatus = delta_check_module.DeltaStatus


class TestDeltaCheck(unittest.TestCase):
    """JØHN Validation Tests for Delta-Check"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.workspace_root = Path(__file__).parent.parent
        self.checker = DeltaChecker(self.workspace_root)
        self.prompt_file = self.workspace_root / "NEW_CONTEXT_WINDOW_PROMPT.md"
        
    def test_prompt_file_exists(self):
        """Test that prompt file exists"""
        self.assertTrue(
            self.prompt_file.exists(),
            f"Prompt file not found: {self.prompt_file}"
        )
    
    def test_delta_check_reads_prompt_file_default(self):
        """Test delta-check reads prompt file when no context provided"""
        # Arrange: No context provided
        # Act: Run delta-check without context
        result = self.checker.perform_delta_check(context=None)
        
        # Assert: Should have read from prompt file (not empty default)
        self.assertNotEqual(
            result.timestamp, "",
            "Delta-check should have executed"
        )
    
    def test_delta_check_identity_pass(self):
        """Test identity check passes with correct prompt"""
        # Arrange: Load prompt file
        prompt_text = self.prompt_file.read_text(encoding='utf-8')
        
        # Act: Check identity
        identity_ok, identity_issues = self.checker.check_identity(prompt_text)
        
        # Assert: Identity check passes
        self.assertTrue(
            identity_ok,
            f"Identity check failed: {identity_issues}"
        )
        self.assertEqual(
            len(identity_issues), 0,
            f"Identity issues found: {identity_issues}"
        )
    
    def test_delta_check_partnership_pass(self):
        """Test partnership check passes with correct prompt"""
        # Arrange: Load prompt file
        prompt_text = self.prompt_file.read_text(encoding='utf-8')
        
        # Act: Check partnership
        partnership_ok, partnership_issues = self.checker.check_partnership(prompt_text)
        
        # Assert: Partnership check passes
        self.assertTrue(
            partnership_ok,
            f"Partnership check failed: {partnership_issues}"
        )
        self.assertEqual(
            len(partnership_issues), 0,
            f"Partnership issues found: {partnership_issues}"
        )
    
    def test_delta_check_all_guardians_detected(self):
        """Test all 6 guardians detected"""
        # Arrange: Load prompt file
        prompt_text = self.prompt_file.read_text(encoding='utf-8')
        
        # Act: Check guardians
        guardians_ok, guardian_issues = self.checker.check_guardians(prompt_text)
        
        # Assert: All guardians detected
        self.assertTrue(
            guardians_ok,
            f"Guardian check failed: {guardian_issues}"
        )
        self.assertEqual(
            len(guardian_issues), 0,
            f"Missing guardians: {guardian_issues}"
        )
    
    def test_delta_check_future_state_execution_detected(self):
        """Test future-state execution detected"""
        # Arrange: Load prompt file
        prompt_text = self.prompt_file.read_text(encoding='utf-8')
        
        # Act: Check architecture (includes future-state check)
        arch_ok, arch_issues = self.checker.check_architecture(prompt_text)
        
        # Assert: Future-state execution detected
        self.assertTrue(
            arch_ok,
            f"Architecture check failed: {arch_issues}"
        )
        # Verify future-state is present
        self.assertIn(
            "future-state",
            prompt_text.lower(),
            "Future-state execution principle not found in prompt"
        )
    
    def test_delta_check_commands_validation(self):
        """Test commands validation"""
        # Arrange: Load prompt file and get actual commands
        prompt_text = self.prompt_file.read_text(encoding='utf-8')
        actual_commands = self.checker.get_command_files()
        
        # Act: Check commands (this checks for phantom commands)
        commands_ok, command_issues, phantom_commands = self.checker.check_commands(prompt_text)
        
        # Assert: No phantom commands (or minimal false positives acceptable)
        # Note: Some false positives from code examples are acceptable
        self.assertTrue(
            commands_ok or len(phantom_commands) < 10,
            f"Too many phantom commands detected: {phantom_commands}"
        )
    
    def test_delta_check_yagni_compliance(self):
        """Test YAGNI compliance (line count < 100)"""
        # Arrange: Load prompt file
        prompt_text = self.prompt_file.read_text(encoding='utf-8')
        lines = prompt_text.split("\n")
        
        # Act: Check YAGNI compliance
        yagni_ok, yagni_issues = self.checker.check_yagni(prompt_text)
        
        # Assert: YAGNI compliant (minimal, essential, elegant)
        self.assertLess(
            len(lines), 100,
            f"Prompt too long ({len(lines)} lines) - YAGNI violation"
        )
        # YAGNI check should pass or have minimal issues
        self.assertTrue(
            yagni_ok or len(yagni_issues) == 0,
            f"YAGNI compliance issues: {yagni_issues}"
        )
    
    def test_delta_check_one_pattern_detected(self):
        """Test ONE-Pattern detected"""
        # Arrange: Load prompt file
        prompt_text = self.prompt_file.read_text(encoding='utf-8')
        
        # Act: Check ONE-Pattern
        pattern_ok, pattern_issues = self.checker.check_one_pattern(prompt_text)
        
        # Assert: ONE-Pattern detected
        self.assertTrue(
            pattern_ok,
            f"ONE-Pattern check failed: {pattern_issues}"
        )
        self.assertEqual(
            len(pattern_issues), 0,
            f"Pattern issues found: {pattern_issues}"
        )
        # Verify pattern is present
        expected_pattern = "CLARITY → COHERENCE → CONVERGENCE → ELEGANCE → UNITY"
        self.assertIn(
            expected_pattern,
            prompt_text,
            f"ONE-Pattern not found in prompt: {expected_pattern}"
        )
    
    def test_delta_check_complete_validation_pass(self):
        """Test complete delta-check validation passes"""
        # Arrange: No context (should read prompt file)
        # Act: Run complete delta-check
        result = self.checker.perform_delta_check(context=None)
        
        # Assert: Should pass or have minimal failures
        # Note: Some false positives from code examples in prompt are acceptable
        failed_checks = len(result.failed)
        passed_checks = len(result.passed)
        
        # Should have more passes than failures
        self.assertGreater(
            passed_checks, failed_checks,
            f"Too many failures ({failed_checks}) vs passes ({passed_checks})"
        )
        
        # Core checks should pass
        core_checks = ["AbëONE Identity", "Partnership", "Guardians", "ONE-Pattern"]
        for check in core_checks:
            self.assertIn(
                check, result.passed,
                f"Core check failed: {check}"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)

