import torch
import torch.nn as nn

class SmallMLP(nn.Module):
    def __init__(self, input_dim: int = 8, hidden: int = 32, output_dim: int = 2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, output_dim)
        )

    def forward(self, x):
        return self.net(x)


def load_model(path: str = None, device: str = "cpu") -> nn.Module:
    input_dim = 8
    model = SmallMLP(input_dim=input_dim)
    if path:
        state = torch.load(path, map_location=device)
        model.load_state_dict(state)
    model.to(device)
    model.eval()
    return model
