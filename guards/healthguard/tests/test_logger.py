import unittest
import logging
import os
import yaml
from unittest.mock import patch, mock_open
from poisonguard.logger import setup_logging


class TestLogger(unittest.TestCase):
    def test_setup_logging_with_valid_config(self):
        config = {
            'logging': {
                'version': 1,
                'handlers': {
                    'console': {
                        'class': 'logging.StreamHandler',
                        'level': 'DEBUG',
                    },
                },
                'root': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                },
            }
        }
        m = mock_open(read_data=yaml.dump(config))
        with patch('builtins.open', m):
            setup_logging()

    def test_setup_logging_with_missing_logging_config(self):
        config = {}
        m = mock_open(read_data=yaml.dump(config))
        with patch('builtins.open', m):
            with self.assertLogs('root', level='INFO') as cm:
                setup_logging()
                self.assertEqual(len(cm.output), 1)
                self.assertIn("Logging configuration not found. Using basic configuration.", cm.output[0])

    def test_setup_logging_with_file_not_found(self):
        with patch('builtins.open', mock_open()) as m:
            m.side_effect = FileNotFoundError
            with self.assertLogs('root', level='INFO') as cm:
                setup_logging()
                self.assertEqual(len(cm.output), 1)
                self.assertIn("Configuration file not found. Using basic logging configuration.", cm.output[0])

    def test_setup_logging_with_other_exception(self):
        with patch('builtins.open', mock_open()) as m:
            m.side_effect = Exception("Test exception")
            with self.assertLogs('root', level='ERROR') as cm:
                setup_logging()
                self.assertEqual(len(cm.output), 1)
                self.assertIn("Error loading logging configuration: Test exception", cm.output[0])