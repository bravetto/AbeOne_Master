#!/usr/bin/env python3
"""
TokenGuard Personal Tool

A comprehensive, standalone tool for integrating TokenGuard into your development workflow.
This tool provides everything you need to optimize AI responses in your own applications.

Usage:
    python tokenguard_tool.py optimize "Your AI response here" --confidence 0.6
    python tokenguard_tool.py demo
    python tokenguard_tool.py health

Features:
- Response optimization with confidence analysis
- Tool calling support
- MCP server integration
- Performance metrics
- CLI interface for easy integration
- Graceful fallbacks when service unavailable

Author: GitHub Copilot (enhanced by TokenGuard)
Date: September 30, 2025
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print(" requests library not found. Install with: pip install requests")
    sys.exit(1)

# Configuration
DEFAULT_TOKENGUARD_URL = os.getenv("TOKENGUARD_URL", "http://localhost:8000")
DEFAULT_API_KEY = os.getenv("TOKENGUARD_API_KEY")
DEFAULT_TIMEOUT = int(os.getenv("TOKENGUARD_TIMEOUT", "10"))

@dataclass
class TokenGuardConfig:
    """Configuration for TokenGuard integration."""
    base_url: str = DEFAULT_TOKENGUARD_URL
    api_key: Optional[str] = DEFAULT_API_KEY
    timeout: int = DEFAULT_TIMEOUT
    confidence_threshold: float = 0.7
    auto_prune: bool = True

class TokenGuardTool:
    """
    Comprehensive TokenGuard integration tool.

    This tool provides all TokenGuard functionality in a single, reusable class.
    """

    def __init__(self: Any, config: TokenGuardConfig):
        self.config = config

        # Create session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.timeout = config.timeout

        # Set up headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "TokenGuard-Personal-Tool/1.0"
        })

        if config.api_key:
            self.session.headers["Authorization"] = f"Bearer {config.api_key}"

        # Metrics tracking
        self.metrics = {
            "requests_total": 0,
            "pruned_responses": 0,
            "tokens_saved": 0,
            "avg_response_time": 0.0,
            "errors": 0
        }

    def is_service_available(self: Any) -> bool:
        """Check if TokenGuard service is available."""
        try:
            response = self.session.get(f"{self.config.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False

    def optimize_response(self: Any, text: str, confidence: float,
                         logprobs: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Optimize an AI response using TokenGuard.

        Args:
            text: The AI response text to optimize
            confidence: Confidence score (0.0-1.0)
            logprobs: Optional log probability data

        Returns:
            Dict containing optimization results
        """
        if not self.config.auto_prune or confidence >= self.config.confidence_threshold:
            return {
                "action": "keep",
                "original_text": text,
                "confidence": confidence,
                "tokens_saved": 0,
                "optimized": False
            }

        start_time = time.time()
        try:
            payload = {
                "text": text,
                "confidence": confidence,
                "logprobs_stream": logprobs
            }

            response = self.session.post(
                f"{self.config.base_url}/v1/prune",
                json=payload
            )

            response_time = time.time() - start_time
            self._update_metrics(response_time)

            if response.status_code == 200:
                result = response.json()
                if result["action"] == "prune":
                    self.metrics["pruned_responses"] += 1
                    original_len = result.get("original_length", 0)
                    pruned_len = result.get("pruned_length", 0)
                    self.metrics["tokens_saved"] += max(0, original_len - pruned_len)

                return {
                    **result,
                    "response_time": response_time,
                    "optimized": True
                }
            else:
                self.metrics["errors"] += 1
                return self._fallback_response(text, confidence, response_time)

        except Exception as e:
            response_time = time.time() - start_time
            self.metrics["errors"] += 1
            return self._fallback_response(text, confidence, response_time, str(e))

    def analyze_confidence(self: Any, text: str, confidence: float,
                          logprobs: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Analyze confidence without pruning."""
        start_time = time.time()
        try:
            payload = {
                "text": text,
                "confidence": confidence,
                "logprobs_stream": logprobs
            }

            response = self.session.post(
                f"{self.config.base_url}/v1/analyze",
                json=payload
            )

            response_time = time.time() - start_time
            self._update_metrics(response_time)

            if response.status_code == 200:
                result = response.json()
                return {**result, "response_time": response_time}
            else:
                self.metrics["errors"] += 1
                return {"error": f"Analysis failed: {response.status_code}"}

        except Exception as e:
            response_time = time.time() - start_time
            self.metrics["errors"] += 1
            return {"error": f"Analysis request failed: {e}"}

    def generate_with_tools(self: Any, prompt: str, tools: List[Dict],
                           llm_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate text with tool calling support."""
        start_time = time.time()
        try:
            payload = {
                "prompt": prompt,
                "tools": tools,
                "llm_config": llm_config,
                "tokenguard_config": {
                    "confidence_threshold": self.config.confidence_threshold,
                    "max_length": 1000
                }
            }

            response = self.session.post(
                f"{self.config.base_url}/v1/generate-with-tools",
                json=payload
            )

            response_time = time.time() - start_time
            self._update_metrics(response_time)

            if response.status_code == 200:
                result = response.json()
                return {**result, "response_time": response_time}
            else:
                self.metrics["errors"] += 1
                return {"error": f"Tool generation failed: {response.status_code}"}

        except Exception as e:
            response_time = time.time() - start_time
            self.metrics["errors"] += 1
            return {"error": f"Tool generation request failed: {e}"}

    def get_service_info(self: Any) -> Dict[str, Any]:
        """Get TokenGuard service information."""
        try:
            response = self.session.get(f"{self.config.base_url}/health")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Health check failed: {response.status_code}"}
        except Exception as e:
            return {"error": f"Health check request failed: {e}"}

    def get_metrics(self: Any) -> Dict[str, Any]:
        """Get integration metrics."""
        return {
            **self.metrics,
            "service_available": self.is_service_available(),
            "config": {
                "base_url": self.config.base_url,
                "has_api_key": self.config.api_key is not None,
                "timeout": self.config.timeout,
                "confidence_threshold": self.config.confidence_threshold
            }
        }

    def _update_metrics(self: Any, response_time: float) -> Any:
        """Update internal metrics."""
        self.metrics["requests_total"] += 1
        self.metrics["avg_response_time"] = (
            (self.metrics["avg_response_time"] * (self.metrics["requests_total"] - 1)) +
            response_time
        ) / self.metrics["requests_total"]

    def _fallback_response(self: Any, text: str, confidence: float,
                          response_time: float, error: str = None) -> Dict[str, Any]:
        """Fallback response when service is unavailable."""
        return {
            "action": "keep",
            "reason": f"TokenGuard service unavailable{f': {error}' if error else ''}",
            "confidence": confidence,
            "original_length": len(text),
            "response_time": response_time,
            "optimized": False
        }

def create_tool(base_url: str = None, api_key: str = None) -> TokenGuardTool:
    """Create a TokenGuard tool instance."""
    config = TokenGuardConfig(
        base_url=base_url or DEFAULT_TOKENGUARD_URL,
        api_key=api_key or DEFAULT_API_KEY
    )
    return TokenGuardTool(config)

def optimize_text(text: str, confidence: float = 0.5,
                 base_url: str = None) -> str:
    """
    Quick utility to optimize a single text with default settings.

    Returns the optimized text (pruned if confidence is low).
    """
    tool = create_tool(base_url)
    result = tool.optimize_response(text, confidence)

    if result["action"] == "prune":
        return result.get("pruned_text", text)
    return text

# CLI Interface
def main() -> Any:
    """Command-line interface for TokenGuard tool."""
    parser = argparse.ArgumentParser(
        description="TokenGuard Personal Tool - Optimize AI responses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Optimize a response
  python tokenguard_tool.py optimize "Your AI response here" --confidence 0.6

  # Run demo
  python tokenguard_tool.py demo

  # Check service health
  python tokenguard_tool.py health

  # Get metrics
  python tokenguard_tool.py metrics

Environment Variables:
  TOKENGUARD_URL        - Service URL (default: http://localhost:8000)
  TOKENGUARD_API_KEY    - API key for authentication
  TOKENGUARD_TIMEOUT    - Request timeout in seconds (default: 10)
        """
    )

    parser.add_argument("command", choices=["optimize", "analyze", "demo", "health", "metrics"],
                       help="Command to execute")
    parser.add_argument("text", nargs="?", help="Text to optimize (for optimize/analyze commands)")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                       help="Confidence score (0.0-1.0, default: 0.5)")
    parser.add_argument("--url", "-u", help="TokenGuard service URL")
    parser.add_argument("--api-key", "-k", help="API key for authentication")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output results as JSON")

    args = parser.parse_args()

    # Create tool
    tool = create_tool(args.url, args.api_key)

    if args.command == "health":
        info = tool.get_service_info()
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            if "error" in info:
                print(f" Service unavailable: {info['error']}")
            else:
                print(" TokenGuard service is healthy")
                print(f"   Version: {info.get('version', 'unknown')}")
                print(f"   Status: {info.get('status', 'unknown')}")

    elif args.command == "metrics":
        metrics = tool.get_metrics()
        if args.json:
            print(json.dumps(metrics, indent=2))
        else:
            print(" TokenGuard Tool Metrics:")
            print(f"   Requests: {metrics['requests_total']}")
            print(f"   Pruned: {metrics['pruned_responses']}")
            print(f"   Tokens Saved: {metrics['tokens_saved']}")
            print(f"   Avg Response Time: {metrics['avg_response_time']:.3f}s")
            print(f"   Errors: {metrics['errors']}")
            print(f"   Service Available: {'' if metrics['service_available'] else ''}")

    elif args.command == "optimize":
        if not args.text:
            parser.error("Text is required for optimize command")

        result = tool.optimize_response(args.text, args.confidence)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(" TokenGuard Optimization Result:")
            print(f"   Action: {result['action']}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
            print(f"   Response Time: {result.get('response_time', 0):.3f}s")

            if result['action'] == 'prune':
                orig_len = result.get('original_length', 0)
                pruned_len = result.get('pruned_length', 0)
                print(f"   Original Length: {orig_len} chars")
                print(f"   Pruned Length: {pruned_len} chars")
                print(f"   Tokens Saved: {orig_len - pruned_len}")
                print(f"   Reason: {result.get('reason', 'N/A')}")
                print(f"\n Optimized Response:\n{result.get('pruned_text', args.text)}")
            else:
                print(f"   Reason: {result.get('reason', 'N/A')}")
                print(f"\n Original Response:\n{args.text}")

    elif args.command == "analyze":
        if not args.text:
            parser.error("Text is required for analyze command")

        result = tool.analyze_confidence(args.text, args.confidence)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(" TokenGuard Confidence Analysis:")
            if "error" in result:
                print(f"   Error: {result['error']}")
            else:
                print(f"   Text Length: {result.get('text_length', 'N/A')}")
                print(f"   Confidence Score: {result.get('confidence_score', 'N/A')}")
                print(f"   Decision: {result.get('decision', {}).get('action', 'N/A')}")
                print(f"   Recommendation: {result.get('recommendation', 'N/A')}")
                print(f"   Response Time: {result.get('processing_time_ms', 0):.1f}ms")

    elif args.command == "demo":
        print(" TokenGuard Personal Tool Demo")
        print("=" * 50)

        # Check service
        if not tool.is_service_available():
            print(" TokenGuard service not available")
            print("   Make sure the service is running:")
            print("   TOKENGUARD_SERVICE_MODE=standard python main.py")
            return

        print(" TokenGuard service is available")

        # Demo scenarios
        scenarios = [
            ("High confidence, short", "This is a concise answer.", 0.9),
            ("Medium confidence, medium length", "This is a moderately detailed response that provides good information but could potentially be shortened if the confidence is low enough.", 0.7),
            ("Low confidence, long", "This is a very long and verbose response that goes into extensive detail about the topic, covering many aspects and providing comprehensive information that might benefit from pruning if the confidence level is not sufficiently high to justify keeping all this content. The response continues with additional details and explanations that make it quite lengthy overall. Furthermore, there are more points to consider when evaluating this type of content generation and optimization process. Additional context and background information helps provide a more complete understanding of the subject matter being discussed. The comprehensive nature of this response demonstrates how verbose AI-generated content can become when confidence levels are not properly managed and optimized for efficiency and relevance.", 0.4)
        ]

        print("\n Testing Response Optimization")
        print("-" * 40)

        for name, text, confidence in scenarios:
            print(f"\n Scenario: {name}")
            print(f"   Confidence: {confidence}")
            print(f"   Length: {len(text)} chars")

            result = tool.optimize_response(text, confidence)

            print(f"   Action: {result['action']}")
            print(f"   Response Time: {result.get('response_time', 0):.3f}s")

            if result['action'] == 'prune':
                orig_len = result.get('original_length', 0)
                pruned_len = result.get('pruned_length', 0)
                print(f"   Tokens Saved: {orig_len - pruned_len}")
                print(f"   Reason: {result.get('reason', 'N/A')}")

        # Show final metrics
        print("\n Demo Metrics")
        print("-" * 40)
        metrics = tool.get_metrics()
        print(f"   Total Requests: {metrics['requests_total']}")
        print(f"   Responses Pruned: {metrics['pruned_responses']}")
        print(f"   Total Tokens Saved: {metrics['tokens_saved']}")
        print(f"   Average Response Time: {metrics['avg_response_time']:.3f}s")

        print("\n Demo complete!")
        print(" Use 'python tokenguard_tool.py --help' for more options")

if __name__ == "__main__":
    main()