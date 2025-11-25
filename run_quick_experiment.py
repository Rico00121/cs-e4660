#!/usr/bin/env python3

from ai_agent.main import analyze_logs

# Test configurations
CONFIGS = [
    {"name": "Short Range", "minutes": 1},
    {"name": "Medium Range", "minutes": 5},
    {"name": "Long Range", "minutes": 15}
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
- Time Increase: {results[-1]['metrics']['analysis_time_seconds'] / results[0]['metrics']['analysis_time_seconds']:.1f}x

## Answering Research Questions

### Q1: More data or less data? Behavior change?

Observations:
- Short Range: {results[0]['status']}
- Medium Range: {results[1]['status']}
- Long Range: {results[2]['status']}

[Please fill in your analysis]

### Q2: QoA: time, accuracy, number of devices? Why?

Time Cost: from {results[0]['metrics']['analysis_time_seconds']:.2f} seconds to {results[-1]['metrics']['analysis_time_seconds']:.2f} seconds

[Please fill in your analysis]

### Q3: Try to extend the time range, behavior change? Correct?

Time Range: Short Range → Medium Range → Long Range

[Please fill in your analysis]

## Recommended Configuration

Recommended: {results[1]['config']['name']} ({results[1]['config']['minutes']} minutes, {results[1]['metrics']['log_count']} logs)

Reason: [Please fill in]
"""
    
    with open('Experiment_Report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n✓ Report generated: Experiment_Report.md\n")

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                         Quick Experiment                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run experiments
    results = run_experiments()
    
    # Generate report
    generate_report(results)
    
    # Save raw data
    # with open('experiment_results.json', 'w', encoding='utf-8') as f:
    #     json.dump(results, f, indent=2, ensure_ascii=False)
    
    # print("="*70)
    # print("✓ Complete!")
    # print("="*70)
    # print("\nView REPORT.md and fill in answers to the 3 questions\n")

if __name__ == "__main__":
    main()

