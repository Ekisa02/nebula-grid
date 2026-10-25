import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from .model import SmallMLP

def synthesize_dataset(n=1000, input_dim=8):
    X = np.random.randn(n, input_dim).astype('float32')
    y = (X.sum(axis=1) > 0).astype('int64')
    return X, y

def train_and_save(path='model.pt'):
    X, y = synthesize_dataset(2000)
    dataset = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    loader = DataLoader(dataset, batch_size=64, shuffle=True)
    model = SmallMLP()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.CrossEntropyLoss()
    for epoch in range(5):
        total = 0.0
        for xb, yb in loader:
            opt.zero_grad()
            logits = model(xb)
            loss = loss_fn(logits, yb)
            loss.backward()
            opt.step()
            total += loss.item()
        print(f"epoch {epoch} loss {total}")
    torch.save(model.state_dict(), path)

if __name__ == '__main__':
    train_and_save()
