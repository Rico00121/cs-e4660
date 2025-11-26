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


# What I learned
## Building an end-to-end IoT testing environment
## Constructing observability for an IoT system
## LLM system integration, prompt engineering, and log analysis with LLMs
## Experiment design skills
## Measuring QoA when using LLMs for log analysis

# QoA design
