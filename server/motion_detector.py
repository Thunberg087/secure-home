import cv2
import numpy as np
import threading
import utils

class MotionDetector():
    
    
    enabled = False
    motion_detected = False
    motion_timer: utils.ResettableTimer
    
    def __init__(self, stream_url: str) -> None:
        self.cap = cv2.VideoCapture(stream_url)
        self.motion_timer = utils.ResettableTimer(5.0, self.undetect_motion)


    def start(self):
        self.enabled = True

        t = threading.Thread(target=self.detect_motion, daemon=True)
        self.thread = t
        
        t.start()

    def stop(self):
        self.enabled = False

    def undetect_motion(self):
        print("No motion detected for the last 5 sec")
        self.motion_detected = False

    def detect_motion(self):
        frame_count = 0

        previous_frame = None


        # Loop through frames from the stream
        while self.enabled:
            
            if not self.cap:
                continue
            # Read a frame
            ret, frame = self.cap.read()


            # Check if the frame was successfully read
            if not ret:
                print("Error: failed to read frame")
                break

            # Update the frame count
            frame_count += 1

            # Calculate the current FPS every 10 frames
            if frame_count % 5 == 0:
                img_rgb = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2RGB)
                prepared_frame = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)
                
                if (previous_frame is None):
                    # First frame; there is no previous one yet
                    previous_frame = prepared_frame
                    continue
                
                diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
                previous_frame = prepared_frame
            
                # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
                kernel = np.ones((5, 5))
                diff_frame = cv2.dilate(diff_frame, kernel)

                # 5. Only take different areas that are different enough (>20 / 255)
                thresh_frame = cv2.threshold(src=diff_frame, thresh=100, maxval=255, type=cv2.THRESH_BINARY)[1]
                
                # Calculate the mean pixel value of the thresholded difference frame
                mean_val = np.mean(thresh_frame)
            
                # Set the motion threshold
                motion_threshold = 0.1

                # Check if the mean pixel value is above the motion threshold
                if mean_val > motion_threshold:
                    print("Motion detected")
                    self.motion_detected = True

                    self.motion_timer.restart ()

