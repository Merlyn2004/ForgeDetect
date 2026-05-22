# 🎥 Video Deepfake Detection (FaceForensics++ – DeepFakes Only)

This project detects deepfake videos using only the DeepFakes subset of the FaceForensics++ dataset.  
The system combines spatial feature learning and temporal modeling to classify videos as Real or Fake.

--------------------------------------------
📂 Dataset Used
--------------------------------------------
- FaceForensics++
- Manipulation type: DeepFakes only
- Real videos (original sequences)
- Fake videos (DeepFakes)
- Corresponding manipulation masks

--------------------------------------------
⚙️ Pipeline Overview
--------------------------------------------
1. Frame Extraction
   - Extract frames from real and fake videos
   - Extract masks for fake videos

2. Face Detection & Cropping
   - Detect largest face using MTCNN
   - Crop and resize to 224x224
   - Crop masks using the same bounding box

3. Segmentation Model
   - U-Net with ResNet34 encoder
   - Learns pixel-level manipulation regions
   - Uses BCE + Dice loss

4. Feature Extraction
   - EfficientNet-B4 pretrained model
   - Extracts deep spatial features per frame
   - Saves feature vectors (.npy)

5. Sequence Creation
   - Sliding window of 16 frames
   - Converts frame features into temporal sequences

6. Temporal Modeling
   - 2-layer Bidirectional LSTM
   - Learns motion inconsistencies
   - Outputs final Real / Fake prediction

--------------------------------------------
🧠 Final Flow
--------------------------------------------
Video
→ Frame Extraction
→ Face Cropping
→ Segmentation
→ EfficientNet Feature Extraction
→ Sequence Building
→ BiLSTM Classification

--------------------------------------------
✅ Key Highlights
--------------------------------------------
- Uses DeepFakes subset of FaceForensics++
- Combines spatial and temporal learning
- Video-level train/val/test split
- Checkpoint-based training
- Modular and scalable architecture