#!/usr/bin/env python3
"""
Performance profiling and benchmarking for TokenGuard.

This script provides the tools needed for the systematic performance validation:
1. Single-request latency benchmarking
2. CPU profiling integration
3. Memory usage analysis
4. Performance report generation
"""

import time
import statistics
import json
import sys
import argparse
from typing import List, Dict, Any
import requests


class PerformanceBenchmark:
    """Performance benchmarking and profiling for TokenGuard."""

    def __init__(self: Any, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []

    def benchmark_single_request(
        self: Any, endpoint: str, payload: Dict[str, Any], iterations: int = 100
    ) -> Dict[str, float]:
        """Benchmark a single endpoint with multiple iterations."""
        latencies = []

        print(f"Benchmarking {endpoint} with {iterations} iterations...")

        for i in range(iterations):
            start_time = time.perf_counter()

            try:
                response = requests.post(f"{self.base_url}{endpoint}", json=payload, timeout=10)
                response.raise_for_status()
            except Exception as e:
                print(f"Request {i+1} failed: {e}")
                continue

            end_time = time.perf_counter()
            latency_ms = (end_time - start_time) * 1000
            latencies.append(latency_ms)

            if (i + 1) % 10 == 0:
                print(f"  Completed {i+1}/{iterations} requests")

        if not latencies:
            raise Exception("All requests failed")

        return {
            "mean": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "p95": self._percentile(latencies, 95),
            "p99": self._percentile(latencies, 99),
            "min": min(latencies),
            "max": max(latencies),
            "std_dev": statistics.stdev(latencies) if len(latencies) > 1 else 0,
            "total_requests": len(latencies),
            "failed_requests": iterations - len(latencies),
        }

    def _percentile(self: Any, data: List[float], percentile: int) -> float:
        """Calculate percentile of a dataset."""
        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        if index == len(sorted_data):
            index -= 1
        return sorted_data[index]

    def run_comprehensive_benchmark(self: Any) -> Dict[str, Any]:
        """Run comprehensive benchmarks across different scenarios."""
        test_scenarios = [
            {
                "name": "short_text_high_confidence",
                "endpoint": "/v1/prune",
                "payload": {
                    "text": "This is a short response that should be kept." * 3,
                    "confidence": 0.9,
                },
            },
            {
                "name": "medium_text_medium_confidence",
                "endpoint": "/v1/prune",
                "payload": {
                    "text": "This is a medium length response that may or may not be pruned depending on the confidence threshold. "
                    * 10,
                    "confidence": 0.6,
                },
            },
            {
                "name": "long_text_low_confidence",
                "endpoint": "/v1/prune",
                "payload": {
                    "text": "This is a very long response that should definitely be pruned due to low confidence and excessive length. "
                    * 50,
                    "confidence": 0.4,
                },
            },
            {
                "name": "analyze_endpoint",
                "endpoint": "/v1/analyze",
                "payload": {"text": "This is a sample text for analysis. " * 20, "confidence": 0.7},
            },
        ]

        benchmark_results = {}

        for scenario in test_scenarios:
            print(f"\n=== Benchmarking {scenario['name']} ===")
            try:
                results = self.benchmark_single_request(
                    scenario["endpoint"], scenario["payload"], iterations=100
                )
                benchmark_results[scenario["name"]] = results

                # Check against SLO (20ms p95)
                slo_met = results["p95"] < 20.0
                print(
                    f"  P95 latency: {results['p95']:.2f}ms (SLO: <20ms) {'' if slo_met else ''}"
                )
                print(f"  Mean latency: {results['mean']:.2f}ms")
                print(f"  Failed requests: {results['failed_requests']}")

            except Exception as e:
                print(f"  Benchmark failed: {e}")
                benchmark_results[scenario["name"]] = {"error": str(e)}

        return benchmark_results

    def generate_performance_report(self: Any, results: Dict[str, Any]) -> str:
        """Generate a formatted performance report."""
        report = []
        report.append("# TokenGuard Performance Benchmark Report")
        report.append(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # SLO Analysis
        report.append("## Service Level Objective (SLO) Analysis")
        report.append("Target: <20ms at 95th percentile for all endpoints")
        report.append("")

        slo_passes = 0
        total_scenarios = 0

        for scenario_name, scenario_results in results.items():
            if "error" in scenario_results:
                continue

            total_scenarios += 1
            p95 = scenario_results["p95"]
            slo_met = p95 < 20.0
            if slo_met:
                slo_passes += 1

            report.append(
                f"- **{scenario_name}**: {p95:.2f}ms {' PASS' if slo_met else ' FAIL'}"
            )

        report.append("")
        report.append(
            f"**Overall SLO Compliance: {slo_passes}/{total_scenarios} scenarios passed**"
        )
        report.append("")

        # Detailed Results
        report.append("## Detailed Performance Metrics")

        for scenario_name, scenario_results in results.items():
            if "error" in scenario_results:
                report.append(f"### {scenario_name} (FAILED)")
                report.append(f"Error: {scenario_results['error']}")
                continue

            report.append(f"### {scenario_name}")
            report.append(f"- Mean: {scenario_results['mean']:.2f}ms")
            report.append(f"- Median: {scenario_results['median']:.2f}ms")
            report.append(f"- P95: {scenario_results['p95']:.2f}ms")
            report.append(f"- P99: {scenario_results['p99']:.2f}ms")
            report.append(f"- Min: {scenario_results['min']:.2f}ms")
            report.append(f"- Max: {scenario_results['max']:.2f}ms")
            report.append(f"- Std Dev: {scenario_results['std_dev']:.2f}ms")
            report.append(
                f"- Success Rate: {(scenario_results['total_requests'] / (scenario_results['total_requests'] + scenario_results['failed_requests']) * 100):.1f}%"
            )
            report.append("")

        return "\n".join(report)


def main() -> Any:
    parser = argparse.ArgumentParser(description="TokenGuard Performance Benchmark")
    parser.add_argument(
        "--url", default="http://localhost:8000", help="Base URL of TokenGuard service"
    )
    parser.add_argument("--output", help="Output file for results (optional)")
    parser.add_argument(
        "--profile", action="store_true", help="Enable CPU profiling (requires py-spy)"
    )

    args = parser.parse_args()

    # Check if service is running
    try:
        response = requests.get(f"{args.url}/health", timeout=5)
        response.raise_for_status()
        print(f" TokenGuard service is running at {args.url}")
    except Exception as e:
        print(f" Cannot connect to TokenGuard service at {args.url}: {e}")
        sys.exit(1)

    benchmark = PerformanceBenchmark(args.url)

    if args.profile:
        print("\n Starting CPU profiling...")
        print(
            "Run: py-spy record -o profile.svg -d 60 -- python -m uvicorn main:app --host 0.0.0.0 --port 8000"
        )
        print("in another terminal, then press Enter to continue...")
        input()

    print("\n Starting comprehensive benchmark...")
    results = benchmark.run_comprehensive_benchmark()

    report = benchmark.generate_performance_report(results)
    print("\n" + "=" * 50)
    print(report)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\n Report saved to {args.output}")

    # Save raw results as JSON
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(" Raw results saved to benchmark_results.json")


if __name__ == "__main__":
    main()
