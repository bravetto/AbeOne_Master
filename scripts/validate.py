#!/usr/bin/env python3
"""Simple validation - YAGNI simplified"""
import urllib.request
from pathlib import Path

workspace = Path(__file__).parent.parent
passed = 0
total = 0

# Check app
total += 1
try:
    urllib.request.urlopen("http://localhost:53009/", timeout=2)
    print("✅ App running")
    passed += 1
except:
    print("❌ App not running")

# Check recipients config
total += 1
config_file = workspace / "scripts" / "recipients_config.py"
if config_file.exists():
    print("✅ Recipients config exists")
    passed += 1
    # Check if configured
    if '"email": None' in config_file.read_text():
        print("⚠️  Add emails to recipients_config.py")
else:
    print("❌ Recipients config missing")

# Check component
total += 1
component = workspace / "abeone_app" / "lib" / "substrate" / "molecules" / "shiny_happy_people.dart"
if component.exists():
    print("✅ Component exists")
    passed += 1
else:
    print("❌ Component missing")

print(f"\n{passed}/{total} passed\n∞ AbëONE ∞")

