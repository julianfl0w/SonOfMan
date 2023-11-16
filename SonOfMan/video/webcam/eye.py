import asyncio
import json
import socketio
from aiortc import RTCPeerConnection, RTCSessionDescription

class Eye:
    def __init__(self, server_url="localhost:5000"):
        self.server_url = server_url
        self.ws_url_eye = f"http://{self.server_url}/eye_connect"
        self.sio = socketio.AsyncClient()

    async def setup(self):
        await self.sio.connect(self.ws_url_eye, namespaces=['/eye_connect'])
        self.sio.on('message', self.on_message, namespace='/eye_connect')

        # report_ice_candidate_to_server
        data = {'request': "candidates"}
        await self.sio.emit('message', json.dumps(data), namespace='/eye_connect')


    async def on_message(self, data):
        print(f"Received data: {data}")
        ice_candidates = data.get('candidates')
        if ice_candidates:
            await self.create_peer_connection(ice_candidates)

    async def send_answer(self, answer):
        message = {'type': 'answer', 'answer': str(answer)}
        await self.sio.emit('message', json.dumps(message), namespace='/eye_connect')
        print(f"Answer sent: {message}")

    async def create_peer_connection(self, ice_candidates):
        pc = RTCPeerConnection()
        pc_id = "PeerConnection"
        print(ice_candidates)
        ice_candidate_str = list(ice_candidates.values())[0]
        remote_offer = RTCSessionDescription(sdp=ice_candidate_str, type="offer")
        await pc.setRemoteDescription(remote_offer)
        
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        print(f"{pc_id} Created answer")
        await self.send_answer(answer)

async def main():
    eye_instance = Eye()
    await eye_instance.setup()
    await asyncio.Future()  # Keeps the connection open

if __name__ == "__main__":
    asyncio.run(main())