#!/usr/bin/env python3
import time
from datetime import datetime
from anthropic import Anthropic

def health_check():
    timestamp = datetime.now().isoformat()
    start = time.time()

    try:
        client = Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,
            messages=[{"role": "user", "content": "ping"}]
        )
        elapsed = time.time() - start
        print(f"[{timestamp}] Health check: OK (response time: {elapsed:.2f}s)")
    except Exception as e:
        elapsed = time.time() - start
        print(f"[{timestamp}] Health check: FAILED ({str(e)}, elapsed: {elapsed:.2f}s)")

if __name__ == "__main__":
    health_check()
