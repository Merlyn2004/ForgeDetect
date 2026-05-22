#!/usr/bin/env python3
"""
Train segmentation model on CSV lists created by prepare_pairs.py.
Auto-resume from latest checkpoint.
One-command run: python train_segmentation.py
"""

import argparse
import csv
from pathlib import Path
import numpy as np
from PIL import Image
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

import albumentations as A
from albumentations.pytorch import ToTensorV2
import segmentation_models_pytorch as smp


# ---------------- Dataset ---------------- #
class CSVDataset(Dataset):
    def __init__(self, csvfile, size=224, augment=False):
        self.rows = []
        with open(csvfile, "r") as f:
            reader = csv.DictReader(f)
            for r in reader:
                self.rows.append(r)

        self.size = size
        self.augment = augment

        self.train_aug = A.Compose([
            A.Resize(size, size),
            A.HorizontalFlip(p=0.5),
            A.RandomBrightnessContrast(p=0.4),
            A.ImageCompression(quality_lower=60, quality_upper=95, p=0.4),
            A.Normalize(),
            ToTensorV2()
        ])

        self.val_aug = A.Compose([
            A.Resize(size, size),
            A.Normalize(),
            ToTensorV2()
        ])

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
     r = self.rows[idx]

     img = np.array(Image.open(r["img"]).convert("RGB"))

     if r["mask"]:
         mask = np.array(Image.open(r["mask"]).convert("L"))
         mask = (mask > 127).astype("uint8")
     else:
        mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)

     if self.augment:
        aug = self.train_aug(image=img, mask=mask)
        image = aug["image"]
        mask = aug["mask"].unsqueeze(0).float()   # ✅ FIX
     else:
        aug = self.val_aug(image=img)
        image = aug["image"]
        mask = Image.fromarray(mask).resize((self.size, self.size))
        mask = torch.from_numpy(
            (np.array(mask) > 127).astype("uint8")
        ).unsqueeze(0).float()

     return image, mask



# ---------------- Loss ---------------- #
class ComboLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.bce = nn.BCEWithLogitsLoss()
        self.dice = smp.losses.DiceLoss(mode="binary")

    def forward(self, preds, targets):
        return self.bce(preds, targets) + self.dice(torch.sigmoid(preds), targets)


def iou_score(preds, targets):
    preds = (preds > 0.5).float()
    inter = (preds * targets).sum(dim=(1, 2, 3))
    union = ((preds + targets) >= 1).float().sum(dim=(1, 2, 3))
    return ((inter + 1e-7) / (union + 1e-7)).mean().item()


# ---------------- Utils ---------------- #
def find_latest_checkpoint(out_dir):
    ckpts = sorted(Path(out_dir).glob("last_epoch_*.pth"))
    return ckpts[-1] if ckpts else None


# ---------------- Training ---------------- #
def train(args):
    device = torch.device(args.device)

    train_ds = CSVDataset(Path(args.data_lists) / "train.csv", augment=True)
    val_ds = CSVDataset(Path(args.data_lists) / "val.csv", augment=False)

    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=True
    )

    print(f"Train samples: {len(train_ds)} | Val samples: {len(val_ds)}")
    print(f"Using device: {device}")

    model = smp.Unet(
        encoder_name=args.encoder,
        encoder_weights="imagenet",
        in_channels=3,
        classes=1
    ).to(device)

    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    criterion = ComboLoss()

    start_epoch = 1
    best_iou = 0.0

    if args.resume:
        ckpt = torch.load(args.resume, map_location=device)
        model.load_state_dict(ckpt["model_state"])
        optimizer.load_state_dict(ckpt["opt_state"])
        start_epoch = ckpt["epoch"] + 1
        best_iou = ckpt.get("best_iou", 0.0)
        print(f"[INFO] Resumed from {args.resume}")

    for epoch in range(start_epoch, args.epochs + 1):
        model.train()
        total_loss = 0.0

        for imgs, masks in tqdm(train_loader, desc=f"Epoch {epoch} [Train]"):
            imgs, masks = imgs.to(device), masks.to(device)

            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        train_loss = total_loss / len(train_loader)

        model.eval()
        val_loss = 0.0
        val_ious = []

        with torch.no_grad():
            for imgs, masks in tqdm(val_loader, desc="Validation"):
                imgs, masks = imgs.to(device), masks.to(device)
                outputs = model(imgs)
                val_loss += criterion(outputs, masks).item()
                val_ious.append(iou_score(torch.sigmoid(outputs), masks))

        val_loss /= len(val_loader)
        val_iou = float(np.mean(val_ious))

        print(
            f"Epoch {epoch}: "
            f"TrainLoss={train_loss:.4f} "
            f"ValLoss={val_loss:.4f} "
            f"ValIoU={val_iou:.4f}"
        )

        ckpt = {
            "epoch": epoch,
            "model_state": model.state_dict(),
            "opt_state": optimizer.state_dict(),
            "best_iou": best_iou
        }

        torch.save(ckpt, Path(args.out_dir) / f"last_epoch_{epoch}.pth")

        if val_iou > best_iou:
            best_iou = val_iou
            torch.save(ckpt, Path(args.out_dir) / "best_model.pth")
            print("[INFO] Best model updated")


# ---------------- Main ---------------- #
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data-lists", default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\data_lists")
    p.add_argument("--out-dir", default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\segmentation_run")
    p.add_argument("--epochs", type=int, default=15)
    p.add_argument("--batch-size", type=int, default=12)
    p.add_argument("--lr", type=float, default=1e-4)
    p.add_argument("--encoder", default="resnet34")
    p.add_argument("--num-workers", type=int, default=4)
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = p.parse_args()

    Path(args.out_dir).mkdir(parents=True, exist_ok=True)

    latest = find_latest_checkpoint(args.out_dir)
    args.resume = str(latest) if latest else ""

    if args.resume:
        print(f"[AUTO-RESUME] Using checkpoint: {args.resume}")
    else:
        print("[AUTO-RESUME] Starting fresh training")

    train(args)