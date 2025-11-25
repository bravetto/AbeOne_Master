#!/usr/bin/env python3
"""
Comprehensive End-to-End Test for Guard Metrics and Token Savings Validation

Tests the complete flow from individual guard metrics collection through
aggregation to API exposure, with detailed validation of token savings
and business benefits calculations.
"""

import asyncio
import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Add paths for guard imports
sys.path.insert(0, 'guards/tokenguard')
sys.path.insert(0, 'guards/contextguard/src')
sys.path.insert(0, 'guards/trust-guard')
sys.path.insert(0, 'guards/trust_guard')  # Add underscore version for compatibility
sys.path.insert(0, 'codeguardians-gateway/codeguardians-gateway')

def validate_token_savings_accuracy(metrics, expected_tokens_saved: int, tolerance: float = 0.1) -> bool:
    """Validate that token savings calculations are accurate"""
    actual_tokens_saved = metrics.tokens_saved
    expected_min = expected_tokens_saved * (1 - tolerance)
    expected_max = expected_tokens_saved * (1 + tolerance)
    
    is_accurate = expected_min <= actual_tokens_saved <= expected_max
    if not is_accurate:
        print(f"   WARNING: Token savings accuracy issue: expected ~{expected_tokens_saved}, got {actual_tokens_saved}")
    return is_accurate

def validate_business_benefits_calculation(metrics, expected_cost_savings: float, tolerance: float = 0.1) -> bool:
    """Validate business benefits calculations are reasonable"""
    actual_cost_savings = metrics.cost_savings_usd
    expected_min = expected_cost_savings * (1 - tolerance)
    expected_max = expected_cost_savings * (1 + tolerance)
    
    is_accurate = expected_min <= actual_cost_savings <= expected_max
    if not is_accurate:
        print(f"   WARNING: Cost savings calculation issue: expected ~${expected_cost_savings:.2f}, got ${actual_cost_savings:.2f}")
    return is_accurate

