import os
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

# ================== CONFIG ==================
FEATURE_DIR = "features"
BATCH_SIZE = 16
EPOCHS = 40
LR = 1e-3
            # early stopping
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
SEED = 42
SAVE_DIR = "checkpoints"
os.makedirs(SAVE_DIR, exist_ok=True)
# ============================================


# ---------- Reproducibility ----------
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

set_seed(SEED)


# ---------- Dataset ----------
class LFCCDataset(Dataset):
    def __init__(self, files, labels):
        self.files = files
        self.labels = labels

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        x = np.load(self.files[idx])       # (20, T)
        x = torch.tensor(x.T, dtype=torch.float32)  # (T, 20)
        y = torch.tensor(self.labels[idx], dtype=torch.long)
        return x, y


def load_data():
    files, labels = [], []
    for label, cls in enumerate(["real", "fake"]):
        folder = os.path.join(FEATURE_DIR, cls)
        for f in os.listdir(folder):
            files.append(os.path.join(folder, f))
            labels.append(label)

    return train_test_split(
        files, labels,
        test_size=0.25,
        stratify=labels,
        random_state=SEED
    )


# ---------- Model ----------
class CNN_BiLSTM(nn.Module):
    def __init__(self):
        super().__init__()

        self.cnn = nn.Sequential(
            nn.Conv1d(20, 64, 5, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(64, 128, 5, padding=2),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(2),
        )

        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=64,
            bidirectional=True,
            batch_first=True
        )

        self.fc = nn.Linear(128, 2)

    def forward(self, x):
        x = x.transpose(1, 2)       # (B, 20, T)
        x = self.cnn(x)             # (B, 128, T')
        x = x.transpose(1, 2)       # (B, T', 128)
        _, (h, _) = self.lstm(x)
        h = torch.cat((h[-2], h[-1]), dim=1)
        return self.fc(h)


# ---------- Training ----------
train_files, val_files, train_labels, val_labels = load_data()

train_loader = DataLoader(
    LFCCDataset(train_files, train_labels),
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_loader = DataLoader(
    LFCCDataset(val_files, val_labels),
    batch_size=BATCH_SIZE
)

model = CNN_BiLSTM().to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

best_acc = 0


train_losses, val_losses, val_accs = [], [], []


for epoch in range(EPOCHS):
    # ---- Train ----
    model.train()
    total_loss = 0

    for x, y in train_loader:
        x, y = x.to(DEVICE), y.to(DEVICE)

        optimizer.zero_grad()
        out = model(x)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    train_loss = total_loss / len(train_loader)

    # ---- Validate ----
    model.eval()
    val_loss = 0
    correct, total = 0, 0

    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            out = model(x)
            loss = criterion(out, y)
            val_loss += loss.item()

            preds = out.argmax(1)
            correct += (preds == y).sum().item()
            total += y.size(0)

    val_loss /= len(val_loader)
    acc = 100 * correct / total

    train_losses.append(train_loss)
    val_losses.append(val_loss)
    val_accs.append(acc)

    print(
        f"Epoch {epoch+1:02d} | "
        f"Train Loss {train_loss:.3f} | "
        f"Val Loss {val_loss:.3f} | "
        f"Val Acc {acc:.2f}%"
    )

    # ---- Checkpoint ----
    if acc > best_acc:
        best_acc = acc
        torch.save(model.state_dict(), f"{SAVE_DIR}/best_model.pth")
        


# ---------- Save final model ----------
torch.save(model.state_dict(), f"{SAVE_DIR}/last_model.pth")


# ---------- Plot ----------
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Val Loss")
plt.legend()
plt.title("Loss Curve")

plt.subplot(1, 2, 2)
plt.plot(val_accs, label="Val Accuracy")
plt.legend()
plt.title("Validation Accuracy")

plt.tight_layout()
plt.savefig("training_curves.png")
plt.show()

print(f"Best Validation Accuracy: {best_acc:.2f}%")
