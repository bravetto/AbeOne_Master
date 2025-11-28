#!/usr/bin/env python3
"""
TokenGuard Multi-Mode Demo

Demonstrates TokenGuard's three operating modes:
1. Standard mode - Original confidence-based pruning
2. Tool call mode - LLM tool calling with pruning
3. MCP mode - Model Context Protocol server
"""

import os
import requests
import time
from typing import Dict, Any

try:
    from colorama import init, Fore, Back, Style
    HAS_COLORAMA = True
    init(autoreset=True)
except ImportError:
    HAS_COLORAMA = False

    # Fallback color classes
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""
        RESET = ""

    class Back:
        GREEN = ""
        RED = ""
        RESET = ""

    class Style:
        BRIGHT = ""
        RESET_ALL = ""

DEFAULT_BASE_URL = "http://localhost:8000"


def print_header(text: str, color=Fore.CYAN) -> Any:
    """Print a formatted header."""
    width = 60
    print(f"\n{color}{'' * width}{Style.RESET_ALL}")
    print(f"{color}{Style.BRIGHT} {text.center(width-4)} "
          f"{Style.RESET_ALL}{color}{Style.RESET_ALL}")
    print(f"{color}{'' * width}{Style.RESET_ALL}\n")


def print_section(title: str, color=Fore.BLUE) -> Any:
    """Print a section header."""
    print(f"\n{color} {title} {Fore.WHITE}{'' * (50-len(title))}{Style.RESET_ALL}")


def print_status(message: str, status: str = "info") -> Any:
    """Print a status message with appropriate color."""
    if status == "success":
        icon = ""
        color = Fore.GREEN
    elif status == "error":
        icon = ""
        color = Fore.RED
    elif status == "warning":
        icon = ""
        color = Fore.YELLOW
    elif status == "info":
        icon = "ℹ"
        color = Fore.BLUE
    else:
        icon = "•"
        color = Fore.WHITE

    print(f"{color}{icon} {message}{Style.RESET_ALL}")


def print_progress(current: int, total: int, message: str = "") -> Any:
    """Print a progress bar."""
    width = 30
    percentage = current / total
    filled = int(width * percentage)
    bar = "" * filled + "" * (width - filled)
    percent_text = f"{int(percentage * 100):3d}%"

    print(f"\r{Fore.CYAN} {bar}  {percent_text} {message}{Style.RESET_ALL}", end="", flush=True)
    if current == total:
        print()  # New line when complete


def print_result(title: str, data: Dict[str, Any], color=Fore.GREEN) -> Any:
    """Print formatted result data."""
    print(f"\n{color} {title} {Fore.WHITE}{'' * (50-len(title))}{Style.RESET_ALL}")
    for key, value in data.items():
        if isinstance(value, (int, float)):
            value_str = f"{value:.2f}" if isinstance(value, float) else str(value)
            print(f"{color} {key}: {Fore.YELLOW}{value_str}{Style.RESET_ALL}")
        elif isinstance(value, str) and len(value) > 50:
            print(f"{color} {key}: {Fore.WHITE}{value[:47]}...{Style.RESET_ALL}")
        else:
            print(f"{color} {key}: {Fore.WHITE}{value}{Style.RESET_ALL}")
    print(f"{color}{'' * 58}{Style.RESET_ALL}")


def spinner_task(message: str, task_func, *args, **kwargs) -> Any:
    """Run a task with a spinner."""
    spinner_chars = ""
    start_time = time.time()

    # Start spinner in a separate thread-like approach
    result = None
    error = None

    # Simple spinner animation
    import threading
    import time as time_module

    def spin() -> Any:
        i = 0
        while not hasattr(spin, 'done'):
            char = spinner_chars[i % len(spinner_chars)]
            print(f"\r{Fore.CYAN}{char} {message}{Style.RESET_ALL}", end="", flush=True)
            time_module.sleep(0.1)
            i += 1

    spinner_thread = threading.Thread(target=spin, daemon=True)
    spinner_thread.start()

    try:
        result = task_func(*args, **kwargs)
    except Exception as e:
        error = e
    finally:
        # Stop spinner
        spin.done = True
        spinner_thread.join(timeout=0.2)

    # Clear spinner line
    print(f"\r{' ' * (len(message) + 10)}\r", end="", flush=True)

    if error:
        print_status(f"{message} - Failed: {str(error)}", "error")
        return None
    else:
        elapsed = time.time() - start_time
        print_status(f"{message} - Completed in {elapsed:.2f}s", "success")
        return result


