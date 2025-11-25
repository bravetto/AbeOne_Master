#!/usr/bin/env python3
"""
AEYON Atomic Execution: Convergence Essential Actions
Moves root .md files to docs/ hierarchy atomically
"""

import os
import shutil
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
ROOT_MD_FILES = list(ROOT.glob("*.md"))

# Categorization patterns
CATEGORIES = {
    "architecture": ["ARCHITECTURE", "ARCHITECT", "SYSTEM", "DESIGN", "PATTERN", "ORBIT", "GUARDIAN", "EMERGENT", "KERNEL"],
    "status": ["STATUS", "COMPLETE", "VALIDATION", "REPORT", "ANALYSIS", "CONVERGENCE", "EMERGENCE"],
    "reference": ["REFERENCE", "GUIDE", "API", "ENDPOINT", "MAP"],
    "deployment": ["DEPLOY", "DEPLOYMENT", "AWS", "KUBERNETES", "DOCKER", "ECR", "VERCEL"],
    "workflow": ["WORKFLOW", "CI", "CD", "GITHUB", "ACTIONS"],
    "product": ["PRODUCT", "ABE", "ABEFLOWS", "ABEBEATS", "ABEDESKS", "ABECODES"],
    "marketing": ["MARKETING", "WEBINAR", "CAMPAIGN", "SALES"],
    "security": ["SECURITY", "SECURE", "AUTH", "GUARD", "TRUST"],
    "testing": ["TEST", "TESTING", "VALIDATION", "VERIFY"],
    "documentation": ["DOCUMENTATION", "DOCS", "README", "GUIDE"],
}

def categorize_file(filename):
    """Categorize file based on name patterns"""
    filename_upper = filename.upper()
    
    for category, patterns in CATEGORIES.items():
        if any(pattern in filename_upper for pattern in patterns):
            return category
    
    # Default categorization
    if "AEYON" in filename_upper or "ZERO" in filename_upper or "JOHN" in filename_upper:
        return "status"
    if "CONVERGENCE" in filename_upper or "EMERGENCE" in filename_upper:
        return "status"
    if "FLOW" in filename_upper or "YAGNI" in filename_upper:
        return "status"
    
    return "reference"  # Default fallback

def execute_atomic():
    """Execute atomic convergence actions"""
    print("🔥 AEYON ATOMIC EXECUTION: CONVERGENCE ESSENTIAL")
    print("=" * 60)
    
    # Action 1: Ensure directory structure
    print("\n✅ ACTION 1: Ensuring directory structure...")
    dirs = ["docs/status/convergence", "docs/reference/convergence", "docs/architecture/convergence"]
    for dir_path in dirs:
        (ROOT / dir_path).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {dir_path}")
    
    # Action 2: Categorize and move files
    print(f"\n✅ ACTION 2: Moving {len(ROOT_MD_FILES)} root .md files...")
    
    moved = defaultdict(list)
    skipped = []
    
    for md_file in ROOT_MD_FILES:
        # Skip README.md and PROJECT_MASTER_INDEX.md
        if md_file.name in ["README.md", "PROJECT_MASTER_INDEX.md", "CHANGELOG.md"]:
            skipped.append(md_file.name)
            continue
        
        category = categorize_file(md_file.name)
        target_dir = DOCS / category / "convergence"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target = target_dir / md_file.name
        
        # Handle duplicates
        if target.exists():
            # Add timestamp suffix
            stem = md_file.stem
            suffix = md_file.suffix
            counter = 1
            while target.exists():
                target = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1
        
        shutil.move(str(md_file), str(target))
        moved[category].append(md_file.name)
        print(f"   ✓ {md_file.name} → docs/{category}/convergence/")
    
    # Action 3: Update .project-boundary
    print("\n✅ ACTION 3: Updating .project-boundary...")
    boundary_file = ROOT / ".project-boundary"
    
    with open(boundary_file, 'r') as f:
        boundary = json.load(f)
    
    boundary["organizationalStrategy"] = "ONE_PATTERN"
    boundary["convergenceState"] = "IN_PROGRESS"
    boundary["lastUpdated"] = "2025-01-27"
    boundary["rootMdFilesMoved"] = len(ROOT_MD_FILES) - len(skipped)
    
    with open(boundary_file, 'w') as f:
        json.dump(boundary, f, indent=2)
    
    print(f"   ✓ Updated .project-boundary")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 ATOMIC EXECUTION COMPLETE")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   • Files moved: {len(ROOT_MD_FILES) - len(skipped)}")
    print(f"   • Files skipped: {len(skipped)} ({', '.join(skipped)})")
    print(f"\n📁 Categories:")
    for category, files in moved.items():
        print(f"   • {category}: {len(files)} files")
    
    print(f"\n✅ Convergence state: IN_PROGRESS")
    print(f"✅ Organizational strategy: ONE_PATTERN")
    
    return True

if __name__ == "__main__":
    try:
        execute_atomic()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise

