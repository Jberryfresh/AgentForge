from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.hub import hub

router = APIRouter()


class RouteMessage(BaseModel):
    sender: str
    recipient: str
    data: dict | str


@router.post("/route")
async def route_message(msg: RouteMessage):
    if msg.recipient not in hub.connections:
        raise HTTPException(status_code=404, detail=f"{msg.recipient} not connected")
    await hub.send(msg.recipient, {"from": msg.sender, "data": msg.data})
    return {"success": True}

