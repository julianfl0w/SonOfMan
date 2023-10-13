import stun
import uuid
import json
import requests
import asyncio

from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceServer

async def create_offer_and_gather_candidates(pc):
    # Create an offer and set it as local description to gather ICE candidates
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    return pc.localDescription.sdp

async def report_ice_candidate_to_server(host_id, candidate):
    # API endpoint URL
    url = "http://localhost:5000/report_ice_candidate"
    
    # Create a dictionary with the host_id and the candidate
    data = {'host_id': host_id, 'candidate': candidate}

    # Make HTTP POST request and send the JSON string
    response = requests.post(url, json=data)
    
    # Logging the response from the server
    print(f"Server Response: {response.text}")

async def main():
    rtc_config = RTCConfiguration()
    peer_connection = RTCPeerConnection(configuration=rtc_config)
    data_channel = peer_connection.createDataChannel("dummyChannel")
    
    # Generate a unique host_id using uuid
    host_id = str(uuid.uuid4())
    
    while True:
        sdp = await create_offer_and_gather_candidates(peer_connection)
        print(f"Gathered SDP:\n{sdp}")

        # Report the ICE candidate to the signaling server
        await report_ice_candidate_to_server(host_id, sdp)

        # Wait for 59 minutes before next report
        await asyncio.sleep(59*60)

if __name__ == "__main__":
    asyncio.run(main())
