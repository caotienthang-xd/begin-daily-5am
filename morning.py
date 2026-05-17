import datetime
import json
import sys
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding="utf-8")


def fetch_weather(city: str = "") -> str:
    url = f"https://wttr.in/{city}?format=j1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        feels_c = current["FeelsLikeC"]
        desc = current["weatherDesc"][0]["value"]
        return f"{desc}, {temp_c}°C (feels like {feels_c}°C)"
    except Exception:
        return "Weather unavailable"


def build_summary() -> tuple[str, str]:
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d %Y")
    weather = fetch_weather()

    title = "Good morning! Khởi chạy ngày mới"
    body = f"{date_str}\n{weather}"
    return title, body


def send_notification(title: str, body: str) -> None:
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=body,
            app_name="begin-daily-5am",
            timeout=15,
        )
    except ImportError:
        print("plyer not installed — run: pip install plyer")
    except Exception as e:
        print(f"Notification error: {e}")


def main() -> None:
    title, body = build_summary()
    print(f"{title}\n{body}\n")
    send_notification(title, body)


if __name__ == "__main__":
    main()
