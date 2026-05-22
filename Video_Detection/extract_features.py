#!/usr/bin/env python3
import torch
import numpy as np
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from torchvision import transforms
from efficientnet_pytorch import EfficientNet

# ---------- CONFIG ----------
CROPS_ROOT = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\crops"
OUT_ROOT   = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\features"

BATCH_SIZE = 16          # safe for most NVIDIA GPUs
IMG_SIZE   = 224
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# ---------------------------

transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def load_model():
    model = EfficientNet.from_pretrained("efficientnet-b4")
    model.to(DEVICE)
    model.eval()
    return model

@torch.no_grad()
def extract_video(model, in_dir, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = sorted(in_dir.glob("*.jpg"))

    batch_imgs = []
    batch_names = []

    for f in frames:
        img = Image.open(f).convert("RGB")
        img = transform(img)
        batch_imgs.append(img)
        batch_names.append(f.stem)

        if len(batch_imgs) == BATCH_SIZE:
            process_batch(model, batch_imgs, batch_names, out_dir)
            batch_imgs, batch_names = [], []

    if batch_imgs:
        process_batch(model, batch_imgs, batch_names, out_dir)

def process_batch(model, imgs, names, out_dir):
    x = torch.stack(imgs).to(DEVICE)
    feats = model.extract_features(x)
    feats = torch.mean(feats, dim=[2, 3])  # Global Avg Pool
    feats = feats.cpu().numpy()

    for f, name in zip(feats, names):
        np.save(out_dir / f"{name}.npy", f)

def main():
    model = load_model()

    for subset in ["real", "fake_imgs"]:
        in_root  = Path(CROPS_ROOT) / subset
        out_root = Path(OUT_ROOT) / subset

        for video in tqdm(list(in_root.iterdir()), desc=f"Extracting {subset}"):
            if not video.is_dir():
                continue
            extract_video(model, video, out_root / video.name)

    print("✅ EfficientNet-B4 features extracted")

if __name__ == "__main__":
    main()
