import asyncio
import websockets
import json


async def main():
    uri = "ws://localhost:8000/ws/agents/agentB"
    async with websockets.connect(uri) as websocket:
        while True:
            msg = json.loads(await websocket.recv())
            print("AgentB received:", msg)
            # Reply if message came from agentA
            if msg.get("from") == "agentA":
                await websocket.send(json.dumps({"to": "agentA", "data": {"reply": "hi from B"}}))


asyncio.run(main())

