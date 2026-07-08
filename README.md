# 🛡️ Enterprise Token-Efficient Routing Hub
**Track 1 Optimization Panel - Deployed on AMD Developer Cloud & Fireworks AI Infrastructure**

## 💡 Project Overview
An automated, containerized hybrid routing agent engineered to solve the commercial scalability and cost limitations of enterprise LLM deployments. By sitting between a zero-cost local inference node and high-performance remote AMD Instinct GPU clusters via Fireworks AI managed endpoints, the engine intelligently delegates incoming tasks based on real-time token footprint metrics and semantic reasoning triggers.


## 📊 Strategic Value Proposition & Business Model
* **The Problem**: Relying entirely on heavy cloud APIs introduces unsustainable corporate cost scaling, token budget waste, and unmanaged latency spikes.
* **The Solution**: A modular routing gateway that maximizes hardware efficiency, providing strict budget guardrails while guaranteeing 100% reasoning accuracy.
* **Market Scope (TAM/SAM)**: Targeted at enterprise software architectures deploying production-grade conversational agents, automated data parsing, and continuous code optimization pipelines.

---

## 🛠️ Technology Stack & Architecture
* **Core Engine**: Python 3.11, Tiktoken (`cl100k_base` tokenizer layout)
* **Frontend Dashboard**: Streamlit (Native eye-friendly Dark-Mode Framework)
* **Container Layer**: Docker (Multi-stage lightweight Linux configuration)
* **Target Compute Infrastructure**: AMD Instinct MI300X Hardware Nodes & Fireworks AI Managed Endpoints

---

## 🚀 Local Deployment & Verification

### Prerequisites
Ensure you have Docker Desktop running on your host machine.

### 1. Build the Isolated Container
Execute this command in your terminal to compile the container image using the optimized registry mirror:
```bash
docker build -t amd-router-test .
```

### 2. Launch the Web Interface
Boot the container and map the internal web server network port directly to your local machine browser layout:
```bash
docker run --rm -p 8501:8501 amd-router-test
```

Once initialized, navigate to `http://localhost:8501` in your web browser to interact with the real-time dynamic dashboard.

---

## 🛠️ Local Verification & Development Deployment

Instinct Gate is fully containerized and strictly adheres to the official AMD Hackathon Track 1 execution runtime contract. The container operating architecture is completely stateless, dynamic, and free of hardcoded variables.

### 📦 1. Public Container Registry Ingestion
The compiled cross-platform `linux/amd64` multi-stage build manifest is hosted publicly on the GitHub Container Registry. Verify or pull the production layers using an authenticated or anonymous socket pass:
```bash
docker pull ghcr.io/dwayne-dcosta/amd-hackathon-prep:latest
```

### 🚢 2. Running Local Grader Pipeline Simulation
To simulate the automated grading harness evaluation locally, mount your task input/output directories and pass the required environment configuration variables at runtime:

```bash
docker run --rm \
  -v \$(pwd)/input:/input \
  -v \$(pwd)/output:/output \
  -e FIREWORKS_API_KEY="your_api_key_here" \
  -e FIREWORKS_BASE_URL="https://api.fireworks.ai/inference/v1/" \
  -e ALLOWED_MODELS="minimax-m3,gemma-4-31b-it" \
  ghcr.io/dwayne-dcosta/amd-hackathon-prep:latest
```

### 📋 3. Input / Output Data Contract Enforcement
* **Ingestion Portal:** Reads structured array strings sequentially from `/input/tasks.json` matching the `[{"task_id": "...", "prompt": "..."}]` schema layout.
* **Egress Mapping:** Outputs valid, machine-parsable JSON matching the required schema to `/output/results.json` before signaling execution complete via a clean exit code (`exit 0`).
