# Telemetry package for Datadog instrumentation
from .datadog_setup import init_datadog, emit_custom_metric, increment_counter

__all__ = ["init_datadog", "emit_custom_metric", "increment_counter"]
