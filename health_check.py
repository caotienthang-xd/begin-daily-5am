import datetime
import json
import os
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "health_check.log")


def ping() -> tuple[bool, float]:
    """Send a minimal "ping" message; return (ok, response_time_seconds)."""
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 16,
        "messages": [{"role": "user", "content": "ping"}],
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    start = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        ok = bool(data.get("content"))
    except Exception:
        ok = False
    return ok, time.monotonic() - start


def main() -> int:
    ok, elapsed = ping()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "ok" if ok else "fail"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} status={status} response_time={elapsed:.2f}s\n")

    print(f"[{timestamp}] Health check: {'OK' if ok else 'FAILED'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
