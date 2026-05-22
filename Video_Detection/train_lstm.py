#!/usr/bin/env python3
"""
BiLSTM Training for Video Deepfake Detection
- Auto resume from checkpoint
- Best model saving
- Accuracy & loss plots
"""

import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# ================= CONFIG ================= #
MANIFEST_PATH = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\sequences\manifest.csv"
OUT_DIR       = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\lstm_run"

EPOCHS = 25
BATCH  = 8
LR     = 1e-4

INPUT_DIM = 1792      # EfficientNet-B4
HIDDEN    = 512
# ========================================= #

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", DEVICE)

OUT_DIR = Path(OUT_DIR)
OUT_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PATH = OUT_DIR / "last_checkpoint.pth"
BEST_PATH = OUT_DIR / "best_lstm.pth"

# ================= Dataset ================= #
class SequenceDataset(Dataset):
    def __init__(self, csv_path, split):
        df = pd.read_csv(csv_path)
        self.df = df[df["split"] == split].reset_index(drop=True)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        x = np.load(row["path"])
        y = int(row["label"])
        return torch.tensor(x, dtype=torch.float32), y


# ================= Model ================= #
class BiLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(
            INPUT_DIM,
            HIDDEN,
            num_layers=2,
            batch_first=True,
            bidirectional=True,
            dropout=0.3
        )

        self.fc = nn.Sequential(
            nn.Linear(HIDDEN * 2, 256),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(256, 2)
        )

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1])


# ================= Training ================= #
def main():
    train_ds = SequenceDataset(MANIFEST_PATH, "train")
    val_ds   = SequenceDataset(MANIFEST_PATH, "val")

    train_loader = DataLoader(train_ds, BATCH, shuffle=True)
    val_loader   = DataLoader(val_ds, BATCH, shuffle=False)

    model = BiLSTM().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    criterion = nn.CrossEntropyLoss()

    start_epoch = 1
    best_val_acc = 0.0

    train_accs, val_accs = [], []
    train_losses, val_losses = [], []

    # -------- Resume if exists -------- #
    if CKPT_PATH.exists():
        ckpt = torch.load(CKPT_PATH, map_location=DEVICE)
        model.load_state_dict(ckpt["model"])
        optimizer.load_state_dict(ckpt["optimizer"])
        start_epoch = ckpt["epoch"] + 1
        best_val_acc = ckpt["best_val_acc"]
        train_accs = ckpt["train_accs"]
        val_accs   = ckpt["val_accs"]
        train_losses = ckpt["train_losses"]
        val_losses   = ckpt["val_losses"]
        print(f"🔁 Resumed from epoch {ckpt['epoch']}")

    # -------- Training Loop -------- #
    for epoch in range(start_epoch, EPOCHS + 1):
        model.train()
        correct = total = 0
        loss_sum = 0.0

        for x, y in tqdm(train_loader, desc=f"Epoch {epoch} [Train]"):
            x, y = x.to(DEVICE), y.to(DEVICE)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()

            loss_sum += loss.item()
            pred = out.argmax(1)
            correct += (pred == y).sum().item()
            total += y.size(0)

        train_acc = correct / total
        train_loss = loss_sum / len(train_loader)

        model.eval()
        correct = total = 0
        val_loss_sum = 0.0

        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(DEVICE), y.to(DEVICE)
                out = model(x)
                loss = criterion(out, y)

                val_loss_sum += loss.item()
                pred = out.argmax(1)
                correct += (pred == y).sum().item()
                total += y.size(0)

        val_acc = correct / total
        val_loss = val_loss_sum / len(val_loader)

        train_accs.append(train_acc)
        val_accs.append(val_acc)
        train_losses.append(train_loss)
        val_losses.append(val_loss)

        print(
            f"Epoch {epoch} | "
            f"TrainAcc={train_acc:.4f} ValAcc={val_acc:.4f} | "
            f"TrainLoss={train_loss:.4f} ValLoss={val_loss:.4f}"
        )

        # -------- Save checkpoint -------- #
        torch.save({
            "epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "best_val_acc": best_val_acc,
            "train_accs": train_accs,
            "val_accs": val_accs,
            "train_losses": train_losses,
            "val_losses": val_losses
        }, CKPT_PATH)

        # -------- Save best model -------- #
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), BEST_PATH)
            print("✅ Best model updated")

    # ================= Plots ================= #
    plot_curves(train_accs, val_accs, "Accuracy", "accuracy.png")
    plot_curves(train_losses, val_losses, "Loss", "loss.png")

    print("🎉 Training complete. Plots saved.")


def plot_curves(train, val, title, fname):
    plt.figure()
    plt.plot(train, label="Train")
    plt.plot(val, label="Validation")
    plt.title(title)
    plt.xlabel("Epoch")
    plt.ylabel(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(OUT_DIR / fname)
    plt.close()


if __name__ == "__main__":
    main()
