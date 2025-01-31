import asyncio
import aiohttp
import time

async def get_notes(url):
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url)
                if response.status == 200:
                    print("GET request successful")
                    # Process the response data if needed
                    print(await response.json())
                else:
                    print("GET request failed with status code:", response.status)
        except aiohttp.ClientError as e:
            print("GET request failed:", e)

        await asyncio.sleep(2)  # Delay for 5 seconds before sending the next request

async def main():
    urls = ["http://localhost:8002/notes/", "http://localhost:8002/notes/32"]  # Replace with your desired URLs

    tasks = []
    for url in urls:
        task = asyncio.create_task(get_notes(url))
        tasks.append(task)

    await asyncio.gather(*tasks)

# Run the main function
asyncio.run(main())
