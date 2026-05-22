import os
import subprocess
import numpy as np
import torch
import torch.nn as nn
import librosa

from lfcc_utils import extract_lfcc   # 🔴 SAME LFCC AS TRAINING

# ================= CONFIG =================
MODEL_PATH = "checkpoints/best_model.pth"
MEAN_PATH = "normalization/mean.npy"
STD_PATH = "normalization/std.npy"

SR = 16000
FIXED_LEN = 6 * SR
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# =========================================


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
        self.lstm = nn.LSTM(128, 64, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(128, 2)

    def forward(self, x):
        x = x.transpose(1, 2)
        x = self.cnn(x)
        x = x.transpose(1, 2)
        _, (h, _) = self.lstm(x)
        h = torch.cat((h[-2], h[-1]), dim=1)
        return self.fc(h)


# ---------- Audio loading ----------
def extract_audio_from_video(video_path, out_wav="__temp.wav"):
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-ac", "1",
        "-ar", str(SR),
        out_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_wav


def load_audio_any_format(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    ext = os.path.splitext(path)[1].lower()
    video_exts = [".mp4", ".mkv", ".avi", ".mov", ".webm"]

    if ext in video_exts:
        path = extract_audio_from_video(path)

    y, _ = librosa.load(path, sr=SR, mono=True)
    return y


def pad_or_truncate(y):
    if len(y) < FIXED_LEN:
        return np.pad(y, (0, FIXED_LEN - len(y)))
    return y[:FIXED_LEN]


# ---------- Prediction ----------
def predict(file_path):
    mean = np.load(MEAN_PATH)
    std = np.load(STD_PATH)

    # Load + preprocess audio
    y = load_audio_any_format(file_path)
    y = pad_or_truncate(y)

    # LFCC (IDENTICAL to training)
    lfcc = extract_lfcc(y)

    # Normalize using TRAIN stats
    lfcc = (lfcc - mean) / std

    # Model input
    x = torch.tensor(lfcc.T, dtype=torch.float32).unsqueeze(0).to(DEVICE)

    # Load model
    model = CNN_BiLSTM().to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()

    # Predict
    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

    label = "Real" if probs[0] > probs[1] else "Fake"
    confidence = probs.max() * 100

    print("\n===== DEMO RESULT =====")
    print(f"File       : {file_path}")
    print(f"Prediction : {label}")
    print(f"Confidence : {confidence:.2f}%")
    print("=======================\n")


# predict("sample.mp4")
# predict("sample.wav")
predict("E:/C_0000_15_D.wav")