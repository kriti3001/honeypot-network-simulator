import json
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "honeypot_events.jsonl")

def log_event(service, source_ip, username=None, password=None, extra=None):
    """Append a structured event to the shared log file (JSON Lines format)."""
    os.makedirs(LOG_DIR, exist_ok=True)
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": service,
        "source_ip": source_ip,
        "username": username,
        "password": password,
    }
    if extra:
        event.update(extra)

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

    print(f"[{event['timestamp']}] {service} | {source_ip} | user={username} pass={password}")