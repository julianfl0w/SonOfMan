import uuid
import asyncio
import SonOfMan.video.webcam.rtc_node as rtc_node

class Brain(rtc_node.RTCNode):
    pass

async def main():
    brain_instance = Brain()
    try:
        await brain_instance.connectToReflexPathway()
        await brain_instance.sendOffer()
        await asyncio.Future()

    finally:
        await brain_instance.sio.disconnect()

if __name__ == "__main__":
    asyncio.run(main())