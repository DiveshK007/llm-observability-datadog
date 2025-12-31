# LLM Observability & Incident Response with Datadog and Gemini

## Overview
Large Language Model (LLM) applications fail in subtle but high-impact ways—including silent latency degradation, uncontrolled token usage, and unexpected cost spikes. Traditional monitoring tools focus on infrastructure health and are not designed to detect or respond to model-layer failures.

This project demonstrates a production-grade observability approach for LLM systems by integrating a Gemini-powered application on Google Cloud with Datadog to provide real-time monitoring, anomaly detection, and automated incident response for AI workloads.

## Problem Statement
Modern LLM applications lack visibility into:
- Model latency degradation
- Silent inference failures
- Prompt regressions causing token/cost spikes
- AI-specific incidents that do not crash infrastructure

As a result, engineering teams struggle to detect, diagnose, and respond to LLM failures in production.

## Solution
We built an observability-first LLM system that:
- Uses Gemini (Vertex AI) for inference
- Emits LLM-specific telemetry (latency, errors, tokens, cost)
- Uses Datadog to:
  - Detect anomalies
  - Trigger alerts
  - Automatically create incidents
  - Visualize system health in a single dashboard

## Architecture
```
User → Web UI → FastAPI Backend → Gemini (Vertex AI)
                       ↓
               Datadog Telemetry
        (Metrics • Logs • Traces • Events)
                       ↓
           Monitors → Incident → Dashboard
```

## Tech Stack
- **LLM**: Google Gemini via Google Cloud Vertex AI
- **Backend**: FastAPI (Python)
- **Observability**: Datadog (APM, Metrics, Logs, Incidents)
- **Deployment**: Google Cloud Run
- **Monitoring Signals**: Latency, Error rate, Token usage, Estimated cost

## Quick Start

### Prerequisites
- Python 3.11+
- Google Cloud project with Vertex AI API enabled
- Datadog account (trial is fine)
- Service account JSON key with Vertex AI permissions

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/llm-observability-datadog.git
   cd llm-observability-datadog
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials:
   # - DD_API_KEY: Your Datadog API key
   # - GCP_PROJECT_ID: Your Google Cloud project ID
   # - GOOGLE_APPLICATION_CREDENTIALS: Path to service account JSON
   ```

4. **Run locally**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

5. **Open the app**
   - UI: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

### Traffic Generator
Simulate load to trigger Datadog monitors:
```bash
python backend/traffic_generator.py --url http://localhost:8000 --profile mixed --count 20
```

Load profiles: `normal`, `heavy`, `mixed`, `spike`

## Observability & Detection

### Custom Metrics Emitted
| Metric | Description |
|--------|-------------|
| `llm.request.latency_ms` | End-to-end request latency |
| `llm.request.error_count` | Error count by type |
| `llm.tokens.used` | Total tokens per request |
| `llm.estimated.cost_usd` | Estimated inference cost |

### Datadog Detection Rules
1. **High LLM Latency** - Triggers when avg latency > 3000ms
2. **Elevated Error Rate** - Triggers when errors > 5 in 5 min
3. **Token Usage Anomaly** - Detects abnormal token consumption
4. **Cost Spike Detection** - Alerts on cost exceeding threshold

### Incident Response
When monitors fire, Datadog automatically creates an incident with:
- Signal data and context
- Suggested next steps (runbook)
- Service and severity tags

## Repository Structure
```
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── gemini_client.py        # Vertex AI Gemini integration
│   ├── traffic_generator.py    # Load testing script
│   └── telemetry/
│       └── datadog_setup.py    # Datadog configuration
├── frontend/
│   ├── index.html              # Web UI
│   ├── styles.css              # Styling
│   └── app.js                  # Frontend logic
├── datadog/
│   ├── dashboards.json         # Dashboard export
│   └── monitors.json           # Monitor definitions
├── Dockerfile
├── requirements.txt
├── .env.example
└── LICENSE
```

## Deployment

### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy llm-observability \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DD_API_KEY=xxx,GCP_PROJECT_ID=xxx"
```

### Datadog Setup
1. Import `datadog/monitors.json` via Datadog API or UI
2. Import `datadog/dashboards.json` for visualization
3. Configure incident rules in Datadog Incident Management

## Links
- **Live App**: `<your-deployed-url>`
- **Demo Video**: `<your-video-link>`
- **Datadog Dashboard**: `<your-dashboard-link>`

## Key Takeaway
This project shows how teams can operate LLMs like real production systems, using Datadog to detect failures that traditional monitoring tools miss.

## License
MIT License - see [LICENSE](LICENSE)
