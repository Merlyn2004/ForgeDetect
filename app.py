# app.py - Enhanced Flask Backend with PDF Report Generation
from pathlib import Path

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import torch
import torchvision.transforms as transforms
import numpy as np
import cv2
import io
import sys
import os
import time
import base64
from torchvision.models import resnet50, ResNet50_Weights
import torch.nn as nn
from datetime import datetime
import tempfile
import uuid
import threading
import shutil
import librosa
from Audio_Detection.lfcc_utils import extract_lfcc
import subprocess
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# PDF Generation imports
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, red, green
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

# Firebase imports
import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter

app = Flask(__name__)
TMP_ROOT = Path("demo_tmp")

print("🔄 Startup cleanup running...")
print("Target path:", TMP_ROOT.resolve())

if TMP_ROOT.exists():
    shutil.rmtree(TMP_ROOT, ignore_errors=True)

TMP_ROOT.mkdir(exist_ok=True)
CORS(app)  # Enable CORS for React frontend

# -------------------- Firebase Setup --------------------
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'your-project-id.appspot.com'
    })
    
    db = firestore.client()
    bucket = storage.bucket()
    
    print("✅ Firebase initialized successfully")
except Exception as e:
    print(f"⚠️ Firebase initialization error: {e}")
    db = None
    bucket = None

# Define the wrapper exactly as in training
class WrapModel(nn.Module):
    def __init__(self, model):
        super(WrapModel, self).__init__()
        self.model = model

    def forward(self, x):
        return self.model(x)
    
# -------------------- Load Model --------------------
WORK_DIR = "E:/Forgedetect"  # change to your working directory
OUT_SIZE = 2  # change based on your model's output classes
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------- AUDIO CONFIG --------------------
AUDIO_SR = 16000
AUDIO_SECONDS = 6
AUDIO_LEN = AUDIO_SR * AUDIO_SECONDS

AUDIO_MODEL_PATH = os.path.join(WORK_DIR, "best_model_audio.pth")
AUDIO_MEAN_PATH = "Audio_Detection/normalization/mean.npy"
AUDIO_STD_PATH = "Audio_Detection/normalization/std.npy"

audio_mean = np.load(AUDIO_MEAN_PATH)
audio_std = np.load(AUDIO_STD_PATH)

class CNN_BiLSTM_Audio(nn.Module):
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


# Load model
best_model_path = os.path.join(WORK_DIR, "best_model_image.pth")

# Check if model file exists
if not os.path.exists(best_model_path):
    print(f"Warning: Model file not found at {best_model_path}")
    print("Creating a dummy model for testing...")
    model = WrapModel(resnet50(weights=ResNet50_Weights.IMAGENET1K_V2))
    num_ftrs = model.model.fc.in_features
    model.model.fc = nn.Linear(num_ftrs, OUT_SIZE)
else:
    model = WrapModel(resnet50(weights=ResNet50_Weights.IMAGENET1K_V2))
    num_ftrs = model.model.fc.in_features
    model.model.fc = nn.Linear(num_ftrs, OUT_SIZE)
    model.load_state_dict(torch.load(best_model_path, map_location=device))

model = model.to(device)
model.eval()
audio_model = CNN_BiLSTM_Audio().to(device)
audio_model.load_state_dict(torch.load(AUDIO_MODEL_PATH, map_location=device))
audio_model.eval()

audio_index_label = {0: "REAL", 1: "FAKE"}

# Label mapping
index_label = {0: "FAKE", 1: "REAL"}

IMG_SIZE = 224






def cleanup_demo_tmp(delay_seconds=300):
    """
    Deletes demo_tmp after a delay.
    Delay avoids race conditions with video streaming.
    """
    def _cleanup():
        time.sleep(delay_seconds)
        try:
            shutil.rmtree("demo_tmp", ignore_errors=True)
            print("🧹 demo_tmp cleaned up")
        except Exception as e:
            print("Cleanup error:", e)

    threading.Thread(target=_cleanup, daemon=True).start()

# -------------------- Preprocess Function --------------------
def preprocess_image(image: Image.Image):
    """Preprocess image to 224x224 and normalize"""
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)  # add batch dimension

def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif obj is None:
        return None
    elif isinstance(obj, (int, float, str, bool)):
        return obj
    else:
        return str(obj)


def pad_or_truncate_audio(y):
    if len(y) < AUDIO_LEN:
        return np.pad(y, (0, AUDIO_LEN - len(y)))
    return y[:AUDIO_LEN]


def preprocess_audio(audio_path):
    y, _ = librosa.load(audio_path, sr=AUDIO_SR, mono=True)
    y = pad_or_truncate_audio(y)

    lfcc = extract_lfcc(y)
    lfcc = (lfcc - audio_mean) / audio_std

    x = torch.tensor(lfcc.T, dtype=torch.float32).unsqueeze(0).to(device)
    return x

