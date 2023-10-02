import cv2
from flask import Flask, Response

app = Flask(__name__)

# Open the webcam
camera = cv2.VideoCapture('/dev/video0')

def generate():
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        
        # Encode frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
