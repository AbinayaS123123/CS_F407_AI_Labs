"""
Neural Models Lab: Learning, Depth, Activations, and Output Layers
Implements Tasks 1–5 from the supplied lab sheet.
Run: python neural_models_lab.py
Requires: torch
"""
import random
import numpy as np
import torch
from torch import nn

torch.set_num_threads(1)
SEED = 1
torch.manual_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)

X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = torch.tensor([[0.], [1.], [1.], [0.]])

class XORNet(nn.Module):
    def __init__(self, activation="sigmoid", outputs=1, zero_init=False):
        super().__init__()
        self.fc1 = nn.Linear(2, 2)
        self.fc2 = nn.Linear(2, outputs)
        self.activation = activation
        if zero_init:
            for p in self.parameters():
                nn.init.zeros_(p)

    def forward(self, x):
        z = self.fc1(x)
        if self.activation == "sigmoid":
            h = torch.sigmoid(z)
        elif self.activation == "tanh":
            h = torch.tanh(z)
        elif self.activation == "relu":
            h = torch.relu(z)
        else:
            raise ValueError("Unknown activation")
        return self.fc2(h)  # logits; sigmoid is applied only for reporting binary probabilities

def train_binary(activation="sigmoid", seed=SEED, steps=10000, lr=0.03,
                 zero_init=False, report_early_grad=False):
    torch.manual_seed(seed)
    model = XORNet(activation=activation, zero_init=zero_init)
    loss_fn = nn.BCEWithLogitsLoss()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    early_grad_norm = None
    initial_loss = float(loss_fn(model(X), y).item())
    for step in range(steps):
        opt.zero_grad()
        logits = model(X)
        loss = loss_fn(logits, y)
        loss.backward()
        if step == 0:
            early_grad_norm = float(torch.linalg.vector_norm(model.fc1.weight.grad).item())
        opt.step()
    with torch.no_grad():
        logits = model(X)
        final_loss = float(loss_fn(logits, y).item())
        probs = torch.sigmoid(logits).squeeze(1)
        preds = (probs >= 0.5).int()
    return model, initial_loss, final_loss, probs.tolist(), preds.tolist(), early_grad_norm

def task1_and_2():
    print("TASK 1 — PROBLEM SPECIFICATION")
    print("X = {(0,0), (0,1), (1,0), (1,1)}; Y = {0,1}; labels = [0,1,1,0] (XOR).")
    print("A single affine map plus sigmoid has a linear decision boundary, so it cannot represent XOR.")
    print("\nTASK 2/3/4A — BINARY XOR (2-2-1, sigmoid hidden, BCEWithLogitsLoss)")
    model, initial, final, probs, preds, grad = train_binary("sigmoid", seed=1)
    print(f"seed=1, Adam lr=0.03, steps=10000, initial_loss={initial:.8f}, final_loss={final:.8f}")
    print("probabilities:", [round(p, 8) for p in probs])
    print("predicted labels:", preds, "| target:", [0,1,1,0], "| correct:", preds == [0,1,1,0])
    print("first-layer weight-gradient L2 norm at first backward:", f"{grad:.8g}")
    print("first-layer weight gradient after training:\n", model.fc1.weight.grad)
    return model

def symmetry_experiment():
    print("\nTASK 4C — ZERO-INITIALISATION SYMMETRY")
    model, initial, final, probs, preds, grad = train_binary(
        "sigmoid", seed=1, steps=1000, lr=0.03, zero_init=True)
    w = model.fc1.weight.detach()
    print(f"initial_loss={initial:.8f}, final_loss={final:.8f}")
    print("hidden weight row 1:", w[0].tolist())
    print("hidden weight row 2:", w[1].tolist())
    print("rows identical:", bool(torch.allclose(w[0], w[1])))
    print("probabilities:", [round(p, 6) for p in probs], "predictions:", preds)
    print("Explanation: identical hidden units receive identical gradients and remain identical; they cannot learn distinct XOR features.")

def activation_experiment():
    print("\nTASK 4D — ACTIVATION EXPERIMENT (same seed=1, 10000 steps, Adam lr=0.03)")
    print("Activation | final loss | 4/4 correct | early ||grad W1||_2 | probabilities")
    for act in ("sigmoid", "tanh", "relu"):
        _, _, final, probs, preds, grad = train_binary(act, seed=1, steps=10000, lr=0.03)
        print(f"{act:9s} | {final:.8g} | {preds == [0,1,1,0]} | {grad:.8g} | {[round(p,6) for p in probs]}")

def multiclass_experiment():
    print("\nTASK 5 — THREE-CLASS EXTENSION")
    # Class 0=(0,0), class 1=(0,1)/(1,0), class 2=(1,1)
    labels = torch.tensor([0, 1, 1, 2], dtype=torch.long)
    torch.manual_seed(2)
    model = XORNet(activation="sigmoid", outputs=3)
    loss_fn = nn.CrossEntropyLoss()
    opt = torch.optim.Adam(model.parameters(), lr=0.03)
    initial = float(loss_fn(model(X), labels).item())
    for _ in range(10000):
        opt.zero_grad()
        logits = model(X)
        loss = loss_fn(logits, labels)
        loss.backward()
        opt.step()
    with torch.no_grad():
        logits = model(X)
        probs = torch.softmax(logits, dim=1)
        preds = logits.argmax(dim=1)
        final = float(loss_fn(logits, labels).item())
    print("architecture: 2 inputs -> 2 hidden units -> 3 logits")
    print("final weight matrix shape:", tuple(model.fc2.weight.shape), "(3, 2)")
    print("number of logits per example: 3")
    print(f"initial_loss={initial:.8f}, final_loss={final:.8f}")
    print("class order for inputs [(0,0),(0,1),(1,0),(1,1)]: [0,1,1,2]")
    for x, p, pred in zip(X.tolist(), probs.tolist(), preds.tolist()):
        print(f"input={tuple(int(v) for v in x)} probabilities={[round(v,6) for v in p]} sum={sum(p):.8f} predicted_class={pred}")
    print("Softmax sums to one because it divides each exp(logit) by the sum of all exp(logits).")
    print("For cross-entropy with softmax, the gradient w.r.t. each logit is p - one_hot(target).")

if __name__ == "__main__":
    print("PyTorch version:", torch.__version__)
    task1_and_2()
    symmetry_experiment()
    activation_experiment()
    multiclass_experiment()
