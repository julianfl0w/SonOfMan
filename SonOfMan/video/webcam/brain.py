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

        self.main_task = asyncio.run(self.main())

        return 

    async def on_message(self, data):
        print(f"Received message: {data}")

    async def main(self):
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

        # wait for some time to ensure message is received
        await asyncio.sleep(5)

        # disconnect after receiving the message
        await self.sio.disconnect()

if __name__ == "__main__":
    brain_instance = Brain()
