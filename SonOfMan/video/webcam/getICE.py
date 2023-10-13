import stun
import uuid
import json
import requests
import asyncio

from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceServer


def getInventory():
    # Google's STUN server
    stun_host = "stun.l.google.com"
    stun_port = 19302  # default STUN port

    # Get the external IP and the NAT type
    nat_type, external_ip, external_port = stun.get_ip_info(stun_host=stun_host, stun_port=stun_port)

    mac_num = uuid.getnode()
    mac_address = ':'.join(('%012X' % mac_num)[i:i+2] for i in range(0, 12, 2))


    # Store all values in a dictionary
    network_info = {
        "NAT_Type": nat_type,
        "External_IP": external_ip,
        "External_Port": external_port,
        "MAC_Address": mac_address
    }

    return network_info

# Create the PeerConnection with the configuration
peer_connection = RTCPeerConnection()

def send_ice_candidate_to_signaling_server(candidate):
    message = {
        "type": "ice-candidate",
        "candidate": {
            "candidate": candidate.candidate,
            "sdpMid": candidate.sdpMid,
            "sdpMLineIndex": candidate.sdpMLineIndex
        }
    }
    response = requests.post("https://your-signaling-server/candidates", json=message)
    # Handle the response if needed


async def create_offer_and_gather_candidates(pc):
    # Create an offer and set it as local description to gather ICE candidates
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    return pc.localDescription.sdp

async def main():
    # Create the PeerConnection with the configuration
    rtc_config = RTCConfiguration()
    peer_connection = RTCPeerConnection(configuration=rtc_config)

    # Create a data channel; no need to do anything with it if you're only interested in ICE.
    data_channel = peer_connection.createDataChannel("dummyChannel")

    @peer_connection.on("icecandidate")
    async def on_ice_candidate(candidate):
        if candidate:
            await send_ice_candidate_to_signaling_server(candidate)

    # Use an event loop to run asynchronous function and gather candidates
    sdp = await create_offer_and_gather_candidates(peer_connection)

    # Here `sdp` is a string containing the Session Description Protocol information,
    # which you might send to the signaling server depending on your application logic.

    # You can print or log gathered candidates and SDP information if needed:
    print(f"Gathered SDP:\n{sdp}")

    # ... [you might want to do something with `sdp` here]

# Standard Python idiom to limit scope of variables and allow module-level script to be run
if __name__ == "__main__":
    print(json.dumps(getInventory(), indent=2))

    # Run the asynchronous main function using asyncio.run()
    asyncio.run(main())