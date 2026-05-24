# persistent_client.py
# WebSocket client that maintains a persistent connection
import asyncio
import websockets
import json
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def listen_forever():
    uri = "wss://echo.websocket.org"

    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        print("Connected to server")

        # Continuous message loop - runs until connection closes
        async for message in websocket:
            # Parse JSON messages (common format for WebSocket APIs)
            data = json.loads(message)
            print(f"Received: {data}")

            # Handle different message types
            if data.get("type") == "ping":
                # Respond to server pings to keep connection alive
                await websocket.send(json.dumps({"type": "pong"}))
            elif data.get("type") == "update":
                # Process update messages
                await process_update(data)


async def process_update(data):
    """Handle update messages from the server"""
    print(f"Processing update: {data.get('payload')}")


asyncio.run(listen_forever())
