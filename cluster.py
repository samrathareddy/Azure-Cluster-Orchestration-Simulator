# azure_cluster_simulator/cluster.py

import asyncio
import logging
from utils import simulate_delay, simulate_random_failure, retry_operation, lock_with_timeout

class ClusterManager:
    def __init__(self, name, telemetry):
        self.name = name
        self.telemetry = telemetry
        self.status = 'initializing'
        self.nodes = []
        self.lock = asyncio.Lock()

    async def provision(self):
        async with lock_with_timeout(self.lock):
            logging.info(f"[{self.name}] Provisioning cluster...")
            self.telemetry.log_event(self.name, "provisioning_started")

            async def task():
                await simulate_delay("Provisioning resources", seconds=3)
                self.nodes = [f"{self.name}-node-{i}" for i in range(1, 6)]
                self.status = 'provisioned'

            await retry_operation(task, retries=3, task_name="provision")
            self.telemetry.log_event(self.name, "provisioning_completed", {"nodes": self.nodes})
            logging.info(f"[{self.name}] Cluster provisioned with nodes: {self.nodes}")

    async def refresh(self):
        async with lock_with_timeout(self.lock):
            logging.info(f"[{self.name}] Refreshing cluster...")
            self.telemetry.log_event(self.name, "refresh_started")

            async def task():
                await simulate_delay("Refreshing system", seconds=2)
                await simulate_random_failure(probability=0.2)

            try:
                await retry_operation(task, retries=3, task_name="refresh")
                self.telemetry.log_event(self.name, "refresh_completed")
                logging.info(f"[{self.name}] Cluster refreshed successfully.")
            except Exception as e:
                self.telemetry.log_event(self.name, "refresh_failed", {"error": str(e)})
                logging.error(f"[{self.name}] Refresh failed: {e}")

    async def recover(self):
        async with lock_with_timeout(self.lock):
            logging.info(f"[{self.name}] Recovering from faults...")
            self.telemetry.log_event(self.name, "recovery_started")

            async def task():
                await simulate_delay("Recovering failed services", seconds=4)

            await retry_operation(task, retries=2, task_name="recovery")
            self.telemetry.log_event(self.name, "recovery_completed")
            logging.info(f"[{self.name}] Fault recovery complete.")
