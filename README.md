# Nebula Grid

Nebula Grid is a modular distributed cloud system reference implementation that demonstrates how to orchestrate and execute PyTorch model inference across multiple worker nodes using FastAPI for control and HTTP-based task dispatch. The project is built to be lightweight, extensible, and suitable as a starting point for production-grade distributed inference systems.

Key features:
- Orchestrator service for worker registration and task scheduling (round-robin by default).
- Worker service that hosts a PyTorch model and performs inference via an HTTP API.
- Clean modular Python layout with FastAPI, pydantic and httpx for async communication.
- Example model, basic training utilities, and tests.

Architecture
------------
(Components)
- Orchestrator (FastAPI):
  - /workers/register - workers POST here to register themselves
  - /predict - clients send inference requests; orchestrator schedules the request to a worker
- Worker (FastAPI):
  - /task/predict - accepts input, runs local PyTorch model, returns result
  - registration client helper to register to an orchestrator
- Scheduler: simple pluggable scheduler (round-robin implemented)

Flow:
1. Workers start, load their model, and register with the orchestrator.
2. Clients POST inference requests to the orchestrator's /predict endpoint.
3. Orchestrator selects a healthy worker and forwards the request.
4. Worker returns inference results back to orchestrator, which relays to the client.

Installation
------------
Prerequisites: Python 3.9+, pip, optional Docker.

1) Create a virtual environment and install dependencies

    python -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

2) Run the orchestrator locally

    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

3) Run a worker locally (in another terminal). Edit configs in app/utils/config.py if needed

    python -m app.worker.service --host 0.0.0.0 --port 8100 --orchestrator http://localhost:8000

Usage
-----
- Register a worker: worker service script will register automatically (see service CLI).
- Submit a prediction:

    POST http://localhost:8000/predict
    JSON body: {"input": [0.1, 0.2, 0.3, ...]}

Example using curl:

    curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"input": [0.5, 0.4, 0.1, 0.9]}'

Testing
-------
Run unit tests with pytest:

    pytest -q

Project Layout
--------------
- app/              - application package
  - main.py         - orchestrator FastAPI app
  - api/            - HTTP route modules
  - orchestrator/   - registry and scheduler
  - worker/         - worker app, client and service runner
  - ml/             - model, inference and training utilities
  - utils/          - configuration and helpers
- tests/            - test-suite
- docs/             - additional documentation
- docker/           - example Dockerfiles

Extending
---------
- Replace scheduler with latency-aware or load-aware scheduler.
- Add gRPC for faster RPC between orchestrator and workers.
- Add authentication and mutual TLS for secure communication.

License
-------
MIT
