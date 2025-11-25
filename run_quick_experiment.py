#!/usr/bin/env python3

import json
import os
from datetime import datetime
from ai_agent.main import analyze_logs

# Test configurations
CONFIGS = [
    {"name": "Short Range", "minutes": 5},
    {"name": "Medium Range", "minutes": 15},
    {"name": "Long Range", "minutes": 30}
]

def run_experiments():
    """Run experiments"""
    print("\n" + "="*70)
    print("  Running Experiments")
    print("="*70 + "\n")
    
    results = []
    
    for i, config in enumerate(CONFIGS, 1):
        print(f"[{i}/{len(CONFIGS)}] {config['name']}: {config['minutes']} minutes")
        
        try:
            result = analyze_logs(
                minutes=config['minutes'],
                send_to_discord=False,
            )
            
            print(f"  AI Detected Status: {result['result'].status}")
            print(f"  Time: {result['metrics']['analysis_time_seconds']} seconds\n")
            
            results.append({
                "config": config,
                "status": result['result'].status,
                "summary": result['result'].summary,
                "metrics": result['metrics']
            })
        except Exception as e:
            print(f"  Failed: {e}\n")
    
    return results

def generate_report(results):
    """Generate report"""
    report = f"""# Experiment Report

## Experiment Results

| Config | Time Range | Log Count | Detected Status | Time (seconds) |
|--------|------------|-----------|-----------|----------------|
"""
    
    for r in results:
        report += f"| {r['config']['name']} | {r['config']['minutes']} minutes | {r['metrics']['log_count']} logs | {r['status']} | {r['metrics']['analysis_time_seconds']:.2f} |\n"
    
    # Calculate average
    avg_time = sum(r['metrics']['analysis_time_seconds'] for r in results) / len(results)
    
    report += f"""
## Performance Analysis

- Average Time: {avg_time:.2f} seconds
- Short Range: {results[0]['metrics']['analysis_time_seconds']:.2f} seconds
- Medium Range: {results[1]['metrics']['analysis_time_seconds']:.2f} seconds
- Long Range: {results[-1]['metrics']['analysis_time_seconds']:.2f} seconds
- From Short Range to Medium Range Time Increase: {results[1]['metrics']['analysis_time_seconds'] / results[0]['metrics']['analysis_time_seconds']:.1f}x
- From Medium Range to Long Range Time Increase: {results[-1]['metrics']['analysis_time_seconds'] / results[1]['metrics']['analysis_time_seconds']:.1f}x
- From Short Range to Long Range Time Increase: {results[-1]['metrics']['analysis_time_seconds'] / results[0]['metrics']['analysis_time_seconds']:.1f}x
"""
    
    return report

def prepare_output_directory():
    """Ask user for a folder name and prepare output directory."""
    base_dir = os.path.join(os.getcwd(), "experiment-results")
    os.makedirs(base_dir, exist_ok=True)

    default_name = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    folder_name = input(f"Enter a name for this experiment run [{default_name}]: ").strip()
    if not folder_name:
        folder_name = default_name

    run_dir = os.path.join(base_dir, folder_name)
    os.makedirs(run_dir, exist_ok=True)
    print(f"\nResults will be saved under: {run_dir}\n")
    return run_dir


def main():

    output_dir = prepare_output_directory()
    
    for i in range(5):
        print(f"Running experiment {i+1} of 5...")
        # Run experiments
        results = run_experiments()
        print(f"✓ Experiment {i+1} complete!")
        # Generate report
        report = generate_report(results)

        report_path = os.path.join(output_dir, f'Experiment_Report_{i+1}.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Report generated: {report_path}\n")
        
        # Save raw data
        json_path = os.path.join(output_dir, f'experiment_results_{i+1}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✓ Data saved: {json_path}\n")

    print(f"✓ All experiments complete!")


if __name__ == "__main__":
    main()
