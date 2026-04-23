import torch
import torch.nn as nn
from torchvision import models, transforms
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

# --- NIH CHEST PATHOLOGY CLASSES ---
CHEST_CLASSES = [
    'Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltration', 'Mass', 'Nodule', 
    'Pneumonia', 'Pneumothorax', 'Consolidation', 'Edema', 'Emphysema', 
    'Fibrosis', 'Pleural_Thickening', 'Hernia'
]

class DL_Suite:
    def __init__(self):
        # 1. Load Fracture Model (YOLOv11)
        # Your fr1.pt is a DetectionModel
        self.fracture_model = YOLO("models/fr1.pt")
        
        # 2. Setup Chest Model Architecture (ConvNeXt Tiny)
        # Based on your .pkl file metadata, this matches the required layers
        self.chest_model = models.convnext_tiny(weights=None)
        num_ftrs = self.chest_model.classifier[2].in_features
        self.chest_model.classifier[2] = nn.Sequential(
            nn.Linear(num_ftrs, len(CHEST_CLASSES)),
            nn.Sigmoid()
        )
        
        # 3. Load Chest Weights with Security Bypass
        try:
            state_dict = torch.load(
                "models/best_model_chest.pkl", 
                map_location=torch.device('cpu'), 
                weights_only=False
            )
            self.chest_model.load_state_dict(state_dict)
            self.chest_model.eval()
        except Exception as e:
            print(f"Error loading Chest Model: {e}")

        # 4. Define Image Preprocessing for Chest X-rays
        self.chest_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def detect_fracture(self, image, conf):
        """Processes images using the YOLO fracture model."""
        results = self.fracture_model.predict(source=image, conf=conf, save=False)
        res = results[0]
        
        # Plotting returns a BGR numpy array
        annotated_img = res.plot()
        
        findings = []
        for box in res.boxes:
            findings.append({
                "Condition": res.names[int(box.cls[0])],
                "Confidence": f"{float(box.conf[0]):.2f}"
            })
            
        return annotated_img, findings

    def analyze_chest(self, image, conf):
        """Processes images using the ConvNeXt chest model."""
        # Convert PIL to RGB
        img_rgb = image.convert('RGB')
        img_t = self.chest_transform(img_rgb).unsqueeze(0)
        
        with torch.no_grad():
            outputs = self.chest_model(img_t)
        
        # NIH Dataset is multi-label, so we check every class against threshold
        probs = outputs[0].cpu().numpy()
        findings = []
        
        for i, prob in enumerate(probs):
            if prob > conf:
                findings.append({
                    "Condition": CHEST_CLASSES[i],
                    "Confidence": f"{prob:.2f}"
                })
        
        # Since this is classification, we return the original image
        # (YOLO's .plot() is not applicable here)
        return np.array(img_rgb), findings

# Standardizing for the streamlit page
def run_dl_scan(mode, image, threshold):
    suite = DL_Suite()
    if mode == "Fracture Detection":
        return suite.detect_fracture(image, threshold)
    else:
        return suite.analyze_chest(image, threshold)