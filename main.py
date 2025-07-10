# azure_cluster_simulator/main.py

import asyncio
import logging
from orchestrator import ClusterOrchestrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

async def main():
    orchestrator = ClusterOrchestrator("config/playbook.yaml")
    await orchestrator.run_playbook()

if __name__ == "__main__":
    asyncio.run(main())
