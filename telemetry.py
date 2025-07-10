# azure_cluster_simulator/telemetry.py

import logging
import json
from datetime import datetime

class TelemetryLogger:
    def __init__(self):
        self.events = []

    def log_event(self, cluster_name, event_type, metadata=None):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "cluster": cluster_name,
            "event": event_type,
            "metadata": metadata or {}
        }
        self.events.append(event)
        logging.info(f"[Telemetry] {json.dumps(event)}")
