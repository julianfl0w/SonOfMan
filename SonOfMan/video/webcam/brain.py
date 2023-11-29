import uuid
import asyncio
import reflex_node

class Brain(reflex_node.ReflexNode):
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