# Experiment Result Analysis

The conclusions below summarize the scenario folders under `experiment-results/` (see `README.md` for definitions):
- **Scenario 1** – system remains normal throughout.
- **Scenario 2** – cooling failure triggered within the most recent five minutes.
- **Scenario 3** – five minutes abnormal / five minutes normal alternating (analyzed with the 30-minute window only).
- **Scenario 4** – first ten minutes abnormal, next twenty minutes recovered (30-minute window only).

Scenario 1/2 each have five runs for Short=5 min, Medium=15 min, and Long=30 min (30 reports total). Scenario 3/4 follow the README “30-minute same-window” requirement, so only the Long=30 min window was executed (five runs each, 10 reports total).

## Research Question Breakdown

### Q1: More data or less data? Behavior change?

- **Steady normal scenabirrio (Scenario 1)**  
  - Short Range (5 min) returned `normal` in all runs, proving it captures door-induced oscillations.  
  - Medium Range produced `warning` twice, and Long Range even hit `critical` twice—long windows revive older fluctuations that had already settled.
- **Intermittent / recovery scenarios (Scenario 3 & 4, 30 min only)**  
  - Scenario 3 (intermittent failure): every Long Range run is `critical` because the 30-minute window includes the full abnormal → normal → abnormal cycle.  
  - Scenario 4 (historical residue): all Long Range runs are `critical`. As long as the window contains the first ten minutes of failure, alerts keep firing; with only the final twenty minutes (short/medium windows) the system would look normal—exactly the README experiment goal.
- **Sustained failure scenario (Scenario 2)**  
  - All fifteen runs across short/medium/long report `critical`, showing that extra data does not change the verdict in a stable failure; it only increases processing time and token usage.

**Conclusion:** Bigger windows are not automatically better. Five minutes reliably filters routine noise; fifteen minutes captures most sustained trends; thirty minutes should be used only when full historical context is explicitly required, otherwise historical artifacts bleed into real-time judgments.

### Q2: QoA (time, accuracy, device count) – performance and reasons

- **Response time**  
  - Processing time scales roughly linearly with log count: Scenario 1 rises from ~3.2 s (5 min / 26 logs) to ~5.0 s (30 min / 176 logs); Scenario 3 increases from 2.98 s to 6.40 s.  
  - Some runs (Scenario 2 Short Range up to 7.6 s) trigger multiple anomaly rules, slightly extending API latency, yet all runs remain under 8 s.
- **Accuracy (LLM vs. truth)**  
  - Scenario 1: Short window is 100% correct; medium/long misclassify 40–60% because they include earlier fluctuations.  
  - Scenario 2: All windows are 100% correct.  
  - Scenario 3: Only 15/30 min windows detect the intermittent pattern.  
  - Scenario 4: A 30-minute window keeps flagging past failures, so accuracy is 0% unless older data are downweighted.
- **Device count**  
  - Experiments currently involve a single device (device_count=1). The log format already supports multiple devices, so future work can compare multi-source robustness under the same window settings.

**Insight:** QoA hinges on matching window size to scenario dynamics. Short windows are precise but context-limited; long windows provide context but risk embedding historical noise into present conclusions.

### Q3: Extend the time range—does behavior change correctly?

- **Stable states** (Scenario 1 & 2): extending the window does not change the verdict; it simply adds ~1–2 seconds per extra ten minutes and consumes more tokens.  
- **Rapidly changing states** (Scenario 3, 30 min only): the entire window is required to see the periodic failure; short windows would miss everything.  
- **Recovered states with historical residue** (Scenario 4, 30 min only): the window still contains the early failure, so it keeps flagging `critical`. Production use should pair 30-minute analysis with window trimming or time-decay weighting.

## Conclusion

Based on the experimental results, we can summarize these recommended configurations for different usage scenarios.

- **Routine health check** – `Short Range (5 minutes)`  
  - Fast (~3 s) and sufficient to cover door activity; ideal for high-frequency monitoring. 
- **Diagnostic / secondary confirmation** – `Medium Range (15 minutes)`  
  - Captures trends and catches intermittent failures with 100% accuracy. Takes ~3.5–5.6 s and should be triggered whenever the short window looks suspicious. 
- **Incident review / historical tracing** – `Long Range (30 minutes)`  
  - Best for post-incident analysis or verifying whether a major anomaly just occurred. Not recommended for continuous alerting unless paired with sliding windows or time-decay weighting.

In summary, we can use a 5-minute window for real-time failure detection, and sometimes we also can consider is to adding a 15-minute window for secondary confirmation. When we need a deeper historical insight or intermittent-fault diagnosis, a 30-minute full-window analysis will be required.
