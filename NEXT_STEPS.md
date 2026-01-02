# Next Steps - Action Plan

Follow these steps in order to get your project submission-ready.

## 🚀 Phase 1: Environment Setup (30-60 minutes)

### Step 1.1: Google Cloud Setup
- [ ] Create/select a GCP project
- [ ] Enable Vertex AI API:
  ```bash
  gcloud services enable aiplatform.googleapis.com
  ```
- [ ] Create a service account:
  ```bash
  gcloud iam service-accounts create llm-observability \
    --display-name="LLM Observability Service Account"
  ```
- [ ] Grant Vertex AI User role:
  ```bash
  gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:llm-observability@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
  ```
- [ ] Download service account key:
  ```bash
  gcloud iam service-accounts keys create service_account.json \
    --iam-account=llm-observability@YOUR_PROJECT_ID.iam.gserviceaccount.com
  ```
- [ ] Place `service_account.json` in project root

### Step 1.2: Datadog Setup
- [ ] Sign up for Datadog trial: https://www.datadog.com/trial
- [ ] Get your API key: https://app.datadoghq.com/organization-settings/api-keys
- [ ] Get your Application key: https://app.datadoghq.com/organization-settings/application-keys
- [ ] Note your Datadog organization name (for submission)

### Step 1.3: Local Environment
- [ ] Create `.env` file in project root:
  ```bash
  # Copy the template from README.md
  DD_API_KEY=your_actual_key
  DD_SITE=datadoghq.com
  DD_ENV=prod
  DD_SERVICE=llm-observability-app
  DD_VERSION=1.0.0
  DD_AGENT_HOST=127.0.0.1
  DD_DOGSTATSD_PORT=8125
  GCP_PROJECT_ID=your_project_id
  GOOGLE_APPLICATION_CREDENTIALS=./service_account.json
  APP_HOST=0.0.0.0
  APP_PORT=8000
  ```
- [ ] Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## 🧪 Phase 2: Local Testing (30-45 minutes)

### Step 2.1: Run Datadog Agent (Optional for local)
If testing locally, you can either:
- **Option A**: Install Datadog Agent locally (recommended for full testing)
  - Download: https://docs.datadoghq.com/agent/
  - Configure with your API key
- **Option B**: Use Datadog API directly (simpler, but less APM tracing)
  - Metrics will still work via API

### Step 2.2: Test Application Locally
- [ ] Start the application:
  ```bash
  cd backend
  python -m uvicorn main:app --reload
  ```
- [ ] Test health endpoint: http://localhost:8000/health
- [ ] Test UI: http://localhost:8000
- [ ] Make a test query through the UI
- [ ] Verify response includes latency, tokens, cost

### Step 2.3: Verify Datadog Metrics
- [ ] Open Datadog Metrics Explorer
- [ ] Search for: `llm.request.latency_ms`
- [ ] Search for: `llm.tokens.used`
- [ ] Search for: `llm.estimated.cost_usd`
- [ ] Verify metrics are appearing (may take 1-2 minutes)

### Step 2.4: Test Traffic Generator
- [ ] Run traffic generator:
  ```bash
  python backend/traffic_generator.py --url http://localhost:8000 --profile mixed --count 20
  ```
- [ ] Verify it completes successfully
- [ ] Check Datadog for new metric data

## 📊 Phase 3: Datadog Configuration (45-60 minutes)

### Step 3.1: Import Monitors
- [ ] Open Datadog UI → Monitors → New Monitor
- [ ] For each monitor in `datadog/monitors.json`:
  - Create monitor manually OR
  - Use Datadog API to import (see `datadog/README.md`)
- [ ] Verify all 4 monitors are created and active
- [ ] Test each monitor by adjusting thresholds temporarily

### Step 3.2: Create Dashboard
- [ ] Open Datadog UI → Dashboards → New Dashboard
- [ ] Create widgets from `datadog/dashboards.json`:
  - LLM Request Latency (ms)
  - LLM Error Rate
  - Token Usage per Request
  - Estimated LLM Cost (USD)
  - Active LLM Alerts
- [ ] Save dashboard
- [ ] **Export the actual dashboard JSON** (replace the template)
- [ ] Copy dashboard URL for submission

### Step 3.3: Configure Incident Rules
- [ ] Open Datadog → Incident Management → Rules
- [ ] Create new incident rule:
  - Trigger: 2+ monitors fire within 10 minutes
  - Include all 4 LLM monitors
  - Title: "LLM Service Degradation Detected"
  - Severity: SEV-2
  - Add runbook from `datadog/INCIDENTS.md`
- [ ] Save rule

### Step 3.4: Test Incident Creation
- [ ] Run heavy traffic to trigger monitors:
  ```bash
  python backend/traffic_generator.py --url http://localhost:8000 --profile heavy --count 50
  ```
- [ ] Wait 5-10 minutes for monitors to evaluate
- [ ] Check if monitors fire
- [ ] Verify incident is created automatically
- [ ] **Take screenshot of incident** (required for submission)

## ☁️ Phase 4: Deployment (30-45 minutes)

### Step 4.1: Prepare for Cloud Run
- [ ] Ensure `Dockerfile` is correct (already done)
- [ ] Ensure `start.sh` is executable
- [ ] Test Docker build locally (optional):
  ```bash
  docker build -t llm-observability .
  docker run -p 8000:8000 --env-file .env llm-observability
  ```

