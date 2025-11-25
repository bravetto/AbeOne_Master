#!/usr/bin/env python3
"""
Python Constants Generator
Generates Python constants from design tokens

Usage: python3 generate-python.py [output-path]
Default output: ../../design-system/generated/design_tokens.py
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Load design tokens
script_dir = Path(__file__).parent
tokens_path = script_dir / '../tokens/abeone-design-tokens.json'

with open(tokens_path, 'r', encoding='utf-8') as f:
    tokens = json.load(f)

def generate_python_constants():
    """Generate Python constants from design tokens"""
    
    content = f'''"""
AbëONE Design System - Python Constants
Generated from design-system/tokens/abeone-design-tokens.json
DO NOT EDIT MANUALLY - Run: python3 design-system/generators/generate-python.py
Generated: {datetime.now().isoformat()}
"""

from typing import Dict, List, TypedDict

# Meta Information
META_NAME = "{tokens['meta']['name']}"
META_VERSION = "{tokens['meta']['version']}"
META_DESCRIPTION = "{tokens['meta']['description']}"
META_CREATED = "{tokens['meta']['created']}"
META_GUARDIANS = {tokens['meta']['guardians']}

# Colors - Heart (Red)
HEART_COLORS = {{
'''
    
    # Heart colors
    for key, value in tokens['colors']['heart'].items():
        if key not in ['semantic', 'usage']:
            content += f'    "{key}": "{value}",\n'
    
    content += f'''}}
HEART_SEMANTIC = "{tokens['colors']['heart']['semantic']}"
HEART_USAGE = "{tokens['colors']['heart']['usage']}"

# Colors - Lux (Purple)
LUX_COLORS = {{
'''
    
    for key, value in tokens['colors']['lux'].items():
        if key not in ['semantic', 'usage']:
            content += f'    "{key}": "{value}",\n'
    
    content += f'''}}
LUX_SEMANTIC = "{tokens['colors']['lux']['semantic']}"
LUX_USAGE = "{tokens['colors']['lux']['usage']}"

# Colors - Warm (Orange)
WARM_COLORS = {{
'''
    
    for key, value in tokens['colors']['warm'].items():
        if key not in ['semantic', 'usage']:
            content += f'    "{key}": "{value}",\n'
    
    content += f'''}}
WARM_SEMANTIC = "{tokens['colors']['warm']['semantic']}"
WARM_USAGE = "{tokens['colors']['warm']['usage']}"

# Colors - Peace (Green)
PEACE_COLORS = {{
'''
    
    for key, value in tokens['colors']['peace'].items():
        if key not in ['semantic', 'usage']:
            content += f'    "{key}": "{value}",\n'
    
    content += f'''}}
PEACE_SEMANTIC = "{tokens['colors']['peace']['semantic']}"
PEACE_USAGE = "{tokens['colors']['peace']['usage']}"

# Colors - Neutral
NEUTRAL_COLORS = {{
'''
    
    for key, value in tokens['colors']['neutral'].items():
        if key not in ['semantic', 'usage']:
            content += f'    "{key}": "{value}",\n'
    
    content += f'''}}
NEUTRAL_SEMANTIC = "{tokens['colors']['neutral']['semantic']}"
NEUTRAL_USAGE = "{tokens['colors']['neutral']['usage']}"

# Typography - Font Families
FONT_SANS = {tokens['typography']['fonts']['sans']['family']}
FONT_SANS_WEIGHTS = {tokens['typography']['fonts']['sans']['weights']}
FONT_SANS_USAGE = "{tokens['typography']['fonts']['sans']['usage']}"
FONT_SANS_GOOGLE = "{tokens['typography']['fonts']['sans']['googleFont']}"

FONT_SERIF = {tokens['typography']['fonts']['serif']['family']}
FONT_SERIF_WEIGHTS = {tokens['typography']['fonts']['serif']['weights']}
FONT_SERIF_USAGE = "{tokens['typography']['fonts']['serif']['usage']}"
FONT_SERIF_GOOGLE = "{tokens['typography']['fonts']['serif']['googleFont']}"

FONT_DISPLAY = {tokens['typography']['fonts']['display']['family']}
FONT_DISPLAY_WEIGHTS = {tokens['typography']['fonts']['display']['weights']}
FONT_DISPLAY_USAGE = "{tokens['typography']['fonts']['display']['usage']}"
FONT_DISPLAY_GOOGLE = "{tokens['typography']['fonts']['display']['googleFont']}"

# Typography - Font Sizes
FONT_SIZES = {{
'''
    
    for key, value in tokens['typography']['scale'].items():
        content += f'    "{key}": "{value}",\n'
    
    content += '''}

# Typography - Line Heights
LINE_HEIGHTS = {
'''
    
    for key, value in tokens['typography']['lineHeight'].items():
        content += f'    "{key}": "{value}",\n'
    
    content += '''}

# Spacing
SPACING = {
'''
    
    for key, value in tokens['spacing']['scale'].items():
        content += f'    "{key}": "{value}",\n'
    
    content += '''}

# Border Radius
BORDER_RADIUS = {
'''
    
    for key, value in tokens['borderRadius'].items():
        content += f'    "{key}": "{value}",\n'
    
    content += '''}

# Shadows
SHADOWS = {
'''
    
    for key, value in tokens['shadows'].items():
        # Escape quotes in shadow values
        escaped_value = value.replace('"', '\\"')
        content += f'    "{key}": "{escaped_value}",\n'
    
    content += '''}

# Gradients
GRADIENT_HEALING = "''' + tokens['gradients']['healing']['css'] + '''"
GRADIENT_LUX = "''' + tokens['gradients']['lux']['css'] + '''"
GRADIENT_SIDEBAR = "''' + tokens['gradients']['sidebar']['css'] + '''"
GRADIENT_TEXT_HEALING = "''' + tokens['gradients']['textHealing']['css'] + '''"

# Breakpoints
BREAKPOINTS = {
'''
    
    for key, value in tokens['breakpoints'].items():
        content += f'    "{key}": "{value}",\n'
    
    content += '''}

# Helper Functions
def get_color(color_name: str, shade: str = "500") -> str:
    """Get color value by name and shade"""
    color_map = {
        "heart": HEART_COLORS,
        "lux": LUX_COLORS,
        "warm": WARM_COLORS,
        "peace": PEACE_COLORS,
        "neutral": NEUTRAL_COLORS,
    }
    return color_map.get(color_name, {}).get(shade, "")

def get_gradient(gradient_name: str) -> str:
    """Get gradient CSS by name"""
    gradient_map = {
        "healing": GRADIENT_HEALING,
        "lux": GRADIENT_LUX,
        "sidebar": GRADIENT_SIDEBAR,
        "text_healing": GRADIENT_TEXT_HEALING,
    }
    return gradient_map.get(gradient_name, "")

def get_spacing(size: str) -> str:
    """Get spacing value by size"""
    return SPACING.get(size, size)

def get_font_size(size: str) -> str:
    """Get font size by size name"""
    return FONT_SIZES.get(size, "1rem")

def get_breakpoint(size: str) -> str:
    """Get breakpoint value by size"""
    return BREAKPOINTS.get(size, "")
'''
    
    return content

# Write output
output_path = sys.argv[1] if len(sys.argv) > 1 else script_dir / '../generated/design_tokens.py'
output_content = generate_python_constants()

# Ensure directory exists
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(output_content)

print(f"✅ Generated Python constants: {output_path}")

