#!/usr/bin/env python3
"""
extract_frames.py

Usage examples (PowerShell / cmd):
    python extract_frames.py
    python extract_frames.py --dataset-root "E:\video\datasets\ffpp" --out-root "E:\video\frames" --fps 25

This script extracts frames from three FF++ folders:
- original_sequences/youtube/c23/videos  -> saved to out_root/real/<video_basename>/frame_00001.jpg
- manipulated_sequences/Deepfakes/c23/videos -> out_root/fake/<video_basename>/frame_00001.jpg
- manipulated_sequences/Deepfakes/masks/videos -> out_root/masks/<video_basename>/frame_00001.png

It prefers ffmpeg if available; otherwise uses OpenCV.
It skips videos already extracted (resume-friendly).
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import shutil

try:
    import cv2
except Exception:
    cv2 = None

def has_ffmpeg():
    return shutil.which("ffmpeg") is not None

def ffmpeg_extract(video_path: Path, out_dir: Path, fps: int, ext: str):
    out_pattern = str(out_dir / f"frame_%05d.{ext}")
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-i", str(video_path),
        "-vf", f"fps={fps}",
        "-q:v", "2",
        out_pattern
    ]
    # ensure out_dir exists
    out_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(cmd)
    return result.returncode == 0

def cv_extract(video_path: Path, out_dir: Path, fps: int, ext: str):
    if cv2 is None:
        raise RuntimeError("OpenCV is not installed (cv2). Install opencv-python-headless.")
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return False
    video_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    # compute frame step
    step = max(1, round(video_fps / fps)) if video_fps > 0 else 1
    out_dir.mkdir(parents=True, exist_ok=True)
    idx = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            out_file = out_dir / f"frame_{saved+1:05d}.{ext}"
            # use PNG for masks to avoid compression artifacts
            if ext.lower() == "png":
                cv2.imwrite(str(out_file), frame, [cv2.IMWRITE_PNG_COMPRESSION, 3])
            else:
                cv2.imwrite(str(out_file), frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            saved += 1
        idx += 1
    cap.release()
    return True

def extract_one(video_path: Path, out_dir: Path, fps: int, ext: str, use_ffmpeg: bool):
    # If output dir already has >=1 frames, skip it (resume)
    if out_dir.exists():
        existing = list(out_dir.glob(f"*.{ext}"))
        if len(existing) > 0:
            return "skipped"
    out_dir.mkdir(parents=True, exist_ok=True)
    if use_ffmpeg:
        ok = ffmpeg_extract(video_path, out_dir, fps, ext)
        if ok:
            return "done"
        # if ffmpeg failed, fall back to cv2
    ok = cv_extract(video_path, out_dir, fps, ext)
    return "done" if ok else "failed"

def gather_videos(input_dir: Path):
    if not input_dir.exists():
        return []
    videos = sorted([p for p in input_dir.glob("*.mp4")])
    return videos

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset-root", type=str, default=r"E:\video\datasets\ffpp",
                   help="Root of downloaded FF++ dataset (default matches your path)")
    p.add_argument("--out-root", type=str, default=r"E:\Video\frames",
                   help="Where to write extracted frames")
    p.add_argument("--fps", type=int, default=25, help="Frames per second to extract")
    p.add_argument("--use-ffmpeg", action="store_true", help="Force use of ffmpeg only (fail if not present)")
    p.add_argument("--skip-confirm", action="store_true", help="Skip the confirmation prompt")
    args = p.parse_args()

    ds = Path(args.dataset_root)
    out_root = Path(args.out_root)
    fps = args.fps

    # default locations based on your provided layout
    paths = {
        "real": ds / "original_sequences" / "youtube" / "c23" / "videos",
        "fake": ds / "manipulated_sequences" / "Deepfakes" / "c23" / "videos",
        "masks": ds / "manipulated_sequences" / "Deepfakes" / "masks" / "videos",
    }

    print("Dataset root:", ds)
    print("Output root:", out_root)
    print("Extraction FPS:", fps)
    print("Input folders (expected):")
    for k, v in paths.items():
        print(f"  {k}: {v}")
    if not args.skip_confirm:
        ok = input("Proceed with extraction? (y/N): ").strip().lower()
        if ok not in ("y","yes"):
            print("Aborted.")
            return

    use_ffmpeg_flag = has_ffmpeg()
    if args.use_ffmpeg:
        if not use_ffmpeg_flag:
            print("Warning: ffmpeg not found in PATH but --use-ffmpeg was set. Exiting.")
            return
        use_ffmpeg_flag = True

    print("ffmpeg available:", use_ffmpeg_flag)

    summary = {}
    for k, inp in paths.items():
        videos = gather_videos(inp)
        total = len(videos)
        got = {"done":0, "skipped":0, "failed":0}
        print(f"\nProcessing {k} videos: found {total} files in {inp}")
        # choose extension for frames
        ext = "png" if k == "masks" else "jpg"
        for v in tqdm(videos, desc=f"Extracting [{k}]", unit="video"):
            base = v.stem
            out_dir = out_root / k / base
            try:
                status = extract_one(v, out_dir, fps, ext, use_ffmpeg_flag)
            except Exception as e:
                status = "failed"
            got[status] = got.get(status,0) + 1
        summary[k] = got
        print(f"Finished {k}: {got['done']} done, {got['skipped']} skipped, {got['failed']} failed")

    print("\n=== Summary ===")
    for k, g in summary.items():
        print(f"{k}: done={g['done']}, skipped={g['skipped']}, failed={g['failed']}")
    print("\nCheck output folders under:", out_root)

if __name__ == "__main__":
    main()
