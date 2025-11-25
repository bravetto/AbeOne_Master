"""
Tests for AbëONE adapters.
"""

import pytest
from pathlib import Path
from adapters.kernel_adapter import KernelAdapter
from adapters.guardian_adapter import GuardianAdapter
from adapters.module_adapter import ModuleAdapter
from adapters.bus_adapter import BusAdapter


class TestKernelAdapter:
    """Test suite for KernelAdapter."""
    
    def test_kernel_adapter_initialization(self):
        """Test kernel adapter initializes correctly."""
        adapter = KernelAdapter()
        
        assert adapter is not None
        assert adapter.MODULE_ID == "marketing_automation_orbit"
        assert adapter.MODULE_NAME == "Marketing Automation Orbit"
        assert adapter._registered is False
        assert adapter._active is False
    
    def test_kernel_adapter_register_without_registry(self):
        """Test registration without registry (should handle gracefully)."""
        adapter = KernelAdapter()
        
        result = adapter.register()
        assert result is False  # Should return False when no registry
    
    def test_kernel_adapter_register_with_registry(self):
        """Test registration with mock registry."""
        mock_registry = type('MockRegistry', (), {
            'register_module': lambda self, module_id, name, version, capabilities: True
        })()
        
        adapter = KernelAdapter(module_registry=mock_registry)
        result = adapter.register()
        
        # Should succeed with registry
        assert result is True
        assert adapter._registered is True
    
    def test_kernel_adapter_activate(self):
        """Test kernel adapter activation."""
        adapter = KernelAdapter()
        
        result = adapter.activate()
        # Should handle gracefully even without lifecycle manager
        assert isinstance(result, bool)


class TestGuardianAdapter:
    """Test suite for GuardianAdapter."""
    
    def test_guardian_adapter_initialization(self):
        """Test guardian adapter initializes correctly."""
        adapter = GuardianAdapter()
        
        assert adapter is not None
    
    def test_guardian_adapter_validate(self):
        """Test guardian validation."""
        adapter = GuardianAdapter()
        
        test_data = {
            "strategy": {"name": "Test Strategy"},
            "action": "execute"
        }
        
        result = adapter.validate_with_guardians(test_data)
        
        assert isinstance(result, dict)
        assert "valid" in result
    
    def test_guardian_adapter_get_status(self):
        """Test getting guardian status."""
        adapter = GuardianAdapter()
        
        status = adapter.get_guardian_status()
        
        assert isinstance(status, dict)


class TestModuleAdapter:
    """Test suite for ModuleAdapter."""
    
    def test_module_adapter_initialization(self, config_path):
        """Test module adapter initializes correctly."""
        adapter = ModuleAdapter(config_path=config_path)
        
        assert adapter is not None
    
    def test_module_adapter_get_module_info(self, config_path):
        """Test getting module info."""
        adapter = ModuleAdapter(config_path=config_path)
        
        info = adapter.get_module_info()
        
        assert isinstance(info, dict)
        assert "module_id" in info or "module_name" in info
    
    def test_module_adapter_validate_dependencies(self, config_path):
        """Test dependency validation."""
        adapter = ModuleAdapter(config_path=config_path)
        
        deps = adapter.validate_dependencies()
        
        assert isinstance(deps, dict)
        assert "all_dependencies_met" in deps or "missing_packages" in deps


class TestBusAdapter:
    """Test suite for BusAdapter."""
    
    def test_bus_adapter_initialization(self):
        """Test bus adapter initializes correctly."""
        adapter = BusAdapter()
        
        assert adapter is not None
    
    def test_bus_adapter_publish_without_bus(self):
        """Test publishing without event bus (should handle gracefully)."""
        adapter = BusAdapter()
        
        # Should not raise error
        adapter.publish("test.event", {"data": "test"})
    
    def test_bus_adapter_subscribe(self):
        """Test event subscription."""
        adapter = BusAdapter()
        
        def handler(event):
            pass
        
        # Should not raise error
        adapter.subscribe("test.event", handler)

