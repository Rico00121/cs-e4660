# Observability for Multi-layer IoT System in the LLM Era

This project demonstrates a multi-layer IoT observability and intelligent operations loop that spans from the device layer to the cloud, integrates AI and Human-in-the-loop workflows, and highlights the synergistic value of Observability × AI × Human across a multi-continuum environment.
![idea](img/idea.png)

## Motivation and Goal
This project grew out of the observability and LLM topics covered in the course [CS-E4660](https://github.com/rdsea/sys4bigml) of Aalto CS (Advanced Topics in Software Systems). 

To explore how these two areas could fit together in a practical production setting, I built a small end-to-end prototype that includes simulated device, gateway layer, edge layer, mid-tier broker, and cloud service. Each layer has observability components so we can verify the whole system on a realistic path. 

Furthermore, on top of this prototype I designed scenario-based experiments that evaluate how an LLM-powered observability loop behaves in IoT use cases, and whether its Quality of Analysis (QoA) is good enough for real operations, and also give some [experimental results analysis](docs/Experiment_Analysis.md).

Through an IoT system simulation (Python simulator), the project demonstrates how to use OpenTelemetry (Alloy) + Loki to achieve end-to-end observability, and how to use an AI Agent (including a Discord Bot) to detect anomalies, issue alerts, and close the loop with human confirmation.

![simplified idea](img/simplified-idea.png)


In this project, **It will show**:

- The logs collecting from all layers of the IoT system;

- Data pipeline construction and Exporter configuration of OTel Collector;

- LLM's analysis and interpretation of observation data;

- The integration of Human as a Service (HaaS) concepts in observable systems;

- Full process visualization (Grafana + Discord embed card).

- LLM analysis results for time series data of different length intervals (QoA)

## Simulator Scenarios Definition
The simulator operates in two core states ([details](docs/Device_Scenarios.md)):
- **Scenario 1 – Normal Operation**: door opens sporadically (about 20% of readings), temperature oscillates around 4 °C (3.5–5.0 °C, or up to 5.5 °C when the door is open), and compressor current remains within 4.8–5.6 A.
- **Scenario 2 – Cooling Failure**: door stays closed, temperature rises and stays high (8.0–12.0 °C), and compressor current increases to 6.0–6.8 A because the cooling loop cannot reach the 4.0 °C setpoint.

In this prototype the entire system collects simulator-generated telemetry as unified logs, then periodically feeds them into the LLM for anomaly detection and root-cause analysis.

## QoA Experiment Design
To further verify the impact of LLM's response time, accuracy, and time window size on judgment in various IoT scenarios, I designed a series of tests to evaluate QoA in specific scenarios. The aim is to obtain data to support usability in these scenarios and to gain a deeper understanding of LLM's shortcomings and advantages in the current context.
### Prerequisites
1. Use `generate_test_data.py` for logs batch generation.
2. The generated logs follow the same format we ingest into Loki from `cloud_service.py`.
3. The simulated [scenarios](docs/Device_Scenarios.md) match those in `simulator.py`: (1) Normal Operation, (2) Cooling Failure.
### QoA Measurements
To explore the impact of LLM on **response-time** analysis and **accuracy** of time series data across different time windows, we designed the following experiment. The experiment has two dimensions. One is to examine the basic real-time fault detection capability of LLM for logs. The other specifically targets the interference of past anomalies on LLM detection results and whether LLM can identify complex fault patterns (periodic faults) over a longer time frame (30 minutes).

#### Different time windows (5 / 15 / 30 minutes)
1. Normal condition detection across each window (The impact of different time windows on LLM misjudgments)
2. Real-time failure detection (fault occurs within the last minute) across each time window. (The impact of different time windows on real-time fault detection)
#### Same time window (30 minutes)
1. Intermittent failures (tests AI recognition of complex patterns)
   - 5 minutes abnormal, 5 minutes normal, alternating
2. Impact of past anomalies on real-time detection (Past information interference)
   - First 10 minutes abnormal, last 20 minutes normal
### Experimental Results
All experimental results can be viewed in the folder /experiment-result, I provided the raw JSON data of the experiment (LLM's response) and the report. A detailed summary of the results is also available [here](docs/Experiment_Analysis.md).

# What I Learned
- A deeper understanding of observability topics.
- How to build an end-to-end IoT testing environment.
- How to construct observability for a complex system.
- How to integrate LLMs into a existing system, prompt engineering, and log analysis with LLMs.
- How to evaluate a model's QoA and how to design experiment for it.