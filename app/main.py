from fastapi import FastAPI, HTTPException
from app.api.routes import router as orchestrator_router
from app.orchestrator.registry import WorkerRegistry

app = FastAPI(title="nebula-grid-orchestrator")

# simple global registry instance
registry = WorkerRegistry()

app.include_router(orchestrator_router, prefix="", tags=["orchestrator"], dependencies=[])

@app.on_event("startup")
async def startup_event():
    # place to initialize background tasks, health checks, etc.
    print("Orchestrator started. Ready to accept worker registrations and predict requests.")
