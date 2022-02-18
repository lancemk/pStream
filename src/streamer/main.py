
# python syntax to import from relative package
# from RELATIVE_FOLDER_NAME import CLASS_NAME

# Method1
from flask import Flask, render_template, Response
import pathlib
import cv2

# Method2 - [simple way for mjpeg in flask](https://tree.rocks/a-simple-way-for-motion-jpeg-in-flask-806b8bfefa96)
# it's laggy, frame by frame cause fix 1sec interval 
# import time
# import numpy as np
# import matplotlib.pyplot as plt

# from encoder import Camera

BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

#Initialize the Flask app
app = Flask(__name__)

def gen_frames(id):

    # for hardware disconnection, auto reconnect required approx 25sec after rtsp stream recovered 
    if (id == '1'): vc = cv2.VideoCapture("rtsp://admin:common123@192.168.80.79:554/substream latency=100 ! rtph264depay")
    if (id == '2'): vc = cv2.VideoCapture("rtsp://admin:common123@192.168.80.79:554/substream latency=100 ! rtph264depay")
    # if (id == '1'): vc = cv2.VideoCapture("rtsp://admin:common123@192.168.80.79:554 latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink max-buffers=1 drop=true")
    
    # if (id == '168'): vc = cv2.VideoCapture("rtsp://admin:aaaa1111@192.192.11.168:554")  # aegis      
    # if (id == '178'): vc = cv2.VideoCapture("rtsp://192.192.11.178:554") # aegis drone  

    while True:
        success, frame = vc.read()
        if not success:
            yield 'Frames retrive unsuccessful'
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame) # this is working
            # _, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' 
                    b'Content-Type: image/jpeg\r\n\r\n' + frame  + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/video_feed/<id>')
def video_feed(id):
    return Response(gen_frames(id), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001', threaded=True)