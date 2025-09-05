from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as api_router
from .core.config import settings
from .core.hub import hub  # import the shared hub
from .api.a2a import router as a2a_router  # import the new A2A route
from .api.llm import api as llm_api

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
            recipient = data.get("to")
            if recipient:
                # Relay the message to the intended recipient
                await hub.send(recipient, {"from": agent_id, "data": data.get("data")})
            else:
                # Acknowledge receipt if no target
                await ws.send_json({"ack": True})
    except WebSocketDisconnect:
        hub.unregister(agent_id)

# Mount existing routes
app.include_router(api_router)
# Mount the new A2A route
app.include_router(a2a_router)
app.include_router(llm_api)
