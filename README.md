# Observability for Multi-layer IoT System in the LLM Era

This project demonstrates a multi-layer IoT observability and intelligent operations loop that spans from the device layer to the cloud, integrates AI and Human-in-the-loop workflows, and highlights the synergistic value of Observability × AI × Human across a multi-continuum environment.
![idea](img/idea.png)

# Motivation and Goal
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


# What I learned
## Building an end-to-end IoT testing environment
## Constructing observability for an IoT system
## LLM system integration, prompt engineering, and log analysis with LLMs
## Experiment design skills
## Measuring QoA when using LLMs for log analysis

# QoA design
## Prerequisites
1. Use `generate_test_data.py` for fast log generation.
2. The generated logs follow the same format we ingest into Loki from `cloud_service.py`.
3. The simulated scenarios match those in `simulator.py`: (1) Normal Operation, (2) Cooling Failure.
## QoA measurements
### Different time windows (1 / 15 / 30 minutes)
1. Normal condition detection across each window:
   1. Response-time analysis
   2. Accuracy impact
2. Real-time failure detection (fault occurs within the last minute) across each window:
   1. Response-time analysis
   2. Accuracy impact
### Same time window (30 minutes)
1. Intermittent failures (tests AI recognition of complex patterns)
   - 5 minutes abnormal, 5 minutes normal, alternating
2. Impact of past anomalies on real-time detection
- First 10 minutes abnormal, last 20 minutes normal