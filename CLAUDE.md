# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**begin-daily-5am** ("Khởi chạy ngày mới" — Start a new day) is a project focused on daily startup routines or morning automation. The repository is in its initial stage with no language, framework, or tooling committed yet.

## Commands

```powershell
# Install dependencies
pip install -r requirements.txt

# Run the morning routine
python morning.py
```

To schedule it at 5am daily on Windows, use Task Scheduler pointing to `python morning.py`.

## Architecture

Single-file script (`morning.py`) with three responsibilities:

- **`fetch_weather(city)`** — pulls current conditions from wttr.in (no API key needed; city defaults to auto-detected location)
- **`build_summary()`** — assembles the date string and weather into a `(title, body)` tuple
- **`send_notification(title, body)`** — fires a Windows desktop toast via `plyer`; degrades gracefully if plyer is missing

`main()` wires them together: print summary to stdout, then notify.
