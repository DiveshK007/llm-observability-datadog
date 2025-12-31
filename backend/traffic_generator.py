#!/usr/bin/env python3
"""
Traffic Generator for LLM Observability Testing
Simulates various load patterns to trigger Datadog detection rules.
"""

import argparse
import random
import time
import sys
from typing import Literal

import requests


# Sample prompts for different load profiles
NORMAL_PROMPTS = [
    "What is AI observability?",
    "Explain the benefits of monitoring LLM applications.",
    "How do you detect latency issues in production?",
    "What metrics are important for AI systems?",
    "Describe best practices for LLM deployment.",
]

HEAVY_PROMPTS = [
    "Explain in great detail " * 100 + "what AI observability means.",
    "Write a comprehensive essay " * 50 + "about monitoring systems.",
    "Provide extensive analysis " * 75 + "of machine learning operations.",
]


def generate_prompt(profile: str) -> str:
    """Generate a prompt based on the load profile."""
    if profile == "normal":
        return random.choice(NORMAL_PROMPTS)
    elif profile == "heavy":
        return random.choice(HEAVY_PROMPTS)
    elif profile == "mixed":
        return random.choice(HEAVY_PROMPTS if random.random() > 0.7 else NORMAL_PROMPTS)
    else:
        return random.choice(NORMAL_PROMPTS)


def send_request(url: str, prompt: str, timeout: int = 30) -> dict:
    """Send a single request to the LLM API."""
    try:
        response = requests.post(
            f"{url}/query",
            json={"prompt": prompt, "max_tokens": 1024},
            timeout=timeout,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "timeout"}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"http_{e.response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_load_test(
    url: str,
    profile: Literal["normal", "heavy", "mixed", "spike"],
    count: int,
    delay: float
) -> dict:
    """
    Run a load test with the specified profile.
    
    Args:
        url: Target API URL
        profile: Load profile type
        count: Number of requests
        delay: Delay between requests in seconds
    
    Returns:
        Summary statistics
    """
    stats = {
        "total": count,
        "success": 0,
        "failed": 0,
        "errors": {},
        "latencies": []
    }
    
    print(f"\n🚀 Starting traffic generation")
    print(f"   Target: {url}")
    print(f"   Profile: {profile}")
    print(f"   Requests: {count}")
    print(f"   Delay: {delay}s\n")
    
    for i in range(count):
        # For spike profile, send bursts
        if profile == "spike" and i % 10 == 0:
            current_delay = 0.1  # Fast burst
        else:
            current_delay = delay
        
        prompt = generate_prompt(profile)
        start = time.time()
        result = send_request(url, prompt)
        elapsed = (time.time() - start) * 1000
        
        if result["success"]:
            stats["success"] += 1
            latency = result["data"].get("latency_ms", elapsed)
            stats["latencies"].append(latency)
            status = "✅"
            detail = f"latency={latency:.0f}ms"
        else:
            stats["failed"] += 1
            error = result["error"]
            stats["errors"][error] = stats["errors"].get(error, 0) + 1
            status = "❌"
            detail = f"error={error}"
        
        print(f"   [{i+1}/{count}] {status} {detail}")
        
        if i < count - 1:
            time.sleep(current_delay)
    
    # Calculate summary
    if stats["latencies"]:
        stats["avg_latency"] = sum(stats["latencies"]) / len(stats["latencies"])
        stats["min_latency"] = min(stats["latencies"])
        stats["max_latency"] = max(stats["latencies"])
    
    return stats


def print_summary(stats: dict) -> None:
    """Print test summary."""
    print("\n" + "=" * 50)
    print("📊 TRAFFIC GENERATION SUMMARY")
    print("=" * 50)
    print(f"   Total requests:  {stats['total']}")
    print(f"   Successful:      {stats['success']} ({100*stats['success']/stats['total']:.1f}%)")
    print(f"   Failed:          {stats['failed']} ({100*stats['failed']/stats['total']:.1f}%)")
    
    if stats.get("latencies"):
        print(f"\n   Latency (ms):")
        print(f"      Avg: {stats['avg_latency']:.0f}")
        print(f"      Min: {stats['min_latency']:.0f}")
        print(f"      Max: {stats['max_latency']:.0f}")
    
    if stats.get("errors"):
        print(f"\n   Errors:")
        for error, count in stats["errors"].items():
            print(f"      {error}: {count}")
    
    print("=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Traffic generator for LLM Observability testing"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Target API URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--profile",
        choices=["normal", "heavy", "mixed", "spike"],
        default="mixed",
        help="Load profile: normal, heavy, mixed, or spike (default: mixed)"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=20,
        help="Number of requests to send (default: 20)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)"
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith("http"):
        args.url = f"http://{args.url}"
    
    # Remove trailing slash
    args.url = args.url.rstrip("/")
    
    # Check health first
    print(f"🔍 Checking API health at {args.url}...")
    try:
        health = requests.get(f"{args.url}/health", timeout=5)
        health.raise_for_status()
        print(f"   ✅ API is healthy\n")
    except Exception as e:
        print(f"   ⚠️  Health check failed: {e}")
        print(f"   Continuing anyway...\n")
    
    # Run load test
    stats = run_load_test(
        url=args.url,
        profile=args.profile,
        count=args.count,
        delay=args.delay
    )
    
    # Print summary
    print_summary(stats)
    
    # Exit with appropriate code
    if stats["failed"] > stats["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
