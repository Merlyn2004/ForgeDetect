#!/usr/bin/env python3
import numpy as np
import csv
from pathlib import Path
from multiprocessing import Pool, cpu_count

# ---------- CONFIG ----------
FEATURES_ROOT = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\features"
SPLITS_ROOT   = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\splits"
OUT_ROOT      = r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\sequences"

SEQ_LEN = 16
STRIDE  = 8
WORKERS = max(1, cpu_count() - 1)
# ---------------------------

def read_split(path):
    with open(path) as f:
        return [line.strip().split(",") for line in f if line.strip()]

def process_video(args):
    video, label, split = args
    label = int(label)
    sub = "fake_imgs" if label == 1 else "real"

    feat_dir = Path(FEATURES_ROOT) / sub / video
    if not feat_dir.exists():
        return []

    feats = [np.load(f) for f in sorted(feat_dir.glob("*.npy"))]
    rows = []

    out_dir = Path(OUT_ROOT) / split
    out_dir.mkdir(parents=True, exist_ok=True)

    i = seq_id = 0
    while i + SEQ_LEN <= len(feats):
        seq = np.stack(feats[i:i + SEQ_LEN])
        out_path = out_dir / f"{video}_seq{seq_id}.npy"
        np.save(out_path, seq)
        rows.append([str(out_path), label, video, split])
        i += STRIDE
        seq_id += 1

    return rows

def build(split):
    split_list = read_split(Path(SPLITS_ROOT) / f"{split}_videos.txt")
    tasks = [(v, l, split) for v, l in split_list]

    rows = []
    with Pool(WORKERS) as p:
        for r in p.imap_unordered(process_video, tasks):
            rows.extend(r)

    return rows

if __name__ == "__main__":
    Path(OUT_ROOT).mkdir(parents=True, exist_ok=True)

    manifest = []
    for split in ["train", "val", "test"]:
        manifest.extend(build(split))

    with open(Path(OUT_ROOT) / "manifest.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "label", "video", "split"])
        writer.writerows(manifest)

    print("✅ Sequences built (CPU-parallel)")
