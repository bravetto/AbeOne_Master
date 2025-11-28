"""
Tests for Kernel Adapter

Pattern: TESTS × ADAPTER × KERNEL × ONE
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestKernelAdapter(unittest.TestCase):
    """Test Kernel Adapter functionality."""
    
    def test_adapter_import(self):
        """Test that adapter can be imported."""
        import importlib
        try:
            kernel_module = importlib.import_module('adapters.adapter.kernel')
            self.assertTrue(hasattr(kernel_module, 'get_kernel_adapter'))
        except ImportError as e:
            self.fail(f"Failed to import kernel adapter: {e}")
    
    def test_adapter_initialization(self):
        """Test adapter initialization."""
        import importlib
        kernel_module = importlib.import_module('adapters.adapter.kernel')
        adapter = kernel_module.get_kernel_adapter()
        self.assertIsNotNone(adapter)


if __name__ == '__main__':
    unittest.main()