### Step 4.2: Deploy to Google Cloud Run
- [ ] Authenticate:
  ```bash
  gcloud auth login
  gcloud config set project YOUR_PROJECT_ID
  ```
- [ ] Deploy:
  ```bash
  gcloud run deploy llm-observability \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="DD_API_KEY=xxx,DD_SITE=datadoghq.com,DD_ENV=prod,DD_SERVICE=llm-observability-app,GCP_PROJECT_ID=xxx" \
    --set-secrets="GOOGLE_APPLICATION_CREDENTIALS=service_account.json:latest"
  ```
- [ ] **OR** use environment variables file:
  ```bash
  gcloud run deploy llm-observability \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --env-vars-file .env.yaml
  ```
- [ ] Note the deployed URL (e.g., `https://llm-observability-xxx.run.app`)

### Step 4.3: Verify Deployment
- [ ] Test health endpoint: `https://your-url.run.app/health`
- [ ] Test UI: `https://your-url.run.app`
- [ ] Make a test query
- [ ] Verify Datadog receives metrics from deployed app

### Step 4.4: Update Datadog Agent Host
- [ ] For Cloud Run, you may need to use Datadog API directly
- [ ] Or configure Datadog Agent endpoint in environment variables
- [ ] Verify metrics still flow correctly

## 📸 Phase 5: Evidence Collection (30 minutes)

### Step 5.1: Screenshots Needed
- [ ] **Screenshot 1**: Live application UI with a query
- [ ] **Screenshot 2**: Datadog dashboard showing metrics
- [ ] **Screenshot 3**: Monitor firing (alert state)
- [ ] **Screenshot 4**: Incident created with context
- [ ] **Screenshot 5**: Traffic generator output

### Step 5.2: Links to Collect
- [ ] Live app URL
- [ ] Datadog dashboard URL (if shareable)
- [ ] GitHub repo URL
- [ ] Video URL (after recording)

## 🎥 Phase 6: Video Creation (60-90 minutes)

### Step 6.1: Prepare Script
- [ ] Review video script in README.md
- [ ] Practice timing (must be ≤3 minutes)
- [ ] Prepare screen recordings:
  - Application demo
  - Datadog dashboard walkthrough
  - Monitor firing demonstration

### Step 6.2: Record Video
- [ ] Record screen with audio
- [ ] Follow script timing:
  - 0:00-0:20: Problem statement
  - 0:20-0:50: Architecture
  - 0:50-1:30: Live app
  - 1:30-2:20: Datadog dashboard
  - 2:20-2:55: Incident firing
  - 2:55-3:00: Close
- [ ] Edit to ensure it's exactly 3 minutes or less
- [ ] Upload to YouTube/Vimeo (unlisted is fine)

## 📝 Phase 7: Final Submission Prep (30 minutes)

### Step 7.1: Update README
- [ ] Replace `<your-deployed-url>` with actual URL
- [ ] Replace `<your-video-link>` with video URL
- [ ] Replace `<your-dashboard-link>` with dashboard URL
- [ ] Add your Datadog organization name
- [ ] Add your GitHub repo URL

### Step 7.2: Update Devpost
- [ ] Copy content from `DEVPOST.md`
- [ ] Fill in all placeholders
- [ ] Add screenshots
- [ ] Add video link
- [ ] Add GitHub repo link

### Step 7.3: Final Verification
- [ ] Run through `SUBMISSION_CHECKLIST.md`
- [ ] Verify all links work
- [ ] Test traffic generator one more time
- [ ] Verify monitors can fire
- [ ] Confirm incident creation works
- [ ] Check video is accessible

### Step 7.4: Export Final Datadog Configs
- [ ] Export actual dashboard JSON from Datadog UI
- [ ] Replace `datadog/dashboards.json` with real export
- [ ] Export actual monitors JSON
- [ ] Replace `datadog/monitors.json` with real exports (if different)

## ✅ Phase 8: Submit!

- [ ] Submit to Devpost
- [ ] Double-check all requirements met
- [ ] Celebrate! 🎉

---

## 🆘 Troubleshooting

### Metrics not appearing in Datadog?
- Check DD_API_KEY is correct
- Verify Datadog Agent is running (if using local agent)
- Check network connectivity
- Wait 2-3 minutes for metrics to appear

### Monitors not firing?
- Verify metrics are actually being sent
- Check monitor queries match your metric names
- Lower thresholds temporarily to test
- Ensure evaluation window has passed

### Incident not creating?
- Verify incident rule is configured correctly
- Check that 2+ monitors actually fired
- Verify time window (10 minutes)
- Check incident rule is enabled

### Deployment issues?
- Verify service account has correct permissions
- Check environment variables are set correctly
- Review Cloud Run logs: `gcloud run services logs read llm-observability`

---

## 📅 Suggested Timeline

- **Day 1**: Phase 1-2 (Setup + Local Testing)
- **Day 2**: Phase 3-4 (Datadog Config + Deployment)
- **Day 3**: Phase 5-6 (Evidence + Video)
- **Day 4**: Phase 7-8 (Final Prep + Submit)

Good luck! 🚀

