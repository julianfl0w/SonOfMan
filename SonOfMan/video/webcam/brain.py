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

import reflex_node

class Brain(reflex_node.ReflexNode):
    pass

async def main():
    brain_instance = Brain()
    await brain_instance.connectToReflexPathway()
    await asyncio.Future()  # Keeps the connection open

if __name__ == "__main__":
    asyncio.run(main())