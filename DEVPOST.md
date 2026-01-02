# Devpost Submission Template

Use this content for your Devpost submission. Copy and paste, then fill in the placeholders.

---

## Project Name

**Production-Grade Observability for LLM Systems using Datadog & Gemini**

---

## Tagline

Detect, diagnose, and respond to LLM failures before users or costs are impacted.

---

## Inspiration

As LLMs move into production, failures shift from infrastructure to the model layer. Latency spikes, silent errors, and runaway token usage often go unnoticed until users complain or costs explode.

We wanted to explore how modern observability tools can be adapted to operate AI systems safely and reliably.

---

## What It Does

Our project integrates a Gemini-powered LLM application with Datadog to provide:
- Real-time LLM performance monitoring
- Detection of AI-specific failure modes
- Automated incident creation
- Unified dashboards for latency, errors, and cost

This enables teams to respond to LLM issues before they cause real-world impact.

---

## How We Built It

- Built an LLM backend using Google Vertex AI (Gemini)
- Instrumented the system with Datadog APM, logs, and custom metrics
- Designed detection rules for:
  - Latency degradation
  - Error bursts
  - Token anomalies
  - Cost spikes
- Automated incident creation and response workflows
- Deployed the system on Google Cloud Run

---

## Challenges We Ran Into

- Identifying meaningful LLM-specific signals (latency, tokens, cost)
- Designing alerts that are actionable, not noisy
- Correlating model behavior with backend performance
- Setting appropriate thresholds for anomaly detection

---

## Accomplishments We're Proud Of

- Built real, verifiable Datadog dashboards and monitors
- Demonstrated automated incident response for AI systems
- Created a reusable reference architecture for LLM observability
- Proved that traditional monitoring can be adapted for AI workloads

---

## What We Learned

- Traditional monitoring is insufficient for AI systems
- LLM observability requires model-aware metrics (tokens, cost, latency)
- Production AI needs the same rigor as backend services
- Anomaly detection is crucial for catching prompt regressions
- Automated incident response dramatically improves MTTR

---

## What's Next

- Add prompt-level tracing for deeper debugging
- Extend support to multi-model systems
- Integrate auto-remediation actions (rate limiting, fallback models)
- Add user-facing SLA tracking
- Build cost optimization recommendations

---

## Demo & Links

- 🔗 **Live App**: `<your-deployed-url>`
- 🎥 **Demo Video (≤3 mins)**: `<your-video-link>`
- 💻 **GitHub Repo**: `<your-repo-url>`
- 📊 **Datadog Dashboard**: `<your-dashboard-link>`

---

## Tech Stack

- **LLM**: Google Gemini via Vertex AI
- **Backend**: FastAPI (Python)
- **Observability**: Datadog (APM, Metrics, Logs, Incidents)
- **Deployment**: Google Cloud Run
- **Frontend**: HTML/CSS/JavaScript

---

## Key Features

✅ **LLM-Aware Monitoring**
- Custom metrics for latency, tokens, and cost
- Anomaly detection for prompt regressions
- Real-time error tracking

✅ **Automated Incident Response**
- Monitors trigger incidents automatically
- Pre-filled context and runbooks
- Service and severity tagging

✅ **Production-Ready**
- Deployed on Google Cloud Run
- Traffic generator for testing
- Complete observability stack

---

## Screenshots

*Add screenshots of:*
1. Live application
2. Datadog dashboard showing metrics
3. Monitor firing and incident creation
4. Traffic generator in action

---

## Submission Notes

- ✅ Uses Google Gemini (Vertex AI) exclusively
- ✅ Deployed on Google Cloud Platform
- ✅ Real Datadog instrumentation (not mockups)
- ✅ Minimum 3 detection rules implemented
- ✅ Automated incident creation working
- ✅ Public GitHub repo with OSI license
- ✅ Video under 3 minutes

