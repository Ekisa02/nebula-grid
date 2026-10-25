import argparse
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from app.ml.inference import InferenceEngine
from app.worker.client import register_to_orchestrator

class PredictRequest(BaseModel):
    input: list

def create_worker_app(model_path: str = None):
    app = FastAPI(title="nebula-grid-worker")
    engine = InferenceEngine(model_path=model_path)

    @app.post("/task/predict")
    async def task_predict(req: PredictRequest):
        try:
            result = engine.predict(req.input)
            return {"result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app

async def _run_register(orchestrator_url: str, worker_id: str, worker_url: str):
    # try multiple times on startup
    for attempt in range(5):
        try:
            ok = await register_to_orchestrator(orchestrator_url, worker_id, worker_url)
            if ok:
                print(f"registered worker {worker_id} -> {orchestrator_url}")
                return
        except Exception:
            await asyncio.sleep(1)
    print("failed to register after retries")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="worker")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8100)
    parser.add_argument("--orchestrator", default="http://127.0.0.1:8000")
    parser.add_argument("--id", default=None)
    parser.add_argument("--model", default=None)
    args = parser.parse_args()

    worker_id = args.id or f"worker-{args.port}"
    worker_url = f"http://{args.host}:{args.port}"

    app = create_worker_app(model_path=args.model)

    # schedule registration after server is up
    config = uvicorn.Config(app, host=args.host, port=args.port, log_level="info")
    server = uvicorn.Server(config)

    async def main():
        # start server in background
        server_task = asyncio.create_task(server.serve())
        # try registering
        await _run_register(args.orchestrator, worker_id, worker_url)
        await server_task

    asyncio.run(main())