def demo_standard_mode(base_url: str = DEFAULT_BASE_URL) -> Any:
    """Demo standard TokenGuard mode."""
    print(" TokenGuard Standard Mode Demo")
    print("=" * 50)

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print(" Health check passed")
        else:
            print(f" Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f" Cannot connect to service: {e}")
        return

    # Test prune endpoint
    prune_payload = {
        "text": "This is a very long response that should be pruned because it "
                "exceeds reasonable length limits and may not be very confident "
                "in its later parts.",
        "confidence": 0.6
    }

    try:
        response = requests.post(f"{base_url}/v1/prune", json=prune_payload)
        if response.status_code == 200:
            result = response.json()
            print(f" Prune result: {result['decision']['action']}")
            if result['decision']['action'] == 'prune':
                print(f"   Estimated savings: {result['decision']['estimated_savings']} chars")
        else:
            print(f" Prune failed: {response.status_code}")
    except Exception as e:
        print(f" Prune request failed: {e}")

    print()


def demo_tool_call_mode(base_url: str = DEFAULT_BASE_URL) -> Any:
    """Demo tool call mode."""
    print(" TokenGuard Tool Call Mode Demo")
    print("=" * 50)

    # Test tool call endpoint
    tool_payload = {
        "prompt": "Please analyze this text for confidence and prune if needed.",
        "llm_config": {
            "model": "gpt-4",
            "max_tokens": 200
        },
        "tokenguard_config": {
            "confidence_threshold": 0.7,
            "max_length": 500
        },
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "prune_text",
                    "description": "Prune text based on confidence analysis",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "confidence_threshold": {"type": "number"}
                        },
                        "required": ["text"]
                    }
                }
            }
        ]
    }

    try:
        response = requests.post(f"{base_url}/v1/generate-with-tools", json=tool_payload)
        if response.status_code == 200:
            result = response.json()
            print(" Tool call generation successful")
            print(f"   Generated text: {result['text'][:100]}...")
            print(f"   Tool calls made: {len(result.get('tool_calls', []))}")
            print(f"   Stop reason: {result['stop_reason']}")
        else:
            print(f" Tool call failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f" Tool call request failed: {e}")

    print()


def demo_mcp_mode(base_url: str = DEFAULT_BASE_URL) -> Any:
    """Demo MCP mode."""
    print(" TokenGuard MCP Mode Demo")
    print("=" * 50)

    # Test MCP initialize
    init_payload = {
        "method": "initialize",
        "params": {}
    }

    try:
        response = requests.post(f"{base_url}/mcp", json=init_payload)
        if response.status_code == 200:
            result = response.json()
            print(" MCP initialize successful")
            print(f"   Protocol version: {result['result']['protocolVersion']}")
            print(f"   Server: {result['result']['serverInfo']['name']}")
        else:
            print(f" MCP initialize failed: {response.status_code}")
    except Exception as e:
        print(f" MCP initialize request failed: {e}")

    # Test MCP tools list
    try:
        tools_payload = {
            "method": "tools/list",
            "params": {}
        }
        response = requests.post(f"{base_url}/mcp", json=tools_payload)
        if response.status_code == 200:
            result = response.json()
            tools = result['result']['tools']
            print(f" MCP tools list: {len(tools)} tools available")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['description'][:50]}...")
        else:
            print(f" MCP tools list failed: {response.status_code}")
    except Exception as e:
        print(f" MCP tools list request failed: {e}")

    # Test MCP tool call
    try:
        call_payload = {
            "method": "tools/call",
            "params": {
                "name": "prune_text",
                "arguments": {
                    "text": "This is a test text that might be pruned.",
                    "confidence_threshold": 0.8
                }
            }
        }
        response = requests.post(f"{base_url}/mcp", json=call_payload)
        if response.status_code == 200:
            result = response.json()
            print(" MCP tool call successful")
            print(f"   Should prune: {result['result']['should_prune']}")
        else:
            print(f" MCP tool call failed: {response.status_code}")
    except Exception as e:
        print(f" MCP tool call request failed: {e}")

    print()


def main() -> Any:
    """Run all demos."""
    print(" TokenGuard Multi-Mode Demo")
    print("Demonstrating all three operating modes\n")

    # Check which mode the service is running in
    base_url = os.environ.get("TOKENGUARD_URL", DEFAULT_BASE_URL)

    print(f"Testing service at: {base_url}")
    print("Note: Make sure the TokenGuard service is running with the appropriate mode set\n")

    # Demo standard mode (always available)
    demo_standard_mode(base_url)

    # Demo tool call mode
    demo_tool_call_mode(base_url)

    # Demo MCP mode
    demo_mcp_mode(base_url)

    print(" Demo complete!")
    print("\nTo run in different modes:")
    print("  Standard: TOKENGUARD_SERVICE_MODE=standard python main.py")
    print("  Tool Call: TOKENGUARD_SERVICE_MODE=tool_call python main.py")
    print("  MCP: TOKENGUARD_SERVICE_MODE=mcp python main.py")


if __name__ == "__main__":
    main()
