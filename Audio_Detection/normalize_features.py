import os
import numpy as np

# ================= CONFIG =================
FEATURE_DIR = "features"          # training: features/, eval: features_eval/
MODE = "eval"                    # "train" or "eval"
NORM_DIR = "normalization"        # where mean/std are stored
os.makedirs(NORM_DIR, exist_ok=True)
# =========================================


def load_all_features(feature_dir):
    feats = []
    for cls in ["real", "fake"]:
        folder = os.path.join(feature_dir, cls)
        for f in os.listdir(folder):
            feat = np.load(os.path.join(folder, f))
            feats.append(feat)
    return feats


if MODE == "train":
    print("Running normalization in TRAIN mode")

    all_feats = load_all_features(FEATURE_DIR)
    all_feats = np.concatenate(all_feats, axis=1)  # (20, total_frames)

    mean = np.mean(all_feats, axis=1, keepdims=True)
    std = np.std(all_feats, axis=1, keepdims=True) + 1e-8

    np.save(os.path.join(NORM_DIR, "mean.npy"), mean)
    np.save(os.path.join(NORM_DIR, "std.npy"), std)

    print("Saved normalization mean/std")

elif MODE == "eval":
    print("Running normalization in EVAL mode")

    mean = np.load(os.path.join(NORM_DIR, "mean.npy"))
    std = np.load(os.path.join(NORM_DIR, "std.npy"))

else:
    raise ValueError("MODE must be 'train' or 'eval'")

# ---------- Apply normalization ----------
for cls in ["real", "fake"]:
    folder = os.path.join(FEATURE_DIR, cls)
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        feat = np.load(path)
        feat = (feat - mean) / std
        np.save(path, feat)

print("Normalization complete.")
