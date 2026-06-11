#!/usr/bin/env python3
import os
import sys
from datetime import datetime
import time

try:
    import anthropic
except ImportError:
    print(f"[{datetime.now().isoformat()}] Health check: FAILED - anthropic not installed")
    sys.exit(1)

start_time = time.time()
timestamp = datetime.now().isoformat()

try:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=10,
        messages=[
            {"role": "user", "content": "ping"}
        ]
    )

    response_time = time.time() - start_time
    print(f"[{timestamp}] Health check: OK (response time: {response_time:.2f}s)")

except anthropic.AuthenticationError:
    response_time = time.time() - start_time
    print(f"[{timestamp}] Health check: FAILED - authentication error (response time: {response_time:.2f}s)")
    sys.exit(1)
except anthropic.APIConnectionError as e:
    response_time = time.time() - start_time
    print(f"[{timestamp}] Health check: FAILED - connection error (response time: {response_time:.2f}s)")
    sys.exit(1)
except Exception as e:
    response_time = time.time() - start_time
    print(f"[{timestamp}] Health check: FAILED - {str(e)} (response time: {response_time:.2f}s)")
    sys.exit(1)
