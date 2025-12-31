"""
Datadog Setup Module
Initializes Datadog APM, metrics, and logging for LLM observability.
"""

import os
import logging

from datadog import initialize, statsd
from ddtrace import patch_all, tracer
import structlog


def init_datadog() -> None:
    """
    Initialize Datadog SDK and instrumentation.
    
    Configures:
    - DogStatsD for custom metrics
    - APM tracing with ddtrace
    - Structured logging
    """
    # Get configuration from environment
    dd_api_key = os.getenv("DD_API_KEY")
    dd_site = os.getenv("DD_SITE", "datadoghq.com")
    dd_env = os.getenv("DD_ENV", "dev")
    dd_service = os.getenv("DD_SERVICE", "llm-observability-app")
    dd_version = os.getenv("DD_VERSION", "1.0.0")
    
    # Initialize Datadog client
    options = {
        "api_key": dd_api_key,
        "statsd_host": os.getenv("DD_AGENT_HOST", "127.0.0.1"),
        "statsd_port": int(os.getenv("DD_DOGSTATSD_PORT", "8125")),
        "statsd_constant_tags": [
            f"env:{dd_env}",
            f"service:{dd_service}",
            f"version:{dd_version}"
        ]
    }
    initialize(**options)
    
    # Enable automatic instrumentation for common libraries
    # Note: tracer is auto-configured via DD_* environment variables
    try:
        patch_all()
    except Exception as e:
        # Gracefully handle if some patches fail
        logger = structlog.get_logger()
        logger.warning("patch_all_partial_failure", error=str(e))
    
    # Setup structured logging
    _setup_logging(dd_service, dd_env, dd_version)
    
    logger = structlog.get_logger()
    logger.info(
        "datadog_initialized",
        service=dd_service,
        env=dd_env,
        version=dd_version,
        site=dd_site
    )


def _setup_logging(service: str, env: str, version: str) -> None:
    """Configure structured logging with Datadog correlation."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def emit_custom_metric(name: str, value: float, tags: list = None) -> None:
    """
    Emit a custom metric to Datadog.
    
    Args:
        name: Metric name (e.g., 'llm.custom.metric')
        value: Metric value
        tags: Optional list of tags
    """
    statsd.gauge(name, value, tags=tags or [])


def increment_counter(name: str, value: int = 1, tags: list = None) -> None:
    """
    Increment a counter metric.
    
    Args:
        name: Counter name
        value: Increment amount
        tags: Optional list of tags
    """
    statsd.increment(name, value, tags=tags or [])
