import time
from threading import Lock
from typing import Dict, List

class WorkerRegistry:
    """Simple in-memory registry for workers.
    Worker entries: {id: {id, url, metadata, last_seen, healthy}}
    """
    def __init__(self):
        self._workers: Dict[str, dict] = {}
        self._lock = Lock()

    def register(self, worker_id: str, url: str, metadata: dict):
        with self._lock:
            self._workers[worker_id] = {
                "id": worker_id,
                "url": url,
                "metadata": metadata,
                "last_seen": time.time(),
                "healthy": True,
            }

    def list_workers(self) -> List[dict]:
        with self._lock:
            return list(self._workers.values())

    def mark_unhealthy(self, worker_id: str):
        with self._lock:
            if worker_id in self._workers:
                self._workers[worker_id]["healthy"] = False

    def get_healthy_workers(self) -> List[dict]:
        with self._lock:
            return [w for w in self._workers.values() if w.get("healthy")]

    def get(self, worker_id: str):
        with self._lock:
            return self._workers.get(worker_id)
