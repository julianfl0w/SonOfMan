import stun
import uuid
import json
import asyncio
import constants
import socketio

from aiortc import (
    RTCPeerConnection, 
    RTCConfiguration, 
    RTCIceServer, 
    RTCSessionDescription,
    RTCIceCandidate  # import RTCIceCandidate
)

class ReflexNode:
    def __init__(self):
        self.connections = []

        #self.pc = RTCPeerConnection(configuration=RTCConfiguration())

        mac_num = uuid.getnode()
        mac_address = ':'.join(('%012X' % mac_num)[i:i+2] for i in range(0, 12, 2))
        self.host_id = mac_address

        self.server_url = "localhost:5000"

    async def handle_offer(self, message):
        print(f"Received answer")
        answer_json = json.loads(message)
        
        # Create a new dictionary without the 'host_sid' key
        new_dict = {key: value for key, value in answer_json.items() if key != 'host_sid'}

        # Create RTCSessionDescription from JSON
        answer_sdp = RTCSessionDescription(**new_dict)

        await self.pc.setRemoteDescription(answer_sdp)
        print("Set remote description successfully")

    async def handle_answer(self, message):
        print(f"Received answer")
        answer_json = json.loads(message)
        
        # Create a new dictionary without the 'host_sid' key
        new_dict = {key: value for key, value in answer_json.items() if key != 'host_sid'}

        # Create RTCSessionDescription from JSON
        answer_sdp = RTCSessionDescription(**new_dict)

        await self.pc.setRemoteDescription(answer_sdp)
        print("Set remote description successfully")

    async def handle_disconnect(self):
        print(f"Received SIO disconnect")
        await self.sio.disconnect()
        if hasattr(self, "pc"):
            await self.pc.close()

    async def connectToPeer(self):

        self.data_channel = self.pc.createDataChannel("dummyChannel")
        @self.data_channel.on("open")
        def on_open():
            print("Data channel is open")
            self.data_channel.send("hello world")

        @self.data_channel.on("message")
        def on_message(message):
            print(f"Received message: {message}")


        self.pc = RTCPeerConnection()
        # create_offer_and_gather_candidates
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        print("Local desc set")
        print(f"Gathered SDP:\n{offer}")

        # report_ice_candidate_to_server
        #print(offer.sdp)
        offerDict = dict(host_id = self.host_id, sdp = offer.sdp, type = offer.type)
        await self.sio.emit('offer', json.dumps(offerDict), namespace='/connect')

        # Keep the connection open
        await asyncio.Future()  # This will keep the connection open indefinitely



    async def connectToReflexPathway(self):

        try:
            # connect to server
            self.sio = socketio.AsyncClient()

            # listen for messages from server
            #self.sio.on('offer', self.handle_offer, namespace='/connect')
            self.sio.on('answer', self.handle_answer, namespace='/connect')
            self.sio.on('disconnect', self.handle_disconnect, namespace='/connect')
            self.sio.on('candidates', self.chooseCandidate, namespace='/connect')

            await self.sio.connect("http://localhost:5000", namespaces=['/connect'])

            await asyncio.Future()

        finally:
            await self.sio.disconnect()

    async def connectToPeer(self, remote_sid, candidate):
        pc = RTCPeerConnection()
        pc_id = "PeerConnection"

        # Set up a handler for the "datachannel" event
        @pc.on("datachannel")
        def on_datachannel(channel):
            print("Data channel received")
            
            @channel.on("open")
            def on_open():
                print("Data channel is open")

            @channel.on("message")
            def on_message(message):
                print(f"Received message: {message}")

        remote_offer = RTCSessionDescription(sdp=candidate['sdp'], type=candidate['type'])
        await pc.setRemoteDescription(remote_offer)
        print("Remote description set")
        
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        print("Local description set")

        print(f"{pc_id} Created answer")
        
        message = dict(host_sid = remote_sid,  sdp = answer.sdp, type = answer.type)
        await self.sio.emit('answer', json.dumps(message), namespace='/connect')
        print(f"Answer sent")

    async def chooseCandidate(self, offer):
        print("Received candidates")
        offerDict = json.loads(offer)
        if offerDict:
            remote_sid, candidate = list(offerDict.items())[0]
            print(f"offer {remote_sid}")
            #await self.sio.emit('message', json.dumps({"request":"remote_sid", "remote_sid" : remote_sid}), namespace='/connect')
            await self.connectToPeer(remote_sid, candidate)
