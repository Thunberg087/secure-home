import cv2
import frame_processor as fp
import uuid
from threading import Thread
import random




class Camera:  
    
    def __init__(self, name: str, stream_url: str) -> None:
        self.name = name
        self.stream_url = stream_url
        
        self.id = str(uuid.uuid4())
        
        self.online = False
        self.capture: cv2.VideoCapture = None
        
        self.frame_processer = fp.FrameProcessor(self.capture)

        self.enable_motion_detection()
        
        print('Started camera: {}'.format(self.stream_url))
        self.load_network_stream()


    def load_network_stream(self):
        """Verifies stream link and open new stream if valid"""

        def load_network_stream_thread():
            if self.verify_network_stream(self.stream_url):
                self.capture = cv2.VideoCapture(self.stream_url)
                self.online = True

        self.load_stream_thread = Thread(target=load_network_stream_thread, args=())
        self.load_stream_thread.daemon = True
        self.load_stream_thread.start()
        
        
        
    def verify_network_stream(self, link):
        """Attempts to receive a frame from given link"""
        
        cap = cv2.VideoCapture(link)
        if not cap.isOpened():
            return False
        cap.release()
        return True
    
    
    def is_connected(self):
        return self.verify_network_stream(self.stream_url)
    
    
    def enable_motion_detection(self):
        self.frame_processer.md.start()
        
        
    def get_frame(self):

        while True:
            if self.capture is None:
                continue
            num = random.random()
            print(num)
            _, img = self.capture.read()
            
            
            imgencode = cv2.imencode('.jpg', img)[1]
            stringData = imgencode.tostring()
            
            yield (b'--frame\r\n'
                b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
