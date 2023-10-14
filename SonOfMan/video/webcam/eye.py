import aiohttp
import asyncio
import json 

async def fetch_ice_candidates(server_url):
    """
    Fetch ICE candidates from the server.

    :param server_url: str, The server URL
    :return: dict, The ICE candidates
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{server_url}/get_ice_candidates') as response:
            if response.status == 200:
                ice_candidates = await response.json()
                return ice_candidates
            else:
                print(f"Failed to fetch ICE candidates: {response.status}")
                return None

async def main():
    server_url = "http://localhost:5000"  # Replace with your server URL
    ice_candidates = await fetch_ice_candidates(server_url)
    if ice_candidates is not None:
        print(f"ICE Candidates: {ice_candidates}")
        print(ice_candidates)

# To run the async function
if __name__ == "__main__":
    asyncio.run(main())
