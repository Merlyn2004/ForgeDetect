--------------------------------------------
🎙️ Audio Deepfake Detection (ASVspoof 2019 LA – Subset)
--------------------------------------------

This module detects spoofed / synthetic speech using a subset of
the ASVspoof 2019 Logical Access (LA) dataset.

Only a balanced subset was used:

- 800 Bonafide (Real) samples
- 800 Spoof (Fake) samples
- Total: 1600 audio files

The system extracts LFCC features and uses a hybrid
CNN + Bidirectional LSTM architecture to classify
audio as Bonafide or Spoof.

--------------------------------------------
📂 Dataset Details
--------------------------------------------

Dataset: ASVspoof 2019 – Logical Access (LA)

Subset Used:
- 800 Real (Bonafide)
- 800 Fake (Spoof)
- Balanced dataset
- Audio format: .flac
- Sample rate: 16 kHz

--------------------------------------------
⚙️ Audio Processing Pipeline
--------------------------------------------

1️⃣ Preprocessing
   - Resample to 16 kHz
   - Convert to mono
   - Pad / truncate to fixed length (6 seconds)

2️⃣ LFCC Feature Extraction
   - 20 linear filterbank coefficients
   - STFT-based spectral analysis
   - DCT applied to log energies
   - Output shape: (20, Time)

3️⃣ Feature Normalization
   - Mean and std computed from training data
   - Applied to validation and evaluation
   - Prevents data leakage

--------------------------------------------
🧠 Model Architecture
--------------------------------------------

CNN + BiLSTM

CNN Layers:
- Conv1D (20 → 64)
- BatchNorm + ReLU + MaxPool
- Conv1D (64 → 128)
- BatchNorm + ReLU + MaxPool

BiLSTM:
- Hidden size: 64
- Bidirectional

Final Layer:
- Fully connected (128 → 2 classes)

--------------------------------------------
📊 Training Setup
--------------------------------------------

- Optimizer: Adam
- Loss: CrossEntropyLoss
- Batch size: 16
- Epochs: 40
- Train/Validation split: 75% / 25%
- Best model saved automatically

--------------------------------------------
🧠 Final Audio Flow
--------------------------------------------

Audio
→ Resample (16kHz)
→ Pad / Truncate (6 sec)
→ LFCC Extraction
→ Normalization
→ CNN Feature Learning
→ BiLSTM Temporal Modeling
→ Bonafide / Spoof Prediction

--------------------------------------------
✅ Key Highlights
--------------------------------------------

- Uses balanced subset (1600 total samples)
- LFCC-based spoof detection
- Combines spectral + temporal modeling
- Prevents data leakage via proper normalization
- Checkpoint-based training
- Lightweight and reproducible

--------------------------------------------