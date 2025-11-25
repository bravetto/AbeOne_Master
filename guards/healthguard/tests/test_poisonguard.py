import unittest
import sys
import os
import yaml
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.poisonguard import __version__
from src.poisonguard.core import DataSample, AnalysisResult
from src.poisonguard.analyzer import Analyzer
from src.poisonguard.mitigator import Mitigator
from src.poisonguard.logger import setup_logging


class TestPoisonGuard(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, "0.3.0")


class TestAnalyzerWithPlugins(unittest.TestCase):
    def setUp(self):
        self.config = {
            'analyzer': {
                'plugins': [
                    {
                        'name': 'keyword',
                        'class': 'heuristics.KeywordPlugin',
                        'config': {'keyword_list': ['bad', 'wrong']}
                    },
                    {
                        'name': 'length',
                        'class': 'heuristics.LengthPlugin',
                        'config': {'min_length': 10, 'max_length': 50}
                    },
                    {
                        'name': 'model',
                        'class': 'model.ModelPlugin',
                        'config': {
                            'model_name': 'distilbert-base-uncased-finetuned-sst-2-english',
                            'toxicity_threshold': 0.9
                        }
                    }
                ]
            }
        }
        self.analyzer = Analyzer(self.config)

    def test_clean_sample(self):
        samples = [DataSample(id="1", content="This is a perfectly fine sentence.")]
        results = self.analyzer.analyze(samples)
        self.assertFalse(results[0].is_poisoned)

    def test_poisoned_by_keyword_plugin(self):
        samples = [DataSample(id="2", content="This sentence has a bad word.")]
        results = self.analyzer.analyze(samples)
        self.assertTrue(results[0].is_poisoned)
        self.assertTrue(any("keywords" in reason for reason in results[0].details.get('reasons', [])))

    def test_poisoned_by_length_plugin(self):
        samples = [DataSample(id="3", content="Too short")]
        results = self.analyzer.analyze(samples)
        self.assertTrue(results[0].is_poisoned)
        self.assertTrue(any("length" in reason for reason in results[0].details.get('reasons', [])))

    def test_poisoned_by_model_plugin(self):
        samples = [DataSample(id="5", content="I hate this, it's the worst.")]
        results = self.analyzer.analyze(samples)
        self.assertTrue(results[0].is_poisoned)
        self.assertTrue(any("toxicity" in reason for reason in results[0].details.get('reasons', [])))


class TestAnalyzerEdgeCases(unittest.TestCase):
    def setUp(self):
        self.config = {'analyzer': {'plugins': []}}
        self.analyzer = Analyzer(self.config)

    def test_no_plugins_loaded(self):
        samples = [DataSample(id="1", content="This is a test.")]
        results = self.analyzer.analyze(samples)
        self.assertFalse(results[0].is_poisoned)

    def test_non_string_content(self):
        samples = [DataSample(id="1", content=123)]
        results = self.analyzer.analyze(samples)
        self.assertFalse(results[0].is_poisoned)

    def test_empty_samples_list(self):
        results = self.analyzer.analyze([])
        self.assertEqual(len(results), 0)


class TestMitigatorAdvanced(unittest.TestCase):
    def setUp(self):
        self.samples = [DataSample(id="1", content="This is a malicious sentence.")]
        self.analysis_results = [
            AnalysisResult(sample_id="1", is_poisoned=True, confidence=0.9, details={'reasons': ['keyword']})
        ]

    def test_flag_action(self):
        config = {'mitigator': {'default_action': 'flag'}}
        mitigator = Mitigator(config)
        actions = mitigator.mitigate(self.samples, self.analysis_results)
        self.assertEqual(actions[0].action_taken, "flag")

    def test_sanitize_action(self):
        config = {'mitigator': {'default_action': 'sanitize', 'sanitize_keywords': ['malicious']}}
        mitigator = Mitigator(config)
        actions = mitigator.mitigate(self.samples, self.analysis_results)
        self.assertEqual(actions[0].action_taken, "sanitize")
        self.assertNotIn("malicious", actions[0].details.get('sanitized_content', ''))

    def test_sanitize_action_case_insensitive(self):
        samples = [DataSample(id="1", content="This is a Malicious sentence.")]
        analysis_results = [
            AnalysisResult(sample_id="1", is_poisoned=True, confidence=0.9, details={'reasons': ['keyword']})
        ]
        config = {'mitigator': {'default_action': 'sanitize', 'sanitize_keywords': ['malicious']}}
        mitigator = Mitigator(config)
        actions = mitigator.mitigate(samples, analysis_results)
        self.assertEqual(actions[0].action_taken, "sanitize")
        self.assertEqual(actions[0].details.get('sanitized_content'), "This is a [SANITIZED] sentence.")

    def test_redact_action(self):
        config = {'mitigator': {'default_action': 'redact'}}
        mitigator = Mitigator(config)
        actions = mitigator.mitigate(self.samples, self.analysis_results)
        self.assertEqual(actions[0].action_taken, "redact")
        self.assertEqual(actions[0].details.get('redacted_content_preview'), "[REDACTED]")


class TestLogging(unittest.TestCase):
    def test_logging_setup(self):
        # Create a dummy config with logging
        with open("test_config.yaml", "w") as f:
            yaml.dump({
                "logging": {
                    "version": 1,
                    "handlers": {"null": {"class": "logging.NullHandler"}},
                    "root": {"level": "DEBUG", "handlers": ["null"]},
                }
            }, f)

        setup_logging("test_config.yaml")
        # Check that the root logger has a NullHandler
        self.assertIsInstance(logging.getLogger().handlers[0], logging.NullHandler)
        os.remove("test_config.yaml")

if __name__ == '__main__':
    unittest.main()