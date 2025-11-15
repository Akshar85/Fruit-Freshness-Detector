import cv2
import os
from datetime import datetime

def capture_image():
    """Capture image from webcam"""
    try:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        
        cam = cv2.VideoCapture(0)
        
        if not cam.isOpened():
            raise Exception("Camera not available")
        
        ret, frame = cam.read()
        cam.release()
        
        if not ret:
            raise Exception("Failed to capture frame")
        
        filename = f"uploads/captured_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, frame)
        
        return filename
    
    except Exception as e:
        raise Exception(f"Camera capture failed: {str(e)}")
