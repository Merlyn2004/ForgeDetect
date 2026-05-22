import numpy as np
import librosa
from scipy.fftpack import dct

SR = 16000
N_FFT = 512
HOP_LEN = 160
WIN_LEN = 400
N_FILTERS = 20
N_LFCC = 20

def extract_lfcc(y):
    stft = np.abs(
        librosa.stft(
            y,
            n_fft=N_FFT,
            hop_length=HOP_LEN,
            win_length=WIN_LEN,
            window="hann"
        )
    ) ** 2

    freqs = np.linspace(0, SR // 2, N_FFT // 2 + 1)
    edges = np.linspace(0, SR // 2, N_FILTERS + 2)

    filterbank = np.zeros((N_FILTERS, len(freqs)))
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

    return dct(log_energy, type=2, axis=0, norm="ortho")[:N_LFCC]
