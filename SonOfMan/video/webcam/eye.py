import asyncio
import reflex_node

class Eye(reflex_node.ReflexNode):
    pass

async def main():
    eye_instance = Eye()
    await eye_instance.connectToReflexPathway()
    await asyncio.Future()  # Keeps the connection open

if __name__ == "__main__":
    asyncio.run(main())