# Datadog Configuration Files

This directory contains all Datadog configuration files required for the hackathon submission.

## Files

- **`monitors.json`** - Datadog monitor definitions (REQUIRED for submission)
- **`dashboards.json`** - Dashboard configuration (REQUIRED for submission)
- **`INCIDENTS.md`** - Incident configuration guide

## Import Instructions

### Monitors

1. **Via Datadog UI:**
   - Navigate to **Monitors** → **New Monitor**
   - For each monitor in `monitors.json`, create manually using the provided query and settings

2. **Via Datadog API:**
   ```bash
   curl -X POST "https://api.datadoghq.com/api/v1/monitor" \
     -H "Content-Type: application/json" \
     -H "DD-API-KEY: ${DD_API_KEY}" \
     -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
     -d @monitors.json
   ```

### Dashboard

1. **Via Datadog UI:**
   - Navigate to **Dashboards** → **New Dashboard**
   - Import JSON or recreate widgets manually using the provided configuration

2. **Via Datadog API:**
   ```bash
   curl -X POST "https://api.datadoghq.com/api/v1/dashboard" \
     -H "Content-Type: application/json" \
     -H "DD-API-KEY: ${DD_API_KEY}" \
     -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
     -d @dashboards.json
   ```

## Monitor Details

### 1. High LLM Request Latency
- **Type**: Metric Alert
- **Query**: `avg(last_5m):avg:llm.request.latency_ms{*} > 3000`
- **Purpose**: Detects latency degradation, the earliest sign of LLM instability
- **Threshold**: 3000ms (adjust based on your baseline)

### 2. Elevated LLM Error Rate
- **Type**: Metric Alert
- **Query**: `sum(last_5m):sum:llm.request.error_count{*} > 5`
- **Purpose**: Detects silent model failures that don't crash infrastructure
- **Threshold**: 5 errors in 5 minutes

### 3. Abnormal LLM Token Usage
- **Type**: Query Alert (Anomaly Detection)
- **Query**: `anomalies(avg:llm.tokens.used{*}, 'basic', 2, direction='above', interval=60)`
- **Purpose**: Detects prompt regressions or abuse patterns
- **Method**: Anomaly detection (2 standard deviations above baseline)

### 4. LLM Cost Spike Detection
- **Type**: Metric Alert
- **Query**: `avg(last_10m):avg:llm.estimated.cost_usd{*} > 2`
- **Purpose**: Protects against runaway AI costs
- **Threshold**: $2 USD per 10-minute window (adjust based on baseline)

## Dashboard Widgets

The dashboard includes:
1. **LLM Request Latency (ms)** - Timeseries of latency over time
2. **LLM Error Rate** - Bar chart of error counts
3. **Token Usage per Request** - Timeseries of token consumption
4. **Estimated LLM Cost (USD)** - Timeseries of cost trends
5. **Active LLM Alerts** - Alert graph showing monitor status

## Verification Checklist

Before submission, verify:
- [ ] All 4 monitors are active in Datadog
- [ ] Dashboard is accessible and shows real data
- [ ] Monitors have fired at least once (use traffic generator)
- [ ] Incident was created when monitors fired
- [ ] JSON exports match your actual Datadog configuration
- [ ] Datadog org name is documented in main README

## Notes for Judges

- All monitors use real metrics emitted from the application
- Thresholds are set for demonstration purposes and should be adjusted for production
- The anomaly detection monitor uses Datadog's built-in anomaly detection algorithm
- All monitors include tags for service, component, and severity

