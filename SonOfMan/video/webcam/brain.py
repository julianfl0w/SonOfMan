import stun
import uuid
import json
import asyncio
import constants
import socketio

from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceServer, RTCSessionDescription

class Brain:
    def __init__(self):
        self.pc = RTCPeerConnection(configuration=RTCConfiguration())
        self.data_channel = self.pc.createDataChannel("dummyChannel")

        mac_num = uuid.getnode()
        mac_address = ':'.join(('%012X' % mac_num)[i:i+2] for i in range(0, 12, 2))
        self.host_id = mac_address

        self.ws_url = "http://localhost:5000"
        self.sio = socketio.AsyncClient()

    async def handle_answer(self, message):
        print(f"Received answer")
        answer_json = json.loads(message)
        
        # Create a new dictionary without the 'host_sid' key
        new_dict = {key: value for key, value in answer_json.items() if key != 'host_sid'}


        # Create RTCSessionDescription from JSON
        answer_sdp = RTCSessionDescription(**new_dict)

        await self.pc.setRemoteDescription(answer_sdp)
        print("Set remote description successfully")

    async def start(self):
        # create_offer_and_gather_candidates
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        #print(f"Gathered SDP:\n{offer}")

        # connect to server
        await self.sio.connect(self.ws_url, namespaces=['/brain_connect'])
        
        # listen for messages from server
        self.sio.on('answer', self.handle_answer, namespace='/brain_connect')

        # report_ice_candidate_to_server
        offerDict = dict(host_id = self.host_id, sdp = offer.sdp, type = offer.type)
        await self.sio.emit('offer', json.dumps(offerDict), namespace='/brain_connect')

        # Keep the connection open
        await asyncio.Future()  # This will keep the connection open indefinitely

    async def stop(self):
        await self.sio.disconnect()
        await self.pc.close()

def main():
    brain_instance = Brain()
    asyncio.run(brain_instance.start())

if __name__ == "__main__":
    main()
