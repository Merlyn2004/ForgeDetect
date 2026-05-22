import os
import librosa
import numpy as np

def check_folder(folder_path, max_files=50):
    sample_rates = []
    durations = []

    files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".flac")
    ][:max_files]

    for f in files:
        path = os.path.join(folder_path, f)
        y, sr = librosa.load(path, sr=None)  # sr=None = no resampling
        sample_rates.append(sr)
        durations.append(len(y) / sr)

    print(f"\nFolder: {folder_path}")
    print("Unique sample rates:", set(sample_rates))
    print(
        f"Duration (sec): min={min(durations):.2f}, "
        f"max={max(durations):.2f}, "
        f"mean={np.mean(durations):.2f}"
    )

# ====== CHANGE THESE PATHS ======
check_folder("C:/Users/merly/Downloads/dataset_subset/real")
check_folder("C:/Users/merly/Downloads/dataset_subset/fake")

