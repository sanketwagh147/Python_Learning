# basic_client.py

# Simple WebSocket client that sends one message and receives a response
import asyncio
import websockets
import certifi
import ssl


async def hello():
    # Connect to WebSocket server using async context manager
    uri = "wss://echo.websocket.org"
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        # Send a message to the server
        await websocket.send("Hello, Server!")
        print("Sent: Hello, Server!")

        # Wait for and receive the response
        response = await websocket.recv()
        print(f"Received: {response}")


# Run the async function
asyncio.run(hello())
