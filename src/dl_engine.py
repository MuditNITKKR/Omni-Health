# File: D:\coding\OMNI HEALTH\src\dl_engine.py
from ultralytics import YOLO
import cv2

class FractureDetector:
    def __init__(self, model_path):
        # Load the YOLO model (e.g., your fr1.pt)
        self.model = YOLO(model_path)

    def predict(self, image, conf=0.25):
        """
        Runs inference and returns the plotted image and detection data.
        """
        results = self.model.predict(source=image, conf=conf, save=False)
        res = results[0]
        
        # Plotting the results on the image (returns BGR array)
        annotated_img = res.plot()
        
        # Extracting box data for the report
        detections = []
        for box in res.boxes:
            detections.append({
                "class": res.names[int(box.cls[0])],
                "conf": float(box.conf[0])
            })
            
        return annotated_img, detections