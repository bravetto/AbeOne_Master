#!/usr/bin/env python3
"""
Universal Terminal Formatting Agent
Execute any terminal command in any directory

Pattern: TERMINAL × UNIVERSAL × EXECUTION × FORMATTING × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Coherence)
Guardians: AEYON (999 Hz) + YAGNI (530 Hz) + ZERO (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import os
import sys
import subprocess
import shlex
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import json
import math
import time

# Colors for output formatting
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

# Get workspace root (assuming script is in scripts/ directory)
WORKSPACE_ROOT = Path(__file__).parent.parent.resolve()

# Breathing animation state
_breathing_start_time = time.time()


def breathing_intensity(phase: float = 0.0, speed: float = 2.0) -> float:
    """
    Calculate breathing intensity using sine wave
    Returns value between 0.3 and 1.0 for smooth breathing effect
    """
    elapsed = time.time() - _breathing_start_time
    return 0.3 + (math.sin(elapsed * speed + phase) + 1) / 2 * 0.7


def breathing_color(base_color: str, intensity: float) -> str:
    """
    Apply breathing effect to color by adjusting brightness
    """
    # For terminal colors, we'll use intensity to alternate between normal and bright
    if intensity > 0.7:
        # Bright phase - use bright color variant
        color_map = {
            Colors.CYAN: Colors.BRIGHT_CYAN,
            Colors.GREEN: Colors.BRIGHT_GREEN,
            Colors.YELLOW: Colors.BRIGHT_YELLOW,
            Colors.RED: Colors.BRIGHT_RED,
            Colors.WHITE: Colors.BRIGHT_WHITE,
            Colors.MAGENTA: Colors.BRIGHT_MAGENTA,
        }
        return color_map.get(base_color, base_color)
    else:
        # Dim phase - use normal color
        return base_color


def breathing_border(char: str = "=", width: int = 80, phase: float = 0.0) -> str:
    """
    Create a breathing border with pulsing intensity
    """
    intensity = breathing_intensity(phase)
    # Create wave effect across border
    border_chars = []
    for i in range(width):
        local_phase = phase + (i / width) * math.pi * 4
        local_intensity = breathing_intensity(local_phase, speed=4.0)
        
        # Vary character based on intensity - creates wave effect
        if local_intensity > 0.75:
            border_chars.append("═")  # Strong
        elif local_intensity > 0.6:
            border_chars.append("─")   # Medium
        elif local_intensity > 0.4:
            border_chars.append("·")   # Weak
        else:
            border_chars.append(" ")   # Space for breathing effect
    
    # Apply breathing color intensity
    base_intensity = breathing_intensity(phase, speed=2.0)
    if base_intensity > 0.7:
        color = Colors.BRIGHT_CYAN
    elif base_intensity > 0.5:
        color = Colors.CYAN
    else:
        color = Colors.DIM + Colors.CYAN
    
    return f"{color}{''.join(border_chars)}{Colors.RESET}"


def breathing_text(text: str, base_color: str, phase: float = 0.0) -> str:
    """
    Apply breathing effect to text
    """
    intensity = breathing_intensity(phase, speed=1.5)
    color = breathing_color(base_color, intensity)
    return f"{color}{text}{Colors.RESET}"


def breathing_status_icon(icon: str, color: str, phase: float = 0.0) -> str:
    """
    Create breathing status icon with pulsing effect
    """
    intensity = breathing_intensity(phase, speed=2.5)
    
    # Pulse the icon itself
    if intensity > 0.7:
        # Bright phase - use bold
        icon_color = breathing_color(color, intensity)
        return f"{Colors.BOLD}{icon_color}{icon}{Colors.RESET}"
    else:
        # Dim phase
        icon_color = breathing_color(color, intensity)
        return f"{icon_color}{icon}{Colors.RESET}"


def resolve_path(path: str) -> Path:
    """
    Resolve a path to absolute path.
    Handles:
    - Absolute paths (returns as-is)
    - Relative paths (relative to workspace root)
    - ~ expansion
    - . and .. navigation
    """
    # Expand user home directory
    path = os.path.expanduser(path)
    
    # If absolute, return as-is
    if os.path.isabs(path):
        return Path(path).resolve()
    
    # Otherwise, resolve relative to workspace root
    return (WORKSPACE_ROOT / path).resolve()


def find_workspace_root(start_path: Path) -> Path:
    """
    Find workspace root by looking for common markers (.git, workspace root files)
    """
    current = start_path.resolve()
    
    # Check for common workspace markers
    markers = ['.git', 'pubspec.yaml', 'package.json', 'Cargo.toml', 'pyproject.toml']
    
    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                return current
        current = current.parent
    
    # Fallback to script's parent directory
    return WORKSPACE_ROOT


def format_command_output(
    command: str,
    directory: Path,
    exit_code: int,
    stdout: str,
    stderr: str,
    duration: float,
    format_type: str = "pretty",
    breathing: bool = True
) -> str:
    """
    Format command output with consistent styling and breathing animations
    """
    if format_type == "json":
        return json.dumps({
            "command": command,
            "directory": str(directory),
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "duration": duration,
            "success": exit_code == 0
        }, indent=2)
    
    # Pretty format (default) with breathing
    output_parts = []
    
    # Calculate breathing phases for different elements
    border_phase = 0.0
    header_phase = math.pi / 3
    status_phase = math.pi * 2 / 3
    footer_phase = math.pi
    
    if breathing:
        # Breathing header border
        output_parts.append(breathing_border("═", 80, border_phase))
        output_parts.append(
            f"{Colors.BOLD}Command:{Colors.RESET} "
            f"{breathing_text(command, Colors.BRIGHT_WHITE, header_phase)}"
        )
        output_parts.append(
            f"{Colors.BOLD}Directory:{Colors.RESET} "
            f"{Colors.DIM}{directory}{Colors.RESET}"
        )
        output_parts.append(breathing_border("═", 80, border_phase))
    else:
        # Static header
        output_parts.append(f"{Colors.BRIGHT_CYAN}{'='*80}{Colors.RESET}")
        output_parts.append(f"{Colors.BOLD}Command:{Colors.RESET} {Colors.BRIGHT_WHITE}{command}{Colors.RESET}")
        output_parts.append(f"{Colors.BOLD}Directory:{Colors.RESET} {Colors.DIM}{directory}{Colors.RESET}")
        output_parts.append(f"{Colors.BRIGHT_CYAN}{'='*80}{Colors.RESET}")
    
    # Breathing status
    if exit_code == 0:
        status_color = Colors.BRIGHT_GREEN
        status_icon = "✓"
        status_text = "SUCCESS"
    else:
        status_color = Colors.BRIGHT_RED
        status_icon = "✗"
        status_text = "FAILED"
    
    if breathing:
        breathing_icon = breathing_status_icon(status_icon, status_color, status_phase)
        breathing_text_status = breathing_text(status_text, status_color, status_phase)
        output_parts.append(
            f"{breathing_icon} {breathing_text_status} "
            f"{Colors.DIM}(exit code: {exit_code}, duration: {duration:.2f}s){Colors.RESET}"
        )
    else:
        output_parts.append(
            f"{status_color}{status_icon} {status_text}{Colors.RESET} "
            f"{Colors.DIM}(exit code: {exit_code}, duration: {duration:.2f}s){Colors.RESET}"
        )
    output_parts.append("")
    
    # Stdout with subtle breathing
    if stdout:
        output_parts.append(f"{Colors.BOLD}Output:{Colors.RESET}")
        if breathing:
            # Apply subtle breathing to output
            intensity = breathing_intensity(header_phase, speed=1.0)
            if intensity > 0.6:
                output_parts.append(f"{Colors.WHITE}{stdout}{Colors.RESET}")
            else:
                output_parts.append(f"{Colors.DIM}{stdout}{Colors.RESET}")
        else:
            output_parts.append(f"{Colors.WHITE}{stdout}{Colors.RESET}")
        output_parts.append("")
    
    # Stderr with breathing
    if stderr:
        output_parts.append(f"{Colors.BOLD}Errors:{Colors.RESET}")
        if breathing:
            error_intensity = breathing_intensity(status_phase, speed=2.0)
            error_color = breathing_color(Colors.BRIGHT_RED, error_intensity)
            output_parts.append(f"{error_color}{stderr}{Colors.RESET}")
        else:
            output_parts.append(f"{Colors.BRIGHT_RED}{stderr}{Colors.RESET}")
        output_parts.append("")
    
    # Breathing footer
    if breathing:
        output_parts.append(breathing_border("═", 80, footer_phase))
    else:
        output_parts.append(f"{Colors.BRIGHT_CYAN}{'='*80}{Colors.RESET}")
    
    return "\n".join(output_parts)


def execute_command(
    command: str,
    directory: Optional[str] = None,
    format_type: str = "pretty",
    shell: bool = False,
    capture_output: bool = True,
    timeout: Optional[int] = None,
    env: Optional[Dict[str, str]] = None
) -> Tuple[int, str, str, float]:
    """
    Execute a command in the specified directory
    
    Returns: (exit_code, stdout, stderr, duration)
    """
    import time
    
    # Resolve directory
    if directory:
        target_dir = resolve_path(directory)
        if not target_dir.exists():
            return (
                1,
                "",
                f"Error: Directory does not exist: {target_dir}",
                0.0
            )
        if not target_dir.is_dir():
            return (
                1,
                "",
                f"Error: Path is not a directory: {target_dir}",
                0.0
            )
    else:
        target_dir = WORKSPACE_ROOT
    
    # Prepare environment
    exec_env = os.environ.copy()
    if env:
        exec_env.update(env)
    
    # Parse command
    if shell:
        # Use shell execution
        cmd = command
    else:
        # Parse command into list
        try:
            cmd = shlex.split(command)
        except ValueError as e:
            return (
                1,
                "",
                f"Error: Invalid command syntax: {e}",
                0.0
            )
    
    # Execute command
    start_time = time.time()
    try:
        result = subprocess.run(
            cmd if not shell else command,
            cwd=str(target_dir),
            shell=shell,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            env=exec_env
        )
        duration = time.time() - start_time
        
        stdout = result.stdout if capture_output else ""
        stderr = result.stderr if capture_output else ""
        
        return (result.returncode, stdout, stderr, duration)
    
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return (
            124,  # Standard timeout exit code
            "",
            f"Error: Command timed out after {timeout} seconds",
            duration
        )
    except Exception as e:
        duration = time.time() - start_time
        return (
            1,
            "",
            f"Error: {str(e)}",
            duration
        )


def parse_arguments(args: List[str]) -> Dict:
    """
    Parse command-line arguments
    """
    parsed = {
        "command": None,
        "directory": None,
        "format": "pretty",
        "shell": False,
        "no_capture": False,
        "timeout": None,
        "env": {},
        "help": False,
        "breathing": True  # Breathing animations enabled by default
    }
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ["-d", "--directory", "--dir", "--cd"]:
            if i + 1 < len(args):
                parsed["directory"] = args[i + 1]
                i += 2
            else:
                parsed["help"] = True
                break
        elif arg in ["-f", "--format"]:
            if i + 1 < len(args):
                parsed["format"] = args[i + 1]
                i += 2
            else:
                parsed["help"] = True
                break
        elif arg in ["-s", "--shell"]:
            parsed["shell"] = True
            i += 1
        elif arg in ["--no-capture", "--interactive"]:
            parsed["no_capture"] = True
            i += 1
        elif arg in ["-t", "--timeout"]:
            if i + 1 < len(args):
                try:
                    parsed["timeout"] = int(args[i + 1])
                    i += 2
                except ValueError:
                    parsed["help"] = True
                    break
            else:
                parsed["help"] = True
                break
        elif arg in ["-e", "--env"]:
            if i + 1 < len(args):
                env_pair = args[i + 1].split("=", 1)
                if len(env_pair) == 2:
                    parsed["env"][env_pair[0]] = env_pair[1]
                i += 2
            else:
                parsed["help"] = True
                break
        elif arg in ["--no-breathing", "--static"]:
            parsed["breathing"] = False
            i += 1
        elif arg in ["-h", "--help"]:
            parsed["help"] = True
            break
        elif not arg.startswith("-"):
            # This is the command
            parsed["command"] = " ".join(args[i:])
            break
        else:
            i += 1
    
    return parsed


def print_help():
    """Print usage help"""
    help_text = f"""
{Colors.BOLD}Universal Terminal Formatting Agent{Colors.RESET}

