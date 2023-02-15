import threading
import motion_detector as md
import cv2


class FrameProcessor:
    
    def __init__(self, cap: cv2.VideoCapture) -> None:
        self.md = md.MotionDetector(cap)
        
    
        
        
    