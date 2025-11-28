#!/usr/bin/env python3
import subprocess
import os
import sys

os.chdir('/Users/michaelmataluni/Documents/AbeOne_Master')

def run_cmd(cmd, check=True):
    """Run a command and return the result"""
    print(f" Running: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"  {result.stderr}", file=sys.stderr)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f" Error: {e}", file=sys.stderr)
        return False

# Remove lock file
print(" Removing lock files...")
run_cmd("rm -f .git/index.lock", check=False)

# Stage files in batches
print("\n Staging files...")
dirs_to_stage = [
    ".abeone_memory", ".ai-context-source-of-truth.json", ".cursor", 
    ".cursorignore", ".cursorrules", "docs", "marketing", "products", 
    "scripts", "orbital", "atomic", "kernel", "protocol", "infra",
    "design-system", "templates"
]

for dir_path in dirs_to_stage:
    if os.path.exists(dir_path):
        run_cmd(f"git add {dir_path}", check=False)

# Stage root files
print("\n Staging root files...")
run_cmd("git add *.md *.txt *.json *.sh *.py 2>/dev/null || true", check=False)

# Check status
print("\n Checking status...")
run_cmd("git status --short | head -20", check=False)

# Commit
print("\n Committing...")
if os.path.exists("FINAL_COMMIT_MESSAGE.txt"):
    success = run_cmd("git commit -F FINAL_COMMIT_MESSAGE.txt", check=False)
elif os.path.exists("COMMIT_MESSAGE.txt"):
    success = run_cmd("git commit -F COMMIT_MESSAGE.txt", check=False)
else:
    success = run_cmd('git commit -m " AbëONE: Full local state preservation + team-ready version"', check=False)

if success:
    print("\n Pushing to GitHub...")
    run_cmd("git push -u --force origin refactor/codebase-cleanup-convergence", check=False)
    print("\n SUCCESS: All files committed and pushed!")
else:
    print("\n  Commit may have failed. Check status above.")


