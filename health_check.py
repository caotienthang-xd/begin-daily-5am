#!/usr/bin/env python3
import time
from datetime import datetime
import sys

try:
    from anthropic import Anthropic

    client = Anthropic()
    start_time = time.time()
    timestamp = datetime.now().isoformat()

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=10,
        messages=[{"role": "user", "content": "ping"}]
    )

    elapsed = time.time() - start_time
    status = "OK"

except Exception as e:
    timestamp = datetime.now().isoformat()
    status = "FAILED"
    elapsed = 0
    print(f"[{timestamp}] Health check: FAILED - {str(e)}", file=sys.stderr)
    sys.exit(1)

print(f"[{timestamp}] Health check: {status} (response time: {elapsed:.2f}s)")
