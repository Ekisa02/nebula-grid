# Example: send a prediction to the orchestrator
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"input": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]}'
