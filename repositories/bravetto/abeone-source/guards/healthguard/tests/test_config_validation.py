"""
Tests for configuration validation functionality.
"""

import unittest
import tempfile
import os
import yaml
from unittest.mock import patch, mock_open
from src.poisonguard.config_validator import (
    ConfigValidator, validate_config, get_config_validation_report,
    PluginConfig, AnalyzerConfig, MitigatorConfig, LoggingConfig, DatabaseConfig, PoisonGuardConfig
)


class TestPluginConfig(unittest.TestCase):
    """Test plugin configuration validation."""
    
    def test_valid_plugin_config(self):
        """Test valid plugin configuration."""
        config = PluginConfig(
            name="keyword",
            **{"class": "heuristics.KeywordPlugin"},
            config={"keyword_list": ["bad", "evil"]}
        )
        
        self.assertEqual(config.name, "keyword")
        self.assertEqual(config.class_name, "heuristics.KeywordPlugin")
        self.assertEqual(config.config, {"keyword_list": ["bad", "evil"]})
    
    def test_invalid_plugin_name(self):
        """Test invalid plugin name."""
        with self.assertRaises(ValueError):
            PluginConfig(name="", class_name="test.Plugin", config={})
    
    def test_invalid_class_name(self):
        """Test invalid class name."""
        with self.assertRaises(ValueError):
            PluginConfig(name="test", **{"class": ""}, config={})
        
        with self.assertRaises(ValueError):
            PluginConfig(name="test", **{"class": "InvalidFormat"}, config={})


class TestAnalyzerConfig(unittest.TestCase):
    """Test analyzer configuration validation."""
    
    def test_valid_analyzer_config(self):
        """Test valid analyzer configuration."""
        plugins = [
            PluginConfig(name="keyword", **{"class": "heuristics.KeywordPlugin"}, config={}),
            PluginConfig(name="length", **{"class": "heuristics.LengthPlugin"}, config={})
        ]
        config = AnalyzerConfig(plugins=plugins)
        
        self.assertEqual(len(config.plugins), 2)
        self.assertEqual(config.plugins[0].name, "keyword")
        self.assertEqual(config.plugins[1].name, "length")
    
    def test_duplicate_plugin_names(self):
        """Test duplicate plugin names."""
        plugins = [
            PluginConfig(name="keyword", **{"class": "heuristics.KeywordPlugin"}, config={}),
            PluginConfig(name="keyword", **{"class": "heuristics.AnotherPlugin"}, config={})
        ]
        
        with self.assertRaises(ValueError):
            AnalyzerConfig(plugins=plugins)
    
    def test_empty_plugins_list(self):
        """Test empty plugins list."""
        config = AnalyzerConfig(plugins=[])
        self.assertEqual(len(config.plugins), 0)


class TestMitigatorConfig(unittest.TestCase):
    """Test mitigator configuration validation."""
    
    def test_valid_mitigator_config(self):
        """Test valid mitigator configuration."""
        config = MitigatorConfig(
            default_action="sanitize",
            sanitize_keywords=["bad", "evil"]
        )
        
        self.assertEqual(config.default_action, "sanitize")
        self.assertEqual(config.sanitize_keywords, ["bad", "evil"])
    
    def test_invalid_default_action(self):
        """Test invalid default action."""
        with self.assertRaises(ValueError):
            MitigatorConfig(default_action="invalid_action")
    
    def test_valid_actions(self):
        """Test all valid actions."""
        valid_actions = ["flag", "sanitize", "redact", "none"]
        for action in valid_actions:
            config = MitigatorConfig(default_action=action)
            self.assertEqual(config.default_action, action)
    
    def test_invalid_sanitize_keywords(self):
        """Test invalid sanitize keywords."""
        with self.assertRaises(ValueError):
            MitigatorConfig(sanitize_keywords="not_a_list")
        
        with self.assertRaises(ValueError):
            MitigatorConfig(sanitize_keywords=["", "valid"])


