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
        self.sio.on('candidates', self.handle_candidates, namespace='/eye_connect')

        # send the request for candidates
        await self.sio.emit('candidates', "", namespace='/eye_connect')


    async def handle_candidates(self, offer):
        print("Received candidates")
        offerDict = json.loads(offer)
        if offerDict:
            sid, candidate = list(offerDict.items())[0]
            await self.sio.emit('message', json.dumps({"request":"sid", "sid" : sid}), namespace='/eye_connect')
            await self.create_peer_connection(sid, candidate)

    async def create_peer_connection(self, sid, candidate):
        pc = RTCPeerConnection()
        pc_id = "PeerConnection"
        sdp = candidate['sdp']
        remote_offer = RTCSessionDescription(sdp=sdp, type="offer")
        await pc.setRemoteDescription(remote_offer)
        print("Remote description set")
        
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        print("Local description set")

        print(f"{pc_id} Created answer")
        
        message = dict(host_sid = sid,  sdp = answer.sdp, type = answer.type)
        await self.sio.emit('answer', json.dumps(message), namespace='/eye_connect')
        print(f"Answer sent")

async def main():
    eye_instance = Eye()
    await eye_instance.setup()
    await asyncio.Future()  # Keeps the connection open

if __name__ == "__main__":
    asyncio.run(main())