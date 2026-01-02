# Hackathon Submission Checklist

Use this checklist to ensure your submission meets all requirements and is judge-ready.

## ✅ Project Eligibility (Non-Negotiable)

- [ ] Project built during contest period (newly created)
- [ ] Original work (no reuse of old repos)
- [ ] Hosted and publicly accessible (URL works)
- [ ] Runnable exactly as shown in video
- [ ] Web/Android/iOS app (web is safest)

## ✅ AI Usage Constraints

- [ ] **ONLY** using Google Cloud Vertex AI / Gemini
- [ ] **NO** OpenAI, Claude, Groq, or other external LLMs
- [ ] **NO** HuggingFace hosted models
- [ ] **NO** self-hosted LLMs
- [ ] Gemini/Vertex usage explicitly shown in:
  - [ ] README
  - [ ] Code comments
  - [ ] Video narration

## ✅ Datadog Challenge Requirements

### Core Application
- [ ] LLM application using Gemini (Vertex AI)
- [ ] Any use case (chatbot, agent, analyzer, etc.)
- [ ] Deployed and accessible

### Telemetry Streaming
- [ ] Real signals sent to Datadog (not fake logs)
- [ ] Latency metrics
- [ ] Error metrics
- [ ] Token usage metrics
- [ ] Cost estimation metrics
- [ ] Request volume metrics
- [ ] Model failure tracking
- [ ] App health metrics

### Datadog Dashboard
- [ ] Actual dashboard (not just screenshots)
- [ ] Shows app health (latency, error rate, throughput)
- [ ] Shows LLM-specific signals
- [ ] Shows detection rule status
- [ ] Shows active incidents/cases
- [ ] Dashboard is clickable by judges

### Detection Rules (Minimum 3)
- [ ] **Monitor 1**: High Latency
- [ ] **Monitor 2**: Error Rate
- [ ] **Monitor 3**: Token Usage Anomaly
- [ ] **Monitor 4** (Bonus): Cost Spike
- [ ] Each monitor has:
  - [ ] Clear query/condition
  - [ ] Meaningful threshold
  - [ ] Explanation of why it exists
  - [ ] Documented in monitors.json

### Actionable Incident/Case
- [ ] Incident or Case created when rules fire
- [ ] Includes signal data
- [ ] Includes context
- [ ] Includes suggested next steps/runbook
- [ ] Screenshot captured for submission

### Traffic Generator
- [ ] Script included in repo
- [ ] Simulates real usage
- [ ] Intentionally triggers detection rules
- [ ] Proves alerts work
- [ ] Documented in README

### Evidence Artifacts
- [ ] Dashboard links or screenshots
- [ ] Detection rule explanations
- [ ] Incident screenshots (what happened, when, why)
- [ ] All evidence accessible to judges

## ✅ Repository Requirements

- [ ] Public GitHub repo
- [ ] OSI-approved license (MIT/Apache 2.0) at repo top
- [ ] Full source code included
- [ ] README with:
  - [ ] Architecture diagram/explanation
  - [ ] Deployment steps
  - [ ] Gemini/Vertex usage clearly stated
  - [ ] Datadog org name included
- [ ] JSON exports in `/datadog` folder:
  - [ ] `dashboards.json`
  - [ ] `monitors.json`
  - [ ] (Optional) `slos.json`

## ✅ Video Requirements (≤3 minutes)

- [ ] Video is 3 minutes or less (only first 3 mins judged)
- [ ] Shows problem statement (0:00-0:20)
- [ ] Shows architecture (0:20-0:50)
- [ ] Shows live app working (0:50-1:30)
- [ ] Shows Datadog dashboard (1:30-2:20)
- [ ] Shows detection firing → incident created (2:20-2:55)
- [ ] Clear closing (2:55-3:00)

## ✅ Code Quality

- [ ] Clean, readable code
- [ ] Proper error handling
- [ ] Environment variables for configuration
- [ ] Production-ready structure
- [ ] No hardcoded secrets
- [ ] Proper logging

## ✅ Deployment

- [ ] Deployed on Google Cloud Platform
- [ ] Publicly accessible URL
- [ ] Health endpoint working
- [ ] API endpoints functional
- [ ] Frontend accessible (if applicable)

## ✅ Documentation

- [ ] README.md comprehensive and clear
- [ ] Architecture explained
- [ ] Setup instructions work
- [ ] Deployment guide included
- [ ] Datadog setup documented
- [ ] Incident configuration explained

## 🚫 Disqualification Traps (AVOID)

- [ ] ❌ Using OpenAI even once
- [ ] ❌ Fake screenshots
- [ ] ❌ No incident creation
- [ ] ❌ Only logs, no metrics
- [ ] ❌ No traffic generator
- [ ] ❌ Missing JSON exports
- [ ] ❌ Repo without license
- [ ] ❌ Video longer than 3 mins
- [ ] ❌ App not publicly accessible
- [ ] ❌ Using AWS/Azure infrastructure

## 📋 Final Pre-Submission

- [ ] All code pushed to GitHub
- [ ] README updated with actual URLs
- [ ] Video uploaded and link ready
- [ ] Datadog dashboard shared (if possible)
- [ ] All screenshots captured
- [ ] Devpost submission filled out
- [ ] Double-check all links work
- [ ] Test traffic generator one more time
- [ ] Verify monitors can fire
- [ ] Confirm incident creation works

## 🎯 Judge Verification Points

Judges will check:
1. ✅ Gemini/Vertex used? (Code + README + Video)
2. ✅ Telemetry real? (Datadog dashboard)
3. ✅ ≥3 monitors? (monitors.json + Datadog UI)
4. ✅ Incident created? (Screenshot + Datadog UI)
5. ✅ Dashboard clickable? (Link works)
6. ✅ Traffic generator present? (Code in repo)

If all ✅ → Top-tier submission

---

**Remember:** You're not competing on taste. You're competing on correctness.

