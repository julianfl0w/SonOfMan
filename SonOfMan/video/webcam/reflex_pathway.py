from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import constants
from flask import request

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

brains = {}

import multiprocessing as mp
import brain


@socketio.on('connect', namespace='/brain_connect')
def handle_brain_connect():
    print("Client connected to /brain_connect")

@socketio.on('disconnect', namespace='/brain_connect')
def handle_brain_disconnect():
    sid = request.sid  # Access the session ID of the disconnected client
    print(f"Client disconnected from /brain_connect with session ID {sid}")
    brains.pop(sid, None)  # Remove the candidate associated with the disconnected session

@socketio.on('offer', namespace='/brain_connect')
def handle_brain_message(message):
    print(f"Received brain connect offer")

    offer = json.loads(message)

    host_id = offer.get('host_id')
    sdp = offer.get('sdp')

    if not host_id or not sdp:
        emit('failure', 'host_id and sdp required')
        return

    brains[request.sid] = json.loads(message)
    emit('success', 'Candidate saved successfully')

@socketio.on('connect', namespace='/eye_connect')
def handle_eye_connect():
    print("Client connected to /eye_connect")

@socketio.on('disconnect', namespace='/eye_connect')
def handle_eye_disconnect():
    print("Client disconnected from /eye_connect")

@socketio.on('candidates', namespace='/eye_connect')
def handle_candidates(message):
    print(f"Received candidates")
    #message = json.loads(message)
    # send list of ice candidates on connect
    #print(brains)
    emit('candidates', json.dumps(brains))
    print("Candidates sent")

@socketio.on('answer', namespace='/eye_connect')
def handle_answer(answer):
    print(f"Received answer")
    answer = json.loads(answer)

    # Placeholder for updating the peer connection with the answer
    # This typically involves fetching the peer connection object for the given client
    # and setting the answer on it.
    print("-----------------")
    host_sid = answer['host_sid']
    print(host_sid)
    # Fetch the peer connection object for the given client
    # This is a placeholder, replace with your actual logic to get the peer connection
    peer_connection = brains.get(host_sid)

    if peer_connection:
        # Here you would typically set the answer on the peer connection
        # Since this is highly dependent on your WebRTC setup, replace with your actual logic
        # For example: peer_connection.setRemoteDescription(answer)

        # Emit a message to the specific client identified by host_sid
        # to inform them that the answer has been processed and any further steps if needed
        emit('answer', json.dumps(answer), to=host_sid, namespace='/brain_connect')

        # Signal back to the client who sent the answer if needed
        emit('status', json.dumps({'status': 'success', 'message': 'Answer processed successfully'}))
    else:
        emit('status', json.dumps({'status': 'failed', 'message': 'Peer connection not found'}), to=host_sid, namespace='/brain_connect')


if __name__ == '__main__':
    # Create a new process targeting brain.main
    #process = mp.Process(target=brain.main)
    # Start the process
    #process.start()

    socketio.run(app, debug=False, port=5000) 
