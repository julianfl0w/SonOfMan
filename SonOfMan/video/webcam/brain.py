import stun
import uuid
import json
import asyncio
import constants
import socketio

from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceServer

class Brain:
    def __init__(self):
        self.pc = RTCPeerConnection(configuration=RTCConfiguration())
        self.data_channel = self.pc.createDataChannel("dummyChannel")

        mac_num = uuid.getnode()
        mac_address = ':'.join(('%012X' % mac_num)[i:i+2] for i in range(0, 12, 2))
        self.host_id = mac_address

        self.ws_url = "http://localhost:5000"
        self.sio = socketio.AsyncClient()

    async def on_message(self, data):
        print(f"Received message: {data}")
        # TODO: Handle ICE candidates received from server

    async def start(self):
        # create_offer_and_gather_candidates
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        sdp = self.pc.localDescription.sdp
        print(f"Gathered SDP:\n{sdp}")

        # connect to server
        await self.sio.connect(self.ws_url, namespaces=['/brain_connect'])
        
        # listen for messages from server
        self.sio.on('message', self.on_message, namespace='/brain_connect')

        # report_ice_candidate_to_server
        data = {'host_id': self.host_id, 'candidate': sdp}
        await self.sio.emit('message', json.dumps(data), namespace='/brain_connect')

        # TODO: Handle ICE candidate gathering

        # Keep the connection open
        await asyncio.Future()  # This will keep the connection open indefinitely

    async def stop(self):
        await self.sio.disconnect()
        await self.pc.close()

if __name__ == "__main__":
    brain_instance = Brain()
    asyncio.run(brain_instance.start())
