help:
	@echo "Available targets: test, run-orchestrator, run-worker"

test:
	pytest -q

run-orchestrator:
	uvicorn app.main:app --reload

run-worker:
	python -m app.worker.service
