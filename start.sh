#!/bin/bash
# Startup script for LLM Observability Application

# Exit on error
set -e

echo "🚀 Starting LLM Observability Application..."

# Run with ddtrace for Datadog APM
exec ddtrace-run uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port ${APP_PORT:-8000} \
    --workers 1 \
    --log-level info
