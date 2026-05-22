#!/usr/bin/env python3
"""
Prepare CSV lists for segmentation training.
Each row: img_path, mask_path, label

Paths modified for Sneha's laptop.
"""

import argparse
import csv
import random
from pathlib import Path

def read_split(path):
    with open(path, "r") as f:
        return [tuple(l.strip().split(",")) for l in f if l.strip()]

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--crops-root",
        default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\crops",
        help="Path to cropped images"
    )
    p.add_argument(
        "--splits-dir",
        default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\splits",
        help="Path to train/val/test split files"
    )
    p.add_argument(
        "--out",
        default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\data_lists",
        help="Where to write CSV files"
    )
    p.add_argument(
        "--max-samples",
        type=int,
        default=0,
        help="Limit total samples per split (0 = all)"
    )
    p.add_argument(
        "--sample-per-video",
        type=int,
        default=10,
        help="Max frames per video (0 = all)"
    )
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    random.seed(args.seed)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    splits = {
        "train": read_split(Path(args.splits_dir) / "train_videos.txt"),
        "val":   read_split(Path(args.splits_dir) / "val_videos.txt"),
        "test":  read_split(Path(args.splits_dir) / "test_videos.txt"),
    }

    def build_and_write(split_items, split_name):
        rows = []

        for video, label in split_items:
            label = int(label)
            img_dir = Path(args.crops_root) / ("fake_imgs" if label == 1 else "real") / video
            mask_dir = Path(args.crops_root) / "fake_masks" / video if label == 1 else None

            if not img_dir.exists():
                continue

            frames = sorted(img_dir.glob("*.jpg"))

            if args.sample_per_video > 0:
                frames = frames[:args.sample_per_video]

            for img_path in frames:
                mask_path = ""
                if label == 1:
                    mp = mask_dir / f"{img_path.stem}.png"
                    if mp.exists():
                        mask_path = str(mp)

                rows.append((str(img_path), mask_path, label))

        if args.max_samples > 0 and len(rows) > args.max_samples:
            random.shuffle(rows)
            rows = rows[:args.max_samples]

        out_csv = out_dir / f"{split_name}.csv"
        with open(out_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["img", "mask", "label"])
            writer.writerows(rows)

        print(f"{split_name}: wrote {len(rows)} samples")

    for split_name, split_items in splits.items():
        build_and_write(split_items, split_name)

    print("prepare_pairs completed.")
