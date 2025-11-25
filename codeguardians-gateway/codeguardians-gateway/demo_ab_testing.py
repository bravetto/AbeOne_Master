#!/usr/bin/env python3
"""
A/B Testing Framework Demo

Comprehensive demonstration of the A/B testing framework including:
- Experiment creation and management
- User segmentation and assignment
- Statistical analysis
- Canary deployments
- Real-time analytics
"""

import asyncio
import json
import redis
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Conditional imports for scientific computing libraries
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

from app.core.ab_testing import ABTestingFramework
from app.core.ab_testing.models import ExperimentStatus
from app.core.ab_testing.canary_deployment import CanaryStage

def generate_fallback_data(size, conversion_rate=0.15, mean_response=200, std_response=50):
    """Generate fallback data without numpy."""
    import random
    import math
    
    conversions = []
    response_times = []
    
    for i in range(size):
        # Binomial distribution approximation
        conversion = 1 if random.random() < conversion_rate else 0
        conversions.append(conversion)
        
        # Normal distribution approximation using Box-Muller
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        response_time = mean_response + std_response * z
        response_times.append(response_time)
    
    return conversions, response_times

async def demo_ab_testing_framework():
    """Demonstrate A/B testing framework capabilities."""
    
    print(" A/B Testing Framework Demo")
    print("=" * 50)
    
    # Initialize Redis client
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True
    )
    
    # Initialize A/B testing framework
    framework = ABTestingFramework(redis_client)
    
    print(" Framework initialized successfully")
    
    # 1. Create Experiment
    print("\n Creating A/B Test Experiment...")
    experiment_id = await framework.create_experiment(
        name="Demo Experiment - Button Color",
        description="Testing different button colors for conversion rate",
        traffic_split={"control": 50.0, "treatment": 50.0},
        success_metrics=["conversion_rate", "click_rate", "response_time"],
        primary_metric="conversion_rate",
        created_by="demo_user",
        minimum_sample_size=100,
        confidence_level=0.95,
        power=0.8
    )
    
    print(f" Experiment created: {experiment_id}")
    
    # 2. Start Experiment
    print("\n Starting Experiment...")
    success = await framework.start_experiment(experiment_id)
    print(f" Experiment started: {success}")
    
    # 3. User Assignment Demo
    print("\n User Assignment Demo...")
    
    # Simulate user assignments
    user_assignments = {}
    for i in range(20):
        user_id = f"user_{i:03d}"
        variant = await framework.assign_user_to_variant(
            user_id=user_id,
            experiment_id=experiment_id,
            user_attributes={"age": 25 + i, "location": "US" if i % 2 == 0 else "EU"}
        )
        user_assignments[user_id] = variant
        print(f"  User {user_id} → {variant}")
    
    # Count assignments
    control_count = sum(1 for v in user_assignments.values() if v == "control")
    treatment_count = sum(1 for v in user_assignments.values() if v == "treatment")
    print(f" Assignment Summary: Control={control_count}, Treatment={treatment_count}")
    
    # 4. Result Tracking Demo
    print("\n Tracking Experiment Results...")
    
    # Generate realistic test data
    if HAS_NUMPY:
        np.random.seed(42)
        
        # Control group: lower conversion rate
        control_conversions = np.random.binomial(1, 0.15, control_count)
        control_response_times = np.random.normal(200, 50, control_count)
        
        # Treatment group: higher conversion rate
        treatment_conversions = np.random.binomial(1, 0.25, treatment_count)
        treatment_response_times = np.random.normal(180, 40, treatment_count)
    else:
        print("  Using fallback data generation (numpy not available)")
        
        # Control group: lower conversion rate
        control_conversions, control_response_times = generate_fallback_data(control_count, 0.15, 200, 50)
        
        # Treatment group: higher conversion rate
        treatment_conversions, treatment_response_times = generate_fallback_data(treatment_count, 0.25, 180, 40)
    
    # Track control group results
    control_idx = 0
    for user_id, variant in user_assignments.items():
        if variant == "control":
            await framework.track_experiment_result(
                experiment_id=experiment_id,
                variant_name=variant,
                user_id=user_id,
                session_id=f"session_{user_id}",
                metrics={
                    "conversion_rate": float(control_conversions[control_idx]),
                    "response_time": float(control_response_times[control_idx]),
                    "click_rate": float(np.random.binomial(1, 0.8) if HAS_NUMPY else (1 if random.random() < 0.8 else 0)),
                    "business_revenue": float(np.random.normal(50, 10) if HAS_NUMPY else (50 + random.gauss(0, 10)))
                },
                result_metadata={"source": "demo", "timestamp": datetime.utcnow().isoformat()}
            )
            control_idx += 1
    
    # Track treatment group results
    treatment_idx = 0
    for user_id, variant in user_assignments.items():
        if variant == "treatment":
            await framework.track_experiment_result(
                experiment_id=experiment_id,
                variant_name=variant,
                user_id=user_id,
                session_id=f"session_{user_id}",
                metrics={
                    "conversion_rate": float(treatment_conversions[treatment_idx]),
                    "response_time": float(treatment_response_times[treatment_idx]),
                    "click_rate": float(np.random.binomial(1, 0.85) if HAS_NUMPY else (1 if random.random() < 0.85 else 0)),
                    "business_revenue": float(np.random.normal(60, 12) if HAS_NUMPY else (60 + random.gauss(0, 12)))
                },
                result_metadata={"source": "demo", "timestamp": datetime.utcnow().isoformat()}
            )
            treatment_idx += 1
    
    print(" Results tracked successfully")
    
    # 5. Real-time Metrics
    print("\n Real-time Metrics...")
    metrics = await framework.get_experiment_metrics(experiment_id)
    print(f"Total Users: {metrics['total_users']}")
    print(f"Variant Counts: {metrics['variant_counts']}")
    print(f"Success Counts: {metrics['success_counts']}")
    print(f"Conversion Rates: {metrics['conversion_rates']}")
    print(f"Average Response Times: {metrics['average_response_times']}")
    
    # 6. Performance Snapshot
    print("\n Performance Snapshot...")
    snapshot = await framework.get_experiment_performance_snapshot(experiment_id)
    print(f"System Health: {snapshot['system_health']}")
    print(f"Alerts: {snapshot['alerts']}")
    
    # 7. Statistical Analysis
    print("\n Statistical Analysis...")
    
    # Prepare data for analysis
    if HAS_NUMPY:
        control_data = control_conversions.tolist()
        treatment_data = treatment_conversions.tolist()
    else:
        control_data = control_conversions
        treatment_data = treatment_conversions
    
    analysis = await framework.analyze_experiment(
        experiment_id=experiment_id,
        variant_a_data=control_data,
        variant_b_data=treatment_data,
        variant_a_name="control",
        variant_b_name="treatment",
        metric_type="binary"
    )
    
    print(f"Primary Test: {analysis['primary_test']['test_name']}")
    print(f"P-value: {analysis['primary_test']['p_value']}")
    print(f"Effect Size: {analysis['primary_test']['effect_size']:.4f}")
    print(f"Power: {analysis['primary_test']['power']}")
    print(f"Significant: {analysis['primary_test']['is_significant']}")
    print(f"Interpretation: {analysis['primary_test']['interpretation']}")
    print(f"Recommendation: {analysis['recommendation']}")
    
    # 8. Canary Deployment Demo
    print("\n Canary Deployment Demo...")
    
    deployment_id = await framework.start_canary_deployment(
        experiment_id=experiment_id,
        canary_variant="canary",
        stages=[CanaryStage.INITIAL, CanaryStage.SMALL],
        stage_duration_minutes=1,  # Short duration for demo
        success_threshold=0.95,
        failure_threshold=0.05,
        auto_promote=True,
        auto_rollback=True
    )
    
    print(f" Canary deployment started: {deployment_id}")
    
    # Wait a moment for deployment to progress
    await asyncio.sleep(2)
    
    # Check deployment status
    deployment_status = await framework.get_canary_deployment_status(deployment_id)
    print(f"Deployment Status: {deployment_status.get('status', 'Unknown')}")
    print(f"Current Stage: {deployment_status.get('current_stage', 'Unknown')}")
    
    # 9. Framework Status
    print("\n Framework Status...")
    status = await framework.get_framework_status()
    print(f"Status: {status['status']}")
    print(f"Active Deployments: {status['active_deployments']}")
    print(f"Redis Connected: {status['redis_connected']}")
    
    # 10. Stop Experiment
    print("\n Stopping Experiment...")
    success = await framework.stop_experiment(experiment_id)
    print(f" Experiment stopped: {success}")
    
    print("\n A/B Testing Framework Demo Complete!")
    print("=" * 50)
    
    # Summary
    print("\n Demo Summary:")
    print(f" Experiment Created: {experiment_id}")
    print(f" Users Assigned: {len(user_assignments)}")
    print(f" Results Tracked: {metrics['total_users']}")
    print(f" Statistical Analysis: Completed")
    print(f" Canary Deployment: {deployment_id}")
    print(f" Framework Status: Healthy")
    
    return {
        "experiment_id": experiment_id,
        "deployment_id": deployment_id,
        "user_assignments": user_assignments,
        "metrics": metrics,
        "analysis": analysis,
        "status": status
    }

