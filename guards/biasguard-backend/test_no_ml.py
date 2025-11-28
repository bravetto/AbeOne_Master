#!/usr/bin/env python3
"""
Test script to verify BiasGuard functionality without ML dependencies.
"""

import sys
import os

# Add the temp/src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'temp', 'src'))

from fastapi.testclient import TestClient
import yaml

def test_imports():
    """Test that core modules can be imported without ML dependencies."""
    print("=== Testing Imports (No ML Dependencies) ===")
    
    try:
        from poisonguard.core import DataSample, AnalysisResult
        print(" Core modules imported successfully")
    except ImportError as e:
        print(f" Failed to import core modules: {e}")
        return False
    
    try:
        from poisonguard.plugins.heuristics import KeywordPlugin, LengthPlugin
        print(" Heuristic plugins imported successfully")
    except ImportError as e:
        print(f" Failed to import heuristic plugins: {e}")
        return False
    
    try:
        from poisonguard.plugins.model import ModelPlugin, TRANSFORMERS_AVAILABLE
        print(f" ModelPlugin imported successfully (transformers available: {TRANSFORMERS_AVAILABLE})")
        if TRANSFORMERS_AVAILABLE:
            print("  WARNING: transformers is available, but should not be for this test")
            return False
        else:
            print("   Correctly detects transformers is NOT available")
    except ImportError as e:
        print(f" Failed to import ModelPlugin: {e}")
        return False
    
    return True

def test_plugins():
    """Test that plugins work without ML dependencies."""
    print("\n=== Testing Plugins ===")
    
    from poisonguard.core import DataSample
    from poisonguard.plugins.heuristics import KeywordPlugin, LengthPlugin
    
    # Test KeywordPlugin
    try:
        keyword_config = {"keyword_list": ["exploit", "malicious"]}
        keyword_plugin = KeywordPlugin(keyword_config)
        
        clean_sample = DataSample(id="test-1", content="This is a clean sample.")
        result = keyword_plugin.analyze(clean_sample)
        assert not result.is_poisoned, "Clean sample should not be flagged"
        print(" KeywordPlugin: Clean sample correctly identified")
        
        poisoned_sample = DataSample(id="test-2", content="This contains exploit code.")
        result = keyword_plugin.analyze(poisoned_sample)
        assert result.is_poisoned, "Poisoned sample should be flagged"
        print(" KeywordPlugin: Poisoned sample correctly flagged")
    except Exception as e:
        print(f" KeywordPlugin test failed: {e}")
        return False
    
    # Test LengthPlugin
    try:
        length_config = {"min_length": 10, "max_length": 100}
        length_plugin = LengthPlugin(length_config)
        
        short_sample = DataSample(id="test-3", content="Short")
        result = length_plugin.analyze(short_sample)
        assert result.is_poisoned, "Short sample should be flagged"
        print(" LengthPlugin: Short sample correctly flagged")
        
        valid_sample = DataSample(id="test-4", content="This is a valid length sample.")
        result = length_plugin.analyze(valid_sample)
        assert not result.is_poisoned, "Valid length sample should not be flagged"
        print(" LengthPlugin: Valid length sample correctly identified")
    except Exception as e:
        print(f" LengthPlugin test failed: {e}")
        return False
    
    # Test ModelPlugin fails gracefully
    try:
        from poisonguard.plugins.model import ModelPlugin
        model_config = {"model_name": "test-model", "toxicity_threshold": 0.9}
        try:
            model_plugin = ModelPlugin(model_config)
            print(" ModelPlugin should fail without transformers")
            return False
        except ImportError as e:
            print(f" ModelPlugin correctly fails without transformers: {e}")
    except Exception as e:
        print(f" ModelPlugin test failed: {e}")
        return False
    
    return True

def test_analyzer():
    """Test that Analyzer works with config without model plugin."""
    print("\n=== Testing Analyzer ===")
    
    try:
        from poisonguard.analyzer import Analyzer
        from poisonguard.core import DataSample
        
        # Load config without model plugin
        config = {
            'analyzer': {
                'plugins': [
                    {
                        'name': 'keyword',
                        'class': 'heuristics.KeywordPlugin',
                        'config': {'keyword_list': ['exploit', 'malicious']}
                    },
                    {
                        'name': 'length',
                        'class': 'heuristics.LengthPlugin',
                        'config': {'min_length': 10, 'max_length': 1000}
                    }
                ]
            }
        }
        
        analyzer = Analyzer(config)
        print(f" Analyzer initialized with {len(analyzer.plugins)} plugins")
        
        # Test analysis
        samples = [
            DataSample(id="test-1", content="This is a clean sample for testing."),
            DataSample(id="test-2", content="This contains exploit code.")
        ]
        
        results = analyzer.analyze(samples)
        assert len(results) == 2, "Should return 2 results"
        assert not results[0].is_poisoned, "First sample should be clean"
        assert results[1].is_poisoned, "Second sample should be flagged"
        print(" Analyzer correctly processes samples")
        print(f"  - Sample 1: {'POISONED' if results[0].is_poisoned else 'CLEAN'}")
        print(f"  - Sample 2: {'POISONED' if results[1].is_poisoned else 'CLEAN'}")
        
    except Exception as e:
        print(f" Analyzer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_config_loading():
    """Test that config.yaml loads correctly without model plugin."""
    print("\n=== Testing Config Loading ===")
    
    try:
        import yaml
        config_path = 'config.yaml'
        if not os.path.exists(config_path):
            print(f" Config file not found at {config_path}, skipping")
            return True
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        plugins = config.get('analyzer', {}).get('plugins', [])
        model_plugin_enabled = any(p.get('class') == 'model.ModelPlugin' for p in plugins)
        
        if model_plugin_enabled:
            print(" Model plugin is still enabled in config.yaml")
            return False
        else:
            print(" Config correctly has model plugin disabled")
            print(f"  - Active plugins: {[p.get('name') for p in plugins]}")
        
    except Exception as e:
        print(f" Config loading test failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("BiasGuard Functionality Test (Without ML Dependencies)\n")
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Plugins", test_plugins()))
    results.append(("Analyzer", test_analyzer()))
    results.append(("Config Loading", test_config_loading()))
    
    print("\n=== Test Summary ===")
    for name, passed in results:
        status = " PASSED" if passed else " FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n SUCCESS: All tests passed! BiasGuard works without ML dependencies.")
        sys.exit(0)
    else:
        print("\n FAILURE: Some tests failed.")
        sys.exit(1)

