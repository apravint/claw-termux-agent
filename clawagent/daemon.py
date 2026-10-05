"""
Claw Agent Background Daemon
============================
Schedules autonomous web scraping & monitoring tasks in Termux background.
"""

import os
import json
import time
import shutil
import subprocess
from typing import Dict, Any, List
from clawagent.scraper import scrape_webpage

LOG_FILE = os.path.expanduser("~/.clawagent/daemon_log.json")

def ensure_log_dir():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

def append_task_log(task_info: Dict[str, Any]):
    ensure_log_dir()
    with open(LOG_FILE, "r") as f:
        try:
            logs = json.load(f)
        except Exception:
            logs = []
    logs.append(task_info)
    with open(LOG_FILE, "w") as f:
        json.dump(logs[-50:], f, indent=2)

def send_termux_notification(title: str, content: str):
    """Trigger Android notification via Termux-API if installed."""
    if shutil.which("termux-notification"):
        try:
            subprocess.run(["termux-notification", "-t", title, "-c", content[:100]], timeout=5)
        except Exception:
            pass

def run_daemon_task(target_url: str) -> Dict[str, Any]:
    """Execute a single autonomous background scraping check."""
    scraped = scrape_webpage(target_url)
    task_log = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "target_url": target_url,
        "title": scraped.get("title", "Unknown"),
        "status": "SUCCESS" if "error" not in scraped else "FAILED",
        "char_count": scraped.get("character_count", 0)
    }
    
    append_task_log(task_log)
    send_termux_notification(f"ClawAgent Monitor: {task_log['title']}", f"Scraped {task_log['char_count']} chars from {target_url}")
    return task_log

def get_daemon_logs() -> List[Dict[str, Any]]:
    ensure_log_dir()
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []
