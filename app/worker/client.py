import httpx
import asyncio

async def register_to_orchestrator(orchestrator_url: str, worker_id: str, worker_url: str) -> bool:
    endpoint = f"{orchestrator_url.rstrip('/')}/workers/register"
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.post(endpoint, json={"id": worker_id, "url": worker_url, "metadata": {}})
        resp.raise_for_status()
    return True

# convenience synchronous wrapper
def register_sync(orchestrator_url: str, worker_id: str, worker_url: str):
    return asyncio.run(register_to_orchestrator(orchestrator_url, worker_id, worker_url))