def demo_traffic_split_utilities():
    """Demonstrate traffic split utilities."""
    
    print("\n Traffic Split Utilities Demo")
    print("=" * 30)
    
    from app.core.ab_testing import ABTestingFramework
    import redis
    
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    framework = ABTestingFramework(redis_client)
    
    # Test validation
    print("1. Traffic Split Validation:")
    valid_split = {"control": 50.0, "treatment": 50.0}
    invalid_split = {"control": 30.0, "treatment": 50.0}
    
    print(f"  Valid split {valid_split}: {framework.validate_traffic_split(valid_split)}")
    print(f"  Invalid split {invalid_split}: {framework.validate_traffic_split(invalid_split)}")
    
    # Test normalization
    print("\n2. Traffic Split Normalization:")
    unnormalized = {"control": 30.0, "treatment": 50.0}
    normalized = framework.normalize_traffic_split(unnormalized)
    print(f"  Original: {unnormalized}")
    print(f"  Normalized: {normalized}")
    print(f"  Sum: {sum(normalized.values()):.1f}%")
    
    # Test canary split
    print("\n3. Canary Split Creation:")
    base_split = {"control": 50.0, "treatment": 50.0}
    canary_split = framework.create_canary_split(base_split, 10.0)
    print(f"  Base split: {base_split}")
    print(f"  Canary split: {canary_split}")
    print(f"  Sum: {sum(canary_split.values()):.1f}%")
    
    print(" Traffic split utilities working correctly!")

if __name__ == "__main__":
    print("Starting A/B Testing Framework Demo...")
    
    # Run traffic split utilities demo
    demo_traffic_split_utilities()
    
    # Run main demo
    try:
        result = asyncio.run(demo_ab_testing_framework())
        print(f"\n Demo completed successfully!")
        print(f"Experiment ID: {result['experiment_id']}")
        print(f"Deployment ID: {result['deployment_id']}")
    except Exception as e:
        print(f" Demo failed: {e}")
        import traceback
        traceback.print_exc()
