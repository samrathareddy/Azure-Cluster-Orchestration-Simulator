# azure_cluster_simulator/utils.py

import asyncio
import logging
import random

async def simulate_delay(task_name: str, seconds: int = 2):
    logging.info(f"[Simulator] {task_name} in progress... (approx {seconds}s)")
    await asyncio.sleep(seconds)
    logging.info(f"[Simulator] {task_name} completed.")

async def simulate_random_failure(probability: float = 0.2):
    """
    Simulate a random failure with the given probability.
    """
    if random.random() < probability:
        raise RuntimeError("Simulated random fault occurred.")

async def retry_operation(operation_coro, retries=3, base_delay=1, task_name=""):
    """
    Retry an async operation with exponential backoff.
    """
    for attempt in range(retries):
        try:
            return await operation_coro()
        except Exception as e:
            wait = base_delay * (2 ** attempt)
            logging.warning(f"[Retry] Attempt {attempt + 1} failed for {task_name}: {e}. Retrying in {wait}s...")
            await asyncio.sleep(wait)
    raise RuntimeError(f"[Retry] Operation failed after {retries} retries: {task_name}")

class lock_with_timeout:
    """
    Async context manager for acquiring a lock with timeout.
    """
    def __init__(self, lock: asyncio.Lock, timeout: float = 5.0):
        self.lock = lock
        self.timeout = timeout

    async def __aenter__(self):
        if not await asyncio.wait_for(self.lock.acquire(), timeout=self.timeout):
            raise TimeoutError("Failed to acquire lock within timeout.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
