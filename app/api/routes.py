from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.orchestrator.registry import WorkerRegistry
from app.orchestrator.scheduler import RoundRobinScheduler
import httpx

router = APIRouter()

# Use the shared registry module-level instance from app.main for simplicity
from app.main import registry
scheduler = RoundRobinScheduler(registry)

class PredictRequest(BaseModel):
    input: List[float]

@router.post("/workers/register")
async def register_worker(info: Dict[str, Any]):
    # info should include: id, url, metadata
    if not info.get("id") or not info.get("url"):
        raise HTTPException(status_code=400, detail="worker registration requires 'id' and 'url'")
    registry.register(info["id"], info["url"], info.get("metadata", {}))
    return {"status": "registered", "id": info["id"]}

@router.get("/workers")
async def list_workers():
    return registry.list_workers()

@router.post("/predict")
async def predict(req: PredictRequest):
    # Select a worker and forward request
    worker = scheduler.select()
    if not worker:
        raise HTTPException(status_code=503, detail="no available workers")
    endpoint = f"{worker['url'].rstrip('/')}/task/predict"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(endpoint, json={"input": req.input})
            resp.raise_for_status()
        except httpx.RequestError as exc:
            # mark worker unhealthy
            registry.mark_unhealthy(worker['id'])
            raise HTTPException(status_code=502, detail=f"failed to contact worker {worker['id']}: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=502, detail=f"worker error: {exc.response.text}")
    return resp.json()
