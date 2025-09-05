import asyncio
import websockets
import json


async def main():
    uri = "ws://localhost:8000/ws/agents/agentA"
    async with websockets.connect(uri) as websocket:
        # Send a message to agentB
        await websocket.send(json.dumps({"to": "agentB", "data": {"message": "hello from A"}}))
        # Listen for reply
        reply = await websocket.recv()
        print("AgentA received:", reply)


asyncio.run(main())

