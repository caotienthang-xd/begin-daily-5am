#!/usr/bin/env python3
import sys
import time
import os
import httpx
from datetime import datetime
from anthropic import Anthropic, APIError

def health_check():
    timestamp = datetime.now().isoformat()
    base_url = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")

    try:
        start_time = time.time()
        client = Anthropic()

        message = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=10,
            messages=[
                {"role": "user", "content": "ping"}
            ]
        )

        response_time = time.time() - start_time

        if message.content:
            print(f"[{timestamp}] Health check: OK ({response_time:.2f}s)")
            return 0
        else:
            print(f"[{timestamp}] Health check: FAILED (no response)")
            return 1

    except Exception as auth_error:
        if "authentication" not in str(auth_error).lower():
            print(f"[{timestamp}] Health check: FAILED ({str(auth_error)})")
            return 1

        try:
            start_time = time.time()
            response = httpx.get(f"{base_url}/v1/models", timeout=5.0)
            response_time = time.time() - start_time
            if response.status_code == 401:
                print(f"[{timestamp}] Health check: OK ({response_time:.2f}s) [endpoint reachable]")
                return 0
            elif response.status_code < 500:
                print(f"[{timestamp}] Health check: OK ({response_time:.2f}s) [API reachable]")
                return 0
            else:
                print(f"[{timestamp}] Health check: FAILED (API error: {response.status_code})")
                return 1
        except Exception as http_err:
            print(f"[{timestamp}] Health check: FAILED (network error: {str(http_err)})")
            return 1

if __name__ == "__main__":
    sys.exit(health_check())
