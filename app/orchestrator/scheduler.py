from typing import Optional
from app.orchestrator.registry import WorkerRegistry

class RoundRobinScheduler:
    def __init__(self, registry: WorkerRegistry):
        self.registry = registry
        self._index = 0

    def select(self) -> Optional[dict]:
        workers = self.registry.get_healthy_workers()
        if not workers:
            return None
        # simple round robin
        worker = workers[self._index % len(workers)]
        self._index = (self._index + 1) % max(1, len(workers))
        return worker
