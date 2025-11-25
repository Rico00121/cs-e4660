# Overview
I want to build a multi-layer IoT system’s observability and intelligent operation and maintenance closed loop, from the device side to the cloud, to AI and Human-in-the-loop. This reflects the synergistic value of Observability × AI × Human in a multi-continuum environment.
![idea](img/idea.png)

# What I want to do
Through an IoT system simulation (Python simulator), it demonstrates how to use OpenTelemetry + Loki to achieve end-to-end observability, and use an AI Agent (including Discord Bot) to automatically detect anomalies, generate alarms, and accept manual confirmation to form an AI-Human-Observability closed loop.
![simplified idea](img/simplified-idea.png)

And **It will show**:
- The logs collecting from all layers of the IoT system;

- Data pipeline construction and Exporter configuration of OTel Collector;

- AI Agent’s analysis and interpretation of observation data;

- The integration of Human as a Service (HaaS) concepts in observable systems;

- Full process visualization (Grafana + Discord embed card).

# Tasks plan
## Stage 1: Observability pipeline construction ✅
Build the observation path, from Python Simulator/Gateway/Edge/Cloud → OTel Collector → Loki  → Grafana.

## Stage 2: AI Agent Anomaly Detection ✅
The AI Agent periodically reads log data, detects anomalies and pushes them to Discord, forming a closed loop of interaction.

## Stage 3: Integration and Demonstration Preparation
Complete the presentation script and documentation.


# 我学到了什么
## End-to-end IoT 测试环境的构建
## 基于 IoT 系统的可观性构建
## LLM 的系统集成, Prompt Engineering，使用 LLM 进行日志分析
## 实验设计能力
## 对于用 LLM 进行日志分析的 QoA

# 对于 QoA 的设计
## 前置条件：
1. 使用 generate_test_data.py 来进行快速的日志生成。
2. 生成日志的格式使用了和我们在 cloud_service.py中上传到 Loki 中相同的格式。
3. 对于生成日志的场景，我使用了 simulator.py实现的 Simulator 相同的场景，即 1. Normal Operation 2. Cooling Failure
## QoA 的测量方面
### 对于摄取不同时间范围的日志(1/15/30 min)
1. 检测正常的情况，对于不同时间范围的日志(1/15/30 min)
   1. 响应时间的分析
   2. 准确度的影响
2. 实时产生的故障的检测 对于不同时间范围的日志(1/15/30 min)
   1. 响应时间的分析
   2. 准确度的影响
###  在同一时间范围下（30 min）
1. 间歇性故障（测试AI识别复杂模式）
5 分钟异常，5 分钟正常，交替。
## 过去的异常对于实时故障检测的影响
前 10 分钟异常，后 20 分钟正常。