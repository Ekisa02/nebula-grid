# Nebula Grid - Architecture

This document explains the high-level architecture and rationale.

Components
- Orchestrator Service
  - Provides worker lifecycle and a scheduling endpoint.
  - Exposes /workers/register and /predict endpoints.
  - Keeps a simple in-memory worker registry for demonstration.
- Worker Service
  - Hosts a local PyTorch model and an inference endpoint at /task/predict.
  - Registers itself with the orchestrator on startup.
- Scheduler
  - The default scheduler is round-robin. It is intentionally simple and pluggable.

Design goals
- Simplicity: minimal dependencies and HTTP-based RPC to be friendly with cloud platforms.
- Modularity: clear separation between orchestrator, worker, and ML code.
- Extensibility: replace scheduler, add authentication, or swap HTTP for gRPC.

Operational considerations
- For production use, replace in-memory registry with persistent store.
- Add health checks and retries with exponential backoff for worker communication.
- Add metrics and logging for observability (Prometheus, OpenTelemetry).
