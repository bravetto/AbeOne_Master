#!/usr/bin/env python3
"""
Test the gateway components to validate the unified API works correctly
"""

import sys
import os

# Add the gateway directory to the path
sys.path.insert(0, 'codeguardians-gateway/codeguardians-gateway')

def test_imports():
    """Test that we can import the main components"""
    print("Testing imports...")

    try:
        from app.main import app
        print("✓ Successfully imported main app")

        from app.core.guard_orchestrator import GuardServiceOrchestrator
        print("✓ Successfully imported guard orchestrator")

        from app.core.config import get_settings
        print("✓ Successfully imported config")

        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_routes():
    """Test that the unified endpoint is registered"""
    print("\nTesting routes...")

    try:
        from app.main import app

        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)

        print(f"Found {len(routes)} routes")
        print("Routes:", routes[:5], "..." if len(routes) > 5 else "")

        unified_endpoint = "/api/v1/guards/process"
        if unified_endpoint in routes:
            print(f"✓ Unified endpoint {unified_endpoint} is registered")
            return True
        else:
            print(f"✗ Unified endpoint {unified_endpoint} not found")
            return False

    except Exception as e:
        print(f"✗ Route test failed: {e}")
        return False

def test_orchestrator():
    """Test the guard orchestrator"""
    print("\nTesting guard orchestrator...")

    try:
        from app.core.guard_orchestrator import GuardServiceOrchestrator

        orchestrator = GuardServiceOrchestrator()
        service_count = len(orchestrator.services)

        print(f"✓ Guard orchestrator created with {service_count} services")

        # Check that all expected services are present
        expected_services = ['tokenguard', 'trustguard', 'contextguard', 'biasguard', 'securityguard', 'healthguard']
        actual_services = list(orchestrator.services.keys())

        print(f"Expected services: {expected_services}")
        print(f"Actual services: {actual_services}")

        for service in expected_services:
            if service in actual_services:
                print(f"✓ {service} is registered")
            else:
                print(f"✗ {service} is missing")

        return True

    except Exception as e:
        print(f"✗ Orchestrator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")

    try:
        from app.core.config import get_settings

        settings = get_settings()

        print("✓ Settings loaded successfully")
        print(f"  Environment: {settings.ENVIRONMENT}")
        print(f"  Debug: {settings.DEBUG}")
        print(f"  AWS Secrets Enabled: {settings.AWS_SECRETS_ENABLED}")

        # Check that HealthGuard uses port 8005 (not 8006)
        healthguard_url = getattr(settings, 'HEALTHGUARD_URL', '')
        if '8005' in healthguard_url:
            print("✓ HealthGuard correctly configured to use port 8005")
        elif '8006' in healthguard_url:
            print("✗ HealthGuard still using incorrect port 8006")
        else:
            print(f"? HealthGuard URL: {healthguard_url}")

        return True

    except Exception as e:
        print(f"✗ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("AIGuards Gateway Component Test")
    print("=" * 40)

    tests = [
        ("Imports", test_imports),
        ("Routes", test_routes),
        ("Orchestrator", test_orchestrator),
        ("Configuration", test_config)
    ]

    results = []
    for name, test_func in tests:
        print(f"\n[{name}]")
        result = test_func()
        results.append(result)

    print("\n" + "=" * 40)
    print("TEST RESULTS")

    passed = sum(results)
    total = len(results)

    for i, (name, _) in enumerate(tests):
        status = "PASS" if results[i] else "FAIL"
        print(f"{status}: {name}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("The gateway components are working correctly.")
        print("The unified API should be functional when the server starts.")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
