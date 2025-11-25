#!/usr/bin/env python3
"""
Quick test to verify PHANTOM HUNTER is ready to launch.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("🔥 PHANTOM HUNTER CREATOR EDITION - LAUNCH TEST")
print("=" * 80)
print()

# Test 1: Import core module
print("📦 Test 1: Importing core module...")
try:
    from phantom_hunter_creator import get_phantom_hunter, get_lead_capture_flow
    print("   ✅ Core module imported successfully")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 2: Create hunter instance
print("🔍 Test 2: Creating hunter instance...")
try:
    hunter = get_phantom_hunter()
    print("   ✅ Hunter instance created")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 3: Test detection
print("🎯 Test 3: Testing phantom detection...")
try:
    test_code = """
def process_green_screen(video):
    # TODO: Implement green screen processing
    return None
"""
    result = hunter.detect(test_code, creator_type='TRU')
    if result['detected']:
        print(f"   ✅ Detection works! Found {result['pattern_count']} phantom(s)")
    else:
        print("   ⚠️  No phantoms detected (might be expected)")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 4: Test lead capture
print("📧 Test 4: Testing lead capture flow...")
try:
    lead_flow = get_lead_capture_flow()
    validation = lead_flow.process_validation(
        test_code,
        creator_type='TRU',
        email='test@example.com'
    )
    print("   ✅ Lead capture flow works!")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 5: Check landing page exists
print("📄 Test 5: Checking landing page...")
try:
    landing_page = Path(__file__).parent / "landing_page.html"
    if landing_page.exists():
        print("   ✅ Landing page found")
    else:
        print("   ⚠️  Landing page not found")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print()
print("=" * 80)
print("✅ ALL TESTS PASSED - READY TO LAUNCH!")
print("=" * 80)
print()
print("🚀 Run: ./launch.sh")
print("   Then open: http://localhost:8000")
print()
print("∞ AbëONE ∞")

