#!/usr/bin/env python3
"""
Create video-level train/val/test splits (80/10/10), class-balanced.
GPU NOT required.
"""

import argparse
import random
from pathlib import Path

def split_class(videos, val_frac, test_frac, seed):
    random.seed(seed)
    random.shuffle(videos)

    n = len(videos)
    n_val = int(n * val_frac)
    n_test = int(n * test_frac)
    n_train = n - n_val - n_test

    return (
        videos[:n_train],
        videos[n_train:n_train + n_val],
        videos[n_train + n_val:]
    )

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--crops-root",
        default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\crops",
        help="Path to crops folder"
    )
    p.add_argument(
        "--out-dir",
        default=r"C:\Users\sneha\OneDrive\Desktop\Video_deepfake\splits",
        help="Where to write split files"
    )
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--val-frac", type=float, default=0.1)
    p.add_argument("--test-frac", type=float, default=0.1)
    args = p.parse_args()

    crops = Path(args.crops_root)

    fake = sorted(
        [p.name for p in (crops / "fake_imgs").iterdir() if p.is_dir()]
    )
    real = sorted(
        [p.name for p in (crops / "real").iterdir() if p.is_dir()]
    )

    fake_split = split_class(fake, args.val_frac, args.test_frac, args.seed)
    real_split = split_class(real, args.val_frac, args.test_frac, args.seed)

    train = [(v, 1) for v in fake_split[0]] + [(v, 0) for v in real_split[0]]
    val   = [(v, 1) for v in fake_split[1]] + [(v, 0) for v in real_split[1]]
    test  = [(v, 1) for v in fake_split[2]] + [(v, 0) for v in real_split[2]]

    random.shuffle(train)
    random.shuffle(val)
    random.shuffle(test)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    def write(name, data):
        with open(out / name, "w") as f:
            for v, l in data:
                f.write(f"{v},{l}\n")

    write("train_videos.txt", train)
    write("val_videos.txt", val)
    write("test_videos.txt", test)

    print("Split completed:")
    print(f"  Train: {len(train)}")
    print(f"  Val:   {len(val)}")
    print(f"  Test:  {len(test)}")
