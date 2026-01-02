# Datadog Incident Configuration

This document explains how to configure automated incident creation in Datadog for this LLM observability project.

## Overview

When multiple monitors fire within a short time window, Datadog automatically creates an incident with context, signal data, and remediation steps. This demonstrates production-grade incident response for AI systems.

## Incident Trigger Rule

### Configuration in Datadog UI

1. Navigate to **Incident Management** → **Rules**
2. Create a new incident rule with the following settings:

**Trigger Condition:**
- When **2 or more monitors** fire within **10 minutes**
- Monitors to include:
  - `High LLM Request Latency`
  - `Elevated LLM Error Rate`
  - `Abnormal LLM Token Usage`
  - `LLM Cost Spike Detected`

**Incident Metadata:**
- **Title**: `LLM Service Degradation Detected`
- **Severity**: `SEV-2` (Degraded service)
- **Service**: `llm-observability-app`
- **Component**: `gemini`

## Incident Description Template

```
Automated detection of LLM service degradation due to elevated latency, error rate, or abnormal token usage. Immediate investigation recommended to prevent user impact or cost escalation.

Affected Service: llm-observability-app
Component: Gemini (Vertex AI)
Detection Time: {{timestamp}}
```

## Runbook / Next Steps

Include these steps in the incident runbook:

1. **Check Gemini API health & quotas**
   - Verify Vertex AI service status
   - Check quota limits in GCP Console
   - Review recent API usage patterns

2. **Inspect recent prompt changes**
   - Review recent deployments
   - Check for prompt modifications
   - Validate prompt size trends

3. **Review token usage graphs**
   - Open Datadog dashboard
   - Analyze token usage anomaly graph
   - Identify if specific prompts are causing spikes

4. **Validate traffic patterns**
   - Check traffic source
   - Review request volume trends
   - Identify any unusual patterns

5. **Roll back or rate-limit if needed**
   - If prompt regression detected, roll back to previous version
   - If abuse detected, implement rate limiting
   - If quota exceeded, request quota increase

## Testing Incident Creation

To test that incidents are created correctly:

1. Run the traffic generator with heavy load:
   ```bash
   python backend/traffic_generator.py --url http://your-app-url --profile heavy --count 50
   ```

2. Wait for monitors to fire (typically within 5-10 minutes)

3. Check Datadog Incident Management for the automatically created incident

4. Verify the incident includes:
   - Correct severity and tags
   - Signal data from monitors
   - Suggested remediation steps

## Evidence for Submission

When submitting your hackathon entry, include:

- Screenshot of the incident in Datadog UI
- Link to the incident (if accessible)
- Explanation of which monitors triggered it
- Evidence of the runbook being followed

This demonstrates operational maturity and production-readiness.

