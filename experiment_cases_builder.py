#!/usr/bin/env python3

from generate_test_data import generate_scenario_data, push_to_loki
import time

# Scenario 1: All normal (tests Q1 – behavior when only normal data exists)
def scenario_all_normal():
    """Past 30 minutes remain in normal operation"""
    print("\nScenario 1: All normal (30 minutes)")
    logs, count = generate_scenario_data(
        scenario="normal",
        start_minutes_ago=30,
        end_minutes_ago=0,
        interval_seconds=10
    )
    push_to_loki(logs)
    print(f"✓ Generated {count} normal logs")


# Scenario 2: Failure started 1 minute ago (tests real-time detection)
def scenario_failure_at_1min():
    """Normal for 29 minutes, failure begins 1 minute ago"""
    print("\nScenario 2: Failure started 1 minute ago")
    
    # Normal phase (30 → 1 minutes ago)
    normal_logs, normal_count = generate_scenario_data(
        scenario="normal",
        start_minutes_ago=30,
        end_minutes_ago=1,
        interval_seconds=10
    )
    push_to_loki(normal_logs)
    print(f"✓ Normal phase: {normal_count} logs")
    
    time.sleep(1)
    
    # Failure phase (last minute → now)
    failure_logs, failure_count = generate_scenario_data(
        scenario="failure",
        start_minutes_ago=1,
        end_minutes_ago=0,
        interval_seconds=10
    )
    push_to_loki(failure_logs)
    print(f"✓ Failure phase: {failure_count} logs")


# Scenario 3: Intermittent failure (5 minutes abnormal then 5 minutes normal, alternating – tests AI recognition of complex patterns)
def scenario_intermittent_failure():
    """5 minutes abnormal, 5 minutes normal, alternating"""
    print("\nScenario 3: Intermittent failure")
    
    # Normal phase (30 → 25 minutes ago)
    normal_logs, normal_count = generate_scenario_data(
        scenario="normal",
        start_minutes_ago=30,
        end_minutes_ago=25,
        interval_seconds=10
    )
    push_to_loki(normal_logs)
    print(f"✓ Normal phase: {normal_count} logs")
    
    time.sleep(1)
    
    # Failure phase (25 → 20 minutes ago)
    failure_logs, failure_count = generate_scenario_data(
        scenario="failure",
        start_minutes_ago=25,
        end_minutes_ago=20,
        interval_seconds=10
    )
    push_to_loki(failure_logs)
    print(f"✓ Failure phase: {failure_count} logs")
    
    time.sleep(1)
    
    # Normal phase (20 → 15 minutes ago)
    normal_logs, normal_count = generate_scenario_data(
        scenario="normal",
        start_minutes_ago=20,
        end_minutes_ago=15,
        interval_seconds=10
    )
    push_to_loki(normal_logs)
    print(f"✓ Normal phase: {normal_count} logs")

    # Failure phase (15 → 10 minutes ago)
    failure_logs, failure_count = generate_scenario_data(
        scenario="failure",
        start_minutes_ago=15,
        end_minutes_ago=10,
        interval_seconds=10
    )
    push_to_loki(failure_logs)
    print(f"✓ Failure phase: {failure_count} logs")

    # Normal phase (10 → 5 minutes ago)
    normal_logs, normal_count = generate_scenario_data(
        scenario="normal",
        start_minutes_ago=10,
        end_minutes_ago=5,
        interval_seconds=10
    )
    push_to_loki(normal_logs)
    print(f"✓ Normal phase: {normal_count} logs")

# Scenario 4: First 10 minutes abnormal, next 20 minutes normal (tests impact of past anomalies)
def scenario_past_failure_affects_real_time():
    """First 10 minutes failure, following 20 minutes normal"""
    print("\nScenario 4: First 10 minutes failure, next 20 minutes normal")
    
    # Failure phase (30 → 20 minutes ago)
    failure_logs, failure_count = generate_scenario_data(
        scenario="failure",
        start_minutes_ago=30,
        end_minutes_ago=20,
        interval_seconds=10
    )
    push_to_loki(failure_logs)
    print(f"✓ Failure phase: {failure_count} logs")
    
    time.sleep(1)
    
    # Normal phase (20 minutes ago → now)
    normal_logs, normal_count = generate_scenario_data(
        scenario="normal",
        start_minutes_ago=20,
        end_minutes_ago=0,
        interval_seconds=10
    )
    push_to_loki(normal_logs)
    print(f"✓ Normal phase: {normal_count} logs")

if __name__ == "__main__":
    print("="*70)
    print("  Custom Scenario Builder")
    print("="*70)
    print("\nSelect a scenario:")
    print("  1 - All normal (30 minutes)")
    print("  2 - Failure started 1 minute ago")
    print("  3 - Intermittent failure")
    print("  4 - First 10 minutes failure, next 20 minutes normal")
    print()
    
    choice = input("Enter scenario number [1-4]: ").strip()
    
    scenarios = {
        "1": scenario_all_normal,
        "2": scenario_failure_at_1min,
        "3": scenario_intermittent_failure,
        "4": scenario_past_failure_affects_real_time,
    }
    
    if choice in scenarios:
        scenarios[choice]()
        print("\n✓ Scenario generation complete!")
        print("Now run: python3 run_quick_experiment.py\n")
    else:
        print("Invalid selection")

