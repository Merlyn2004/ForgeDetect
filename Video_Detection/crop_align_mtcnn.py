#!/usr/bin/env python3
"""
Detect faces with MTCNN, crop images and corresponding masks with same bbox,
resize to square, save to crops_root/{fake_imgs, fake_masks, real}/<video>/frame_xxx
CPU-optimized version (safe for resume)
"""

import argparse, os
from pathlib import Path
import cv2
import numpy as np
from mtcnn import MTCNN
from tqdm import tqdm

# ✅ MTCNN detector (runs on CPU since no GPU)
detector = MTCNN()

def expand_box(x, y, w, h, W, H, pad=0.20):  # ✅ reduced padding
    cx, cy = x + w / 2, y + h / 2
    nw, nh = w * (1 + pad), h * (1 + pad)
    x1 = int(max(0, cx - nw / 2))
    y1 = int(max(0, cy - nh / 2))
    x2 = int(min(W, cx + nw / 2))
    y2 = int(min(H, cy + nh / 2))
    return x1, y1, x2, y2

def detect_largest_face(img):
    try:
        res = detector.detect_faces(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    except Exception:
        return None
    if not res:
        return None
    face = max(res, key=lambda r: r['box'][2] * r['box'][3])
    x, y, w, h = face['box']
    return max(0, x), max(0, y), max(0, w), max(0, h)

def crop_pair(img_path, mask_path, out_img_path, out_mask_path, size, pad):
    img = cv2.imread(str(img_path))
    if img is None:
        return False, "noimg"

    H, W = img.shape[:2]

    # ✅ CPU OPTIMIZATION: detect on smaller image
    img_small = cv2.resize(img, (640, 640))
    det = detect_largest_face(img_small)
    if det is None:
        return False, "noface"

    x, y, w, h = det

    # ✅ Scale box back to original size
    sx = W / 640
    sy = H / 640
    x = int(x * sx)
    y = int(y * sy)
    w = int(w * sx)
    h = int(h * sy)

    x1, y1, x2, y2 = expand_box(x, y, w, h, W, H, pad)

    crop = img[y1:y2, x1:x2]
    crop = cv2.resize(crop, (size, size), interpolation=cv2.INTER_LINEAR)

    # --- MASK ---
    if mask_path and Path(mask_path).exists():
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if mask is None:
            mask = np.zeros((H, W), dtype=np.uint8)

        mask_crop = mask[y1:y2, x1:x2]
        mask_crop = cv2.resize(mask_crop, (size, size), interpolation=cv2.INTER_NEAREST)
        _, mask_crop = cv2.threshold(mask_crop, 127, 255, cv2.THRESH_BINARY)
    else:
        mask_crop = np.zeros((size, size), dtype=np.uint8)

    out_img_path.parent.mkdir(parents=True, exist_ok=True)
    out_mask_path.parent.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(out_img_path), crop, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    cv2.imwrite(str(out_mask_path), mask_crop)

    return True, "ok"

def process_subset(frames_root, masks_root, crops_root, subset, size, pad):
    frames_root = Path(frames_root)
    masks_root = Path(masks_root) if masks_root else None
    crops_root = Path(crops_root)

    in_dir = frames_root / subset
    if not in_dir.exists():
        print(f"[WARN] {in_dir} doesn't exist - skipping")
        return

    videos = sorted([p for p in in_dir.iterdir() if p.is_dir()])
    stats = {"ok": 0, "noface": 0, "noimg": 0, "skipped": 0}

    for v in tqdm(videos, desc=f"Process {subset}"):
        name = v.name

        out_img_vid = crops_root / ("real" if subset == "real" else "fake_imgs") / name
        out_mask_vid = crops_root / "fake_masks" / name if subset != "real" else out_img_vid

        frames = sorted([f for f in v.iterdir() if f.suffix.lower() in (".jpg", ".png")])

        # ✅ OPTIONAL: use every alternate frame for more speed
        # frames = frames[::2]

        for f in frames:
            base = f.name
            out_img = out_img_vid / base
            out_mask = out_mask_vid / (Path(base).stem + ".png")

            # ✅ AUTO-RESUME LOGIC (SAFE)
            if out_img.exists() and out_mask.exists():
                stats["skipped"] += 1
                continue

            mask_path = masks_root / name / (Path(base).stem + ".png") if masks_root else None
            ok, code = crop_pair(f, mask_path, out_img, out_mask, size, pad)
            stats[code] = stats.get(code, 0) + 1

    print(f"{subset} done: {stats}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--frames-root", default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\frames")
    p.add_argument("--masks-root", default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\frames\masks")
    p.add_argument("--crops-root", default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\crops")
    p.add_argument("--size", type=int, default=224)
    p.add_argument("--pad", type=float, default=0.20)
    p.add_argument("--process-real", action="store_true")

    args = p.parse_args()

    process_subset(args.frames_root, args.masks_root, args.crops_root, "fake", args.size, args.pad)

    if args.process_real:
        process_subset(args.frames_root, None, args.crops_root, "real", args.size, args.pad)

    print("crop_align finished.")