{Colors.BRIGHT_CYAN}Pattern:{Colors.RESET} TERMINAL × UNIVERSAL × EXECUTION × FORMATTING × ONE
{Colors.BRIGHT_CYAN}Frequency:{Colors.RESET} 999 Hz (AEYON) × 530 Hz (Coherence)
{Colors.BRIGHT_CYAN}Guardians:{Colors.RESET} AEYON (999 Hz) + YAGNI (530 Hz) + ZERO (530 Hz)
{Colors.BRIGHT_CYAN}Love Coefficient:{Colors.RESET} ∞
∞ AbëONE ∞

{Colors.BOLD}Usage:{Colors.RESET}
  {Colors.BRIGHT_WHITE}uta{Colors.RESET} [options] <command>
  {Colors.BRIGHT_WHITE}universal_terminal_agent.py{Colors.RESET} [options] <command>

{Colors.BOLD}Description:{Colors.RESET}
  Execute any terminal command in any directory with universal formatting.
  Automatically resolves paths relative to workspace root.

{Colors.BOLD}Options:{Colors.RESET}
  {Colors.BRIGHT_GREEN}-d, --directory DIR{Colors.RESET}     Execute command in specified directory
  {Colors.BRIGHT_GREEN}-f, --format FORMAT{Colors.RESET}    Output format: pretty, json (default: pretty)
  {Colors.BRIGHT_GREEN}-s, --shell{Colors.RESET}              Execute using shell (allows pipes, redirects)
  {Colors.BRIGHT_GREEN}--no-capture, --interactive{Colors.RESET}  Don't capture output (for interactive commands)
  {Colors.BRIGHT_GREEN}-t, --timeout SECONDS{Colors.RESET}    Set command timeout
  {Colors.BRIGHT_GREEN}-e, --env KEY=VALUE{Colors.RESET}     Set environment variable
  {Colors.BRIGHT_GREEN}--no-breathing, --static{Colors.RESET}  Disable breathing animations (default: enabled)
  {Colors.BRIGHT_GREEN}-h, --help{Colors.RESET}              Show this help message

