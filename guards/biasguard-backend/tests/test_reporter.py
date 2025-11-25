import unittest
from poisonguard.core import AnalysisResult, MitigationAction, Report
from poisonguard.reporter import Reporter


class TestReporter(unittest.TestCase):
    def setUp(self):
        self.reporter = Reporter()

    def test_generate_report(self):
        analysis_results = [
            AnalysisResult(sample_id='1', is_poisoned=True, confidence=0.9, details={'reasons': ['High toxicity']}),
            AnalysisResult(sample_id='2', is_poisoned=False, confidence=0.1, details={}),
        ]
        mitigation_actions = [
            MitigationAction(sample_id='1', action_taken='blocked', details={'reasons': ['High toxicity']}),
            MitigationAction(sample_id='2', action_taken='none', details={}),
        ]

        report = self.reporter.generate_report(analysis_results, mitigation_actions)

        self.assertIsInstance(report, Report)
        self.assertEqual(report.total_samples, 2)
        self.assertEqual(report.poisoned_samples, 1)
        self.assertEqual(report.mitigated_samples, 1)
        self.assertEqual(report.analysis_results, analysis_results)
        self.assertEqual(report.mitigation_actions, mitigation_actions)

    def test_format_report(self):
        report = Report(
            total_samples=2,
            poisoned_samples=1,
            mitigated_samples=1,
            analysis_results=[
                AnalysisResult(sample_id='1', is_poisoned=True, confidence=0.9, details={'reasons': ['High toxicity']}),
                AnalysisResult(sample_id='2', is_poisoned=False, confidence=0.1, details={}),
            ],
            mitigation_actions=[
                MitigationAction(sample_id='1', action_taken='blocked', details={'reasons': ['High toxicity']}),
                MitigationAction(sample_id='2', action_taken='none', details={}),
            ],
        )

        formatted_report = self.reporter.format_report(report)

        self.assertIn("--- PoisonGuard Analysis Report ---", formatted_report)
        self.assertIn("Total Samples Analyzed: 2", formatted_report)
        self.assertIn("Potentially Poisoned Samples Detected: 1", formatted_report)
        self.assertIn("Samples Mitigated: 1", formatted_report)
        self.assertIn("Sample ID: 1 | Status: Poisoned | Confidence: 0.90", formatted_report)
        self.assertIn("Details: High toxicity", formatted_report)
        self.assertIn("Sample ID: 1 | Action: blocked", formatted_report)
        self.assertIn("Reason: High toxicity", formatted_report)
        self.assertIn("--- End of Report ---", formatted_report)

    def test_format_report_no_mitigation(self):
        report = Report(
            total_samples=1,
            poisoned_samples=0,
            mitigated_samples=0,
            analysis_results=[
                AnalysisResult(sample_id='1', is_poisoned=False, confidence=0.1, details={}),
            ],
            mitigation_actions=[
                MitigationAction(sample_id='1', action_taken='none', details={}),
            ],
        )

        formatted_report = self.reporter.format_report(report)

        self.assertNotIn("--- Mitigation Actions ---", formatted_report)