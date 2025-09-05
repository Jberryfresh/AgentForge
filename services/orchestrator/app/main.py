from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as api_router
from .core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory WS hub (MVP)
class Hub:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def register(self, agent_id: str, ws: WebSocket):
        await ws.accept()
        self.connections[agent_id] = ws

    def unregister(self, agent_id: str):
        self.connections.pop(agent_id, None)

    async def send(self, agent_id: str, message: dict):
        ws = self.connections.get(agent_id)
        if ws:
            await ws.send_json(message)

hub = Hub()

@app.websocket("/ws/agents/{agent_id}")
async def agent_socket(ws: WebSocket, agent_id: str):
    await hub.register(agent_id, ws)
    try:
        while True:
            data = await ws.receive_json()
            target = data.get("to")
            if target:
                await hub.send(target, {"from": agent_id, "data": data.get("data")})
            else:
                await ws.send_json({"ack": True})
    except WebSocketDisconnect:
        hub.unregister(agent_id)

# Mount REST routes
app.include_router(api_router, prefix="")
