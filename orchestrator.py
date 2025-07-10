# azure_cluster_simulator/orchestrator.py

import yaml
import asyncio
import logging
from cluster import ClusterManager
from telemetry import TelemetryLogger

class ClusterOrchestrator:
    def __init__(self, playbook_path):
        self.playbook_path = playbook_path
        self.telemetry = TelemetryLogger()

    async def run_playbook(self):
        logging.info("Loading playbook...")
        with open(self.playbook_path, 'r') as f:
            playbook = yaml.safe_load(f)

        cluster = ClusterManager(playbook['cluster_name'], self.telemetry)

        for step in playbook['steps']:
            action = step.get('action')
            delay = step.get('delay', 1)

            if action == 'provision':
                await cluster.provision()
            elif action == 'refresh':
                await cluster.refresh()
            elif action == 'recover':
                await cluster.recover()
            else:
                logging.warning(f"Unknown action: {action}")
            await asyncio.sleep(delay)

        logging.info("Playbook execution completed.")