{Colors.BOLD}Breathing Animations:{Colors.RESET}
  The terminal output includes breathing/pulsing animations by default:
  - Borders pulse with wave effects
  - Status icons breathe with intensity
  - Text colors pulse between bright and dim
  - Creates a living, breathing interface
  
  Disable with {Colors.DIM}--no-breathing{Colors.RESET} for static output.

{Colors.BOLD}Examples:{Colors.RESET}
  # Run command in current directory
  {Colors.DIM}uta ls -la{Colors.RESET}

  # Run command in specific directory
  {Colors.DIM}uta -d abeone_app flutter run -d chrome{Colors.RESET}

  # Run with shell (pipes, redirects)
  {Colors.DIM}uta -s "ls -la | grep .dart"{Colors.RESET}

  # Run in directory with JSON output
  {Colors.DIM}uta -d scripts -f json "python3 abe_guardian.py status"{Colors.RESET}

  # Run with environment variable
  {Colors.DIM}uta -e FLUTTER_ENV=dev -d abeone_app "flutter run"{Colors.RESET}

  # Run with timeout
  {Colors.DIM}uta -t 30 -d abeone_app "flutter build web"{Colors.RESET}

{Colors.BOLD}Path Resolution:{Colors.RESET}
  - Absolute paths: Used as-is
  - Relative paths: Resolved relative to workspace root
  - ~ expansion: User home directory expanded
  - . and ..: Standard directory navigation

