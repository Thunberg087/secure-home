import cv2
import numpy as np



def detect_motion(cap: cv2.VideoCapture):
    frame_count = 0

    previous_frame = None

    motion_detected = False

    # Loop through frames from the stream
    while True:
        # Read a frame
        ret, frame = cap.read()


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
            diff_frame = cv2.dilate(diff_frame, kernel, 1)

            # 5. Only take different areas that are different enough (>20 / 255)
            thresh_frame = cv2.threshold(src=diff_frame, thresh=100, maxval=255, type=cv2.THRESH_BINARY)[1]
            
            # Calculate the mean pixel value of the thresholded difference frame
            mean_val = np.mean(thresh_frame)
        
            # Set the motion threshold
            motion_threshold = 0.1

            # Check if the mean pixel value is above the motion threshold
            if mean_val > motion_threshold:
                motion_detected = True
                print("Motion detected!")
    

        # Do something with the frame, for example display it

        # Wait for key press or exit
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the VideoCapture object and close the window
    cap.release()
    cv2.destroyAllWindows()