class TestLoggingConfig(unittest.TestCase):
    """Test logging configuration validation."""
    
    def test_valid_logging_config(self):
        """Test valid logging configuration."""
        config = LoggingConfig(
            version=1,
            disable_existing_loggers=False,
            formatters={"standard": {"format": "%(asctime)s - %(message)s"}},
            handlers={"console": {"class": "logging.StreamHandler"}},
            root={"level": "INFO", "handlers": ["console"]}
        )
        
        self.assertEqual(config.version, 1)
        self.assertFalse(config.disable_existing_loggers)
    
    def test_invalid_version(self):
        """Test invalid logging version."""
        with self.assertRaises(ValueError):
            LoggingConfig(version=2)


class TestDatabaseConfig(unittest.TestCase):
    """Test database configuration validation."""
    
    def test_valid_database_config(self):
        """Test valid database configuration."""
        config = DatabaseConfig(
            url="sqlite:///test.db",
            echo=False,
            pool_size=10,
            max_overflow=20
        )
        
        self.assertEqual(config.url, "sqlite:///test.db")
        self.assertFalse(config.echo)
        self.assertEqual(config.pool_size, 10)
        self.assertEqual(config.max_overflow, 20)
    
    def test_invalid_database_url(self):
        """Test invalid database URL."""
        with self.assertRaises(ValueError):
            DatabaseConfig(url="")
    
    def test_invalid_pool_size(self):
        """Test invalid pool size."""
        with self.assertRaises(ValueError):
            DatabaseConfig(pool_size=0)
        
        with self.assertRaises(ValueError):
            DatabaseConfig(pool_size=101)


class TestPoisonGuardConfig(unittest.TestCase):
    """Test main configuration validation."""
    
    def test_valid_full_config(self):
        """Test valid full configuration."""
        config = PoisonGuardConfig(
            analyzer=AnalyzerConfig(plugins=[]),
            mitigator=MitigatorConfig(),
            logging=LoggingConfig(),
            database=DatabaseConfig()
        )
        
        self.assertIsInstance(config.analyzer, AnalyzerConfig)
        self.assertIsInstance(config.mitigator, MitigatorConfig)
        self.assertIsInstance(config.logging, LoggingConfig)
        self.assertIsInstance(config.database, DatabaseConfig)
    
    def test_extra_fields_rejected(self):
        """Test that extra fields are rejected."""
        with self.assertRaises(ValueError):
            PoisonGuardConfig(
                analyzer=AnalyzerConfig(plugins=[]),
                mitigator=MitigatorConfig(),
                logging=LoggingConfig(),
                database=DatabaseConfig(),
                extra_field="should_be_rejected"
            )


