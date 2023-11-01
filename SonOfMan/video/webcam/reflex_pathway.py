from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import constants

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

candidates = {}
connected_hosts = set()

@socketio.on('connect', namespace='/brain_connect')
def handle_brain_connect():
    print("Client connected to /brain_connect")

@socketio.on('disconnect', namespace='/brain_connect')
def handle_brain_disconnect():
    print("Client disconnected from /brain_connect")
    for host_id in connected_hosts:
        candidates.pop(host_id, None)
    connected_hosts.clear()

@socketio.on('message', namespace='/brain_connect')
def handle_brain_message(message):
    print(f"Received on /brain_connect: {message}")

    try:
        data = json.loads(message)
        host_id = data.get('host_id')
        candidate = data.get('candidate')

        if not host_id or not candidate:
            emit('message', {'status': 'failed', 'message': 'host_id and candidate required'})
            return

        candidates[host_id] = {'candidate': candidate}
        connected_hosts.add(host_id)
        emit('message', {'status': 'success', 'message': 'Candidate saved successfully'})
    except json.JSONDecodeError:
        emit('message', {'status': 'failed', 'message': 'Invalid JSON'})

@socketio.on('connect', namespace='/eye_connect')
def handle_eye_connect():
    print("Client connected to /eye_connect")
    # send list of ice candidates on connect
    emit('message', {'candidates': {k: v['candidate'] for k, v in candidates.items()}})

@socketio.on('disconnect', namespace='/eye_connect')
def handle_eye_disconnect():
    print("Client disconnected from /eye_connect")

@socketio.on('message', namespace='/eye_connect')
def handle_eye_message(message):
    print(f"Received on /eye_connect: {message}")

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
