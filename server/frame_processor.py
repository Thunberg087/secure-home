import threading
import motion_detector as md
import cv2


class FrameProcessor:
    
    def __init__(self, stream_url: str) -> None:
        self.md = md.MotionDetector(stream_url)
        
    
        
        
    