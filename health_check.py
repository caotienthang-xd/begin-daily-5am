#!/usr/bin/env python3
import time
from datetime import datetime
import sys

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed. Install with: pip install anthropic")
    sys.exit(1)

def health_check():
    """Ping the Anthropic API and log the response."""
    timestamp = datetime.now().isoformat()
    start_time = time.time()

    try:
        client = Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,
            messages=[
                {"role": "user", "content": "ping"}
            ]
        )

        response_time = time.time() - start_time
        status = "OK"

        # Output the result
        print(f"[{timestamp}] Health check: {status} ({response_time:.2f}s)")
        return True

    except Exception as e:
        response_time = time.time() - start_time
        status = "FAILED"
        print(f"[{timestamp}] Health check: {status} ({response_time:.2f}s)")
        print(f"Error: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1)
