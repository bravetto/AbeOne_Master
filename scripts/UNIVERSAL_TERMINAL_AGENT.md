# 🔧 Universal Terminal Formatting Agent

**Pattern:** TERMINAL × UNIVERSAL × EXECUTION × FORMATTING × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (Coherence)  
**Guardians:** AEYON (999 Hz) + YAGNI (530 Hz) + ZERO (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## ✨ What It Does

The Universal Terminal Agent (UTA) allows you to execute **any terminal command in any directory** with consistent formatting and automatic path resolution. No more `cd` commands needed!

### Key Features

- **Universal Directory Execution**: Run commands in any directory without changing your current directory
- **Automatic Path Resolution**: Resolves paths relative to workspace root automatically
- **Breathing Animations**: Living, pulsing output with wave effects and breathing intensity (enabled by default)
- **Consistent Formatting**: Beautiful, colorized output with consistent structure
- **Multiple Output Formats**: Pretty (human-readable) or JSON (machine-readable)
- **Shell Support**: Execute complex commands with pipes, redirects, etc.
- **Error Handling**: Clear error messages and exit codes
- **Timeout Support**: Set command timeouts for long-running operations
- **Environment Variables**: Pass environment variables to commands

---

## 🚀 Quick Start

### Basic Usage

```bash
# Run command in current directory
python3 scripts/universal_terminal_agent.py ls -la

# Or use the short alias (if added to PATH)
uta ls -la

# Run command in specific directory
uta -d abeone_app flutter run -d chrome

# Run with shell (for pipes, redirects)
uta -s "ls -la | grep .dart"
```

---

## 📖 Full Documentation

### Installation

The agent is already available in the `scripts/` directory. To use it from anywhere:

#### Option 1: Add to PATH (Recommended)

Add this to your `~/.zshrc` or `~/.bashrc`:

```bash
export PATH="$PATH:/Users/michaelmataluni/Documents/AbeOne_Master/scripts"
alias uta="python3 /Users/michaelmataluni/Documents/AbeOne_Master/scripts/universal_terminal_agent.py"
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

#### Option 2: Use Direct Path

```bash
python3 /Users/michaelmataluni/Documents/AbeOne_Master/scripts/universal_terminal_agent.py <command>
```

---

### Command Syntax

```bash
uta [options] <command>
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--directory DIR` | `-d` | Execute command in specified directory |
| `--format FORMAT` | `-f` | Output format: `pretty` (default) or `json` |
| `--shell` | `-s` | Execute using shell (allows pipes, redirects) |
| `--no-capture` | | Don't capture output (for interactive commands) |
| `--interactive` | | Alias for `--no-capture` |
| `--timeout SECONDS` | `-t` | Set command timeout in seconds |
| `--env KEY=VALUE` | `-e` | Set environment variable (can be used multiple times) |
| `--no-breathing` | | Disable breathing animations (default: enabled) |
| `--static` | | Alias for `--no-breathing` |
| `--help` | `-h` | Show help message |

---

## 📝 Examples

### Basic Commands

```bash
# List files in current directory
uta ls -la

# List files in specific directory
uta -d abeone_app ls -la

# Run Flutter command in app directory
uta -d abeone_app flutter run -d chrome

# Run Python script
uta -d scripts python3 abe_guardian.py status
```

### Shell Commands (Pipes, Redirects)

```bash
# Use shell for complex commands
uta -s "ls -la | grep .dart | wc -l"

# Chain commands
uta -s "cd abeone_app && flutter pub get && flutter run"
```

### JSON Output

```bash
# Get JSON output for scripting
uta -f json -d scripts "ls -la"

# Example output:
# {
#   "command": "ls -la",
#   "directory": "/path/to/scripts",
#   "exit_code": 0,
#   "stdout": "...",
#   "stderr": "",
#   "duration": 0.05,
#   "success": true
# }
```

### Environment Variables

```bash
# Set environment variable
uta -e FLUTTER_ENV=dev -d abeone_app "flutter run"

# Multiple environment variables
uta -e NODE_ENV=production -e DEBUG=false -d app "npm start"
```

### Timeout

```bash
# Set 30 second timeout
uta -t 30 -d abeone_app "flutter build web"
```

### Interactive Commands

```bash
# For commands that need interactive input
uta --interactive -d abeone_app "flutter run"
```

---

## 🌊 Breathing Animations

The Universal Terminal Agent includes **breathing animations** by default, making the output feel alive and dynamic:

- **Pulsing Borders**: Wave effects that pulse across the border lines
- **Breathing Status Icons**: Status symbols (✓/✗) pulse with intensity
- **Breathing Text**: Text colors pulse between bright and dim phases
- **Wave Effects**: Multiple wave patterns create a living, breathing interface

### Disable Breathing

To disable breathing animations for static output:

```bash
uta --no-breathing -d abeone_app "flutter run"
# or
uta --static -d abeone_app "flutter run"
```

The breathing effect uses sine wave calculations to create smooth, natural pulsing animations that make the terminal output feel alive and connected to the AbëONE energy field.

---

## 🎨 Output Formatting

### Pretty Format (Default) - With Breathing

```
================================================================================
Command: flutter run -d chrome
Directory: /Users/michaelmataluni/Documents/AbeOne_Master/abeone_app
================================================================================
✓ SUCCESS (exit code: 0, duration: 2.34s)

Output:
[Flutter output here...]

================================================================================
```

### JSON Format

```json
{
  "command": "flutter run -d chrome",
  "directory": "/Users/michaelmataluni/Documents/AbeOne_Master/abeone_app",
  "exit_code": 0,
  "stdout": "[output]",
  "stderr": "",
  "duration": 2.34,
  "success": true
}
```

---

## 🔍 Path Resolution

The agent automatically resolves paths:

- **Absolute paths**: Used as-is
  ```bash
  uta -d /absolute/path/to/dir "ls"
  ```

- **Relative paths**: Resolved relative to workspace root
  ```bash
  uta -d abeone_app "ls"  # Resolves to workspace_root/abeone_app
  ```

- **Home directory**: `~` is expanded
  ```bash
  uta -d ~/Documents "ls"
  ```

- **Current directory**: `.` resolves to workspace root
  ```bash
  uta -d . "ls"
  ```

- **Parent directory**: `..` works as expected
  ```bash
  uta -d ../other_project "ls"
  ```

---

## 🛠️ Integration Examples

### In CI/CD Pipelines

```yaml
# GitHub Actions example
- name: Run Flutter tests
  run: |
    python3 scripts/universal_terminal_agent.py \
      -d abeone_app \
      -f json \
      "flutter test" > test_results.json
```

### In Shell Scripts

```bash
#!/bin/bash
# Use UTA in shell scripts
RESULT=$(uta -f json -d abeone_app "flutter pub get")
EXIT_CODE=$(echo "$RESULT" | jq -r '.exit_code')

if [ "$EXIT_CODE" -eq 0 ]; then
    echo "Success!"
else
    echo "Failed!"
fi
```

### In Python Scripts

```python
import subprocess
import json

result = subprocess.run(
    ["python3", "scripts/universal_terminal_agent.py", 
     "-d", "abeone_app", "-f", "json", "flutter pub get"],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
if data["success"]:
    print("Success!")
else:
    print(f"Failed: {data['stderr']}")
```

---

## 🎯 Use Cases

### 1. Cross-Directory Command Execution

```bash
# Run commands in different directories without cd
uta -d abeone_app "flutter run"
uta -d scripts "python3 abe_guardian.py status"
uta -d docs "ls -la"
```

### 2. Consistent Output Formatting

```bash
# All commands have consistent, beautiful output
uta -d abeone_app "flutter pub get"
uta -d scripts "python3 generate_thanksgiving_video.py"
```

### 3. Scripting and Automation

```bash
# Use JSON output for automation
uta -f json -d abeone_app "flutter test" | jq '.success'
```

### 4. CI/CD Integration

```bash
# Use in CI/CD pipelines for consistent execution
uta -t 300 -d abeone_app "flutter build web"
```

---

## 🔧 Advanced Usage

### Combining Options

```bash
# Complex example with all options
uta \
  -d abeone_app \
  -f json \
  -t 60 \
  -e FLUTTER_ENV=production \
  -e BUILD_MODE=release \
  "flutter build web --release"
```

### Error Handling

The agent returns proper exit codes:
- `0`: Success
- `1`: General error
- `124`: Timeout
- Other: Command-specific exit codes

```bash
# Check exit code
uta -d abeone_app "flutter run" && echo "Success!" || echo "Failed!"
```

---

## 📁 File Structure

```
scripts/
├── universal_terminal_agent.py    # Main Python script
├── uta                             # Shell wrapper script
└── UNIVERSAL_TERMINAL_AGENT.md    # This documentation
```

---

## 💖 THE HEART-TRUTH

**Universal execution. Consistent formatting. One pattern.**

The Universal Terminal Agent brings coherence to command execution across all directories and contexts. Every command executed with UTA follows the same pattern, the same formatting, the same structure.

**UNIVERSAL = ONE**
**EXECUTION = CONVERGENCE**
**FORMATTING = CLARITY**

**LOVE = LIFE = ONE**

---

## 🐛 Troubleshooting

### Command Not Found

If you get "command not found", make sure:
1. The script is executable: `chmod +x scripts/universal_terminal_agent.py`
2. Python 3 is installed: `python3 --version`
3. You're using the correct path

### Path Resolution Issues

If paths aren't resolving correctly:
1. Check that you're running from the workspace root
2. Use absolute paths if needed: `-d /absolute/path`
3. Verify the directory exists: `ls -d <directory>`

### Permission Errors

If you get permission errors:
1. Make script executable: `chmod +x scripts/universal_terminal_agent.py`
2. Check directory permissions: `ls -ld <directory>`
3. Use `sudo` if needed (though not recommended)

---

**Pattern:** TERMINAL × UNIVERSAL × EXECUTION × FORMATTING × ONE  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

**UNIVERSAL. CONSISTENT. ONE. 🔧✨**

