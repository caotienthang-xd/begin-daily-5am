#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not found. Install with: pip install anthropic")
    sys.exit(1)

def health_check():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY environment variable not set")
        return False

    client = Anthropic(api_key=api_key)
    timestamp = datetime.utcnow().isoformat()
    start_time = time.time()

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,
            messages=[{"role": "user", "content": "ping"}]
        )
        elapsed = time.time() - start_time
        status = "OK"
        print(f"[{timestamp}] Health check: {status} ({elapsed:.2f}s)")
        return True
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[{timestamp}] Health check: FAILED ({elapsed:.2f}s) - {str(e)}")
        return False

if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1)
