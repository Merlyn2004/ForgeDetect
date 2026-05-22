The dataset used is https://www.kaggle.com/datasets/manjilkarki/deepfake-and-real-images
which is a subset of "OpenForensics" Dataset.


Test Accuracy: 90.04%

Classification Report:
              precision    recall  f1-score   support

        Fake       0.85      0.98      0.91      5492
        Real       0.98      0.82      0.89      5413

    accuracy                           0.90     10905
   macro avg       0.91      0.90      0.90     10905
weighted avg       0.91      0.90      0.90     10905


Confusion Matrix:
[[5380  112]
 [ 974 4439]]

 Validation Accuracy: 98.48%

Classification Report:
              precision    recall  f1-score   support

        Fake       0.99      0.98      0.98     19641
        Real       0.98      0.99      0.98     19787

    accuracy                           0.98     39428
   macro avg       0.98      0.98      0.98     39428
weighted avg       0.98      0.98      0.98     39428


Confusion Matrix:
[[19291   350]
 [  248 19539]]


FLOWCHART


 Image Dataset (Real & Fake)
⬇
Train–Validation–Test Split (80–10–10)
⬇
Image Preprocessing
(Resize → ToTensor → Normalize)
⬇
Custom Dataset & DataLoader Creation
⬇
Pretrained ResNet50 Model
(Modified Final Layer for Binary Classification)
⬇
Training Process
Forward Pass → Loss Calculation → Backpropagation → Weight Update
⬇
Validation & Accuracy Calculation
⬇
Model Saving (Checkpoint after each epoch)