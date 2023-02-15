import cv2
import numpy as np
import motion_detector as md
import flask 


# Replace the URL with your IP camera stream URL
url = 'rtsp://admin:admin@192.168.0.104:554/11'
# url = 'vid.mp4'

# Create a VideoCapture object to read from the stream
cap = cv2.VideoCapture(url)

# md.detect_motion(cap)

app = flask.Flask(__name__)

def get_frame():

    while True:
        retval, im = cap.read()
        imgencode=cv2.imencode('.jpg',im)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')


@app.route('/stream')
def vid():
     return flask.Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='localhost',port=5000, debug=True, threaded=True)