import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

FEATURE_DIR = "features_eval"  # where eval features are stored
MODEL_PATH = "checkpoints/best_model.pth"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class LFCCDataset(Dataset):
    def __init__(self, files, labels):
        self.files = files
        self.labels = labels

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        x = np.load(self.files[idx])
        x = torch.tensor(x.T, dtype=torch.float32)
        y = torch.tensor(self.labels[idx])
        return x, y

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

files, labels = [], []
for label, cls in enumerate(["real", "fake"]):
    folder = os.path.join(FEATURE_DIR, cls)
    for f in os.listdir(folder):
        files.append(os.path.join(folder, f))
        labels.append(label)

loader = DataLoader(LFCCDataset(files, labels), batch_size=16)

model = CNN_BiLSTM().to(DEVICE)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval()

preds, gts = [], []
with torch.no_grad():
    for x, y in loader:
        x = x.to(DEVICE)
        out = model(x)
        preds.extend(out.argmax(1).cpu().numpy())
        gts.extend(y.numpy())

print("Accuracy:", accuracy_score(gts, preds)*100)
print("Confusion Matrix:\n", confusion_matrix(gts, preds))
print("Report:\n", classification_report(gts, preds, target_names=["Real","Fake"]))