async def test_comprehensive_guard_metrics():
    """Test comprehensive guard metrics with detailed validation"""
    print("COMPREHENSIVE GUARD METRICS VALIDATION")
    print("="*60)

    validation_results = {
        'tokenguard': {'passed': False, 'details': {}},
        'contextguard': {'passed': False, 'details': {}},
        'trustguard': {'passed': False, 'details': {}},
        'aggregation': {'passed': False, 'details': {}},
        'api_integration': {'passed': False, 'details': {}}
    }

    try:
        # Test 1: TokenGuard metrics with comprehensive validation
        print("1. Testing TokenGuard metrics with token savings validation...")
        from guards.tokenguard.tokenguard.metrics import TokenGuardMetricsCollector

        collector = TokenGuardMetricsCollector()
        
        # Test with realistic data for accurate validation
        test_cases = [
            {
                'input': "This is a very long verbose response that contains a lot of unnecessary words and could definitely benefit from compression to reduce token usage and improve efficiency.",
                'output': "This response could be compressed.",
                'confidence': 0.85,
                'response_time': 125.0,
                'expected_tokens_saved': 22  # 27 input words - 5 output words = 22 saved
            },
            {
                'input': "Another lengthy explanation with extensive detail that might not be essential for the user's understanding but takes up valuable token space.",
                'output': "Another explanation with detail.",
                'confidence': 0.78,
                'response_time': 98.0,
                'expected_tokens_saved': 17  # 21 input words - 4 output words = 17 saved
            }
        ]
        
        total_expected_tokens_saved = 0
        for i, test_case in enumerate(test_cases):
            collector.record_pruning_operation(
                input_text=test_case['input'],
                output_text=test_case['output'],
                confidence=test_case['confidence'],
                response_time_ms=test_case['response_time'],
                success=True
            )
            total_expected_tokens_saved += test_case['expected_tokens_saved']

        metrics = collector.get_current_metrics()
        benefits = metrics.get_benefits_summary()

        # Validate token savings accuracy
        token_accuracy = validate_token_savings_accuracy(metrics, total_expected_tokens_saved)
        
        # Validate business benefits calculation
        expected_cost_savings = (total_expected_tokens_saved / 1000) * 0.002  # $0.002 per 1000 tokens
        cost_accuracy = validate_business_benefits_calculation(metrics, expected_cost_savings, tolerance=0.5)  # More lenient tolerance

        print(f"   OK: Requests processed: {metrics.requests_processed}")
        print(f"   COST: Cost savings: ${metrics.cost_savings_usd:.2f}")
        print(f"   RATIO: Compression ratio: {metrics.compression_ratio:.1%}")
        print(f"   TOKENS: Tokens saved: {metrics.tokens_saved}")
        print(f"   BENEFITS: Business benefits: {len(benefits)} categories available")
        
        validation_results['tokenguard']['passed'] = token_accuracy and cost_accuracy
        validation_results['tokenguard']['details'] = {
            'tokens_saved': metrics.tokens_saved,
            'cost_savings': metrics.cost_savings_usd,
            'compression_ratio': metrics.compression_ratio,
            'token_accuracy': token_accuracy,
            'cost_accuracy': cost_accuracy
        }

        # Test 2: ContextGuard metrics with validation
        print("\n2. Testing ContextGuard metrics with productivity validation...")
        from guards.contextguard.src.contextguard.metrics import ContextGuardMetricsCollector

        ctx_collector = ContextGuardMetricsCollector()
        
        # Test multiple context operations
        context_test_cases = [
            {'slots': 15, 'success': True, 'relevance': 0.92, 'time': 45.0},
            {'slots': 8, 'success': True, 'relevance': 0.88, 'time': 32.0},
            {'slots': 12, 'success': False, 'relevance': 0.65, 'time': 28.0}
        ]
        
        for test_case in context_test_cases:
            ctx_collector.record_context_operation(
                slots_used=test_case['slots'],
                retrieval_success=test_case['success'],
                relevance_score=test_case['relevance'],
                response_time_ms=test_case['time'],
                success=test_case['success']
            )

        ctx_metrics = ctx_collector.get_current_metrics()
        ctx_benefits = ctx_metrics.get_benefits_summary()

        # Validate productivity calculations
        expected_success_rate = 2/3  # 2 out of 3 operations successful
        expected_productivity = expected_success_rate * 25.0  # 25% base productivity boost
        productivity_accuracy = abs(ctx_metrics.user_productivity_increase - expected_productivity) < 5.0

        print(f"   OK: Active memory slots: {ctx_metrics.active_memory_slots}")
        print(f"   RELEVANCE: Context relevance: {ctx_metrics.context_relevance_score:.2f}")
        print(f"   PRODUCTIVITY: Productivity increase: {ctx_metrics.user_productivity_increase:.1f}%")
        print(f"   BENEFITS: Business benefits: {len(ctx_benefits)} categories available")
        
        validation_results['contextguard']['passed'] = productivity_accuracy
        validation_results['contextguard']['details'] = {
            'memory_slots': ctx_metrics.active_memory_slots,
            'relevance_score': ctx_metrics.context_relevance_score,
            'productivity_increase': ctx_metrics.user_productivity_increase,
            'productivity_accuracy': productivity_accuracy
        }

        # Test 3: TrustGuard metrics with safety validation
        print("\n3. Testing TrustGuard metrics with safety validation...")
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "trustguard_metrics",
            "guards/trust-guard/trustguard/metrics.py"
        )
        trust_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(trust_module)

        trust_collector = trust_module.TrustGuardMetricsCollector()
        
        # Test multiple safety operations
        safety_test_cases = [
            {'violations': 0, 'blocked': False, 'compliance': 0.97, 'time': 23.0},
            {'violations': 1, 'blocked': True, 'compliance': 0.94, 'time': 31.0},
            {'violations': 0, 'blocked': False, 'compliance': 0.99, 'time': 19.0}
        ]
        
        for test_case in safety_test_cases:
            trust_collector.record_safety_operation(
                violations_detected=test_case['violations'],
                content_blocked=test_case['blocked'],
                compliance_score=test_case['compliance'],
                response_time_ms=test_case['time'],
                success=True
            )

        trust_metrics = trust_collector.get_current_metrics()
        trust_benefits = trust_metrics.get_benefits_summary()

        # Validate safety calculations
        expected_violation_rate = 1/3  # 1 out of 3 operations had violations
        expected_risk_reduction = expected_violation_rate * 80.0  # 80% base risk reduction
        risk_accuracy = abs(trust_metrics.legal_risk_reduction - expected_risk_reduction) < 10.0

        print(f"   OK: Violations blocked: {trust_metrics.violations_blocked}")
        print(f"   COMPLIANCE: Compliance score: {trust_metrics.compliance_score:.2f}")
        print(f"   RISK: Risk reduction: {trust_metrics.legal_risk_reduction:.1f}%")
        print(f"   BENEFITS: Business benefits: {len(trust_benefits)} categories available")
        
        validation_results['trustguard']['passed'] = risk_accuracy
        validation_results['trustguard']['details'] = {
            'violations_blocked': trust_metrics.violations_blocked,
            'compliance_score': trust_metrics.compliance_score,
            'risk_reduction': trust_metrics.legal_risk_reduction,
            'risk_accuracy': risk_accuracy
        }

        # Test 4: Metrics Aggregation Testing
        print("\n4. Testing Guard Metrics Aggregation...")
        try:
            from app.core.guard_metrics_aggregator import GuardMetricsAggregator
            
            aggregator = GuardMetricsAggregator()
            
            # Test aggregation (this will collect from the guards we just populated)
            aggregated_metrics = await aggregator.aggregate_all_metrics()
            
            # Validate aggregation results
            aggregation_valid = (
                aggregated_metrics.total_requests > 0 and
                aggregated_metrics.tokens_saved_total > 0 and
                aggregated_metrics.total_cost_savings_usd > 0
            )
            
            print(f"   OK: Aggregated requests: {aggregated_metrics.total_requests}")
            print(f"   COST: Aggregated cost savings: ${aggregated_metrics.total_cost_savings_usd:.2f}")
            print(f"   TOKENS: Aggregated tokens saved: {aggregated_metrics.tokens_saved_total}")
            print(f"   RATIO: Overall compression ratio: {aggregated_metrics.overall_compression_ratio:.1%}")
            
            validation_results['aggregation']['passed'] = aggregation_valid
            validation_results['aggregation']['details'] = {
                'total_requests': aggregated_metrics.total_requests,
                'total_cost_savings': aggregated_metrics.total_cost_savings_usd,
                'tokens_saved_total': aggregated_metrics.tokens_saved_total,
                'compression_ratio': aggregated_metrics.overall_compression_ratio
            }
            
        except Exception as e:
            print(f"   WARNING: Aggregation test failed: {e}")
            validation_results['aggregation']['passed'] = False
            validation_results['aggregation']['details'] = {'error': str(e)}

        # Test 5: API Integration Testing
        print("\n5. Testing API Integration...")
        try:
            from app.api.v1.analytics import router
            
            # Test that API routes are properly configured
            routes = [route.path for route in router.routes if hasattr(route, 'path')]
            expected_routes = [
                "/benefits/overview",
                "/benefits/detailed", 
                "/performance/dashboard"
            ]
            
            api_routes_valid = all(route in str(routes) for route in expected_routes)
            
            print(f"   OK: Analytics API routes configured: {len(routes)} routes")
            print(f"   ENDPOINTS: Available endpoints: {', '.join(expected_routes)}")
            
            validation_results['api_integration']['passed'] = api_routes_valid
            validation_results['api_integration']['details'] = {
                'total_routes': len(routes),
                'expected_routes_found': api_routes_valid,
                'available_routes': routes
            }
            
        except Exception as e:
            print(f"   WARNING: API integration test failed: {e}")
            validation_results['api_integration']['passed'] = False
            validation_results['api_integration']['details'] = {'error': str(e)}

        # Calculate combined benefits (what MCP client would receive)
        print("\n6. Final Combined Analytics Summary...")

        total_requests = metrics.requests_processed + ctx_metrics.requests_processed + trust_metrics.requests_processed
        total_cost_savings = metrics.cost_savings_usd + 0  # Other guards don't have direct cost savings
        total_violations = trust_metrics.violations_blocked
        total_productivity = ctx_metrics.user_productivity_increase

        print("   OK: Combined metrics calculated")
        print(f"   REQUESTS: Total requests: {total_requests}")
        print(f"   COST: Total cost savings: ${total_cost_savings:.2f}")
        print(f"   SAFETY: Total violations blocked: {total_violations}")
        print(f"   PRODUCTIVITY: Combined productivity gain: {total_productivity:.1f}%")

        # Generate comprehensive validation report
        print("\n" + "="*60)
        print("COMPREHENSIVE VALIDATION REPORT")
        print("="*60)
        
        total_tests = len(validation_results)
        passed_tests = sum(1 for result in validation_results.values() if result['passed'])
        
        print(f"Overall Test Results: {passed_tests}/{total_tests} tests passed")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\nDetailed Results:")
        for test_name, result in validation_results.items():
            status = "PASSED" if result['passed'] else "FAILED"
            print(f"  {test_name.upper()}: {status}")
            if result['details']:
                for key, value in result['details'].items():
                    if key != 'error':
                        print(f"    {key}: {value}")
                if 'error' in result['details']:
                    print(f"    Error: {result['details']['error']}")
        
        if passed_tests == total_tests:
            print("\nSUCCESS: ALL SYSTEMS VALIDATED - MCP SERVER READY!")
            print("\nYour MCP server provides comprehensive client-side benefits:")
            print("- Token savings and cost optimization metrics")
            print("- Productivity improvements and context benefits") 
            print("- Safety compliance and violation prevention stats")
            print("- Per-guard detailed breakdowns for business intelligence")
            print("- Real-time aggregation and API exposure")

            print("\nAVAILABLE API ENDPOINTS:")
            print("- GET /api/v1/analytics/benefits/overview")
            print("- GET /api/v1/analytics/benefits/detailed")
            print("- GET /api/v1/analytics/performance/dashboard")
            print("- GET /api/v1/analytics/guards/{guard_name}/metrics")
        else:
            print(f"\nWARNING: {total_tests - passed_tests} tests failed - review details above")
        
        return passed_tests == total_tests

    except Exception as e:
        print(f"ERROR: Comprehensive validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_guard_metrics_directly():
    """Legacy function for backward compatibility"""
    return test_comprehensive_guard_metrics()

async def main():
    """Main async execution function"""
    success = await test_comprehensive_guard_metrics()
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
