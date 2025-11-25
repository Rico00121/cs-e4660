# Cold Storage Scenario Simulation

## Overview

The simulator supports two operating scenarios that are used to test the LLM’s ability to reason about device status.

## Scenario Details

### Scenario 1: Normal Operation

**Characteristics**:
- **door_open**: Randomly 0/1 (door opens 20% of the time) to mimic occasional operator activity
- **temp_c**: 3.5–5.0 °C (4.5–5.5 °C while the door is open), indicating minor oscillation around the setpoint
- **compressor_current_a**: 4.8–5.6 A, compressor running normally
- **setpoint_c**: 4.0 °C (fixed)
---

### Scenario 2: Cooling Failure

**Characteristics**:
- **door_open**: 0 (always closed), so the temperature rise is not caused by human activity
- **temp_c**: 8.0–12.0 °C, persistently above the setpoint and unable to cool down
- **compressor_current_a**: 6.0–6.8 A, consistently high indicating abnormal compressor load
- **setpoint_c**: 4.0 °C (fixed)
---

## Sample Response
```json
{
  "device_id": "A1",
  "timestamp": 1234567890,
  "temp_c": 4.2,
  "door_open": 0,
  "compressor_current_a": 5.1,
  "setpoint_c": 4.0,
}
```

## Data Comparison

| Metric | Scenario 1 (Normal) | Scenario 2 (Failure) |
|--------|---------------------|----------------------|
| Temperature range | 3.5–5.0 °C | 8.0–12.0 °C |
| Door status | Occasionally open (20%) | Always closed |
| Compressor current | 4.8–5.6 A | 6.0–6.8 A |
| Deviation from setpoint | ±1 °C | +4 ~ 8 °C |
---