class TestConfigValidator(unittest.TestCase):
    """Test configuration validator functionality."""
    
    def setUp(self):
        self.validator = ConfigValidator()
    
    def test_load_and_validate_success(self):
        """Test successful configuration loading and validation."""
        config_data = {
            "analyzer": {
                "plugins": [
                    {
                        "name": "keyword",
                        "class": "heuristics.KeywordPlugin",
                        "config": {"keyword_list": ["bad", "evil"]}
                    }
                ]
            },
            "mitigator": {
                "default_action": "flag",
                "sanitize_keywords": ["bad", "evil"]
            },
            "logging": {
                "version": 1,
                "disable_existing_loggers": False
            },
            "database": {
                "url": "sqlite:///test.db"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            config = self.validator.load_and_validate(config_path)
            self.assertIsInstance(config, PoisonGuardConfig)
            self.assertEqual(len(config.analyzer.plugins), 1)
            self.assertEqual(config.analyzer.plugins[0].name, "keyword")
        finally:
            os.unlink(config_path)
    
    def test_load_and_validate_file_not_found(self):
        """Test configuration loading with missing file."""
        with self.assertRaises(FileNotFoundError):
            self.validator.load_and_validate("nonexistent.yaml")
    
    def test_load_and_validate_invalid_yaml(self):
        """Test configuration loading with invalid YAML."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            config_path = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.validator.load_and_validate(config_path)
        finally:
            os.unlink(config_path)
    
    def test_load_and_validate_empty_file(self):
        """Test configuration loading with empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("")
            config_path = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.validator.load_and_validate(config_path)
        finally:
            os.unlink(config_path)
    
    def test_validate_plugin_configs(self):
        """Test plugin configuration validation."""
        # Set up validator with config
        self.validator.config = PoisonGuardConfig(
            analyzer=AnalyzerConfig(            plugins=[
                PluginConfig(
                    name="keyword",
                    **{"class": "heuristics.KeywordPlugin"},
                    config={"keyword_list": ["bad", "evil"]}
                ),
                PluginConfig(
                    name="length",
                    **{"class": "heuristics.LengthPlugin"},
                    config={"min_length": 10, "max_length": 100}
                ),
                PluginConfig(
                    name="model",
                    **{"class": "model.ModelPlugin"},
                    config={"model_name": "test-model", "toxicity_threshold": 0.9}
                )
            ]),
            mitigator=MitigatorConfig(),
            logging=LoggingConfig(),
            database=DatabaseConfig()
        )
        
        errors = self.validator.validate_plugin_configs()
        self.assertEqual(len(errors), 0)
    
    def test_validate_plugin_configs_with_errors(self):
        """Test plugin configuration validation with errors."""
        # Set up validator with invalid config
        self.validator.config = PoisonGuardConfig(
            analyzer=AnalyzerConfig(            plugins=[
                PluginConfig(
                    name="keyword",
                    **{"class": "heuristics.KeywordPlugin"},
                    config={}  # Missing keyword_list
                ),
                PluginConfig(
                    name="length",
                    **{"class": "heuristics.LengthPlugin"},
                    config={"min_length": 100, "max_length": 10}  # Invalid range
                ),
                PluginConfig(
                    name="model",
                    **{"class": "model.ModelPlugin"},
                    config={"model_name": "test-model", "toxicity_threshold": 1.5}  # Invalid threshold
                )
            ]),
            mitigator=MitigatorConfig(),
            logging=LoggingConfig(),
            database=DatabaseConfig()
        )
        
        errors = self.validator.validate_plugin_configs()
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("keyword_list" in error for error in errors))
        self.assertTrue(any("min_length" in error for error in errors))
        self.assertTrue(any("toxicity_threshold" in error for error in errors))
    
    def test_get_validation_summary(self):
        """Test validation summary generation."""
        # Test with no config
        summary = self.validator.get_validation_summary()
        self.assertFalse(summary["valid"])
        self.assertIn("No configuration loaded", summary["errors"])
        
        # Test with valid config
        self.validator.config = PoisonGuardConfig(
            analyzer=AnalyzerConfig(plugins=[]),
            mitigator=MitigatorConfig(),
            logging=LoggingConfig(),
            database=DatabaseConfig()
        )
        
        summary = self.validator.get_validation_summary()
        self.assertTrue(summary["valid"])
        self.assertEqual(len(summary["errors"]), 0)
        self.assertIn("No analysis plugins configured", summary["warnings"])


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_validate_config_function(self):
        """Test validate_config convenience function."""
        config_data = {
            "analyzer": {"plugins": []},
            "mitigator": {"default_action": "flag"},
            "logging": {"version": 1},
            "database": {"url": "sqlite:///test.db"}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            config = validate_config(config_path)
            self.assertIsInstance(config, PoisonGuardConfig)
        finally:
            os.unlink(config_path)
    
    def test_get_config_validation_report_function(self):
        """Test get_config_validation_report convenience function."""
        config_data = {
            "analyzer": {"plugins": []},
            "mitigator": {"default_action": "flag"},
            "logging": {"version": 1},
            "database": {"url": "sqlite:///test.db"}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            report = get_config_validation_report(config_path)
            self.assertIn("valid", report)
            self.assertIn("errors", report)
            self.assertIn("warnings", report)
        finally:
            os.unlink(config_path)
    
    def test_get_config_validation_report_invalid_file(self):
        """Test get_config_validation_report with invalid file."""
        report = get_config_validation_report("nonexistent.yaml")
        self.assertFalse(report["valid"])
        self.assertGreater(len(report["errors"]), 0)


if __name__ == '__main__':
    unittest.main()
