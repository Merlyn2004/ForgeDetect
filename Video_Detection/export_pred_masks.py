import torch
import numpy as np
import cv2
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import segmentation_models_pytorch as smp

# ---------- CONFIG ----------
CROPS_ROOT = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\crops"
OUT_ROOT   = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\pred_masks"
CKPT_PATH  = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\segmentation_run\best_model.pth"

IMG_SIZE   = 224
DEVICE     = "cuda" if torch.cuda.is_available() else "cpu"
THRESHOLD  = 0.5
# ----------------------------

def load_model():
    model = smp.Unet(
        encoder_name="resnet34",
        encoder_weights=None,
        in_channels=3,
        classes=1
    )

    ckpt = torch.load(CKPT_PATH, map_location=DEVICE)
    model.load_state_dict(ckpt["model_state"])
    model.to(DEVICE)
    model.eval()
    return model

def preprocess(img):
    img = img.resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(img).astype("float32") / 255.0
    arr = arr.transpose(2, 0, 1)  # HWC → CHW
    return torch.from_numpy(arr).unsqueeze(0)

def run_subset(model, subset):
    in_root  = Path(CROPS_ROOT) / subset
    out_root = Path(OUT_ROOT) / subset
    out_root.mkdir(parents=True, exist_ok=True)

    for video in in_root.iterdir():
        if not video.is_dir():
            continue

        out_video = out_root / video.name
        out_video.mkdir(parents=True, exist_ok=True)

        frames = sorted(video.glob("*.jpg"))

        for f in tqdm(frames, desc=f"{subset}/{video.name}", leave=False):
            img = Image.open(f).convert("RGB")
            x = preprocess(img).to(DEVICE)

            with torch.no_grad():
                pred = torch.sigmoid(model(x))[0, 0].cpu().numpy()

            mask = (pred > THRESHOLD).astype("uint8") * 255
            cv2.imwrite(str(out_video / (f.stem + ".png")), mask)

if __name__ == "__main__":
    model = load_model()
    run_subset(model, "fake_imgs")
    run_subset(model, "real")
    print("✅ Predicted masks exported successfully.")