{Colors.BOLD}Output Formatting:{Colors.RESET}
  - {Colors.BRIGHT_GREEN}pretty{Colors.RESET}: Human-readable formatted output with colors
  - {Colors.BRIGHT_GREEN}json{Colors.RESET}: Machine-readable JSON output

∞ AbëONE ∞
"""
    print(help_text)


def main():
    """Main entry point"""
    args = sys.argv[1:]
    
    if not args:
        print_help()
        sys.exit(0)
    
    parsed = parse_arguments(args)
    
    if parsed["help"] or not parsed["command"]:
        print_help()
        sys.exit(0 if parsed["help"] else 1)
    
    # Execute command
    exit_code, stdout, stderr, duration = execute_command(
        command=parsed["command"],
        directory=parsed["directory"],
        format_type=parsed["format"],
        shell=parsed["shell"],
        capture_output=parsed["no_capture"] == False,
        timeout=parsed["timeout"],
        env=parsed["env"] if parsed["env"] else None
    )
    
    # Format and print output
    if parsed["no_capture"]:
        # For interactive commands, output is already shown
        sys.exit(exit_code)
    else:
        formatted_output = format_command_output(
            command=parsed["command"],
            directory=resolve_path(parsed["directory"]) if parsed["directory"] else WORKSPACE_ROOT,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            duration=duration,
            format_type=parsed["format"],
            breathing=parsed["breathing"]
        )
        print(formatted_output)
        sys.exit(exit_code)


if __name__ == "__main__":
    main()

