# ForgeDetect
## 🎭 Multimodal Deepfake Detection System

An AI-powered multimodal deepfake detection system capable of detecting manipulated Image, Video, and Audio content using deep learning techniques.

The project combines:
- Image Deepfake Detection
- Video Deepfake Detection
- Audio Spoof Detection
- React Frontend
- Flask Backend
- Firebase Authentication & Firestore Database

The system provides a user-friendly web interface where users can upload media files and receive prediction results in real time.

> ⚠️ Note:
> Trained model weights (`.pth` files), datasets, Firebase secret keys, and environment files are intentionally excluded from this repository for security and storage reasons.

---

# 🚀 Features

✅ Image Deepfake Detection  
✅ Video Deepfake Detection  
✅ Audio Deepfake Detection  
✅ Real-time Prediction Results  
✅ Firebase Authentication  
✅ Admin Dashboard  
✅ Responsive React Frontend  
✅ Flask API Backend  
✅ Deep Learning Model Integration  
✅ Upload & Analyze Functionality  

---

# 🛠️ Technologies Used

## Frontend
- React.js
- HTML
- CSS
- JavaScript

## Backend
- Flask
- Python

## Database & Authentication
- Firebase Firestore
- Firebase Authentication

## Deep Learning
- PyTorch
- CNN
- BiLSTM
- EfficientNet-B4
- ResNet50
- MTCNN
- U-Net

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Merlyn2004/ForgeDetect.gir
```

## 2️⃣ Open the Project Folder

```bash
cd ForgeDetect
```

---

# 🌐 Frontend Setup

Only the `src` and `public` folders are provided in this repository.

## Create React App

```bash
npx create-react-app frontend
```

## Replace Generated Files

Replace the generated:
- `src`
- `public`

folders and files with the provided frontend files from this repository.

## Navigate to Frontend Folder

```bash
cd frontend
```

## Install Dependencies

```bash
npm install
```

## Start Frontend

```bash
npm start
```

Frontend will run on:

```bash
http://localhost:3000
```

---

# 🔥 Backend Setup

## Create Virtual Environment (Python 3.10 Recommended)

```bash
python -m venv venv
```

## Activate Virtual Environment (Windows)

```bash
venv\Scripts\activate
```

## Install Required Libraries

```bash
pip install -r requirements.txt
```

---

# 🔐 Firebase Setup

1. Create a Firebase project.
2. Enable:
   - Firebase Authentication
   - Firebase Firestore
3. Download the Firebase service account key.
4. Rename it as:

```bash
serviceAccountKey.json
```

5. Place the file inside the main project folder.

⚠️ Do NOT upload the Firebase service account key to GitHub.

---

# 🧠 Model Setup

The trained `.pth` model files are not included in this repository.

Users can:
- train the models using the provided implementation pipeline
- use their own trained model weights
- rename model files as needed and update the corresponding Flask code

The implementation pipelines for:
- Image Deepfake Detection
- Video Deepfake Detection
- Audio Deepfake Detection

are already provided inside their respective folders.

---

# ▶️ Running the Project

## Start Backend

```bash
python app.py
```

## Start Frontend

```bash
npm start
```

Open browser:

```bash
http://localhost:3000
```

---

# 🖼️ Image Deepfake Detection

## Dataset Used

Dataset:
https://www.kaggle.com/datasets/manjilkarki/deepfake-and-real-images

Subset of:
OpenForensics Dataset

---

## Image Detection Pipeline

```text
Image Dataset (Real & Fake)
↓
Train–Validation–Test Split (80–10–10)
↓
Image Preprocessing
(Resize → ToTensor → Normalize)
↓
Custom Dataset & DataLoader Creation
↓
Pretrained ResNet50 Model
(Modified Final Layer for Binary Classification)
↓
Training Process
Forward Pass → Loss Calculation → Backpropagation → Weight Update
↓
Validation & Accuracy Calculation
↓
Model Saving
```

---

# 🎥 Video Deepfake Detection

## Dataset Used

FaceForensics++ Dataset  
DeepFakes Manipulation Subset Only

Includes:
- Real Videos
- Fake Videos
- Manipulation Masks

---

## Video Detection Pipeline

```text
Video
→ Frame Extraction
→ Face Cropping
→ Segmentation
→ EfficientNet Feature Extraction
→ Sequence Building
→ BiLSTM Classification
```

---

## Video Processing Workflow

### 1. Frame Extraction
- Extract frames from videos
- Extract masks for fake videos

### 2. Face Detection & Cropping
- MTCNN face detection
- Resize to 224×224

### 3. Segmentation
- U-Net with ResNet34 encoder
- Learns manipulation regions

### 4. Feature Extraction
- EfficientNet-B4 pretrained model
- Extracts spatial features

### 5. Temporal Modeling
- Bidirectional LSTM
- Learns motion inconsistencies

---

# 🎙️ Audio Deepfake Detection

## Dataset Used

ASVspoof 2019 Logical Access (LA)

Balanced Subset:
- 800 Bonafide Samples
- 800 Spoof Samples

---

## Audio Detection Pipeline

```text
Audio
→ Resample (16kHz)
→ Pad / Truncate
→ LFCC Extraction
→ Normalization
→ CNN Feature Learning
→ BiLSTM Temporal Modeling
→ Bonafide / Spoof Prediction
```

---

## Audio Model Architecture

### CNN Layers
- Conv1D
- Batch Normalization
- ReLU
- MaxPooling

### BiLSTM
- Bidirectional LSTM
- Hidden Size: 64

### Final Classification
- Fully Connected Layer
- 2-Class Output

---

# 🔒 Security Notes

The following files are excluded from GitHub using `.gitignore`:

```bash
venv/
node_modules/
serviceAccountKey.json
__pycache__/
.env
*.pth
Dataset/
```


# 👨‍💻 Authors

Developed by:

- Merlyn Mary Stephen
- Rinny Anna Thomas
- Shalin Ann Thomas
- Sneha Mariam Samuel

This project was developed as a Final Year B.Tech Project.

---

# 📄 License

This project is developed for educational and research purposes.
