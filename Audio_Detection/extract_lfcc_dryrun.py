import os
import numpy as np
import librosa
from scipy.fftpack import dct
from lfcc_utils import extract_lfcc

# ================= CONFIG =================
SR = 16000
FIXED_SECONDS = 6
FIXED_LEN = SR * FIXED_SECONDS

N_FFT = 512
HOP_LEN = 160
WIN_LEN = 400
N_FILTERS = 20
N_LFCC = 20

MAX_FILES = 10  # <<< change to 20 / 50 / 100 for dry run
# ==========================================


def pad_or_truncate(y, target_len):
    if len(y) < target_len:
        return np.pad(y, (0, target_len - len(y)))
    return y[:target_len]


def extract_lfcc(signal, sr):
    stft = np.abs(
        librosa.stft(
            signal,
            n_fft=N_FFT,
            hop_length=HOP_LEN,
            win_length=WIN_LEN,
            window="hann"
        )
    ) ** 2

    freqs = np.linspace(0, sr // 2, N_FFT // 2 + 1)
    filterbank = np.zeros((N_FILTERS, len(freqs)))

    edges = np.linspace(0, sr // 2, N_FILTERS + 2)

    for i in range(N_FILTERS):
        left, center, right = edges[i:i+3]
        for j, f in enumerate(freqs):
            if left <= f < center:
                filterbank[i, j] = (f - left) / (center - left)
            elif center <= f <= right:
                filterbank[i, j] = (right - f) / (right - center)

    energy = np.dot(filterbank, stft)
    energy = np.where(energy == 0, np.finfo(float).eps, energy)

    log_energy = np.log(energy)
    lfcc = dct(log_energy, type=2, axis=0, norm="ortho")[:N_LFCC]

    return lfcc


def process_folder(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.endswith(".flac")]
    if MAX_FILES is not None:
        files = files[:MAX_FILES]


    print(f"\nProcessing {len(files)} files from {input_dir}")

    for f in files:
        path = os.path.join(input_dir, f)
        y, sr = librosa.load(path, sr=SR)

        y = pad_or_truncate(y, FIXED_LEN)
        feat = extract_lfcc(y, sr)

        np.save(
            os.path.join(output_dir, f.replace(".flac", ".npy")),
            feat
        )

        print(f"{f} -> LFCC shape {feat.shape}")


# ============== RUN DRY TEST ==============
process_folder("C:/Users/merly/Downloads/dataset_subset/real", "features/real")
process_folder("C:/Users/merly/Downloads/dataset_subset/fake", "features/fake")

print("\nDry run LFCC extraction DONE.")

