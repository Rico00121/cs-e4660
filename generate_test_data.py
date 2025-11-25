#!/usr/bin/env python3
import requests
import time
from datetime import datetime, timedelta
import random

LOKI_URL = "http://localhost:3100/loki/api/v1/push"

def generate_normal_log(device_id="A1", timestamp_ns=None):
    if timestamp_ns is None:
        timestamp_ns = int(time.time() * 1e9)
    
    temp = round(random.uniform(3.5, 5.0), 1)
    door = random.choice([0, 0, 0, 0, 1])  # 20% probability of opening the door. 0 means the door is closed, 1 means the door is open.
    current = round(random.uniform(4.8, 5.6), 1)
    
    log_line = (
        f"device_id={device_id} "
        f"temp_c={temp} "
        f"door_open={door} "
        f"compressor_current_a={current} "
        f"setpoint_c=4.0 "
    )
    
    return log_line, timestamp_ns

def generate_failure_log(device_id="A1", timestamp_ns=None):
    if timestamp_ns is None:
        timestamp_ns = int(time.time() * 1e9)
    
    temp = round(random.uniform(8.0, 12.0), 1)
    door = 0 
    current = round(random.uniform(6.0, 6.8), 1)
    
    log_line = (
        f"device_id={device_id} "
        f"temp_c={temp} "
        f"door_open={door} "
        f"compressor_current_a={current} "
        f"setpoint_c=4.0 "
    )
    
    return log_line, timestamp_ns

def push_to_loki(logs_with_timestamps, service_name="cloud"):
    streams = []
    
    sorted_logs = sorted(logs_with_timestamps, key=lambda x: x[1])
    
    values = [[str(ts), log] for log, ts in sorted_logs]
    
    stream = {
        "stream": {
            "service": service_name,
        },
        "values": values
    }
    streams.append(stream)
    
    payload = {"streams": streams}
    
    try:
        response = requests.post(
            LOKI_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 204:
            return True
        else:
            print(f"Loki response: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Push failed: {e}")
        return False

def generate_scenario_data(scenario="normal", start_minutes_ago=30, end_minutes_ago=0, interval_seconds=10):
    """
    Generate scenario data for the given scenario in the given time interval.
    
    Args:
        scenario: "normal" or "failure"
        start_minutes_ago: how many minutes ago to start (e.g. 30 means 30 minutes ago)
        end_minutes_ago: how many minutes ago to end (e.g. 0 means now, 10 means 10 minutes ago)
        interval_seconds: interval seconds between logs
    """
    logs = []
    
    now = datetime.now()
    start_time = now - timedelta(minutes=start_minutes_ago)
    end_time = now - timedelta(minutes=end_minutes_ago)
    
    current_time = start_time
    count = 0
    
    while current_time <= end_time:
        timestamp_ns = int(current_time.timestamp() * 1e9)
        
        if scenario == "normal":
            log_line, ts = generate_normal_log(timestamp_ns=timestamp_ns)
        else:  # failure
            log_line, ts = generate_failure_log(timestamp_ns=timestamp_ns)
        
        logs.append((log_line, ts))
        current_time += timedelta(seconds=interval_seconds)
        count += 1
    
    return logs, count

def main():
    print("="*70)
    print("  Loki test data generator")
    print("="*70)
    
    print("\nChecking Loki connection...")
    try:
        response = requests.get("http://localhost:3100/ready", timeout=3)
        print("✓ Loki is ready")
    except:
        print("✗ Loki is not running, please start it: docker-compose up -d")
        return
    
    print("\nGenerating normal scenario data (30 minutes ago → 15 minutes ago)...")
    normal_logs, normal_count = generate_scenario_data(
        scenario="normal",
        start_minutes_ago=30,
        end_minutes_ago=15,
        interval_seconds=10
    )
        
    if push_to_loki(normal_logs):
        print(f"✓ {normal_count} normal scenario logs pushed")
    else:
        print("✗ Normal scenario data push failed")
        return
    
    time.sleep(1)
    
    print("\nGenerating failure scenario data (15 minutes ago → now)...")
    failure_logs, failure_count = generate_scenario_data(
        scenario="failure",
        start_minutes_ago=15,
        end_minutes_ago=0,
        interval_seconds=10
    )
    
    if push_to_loki(failure_logs):
        print(f"✓ {failure_count} failure scenario logs pushed")
    else:
        print("✗ Failure scenario data push failed")
        return
    
    print("\n" + "="*70)
    print("✓ Data generation completed!")
    print("="*70)
    print(f"\nTotal logs generated: {normal_count + failure_count}")
    print(f"  - Normal scenario: {normal_count} logs (30 minutes ago → 15 minutes ago)")
    print(f"  - Failure scenario: {failure_count} logs (15 minutes ago → now)")
    print("\nTimeline:")
    print("  ├─ 30 minutes ago: Normal running started")
    print("  ├─ 15 minutes ago: Failure occurred ⚠️")
    print("  └─ Now: Failure ongoing")
    print("\nNow you can run the experiment: python3 run_quick_experiment.py\n")

if __name__ == "__main__":
    main()

