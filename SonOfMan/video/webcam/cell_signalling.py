from flask import Flask, jsonify, request
import threading
import time

app = Flask(__name__)

# To store the ICE candidates received from the hosts
candidates = {}

@app.route('/report_ice_candidate', methods=['POST'])
def report_ice_candidate():
    data = request.json
    host_id = data.get('host_id')
    candidate = data.get('candidate')
    
    if not host_id or not candidate:
        return jsonify(status='failed', message='host_id and candidate required'), 400
    
    # Store the candidate along with the current timestamp
    candidates[host_id] = {'candidate': candidate, 'timestamp': time.time()}
    
    return jsonify(status='success', message='Candidate saved successfully')

@app.route('/get_ice_candidates', methods=['GET'])
def get_ice_candidates():
    # Return the candidates without the timestamp
    return jsonify({k: v['candidate'] for k, v in candidates.items()})

def cleanup_candidates():
    while True:
        current_time = time.time()
        # Remove candidates older than 3600 seconds (1 hour)
        keys_to_delete = [key for key, value in candidates.items() if current_time - value['timestamp'] > 3600]
        for key in keys_to_delete:
            candidates.pop(key, None)
        # Sleep for a while before the next cleanup
        time.sleep(60)

if __name__ == '__main__':
    # Start a background thread for candidate cleanup
    cleanup_thread = threading.Thread(target=cleanup_candidates, daemon=True)
    cleanup_thread.start()
    
    app.run(debug=True, port=5000)
