import uuid
import json
import asyncio
import constants
import socketio
import dataclasses

from aiortc import (
    RTCPeerConnection, 
    RTCConfiguration, 
    RTCIceServer, 
    RTCSessionDescription,
    RTCIceGatherer,
    RTCIceCandidate  # import RTCIceCandidate,

)

class ReflexNode:
    def __init__(self):
        self.connections = []

        #self.pc = RTCPeerConnection(configuration=RTCConfiguration())

        mac_num = uuid.getnode()
        mac_address = ':'.join(('%012X' % mac_num)[i:i+2] for i in range(0, 12, 2))
        self.host_id = mac_address

        self.server_url = "localhost:5000"

    async def handle_status(self, message):
        print(f"Received status")
        answer_json = json.loads(message)
        print(answer_json)

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


    async def handleIce(self, event):
        print("ICE ICE BABY")
        if event.candidate:
            candidate_dict = dataclasses.asdict(event.candidate)
            # Send this candidate to the remote peer via signaling
            await self.sio.emit('ice_candidate', json.dumps(candidate_dict), namespace='/connect')

    async def sendOffer(self):

        self.pc = RTCPeerConnection()

        # Handle ICE candidates
        @self.pc.on("icecandidate")
        async def on_ice_candidate(event):
            await self.handleIce(event)

        self.data_channel = self.pc.createDataChannel("dummyChannel")
        @self.data_channel.on("open")
        def on_open():
            print("Data channel is open")
            self.data_channel.send("hello world")

        @self.data_channel.on("message")
        def on_message(message):
            print(f"Received message: {message}")

        # create_offer_and_gather_candidates
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        print("Local desc set")
        #print(f"Gathered SDP:\n{offer}")

        # report_ice_candidate_to_server
        #print(offer.sdp)
        offerDict = dict(host_id = self.host_id, sdp = self.pc.localDescription.sdp, type = self.pc.localDescription.type)
        await self.sio.emit('offer', json.dumps(offerDict), namespace='/connect')
        print("Offer Sent")

    async def sendAnswerAndConnect(self, remote_sid, candidate):
        pc = RTCPeerConnection()
        pc_id = "PeerConnection"

        # Handle ICE candidates
        @pc.on("icecandidate")
        async def on_ice_candidate(event):
            await self.handleIce(event)

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

        message = dict(host_sid = remote_sid,  sdp = pc.localDescription.sdp, type = pc.localDescription.type)
        await self.sio.emit('answer', json.dumps(message), namespace='/connect')
        print(f"Answer sent")

    async def connectToReflexPathway(self):

        # connect to server
        self.sio = socketio.AsyncClient()

        # listen for messages from server
        
        self.sio.on('status', self.handle_status, namespace='/connect')
        self.sio.on('answer', self.handle_answer, namespace='/connect')
        self.sio.on('disconnect', self.handle_disconnect, namespace='/connect')
        self.sio.on('candidates', self.chooseCandidate, namespace='/connect')

        await self.sio.connect("http://localhost:5000", namespaces=['/connect'])


    async def chooseCandidate(self, offer):
        print("Received candidates")
        offerDict = json.loads(offer)
        if offerDict:
            remote_sid, candidate = list(offerDict.items())[0]
            print(f"offer {remote_sid}")
            #await self.sio.emit('message', json.dumps({"request":"remote_sid", "remote_sid" : remote_sid}), namespace='/connect')
            await self.sendAnswerAndConnect(remote_sid, candidate)
        #await self.sio.disconnect()