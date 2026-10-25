from typing import List, Dict, Any
import torch
import numpy as np
from .model import load_model

class InferenceEngine:
    def __init__(self, model_path: str = None, device: str = "cpu"):
        self.device = device
        self.model = load_model(model_path, device=self.device)

    def predict(self, inputs: List[float]) -> Dict[str, Any]:
        # Convert input list to tensor, support variable-length by padding/truncating
        arr = np.array(inputs, dtype=np.float32)
        if arr.ndim != 1:
            raise ValueError("input must be a 1D list of floats")
        # expected input dim is 8; if different, pad or truncate
        expected = 8
        if arr.size < expected:
            arr = np.pad(arr, (0, expected - arr.size), mode='constant')
        elif arr.size > expected:
            arr = arr[:expected]
        tensor = torch.from_numpy(arr).float().unsqueeze(0)
        with torch.no_grad():
            logits = self.model(tensor)
            probs = torch.softmax(logits, dim=-1).squeeze(0).cpu().numpy().tolist()
            pred = int(np.argmax(probs))
        return {"prediction": pred, "probabilities": probs}
