import asyncio
import SonOfMan.video.webcam.rtc_node as rtc_node

class Eye(rtc_node.RTCNode):
    pass

async def main():
    eye_instance = Eye()
    await eye_instance.connectToReflexPathway()
    await asyncio.Future()  # Keeps the connection open

if __name__ == "__main__":
    asyncio.run(main())