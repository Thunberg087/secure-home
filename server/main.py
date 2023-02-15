
import flask
import motion_detector as md
from camera import Camera
from flask_cors import CORS

# Replace the URL with your IP camera stream URL
# url = 'rtsp://admin:admin@192.168.0.104:554/11'
# url = 'vid.mp4'
cameras: list[Camera] = []


app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/stream')
def getStream():
    cameraId = flask.request.args.get('camera-id')
    for cam in cameras:
        if cam.id == cameraId:
            return flask.Response(cam.get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
    return "Could not find camera", 400   



@app.get('/cameras')
def getCameras():
    def mapper(cam: Camera):
        send_cam = {
            "id": cam.id,
            "name": cam.name,
        }
        return dict(send_cam)
    
    return list(map(mapper, cameras))



@app.post('/cameras')
def addCamera():
    data = flask.request.get_json()
        
    if not len(data["cameraName"]) > 0:
        return "Camera name not provided", 400
    
    if not len(data["cameraURL"]) > 0:
        return "Camera URL not provided", 400
    
    
    if any(cam.stream_url == data["cameraURL"] for cam in cameras):
        return  "Camera already added", 400

    if any(cam.name == data["cameraName"] for cam in cameras):
        return  "Camera name already used", 400


    cam = Camera(data["cameraName"], data["cameraURL"])
    

    if cam.is_connected() == True:
        cameras.append(cam)
        return "Added camera"
    else:
        return  "No camera connection", 400
        
 



if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, threaded=True)