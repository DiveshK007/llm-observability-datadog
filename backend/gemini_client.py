"""
Gemini Client Module
Handles all interactions with Google Vertex AI Gemini model.
Includes automatic telemetry emission for observability.
"""

import os
import time
from typing import Optional
from dataclasses import dataclass

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from datadog import statsd
import structlog

logger = structlog.get_logger()

# Gemini pricing (approximate, per 1K tokens)
GEMINI_INPUT_PRICE_PER_1K = 0.00025
GEMINI_OUTPUT_PRICE_PER_1K = 0.0005


@dataclass
class GeminiResponse:
    """Response from Gemini model with metadata."""
    text: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency_ms: float
    estimated_cost_usd: float


class GeminiClient:
    """Client for interacting with Gemini model via Vertex AI."""
    
    def __init__(
        self,
        project_id: Optional[str] = None,
        location: str = "us-central1",
        model_name: str = "gemini-1.5-flash"
    ):
        """
        Initialize Gemini client.
        
        Args:
            project_id: GCP project ID. Defaults to env var GCP_PROJECT_ID.
            location: GCP region. Defaults to us-central1.
            model_name: Gemini model variant. Defaults to gemini-1.5-flash.
        """
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        self.location = location
        self.model_name = model_name
        
        if not self.project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set")
        
        # Initialize Vertex AI
        vertexai.init(project=self.project_id, location=self.location)
        self.model = GenerativeModel(self.model_name)
        
        logger.info(
            "gemini_client_initialized",
            project_id=self.project_id,
            location=self.location,
            model=self.model_name
        )
    
    def generate(self, prompt: str, max_tokens: int = 1024) -> GeminiResponse:
        """
        Generate response from Gemini model.
        
        Args:
            prompt: User prompt text.
            max_tokens: Maximum tokens in response.
            
        Returns:
            GeminiResponse with text, tokens, latency, and cost.
        """
        start_time = time.perf_counter()
        
        try:
            # Configure generation parameters
            config = GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.7
            )
            
            # Make the API call
            response = self.model.generate_content(
                prompt,
                generation_config=config
            )
            
            # Calculate latency
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            # Extract response text
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            # Extract token counts from usage metadata
            usage = response.usage_metadata
            if usage:
                input_tokens = usage.prompt_token_count
                output_tokens = usage.candidates_token_count
                total_tokens = usage.total_token_count if hasattr(usage, 'total_token_count') else (input_tokens + output_tokens)
            else:
                # Fallback: estimate tokens (rough approximation)
                input_tokens = len(prompt.split()) * 1.3  # ~1.3 tokens per word
                output_tokens = len(response_text.split()) * 1.3
                total_tokens = int(input_tokens + output_tokens)
            
            # Calculate estimated cost
            estimated_cost = (
                (input_tokens / 1000) * GEMINI_INPUT_PRICE_PER_1K +
                (output_tokens / 1000) * GEMINI_OUTPUT_PRICE_PER_1K
            )
            
            # Emit metrics to Datadog
            self._emit_metrics(
                latency_ms=latency_ms,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                estimated_cost=estimated_cost,
                success=True
            )
            
            logger.info(
                "gemini_request_success",
                latency_ms=round(latency_ms, 2),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=round(estimated_cost, 6)
            )
            
            return GeminiResponse(
                text=response_text,
                input_tokens=int(input_tokens),
                output_tokens=int(output_tokens),
                total_tokens=int(total_tokens),
                latency_ms=latency_ms,
                estimated_cost_usd=estimated_cost
            )
            
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            # Emit error metrics
            self._emit_error(error_type=type(e).__name__, latency_ms=latency_ms)
            
            logger.error(
                "gemini_request_failed",
                error_type=type(e).__name__,
                error_message=str(e),
                latency_ms=round(latency_ms, 2)
            )
            raise
    
    def _emit_metrics(
        self,
        latency_ms: float,
        input_tokens: int,
        output_tokens: int,
        total_tokens: int,
        estimated_cost: float,
        success: bool
    ) -> None:
        """Emit observability metrics to Datadog."""
        tags = [
            f"model:{self.model_name}",
            f"project:{self.project_id}",
            "component:gemini"
        ]
        
        # Latency metric
        statsd.gauge("llm.request.latency_ms", latency_ms, tags=tags)
        
        # Token metrics
        statsd.gauge("llm.tokens.used", total_tokens, tags=tags)
        statsd.gauge("llm.tokens.input", input_tokens, tags=tags)
        statsd.gauge("llm.tokens.output", output_tokens, tags=tags)
        
        # Cost metric
        statsd.gauge("llm.estimated.cost_usd", estimated_cost, tags=tags)
        
        # Success counter
        if success:
            statsd.increment("llm.request.success_count", tags=tags)
    
    def _emit_error(self, error_type: str, latency_ms: float) -> None:
        """Emit error metrics to Datadog."""
        tags = [
            f"model:{self.model_name}",
            f"project:{self.project_id}",
            f"error_type:{error_type}",
            "component:gemini"
        ]
        
        statsd.increment("llm.request.error_count", tags=tags)
        statsd.gauge("llm.request.latency_ms", latency_ms, tags=tags)


# Singleton instance for convenience
_client: Optional[GeminiClient] = None


def get_gemini_client() -> GeminiClient:
    """Get or create singleton Gemini client."""
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client


def call_gemini(prompt: str, max_tokens: int = 1024) -> GeminiResponse:
    """
    Convenience function to call Gemini.
    
    Args:
        prompt: User prompt text.
        max_tokens: Maximum response tokens.
        
    Returns:
        GeminiResponse with text and metadata.
    """
    client = get_gemini_client()
    return client.generate(prompt, max_tokens)
