#!/usr/bin/env python3
"""Health check for Anthropic API."""

import time
from datetime import datetime
import os
from anthropic import Anthropic

def health_check():
    """Verify Anthropic API is reachable with a minimal ping message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        start_time = time.time()
        response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=10,
            messages=[{"role": "user", "content": "ping"}]
        )
        response_time = time.time() - start_time

        status = "OK"
        output = f"[{timestamp}] Health check: {status} ({response_time:.2f}s)"
    except Exception as e:
        status = "FAILED"
        output = f"[{timestamp}] Health check: {status} ({str(e)})"

    print(output)
    return status == "OK"

if __name__ == "__main__":
    health_check()
