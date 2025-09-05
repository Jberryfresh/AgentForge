from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as api_router
from .core.config import settings
from .core.hub import hub  # import the shared hub
from .api.a2a import router as a2a_router  # import the new A2A route

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws/agents/{agent_id}")
async def agent_socket(ws: WebSocket, agent_id: str):
    await hub.register(agent_id, ws)
    try:
        while True:
            data = await ws.receive_json()
            to = data.get("to")
            if to:
                # Relay the message to the intended recipient
                await hub.send(to, {"from": agent_id, "data": data.get("data")})
            else:
                # Acknowledge receipt if no target
                await ws.send_json({"ack": True})
    except WebSocketDisconnect:
        hub.unregister(agent_id)

# Mount existing routes
app.include_router(api_router)
# Mount the new A2A route
app.include_router(a2a_router)
