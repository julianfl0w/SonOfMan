from flask import Flask, Response, stream_with_context
import subprocess

app = Flask(__name__)

VIDEO_SOURCE = '/dev/video0'  # Webcam device

def generate():
    
    # Command to capture video and audio from webcam and stream as h264 over stdout
    cmd = [
        'ffmpeg',
        '-i', VIDEO_SOURCE,             # Input device
        '-f', 'h264',                   # Output format
        '-vcodec', 'libx264',           # Video codec
        '-acodec', 'aac',               # Audio codec
        '-strict', '-2',                # Required for certain audio codecs
        '-preset', 'ultrafast',         # Preset
        '-tune', 'zerolatency',         # Tune
        '-pix_fmt', 'yuv420p',          # Pixel format
        '-movflags', 'frag_keyframe+empty_moov',  # Required for streaming
        'pipe:1'                        # Output to stdout
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for err_line in iter(proc.stderr.readline, b''):
        print(err_line.decode('utf-8'), end='')


@app.route('/')
def video_feed():
    return Response(stream_with_context(generate()), content_type='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