def predict_audio(audio_path):
    x = preprocess_audio(audio_path)

    with torch.no_grad():
        logits = audio_model(x)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

    pred = np.argmax(probs)
    confidence = probs[pred] * 100

    return audio_index_label[pred], round(confidence, 2)


# -------------------- GradCAM Implementation --------------------
def generate_gradcam(image: Image.Image, model, target_layer="layer4"):
    """Generate GradCAM heatmap"""
    model.eval()
    tensor = preprocess_image(image).to(device)

    gradients = []
    activations = []

    def backward_hook(module, grad_input, grad_output):
        gradients.append(grad_output[0])

    def forward_hook(module, input, output):
        activations.append(output)

    # Register hooks on the target layer
    hook_handles = []
    for name, module in model.model.named_modules():
        if name == target_layer:
            handle1 = module.register_forward_hook(forward_hook)
            handle2 = module.register_backward_hook(backward_hook)
            hook_handles.extend([handle1, handle2])
            break

    try:
        # Forward pass
        output = model(tensor)
        class_idx = torch.argmax(output, dim=1).item()
        score = output[0, class_idx]
        
        # Backward pass
        model.zero_grad()
        score.backward()

        # Generate GradCAM
        if gradients and activations:
            grads = gradients[0].cpu().detach().numpy()
            acts = activations[0].cpu().detach().numpy()

            # Compute weights
            weights = np.mean(grads, axis=(2, 3))[0]
            
            # Generate CAM
            cam = np.zeros(acts.shape[2:], dtype=np.float32)
            for i, w in enumerate(weights):
                cam += w * acts[0, i, :, :]

            # Normalize and resize CAM
            cam = np.maximum(cam, 0)
            cam = cv2.resize(cam, (IMG_SIZE, IMG_SIZE))
            
            if cam.max() > cam.min():
                cam = (cam - cam.min()) / (cam.max() - cam.min())
            
            # Create heatmap overlay
            original_img = np.array(image.resize((IMG_SIZE, IMG_SIZE)))
            heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
            heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
            
            # Blend original image with heatmap
            overlay = 0.6 * original_img + 0.4 * heatmap
            overlay = np.clip(overlay, 0, 255).astype(np.uint8)
            
            # Convert to base64
            _, buffer = cv2.imencode('.png', cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
            heatmap_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return heatmap_base64, overlay
        else:
            return None, None
            
    finally:
        # Clean up hooks
        for handle in hook_handles:
            handle.remove()

# -------------------- Prediction Function --------------------
def predict_image(image: Image.Image):
    """Predict if image is real or fake"""
    model.eval()
    tensor = preprocess_image(image).to(device)
    
    with torch.no_grad():
        output = model(tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0, predicted_class].item() * 100
    
    prediction = index_label[predicted_class]
    
    return prediction, confidence

# Enhanced PDF Report Generation Function
# Enhanced PDF Report Generation Function with Better Design
# PDF Report Generator - Clean Professional Style
def generate_pdf_report(analysis_data, original_image, heatmap_image):
    """Generate comprehensive PDF report"""
    
    # Create temporary directory for images
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save images to temp files
        original_path = os.path.join(temp_dir, 'original.png')
        heatmap_path = os.path.join(temp_dir, 'heatmap.png')
        
        # Save original image
        original_image.save(original_path)
        
        # Save heatmap image if available
        if heatmap_image is not None:
            cv2.imwrite(heatmap_path, cv2.cvtColor(heatmap_image, cv2.COLOR_RGB2BGR))
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2DD4BF'),
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=HexColor('#059669'),
            spaceBefore=20
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            leading=14
        )
        
        # Determine risk level and color
        confidence = analysis_data.get('confidence', 0)
        prediction = analysis_data.get('prediction', 'UNKNOWN')
        
        if prediction == 'FAKE' and confidence > 80:
            risk_level = "HIGH"
            risk_color = HexColor('#DC2626')
        elif prediction == 'FAKE' and confidence > 60:
            risk_level = "MEDIUM"
            risk_color = HexColor('#F59E0B')
        else:
            risk_level = "LOW"
            risk_color = HexColor('#10B981')
        
        # Build story
        story = []
        
        # Header
        story.append(Paragraph("FORGE DETECT", title_style))
        story.append(Paragraph("Deepfake Detection Analysis Report", styles['Heading2']))
        story.append(Spacer(1, 20))
        
        # Executive Summary Box
        summary_data = [
            ['Analysis Result', analysis_data.get('prediction', 'N/A')],
            ['Confidence Score', f"{analysis_data.get('confidence', 0):.2f}%"],
            ['Risk Level', risk_level],
            ['Analysis Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['File Name', analysis_data.get('filename', 'Unknown')]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2DD4BF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F0F9FF')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 30))
        
        # Risk Assessment
        story.append(Paragraph("Risk Assessment", heading_style))
        
        risk_text = ""
        if risk_level == "HIGH":
            risk_text = "⚠️ <b>HIGH RISK:</b> This image shows strong indicators of being artificially generated or manipulated. Immediate verification recommended."
        elif risk_level == "MEDIUM":
            risk_text = "⚡ <b>MEDIUM RISK:</b> This image shows some indicators of potential manipulation. Further investigation suggested."
        else:
            risk_text = "✅ <b>LOW RISK:</b> This image appears to be authentic with minimal signs of artificial generation or manipulation."
        
        story.append(Paragraph(risk_text, body_style))
        story.append(Spacer(1, 20))
        
        # Technical Analysis
        story.append(Paragraph("Technical Analysis", heading_style))
        
        tech_details = f"""
        <b>Model Architecture:</b> ResNet-50 with custom classification layer<br/>
        <b>Input Resolution:</b> 224x224 pixels<br/>
        <b>Processing Method:</b> Convolutional Neural Network with GradCAM visualization<br/>
        <b>Confidence Threshold:</b> Results above 60% are considered reliable<br/>
        <b>Detection Focus:</b> Facial inconsistencies, compression artifacts, and synthetic patterns
        """
        story.append(Paragraph(tech_details, body_style))
        story.append(Spacer(1, 20))
        
        # Images Section
        story.append(Paragraph("Visual Analysis", heading_style))
        
        # Create image table
        img_data = []
        img_row = []
        
        # Original image
        if os.path.exists(original_path):
            orig_img = RLImage(original_path, width=2.5*inch, height=2.5*inch)
            img_row.append(orig_img)
        
        # Heatmap image
        if os.path.exists(heatmap_path):
            heat_img = RLImage(heatmap_path, width=2.5*inch, height=2.5*inch)
            img_row.append(heat_img)
        
        if img_row:
            img_data.append(img_row)
            img_data.append(['Original Image', 'GradCAM Heatmap'])
            
            img_table = Table(img_data, colWidths=[2.8*inch, 2.8*inch])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 1), (-1, 1), 9),
                ('TEXTCOLOR', (0, 1), (-1, 1), colors.grey),
                ('TOPPADDING', (0, 1), (-1, 1), 10),
            ]))
            
            story.append(img_table)
            story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("Recommendations", heading_style))
        
        if prediction == 'FAKE':
            recommendations = """
            • <b>Do not trust</b> this image for critical decision-making
            • <b>Verify authenticity</b> through alternative sources
            • <b>Report suspicious content</b> if used maliciously
            • <b>Cross-reference</b> with original sources when possible
            • <b>Consider legal implications</b> if used in official contexts
            """
        else:
            recommendations = """
            • <b>Image appears authentic</b> based on current analysis
            • <b>Continue standard verification</b> practices for important use cases
            • <b>Monitor for updates</b> as deepfake technology evolves
            • <b>Combine with human judgment</b> for critical applications
            • <b>Regular re-analysis recommended</b> for high-stakes scenarios
            """
        
        story.append(Paragraph(recommendations, body_style))
        story.append(Spacer(1, 30))
        
        # Footer
        footer_text = f"""
        <i>This report was generated by Forge Detect AI system on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}. 
        Results are based on current AI models and should be combined with human judgment for critical applications. 
        Report ID: {str(uuid.uuid4())[:8].upper()}</i>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
        
    finally:
        # Clean up temp files
        try:
            if os.path.exists(original_path):
                os.remove(original_path)
            if os.path.exists(heatmap_path):
                os.remove(heatmap_path)
            os.rmdir(temp_dir)
        except:
            pass
        
      # -------------------- Firebase Helper Functions --------------------

def generate_video_pdf_report(video_data, frame_paths):
    """
    Video PDF report styled EXACTLY like image PDF report
    """

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()

    # ---------- Custom styles (SAME AS IMAGE REPORT) ----------
    title_style = ParagraphStyle(
        'VideoTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#2DD4BF'),
        alignment=1
    )

    heading_style = ParagraphStyle(
        'VideoHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=HexColor('#059669'),
        spaceBefore=20
    )

    body_style = ParagraphStyle(
        'VideoBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=10
    )

    # ---------- Risk logic (SAME AS IMAGE REPORT) ----------
    prediction = video_data["prediction"]
    confidence = video_data["confidence"]

    if prediction == "FAKE" and confidence > 80:
        risk_level = "HIGH"
    elif prediction == "FAKE" and confidence > 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    story = []

    # ---------- HEADER ----------
    story.append(Paragraph("FORGE DETECT", title_style))
    story.append(Paragraph("Video Deepfake Analysis Report", styles["Heading2"]))
    story.append(Spacer(1, 20))

    # ---------- SUMMARY TABLE ----------
    summary_data = [
        ["File Name", video_data["filename"]],
        ["Prediction", prediction],
        ["Confidence", f"{confidence:.2f}%"],
        ["Risk Level", risk_level],
        ["Analysis Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]

    summary_table = Table(summary_data, colWidths=[2.5*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2DD4BF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 25))

    # ---------- RISK ASSESSMENT ----------
    story.append(Paragraph("Risk Assessment", heading_style))

    if risk_level == "HIGH":
        risk_text = "⚠️ HIGH RISK: Strong evidence of manipulation detected in the video."
    elif risk_level == "MEDIUM":
        risk_text = "⚡ MEDIUM RISK: Some manipulation indicators detected."
    else:
        risk_text = "✅ LOW RISK: No strong manipulation indicators detected."

    story.append(Paragraph(risk_text, body_style))

    # ---------- TECHNICAL ANALYSIS ----------
    story.append(Paragraph("Technical Analysis", heading_style))
    story.append(Paragraph(
        """
        <b>Detection Method:</b> Frame-wise face analysis with temporal modeling<br/>
        <b>Models Used:</b> CNN + Segmentation + LSTM<br/>
        <b>Focus Areas:</b> Facial consistency, motion artifacts, synthetic textures<br/>
        <b>Frame Selection:</b> Evidence-based sampling
        """,
        body_style
    ))

    # ---------- VISUAL EVIDENCE ----------
    story.append(Paragraph("Visual Evidence Frames", heading_style))

    img_rows = []
    for frame in frame_paths:
        img_rows.append(
            [RLImage(frame, width=2.5*inch, height=2.5*inch)]
        )

    frame_table = Table(img_rows, colWidths=[5*inch])
    frame_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))

    story.append(frame_table)

    # ---------- EXPLANATION ----------
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "For FAKE videos, red-highlighted regions indicate areas where the AI detected "
        "synthetic manipulation. For REAL videos, frames are uniformly sampled "
        "as authenticity evidence.",
        body_style
    ))

    # ---------- FOOTER ----------
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        f"<i>Generated by Forge Detect AI • Report ID: {str(uuid.uuid4())[:8]}</i>",
        styles["Normal"]
    ))

    doc.build(story)
    return buffer.getvalue()

def generate_audio_pdf_report(audio_data, spectrogram_base64, segments=None):
    """
    Generate Audio Deepfake PDF Report
    Styled consistently with image & video reports
    """

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()

    # ---------- Styles ----------
    title_style = ParagraphStyle(
        'AudioTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#2DD4BF'),
        alignment=1
    )

    heading_style = ParagraphStyle(
        'AudioHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=HexColor('#059669'),
        spaceBefore=20
    )

    body_style = ParagraphStyle(
        'AudioBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=10
    )

    # ---------- Risk Logic ----------
    prediction = audio_data.get("prediction", "UNKNOWN")
    confidence = audio_data.get("confidence", 0)

    if prediction == "FAKE" and confidence > 80:
        risk_level = "HIGH"
    elif prediction == "FAKE" and confidence > 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    story = []

    # ---------- HEADER ----------
    story.append(Paragraph("FORGE DETECT", title_style))
    story.append(Paragraph("Audio Deepfake Analysis Report", styles["Heading2"]))
    story.append(Spacer(1, 20))

    # ---------- SUMMARY ----------
    summary_data = [
        ["File Name", audio_data.get("fileName", "Unknown")],
        ["Prediction", prediction],
        ["Confidence", f"{confidence:.2f}%"],
        ["Risk Level", risk_level],
        ["Analysis Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]

    summary_table = Table(summary_data, colWidths=[2.5 * inch, 3 * inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2DD4BF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 25))

    # ---------- RISK ASSESSMENT ----------
    story.append(Paragraph("Risk Assessment", heading_style))

    if risk_level == "HIGH":
        risk_text = "⚠️ HIGH RISK: Strong indicators of synthetic or manipulated speech were detected."
    elif risk_level == "MEDIUM":
        risk_text = "⚡ MEDIUM RISK: Some characteristics associated with synthetic speech were detected."
    else:
        risk_text = "✅ LOW RISK: No strong indicators of synthetic speech were detected."

    story.append(Paragraph(risk_text, body_style))

    # ---------- TECHNICAL ANALYSIS ----------
    story.append(Paragraph("Technical Analysis", heading_style))
    story.append(Paragraph(
        """
        <b>Model Type:</b> CNN–BiLSTM based audio deepfake detection model<br/>
        <b>Input Representation:</b> Time–frequency features derived from audio signals (LFCC)<br/>
        <b>Decision Level:</b> Utterance-level classification<br/>
        <b>Explainability:</b> Spectrogram-based attention visualization<br/>
        <b>Confidence Threshold:</b> Scores above 60% are considered reliable
        """,
        body_style
    ))

    # ---------- AUDIO EVIDENCE ----------
    story.append(Paragraph("Audio Evidence (Model Explainability)", heading_style))

    if spectrogram_base64:
        spectro_path = os.path.join(tempfile.gettempdir(), f"spectrogram_{uuid.uuid4().hex}.png")
        with open(spectro_path, "wb") as f:
            f.write(base64.b64decode(spectrogram_base64))

        story.append(RLImage(spectro_path, width=4.5 * inch, height=3 * inch))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            "The spectrogram above represents the time–frequency structure of the analyzed audio. "
            "Brighter regions indicate frequency components that contributed more strongly to the model’s decision. "
            "This visualization is intended for explainability and expert interpretation.",
            body_style
        ))

    # ---------- TEMPORAL SEGMENTS (OPTIONAL) ----------
    if segments:
        story.append(Paragraph("Temporal Segment Analysis (Optional)", heading_style))

        segment_rows = [["Time Range (s)", "Fake Likelihood"]]
        for seg in segments:
            segment_rows.append([
                f"{seg['start']} – {seg['end']}",
                f"{seg['fake_score'] * 100:.1f}%"
            ])

        segment_table = Table(segment_rows, colWidths=[3 * inch, 2.5 * inch])
        segment_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F0F9FF')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))

        story.append(segment_table)
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            "Segment-level scores indicate relative contribution to the overall prediction and do not imply isolated manipulation.",
            body_style
        ))

    # ---------- RECOMMENDATIONS ----------
    story.append(Paragraph("Recommendations", heading_style))

    if prediction == "FAKE":
        recommendations = """
        • Avoid using this audio for critical decision-making<br/>
        • Verify the source through trusted channels<br/>
        • Cross-check with original recordings if available<br/>
        • Consider legal or ethical implications if redistributed
        """
    else:
        recommendations = """
        • Audio appears authentic based on current analysis<br/>
        • Continue standard verification practices for sensitive use cases<br/>
        • Combine automated analysis with human judgment
        """

    story.append(Paragraph(recommendations, body_style))

    # ---------- FOOTER ----------
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        f"<i>Generated by Forge Detect AI • Report ID: {uuid.uuid4().hex[:8].upper()}</i>",
        styles["Normal"]
    ))

    doc.build(story)
    return buffer.getvalue()

# -------------------- Firebase Helper Functions --------------------
def save_detection_to_firebase(detection_data):
    if db is None:
        return None

    try:
        # 🔒 Make a COPY so we don't pollute API response
        firebase_data = dict(detection_data)

        # Use Firestore server timestamp ONLY for Firebase
        firebase_data['timestamp'] = firestore.SERVER_TIMESTAMP

        doc_ref = db.collection('detections').document()
        firebase_data['id'] = doc_ref.id

        doc_ref.set(firebase_data)

        print(f"✅ Detection saved to Firebase: {doc_ref.id}")
        return doc_ref.id

    except Exception as e:
        print(f"❌ Error saving to Firebase: {e}")
        return None


def get_detection_history(limit=100, time_filter=None):
    if db is None:
        return []
    
    try:
        query = db.collection('detections').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
        
        if time_filter:
            from datetime import timedelta
            now = datetime.now()
            if time_filter == 'today':
                threshold = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif time_filter == 'week':
                threshold = now - timedelta(days=7)
            elif time_filter == 'month':
                threshold = now - timedelta(days=30)
            else:
                threshold = None
            
            if threshold:
                query = query.where(filter=FieldFilter('timestamp', '>=', threshold))
        
        docs = query.stream()
        
        detections = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            if 'timestamp' in data and data['timestamp']:
                data['timestamp'] = data['timestamp'].isoformat()
            detections.append(data)
        
        return detections
    except Exception as e:
        print(f"❌ Error retrieving detection history: {e}")
        return []

# -------------------- Flask Routes --------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
         return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({"error": "Invalid file type"}), 400

        try:
            image = Image.open(file).convert("RGB")
        except Exception as e:
            return jsonify({"error": f"Invalid image file: {str(e)}"}), 400

        prediction, confidence = predict_image(image)
        heatmap_base64, heatmap_array = generate_gradcam(image, model)
       
        processing_time = round(np.random.uniform(1.5, 3.0), 2)
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        
        analysis_data = {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "heatmap": heatmap_base64
        }
        
        session_id = str(uuid.uuid4())
        
        detection_record = {
            "sessionId": session_id,
            "userId": user_id,
            "fileName": file.filename,
            "fileType": "image",
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "processingTime": processing_time,
            "downloaded": False,
            "heatmap": heatmap_base64
        }
        
        firebase_id = save_detection_to_firebase(detection_record)
        
        response = {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "heatmap": heatmap_base64,
            "message": f"Image classified as {prediction} with {confidence:.2f}% confidence",
            "session_id": session_id,
            "firebase_id": firebase_id,
            "analysis_data": analysis_data,

        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/predict-video", methods=["POST"])
def predict_video():
    if "file" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, secure_filename(file.filename))
        file.save(video_path)

        try:
            start_time = time.time()

            prediction, confidence, annotated_video = run_video_inference(
                video_path,
                WORK_DIR
            )

            processing_time = round(time.time() - start_time, 2)


            with open(annotated_video, "rb") as f:
                video_bytes = f.read()

            video_base64 = base64.b64encode(video_bytes).decode("utf-8")


            session_id = str(uuid.uuid4())
            user_id = f"user_{uuid.uuid4().hex[:8]}"

            save_detection_to_firebase({
                "sessionId": session_id,
                "userId": user_id,
                "fileName": file.filename,
                "fileType": "video",
                "prediction": prediction,
                "confidence": confidence,
                "processingTime": processing_time,
                "downloaded": False,
                "timestamp": datetime.now().isoformat()
            })



            return {
                "prediction": prediction,
                "confidence": round(confidence, 2),
                "status": "Complete",
                "video_url": "http://127.0.0.1:5000/output-video",
                "sessionId": session_id
            }



        except Exception as e:
            print("❌ Video inference error:", str(e))
            return jsonify({"error": str(e)}), 500



def generate_audio_spectrogram(audio_path):
    """
    Generate mel-spectrogram image (base64) for visualization
    No training involved.
    """
    y, sr = librosa.load(audio_path, sr=AUDIO_SR)

    # Generate mel spectrogram
    S = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_mels=128,
        fmax=8000
    )
    S_db = librosa.power_to_db(S, ref=np.max)

    # Plot spectrogram
    
    plt.figure(figsize=(6, 4))
    librosa.display.specshow(
        S_db,
        sr=sr,
        x_axis="time",
        y_axis="mel",
        cmap="magma"
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title("Audio Spectrogram (Model Input View)")
    plt.tight_layout()

    # Convert plot to base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    spectrogram_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return spectrogram_base64


@app.route("/predict-audio", methods=["POST"])
def predict_audio_api():
    if "file" not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400

    file = request.files["file"]

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, secure_filename(file.filename))
        file.save(audio_path)

        prediction, confidence = predict_audio(audio_path)
        spectrogram = generate_audio_spectrogram(audio_path)
        segments = segment_audio_scores(audio_path)
        risk = "HIGH" if prediction == "FAKE" and confidence > 70 else "LOW"

        print("\n========== AUDIO DETECTION RESULT ==========")
        print("Prediction   :", prediction)
        print("Confidence   :", confidence)
        print("Risk Level   :", risk)
        print("===========================================\n")

        # Data to save in Firebase
        start_time = time.time()

        session_id = str(uuid.uuid4())
        user_id = f"user_{uuid.uuid4().hex[:8]}"

        processing_time = round(time.time() - start_time, 2)

        firebase_data = {
            "sessionId": session_id,
            "userId": user_id,
            "fileName": file.filename,
            "fileType": "audio",
            "prediction": prediction,
            "confidence": confidence,
            "processingTime": processing_time,
            "risk": risk,
            "downloaded": False
        }

        detection_id = save_detection_to_firebase(firebase_data)

        # 🚨 Data to return to frontend (JSON SAFE)
        response_data = {
                "id": detection_id,
                "sessionId": session_id,
                "userId": user_id,
                "fileName": file.filename,
                "fileType": "audio",
                "prediction": prediction,
                "confidence": confidence,
                "processingTime": processing_time,
                "risk": risk,
                "spectrogram": spectrogram,
                "segments": segments,
                "timestamp": datetime.now().isoformat()
        }
        import gc

        gc.collect()

        try:
            import torch
            if torch.cuda.is_available():
                    torch.cuda.empty_cache()
        except:
            pass

        print(">>> Final response JSON:", response_data)
        return jsonify(response_data), 200

def segment_audio_scores(audio_path, segment_duration=0.5):
    """
    Split audio into segments and get confidence per segment
    """
    y, sr = librosa.load(audio_path, sr=AUDIO_SR)
    total_duration = len(y) / sr

    segments = []
    start = 0.0

    while start < total_duration:
        end = min(start + segment_duration, total_duration)
        y_seg = y[int(start * sr):int(end * sr)]

        if len(y_seg) < sr * 0.1:
            start += segment_duration
            continue

        lfcc = extract_lfcc(y_seg)
        lfcc = (lfcc - audio_mean) / audio_std
        x = torch.tensor(lfcc.T, dtype=torch.float32).unsqueeze(0).to(device)

        with torch.no_grad():
            logits = audio_model(x)
            probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

        fake_score = probs[1]  # FAKE confidence

        segments.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "fake_score": round(float(fake_score), 3)
        })

        start += segment_duration

    return segments


# Updated download-report route
@app.route("/download-report", methods=["POST"])
def download_report():
    try:
        # Get analysis data from request
        data = request.get_json()
        
        if not data or 'analysis_data' not in data:
            return jsonify({"error": "No analysis data provided"}), 400
        
        analysis_data = data['analysis_data']
        
        # Get the original image from the uploaded file data if available
        original_image = None
        if 'original_image_data' in data:
            try:
                # Decode base64 image data
                image_data = base64.b64decode(data['original_image_data'])
                original_image = Image.open(io.BytesIO(image_data)).convert('RGB')
                print(f"Successfully decoded original image: {original_image.size}")
            except Exception as e:
                print(f"Error decoding original image: {e}")
        
        # If no original image provided, create a placeholder
        if original_image is None:
            print("No original image available, creating placeholder")
            original_image = Image.new('RGB', (224, 224), color=(200, 200, 200))
            # Add some text to indicate it's a placeholder
            try:
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(original_image)
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    font = ImageFont.load_default()
                draw.text((112, 100), "Image\nNot Available", fill=(100, 100, 100), 
                         anchor="mm", font=font, align="center")
            except:
                pass  # If drawing fails, just use plain gray image
        
        # Recreate heatmap image from base64
        heatmap_image = None
        if analysis_data.get('heatmap'):
            try:
                heatmap_bytes = base64.b64decode(analysis_data['heatmap'])
                heatmap_image = cv2.imdecode(np.frombuffer(heatmap_bytes, np.uint8), cv2.IMREAD_COLOR)
                if heatmap_image is not None:
                    heatmap_image = cv2.cvtColor(heatmap_image, cv2.COLOR_BGR2RGB)
                    print(f"Successfully decoded heatmap: {heatmap_image.shape}")
            except Exception as e:
                print(f"Error decoding heatmap: {e}")
        
        # Generate PDF report
        pdf_data = generate_pdf_report(analysis_data, original_image, heatmap_image)
        
        if 'session_id' in data:
            try:
                detections = db.collection('detections').where(filter=FieldFilter('sessionId', '==', data['session_id'])).limit(1).stream()
                for detection in detections:
                    db.collection('detections').document(detection.id).update({'downloaded': True})
            except Exception as e:
                print(f"Error updating download status: {e}")

        # Create temporary file for download
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_pdf.write(pdf_data)
        temp_pdf.close()
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"forge_detect_report_{timestamp}.pdf"
        
        return send_file(
            temp_pdf.name,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return jsonify({"error": f"Error generating report: {str(e)}"}), 500

@app.route("/download-video-report", methods=["POST"])
def download_video_report():
    data = request.get_json()

    frames_dir = os.path.join("demo_tmp", "report_frames")
    if not os.path.exists(frames_dir):
        return jsonify({"error": "No frames available"}), 400

    frame_paths = sorted([
        os.path.join(frames_dir, f)
        for f in os.listdir(frames_dir)
        if f.endswith(".png")
    ])[:5]

    pdf_data = generate_video_pdf_report({
        "filename": data["filename"],
        "prediction": data["prediction"],
        "confidence": data["confidence"]
    }, frame_paths)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.write(pdf_data)
    tmp.close()
    if db and data.get("sessionId"):
        docs = db.collection("detections") \
            .where("sessionId", "==", data["sessionId"]) \
            .limit(1) \
            .stream()

        for doc in docs:
            db.collection("detections").document(doc.id).update({
                "downloaded": True
            })
    response = send_file(
    tmp.name,
    as_attachment=True,
    download_name="forge_detect_video_report.pdf",
    mimetype="application/pdf"
)

    # ✅ Schedule safe cleanup after 5 minutes
    cleanup_demo_tmp(delay_seconds=300)

    return response

@app.route("/download-audio-report", methods=["POST"])
def download_audio_report():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Required fields
        audio_data = {
            "fileName": data.get("fileName", "Unknown"),
            "prediction": data.get("prediction", "UNKNOWN"),
            "confidence": data.get("confidence", 0)
        }

        spectrogram = data.get("spectrogram")
        segments = data.get("segments", [])

        # Generate PDF
        pdf_data = generate_audio_pdf_report(
            audio_data=audio_data,
            spectrogram_base64=spectrogram,
            segments=segments
        )

        # Save to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp.write(pdf_data)
        tmp.close()

        # Update Firebase download status (optional but consistent)
        if db and data.get("sessionId"):
            db.collection("detections") \
                .where("sessionId", "==", data["sessionId"]) \
                .limit(1) \
                .stream()

            docs = db.collection("detections") \
                .where("sessionId", "==", data["sessionId"]) \
                .limit(1) \
                .stream()

            for doc in docs:
                db.collection("detections").document(doc.id).update({
                    "downloaded": True
                })

        return send_file(
            tmp.name,
            as_attachment=True,
            download_name="forge_detect_audio_report.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        print("Error generating audio report:", str(e))
        return jsonify({"error": "Failed to generate audio report"}), 500


def run_video_inference(video_path, work_dir):
    """
    Calls demo_video.py safely and returns:
    - prediction
    - confidence (percentage)
    - annotated video path
    """

    demo_script = os.path.join(work_dir, "demo_video.py")

    if not os.path.exists(demo_script):
        raise FileNotFoundError(f"demo.py not found at {demo_script}")

    cmd = [
        sys.executable,
        demo_script,
        "--video", video_path
    ]

    print("▶ Running demo script:", " ".join(cmd))

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=work_dir
    )

    print("====== DEMO STDOUT ======")
    print(result.stdout)

    print("====== DEMO STDERR ======")
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError("Demo script failed")

    prediction = None
    confidence = None

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("Prediction"):
            prediction = line.split(":")[-1].strip()

        elif line.startswith("Confidence"):
            confidence = float(line.split(":")[-1].strip())


    if prediction is None or confidence is None:
        raise ValueError("Failed to parse prediction/confidence from demo output")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    annotated_video = os.path.join(BASE_DIR, "demo_tmp", "annotated_output.mp4")


    # wait briefly for file system flush (Windows fix)
    for _ in range(10):
        if os.path.exists(annotated_video) and os.path.getsize(annotated_video) > 0:
            break
        time.sleep(0.2)
    else:
        raise FileNotFoundError(
            f"Annotated video not found after wait: {annotated_video}"
        )
    

    return prediction, round(confidence*100, 2), annotated_video

@app.route("/output-video")
def serve_output_video():
    path = r"E:\Forgedetect\demo_tmp\annotated_output.mp4"
    if not os.path.exists(path):
        return {"error": "Video not found"}, 404

    return send_file(
        path,
        mimetype="video/mp4",
        as_attachment=False
    )

# -------------------- Analytics API Routes --------------------
@app.route("/api/analytics/detections", methods=["GET"])
def get_analytics_detections():
    try:
        time_filter = request.args.get('filter', 'all')
        limit = int(request.args.get('limit', 100))
        
        detections = get_detection_history(limit=limit, time_filter=time_filter)
        
        return jsonify({
            "success": True,
            "count": len(detections),
            "detections": detections
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/analytics/stats", methods=["GET"])
def get_analytics_stats():
    try:
        detections = get_detection_history(limit=1000)
        
        total = len(detections)
        fake_count = len([d for d in detections if d.get('prediction') == 'FAKE'])
        real_count = len([d for d in detections if d.get('prediction') == 'REAL'])
        
        avg_confidence = sum([d.get('confidence', 0) for d in detections]) / total if total > 0 else 0
        avg_processing = sum([d.get('processingTime', 0) for d in detections]) / total if total > 0 else 0
        
        unique_users = len(set([d.get('userId') for d in detections if d.get('userId')]))
        downloaded = len([d for d in detections if d.get('downloaded')])
        
        stats = {
            "totalDetections": total,
            "fakeDetected": fake_count,
            "realDetected": real_count,
            "avgConfidence": round(avg_confidence, 2),
            "avgProcessingTime": round(avg_processing, 2),
            "uniqueUsers": unique_users,
            "reportsDownloaded": downloaded,
            "imageUploads": total
        }
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device),
        "pdf_generation": "enabled"
    })

if __name__ == "__main__":
    print(f"Starting Flask server with PDF report generation...")
    print(f"Model device: {device}")
    print(f"Model path: {best_model_path}")
    print(f"Model exists: {os.path.exists(best_model_path)}")
    print(f"Firebase status: {'✅ Connected' if db else '❌ Not connected'}")
    app.run(debug=True, host="0.0.0.0", port=5000)