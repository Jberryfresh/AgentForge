from fastapi import WebSocket
from typing import Dict


class Hub:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}

    async def register(self, agent_id: str, ws: WebSocket):
        await ws.accept()
        self.connections[agent_id] = ws

    def unregister(self, agent_id: str):
        self.connections.pop(agent_id, None)

    async def send(self, agent_id: str, message: dict):
        ws = self.connections.get(agent_id)
        if ws:
            await ws.send_json(message)


# single shared hub instance
hub = Hub()

